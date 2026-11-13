#!/usr/bin/env python3
"""
Overnight Automated Drip Engine for The Bull Print YouTube Shorts
Drips the curated viral financial shorts from 10:30 PM tonight (Nov 7) to 6:00 AM tomorrow (Nov 8 IST)
at high-converting viral engagement windows.
"""

import os
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

IST = timezone(timedelta(hours=5, minutes=30))

# Viral Schedule between now and tomorrow 6:00 AM IST
DRIP_SCHEDULE = [
    {
        "id": 1,
        "video_id": "jNijFuJHHQs",
        "title": "The $2.5 Trillion AI Crash: What Happened to Big Tech",
        "release_ist": "2026-11-07 22:30:00",
        "audience": "Prime US Morning (12:00 PM EST) + Indian Late Night Peak",
    },
    {
        "id": 2,
        "video_id": "6Bkxw6NaQAo",
        "title": "SEBI's Shock Move: 12.5% Tax Scrapped for Foreign Funds?",
        "release_ist": "2026-11-07 23:30:00",
        "audience": "Indian Late Night Doomscroll + US Midday Lunch Peak (1:00 PM EST)",
    },
    {
        "id": 3,
        "video_id": "PENDING_03",
        "title": "The October Jobs Shocker: Why 165,000 Jobs Broke Wall Street",
        "release_ist": "2026-11-08 01:00:00",
        "audience": "US Afternoon Trading Session (2:30 PM EST)",
    },
    {
        "id": 4,
        "video_id": "PENDING_04",
        "title": "The ₹14,900 Crore U-Turn: FIIs Rush Back to Dalal Street",
        "release_ist": "2026-11-08 02:15:00",
        "audience": "US Market Close Momentum (3:45 PM EST)",
    },
    {
        "id": 5,
        "video_id": "PENDING_05",
        "title": "The Midterm Gridlock: Why AI Data Centers Face Investigation",
        "release_ist": "2026-11-08 03:30:00",
        "audience": "US Post-Market Earnings & News Cycle (5:00 PM EST)",
    },
    {
        "id": 6,
        "video_id": "PENDING_06",
        "title": "SEBI's Nuclear Option: Why Weekly Expiries Are Being Banned",
        "release_ist": "2026-11-08 04:30:00",
        "audience": "Early European Pre-Market & US Evening Prime",
    },
    {
        "id": 7,
        "video_id": "PENDING_07",
        "title": "Big Tech's Nuclear Secret: Why AI Giants Are Buying Reactors",
        "release_ist": "2026-11-08 05:15:00",
        "audience": "Indian Early Morning Risers + US Late Evening",
    },
    {
        "id": 8,
        "video_id": "PENDING_08",
        "title": "The Rupee at ₹85: How the RBI Is Fighting a Global Currency War",
        "release_ist": "2026-11-08 05:45:00",
        "audience": "Indian Morning Commute & Breakfast News Peak",
    },
    {
        "id": 9,
        "video_id": "PENDING_09",
        "title": "The $36 Trillion Trap: Why Central Banks Are Hoarding Gold",
        "release_ist": "2026-11-08 06:00:00",
        "audience": "Dalal Street Pre-Market Opening Preparation (6:00 AM IST)",
    },
]

LOG_FILE = BASE_DIR / "output" / "shorts" / "overnight_drip.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log_event(msg: str):
    timestamp = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST")
    full_msg = f"[{timestamp}] {msg}"
    print(full_msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")

def parse_ist(dt_str: str) -> datetime:
    naive = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    return naive.replace(tzinfo=IST)

def publish_video(video_id: str, title: str) -> bool:
    if not video_id or video_id.startswith("PENDING"):
        log_event(f"⚠️ Video ID not yet uploaded for '{title}'. Skipping publication.")
        return False
    try:
        uploader = YouTubeUploader()
        srv = uploader._get_service("en")
        body = {
            "id": video_id,
            "status": {
                "privacyStatus": "public"
            }
        }
        res = srv.videos().update(part="status", body=body).execute()
        new_status = res.get("status", {}).get("privacyStatus")
        url = f"https://youtu.be/{video_id}"
        log_event(f"🚀 PUBLISHED TO PUBLIC: '{title}' -> {url} (Status: {new_status})")
        return True
    except Exception as e:
        log_event(f"❌ Failed to publish video {video_id}: {e}")
        return False

def main():
    log_event("=" * 70)
    log_event("🌙 OVERNIGHT SHORTS DRIP ENGINE ACTIVATED")
    log_event(f"Current Local Time: {datetime.now(IST).strftime('%Y-%m-%d %I:%M:%S %p %Z')}")
    log_event(f"Target Finish: 2026-11-08 06:00:00 AM IST")
    log_event("=" * 70)

    for item in DRIP_SCHEDULE:
        target_dt = parse_ist(item["release_ist"])
        now = datetime.now(IST)
        wait_seconds = (target_dt - now).total_seconds()

        if wait_seconds > 0:
            log_event(f"\n⏳ Next Scheduled Drip: Short #{item['id']:02d} - '{item['title']}'")
            log_event(f"   Target Time: {target_dt.strftime('%I:%M %p IST')} | Audience: {item['audience']}")
            log_event(f"   Sleeping for {int(wait_seconds)} seconds (~{round(wait_seconds/60, 1)} minutes)...")
            sys.stdout.flush()
            time.sleep(wait_seconds)

        # Time to publish
        log_event(f"⚡ Releasing Short #{item['id']:02d}: {item['title']}...")
        publish_video(item["video_id"], item["title"])

    log_event("=" * 70)
    log_event("🌅 OVERNIGHT DRIP FEED COMPLETE! All scheduled slots reached 6:00 AM IST.")
    log_event("=" * 70)

if __name__ == "__main__":
    main()
