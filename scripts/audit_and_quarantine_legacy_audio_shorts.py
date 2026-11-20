#!/usr/bin/env python3
"""
Audit & Quarantine Legacy Defective Audio Shorts (Nov 18 - Nov 19)
scripts/audit_and_quarantine_legacy_audio_shorts.py

This script:
1. Audits the 13 legacy Shorts generated on Nov 18-19 that had breathless, checklist audio.
2. Immediately updates their privacyStatus to 'private' on YouTube to protect algorithmic health.
3. Protects today's 2 newly generated high-retention videos (lSdRmaHCets, m34Yd5TphF0) so they remain public.
"""

import sys
import os
import json
from pathlib import Path
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

LEGACY_DEFECTIVE_SHORTS = [
    {"id": "s5SW3OwKXkE", "title": "Prediction Markets on Drugs", "date": "2026-11-19"},
    {"id": "vPnFvx77V6M", "title": "Fed’s Waller Threatens ‘Shock’ Half-Point Rate Hike", "date": "2026-11-19"},
    {"id": "lClkt_TvxJQ", "title": "Trump’s Hormuz Threat: ‘We Have Their Strait’", "date": "2026-11-19"},
    {"id": "IjU2k_r3Rvk", "title": "China Slowdown Deepens", "date": "2026-11-19"},
    {"id": "K14KcBPMomw", "title": "Copper Plunge Signals AI Buildout Bottleneck", "date": "2026-11-19"},
    {"id": "KgK42RFt7PE", "title": "Fed Warns of Rate Shocks", "date": "2026-11-19"},
    {"id": "dVb40TRt0oo", "title": "JPMorgan Software Bug Freezes Consumer Bank Access", "date": "2026-11-19"},
    {"id": "yhtDcAlzDRI", "title": "Nvidia China AI Dilemma", "date": "2026-11-19"},
    {"id": "WmGV5DgUhng", "title": "Refinancing Cliff: Fed Minutes Reveal AI Inflation Fear", "date": "2026-11-19"},
    {"id": "y0638U9KhTw", "title": "The $4.6 Million Mansion: Robot Soldier Startup Scandal", "date": "2026-11-19"},
    {"id": "97cUHB8hmGw", "title": "Polymarket’s $1.8 Billion Betting Trap", "date": "2026-11-18"},
    {"id": "pdggsUas3tE", "title": "The ‘Disturbing’ Inflation Report and Yield Spikes", "date": "2026-11-18"},
    {"id": "b7wrwY09XU0", "title": "The Medicare Part B Premium Surge of 2026", "date": "2026-11-18"},
]

VERIFIED_GOLD_PUBLIC_SHORTS = ["lSdRmaHCets", "m34Yd5TphF0"]


def audit_and_quarantine():
    logger.info("🔍 [Audio Quality Audit] Scanning 13 legacy shorts generated Nov 18-19 with defective breathless audio...")
    uploader = YouTubeUploader()
    srv = uploader._get_service("en")
    if not srv:
        logger.error("Failed to authenticate YouTube API service.")
        sys.exit(1)

    quarantined = []
    already_private = []
    errors = []

    for item in LEGACY_DEFECTIVE_SHORTS:
        vid = item["id"]
        title = item["title"]

        # Ensure we NEVER touch today's verified gold public shorts
        if vid in VERIFIED_GOLD_PUBLIC_SHORTS:
            logger.info(f"🛡️ Skipping verified gold short: {title} ({vid})")
            continue

        try:
            # Check current status
            res = srv.videos().list(part="status,snippet", id=vid).execute()
            items = res.get("items", [])
            if not items:
                logger.warning(f"Video {vid} ({title}) not found on channel (already deleted or draft).")
                continue

            current_priv = items[0]["status"].get("privacyStatus", "unknown")
            if current_priv == "private":
                logger.info(f"✓ Video {vid} ({title}) is already 'private'. Zero action needed.")
                already_private.append(vid)
                continue

            # Update to private
            body = {"id": vid, "status": {"privacyStatus": "private"}}
            up_res = srv.videos().update(part="status", body=body).execute()
            new_priv = up_res.get("status", {}).get("privacyStatus")
            logger.success(f"🚨 QUARANTINED: '{title}' ({vid}) -> Updated from '{current_priv}' to '{new_priv}'!")
            quarantined.append({"id": vid, "title": title, "previous_status": current_priv, "new_status": new_priv})

        except Exception as e:
            logger.error(f"❌ Failed to quarantine {vid} ({title}): {e}")
            errors.append({"id": vid, "title": title, "error": str(e)})

    logger.info("=" * 60)
    logger.success(f"Audit Complete: {len(quarantined)} legacy videos quarantined to 'private', {len(already_private)} were already private, {len(errors)} errors.")
    logger.info("=" * 60)


if __name__ == "__main__":
    audit_and_quarantine()
