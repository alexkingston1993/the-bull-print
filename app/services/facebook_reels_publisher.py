#!/usr/bin/env python3
"""
app/services/facebook_reels_publisher.py
Official Meta Graph API Facebook Page Reels Publisher (The Bull Print)

Publishes short-form video reels directly to Facebook Page:
1. Resumable binary upload to graph.facebook.com/v21.0/{page_id}/video_reels
2. Strict Cloudflare D1 idempotency checks (never double-posts)
3. Strict quarantine gate (permanently blocks Z6LEnQyhuvw)
4. AI/SEO caption generation with UTM tracking and core mission anchor
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
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

QUARANTINED_VIDEO_IDS = {"Z6LEnQyhuvw", "quarantined"}


def get_facebook_credentials() -> Dict[str, str]:
    """Retrieves validated Facebook Page credentials from environment or meta_tokens.json."""
    page_id = os.getenv("FACEBOOK_PAGE_ID", "")
    page_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")

    if not page_id or not page_token:
        # Check local data/meta_tokens.json
        token_path = BASE_DIR / "data" / "meta_tokens.json"
        if token_path.exists():
            try:
                data = json.loads(token_path.read_text(encoding="utf-8"))
                page_id = page_id or data.get("page_id", "")
                page_token = page_token or data.get("page_access_token", "")
            except Exception:
                pass

    if not page_id or not page_token:
        # Check config.toml
        try:
            from app.config import config
            page_id = page_id or config.app.get("facebook_page_id", "")
            page_token = page_token or config.app.get("facebook_page_access_token", "")
        except Exception:
            pass

    return {"page_id": page_id, "page_token": page_token}


def build_facebook_seo_caption(
    title: str,
    synopsis: str = "",
    youtube_video_id: str = "",
    tags: Optional[List[str]] = None
) -> str:
    """
    Constructs an AI & SEO-Optimized caption for Facebook Page Reels with clean UTM tracking.
    """
    clean_title = title.replace("| The Bull Print", "").strip()
    api_key = os.getenv("GEMINI_API_KEY")

    yt_link = f"https://youtu.be/{youtube_video_id}?utm_source=facebook&utm_medium=reels&utm_campaign=thebullprint" if youtube_video_id else ""
    portal_link = "https://thebullprint.com/links?utm_source=facebook&utm_medium=reels&utm_campaign=thebullprint"

    if api_key:
        prompt = f"""You are the Social Media & Community Director for 'The Bull Print' Facebook Page, an elite macro finance media brand.
Write an engaging, high-retention Facebook Reel description for:
TITLE: {clean_title}
CONTEXT: {synopsis or clean_title}
YOUTUBE VIDEO ID: {youtube_video_id or 'latest'}

MANDATORY STRUCTURE:
1. LINE 1: High-impact UPPERCASE headline + specific dollar figure/metric (e.g. "$7.5B LIQUIDITY TRAP 🚨").
2. PARAGRAPH 2: 2–3 dense, informative sentences explaining the institutional mechanism, central bank action, and macroeconomic impact.
3. PARAGRAPH 3: Exactly "Financial freedom for everyone through financial literacy. 💡"
4. PARAGRAPH 4:
📌 Watch the full 12-minute institutional breakdown on YouTube ({yt_link or 'youtu.be/' + (youtube_video_id or 'latest')}).
🌐 Data & Research Hub: {portal_link}
5. FOOTER: #TheBullPrint #MacroEconomics #FinancialLiteracy #StockMarket #Investing plus 3 relevant entity tags.

