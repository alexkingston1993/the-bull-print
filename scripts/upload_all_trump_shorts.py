#!/usr/bin/env python3
"""
Upload Pipeline for all 10 Trump Election & Dalal Street YouTube Shorts
Channel: The Bull Print
"""

import os
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

SHORTS_META = [
    {
        "id": 1,
        "title": "Why Trump's Win Crashes the Indian Rupee to ₹85 #Shorts",
        "description": "Donald Trump's election victory triggers a surging US Dollar Index, sending USD/INR testing ₹85. How it impacts India's crude oil import bill, inflation, and IT/Pharma exporters.\n\n#TheBullPrint #Trump #IndianRupee #DalalStreet #Forex #StockMarketIndia #USDINR #Shorts",
        "tags": ["#TheBullPrint", "#Trump", "#IndianRupee", "#DalalStreet", "#Forex", "#StockMarketIndia", "#USDINR", "#Shorts"]
    },
    {
        "id": 2,
        "title": "Trump's 60% China Tariff: India's Manufacturing Jackpot #Shorts",
        "description": "Trump's blanket 60% tariffs on Chinese goods accelerate the China+1 shift to Indian electronics manufacturers like Dixon and Tata Electronics.\n\n#TheBullPrint #Trump #ChinaTariff #MakeInIndia #DixonTechnologies #StockMarketIndia #Shorts",
        "tags": ["#TheBullPrint", "#Trump", "#ChinaTariff", "#MakeInIndia", "#DixonTechnologies", "#StockMarketIndia", "#Shorts"]
    },
    {
        "id": 3,
        "title": "H-1B Visa Panic vs 15% US Tax Cut: Will Indian IT Crash? #Shorts",
        "description": "Will H-1B restrictions crush TCS and Infosys, or will Trump's 15% US corporate tax cut unleash enterprise tech spending? Here is the real balance sheet truth.\n\n#TheBullPrint #TCS #Infosys #H1B #Trump #IndianIT #DalalStreet #Shorts",
        "tags": ["#TheBullPrint", "#TCS", "#Infosys", "#H1B", "#Trump", "#IndianIT", "#DalalStreet", "#Shorts"]
    },
    {
        "id": 4,
        "title": "Trump's Secret ₹50,000 Cr Weapons Axis with India #Shorts",
        "description": "From GE F414 jet engine transfers to MQ-9B Predator drones, why Trump 2.0 supercharges Indian defense PSUs like HAL, BEL, and Mazagon Dock.\n\n#TheBullPrint #DefenseStocks #HAL #BharatElectronics #Trump #DalalStreet #Shorts",
        "tags": ["#TheBullPrint", "#DefenseStocks", "#HAL", "#BharatElectronics", "#Trump", "#DalalStreet", "#Shorts"]
    },
    {
        "id": 5,
        "title": "Bitcoin at $100K Under Trump: The 30% Indian Tax Disaster #Shorts",
        "description": "As Trump pledges a US Strategic Bitcoin Reserve, why 2 crore Indian crypto holders are trapped by a 30% flat tax and 1% TDS.\n\n#TheBullPrint #Bitcoin #CryptoIndia #Trump #BTC #CryptoTax #Shorts",
        "tags": ["#TheBullPrint", "#Bitcoin", "#CryptoIndia", "#Trump", "#BTC", "#CryptoTax", "#Shorts"]
    },
    {
        "id": 6,
        "title": "Why Foreign Investors Dumped ₹1.2 Lakh Cr from Dalal Street #Shorts",
        "description": "Surging US Treasury yields at 5% trigger a record FII exodus from Indian equities. Can the Indian retail SIP wall withstand Wall Street's selling pressure?\n\n#TheBullPrint #FII #Nifty50 #DalalStreet #MutualFunds #StockMarketIndia #Shorts",
        "tags": ["#TheBullPrint", "#FII", "#Nifty50", "#DalalStreet", "#MutualFunds", "#StockMarketIndia", "#Shorts"]
    },
    {
        "id": 7,
        "title": "Drill Baby Drill: How Cheap Oil Saves India ₹1 Lakh Crore #Shorts",
        "description": "Trump's push for US shale oil flooding global markets could drop crude to $65. Why this saves India over $10 Billion and fuels Asian Paints & IndiGo.\n\n#TheBullPrint #CrudeOil #DrillBabyDrill #AsianPaints #IndiGo #StockMarketIndia #Shorts",
        "tags": ["#TheBullPrint", "#CrudeOil", "#DrillBabyDrill", "#AsianPaints", "#IndiGo", "#StockMarketIndia", "#Shorts"]
    },
    {
        "id": 8,
        "title": "Trump's Drug Price War: Massive Boom for Indian Pharma #Shorts",
        "description": "America cannot slash healthcare costs without Indian generics (40% of US supply). Why a deregulatory Trump White House softens FDA import alerts.\n\n#TheBullPrint #PharmaStocks #SunPharma #DrReddys #Healthcare #StockMarketIndia #Shorts",
        "tags": ["#TheBullPrint", "#PharmaStocks", "#SunPharma", "#DrReddys", "#Healthcare", "#StockMarketIndia", "#Shorts"]
    },
    {
        "id": 9,
        "title": "Sona Crash or Gold Boom? What Trump Means for Gold #Shorts",
        "description": "Gold pulled back after Trump's election win, but a $35 Trillion US debt explosion means central banks and the RBI are hoarding physical gold. Is this dip a buy?\n\n#TheBullPrint #GoldPrice #Sona #GoldInvestment #TrumpTrade #DalalStreet #Shorts",
        "tags": ["#TheBullPrint", "#GoldPrice", "#Sona", "#GoldInvestment", "#TrumpTrade", "#DalalStreet", "#Shorts"]
    },
    {
        "id": 10,
        "title": "The Adani-Trump Energy Axis: What You Weren't Told #Shorts",
        "description": "As Trump dismantles climate red tape, why global energy pragmatism gives unprecedented certainty to Indian industrial titans like Adani and Reliance.\n\n#TheBullPrint #Adani #Reliance #EnergyPolicy #Trump #DalalStreet #Shorts",
        "tags": ["#TheBullPrint", "#Adani", "#Reliance", "#EnergyPolicy", "#Trump", "#DalalStreet", "#Shorts"]
    }
]

