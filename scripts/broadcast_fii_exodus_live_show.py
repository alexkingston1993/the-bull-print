#!/usr/bin/env python3
"""
Dedicated Live Stream Broadcaster for Doc 02:
'The ₹14,900 Crore U-Turn: How Foreign Investors Broke and Rescued the Indian Market'
Channel: The Bull Print (@thebullprint)

Provisions:
1. YouTube Live Broadcast with Public status, chapters & global compliance shield
2. 1080p RTMP Ingestion Stream with automatic start/stop and DVR enabled
3. Sets Gold Standard Viral Thumbnail (thumb_fii_exodus_viral_ctr.jpg)
4. Sends Telegram Live Alert to Alex
5. Streams the 10:18 Master directly to RTMP via FFmpeg
6. Outputs real-time Live YouTube watch link
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

VIDEO_PATH = BASE_DIR / "output" / "fii_exodus_documentary" / "the_fii_exodus_12min_master.mp4"
THUMBNAIL_PATH = BASE_DIR / "output" / "thumbnails" / "thumb_fii_exodus_viral_ctr.jpg"

TITLE = "🔴 LIVE SPECIAL: The ₹14,900 Crore U-Turn: How Foreign Investors Broke and Rescued the Indian Market"

DESCRIPTION = """Comprehensive forensic investigation into foreign institutional capital flows, the ₹1.8 Lakh Crore October panic, domestic retail SIP resilience, the China trade rotation collapse, and how India set its own price on the global stage.

⏱️ CHAPTER TIMESTAMPS:
00:00 - The ₹1.8 Lakh Crore Flash Sell-Off
00:17 - When the Tickers Bleed Crimson
00:35 - Thirty Days of Relentless Exits
00:53 - Master Title Plate: The ₹14,900 Crore U-Turn
01:11 - Global Funds Head for the Exit
01:29 - The Great 2024 Valuation Peak
01:47 - When Domestic Valuations Stretched
02:04 - Red Flags in Mid and Small Caps
02:22 - The Warning Signs in Retail Leverage
02:40 - The Currency Trap: Rupee Under Pressure
02:58 - The RBI's Foreign Exchange War Chest
03:16 - Defense of the ₹84 Per Dollar Line
03:33 - Inflation Differentials and Bond Yields
03:51 - Foreign Custody Clearing Houses Empty
04:09 - Nifty at 23x P/E: The Premium Debate
04:27 - The 12.5% LTCG Tax Backlash
04:45 - The Federal Reserve 50 bps Cut Shock
05:03 - China Announces Bazooka Stimulus
05:21 - Buy China, Sell India: The Rotation
05:39 - October 2024: The Record Pullout
05:57 - Auto and FMCG Growth Hits a Wall
06:15 - Corporate Earnings Misses Mount
06:33 - The 24,000 Support Level Breach
06:51 - Domestic Mutual Funds Stand Their Ground
07:09 - The ₹25,000 Crore Monthly SIP Shield
07:27 - Foreign Ownership Drops to Historical Low
07:45 - Rupee Pressure & Central Bank Defense
08:03 - The China Trade Rotation Fizzles Out
08:21 - Valuation Reset: Nifty Hits Fair Value
08:39 - Trump Tariff Shock: Emerging Markets
08:57 - India's Domestic Consumption Immunity
09:15 - The Capitulation Bottom
09:33 - The ₹14,900 Crore Comeback Inflow
09:51 - Private Banks & Tech Giants Lead Reversal
10:09 - Final Verdict: India Sets Its Price

Forensic breakdown: Foreign institutional funds pulled over ₹1.8 Lakh Crore from Indian equities in a single quarter, chasing cheaper valuations in China and reacting to domestic tax shifts. But unlike 2008 or 2013, the Indian market did not collapse. Anchored by ₹25,000 Crore monthly domestic SIP inflows, retail and institutional domestic capital absorbed the shock, forcing foreign funds to execute a historic ₹14,900 Crore U-turn.