Output ONLY the final description. Zero conversational filler, zero markdown formatting."""

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
                            if len(ai_caption) > 100:
                                return ai_caption[:2150]
            except Exception as e:
                logger.debug(f"Facebook Gemini caption notice ({model}): {e}")

    # Deterministic Fallback Template
    upper_hook = clean_title.upper()
    summary_part = synopsis.strip() if synopsis else (
        f"Forensic breakdown of sovereign liquidity flows, regulatory interventions, "
        f"and institutional order book dynamics driving {clean_title}."
    )
    mission_anchor = "Financial freedom for everyone through financial literacy. 💡"
    cta_part = (
        f"📌 Watch the full 12-minute institutional breakdown on YouTube: {yt_link}\n"
        f"🌐 Research & Analytical Tools: {portal_link}\n"
        f"👉 Follow The Bull Print for daily macro briefings."
    )

    default_tags = ["#TheBullPrint", "#MacroEconomics", "#FinancialLiteracy", "#StockMarket", "#GlobalLiquidity"]
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
        f"{' '.join(all_tags)}"
    )
    return caption[:2150]


def publish_local_facebook_reel(
    video_path: str,
    caption: str,
    page_id: Optional[str] = None,
    page_token: Optional[str] = None,
    video_id: str = "",
    release_slot: str = "routine",
    max_wait_sec: int = 300
) -> Dict[str, Any]:
    """
    Publishes a local .mp4 video to Facebook Page Reels using Meta Graph API v21.0.
    Includes strict quarantine filtering and Cloudflare D1 idempotency checks.
    """
    # 1. Quarantine Guardrail
    if video_id in QUARANTINED_VIDEO_IDS or "Z6LEnQyhuvw" in (caption or "") or "Z6LEnQyhuvw" in video_path:
        logger.warning(f"🚫 [Quarantine Gate] Video '{video_id}' is quarantined. Aborting Facebook publish.")
        return {"success": False, "error": "Blocked by quarantine guardrail", "quarantined": True}

    # 2. Idempotency Check via Cloudflare D1
    d1_client = None
    if video_id:
        try:
            from app.services.cloudflare_r2_vault import CloudflareD1Client
            d1_client = CloudflareD1Client()
            existing = d1_client.check_cross_post_idempotency(video_id, "facebook", release_slot)
            if existing and existing.get("status") == "SUCCESS":
                logger.info(f"⏭️ [Idempotency Gate] Video '{video_id}' already published to Facebook for slot '{release_slot}'. Skipping.")
                return {"success": True, "skipped": True, "permalink": existing.get("permalink")}
        except Exception as de:
            logger.debug(f"D1 idempotency check notice: {de}")

    creds = get_facebook_credentials()
    fb_page_id = page_id or creds["page_id"]
    fb_token = page_token or creds["page_token"]

    if not fb_page_id or not fb_token:
        err = "Missing FACEBOOK_PAGE_ID or FACEBOOK_PAGE_ACCESS_TOKEN."
        logger.error(f"❌ {err}")
        return {"success": False, "error": err}

    p = Path(video_path)
    if not p.exists():
        return {"success": False, "error": f"File not found: {video_path}"}
    file_size = p.stat().st_size

    logger.info(f"📘 [Facebook Publisher] Initializing Reel upload for '{p.name}' to Page {fb_page_id}...")

    # Step 1: Initialize Reel Upload Session
    init_url = f"https://graph.facebook.com/v21.0/{fb_page_id}/video_reels"
    init_params = {
        "upload_phase": "start",
        "access_token": fb_token
    }
    try:
        init_res = requests.post(init_url, data=init_params, timeout=30)
        init_data = init_res.json()
    except Exception as e:
        logger.error(f"Failed to initialize Facebook Reel session: {e}")
        return {"success": False, "error": str(e)}

    fb_video_id = init_data.get("video_id")
    upload_url = init_data.get("upload_url")

    if not fb_video_id or not upload_url:
        logger.error(f"❌ Facebook Reel initialization failed: {init_data}")
        return {"success": False, "error": f"Initialization failed: {init_data}"}

    logger.success(f"✓ Facebook Reel session created: ID {fb_video_id}. Uploading binary bytes...")

    # Step 2: Upload Video File
    try:
        with open(p, "rb") as f:
            headers = {
                "Authorization": f"OAuth {fb_token}",
                "offset": "0",
                "file_size": str(file_size),
                "Content-Type": "application/octet-stream"
            }
            upload_res = requests.post(upload_url, data=f, headers=headers, timeout=120)
            if upload_res.status_code not in (200, 201):
                err_msg = f"Binary upload failed ({upload_res.status_code}): {upload_res.text}"
                logger.error(f"❌ {err_msg}")
                if d1_client and video_id:
                    d1_client.record_cross_post_attempt(video_id, "facebook", release_slot, "FAILED", error=err_msg)
                return {"success": False, "error": err_msg}
    except Exception as ue:
        logger.error(f"Error streaming video to Facebook: {ue}")
        return {"success": False, "error": str(ue)}

    logger.success("✓ Video binary uploaded to Facebook! Publishing Reel...")

    # Step 3: Finish and Publish
    finish_url = f"https://graph.facebook.com/v21.0/{fb_page_id}/video_reels"
    finish_params = {
        "upload_phase": "finish",
        "video_id": fb_video_id,
        "video_state": "PUBLISHED",
        "description": caption[:2150],
        "access_token": fb_token
    }

    try:
        fin_res = requests.post(finish_url, data=finish_params, timeout=30)
        fin_data = fin_res.json()
    except Exception as fe:
        logger.error(f"Failed to finish Facebook Reel publish: {fe}")
        return {"success": False, "error": str(fe)}

    if not fin_data.get("success"):
        logger.error(f"❌ Facebook Reel finish failed: {fin_data}")
        if d1_client and video_id:
            d1_client.record_cross_post_attempt(video_id, "facebook", release_slot, "FAILED", error=str(fin_data))
        return {"success": False, "error": str(fin_data)}

    permalink = f"https://www.facebook.com/reel/{fb_video_id}/"
    logger.success(f"🎉 [Facebook Reel Published] ID: {fb_video_id} | Permalink: {permalink}")

    # Record in D1 Ledger
    if d1_client and video_id:
        try:
            d1_client.record_cross_post_attempt(video_id, "facebook", release_slot, "SUCCESS", permalink=permalink)
        except Exception as de:
            logger.debug(f"D1 record success notice: {de}")

    return {
        "success": True,
        "video_id": fb_video_id,
        "permalink": permalink
    }
