#!/usr/bin/env python3
"""
Dedicated Live Stream Broadcaster for Doc 03:
'Big Tech's Nuclear Secret: Why AI Giants Are Buying Up Atomic Power Plants'
Channel: The Bull Print (@thebullprint)

Provisions:
1. YouTube Live Broadcast with Public status, 36 chapters & global compliance shield
2. 1080p RTMP Ingestion Stream with automatic start/stop and DVR enabled
3. Sets Gold Standard Viral Thumbnail (thumb_nuclear_ai_viral_ctr.jpg)
4. Sends Telegram Live Alert to Alex
5. Streams the 12-Minute Master directly to RTMP via FFmpeg
6. Outputs real-time Live YouTube watch link
"""

import os
import subprocess
import sys
import time
import json
from datetime import datetime, timezone
from pathlib import Path
from googleapiclient.http import MediaFileUpload

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader
from app.services.compliance_shield import generate_global_compliance_footer

VIDEO_PATH = BASE_DIR / "output" / "nuclear_ai_documentary" / "the_nuclear_ai_race_12min_master.mp4"
THUMBNAIL_PATH = BASE_DIR / "output" / "thumbnails" / "thumb_nuclear_ai_viral_ctr.jpg"

TITLE = "🔴 LIVE SPECIAL: Big Tech's Nuclear Secret: Why AI Giants Are Buying Up Atomic Power Plants"

