#!/usr/bin/env python3
"""
Official Meta Instagram Graph API Reels Publisher (The Bull Print)
app/services/instagram_reels_publisher.py

Direct integration with Meta Graph API v21.0:
1. Provisions Reels container via POST /{ig_user_id}/media
2. Polls container status until 'FINISHED'
3. Publishes container via POST /{ig_user_id}/media_publish
4. Auto-generates AI & SEO-optimized entity keyword captions pointing to YouTube
"""

import os
import sys
import time
import json
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_instagram_credentials() -> Dict[str, str]:
    """Retrieves validated Instagram credentials from environment."""
    account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
    access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")

    if not account_id or not access_token:
        # Check .env or config.toml
        from app.config import config
        account_id = account_id or config.app.get("instagram_account_id")
        access_token = access_token or config.app.get("instagram_access_token")

    if not account_id or not access_token:
        raise ValueError("Missing INSTAGRAM_ACCOUNT_ID or INSTAGRAM_ACCESS_TOKEN in environment.")

    return {"account_id": account_id, "access_token": access_token}


QUARANTINED_VIDEO_IDS = {"Z6LEnQyhuvw", "quarantined"}


def build_instagram_seo_caption(title: str, synopsis: str = "", youtube_video_id: str = "", tags: Optional[list] = None) -> str:
    """
    Constructs an AI & SEO-Optimized caption for Instagram Reels using Gemini (gemini-2.5-flash)
    with a deterministic institutional template fallback and clean UTM tracking.
    """
    clean_title = title.replace("| The Bull Print", "").strip()
    api_key = os.getenv("GEMINI_API_KEY")

    yt_link = f"https://youtu.be/{youtube_video_id}?utm_source=instagram&utm_medium=reels&utm_campaign=thebullprint" if youtube_video_id else ""
    portal_link = "https://thebullprint.com/links?utm_source=instagram&utm_medium=reels&utm_campaign=thebullprint"

    if api_key:
        prompt = f"""You are the social media director and SEO strategist for 'The Bull Print' (@thebullprint), an elite institutional macro finance media brand.
Write a high-converting, search-optimized Instagram Reel caption for a short video about:
TITLE: {clean_title}
SUMMARY / CONTEXT: {synopsis or clean_title}
YOUTUBE VIDEO ID: {youtube_video_id or 'latest'}

MANDATORY STRUCTURE:
1. LINE 1: UPPERCASE punchy hook headline + specific financial shock figure (e.g. "$7.5B DEBT TRAP", "21% PREMIUM SURGE", "1.3M TRAPPED").
2. PARAGRAPH 2: 2–3 dense sentences explicitly naming primary institutions, central banks, tickers, dollar amounts, and macro catalysts for search indexers.
3. PARAGRAPH 3: Exactly "Financial freedom for everyone through financial literacy. 💡"
4. PARAGRAPH 4:
📌 Watch the full 12-minute institutional breakdown on YouTube — tap the link in our bio (@thebullprint) or search "{clean_title}" on YouTube ({yt_link or 'youtu.be/' + (youtube_video_id or 'latest')}).
🌐 Portal: {portal_link} | 📘 Facebook: The Bull Print
5. FOOTER: #TheBullPrint #MacroEconomics #FinancialLiteracy #InstitutionalTrading plus 3 to 4 hyper-relevant entity hashtags.

Output ONLY the final caption text. Zero conversational meta-commentary, zero intro, zero markdown code fences."""

        models_to_try = ["gemini-2.5-flash", "gemini-flash-latest", "gemini-flash-lite-latest"]
        import requests
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
                            if len(ai_caption) > 100:
                                return ai_caption[:2150]
            except Exception as e:
                logger.debug(f"Gemini caption generation note ({model}): {e}")

    # Deterministic Institutional Fallback Template with clean UTM parameters
    upper_hook = clean_title.upper()
    summary_part = synopsis.strip() if synopsis else (
        f"Forensic breakdown of institutional capital flows, regulatory actions, "
        f"and macro order book dynamics driving {clean_title}."
    )
    mission_anchor = "Financial freedom for everyone through financial literacy. 💡"
    cta_part = (
        f"📌 Watch the full 12-minute institutional breakdown on YouTube — "
        f"tap the link in our bio (@thebullprint) or search \"{clean_title}\" on YouTube"
        + (f" ({yt_link})." if yt_link else ".")
        + f"\n🌐 Portal: {portal_link} | 📘 Facebook: The Bull Print"
    )
    save_cta = "Save this briefing for market open & drop your outlook below. 👇"

    default_tags = ["#TheBullPrint", "#MacroEconomics", "#FinancialLiteracy", "#InstitutionalTrading", "#GlobalLiquidity"]
    if tags:
        custom_tags = [f"#{t.replace(' ', '')}" for t in tags[:3] if not t.startswith("#")]
        all_tags = default_tags[:3] + custom_tags
    else:
        all_tags = default_tags

    caption = (
        f"{upper_hook} 🚨\n\n"
        f"{summary_part}\n\n"
        f"{mission_anchor}\n\n"
        f"{cta_part}\n\n"
        f"{save_cta}\n\n"
        f"{' '.join(all_tags)}"
    )
    return caption[:2150]


