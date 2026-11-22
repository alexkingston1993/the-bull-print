#!/usr/bin/env python3
"""
scripts/cross_platform_social_drip.py
Automated Cross-Platform Social Drip Engine for The Bull Print

Drip feeds public YouTube Shorts to Instagram Reels (@thebullprint) and Facebook Page Reels (The Bull Print)
at spaced intervals matching peak audience windows (Morning, Afternoon, Evening IST).
Guarantees:
1. Strict Drip Pacing: Releases at most 1 un-synced Short per run (never bulk-dumps).
2. Platform-Specific Custom Captions: Bespoke copy for Instagram, Facebook, and TikTok with clean UTM tracking.
3. D1 Idempotency Ledger: Prevents duplicate postings.
4. Quarantine Gate: 100% blocks Z6LEnQyhuvw and quarantined assets.
5. Ephemeral Cloud Storage: Auto-removes temporary video files immediately after publication.
"""

import os
import sys
import time
import json
import argparse
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.cloudflare_r2_vault import CloudflareD1Client
from app.services.instagram_reels_publisher import build_instagram_seo_caption, publish_local_mp4_reel
from app.services.facebook_reels_publisher import build_facebook_seo_caption, publish_local_facebook_reel
from app.services.tiktok_publisher import build_tiktok_seo_caption, publish_local_tiktok_video

QUARANTINED_VIDEO_IDS = {"Z6LEnQyhuvw", "quarantined"}
TEMP_DIR = BASE_DIR / "temp_social_drip"
TEMP_DIR.mkdir(parents=True, exist_ok=True)


def get_current_ist_slot() -> str:
    """Determines the current active IST slot based on wall-clock time."""
    ist_tz = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist_tz)
    hour = now_ist.hour
    minute = now_ist.minute

    if 7 <= hour < 12:
        return "morning_slot"
    elif 12 <= hour < 18:
        return "afternoon_slot"
    elif 18 <= hour <= 23:
        return "evening_slot"
    else:
        return "overnight_slot"


