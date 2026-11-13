#!/usr/bin/env python3
"""
Upload and Schedule 10 Viral Catchy Shorts (Past 24h News)
Channel: The Bull Print (@thebullprint)
Format: 9:16 Vertical Shorts
Scheduled across peak viral intervals throughout today.
"""

import os
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

SHORTS_DIR = BASE_DIR / "output" / "viral_shorts_past24h"
RENDERED_DIR = SHORTS_DIR / "rendered"
FRAMES_DIR = SHORTS_DIR / "frames"

# 10 Shorts Metadata with high-converting titles, descriptions & hashtags
SHORTS_META = [
    {
        "id": "short_01",
        "num": 1,
        "title": "Nvidia Crushes Apple: The $5 Trillion Crown #Shorts",
        "description": "Nvidia officially surpasses Apple to become the most valuable company in human history, racing toward a $5 Trillion market cap as AI chip dominance squeezes Big Tech margins.\n\n#TheBullPrint #Nvidia #Apple #StockMarket #AI #NVDA #WallStreet #Shorts",
        "tags": ["#TheBullPrint", "#Nvidia", "#Apple", "#StockMarket", "#AI", "#NVDA", "#WallStreet", "#Shorts"],
        "offset_minutes": 15, # 1:15 PM IST (Immediate release)
    },
    {
        "id": "short_02",
        "num": 2,
        "title": "The $2.5 Trillion Wipeout: Wall Street AI Panic #Shorts",
        "description": "$2.5 Trillion wiped out from the Nasdaq as antitrust fears, post-midterm political shockwaves, and the looming power grid bottleneck hit tech giants.\n\n#TheBullPrint #Nasdaq #MarketCrash #TechStocks #WallStreet #AI #Shorts",
        "tags": ["#TheBullPrint", "#Nasdaq", "#MarketCrash", "#TechStocks", "#WallStreet", "#AI", "#Shorts"],
        "offset_minutes": 90, # 2:30 PM IST (Europe Open)
    },
    {
        "id": "short_03",
        "num": 3,
        "title": "Elon Musk Kills Cybertruck: The Cybercab Pivot #Shorts",
        "description": "Elon Musk confirms Cybertruck production winds down by 2027 as Tesla pivots all capex into autonomous Cybercabs and xAI's Colossus cluster.\n\n#TheBullPrint #ElonMusk #Tesla #Cybercab #Cybertruck #Robotaxi #xAI #Shorts",
        "tags": ["#TheBullPrint", "#ElonMusk", "#Tesla", "#Cybercab", "#Cybertruck", "#Robotaxi", "#xAI", "#Shorts"],
        "offset_minutes": 165, # 3:45 PM IST (US Pre-Market)
    },
    {
        "id": "short_04",
        "num": 4,
        "title": "Diwali Muhurat Trading: Nifty Below 25,000 #Shorts",
        "description": "Nifty snaps 7-day winning streak in Samvat 2083 Muhurat session. FII selling collides with ₹25,000 Cr monthly domestic retail SIP inflows.\n\n#TheBullPrint #Nifty50 #MuhuratTrading #StockMarketIndia #Sensex #FII #MutualFunds #Shorts",
        "tags": ["#TheBullPrint", "#Nifty50", "#MuhuratTrading", "#StockMarketIndia", "#Sensex", "#FII", "#MutualFunds", "#Shorts"],
        "offset_minutes": 240, # 5:00 PM IST (India Closing Bell)
    },
    {
        "id": "short_05",
        "num": 5,
        "title": "OpenAI's $1.25 Trillion Round vs Anthropic IPO #Shorts",
        "description": "OpenAI raises $11 Billion at $1.25T valuation while Anthropic prepares its IPO roadshow. Can AI software generate enough cash to justify trillion-dollar valuations?\n\n#TheBullPrint #OpenAI #SamAltman #Anthropic #VentureCapital #AI #IPO #Shorts",
        "tags": ["#TheBullPrint", "#OpenAI", "#SamAltman", "#Anthropic", "#VentureCapital", "#AI", "#IPO", "#Shorts"],
        "offset_minutes": 315, # 6:15 PM IST (US Market Open rush)
    },
    {
        "id": "short_06",
        "num": 6,
        "title": "Gold Hits All-Time Highs: The Dollar Flight #Shorts",
        "description": "Spot gold surges to record territory as central banks accelerate their flight away from fiat currency amid US debt expansion and falling yields.\n\n#TheBullPrint #GoldPrice #CentralBanks #USFederalReserve #GoldBullion #MacroFinance #Shorts",
        "tags": ["#TheBullPrint", "#GoldPrice", "#CentralBanks", "#USFederalReserve", "#GoldBullion", "#MacroFinance", "#Shorts"],
        "offset_minutes": 390, # 7:30 PM IST (Prime evening)
    },
    {
        "id": "short_07",
        "num": 7,
        "title": "Brent Crude Drops to $100: Inflation Relief #Shorts",
        "description": "Crude oil plunges toward $100 as geopolitical supply fears ease. Central banks get inflation breathing room while energy producers brace for revenue shock.\n\n#TheBullPrint #CrudeOil #OPEC #Inflation #EnergyCrisis #Economy #Shorts",
        "tags": ["#TheBullPrint", "#CrudeOil", "#OPEC", "#Inflation", "#EnergyCrisis", "#Economy", "#Shorts"],
        "offset_minutes": 465, # 8:45 PM IST (Prime US Lunch)
    },
    {
        "id": "short_08",
        "num": 8,
        "title": "The Memory Chip Crisis: Why Big Tech Is Panicking #Shorts",
        "description": "Apple warns margins are squeezed by High Bandwidth Memory shortages. Generative AI clusters consume so much DRAM that the hardware bottleneck is no longer just GPUs.\n\n#TheBullPrint #Semiconductors #ChipShortage #HBM #Apple #Hardware #AI #Shorts",
        "tags": ["#TheBullPrint", "#Semiconductors", "#ChipShortage", "#HBM", "#Apple", "#Hardware", "#AI", "#Shorts"],
        "offset_minutes": 540, # 10:00 PM IST (US Afternoon)
    },
    {
        "id": "short_09",
        "num": 9,
        "title": "The 2030 Power Wall: Big Tech Buys Nuclear #Shorts",
        "description": "Microsoft, Amazon, and Google buy up atomic power plants as data centers threaten to outstrip national grids. The race for atomic baseload megawatts is on.\n\n#TheBullPrint #NuclearEnergy #BigTech #AI #DataCenters #CleanEnergy #Shorts",
        "tags": ["#TheBullPrint", "#NuclearEnergy", "#BigTech", "#AI", "#DataCenters", "#CleanEnergy", "#Shorts"],
        "offset_minutes": 615, # 11:15 PM IST (US Market Close)
    },
    {
        "id": "short_10",
        "num": 10,
        "title": "Bitcoin Short Squeeze: The Liquidity Rebound #Shorts",
        "description": "$1.2 Billion in Bitcoin shorts liquidated in 24 hours. Central bank monetary easing signals send macro liquidity cascading back into digital assets.\n\n#TheBullPrint #Bitcoin #CryptoMarket #ShortSqueeze #BTC #Liquidity #ETF #Shorts",
        "tags": ["#TheBullPrint", "#Bitcoin", "#CryptoMarket", "#ShortSqueeze", "#BTC", "#Liquidity", "#ETF", "#Shorts"],
        "offset_minutes": 690, # 12:30 AM IST (US After-Hours Wrap)
    }
]