def generate_chapters() -> str:
    timing_file = BASE_DIR / "output" / "nuclear_ai_documentary" / "timing_and_timestamps.json"
    if not timing_file.exists():
        return ""
    with open(timing_file, "r") as f:
        data = json.load(f)
        
    lines = ["⏱️ CHAPTER TIMESTAMPS:"]
    cur_time = 0.0
    for seg_id in range(1, 37):
        s_data = data["segments"].get(str(seg_id), {})
        title = s_data.get("title", f"Segment {seg_id}")
        dur = float(s_data.get("duration", 18.0))
        m = int(cur_time // 60)
        s = int(cur_time % 60)
        lines.append(f"{m:02d}:{s:02d} - {title}")
        cur_time += dur
    return "\n".join(lines)

CHAPTERS_TEXT = generate_chapters()

DESCRIPTION = f"""Comprehensive forensic documentary investigating why Microsoft, Amazon, Google, and Meta are investing billions directly into nuclear reactors, reviving decommissioned atomic plants like Three Mile Island, and bypassing the public electrical grid.

{CHAPTERS_TEXT}

Forensic breakdown: Artificial intelligence data centers are encountering a physical limit: the electrical power grid. By 2030, AI compute clusters are projected to consume more electricity than entire industrialized nations. In this master investigation, we analyze the multi-billion dollar Power Purchase Agreements, Small Modular Reactor (SMR) supply chains, uranium market dynamics, and how Big Tech is transitioning from software platforms into sovereign energy utilities.

#TheBullPrint #ArtificialIntelligence #NuclearEnergy #BigTech #Nvidia #Microsoft #Google #Amazon #EnergyCrisis #Economy #LiveStream #ForensicFinance
"""

TAGS = [
    "#TheBullPrint", "#NuclearEnergy", "#ArtificialIntelligence", "#BigTech",
    "#Nvidia", "#Microsoft", "#Google", "#Amazon", "#DataCenters",
    "#EnergyCrisis", "#LiveStream", "#ForensicFinance", "#Documentary"
]

def send_telegram_live_alert(title: str, live_url: str, watch_url: str):
    import urllib.request, urllib.parse
    tg_token = "8829963924:AAE7v_xEQXLmy3-YEx8kqMo2GRfnbnxf4GA"
    chat_id = "1126599043"
    msg = (
        f"🔴 <b>THE BULL PRINT - LIVE BROADCAST INITIATED</b>\n\n"
        f"🎬 <b>Show:</b> {title}\n"
        f"⚡ <b>Format:</b> 1080p Master Documentary Live Premiere (12-Minute Duration)\n"
        f"🖼️ <b>Thumbnail:</b> Gold Standard Viral CTR Thumbnail Attached\n"
        f"🌐 <b>Status:</b> PUBLIC LIVE SHOW\n\n"
        f"🔴 <b>Watch Live:</b> {live_url}\n"
        f"📺 <b>Standard URL:</b> {watch_url}\n\n"
        f"✨ Live streaming actively broadcasting to YouTube right now!"
    )
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{tg_token}/sendMessage", data=data)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print("📲 Telegram live alert sent successfully!")
    except Exception as e:
        print(f"⚠️ Telegram alert failed: {e}")

def main():
    print("=" * 75)
    print("🎬 THE BULL PRINT: DOC 03 LIVE BROADCAST LAUNCHER")
    print(f"Title: {TITLE}")
    print("=" * 75)

    if not VIDEO_PATH.exists():
        print(f"❌ Video not found at {VIDEO_PATH}")
        sys.exit(1)

    vid_size_mb = VIDEO_PATH.stat().st_size / 1024 / 1024
    print(f"📦 Master Video: {VIDEO_PATH.name} ({vid_size_mb:.1f} MB)")
    print(f"🖼️ Thumbnail: {THUMBNAIL_PATH.name} (Exists: {THUMBNAIL_PATH.exists()})")

    # 1. Initialize YouTube API client
    uploader = YouTubeUploader()
    srv = uploader._get_service("en")

    # 2. Add Compliance Shield
    full_description = DESCRIPTION.strip() + "\n\n" + generate_global_compliance_footer()

    # 3. Create Live Broadcast Resource
    now_iso = datetime.now(timezone.utc).isoformat()
    broadcast_body = {
        "snippet": {
            "title": TITLE,
            "description": full_description,
            "scheduledStartTime": now_iso
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        },
        "contentDetails": {
            "enableAutoStart": True,
            "enableAutoStop": True,
            "enableDvr": True,
            "recordFromStart": True
        }
    }

    print("📡 Creating YouTube Live Broadcast...")
    broadcast_resp = srv.liveBroadcasts().insert(
        part="snippet,status,contentDetails",
        body=broadcast_body
    ).execute()

    broadcast_id = broadcast_resp["id"]
    watch_url = f"https://www.youtube.com/watch?v={broadcast_id}"
    live_url = f"https://www.youtube.com/live/{broadcast_id}"
    print(f"✅ Live Broadcast Created! ID: {broadcast_id}")
    print(f"🔗 Permanent Watch URL: {watch_url}")
    print(f"🔴 Live URL: {live_url}")

    # 4. Create Live Stream Resource (RTMP ingestion)
    stream_body = {
        "snippet": {
            "title": f"The Bull Print RTMP Stream - {broadcast_id[:8]}"
        },
        "cdn": {
            "frameRate": "30fps",
            "ingestionType": "rtmp",
            "resolution": "1080p"
        }
    }

    print("🔌 Provisioning RTMP Ingestion Endpoint...")
    stream_resp = srv.liveStreams().insert(
        part="snippet,cdn",
        body=stream_body
    ).execute()

    stream_id = stream_resp["id"]
    ingestion_info = stream_resp["cdn"]["ingestionInfo"]
    rtmp_url = ingestion_info["ingestionAddress"]
    stream_key = ingestion_info["streamName"]
    full_rtmp_target = f"{rtmp_url}/{stream_key}"
    print(f"✅ RTMP Ingestion Ready! Stream ID: {stream_id}")

    # 5. Bind Broadcast to Stream
    print("🔗 Binding Broadcast to RTMP Stream...")
    srv.liveBroadcasts().bind(
        part="id,contentDetails",
        id=broadcast_id,
        streamId=stream_id
    ).execute()
    print("✅ Broadcast & Stream Bound Successfully!")

    # 6. Upload Gold Standard Viral Thumbnail
    if THUMBNAIL_PATH.exists():
        print(f"🖼️ Setting Video Thumbnail from {THUMBNAIL_PATH.name}...")
        try:
            srv.thumbnails().set(
                videoId=broadcast_id,
                media_body=MediaFileUpload(str(THUMBNAIL_PATH), mimetype="image/jpeg")
            ).execute()
            print("✅ Viral Thumbnail Applied Successfully!")
        except Exception as e:
            print(f"⚠️ Thumbnail upload warning: {e}")

    # 7. Send Telegram Alert to Alex
    send_telegram_live_alert(TITLE, live_url, watch_url)

    # 8. Start RTMP Streaming via FFmpeg
    print("=" * 75)
    print("🚀 COMMENCING 1080P RTMP LIVE STREAM VIA FFMPEG...")
    print(f"Target: {rtmp_url} (Key: {stream_key[:6]}...)")
    print("=" * 75)

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
        "-g", "60",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-f", "flv",
        full_rtmp_target
    ]

    print("Streaming in progress...")
    proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    if proc.returncode == 0:
        print("=" * 75)
        print("🎉 LIVE BROADCAST STREAM COMPLETED SUCCESSFULLY!")
        print(f"📺 Archive & Replay URL: {watch_url}")
        print("=" * 75)
    else:
        print(f"⚠️ Stream finished with code {proc.returncode}")
        print(stderr.decode()[-400:])

if __name__ == "__main__":
    main()