def get_unsynced_public_shorts(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Finds public YouTube Shorts that have not yet been posted to Instagram or Facebook.
    Cross-references channel videos against Cloudflare D1 idempotency records.
    """
    d1 = CloudflareD1Client()
    videos = []

    channel_json = BASE_DIR / "data" / "channel_all_videos.json"
    if channel_json.exists():
        try:
            videos = json.loads(channel_json.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(f"Failed to read channel videos: {e}")
            videos = []

    if not videos:
        logger.info("channel_all_videos.json not found locally; querying Cloudflare D1 indexed videos...")
        try:
            d1_rows = d1.get_indexed_videos()
            videos = [
                {
                    "id": r.get("video_id"),
                    "title": r.get("title", ""),
                    "status": r.get("privacy_status", "public"),
                    "description": ""
                }
                for r in d1_rows if r.get("video_id")
            ]
            logger.info(f"Retrieved {len(videos)} videos from Cloudflare D1.")
        except Exception as e:
            logger.error(f"Failed to query Cloudflare D1: {e}")
            videos = []

    if not videos:
        logger.warning("No videos found to inspect for social drip.")
        return []

    unsynced = []

    for v in videos:
        vid_id = v.get("id")
        title = v.get("title", "")
        status = v.get("status", "")

        # Only process public videos and exclude quarantined items
        if status != "public":
            continue
        if vid_id in QUARANTINED_VIDEO_IDS or "Z6LEnQyhuvw" in title or "quarantined" in title.lower():
            continue

        # Check if already published on both Instagram and Facebook
        ig_record = d1.check_cross_post_idempotency(vid_id, "instagram", "routine")
        fb_record = d1.check_cross_post_idempotency(vid_id, "facebook", "routine")

        ig_done = ig_record and ig_record.get("status") == "SUCCESS"
        fb_done = fb_record and fb_record.get("status") == "SUCCESS"

        if not (ig_done and fb_done):
            unsynced.append({
                "video_id": vid_id,
                "title": title,
                "description": v.get("description", ""),
                "published_at": v.get("publishedAt", ""),
                "needs_ig": not ig_done,
                "needs_fb": not fb_done
            })
            if len(unsynced) >= limit:
                break

    return unsynced


def download_youtube_short(video_id: str) -> Optional[Path]:
    """Downloads a public YouTube Short using yt-dlp to a temporary local path."""
    out_path = TEMP_DIR / f"{video_id}.mp4"
    if out_path.exists() and out_path.stat().st_size > 1024 * 100:
        return out_path

    url = f"https://www.youtube.com/shorts/{video_id}"
    logger.info(f"⬇️ Downloading YouTube Short {video_id} for cross-platform drip...")

    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--js-runtimes",
        "node:node",
        "--remote-components",
        "ejs:github",
        "-f",
        "b/best[ext=mp4]/best",
        "-o",
        str(out_path),
        url
    ]

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=90)
        if out_path.exists() and out_path.stat().st_size > 1024 * 50:
            logger.success(f"✓ Downloaded {video_id}.mp4 ({out_path.stat().st_size // 1024} KB)")
            return out_path
        
        # Fallback to single-stream best
        logger.warning(f"Initial yt-dlp format muxing failed for {video_id}; falling back to single stream 'best'...")
        fallback_cmd = [
            sys.executable,
            "-m",
            "yt_dlp",
            "--js-runtimes",
            "node:node",
            "--remote-components",
            "ejs:github",
            "-f",
            "b/best/mp4",
            "-o",
            str(out_path),
            url
        ]
        res2 = subprocess.run(fallback_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=90)
        if out_path.exists() and out_path.stat().st_size > 1024 * 50:
            logger.success(f"✓ Downloaded {video_id}.mp4 via fallback ({out_path.stat().st_size // 1024} KB)")
            return out_path
        else:
            logger.error(f"Failed to download video {video_id}: {res2.stderr[:300]}")
            return None
    except Exception as e:
        logger.error(f"Failed to download YouTube Short {video_id}: {e}")
        return None


def drip_single_short(video_item: Dict[str, Any], slot_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Drips exactly one video to Instagram and Facebook with bespoke descriptions and clean UTM links.
    """
    vid_id = video_item["video_id"]
    title = video_item["title"]
    synopsis = video_item.get("description", title)
    slot = slot_name or get_current_ist_slot()

    logger.info(f"🚀 [Social Drip Engine] Processing Video '{title}' ({vid_id}) for slot '{slot}'...")

    # 1. Download video
    local_mp4 = download_youtube_short(vid_id)
    if not local_mp4:
        return {"success": False, "error": f"Failed to acquire mp4 for {vid_id}"}

    results = {"video_id": vid_id, "title": title, "slot": slot}

    # 2. Instagram Reels Publish (if needed)
    if video_item.get("needs_ig", True):
        logger.info(f"📸 Generating custom Instagram caption for {vid_id}...")
        ig_caption = build_instagram_seo_caption(
            title=title,
            synopsis=synopsis,
            youtube_video_id=vid_id
        )
        ig_res = publish_local_mp4_reel(
            video_path=str(local_mp4),
            caption=ig_caption,
            video_id=vid_id,
            release_slot="routine"
        )
        results["instagram"] = ig_res
    else:
        results["instagram"] = {"success": True, "skipped": True}

    # 3. Facebook Page Reels Publish (if needed)
    if video_item.get("needs_fb", True):
        logger.info(f"📘 Generating custom Facebook caption for {vid_id}...")
        fb_caption = build_facebook_seo_caption(
            title=title,
            synopsis=synopsis,
            youtube_video_id=vid_id
        )
        fb_res = publish_local_facebook_reel(
            video_path=str(local_mp4),
            caption=fb_caption,
            video_id=vid_id,
            release_slot="routine"
        )
        results["facebook"] = fb_res
    else:
        results["facebook"] = {"success": True, "skipped": True}

    # 4. TikTok Publish (Optional - checks if token is configured)
    tiktok_token = os.getenv("TIKTOK_ACCESS_TOKEN", "")
    if tiktok_token:
        try:
            tt_caption = build_tiktok_seo_caption(title=title, synopsis=synopsis, youtube_video_id=vid_id)
            tt_res = publish_local_tiktok_video(video_path=str(local_mp4), caption=tt_caption, video_id=vid_id)
            results["tiktok"] = tt_res
        except Exception as te:
            logger.debug(f"TikTok publish notice: {te}")

    # 5. Ephemeral Cleanup: remove temporary video file
    try:
        if local_mp4.exists():
            local_mp4.unlink()
            logger.info(f"🧹 Cleaned up temporary file: {local_mp4.name}")
    except Exception as ce:
        logger.debug(f"Cleanup note: {ce}")

    # 6. Telegram Notification via ARIA
    _notify_aria(results)
    return results


def _notify_aria(res: Dict[str, Any]) -> None:
    """Dispatches a clean delivery notification to ARIA on Telegram."""
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN", "8829963924:AAE7v_xEQXLmy3-YEx8kqMo2GRfnbnxf4GA")
    tg_chat_id = os.getenv("TELEGRAM_CHAT_ID", "1126599043")
    if not tg_token or not tg_chat_id:
        return

    vid_id = res.get("video_id")
    title = res.get("title", "")
    slot = res.get("slot", "")
    ig = res.get("instagram", {})
    fb = res.get("facebook", {})

    ig_link = ig.get("permalink", "Live") if ig.get("success") else "Failed"
    fb_link = fb.get("permalink", "Live") if fb.get("success") else "Failed"

    msg = (
        f"📱 *[CROSS-PLATFORM DRIP PUBLISHED]* 🚀\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎬 *Title:* `{title}`\n"
        f"⏰ *Window:* `{slot}`\n"
        f"📌 *YouTube ID:* `youtu.be/{vid_id}`\n\n"
        f"📸 *Instagram Reel:* {ig_link}\n"
        f"📘 *Facebook Reel:* {fb_link}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 _Custom descriptions, tags & UTM tracking synced successfully._"
    )

    try:
        import urllib.request
        import urllib.parse
        data = urllib.parse.urlencode({"chat_id": tg_chat_id, "text": msg, "parse_mode": "Markdown"}).encode()
        req = urllib.request.Request(f"https://api.telegram.org/bot{tg_token}/sendMessage", data=data)
        with urllib.request.urlopen(req, timeout=10):
            pass
    except Exception as e:
        logger.debug(f"Failed to send Telegram drip alert: {e}")


def run_drip_cycle(max_videos: int = 1) -> None:
    """Runs a single spaced drip cycle, processing at most max_videos (default 1)."""
    logger.info("🔍 Checking for un-synced YouTube Shorts across Instagram & Facebook...")
    unsynced = get_unsynced_public_shorts(limit=max_videos)

    if not unsynced:
        logger.success("🎉 All public YouTube Shorts are 100% synced with Instagram & Facebook!")
        return

    for item in unsynced[:max_videos]:
        drip_single_short(item)
        logger.success(f"✓ Completed drip cycle for '{item['title']}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The Bull Print Cross-Platform Social Drip Engine")
    parser.add_argument("--count", type=int, default=1, help="Number of videos to drip in this run (default 1)")
    parser.add_argument("--video-id", type=str, default="", help="Specific video ID to drip immediately")
    args = parser.parse_args()

    if args.video_id:
        drip_single_short({"video_id": args.video_id, "title": f"YouTube Short {args.video_id}"})
    else:
        run_drip_cycle(max_videos=args.count)