def main():
    print("=" * 75)
    print("🚀 SCHEDULING & UPLOADING 10 VIRAL PAST 24H SHORTS TO YOUTUBE")
    print("=" * 75)

    uploader = YouTubeUploader()
    now_utc = datetime.now(timezone.utc)
    results = []

    for item in SHORTS_META:
        sid = item["id"]
        v_path = RENDERED_DIR / f"{sid}.mp4"
        t_path = FRAMES_DIR / sid / "frame_01.jpg"

        if not v_path.exists():
            print(f"❌ Missing video: {v_path}")
            continue

        # Calculate scheduled release time
        offset = item["offset_minutes"]
        target_dt = now_utc + timedelta(minutes=offset)
        # Format as RFC 3339 (e.g. 2026-11-09T14:30:00Z)
        target_iso = target_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        ist_dt = target_dt + timedelta(hours=5, minutes=30)
        ist_str = ist_dt.strftime("%I:%M %p IST")

        print(f"\n[{item['num']:02d}/10] Uploading: {item['title']}")
        print(f"   Target Timing: {ist_str} (UTC: {target_iso})")
        print(f"   Video: {v_path.name} ({v_path.stat().st_size / 1024 / 1024:.2f} MB)")
        print(f"   Thumbnail: {t_path.name}")

        try:
            # If offset is small (< 20 mins), publish as public immediately!
            if offset <= 20:
                print(f"   ⚡ Publishing as PUBLIC immediately!")
                res = uploader.upload_video(
                    language="en",
                    video_path=str(v_path),
                    title=item["title"],
                    description=item["description"],
                    tags=item["tags"],
                    category_id="27", # Education
                    privacy_status="public",
                    is_short=True,
                    thumbnail_path=str(t_path) if t_path.exists() else None,
                    force_upload=True
                )
            else:
                print(f"   ⏰ Scheduling release for {ist_str} ({target_iso})")
                res = uploader.upload_video(
                    language="en",
                    video_path=str(v_path),
                    title=item["title"],
                    description=item["description"],
                    tags=item["tags"],
                    category_id="27",
                    privacy_status="private",
                    publish_at=target_iso,
                    is_short=True,
                    thumbnail_path=str(t_path) if t_path.exists() else None,
                    force_upload=True
                )

            if res.get("success"):
                vid_id = res.get("video_id")
                url = res.get("url")
                print(f"   🎉 SUCCESS: {url} (ID: {vid_id})")
                results.append((item["num"], item["title"], url, ist_str, "SCHEDULED/LIVE"))
            else:
                print(f"   ❌ FAILED: {res.get('error')}")
                results.append((item["num"], item["title"], None, ist_str, f"FAILED: {res.get('error')}"))
        except Exception as e:
            print(f"   ❌ EXCEPTION: {e}")
            results.append((item["num"], item["title"], None, ist_str, f"ERROR: {e}"))

        time.sleep(3)

    print("\n" + "=" * 75)
    print("📋 10 VIRAL SHORTS UPLOAD & SCHEDULE SUMMARY:")
    print("=" * 75)
    for num, title, url, timing, status in results:
        print(f"Short {num:02d} [{timing}]: [{status}] {title}")
        if url:
            print(f"   -> {url}")

if __name__ == "__main__":
    main()
