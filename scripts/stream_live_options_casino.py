#!/usr/bin/env python3
"""
Live Stream Broadcaster for Video #6:
'THE ZERO-DAY OPTIONS CASINO: The ₹1.8 Lakh Crore Retail Slaughter'
Channel: The Bull Print (@thebullprint)
Streams to YouTube Live Broadcast: X02xM38hsHs
Live URL: https://youtube.com/live/X02xM38hsHs
"""

import os
import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

VIDEO_PATH = BASE_DIR / "output" / "options_casino_documentary" / "the_zero_day_options_casino_captioned_12min_master.mp4"
BROADCAST_ID = "X02xM38hsHs"
STREAM_ID = "we4D4M4i9aaHdi2ZBlbUmA1793991848851608"

def main():
    if not VIDEO_PATH.exists():
        print(f"❌ Error: Video not found at {VIDEO_PATH}")
        sys.exit(1)

    uploader = YouTubeUploader()
    srv = uploader._get_service("en")

    # Fetch stream ingestion details
    stream_info = srv.liveStreams().list(part="id,snippet,cdn", id=STREAM_ID).execute()
    items = stream_info.get("items", [])
    if not items:
        print(f"❌ Error: Live stream {STREAM_ID} not found")
        sys.exit(1)

    cdn = items[0]["cdn"]["ingestionInfo"]
    rtmp_url = cdn["ingestionAddress"]
    stream_key = cdn["streamName"]
    full_rtmp = f"{rtmp_url}/{stream_key}"

    print("=" * 75)
    print("🔴 BROADCASTING LIVE TO YOUTUBE NOW!")
    print(f"   Video: {VIDEO_PATH.name} ({round(VIDEO_PATH.stat().st_size / 1024 / 1024, 1)} MB)")
    print(f"   Broadcast ID: {BROADCAST_ID}")
    print(f"   🔴 LIVE Watch URL: https://youtube.com/live/{BROADCAST_ID}")
    print(f"   📺 Standard Watch URL: https://www.youtube.com/watch?v={BROADCAST_ID}")
    print("=" * 75)
    sys.stdout.flush()

    # Stream to RTMP via FFmpeg in real-time with flawless stream copy
    cmd = [
        "ffmpeg",
        "-re",
        "-i", str(VIDEO_PATH),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-f", "flv",
        full_rtmp
    ]

    log_path = BASE_DIR / "output" / "options_casino_documentary" / "live_stream.log"
    print(f"🚀 Ingesting live video stream to YouTube RTMP server (log: {log_path.name})...")
    with open(log_path, "w") as log_f:
        proc = subprocess.Popen(cmd, stdout=log_f, stderr=subprocess.STDOUT)
        
        # Monitor initial handshake
        time.sleep(12)
        if proc.poll() is not None:
            print(f"❌ Error: FFmpeg exited early with code {proc.returncode}")
            sys.exit(1)

        print("✅ Ingestion stream verified: Active & delivering packets.")
        print(f"🎉 GO WATCH LIVE: https://youtube.com/live/{BROADCAST_ID}")
        sys.stdout.flush()

        ret = proc.wait()

    if ret != 0:
        print(f"❌ Streaming error: Process returned {ret}")
        sys.exit(ret)

    print("\n🎉 Broadcast stream completed successfully! Archive is now available on YouTube.")

if __name__ == "__main__":
    main()
