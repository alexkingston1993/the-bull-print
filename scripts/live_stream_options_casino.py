#!/usr/bin/env python3
"""
Dedicated Live Stream Broadcaster for Video #6:
'THE ZERO-DAY OPTIONS CASINO: The ₹1.8 Lakh Crore Retail Slaughter'
Channel: The Bull Print (@thebullprint)

Provisions:
1. YouTube Live Broadcast with Public status, full chapters & compliance shield
2. 1080p RTMP Ingestion Stream with automatic start/stop and DVR enabled
3. Binds Broadcast to Stream and sets 2K Custom Thumbnail
4. Streams the 12-Minute Animated Captioned Master directly to RTMP via FFmpeg
5. Shares the real-time Live YouTube watch link
"""

import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from googleapiclient.http import MediaFileUpload

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader
from app.services.compliance_shield import generate_global_compliance_footer

VIDEO_PATH = BASE_DIR / "output" / "options_casino_documentary" / "the_zero_day_options_casino_captioned_12min_master.mp4"
THUMBNAIL_PATH = BASE_DIR / "output" / "options_casino_documentary" / "frames" / "segment_01.jpg"

TITLE = "THE ZERO-DAY OPTIONS CASINO: The ₹1.8 Lakh Crore Retail Slaughter"

DESCRIPTION = """Comprehensive forensic investigation into India's zero-day options explosion, SEBI's bombshell study revealing 93% retail losses, high-frequency quant predatory algorithms, finfluencer fake P&L scams, and the sovereign survival blueprint for everyday investors.

⏱️ CHAPTER TIMESTAMPS:
00:00 - Prologue: The 3:15 PM Expiry Zero & The ₹1.8 Lakh Crore Black Hole
01:00 - The Master Title Plate: The Zero-Day Options Casino
01:20 - Chapter 1: The 5-Expiry Week & India's ₹400 Trillion Volume Boom
02:20 - Chapter 2: The Quants: Theta Decay, Gamma Crush & Stop-Loss Hunting
03:40 - The Latency Trap: 300ns Co-Location Servers vs. 300ms Mobile 4G
04:40 - Chapter 3: The Finfluencer Illusion: Inspect Element & ₹20,000 Courses
06:00 - The SEBI Clampdown: Guru Raids, Frozen Accounts & Dopamine Loops
07:00 - Chapter 4: The House Always Wins: ₹5,000 Cr Brokerage Profits & STT
08:40 - SEBI's 7-Point Regulatory Mandate: Tripling Lot Sizes to ₹15 Lakhs
09:20 - Chapter 5: The Math of Recovery: Why -90% Requires +900% to Break Even
10:00 - The Sovereign Blueprint: Disabling F&O, Real Hedging & Index Compounding
11:40 - The Bull Print Verdict & The Fundamental Law of Dalal Street

According to market regulator SEBI, over one lakh eighty-one thousand crore rupees were incinerated by retail traders in equity derivatives over three financial years. This documentary breaks down the exact mathematical mechanics of why individual retail option buyers face nearly 100% ruin probability over time, and how to protect your family's financial future.

Golden Rule: The stock market is a device for transferring wealth from the impatient to the patient. Options were engineered as insurance contracts, not lottery tickets.

#TheBullPrint #OptionsTrading #SEBI #Nifty #BankNifty #StockMarketIndia #ZeroDayOptions #DalalStreet #FinancialLiteracy #ForensicFinance #LiveStream
"""

TAGS = [
    "#TheBullPrint", "#OptionsTrading", "#SEBI", "#Nifty",
    "#BankNifty", "#StockMarketIndia", "#ZeroDayOptions", "#DalalStreet",
    "#Finfluencers", "#TradingLosses", "#Documentary", "#FinancialLiteracy"
]

