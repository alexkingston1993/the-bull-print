#!/usr/bin/env python3
"""
Automated Drip Engine for Trump Election YouTube Shorts
Channel: The Bull Print (@thebullprint)
Drips Shorts 02 through 10 at peak viral evening/night windows before midnight IST.
"""

import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

IST = timezone(timedelta(hours=5, minutes=30))

DRIP_SCHEDULE = [
    {
        "id": 6,
        "video_id": "fwNkXmnWaHo",
        "title": "Why Foreign Investors Dumped ₹1.2 Lakh Cr from Dalal Street",
        "release_ist": "2026-11-06 21:15:00",
    },
    {
        "id": 7,
        "video_id": "4rkbyVAi-pA",
        "title": "Drill Baby Drill: How Cheap Oil Saves India ₹1 Lakh Crore",
        "release_ist": "2026-11-06 21:55:00",
    },
    {
        "id": 8,
        "video_id": "qhtpW1OL3EE",
        "title": "Trump's Drug Price War: Massive Boom for Indian Pharma",
        "release_ist": "2026-11-06 22:35:00",
    },
    {
        "id": 9,
        "video_id": "UHq60qmTAA0",
        "title": "Sona Crash or Gold Boom? What Trump Means for Gold",
        "release_ist": "2026-11-06 23:15:00",
    },
    {
        "id": 10,
        "video_id": "XYyXJ-Zi1a4",
        "title": "The Adani-Trump Energy Axis: What You Weren't Told",
        "release_ist": "2026-11-06 23:45:00",
    },
]

def parse_ist(dt_str: str) -> datetime:
    naive = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    return naive.replace(tzinfo=IST)

def main():
    print("=" * 75)
    print("🚀 THE BULL PRINT: TONIGHT VIRAL DRIP SCHEDULER")
    print(f"Current Time (IST): {datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print("=" * 75)

    uploader = YouTubeUploader()
    srv = uploader._get_service("en")

    log_path = BASE_DIR / "output" / "trump_shorts" / "drip_schedule.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    for item in DRIP_SCHEDULE:
        target_time = parse_ist(item["release_ist"])
        now = datetime.now(IST)

        wait_seconds = (target_time - now).total_seconds()

        if wait_seconds > 0:
            print(f"\n⏳ Next up: Short #{item['id']:02d} - '{item['title']}'")
            print(f"   Scheduled For: {target_time.strftime('%I:%M %p IST')}")
            print(f"   Sleeping for {int(wait_seconds)} seconds (~{round(wait_seconds/60, 1)} mins)...")
            sys.stdout.flush()
            time.sleep(wait_seconds)

        # Fresh authenticated service call
        srv = uploader._get_service("en")

        # Release to PUBLIC
        print(f"\n⚡ RELEASING SHORT #{item['id']:02d}: {item['title']} to PUBLIC...")
        try:
            body = {
                "id": item["video_id"],
                "status": {
                    "privacyStatus": "public"
                }
            }
            res = srv.videos().update(part="status", body=body).execute()
            pub_status = res.get("status", {}).get("privacyStatus")
            url = f"https://youtu.be/{item['video_id']}"
            msg = f"[{datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S IST')}] LIVE: Short #{item['id']:02d} -> {url} (Status: {pub_status})"
            print(f"   🎉 SUCCESS: {msg}")
            with open(log_path, "a") as f:
                f.write(msg + "\n")
        except Exception as e:
            err_msg = f"[{datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S IST')}] ERROR releasing Short #{item['id']:02d} ({item['video_id']}): {e}"
            print(f"   ❌ {err_msg}")
            with open(log_path, "a") as f:
                f.write(err_msg + "\n")
        sys.stdout.flush()

    print("\n" + "=" * 75)
    print("🏆 ALL 10 SHORTS HAVE COMPLETED TONIGHT'S SCHEDULED VIRAL DRIP!")
    print("=" * 75)

if __name__ == "__main__":
    main()