def main():
    print("=" * 70)
    print("🚀 PUBLISHING ALL 10 TRUMP ELECTION SHORTS TO YOUTUBE")
    print("=" * 70)

    uploader = YouTubeUploader()
    results = []

    for item in SHORTS_META:
        sid = item["id"]
        v_path = BASE_DIR / "output" / "trump_shorts" / "rendered" / f"trump_short_{sid:02d}.mp4"
        t_path = BASE_DIR / "output" / "trump_shorts" / "frames" / f"short_{sid:02d}" / "seg_01.jpg"

        if not v_path.exists():
            print(f"❌ Missing video file: {v_path}")
            continue

        print(f"\n[{sid:02d}/10] Uploading: {item['title']}...")
        print(f"   Video: {v_path.name} ({round(v_path.stat().st_size / 1024 / 1024, 2)} MB)")
        print(f"   Thumbnail: {t_path.name}")

        try:
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
            if res.get("success"):
                vid_id = res.get("video_id")
                url = res.get("url")
                print(f"   🎉 SUCCESS: {url} (ID: {vid_id})")
                results.append((sid, item["title"], url, "LIVE"))
            else:
                print(f"   ❌ FAILED: {res.get('error')}")
                results.append((sid, item["title"], None, f"FAILED: {res.get('error')}"))
        except Exception as e:
            print(f"   ❌ EXCEPTION: {e}")
            results.append((sid, item["title"], None, f"ERROR: {e}"))

        time.sleep(3) # Small pacing between uploads

    print("\n" + "=" * 70)
    print("📋 UPLOAD SUMMARY FOR 10 TRUMP ELECTION SHORTS:")
    print("=" * 70)
    for sid, title, url, status in results:
        print(f"Short {sid:02d}: [{status}] {title}")
        if url:
            print(f"   -> {url}")

if __name__ == "__main__":
    main()
