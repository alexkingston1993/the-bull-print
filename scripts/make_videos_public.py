#!/usr/bin/env python3
"""
Make Videos Public on YouTube
scripts/make_videos_public.py
"""

import sys
import os
from pathlib import Path
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader


def make_videos_public(video_ids):
    logger.info(f"Setting privacyStatus to 'public' for: {video_ids}")
    uploader = YouTubeUploader()
    srv = uploader._get_service("en")
    if not srv:
        logger.error("Failed to authenticate YouTube API service.")
        sys.exit(1)

    for vid in video_ids:
        vid = vid.strip()
        if not vid:
            continue
        try:
            body = {
                "id": vid,
                "status": {
                    "privacyStatus": "public"
                }
            }
            res = srv.videos().update(part="status", body=body).execute()
            status = res.get("status", {}).get("privacyStatus")
            logger.success(f"✓ Video {vid} privacyStatus updated to: '{status}' -> https://youtu.be/{vid}")
        except Exception as e:
            logger.error(f"❌ Failed to update video {vid}: {e}")


if __name__ == "__main__":
    vids = sys.argv[1:] if len(sys.argv) > 1 else ["lSdRmaHCets", "m34Yd5TphF0"]
    make_videos_public(vids)
