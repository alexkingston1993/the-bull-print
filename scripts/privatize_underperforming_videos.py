#!/usr/bin/env python3
"""
Privatize Underperforming Channel Videos (scripts/privatize_underperforming_videos.py)
Channel: The Bull Print (@thebullprint)

Safely moves low-view, stale prototype tests (<40 views from October or <15 views)
and junk test uploads to 'private' status, keeping only top-tier Master Documentaries,
the scheduled Trump Shorts series, and proven high-performing videos.
"""

import sys
import time
from pathlib import Path
from typing import Set

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

# Whitelist: Master Documentaries & Active High-CTR Shorts that must NEVER be privatized
PERMANENT_WHITELIST: Set[str] = {
    # 12-Minute Investigative Master Documentaries
    "t30Zwep0L9s",  # Video #5: Health Insurance Claim Rejection Machine
    "MRaIL_-X3wA",  # Video #3: The Operator Syndicate
    "J2yXwOno1lA",  # Video #2: The ₹2,000 Crore Vault Heist (WazirX)
    "UWH9EJhDU9Q",  # Video #1: The ₹20 Lakh Barrier (SEBI Algorithms)
    "OwNPa-sz-2Q",  # Master: The $32 Billion Illusion (FTX & Alameda)

    # 10 Trump Election & Dalal Street Shorts Series
    "sXW3aekYFx8",  # Short 01 (Public & Live)
    "W0eARjv3IVE",  # Short 02 (In scheduled drip queue)
    "uCTA_6AuxfI",  # Short 03 (In scheduled drip queue)
    "5kTihclG_bw",  # Short 04 (In scheduled drip queue)
    "t1h7gZMGMUs",  # Short 05 (In scheduled drip queue)
    "fwNkXmnWaHo",  # Short 06 (In scheduled drip queue)
    "4rkbyVAi-pA",  # Short 07 (In scheduled drip queue)
    "qhtpW1OL3EE",  # Short 08 (In scheduled drip queue)
    "UHq60qmTAA0",  # Short 09 (In scheduled drip queue)
    "XYyXJ-Zi1a4",  # Short 10 (In scheduled drip queue)
}

def clean_channel():
    print("=" * 75)
    print("🧹 THE BULL PRINT: PRIVATIZING UNDERPERFORMING / LOW-POTENTIAL UPLOADS")
    print("=" * 75)

    uploader = YouTubeUploader()
    srv = uploader._get_service("en")
    if not srv:
        print("❌ Could not get authenticated YouTube service.")
        return

    ch = srv.channels().list(mine=True, part="contentDetails,statistics").execute()
    uploads_pl = ch["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    all_vids = []
    page_token = None
    while True:
        res = srv.playlistItems().list(playlistId=uploads_pl, part="snippet", maxResults=50, pageToken=page_token).execute()
        for item in res.get("items", []):
            all_vids.append(item["snippet"]["resourceId"]["videoId"])
        page_token = res.get("nextPageToken")
        if not page_token:
            break

    print(f"Auditing {len(all_vids)} total uploads on channel...")

    details = []
    for i in range(0, len(all_vids), 50):
        batch = all_vids[i:i+50]
        res = srv.videos().list(part="snippet,status,statistics,contentDetails", id=",".join(batch)).execute()
        details.extend(res.get("items", []))

    to_privatize = []
    for v in details:
        vid = v["id"]
        title = v["snippet"]["title"]
        status = v["status"]["privacyStatus"]
        views = int(v["statistics"].get("viewCount", 0))
        published = v["snippet"]["publishedAt"]

        if vid in PERMANENT_WHITELIST:
            continue
        if status == "private":
            continue

        # Keep proven high-performing videos (>50 views)
        if views >= 50:
            continue

        # Target low potential
        # 1. Obvious junk or test titles
        if any(w in title.lower() for w in ["delete this", "crap", "test"]):
            to_privatize.append((vid, title, views, published, "Junk/Draft title"))
        # 2. Uploaded before Nov 1, 2026 with < 40 views
        elif published < "2026-11-01" and views < 40:
            to_privatize.append((vid, title, views, published, f"Stale upload ({views} views)"))
        # 3. Uploaded before Nov 5 with < 15 views
        elif published < "2026-11-05" and views < 15:
            to_privatize.append((vid, title, views, published, f"Flatlined ({views} views)"))

    print(f"\nFound {len(to_privatize)} underperforming videos to move to PRIVATE.")
    
    privatized_count = 0
    for vid, title, views, published, reason in to_privatize:
        try:
            srv.videos().update(
                part="status",
                body={
                    "id": vid,
                    "status": {
                        "privacyStatus": "private"
                    }
                }
            ).execute()
            privatized_count += 1
            print(f"✓ [{privatized_count:02d}/{len(to_privatize)}] Privatized: {title[:50]} ({vid}) | {views}v | Reason: {reason}")
            time.sleep(0.2)
        except Exception as e:
            print(f"❌ Failed to privatize {vid}: {e}")

    print("\n" + "=" * 75)
    print(f"✨ COMPLETED: Successfully moved {privatized_count} underperforming videos to PRIVATE.")
    print("Channel feed is now strictly focused on high-quality, high-potential productions!")
    print("=" * 75)

if __name__ == "__main__":
    clean_channel()
