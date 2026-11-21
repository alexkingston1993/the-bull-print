#!/usr/bin/env python3
"""
Official TikTok Content Posting API v2 Publisher (The Bull Print)
app/services/tiktok_publisher.py

Direct integration with TikTok Content Posting API v2:
1. Video Initialization: POST /v2/post/publish/video/init/ (FILE_UPLOAD & PULL_FROM_URL)
2. Resumable Binary Streaming: PUT to TikTok upload_url with Content-Range
3. Status Polling: POST /v2/post/publish/status/fetch/
4. Token Refresh: POST /v2/oauth/token/
5. AI/SEO Caption Optimization for TikTok Search & FinanceTok discovery
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from loguru import logger
import requests

BASE_DIR = Path(__file__).resolve().parent.parent.parent
QUARANTINED_VIDEO_IDS = {"Z6LEnQyhuvw", "quarantined"}


def get_tiktok_credentials() -> Dict[str, str]:
    """Retrieves validated TikTok API credentials from environment."""
    client_key = os.getenv("TIKTOK_CLIENT_KEY", "")
    client_secret = os.getenv("TIKTOK_CLIENT_SECRET", "")
    access_token = os.getenv("TIKTOK_ACCESS_TOKEN", "")
    refresh_token = os.getenv("TIKTOK_REFRESH_TOKEN", "")

    return {
        "client_key": client_key,
        "client_secret": client_secret,
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def build_tiktok_seo_caption(
    title: str,
    synopsis: str = "",
    youtube_video_id: str = "",
    tags: Optional[List[str]] = None
) -> str:
    """
    Generates an AI & SEO-Optimized caption specifically tailored for TikTok search with clean UTM tracking.
    Includes uppercase hook, entity-rich search phrases, mission anchor, YouTube CTA,
    and high-intent #FinanceTok tags. Max 2,200 characters.
    """
    clean_title = title.replace("| The Bull Print", "").strip()
    api_key = os.getenv("GEMINI_API_KEY")

    yt_link = f"youtu.be/{youtube_video_id}?utm_source=tiktok&utm_medium=short&utm_campaign=thebullprint" if youtube_video_id else ""
    portal_link = "thebullprint.com/links?utm_source=tiktok&utm_medium=short&utm_campaign=thebullprint"

    if api_key:
        prompt = f"""You are the TikTok Growth Director and SEO Strategist for 'The Bull Print' (@thebullprint), an elite macro finance media brand.
Write a viral, search-optimized TikTok caption for a short video:
TITLE: {clean_title}
CONTEXT: {synopsis or clean_title}
YOUTUBE VIDEO ID: {youtube_video_id or 'latest'}

MANDATORY TIKTOK STRUCTURE:
1. LINE 1: High-curiosity uppercase hook with exact financial number/figure (e.g., "$7.5B DEBT TRAP 🚨", "21% PREMIUM SURGE ⚠️").
2. PARAGRAPH 2: 2–3 dense, fast-paced sentences naming institutions, tickers, central banks, and dollar amounts for TikTok search ranking.
3. PARAGRAPH 3: Exactly "Financial freedom for everyone through financial literacy. 💡"
4. PARAGRAPH 4: "Watch full 12-minute institutional breakdown on YouTube @TheBullPrint ({yt_link or 'link in bio'})."
5. FOOTER: #TheBullPrint #MacroEconomics #FinancialLiteracy #FinanceTok #StockMarket plus 3–4 dynamic entity tags.