def publish_instagram_reel(
    video_url: str,
    caption: str,
    cover_url: Optional[str] = None,
    account_id: Optional[str] = None,
    access_token: Optional[str] = None,
    max_wait_sec: int = 300,
    video_id: str = "",
    release_slot: str = "routine"
) -> Dict[str, Any]:
    """
    Executes the 2-step Instagram Reels publishing pipeline via Meta Graph API v21.0
    with strict quarantine blocking and Cloudflare D1 idempotency protection.
    """
    # 1. Quarantine Guardrail
    if video_id in QUARANTINED_VIDEO_IDS or "Z6LEnQyhuvw" in (caption or ""):
        logger.warning(f"🚫 [Quarantine Gate] Video '{video_id}' is permanently quarantined. Aborting Instagram publish.")
        return {"success": False, "error": "Blocked by quarantine guardrail", "quarantined": True}

    # 2. Idempotency Check via Cloudflare D1
    d1_client = None
    if video_id:
        try:
            from app.services.cloudflare_r2_vault import CloudflareD1Client
            d1_client = CloudflareD1Client()
            existing = d1_client.check_cross_post_idempotency(video_id, "instagram", release_slot)
            if existing and existing.get("status") == "SUCCESS":
                logger.info(f"⏭️ [Idempotency Gate] Video '{video_id}' already published to Instagram for slot '{release_slot}'. Skipping duplicate.")
                return {"success": True, "skipped": True, "permalink": existing.get("permalink")}
        except Exception as de:
            logger.debug(f"D1 idempotency check notice: {de}")

    creds = get_instagram_credentials()
    ig_id = account_id or creds["account_id"]
    token = access_token or creds["access_token"]

    logger.info(f"📸 [Instagram Publisher] Initializing Reel container for Account: {ig_id}...")

    # Step 1: Create Container
    container_url = f"https://graph.facebook.com/v21.0/{ig_id}/media"
    container_params = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "share_to_feed": "true",
        "access_token": token
    }
    if cover_url:
        container_params["cover_url"] = cover_url

    encoded_data = urllib.parse.urlencode(container_params).encode("utf-8")
    req = urllib.request.Request(container_url, data=encoded_data, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            container_res = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode()
        logger.error(f"❌ Failed to create Instagram Reel container: {err_msg}")
        return {"success": False, "error": err_msg}

    creation_id = container_res.get("id")
    if not creation_id:
        return {"success": False, "error": f"No creation_id returned: {container_res}"}

    logger.success(f"✓ [Instagram Container Created] ID: {creation_id}. Polling processing status...")

    # Step 2: Poll Container Status
    status_url = f"https://graph.facebook.com/v21.0/{creation_id}?fields=status_code,status&access_token={token}"
    start_time = time.time()
    while time.time() - start_time < max_wait_sec:
        time.sleep(10)
        try:
            with urllib.request.urlopen(status_url, timeout=15) as s_resp:
                s_data = json.loads(s_resp.read().decode())
                status_code = s_data.get("status_code")
                logger.info(f"⏳ Reel processing status: {status_code} ({int(time.time() - start_time)}s elapsed)")

                if status_code == "FINISHED":
                    logger.success("✓ Reel container processing finished! Ready to publish.")
                    break
                elif status_code in ("ERROR", "EXPIRED"):
                    return {"success": False, "error": f"Reel processing failed with status: {status_code}"}
        except Exception as pe:
            logger.warning(f"Polling warning: {pe}")

    # Step 3: Publish Media
    logger.info(f"🚀 Publishing Reel {creation_id} to @thebullprint feed...")
    publish_url = f"https://graph.facebook.com/v21.0/{ig_id}/media_publish"
    pub_data = urllib.parse.urlencode({
        "creation_id": creation_id,
        "access_token": token
    }).encode("utf-8")

    pub_req = urllib.request.Request(publish_url, data=pub_data, method="POST")
    try:
        with urllib.request.urlopen(pub_req, timeout=30) as p_resp:
            pub_res = json.loads(p_resp.read().decode())
    except urllib.error.HTTPError as pe:
        err_msg = pe.read().decode()
        logger.error(f"❌ Failed to publish Instagram Reel: {err_msg}")
        return {"success": False, "error": err_msg}

    media_id = pub_res.get("id")
    if not media_id:
        return {"success": False, "error": f"No published media ID returned: {pub_res}"}

    # Fetch permalink
    permalink = f"https://www.instagram.com/reel/{media_id}/"
    try:
        media_url = f"https://graph.facebook.com/v21.0/{media_id}?fields=permalink&access_token={token}"
        with urllib.request.urlopen(media_url, timeout=10) as m_resp:
            m_data = json.loads(m_resp.read().decode())
            permalink = m_data.get("permalink", permalink)
    except Exception:
        pass

    logger.success(f"🎉 [Instagram Reel Published] ID: {media_id} | Permalink: {permalink}")
    if d1_client and video_id:
        try:
            d1_client.record_cross_post_attempt(video_id, "instagram", release_slot, "SUCCESS", permalink=permalink)
        except Exception as de:
            logger.debug(f"D1 record success notice: {de}")

    return {
        "success": True,
        "media_id": media_id,
        "permalink": permalink,
        "creation_id": creation_id
    }


def publish_local_mp4_reel(
    video_path: str,
    caption: str,
    account_id: Optional[str] = None,
    access_token: Optional[str] = None,
    max_wait_sec: int = 300,
    video_id: str = "",
    release_slot: str = "routine"
) -> Dict[str, Any]:
    """
    Publishes a local .mp4 video file to Instagram Reels using the official
    Meta Graph API Resumable Upload protocol (rupload.facebook.com)
    with strict quarantine blocking and Cloudflare D1 idempotency protection.
    """
    # 1. Quarantine Guardrail
    if video_id in QUARANTINED_VIDEO_IDS or "Z6LEnQyhuvw" in (caption or "") or "Z6LEnQyhuvw" in video_path:
        logger.warning(f"🚫 [Quarantine Gate] Video '{video_id}' is permanently quarantined. Aborting Instagram publish.")
        return {"success": False, "error": "Blocked by quarantine guardrail", "quarantined": True}

    # 2. Idempotency Check via Cloudflare D1
    d1_client = None
    if video_id:
        try:
            from app.services.cloudflare_r2_vault import CloudflareD1Client
            d1_client = CloudflareD1Client()
            existing = d1_client.check_cross_post_idempotency(video_id, "instagram", release_slot)
            if existing and existing.get("status") == "SUCCESS":
                logger.info(f"⏭️ [Idempotency Gate] Video '{video_id}' already published to Instagram for slot '{release_slot}'. Skipping duplicate.")
                return {"success": True, "skipped": True, "permalink": existing.get("permalink")}
        except Exception as de:
            logger.debug(f"D1 idempotency check notice: {de}")

    import requests
    creds = get_instagram_credentials()
    ig_id = account_id or creds["account_id"]
    token = access_token or creds["access_token"]

    p = Path(video_path)
    if not p.exists():
        return {"success": False, "error": f"File not found: {video_path}"}
    file_size = p.stat().st_size

    logger.info(f"📸 [Instagram Resumable Upload] Initializing container for {p.name} ({file_size // 1024} KB)...")

    # Step 1: Initialize Resumable Container
    init_url = f"https://graph.facebook.com/v21.0/{ig_id}/media"
    init_data = {
        "media_type": "REELS",
        "upload_type": "resumable",
        "caption": caption,
        "share_to_feed": "true",
        "access_token": token
    }
    init_res = requests.post(init_url, data=init_data, timeout=30)
    if init_res.status_code != 200:
        return {"success": False, "error": f"Container init failed ({init_res.status_code}): {init_res.text}"}

    init_json = init_res.json()
    creation_id = init_json.get("id")
    upload_uri = init_json.get("uri")

    if not creation_id or not upload_uri:
        return {"success": False, "error": f"Invalid init response: {init_json}"}

    logger.success(f"✓ Container ID: {creation_id}. Streaming binary video bytes to Meta...")

    # Step 2: Stream bytes to Meta rupload endpoint
    with open(p, "rb") as f:
        headers = {
            "Authorization": f"OAuth {token}",
            "offset": "0",
            "file_size": str(file_size),
            "Content-Type": "application/octet-stream"
        }
        upload_resp = requests.post(upload_uri, data=f, headers=headers, timeout=120)
        if upload_resp.status_code not in (200, 201):
            return {"success": False, "error": f"Binary upload failed ({upload_resp.status_code}): {upload_resp.text}"}

    logger.success("✓ Video bytes uploaded successfully to Meta! Polling encoding status...")

    # Step 3: Poll status
    status_url = f"https://graph.facebook.com/v21.0/{creation_id}?fields=status_code,status&access_token={token}"
    start_time = time.time()
    while time.time() - start_time < max_wait_sec:
        time.sleep(6)
        s_res = requests.get(status_url, timeout=15)
        if s_res.status_code == 200:
            status_data = s_res.json()
            code = status_data.get("status_code")
            logger.info(f"⏳ Reel processing: {code} ({int(time.time() - start_time)}s)")
            if code == "FINISHED":
                break
            elif code in ("ERROR", "EXPIRED"):
                return {"success": False, "error": f"Container processing failed: {code}"}

    # Step 4: Publish
    logger.info(f"🚀 Publishing Reel container {creation_id} to @thebullprint...")
    pub_url = f"https://graph.facebook.com/v21.0/{ig_id}/media_publish"
    pub_res = requests.post(pub_url, data={"creation_id": creation_id, "access_token": token}, timeout=30)
    if pub_res.status_code != 200:
        return {"success": False, "error": f"Media publish failed ({pub_res.status_code}): {pub_res.text}"}

    media_id = pub_res.json().get("id")
    permalink = f"https://www.instagram.com/reel/{media_id}/"
    try:
        m_res = requests.get(f"https://graph.facebook.com/v21.0/{media_id}?fields=permalink&access_token={token}", timeout=10)
        if m_res.status_code == 200:
            permalink = m_res.json().get("permalink", permalink)
    except Exception:
        pass

    logger.success(f"🎉 [Instagram Reel Published] ID: {media_id} | Permalink: {permalink}")
    if d1_client and video_id:
        try:
            d1_client.record_cross_post_attempt(video_id, "instagram", release_slot, "SUCCESS", permalink=permalink)
        except Exception as de:
            logger.debug(f"D1 record success notice: {de}")

    return {
        "success": True,
        "media_id": media_id,
        "permalink": permalink,
        "creation_id": creation_id
    }


def refresh_instagram_long_lived_token(app_id: str, app_secret: str, current_token: str) -> Dict[str, Any]:
    """
    Exchanges short-lived or existing long-lived token for fresh 60-day token.
    """
    url = (
        "https://graph.facebook.com/v21.0/oauth/access_token?"
        f"grant_type=fb_exchange_token&"
        f"client_id={app_id}&"
        f"client_secret={app_secret}&"
        f"fb_exchange_token={current_token}"
    )
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode())

