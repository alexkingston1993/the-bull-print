#!/usr/bin/env python3
"""
Upload Script for Viral YouTube Short: The ₹65,700 Cr FII Rotation
Channel: The Bull Print (@thebullprint)
Format: 9:16 Vertical Short
Engine: 100% Kaggle Dual-T4 GPU diffusers plates + 3D Kinetic Typography + Safe-Zone Word Captions
"""

import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

VIDEO_PATH = BASE_DIR / "output" / "the_fii_rotation_viral_short_master.mp4"
SLUG = "the-65700-cr-fii-rotation-why-wall-street-dumps-nvidia-for-indian-bluechips"
ARTICLE_URL = f"https://bullprintmedia.com/article/{SLUG}"

TITLE = "Why Wall Street Dumped Nvidia to Flood India With ₹65,700 Cr #Shorts"

DESCRIPTION = f"""Wall Street algorithms just executed a massive ₹65,700 Crore liquidity rotation: dumping overstretched US tech giants like Nvidia to flood into undervalued Indian bluechips.

As Nvidia's after-hours slide exposed severe AI CapEx exhaustion and power grid constraints, foreign institutional investors (FIIs) shifted liquidity toward high-ROIC banking monopolies and energy heavyweights on Dalal Street.

👉 Read the full investigative forensic report on The Bull Print:
{ARTICLE_URL}

⚡ KEY INSTITUTIONAL HIGHLIGHTS:
• ₹65,700 Cr Rotation: Foreign funds rotate out of crowded US megacaps into Indian equities.
• Silicon Valley Power Wall: 1GW hyperscale clusters face severe delays, compressing forward semiconductor multiples.
• Cash Flow Over Hype: Bluechip banks and infrastructure monopolies trade at attractive dividend-backed margins.
• Retail Warning: Never chase parabolic rallies at all-time highs; track institutional volume absorption.

Subscribe to @TheBullPrint for daily institutional market intelligence and forensic financial documentaries.

⚖️ STATUTORY REGULATORY DISCLAIMER:
Content is provided strictly for educational and informational purposes. The Bull Print and its creators are NOT registered with the Securities and Exchange Board of India (SEBI) as Investment Advisers (IA) or Research Analysts (RA). No information herein constitutes financial advice or an offer to buy/sell securities. Per official SEBI studies, 9 out of 10 individual traders in equity F&O incur net financial losses. Always consult an independent certified financial advisor.

#Shorts #TheBullPrint #Nvidia #IndianStockMarket #Nifty50 #StockMarketIndia #FII #DalalStreet #Investing #Sensex #WallStreet"""

TAGS = [
    "TheBullPrint", "The Bull Print", "Nvidia", "IndianStockMarket",
    "Nifty50", "StockMarketIndia", "FII", "FII DII Flows", "DalalStreet",
    "Wall Street", "Sensex", "Investing", "Shorts", "Stock Market India",
    "Personal Finance India", "Mutual Funds"
]

def upload():
    print("=" * 70)
    print("🚀 UPLOADING VIRAL SHORT TO YOUTUBE: THE FII ROTATION")
    print("=" * 70)

    if not VIDEO_PATH.exists():
        print(f"❌ Error: Video file not found at {VIDEO_PATH}")
        sys.exit(1)

    print(f"File: {VIDEO_PATH.name} ({round(VIDEO_PATH.stat().st_size / 1024 / 1024, 2)} MB)")
    print(f"Title: {TITLE}")
    print(f"Privacy: PUBLIC")

    uploader = YouTubeUploader()

    res = uploader.upload_video(
        language="en",
        video_path=str(VIDEO_PATH),
        title=TITLE,
        description=DESCRIPTION,
        tags=TAGS,
        category_id="25",  # News & Politics
        privacy_status="public",
        is_short=True,
        force_upload=True
    )

    if res.get("success"):
        video_id = res.get("video_id")
        video_url = res.get("url") or f"https://www.youtube.com/shorts/{video_id}"
        print("\n" + "=" * 70)
        print("🎉 SHORT IS LIVE ON YOUTUBE!")
        print(f"🔗 Watch URL: {video_url}")
        print(f"🆔 Video ID: {video_id}")
        print("🌐 Privacy Status: PUBLIC")
        print("=" * 70)
        return video_id, video_url
    else:
        err = res.get("error")
        print(f"\n❌ Upload failed: {err}")
        sys.exit(1)

if __name__ == "__main__":
    upload()