Output ONLY the final caption text. Zero conversational filler, zero markdown formatting."""

        models_to_try = ["gemini-2.5-flash", "gemini-flash-latest", "gemini-flash-lite-latest"]
        for model in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                resp = requests.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    json={"contents": [{"parts": [{"text": prompt}]}]},
                    timeout=10
                )
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts and "text" in parts[0]:
                            ai_caption = parts[0]["text"].strip()
                            if len(ai_caption) > 80:
                                return ai_caption[:2150]
            except Exception as e:
                logger.debug(f"TikTok Gemini caption notice ({model}): {e}")

    # Deterministic Institutional Fallback Template with clean UTM tracking
    upper_hook = clean_title.upper()
    summary_part = synopsis.strip() if synopsis else (
        f"Forensic breakdown of sovereign liquidity flows, central bank interventions, "
        f"and macro capital shifts driving {clean_title}."
    )
    mission_anchor = "Financial freedom for everyone through financial literacy. 💡"
    cta_part = (
        f"Watch the full 12-minute institutional briefing on YouTube @TheBullPrint "
        + (f"(search ID: {yt_link}). " if yt_link else "")
        + f"Tap the link in our bio ({portal_link})! 🔗"
    )

    default_tags = ["#TheBullPrint", "#MacroEconomics", "#FinancialLiteracy", "#FinanceTok", "#StockMarket"]
    if tags:
        custom_tags = [f"#{t.replace(' ', '')}" for t in tags[:3] if not t.startswith("#")]
        all_tags = default_tags + custom_tags
    else:
        all_tags = default_tags

    caption = (
        f"{upper_hook} 🚨\n\n"
        f"{summary_part}\n\n"
        f"{mission_anchor}\n\n"
        f"{cta_part}\n\n"
        f"{' '.join(all_tags)}"
    )
    return caption[:2150]


def publish_local_tiktok_video(
    video_path: str,
    caption: str,
    access_token: Optional[str] = None,
    privacy_level: str = "PUBLIC_TO_EVERYONE",
    disable_duet: bool = False,
    disable_stitch: bool = False,
    disable_comment: bool = False,
    max_wait_sec: int = 300,
    video_id: str = "",
    release_slot: str = "routine"
) -> Dict[str, Any]:
    """
    Publishes a local .mp4 video to TikTok via the official Content Posting API v2.
    Uses FILE_UPLOAD protocol with direct chunk streaming, strict quarantine enforcement,
    and Cloudflare D1 idempotency protection.
    """
    # 1. Quarantine Guardrail
    if video_id in QUARANTINED_VIDEO_IDS or "Z6LEnQyhuvw" in (caption or "") or "Z6LEnQyhuvw" in video_path:
        logger.warning(f"🚫 [Quarantine Gate] Video '{video_id}' is permanently quarantined. Aborting TikTok publish.")
        return {"success": False, "error": "Blocked by quarantine guardrail", "quarantined": True}

    # 2. Idempotency Check via Cloudflare D1
    d1_client = None
    if video_id:
        try:
            from app.services.cloudflare_r2_vault import CloudflareD1Client
            d1_client = CloudflareD1Client()
            existing = d1_client.check_cross_post_idempotency(video_id, "tiktok", release_slot)
            if existing and existing.get("status") == "SUCCESS":
                logger.info(f"⏭️ [Idempotency Gate] Video '{video_id}' already published to TikTok for slot '{release_slot}'. Skipping duplicate.")
                return {"success": True, "skipped": True, "publish_id": existing.get("permalink")}
        except Exception as de:
            logger.debug(f"D1 idempotency check notice: {de}")

    creds = get_tiktok_credentials()
    token = access_token or creds["access_token"]
    if not token:
        return {"success": False, "error": "TIKTOK_ACCESS_TOKEN not configured."}

    p = Path(video_path)
    if not p.exists():
        return {"success": False, "error": f"Video file not found: {video_path}"}
    file_size = p.stat().st_size

    logger.info(f"📱 [TikTok Publisher] Initializing video upload for '{p.name}' ({file_size // 1024} KB)...")

    # Step 1: Initialize Direct File Upload
    init_url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=UTF-8"
    }

    init_payload = {
        "post_info": {
            "title": caption[:2150],
            "privacy_level": privacy_level,
            "disable_duet": disable_duet,
            "disable_stitch": disable_stitch,
            "disable_comment": disable_comment,
            "video_cover_timestamp_ms": 1000
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": file_size,
            "chunk_size": file_size,
            "total_chunk_count": 1
        }
    }

    try:
        init_res = requests.post(init_url, json=init_payload, headers=headers, timeout=30)
        init_data = init_res.json()
    except Exception as e:
        logger.error(f"Failed to reach TikTok API: {e}")
        return {"success": False, "error": str(e)}

    err = init_data.get("error", {})
    if err.get("code") != "ok":
        err_msg = f"TikTok init failed: {err.get('message', init_res.text)}"
        logger.error(f"❌ {err_msg}")
        return {"success": False, "error": err_msg}

    data = init_data.get("data", {})
    publish_id = data.get("publish_id")
    upload_url = data.get("upload_url")

    if not publish_id or not upload_url:
        return {"success": False, "error": f"Invalid TikTok init response: {init_data}"}

    logger.success(f"✓ [TikTok Initialized] Publish ID: {publish_id}. Streaming video payload...")

    # Step 2: Upload Binary Bytes to TikTok
    with open(p, "rb") as f:
        upload_headers = {
            "Content-Type": "video/mp4",
            "Content-Range": f"bytes 0-{file_size - 1}/{file_size}",
            "Content-Length": str(file_size)
        }
        upload_res = requests.put(upload_url, data=f, headers=upload_headers, timeout=180)
        if upload_res.status_code not in (200, 201, 206):
            err_msg = f"TikTok byte upload failed ({upload_res.status_code}): {upload_res.text}"
            logger.error(f"❌ {err_msg}")
            return {"success": False, "error": err_msg}

    logger.success("✓ [TikTok Upload] Binary payload received by TikTok. Polling publication status...")

    # Step 3: Poll Publish Status
    status_url = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"
    status_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=UTF-8"
    }
    status_payload = {"publish_id": publish_id}

    start_time = time.time()
    while time.time() - start_time < max_wait_sec:
        time.sleep(8)
        try:
            s_res = requests.post(status_url, json=status_payload, headers=status_headers, timeout=15)
            s_data = s_res.json()
            s_status = s_data.get("data", {}).get("status")
            logger.info(f"⏳ TikTok publish status: {s_status} ({int(time.time() - start_time)}s elapsed)")

            if s_status == "SUCCESS":
                logger.success(f"🎉 [TikTok Video Live] Publish ID: {publish_id}")
                if d1_client and video_id:
                    try:
                        d1_client.record_cross_post_attempt(video_id, "tiktok", release_slot, "SUCCESS", permalink=publish_id)
                    except Exception as de:
                        logger.debug(f"D1 record success notice: {de}")
                return {
                    "success": True,
                    "publish_id": publish_id,
                    "status": "SUCCESS"
                }
            elif s_status == "FAILED":
                fail_reason = s_data.get("data", {}).get("fail_reason", "Unknown error")
                logger.error(f"❌ TikTok publish failed: {fail_reason}")
                if d1_client and video_id:
                    try:
                        d1_client.record_cross_post_attempt(video_id, "tiktok", release_slot, "FAILED", error=fail_reason)
                    except Exception as de:
                        logger.debug(f"D1 record failure notice: {de}")
                return {"success": False, "error": fail_reason, "publish_id": publish_id}
        except Exception as pe:
            logger.warning(f"TikTok status poll warning: {pe}")

    logger.warning("Timed out polling TikTok publish status; video is queued asynchronously.")
    return {"success": True, "publish_id": publish_id, "status": "PENDING_ASYNC"}


def publish_tiktok_via_url(
    video_url: str,
    caption: str,
    access_token: Optional[str] = None,
    privacy_level: str = "PUBLIC_TO_EVERYONE"
) -> Dict[str, Any]:
    """
    Submits a video URL for TikTok server-side fetching (PULL_FROM_URL).
    """
    creds = get_tiktok_credentials()
    token = access_token or creds["access_token"]
    if not token:
        return {"success": False, "error": "TIKTOK_ACCESS_TOKEN not configured."}

    init_url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=UTF-8"
    }

    payload = {
        "post_info": {
            "title": caption[:2150],
            "privacy_level": privacy_level,
            "disable_duet": False,
            "disable_stitch": False,
            "disable_comment": False
        },
        "source_info": {
            "source": "PULL_FROM_URL",
            "video_url": video_url
        }
    }

    resp = requests.post(init_url, json=payload, headers=headers, timeout=30)
    data = resp.json()
    err = data.get("error", {})
    if err.get("code") != "ok":
        return {"success": False, "error": err.get("message", resp.text)}

    publish_id = data.get("data", {}).get("publish_id")
    return {"success": True, "publish_id": publish_id}


def refresh_tiktok_token(client_key: str, client_secret: str, refresh_token: str) -> Dict[str, Any]:
    """
    Refreshes TikTok OAuth access token via POST /v2/oauth/token/
    """
    url = "https://open.tiktokapis.com/v2/oauth/token/"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "client_key": client_key,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    resp = requests.post(url, data=payload, headers=headers, timeout=15)
    return resp.json()


if __name__ == "__main__":
    print("TikTok Content Posting Service loaded.")
    test_caption = build_tiktok_seo_caption(
        title="CoreWeave’s High-Stakes Debt vs. Nvidia’s Discipline",
        synopsis="CoreWeave leveraged $7.5B in debt against Nvidia H100 GPUs.",
        youtube_video_id="FwrVEOSmQyg"
    )
    print("Sample TikTok Caption:\n", test_caption)
