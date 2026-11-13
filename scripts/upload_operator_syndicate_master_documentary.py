#!/usr/bin/env python3
"""
Dedicated Uploader for Video #3:
'THE OPERATOR SYNDICATE: How Indian Penny Stocks Are Pumped, Dumped, and Fixed'
Channel: The Bull Print
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

VIDEO_PATH = BASE_DIR / "output" / "operator_syndicate_documentary" / "the_operator_syndicate_12min_master.mp4"
THUMBNAIL_PATH = BASE_DIR / "output" / "operator_syndicate_documentary" / "frames" / "segment_01.jpg"

TITLE = "THE OPERATOR SYNDICATE: How Indian Penny Stocks Are Pumped, Dumped, and Fixed"

DESCRIPTION = """Comprehensive forensic documentary investigating the underground machinery of Dalal Street penny stock operators, circular wash trading, Kolkata shell conduits, and why retail investors get trapped in lower circuit liquidity deserts.

⏱️ CHAPTER TIMESTAMPS:
00:00 - Prologue: The 9:15 AM Upper Circuit Illusion & Kolkata Shells
01:20 - The ₹2 Crore Dormant Shell Buyout & The Fake AI/Green Rebranding
02:20 - The Architecture of Rigging: Circular Trading & 100-Share Circuits
03:20 - The Exit Machine: Finfluencer Kickbacks & 5 Million Bulk SMS Blasts
04:20 - The 10:15 AM Dump: The Lower Circuit Lockout & Zero Buyers
05:40 - The Graded Surveillance Measure (GSM Stage 4) & The Khoka Trail
06:40 - The SME IPO Mania: 400x Oversubscription on Bicycle Sheds
07:00 - The Psychological Trap: The Cheap Nominal Share Price Fallacy
08:20 - The 4 Forensic Red Flags Every Indian Retail Investor Must Know
10:00 - The Mathematical Reality: Why -90% Requires +900% to Break Even

This investigative breakdown reveals how shadowy syndicates corner eighty percent of free-floating shares, generate artificial Level-2 bid depth, and coordinate social media hype to dump preferential warrants on retail buyers.

Golden Rule: If an investment requires an urgent Telegram message, a secret WhatsApp tip, or an unverified YouTube screenshot, you are not an investor—you are the exit liquidity.

#TheBullPrint #StockMarketIndia #PennyStocks #OperatorSyndicate #SEBI #DalalStreet #SMEIPO #TradingTruth #ForensicFinance"""

TAGS = [
    "#TheBullPrint", "#StockMarketIndia", "#PennyStocks", "#OperatorSyndicate",
    "#SEBI", "#DalalStreet", "#SMEIPO", "#CircularTrading",
    "#UpperCircuit", "#StockMarketScam", "#FinancialDocumentary", "#InvestingIndia"
]

def main():
    print("=" * 70)
    print("🚀 PUBLISHING OPERATOR SYNDICATE 12-MINUTE MASTER DOCUMENTARY TO YOUTUBE")
    print(f"   Video: {VIDEO_PATH.name} ({round(VIDEO_PATH.stat().st_size / 1024 / 1024, 1)} MB)")
    print(f"   Thumbnail: {THUMBNAIL_PATH.name}")
    print(f"   Privacy: Public")
    print("=" * 70)

    uploader = YouTubeUploader()
    result = uploader.upload_video(
        language="en",
        video_path=str(VIDEO_PATH),
        title=TITLE,
        description=DESCRIPTION,
        tags=TAGS,
        category_id="27", # Education
        privacy_status="public",
        is_short=False,
        thumbnail_path=str(THUMBNAIL_PATH),
        force_upload=True
    )

    if result.get("success"):
        print("\n" + "=" * 70)
        print("🎉 SUCCESS! Video is LIVE on YouTube:")
        print(f"   Video ID: {result.get('video_id')}")
        print(f"   Watch URL: {result.get('url')}")
        print("=" * 70)
    else:
        print(f"\n❌ Upload failed: {result.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
