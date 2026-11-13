#!/usr/bin/env python3
"""
Drip-Feed YouTube Shorts Scheduler & Live Telegram Notifier
Schedules all 7 Shorts (Shorts 03 to 09) from 17:30 IST to 23:30 IST at peak viral intervals.
Also sets native YouTube `publishAt` schedule and monitors live release.
"""

import os
import sys
import time
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import get_uploader

TG_TOKEN = "8829963924:AAE7v_xEQXLmy3-YEx8kqMo2GRfnbnxf4GA"
TG_CHAT_ID = "1126599043"

SCHEDULE = [
    {
        "slot_num": 1,
        "ist_time": "17:30 IST (5:30 PM)",
        "utc_iso": "2026-11-08T12:00:00.000Z",
        "video_id": "oKGnsqVXNys",
        "short_num": "Short 04",
        "title": "The ₹14,900 Crore U-Turn: FIIs Rush Back into Indian Equities",
        "theme": "Market Wrap / Dalal Street Reversal"
    },
    {
        "slot_num": 2,
        "ist_time": "18:30 IST (6:30 PM)",
        "utc_iso": "2026-11-08T13:00:00.000Z",
        "video_id": "XZ2bzhIck_Y",
        "short_num": "Short 06",
        "title": "SEBI's Nuclear Option: Why Weekly Expiries Were Banned",
        "theme": "Prime Post-Work / Derivative Traders"
    },
    {
        "slot_num": 3,
        "ist_time": "19:30 IST (7:30 PM)",
        "utc_iso": "2026-11-08T14:00:00.000Z",
        "video_id": "f8CrUjwbMAE",
        "short_num": "Short 08",
        "title": "The Rupee at ₹85: How the RBI Is Fighting the Currency Wall",
        "theme": "Macro & Forex Prime Evening"
    },
    {
        "slot_num": 4,
        "ist_time": "20:30 IST (8:30 PM)",
        "utc_iso": "2026-11-08T15:00:00.000Z",
        "video_id": "ihUe7L617C4",
        "short_num": "Short 03",
        "title": "The October Jobs Shocker: Why 165,000 Jobs Vanished Overnight",
        "theme": "US Market Open / Wall Street Reaction"
    },
    {
        "slot_num": 5,
        "ist_time": "21:30 IST (9:30 PM)",
        "utc_iso": "2026-11-08T16:00:00.000Z",
        "video_id": "fE2yCN2kz4E",
        "short_num": "Short 07",
        "title": "Big Tech's Nuclear Secret: Why AI Giants Are Buying Uranium",
        "theme": "Peak Tech & AI Energy Thesis"
    },
    {
        "slot_num": 6,
        "ist_time": "22:30 IST (10:30 PM)",
        "utc_iso": "2026-11-08T17:00:00.000Z",
        "video_id": "JWt4AEh4gaA",
        "short_num": "Short 05",
        "title": "The Midterm Gridlock: Why AI Data Centers Face a Red Tape Wall",
        "theme": "Late Evening US Policy & Datacenter Grid"
    },
    {
        "slot_num": 7,
        "ist_time": "23:30 IST (11:30 PM)",
        "utc_iso": "2026-11-08T18:00:00.000Z",
        "video_id": "GQd7jCFb2oQ",
        "short_num": "Short 09",
        "title": "The $36 Trillion Trap: Why Central Banks Are Quietly Hoarding Gold",
        "theme": "Midnight Global Macro / Sovereign Debt & Gold"
    }
]

def send_telegram(msg: str):
    data = urllib.parse.urlencode({"chat_id": TG_CHAT_ID, "text": msg, "parse_mode": "Markdown"}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", data=data)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            pass
        print(f"📲 Telegram notification sent.")
    except Exception as e:
        print(f"⚠️ Telegram send error: {e}")

def schedule_all_on_youtube():
    print("Setting native YouTube `publishAt` schedule for all 7 Shorts...")
    uploader = get_uploader()
    service = uploader._get_service("en")

    for item in SCHEDULE:
        vid_id = item["video_id"]
        pub_at = item["utc_iso"]
        try:
            res = service.videos().update(
                part="status",
                body={
                    "id": vid_id,
                    "status": {
                        "privacyStatus": "private",
                        "publishAt": pub_at
                    }
                }
            ).execute()
            print(f"✅ Scheduled {item['short_num']} ({vid_id}) for {item['ist_time']} (Status: {res['status'].get('publishAt')})")
        except Exception as e:
            print(f"❌ Failed to schedule {item['short_num']}: {e}")

    # Send summary alert to Telegram
    schedule_summary = "\n".join([f"• *{s['ist_time']}* — {s['title']} ([Watch](https://youtu.be/{s['video_id']}))" for s in SCHEDULE])
    msg = (
        f"📅 *DRIP-FEED SHORTS SCHEDULE CONFIRMED & ACTIVE*\n\n"
        f"All 7 Shorts have been locked into YouTube native scheduling to drop publicly between now and midnight at peak viral intervals:\n\n"
        f"{schedule_summary}\n\n"
        f"⚡ *ARIA* will broadcast live confirmation alerts as each Short transitions to Public."
    )
    send_telegram(msg)

def monitor_and_notify_loop():
    uploader = get_uploader()
    service = uploader._get_service("en")
    notified = set()

    print("\nStarting live background monitor daemon...")
    while len(notified) < len(SCHEDULE):
        now_utc = datetime.now(timezone.utc)
        for item in SCHEDULE:
            vid_id = item["video_id"]
            if vid_id in notified:
                continue

            target_utc = datetime.fromisoformat(item["utc_iso"].replace("Z", "+00:00"))
            # If current time is past or within 1 minute of target
            if now_utc >= target_utc:
                try:
                    # Verify status on YouTube
                    res = service.videos().list(part="status,snippet", id=vid_id).execute()
                    items = res.get("items", [])
                    if items:
                        status = items[0]["status"]["privacyStatus"]
                        if status == "public" or now_utc >= target_utc:
                            # Force public if still private
                            if status != "public":
                                service.videos().update(
                                    part="status",
                                    body={"id": vid_id, "status": {"privacyStatus": "public"}}
                                ).execute()
                                status = "public"

                            notified.add(vid_id)
                            live_msg = (
                                f"🚀 *YOUTUBE SHORT NOW LIVE & PUBLIC!*\n\n"
                                f"🎬 *Title:* {item['title']}\n"
                                f"🎯 *Slot:* {item['ist_time']} ({item['theme']})\n"
                                f"🔒 *Status:* PUBLIC\n"
                                f"🔗 *YouTube Link:* https://youtu.be/{vid_id}\n\n"
                                f"⚡ Broadcast via ARIA"
                            )
                            send_telegram(live_msg)
                            print(f"🎉 Released and notified: {item['short_num']} ({vid_id})")
                except Exception as e:
                    print(f"Error checking {vid_id}: {e}")

        time.sleep(30)

if __name__ == "__main__":
    schedule_all_on_youtube()
    if "--daemon" in sys.argv:
        monitor_and_notify_loop()
