#!/usr/bin/env python3
"""
Upload Script for Viral YouTube Short: The $3 Billion/Day US Debt Spiral
Channel: The Bull Print (@TheBullPrint)
Privacy Status: PUBLIC
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

VIDEO_PATH = BASE_DIR / "output" / "shorts" / "us_debt_spiral_magnates_short.mp4"
THUMBNAIL_PATH = Path("/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364/verify_short_cut01.jpg")

TITLE = "America's $3 Billion/Day Debt Trap Exposed #Shorts"
DESCRIPTION = """At this exact second, the United States is paying nearly $3 Billion every single day... just on interest.

Net interest outlays on the national debt have crossed $1.05 Trillion annually—officially surpassing the entire U.S. military defense budget. To pay that interest, the Treasury must borrow brand new debt, triggering a mathematical compound trap.

Subscribe to @TheBullPrint for daily financial intelligence and investigative documentaries.

#TheBullPrint #USDebt #NationalDebt #Economy #FederalReserve #Finance #Money #Shorts"""

TAGS = [
    "TheBullPrint", "USDebt", "NationalDebt", "Economy",
    "FederalReserve", "Finance", "Money", "Treasury",
    "Inflation", "Shorts"
]

def upload_short():
    print("=" * 70)
    print("🚀 UPLOADING VIRAL US DEBT SHORT TO YOUTUBE (PUBLIC)")
    print("=" * 70)

    if not VIDEO_PATH.exists():
        print(f"❌ Error: Video file not found at {VIDEO_PATH}")
        sys.exit(1)

    print(f"File: {VIDEO_PATH.name} ({round(VIDEO_PATH.stat().st_size / 1024 / 1024, 2)} MB)")
    print(f"Title: {TITLE}")
    print(f"Privacy: PUBLIC")

    uploader = YouTubeUploader()

    res = uploader.upload_video(
        language="en",
        video_path=str(VIDEO_PATH),
        title=TITLE,
        description=DESCRIPTION,
        tags=TAGS,
        category_id="25",  # News & Politics
        privacy_status="public",
        is_short=True,
        thumbnail_path=str(THUMBNAIL_PATH) if THUMBNAIL_PATH.exists() else None,
        force_upload=True
    )

    if res.get("success"):
        video_id = res.get("video_id")
        video_url = res.get("url") or f"https://www.youtube.com/shorts/{video_id}"
        print("\n" + "=" * 70)
        print(f"🎉 SHORT IS LIVE ON YOUTUBE!")
        print(f"🔗 Watch URL: {video_url}")
        print(f"🆔 Video ID: {video_id}")
        print(f"🌐 Privacy Status: PUBLIC")
        print("=" * 70)
        return video_url, video_id
    else:
        err = res.get("error")
        print(f"\n❌ Upload failed: {err}")
        sys.exit(1)

if __name__ == "__main__":
    upload_short()
