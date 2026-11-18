#!/usr/bin/env python3
"""
YouTube Live Broadcast Engine for Master Documentaries (The Bull Print)
app/services/youtube_live_streamer.py

Creates a YouTube Live Broadcast, provisions RTMP ingestion, attaches high-CTR thumbnail,
and streams the master 1080p documentary video live to the channel.
Upon stream completion, YouTube automatically archives the live broadcast as a permanent video.
"""

import os
import sys
import json
import pickle
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_authenticated_youtube_service():
    """Initializes and returns authenticated Google API client for YouTube."""
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials

    # 1. Try local pickle
    token_pickle = BASE_DIR / "data" / "youtube_tokens" / "youtube_token_en.pickle"
    if token_pickle.exists():
        try:
            with open(token_pickle, "rb") as f:
                creds = pickle.load(f)
                return build("youtube", "v3", credentials=creds)
        except Exception as e:
            logger.warning(f"Failed loading token from {token_pickle}: {e}")

    # 2. Try environment / pool JSON
    pool_json = os.getenv("YT_OAUTH_POOL_JSON")
    if pool_json:
        try:
            pool = json.loads(pool_json)
            client = pool.get("client_1", {})
            creds = Credentials(
                token=None,
                refresh_token=client.get("refresh_token"),
                token_uri="https://oauth2.googleapis.com/token",
                client_id=client.get("client_id"),
                client_secret=client.get("client_secret")
            )
            return build("youtube", "v3", credentials=creds)
        except Exception as e:
            logger.warning(f"Failed loading credentials from YT_OAUTH_POOL_JSON: {e}")

    cid = os.getenv("YOUTUBE_CLIENT_ID") or os.getenv("YT_CLIENT_ID_1")
    csec = os.getenv("YOUTUBE_CLIENT_SECRET") or os.getenv("YT_CLIENT_SECRET_1")
    rtok = os.getenv("YOUTUBE_REFRESH_TOKEN") or os.getenv("YT_REFRESH_TOKEN_1")
    if cid and csec and rtok:
        creds = Credentials(
            token=None,
            refresh_token=rtok,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=cid,
            client_secret=csec
        )
        return build("youtube", "v3", credentials=creds)

    raise RuntimeError("No valid YouTube authentication credentials found.")


def broadcast_documentary_as_live(
    video_path: Path,
    thumbnail_path: Optional[Path],
    title: str,
    description: str,
    scheduled_start_iso: Optional[str] = None
) -> Dict[str, Any]:
    """
    Schedules and streams a master documentary as an official YouTube Live Broadcast.
    """
    from googleapiclient.http import MediaFileUpload

    logger.info(f"🔴 [Live Broadcaster] Initializing YouTube Live Broadcast for: '{title}'")
    srv = get_authenticated_youtube_service()

    now_iso = scheduled_start_iso or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # 1. Create Live Broadcast
    broadcast_body = {
        "snippet": {
            "title": f"🔴 LIVE SPECIAL: {title[:80]}",
            "description": description,
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

    logger.info("📡 Creating YouTube Live Broadcast resource...")
    broadcast_resp = srv.liveBroadcasts().insert(
        part="snippet,status,contentDetails",
        body=broadcast_body
    ).execute()

    broadcast_id = broadcast_resp["id"]
    watch_url = f"https://www.youtube.com/watch?v={broadcast_id}"
    live_url = f"https://www.youtube.com/live/{broadcast_id}"
    logger.success(f"✅ Live Broadcast Created! ID: {broadcast_id} | Live: {live_url}")

    # 2. Create Live Stream Resource (RTMP ingestion)
    stream_body = {
        "snippet": {
            "title": f"The Bull Print Live Stream - {broadcast_id[:8]}"
        },
        "cdn": {
            "frameRate": "30fps",
            "ingestionType": "rtmp",
            "resolution": "1080p"
        }
    }

    logger.info("🔌 Provisioning RTMP Ingestion Endpoint...")
    stream_resp = srv.liveStreams().insert(
        part="snippet,cdn",
        body=stream_body
    ).execute()

    stream_id = stream_resp["id"]
    ingestion_info = stream_resp["cdn"]["ingestionInfo"]
    rtmp_url = ingestion_info["ingestionAddress"]
    stream_key = ingestion_info["streamName"]
    full_rtmp_target = f"{rtmp_url}/{stream_key}"
    logger.success(f"✅ RTMP Ingestion Ready! Stream ID: {stream_id}")

    # 3. Bind Broadcast to Stream
    logger.info("🔗 Binding Broadcast to RTMP Stream...")
    srv.liveBroadcasts().bind(
        part="id,contentDetails",
        id=broadcast_id,
        streamId=stream_id
    ).execute()

    # 4. Attach High-CTR Thumbnail
    if thumbnail_path and thumbnail_path.exists():
        try:
            logger.info(f"🖼️ Setting Live Thumbnail from {thumbnail_path.name}...")
            srv.thumbnails().set(
                videoId=broadcast_id,
                media_body=MediaFileUpload(str(thumbnail_path), mimetype="image/jpeg")
            ).execute()
            logger.success("✅ Viral Thumbnail Applied Successfully!")
        except Exception as e:
            logger.warning(f"Thumbnail upload warning: {e}")

    # 5. Stream Video to RTMP Target via FFmpeg
    logger.info("=" * 70)
    logger.info("🚀 COMMENCING 1080P RTMP LIVE STREAM VIA FFMPEG...")
    logger.info(f"Source: {video_path.name} ({video_path.stat().st_size // (1024*1024)} MB)")
    logger.info(f"Target: {rtmp_url} (Key: {stream_key[:6]}...)")
    logger.info("=" * 70)

    ffmpeg_cmd = [
        "ffmpeg",
        "-re",
        "-i", str(video_path),
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

    proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    if proc.returncode == 0:
        logger.success("🎉 LIVE BROADCAST STREAM COMPLETED SUCCESSFULLY!")
        logger.success(f"📺 Archive & Permanent Replay URL: {watch_url}")
        return {
            "success": True,
            "broadcast_id": broadcast_id,
            "watch_url": watch_url,
            "live_url": live_url,
            "stream_id": stream_id
        }
    else:
        err_msg = stderr.decode()[-400:] if stderr else "Unknown error"
        logger.error(f"⚠️ Live stream process terminated with code {proc.returncode}: {err_msg}")
        return {
            "success": False,
            "broadcast_id": broadcast_id,
            "error": err_msg
        }
