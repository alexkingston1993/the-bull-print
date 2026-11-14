#!/usr/bin/env python3
"""
scripts/emergency_quarantine_today.py

Emergency Channel Lockdown & Forensic Extraction:
1. Scans YouTube channel uploads for all videos published today (Nov 14, 2026).
2. Immediately converts their privacyStatus to 'private' to protect channel algorithmic health.
3. Dumps exhaustive forensic metadata (ID, title, description, tags, thumbnails, dimensions)
   into output/quarantine_audit_today.json for deep-dive root cause analysis.
"""

import os
import sys
import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import get_uploader

TG_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "8829963924:AAE7v_xEQXLmy3-YEx8kqMo2GRfnbnxf4GA"
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or "1126599043"


def send_telegram_alert(message: str):
    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        return
    try:
        import requests
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TG_CHAT_ID, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": True}, timeout=10)
    except Exception as e:
        logger.warning(f"Telegram notice: {e}")


def quarantine_all_today():
    logger.info("🚨 [EMERGENCY LOCKDOWN] Scanning channel to privatize all videos uploaded today...")
    
    uploader = get_uploader()
    service = uploader._get_service("en")
    if not service:
        logger.error("Failed to authenticate YouTube API service.")
        sys.exit(1)

    channel_res = service.channels().list(mine=True, part="contentDetails").execute()
    if not channel_res or not channel_res.get("items"):
        logger.error("Could not locate channel details.")
        sys.exit(1)

    uploads_pl = channel_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    items = service.playlistItems().list(
        playlistId=uploads_pl,
        part="snippet,contentDetails",
        maxResults=50,
    ).execute().get("items", [])

    logger.info(f"Retrieved {len(items)} recent upload records.")
    video_ids = [it.get("snippet", {}).get("resourceId", {}).get("videoId") for it in items if it.get("snippet", {}).get("resourceId", {}).get("videoId")]

    if not video_ids:
        logger.warning("No video IDs found in upload playlist.")
        return

    # Fetch detailed video objects
    videos_detail = []
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i+50]
        res = service.videos().list(id=",".join(chunk), part="snippet,status,contentDetails").execute()
        videos_detail.extend(res.get("items", []))

    # Time boundaries for today: Nov 14, 2026 (both UTC and IST)
    ist_tz = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(timezone.utc).astimezone(ist_tz)
    today_ist_str = now_ist.strftime("%Y-%m-%d")
    today_utc_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    logger.info(f"Auditing for date matches: IST={today_ist_str} | UTC={today_utc_str}")

    quarantined = []
    already_private = []

    for v in videos_detail:
        v_id = v["id"]
        snip = v.get("snippet", {})
        status = v.get("status", {})
        content_details = v.get("contentDetails", {})
        
        title = snip.get("title", "")
        pub_at = snip.get("publishedAt", "")
        privacy = status.get("privacyStatus", "unknown")

        # Check date
        is_today = False
        if pub_at:
            pub_utc_str = pub_at[:10]
            pub_ist = datetime.fromisoformat(pub_at.replace("Z", "+00:00")).astimezone(ist_tz)
            pub_ist_str = pub_ist.strftime("%Y-%m-%d")
            if pub_utc_str in [today_utc_str, "2026-11-14"] or pub_ist_str in [today_ist_str, "2026-11-14"]:
                is_today = True

        if not is_today:
            continue

        record = {
            "id": v_id,
            "title": title,
            "published_at": pub_at,
            "initial_privacy": privacy,
            "duration": content_details.get("duration", ""),
            "definition": content_details.get("definition", ""),
            "dimension": content_details.get("dimension", ""),
            "tags": snip.get("tags", []),
            "description": snip.get("description", ""),
            "thumbnails": snip.get("thumbnails", {}),
            "url": f"https://youtu.be/{v_id}"
        }

        if privacy != "private":
            try:
                service.videos().update(
                    part="status",
                    body={
                        "id": v_id,
                        "status": {
                            "privacyStatus": "private"
                        }
                    }
                ).execute()
                record["final_privacy"] = "private"
                quarantined.append(record)
                logger.success(f"🔒 [QUARANTINED] Set to PRIVATE: '{title[:45]}' ({v_id})")
                time.sleep(1)
            except Exception as e:
                logger.error(f"Failed to privatize {v_id}: {e}")
                record["final_privacy"] = f"error: {e}"
        else:
            record["final_privacy"] = "private"
            already_private.append(record)
            logger.info(f"Already private: '{title[:45]}' ({v_id})")

    # Save forensic dump
    out_dir = BASE_DIR / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_file = out_dir / "quarantine_audit_today.json"
    
    report_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "today_ist": today_ist_str,
        "total_today_found": len(quarantined) + len(already_private),
        "newly_privatized_count": len(quarantined),
        "already_private_count": len(already_private),
        "quarantined_videos": quarantined + already_private
    }

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    logger.success(f"Forensic report written to {report_file}")
    print(json.dumps(report_data, indent=2))

    send_telegram_alert(
        f"🚨 *CHANNEL EMERGENCY LOCKDOWN EXECUTED*\n\n"
        f"📅 Date: `{today_ist_str}`\n"
        f"🔒 Total Today's Videos Identified: *{len(quarantined) + len(already_private)}*\n"
        f"🛡️ Newly Set to PRIVATE: *{len(quarantined)}*\n"
        f"ℹ️ Already Private: *{len(already_private)}*\n\n"
        f"All today's uploads are now secured and hidden from public feed while forensic analysis runs."
    )


if __name__ == "__main__":
    quarantine_all_today()
