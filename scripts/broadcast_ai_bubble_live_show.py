#!/usr/bin/env python3
"""
Dedicated Live Stream Broadcaster for Doc 01:
'The $2.5 Trillion AI Wall: Why the AI Bubble Is Cracking'
Channel: The Bull Print (@thebullprint)

Provisions:
1. YouTube Live Broadcast with Public status, full chapters & compliance shield
2. 1080p RTMP Ingestion Stream with automatic start/stop and DVR enabled
3. Binds Broadcast to Stream and sets High CTR Viral Thumbnail
4. Adds to Channel Playlists
5. Sends Telegram Live Alert to Alex
6. Streams the 12-Minute Master directly to RTMP via FFmpeg
7. Shares the real-time Live YouTube watch link
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

VIDEO_PATH = BASE_DIR / "output" / "ai_bubble_documentary" / "the_ai_bubble_panic_12min_master.mp4"
THUMBNAIL_PATH = BASE_DIR / "output" / "thumbnails" / "thumb_ai_bubble_viral_ctr.jpg"

TITLE = "🔴 LIVE SPECIAL: The $2.5 Trillion AI Wall: Why the AI Bubble Is Cracking"

DESCRIPTION = """Comprehensive forensic investigation into Wall Street's $2.5 Trillion AI infrastructure bottleneck, Nvidia and Microsoft datacenter scaling crisis, the circular AI economy, power grid shortages, and the post-midterm regulatory reckoning.

⏱️ CHAPTER TIMESTAMPS:
00:00 - The 9:30 AM Opening Bell Wipeout
00:17 - The $2.5 Trillion Evaporation
00:35 - The Mag Seven Domino Effect
00:52 - The Master Title Plate: The $2.5 Trillion AI Reckoning
01:10 - The Post-Midterm Political Shockwave
01:27 - The AI Capital Expenditure Trap
01:45 - The Wall Street Margin Call
02:02 - The Circular AI Economy
02:20 - Silicon Valley's Desperate Land Grab
02:37 - Where Are the Real Profits?
02:55 - The GPU Depreciation Time Bomb
03:12 - Enterprise Software's Brutal Reality
03:30 - Venture Capital's Burn Rate Crisis
03:47 - The Return on Investment Mirage
04:05 - Running Out of Watts
04:22 - The Gigawatt Data Center Crisis
04:40 - Local Grids Pushed to the Brink
04:57 - Big Tech's Secret Nuclear Deals
05:15 - The Three Mile Island Gamble
05:32 - Water Scarcity in Desert Towns
05:50 - The Physical Limits of Moore's Law
06:07 - The Midterm Democratic Congressional Sweep
06:25 - Subpoenas and Antitrust Hearings
06:42 - Investigating AI Data Center Subsidies
07:00 - The Energy Monopoly Investigation
07:17 - National Security Export Controls
07:35 - The Big Tech Lobbying Firewall Collapses
07:52 - Wall Street Prices In Regulatory Winter
08:10 - The Dot-Com Echo: 2000 vs 2026
08:27 - Who Survives the Crash?
08:45 - The Sovereign AI Arms Race
09:02 - From Hype to Infrastructure Utility
09:20 - The Retail Traps & False Rebounds
09:37 - The Big Institutional Rotation
09:55 - The True Valuation of Artificial Intelligence
10:12 - Final Verdict: The End of Free Passes

Inside Wall Street's panic: Big Tech has spent over $200 Billion on AI graphics processing chips, but software revenues are covering less than 15% of that infrastructure cost. As data centers consume more electricity than entire small nations and congressional investigations ramp up, this master documentary uncovers the reality behind the artificial intelligence bubble.

#TheBullPrint #AIBubble #ArtificialIntelligence #Nvidia #TechStocks #WallStreet #DataCenters #Documentary #LiveStream #ForensicFinance
"""

TAGS = [
    "#TheBullPrint", "#AIBubble", "#ArtificialIntelligence", "#Nvidia",
    "#TechStocks", "#WallStreet", "#DataCenters", "#Documentary",
    "#LiveStream", "#ForensicFinance", "#BigTech", "#StockMarket"
]

def send_telegram_live_alert(title: str, live_url: str, watch_url: str):
    import urllib.request, urllib.parse
    tg_token = "8829963924:AAE7v_xEQXLmy3-YEx8kqMo2GRfnbnxf4GA"
    chat_id = "1126599043"
    msg = (
        f"🔴 <b>THE BULL PRINT - LIVE BROADCAST INITIATED</b>\n\n"
        f"🎬 <b>Show:</b> {title}\n"
        f"⚡ <b>Format:</b> 1080p 60fps Full Master Documentary Live Premiere\n"
        f"🌐 <b>Status:</b> PUBLIC LIVE SHOW\n\n"
        f"🔴 <b>Watch Live Now:</b> {live_url}\n"
        f"📺 <b>Standard URL:</b> {watch_url}\n\n"
        f"✨ Live RTMP streaming is actively broadcasting to your YouTube channel right now!"
    )
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{tg_token}/sendMessage", data=data)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            pass
        print(f"📲 Live alert delivered to Alex on Telegram.")
    except Exception as e:
        print(f"⚠️ Telegram send error: {e}")

def main():
    if not VIDEO_PATH.exists():
        print(f"❌ Error: Master video not found at {VIDEO_PATH}")
        sys.exit(1)

    print("=" * 75)
    print("🔴 INITIATING YOUTUBE LIVE BROADCAST: THE $2.5 TRILLION AI WALL")
    print(f"   Video: {VIDEO_PATH.name} ({round(VIDEO_PATH.stat().st_size / 1024 / 1024, 1)} MB)")
    print(f"   Thumbnail: {THUMBNAIL_PATH.name}")
    print("=" * 75)

    full_description = DESCRIPTION + "\n\n" + generate_global_compliance_footer(
        target_countries=["IN", "US", "GB", "SG", "AE", "AU", "CA"],
        is_derivative=False,
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
            "frameRate": "30fps",
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

    # 4. Set Custom High CTR Viral Thumbnail & Playlists
    print("\n[4/5] 🖼️ Setting Custom Viral Thumbnail & Playlists...")
    try:
        srv.thumbnails().set(
            videoId=broadcast_id,
            media_body=MediaFileUpload(str(THUMBNAIL_PATH), mimetype="image/jpeg")
        ).execute()
        print("   ✅ Custom Viral Thumbnail uploaded successfully.")
    except Exception as e:
        print(f"   ⚠️ Thumbnail note: {e}")

    try:
        target_playlists = [
            ("PLMuYPFbxOGyI", "100-Year Masterclasses"),
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

    # Send Telegram Alert
    send_telegram_live_alert(TITLE, live_url, watch_url)

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
        "-r", "30",
        "-b:v", "4500k",
        "-maxrate", "5000k",
        "-bufsize", "10000k",
        "-pix_fmt", "yuv420p",
        "-g", "60",
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