#TheBullPrint #ForeignInvestors #IndianMarket #Nifty #StockMarketIndia #FII #DII #Economy #Documentary #LiveStream #ForensicFinance
"""

TAGS = [
    "#TheBullPrint", "#ForeignInvestors", "#IndianMarket", "#Nifty",
    "#StockMarketIndia", "#FII", "#DII", "#Economy",
    "#Documentary", "#LiveStream", "#ForensicFinance", "#Sensex"
]

def send_telegram_live_alert(title: str, live_url: str, watch_url: str):
    import urllib.request, urllib.parse
    tg_token = "8829963924:AAE7v_xEQXLmy3-YEx8kqMo2GRfnbnxf4GA"
    chat_id = "1126599043"
    msg = (
        f"🔴 <b>THE BULL PRINT - LIVE BROADCAST INITIATED</b>\n\n"
        f"🎬 <b>Show:</b> {title}\n"
        f"⚡ <b>Format:</b> 1080p Master Documentary Live Premiere (10:18 Duration)\n"
        f"🖼️ <b>Thumbnail:</b> Gold Standard Viral CTR Thumbnail Attached\n"
        f"🌐 <b>Status:</b> PUBLIC LIVE SHOW\n\n"
        f"🔴 <b>Watch Live:</b> {live_url}\n"
        f"📺 <b>Standard URL:</b> {watch_url}\n\n"
        f"✨ Live streaming actively broadcasting to YouTube right now!"
    )
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{tg_token}/sendMessage", data=data)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            pass
        print(f"📲 Live alert delivered to Alex on Telegram.")
    except Exception as e:
        print(f"⚠️ Telegram send error: {e}")

def create_and_start_live_broadcast(schedule_time_utc: str = None):
    if not VIDEO_PATH.exists():
        print(f"❌ Error: Master video not found at {VIDEO_PATH}")
        sys.exit(1)

    print("=" * 75)
    print("🔴 INITIATING YOUTUBE LIVE BROADCAST: THE ₹14,900 CRORE U-TURN")
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

    now_utc = schedule_time_utc or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

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

    # 4. Set Custom Viral Thumbnail
    print("\n[4/5] 🖼️ Setting Custom Gold Standard Viral Thumbnail...")
    if THUMBNAIL_PATH.exists():
        try:
            srv.thumbnails().set(
                videoId=broadcast_id,
                media_body=MediaFileUpload(str(THUMBNAIL_PATH), mimetype="image/jpeg")
            ).execute()
            print("   ✅ Gold standard viral thumbnail attached successfully!")
        except Exception as e:
            print(f"   ⚠️ Thumbnail upload warning: {e}")

    # 5. Send Telegram Notification
    send_telegram_live_alert(TITLE, live_url, watch_url)

    # 6. Stream video to RTMP via FFmpeg
    print(f"\n[5/5] 🚀 Starting RTMP Live Stream to YouTube ({broadcast_id})...")
    ffmpeg_cmd = [
        "ffmpeg", "-re",
        "-i", str(VIDEO_PATH),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-b:v", "4500k",
        "-maxrate", "5000k",
        "-bufsize", "10000k",
        "-pix_fmt", "yuv420p",
        "-g", "60",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        "-f", "flv",
        full_rtmp
    ]

    print("   📡 Streaming active... Broadcasting master documentary...")
    sys.stdout.flush()
    proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    
    stderr_output = proc.communicate()[1]
    if proc.returncode != 0:
        print(f"\n❌ FFmpeg streaming exited with error:\n{stderr_output.decode()[-500:]}")
        sys.exit(proc.returncode)

    print("\n" + "=" * 75)
    print("🎉 LIVE BROADCAST STREAM COMPLETED SUCCESSFULLY!")
    print(f"   Permanent Archive / Replay URL: {watch_url}")
    print("=" * 75)

if __name__ == "__main__":
    create_and_start_live_broadcast()