def main():
    if not VIDEO_PATH.exists():
        print(f"❌ Error: Master video not found at {VIDEO_PATH}")
        sys.exit(1)

    print("=" * 75)
    print("🔴 INITIATING YOUTUBE LIVE STREAM: THE ZERO-DAY OPTIONS CASINO")
    print(f"   Video: {VIDEO_PATH.name} ({round(VIDEO_PATH.stat().st_size / 1024 / 1024, 1)} MB)")
    print(f"   Thumbnail: {THUMBNAIL_PATH.name}")
    print("=" * 75)

    full_description = DESCRIPTION + "\n\n" + generate_global_compliance_footer(
        target_countries=["IN", "US", "GB", "SG", "AE", "AU", "CA"],
        is_derivative=True,
        is_crypto=False
    )

    uploader = YouTubeUploader()
    srv = uploader._get_service("en")

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # 1. Create Live Broadcast
    print("\n[1/5] 📡 Creating YouTube Live Broadcast resource...")
    broadcast_body = {
        "snippet": {
            "title": TITLE,
            "description": full_description,
            "scheduledStartTime": now_utc,
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
        "contentDetails": {
            "enableAutoStart": True,
            "enableAutoStop": True,
            "enableDvr": True,
            "recordFromStart": True,
            "startWithSlate": False,
            "latencyPreference": "low",
        }
    }
    broadcast_resp = srv.liveBroadcasts().insert(
        part="snippet,status,contentDetails",
        body=broadcast_body
    ).execute()

    broadcast_id = broadcast_resp["id"]
    watch_url = f"https://www.youtube.com/watch?v={broadcast_id}"
    live_url = f"https://youtube.com/live/{broadcast_id}"
    print(f"   ✅ Broadcast Created! ID: {broadcast_id}")
    print(f"   🔴 LIVE Watch URL: {live_url}")
    print(f"   📺 Standard Watch URL: {watch_url}")

    # 2. Create Live Stream (RTMP)
    print("\n[2/5] 🔌 Provisioning RTMP Ingestion Stream...")
    stream_body = {
        "snippet": {
            "title": f"The Bull Print Live Stream - {broadcast_id}",
        },
        "cdn": {
            "frameRate": "variable",
            "ingestionType": "rtmp",
            "resolution": "1080p",
        }
    }
    stream_resp = srv.liveStreams().insert(
        part="snippet,cdn",
        body=stream_body
    ).execute()

    stream_id = stream_resp["id"]
    ingestion_info = stream_resp["cdn"]["ingestionInfo"]
    rtmp_url = ingestion_info["ingestionAddress"]
    stream_key = ingestion_info["streamName"]
    full_rtmp = f"{rtmp_url}/{stream_key}"
    print(f"   ✅ Stream Ingestion Ready! Endpoint: {rtmp_url}")

    # 3. Bind Broadcast to Stream
    print("\n[3/5] 🔗 Binding Live Broadcast to RTMP Stream...")
    srv.liveBroadcasts().bind(
        id=broadcast_id,
        part="id,contentDetails",
        streamId=stream_id
    ).execute()
    print("   ✅ Broadcast successfully bound to stream.")

    # 4. Set Custom 2K Thumbnail & Playlist
    print("\n[4/5] 🖼️ Setting Custom 2K Thumbnail & Playlists...")
    try:
        srv.thumbnails().set(
            videoId=broadcast_id,
            media_body=MediaFileUpload(str(THUMBNAIL_PATH))
        ).execute()
        print("   ✅ Custom 2K Thumbnail uploaded successfully.")
    except Exception as e:
        print(f"   ⚠️ Thumbnail note: {e}")

    try:
        target_playlists = [
            ("PLMuYPFbxOGyI", "100-Year Masterclasses"),
            ("PLDhTdRWRS2bo", "India Dalal Street Forensics"),
            ("PLIFXZFrnw2Fc", "United States Macro")
        ]
        for pl_id, pl_name in target_playlists:
            try:
                srv.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": pl_id,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": broadcast_id
                            }
                        }
                    }
                ).execute()
                print(f"   ✅ Added to Playlist: {pl_name} ({pl_id})")
            except Exception as pl_err:
                print(f"   ⚠️ Playlist {pl_name} note: {pl_err}")
    except Exception as e:
        print(f"   ⚠️ Playlist error: {e}")

    # 5. Launch RTMP Streaming via FFmpeg
    print("\n[5/5] 🚀 BROADCASTING LIVE TO YOUTUBE NOW!")
    print(f"   🔴 TUNE IN LIVE: {live_url}")
    print("=" * 75)
    sys.stdout.flush()

    ffmpeg_cmd = [
        "ffmpeg",
        "-re",
        "-i", str(VIDEO_PATH),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-b:v", "4500k",
        "-maxrate", "5000k",
        "-bufsize", "10000k",
        "-pix_fmt", "yuv420p",
        "-g", "50",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-f", "flv",
        full_rtmp
    ]

    # Run FFmpeg to stream the video
    proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    
    # Wait for completion or errors
    stderr_output = proc.communicate()[1]
    if proc.returncode != 0:
        print(f"\n❌ FFmpeg streaming exited with error:\n{stderr_output.decode()[-500:]}")
        sys.exit(proc.returncode)

    print("\n" + "=" * 75)
    print("🎉 LIVE BROADCAST STREAM COMPLETED SUCCESSFULLY!")
    print(f"   Archive / Replay URL: {watch_url}")
    print("=" * 75)

if __name__ == "__main__":
    main()
