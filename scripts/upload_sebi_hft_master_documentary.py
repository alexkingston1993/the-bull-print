#!/usr/bin/env python3
"""
Dedicated Uploader for the Flagship 12-Minute Master Documentary:
'THE ₹20 LAKH BARRIER: The Secret Algorithms That Blew Up Indian Retail Trading'
Channel: The Bull Print
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

VIDEO_PATH = BASE_DIR / "output" / "sebi_hft_documentary" / "the_20_lakh_barrier_12min_master.mp4"
THUMBNAIL_PATH = BASE_DIR / "output" / "sebi_hft_documentary" / "frames" / "segment_02.jpg"

TITLE = "THE ₹20 LAKH BARRIER: The Secret Algorithms That Blew Up Indian Trading"

DESCRIPTION = """Official forensic investigation into the ₹1,81,000 Crore derivatives wipeout and why SEBI built the ₹20 Lakh Barrier to dismantle the retail options casino.

⏱️ CHAPTER TIMESTAMPS:
00:00 - Prologue: The 3:15 PM Trap & 93% Retail Loss Audit
01:20 - The Illusion of Quick Wealth & 160M Demat Explosion
02:20 - The BKC Server Vaults: 4 Microseconds vs 400ms 4G Lag
03:20 - The Jane Street $1 Billion Profit Leak & Gamma Hedging
04:40 - The ₹10 Hero-Zero Lottery & The Mathematical Theta Cliff
05:20 - The Dubai Finfluencers & Underground Telegram Syndicates
06:40 - The Tipping Point: ₹500 Trillion Derivatives Casino
07:20 - The SEBI Hammer: Lot Size Hikes, Expiry Cull & The ₹20 Lakh Rule
09:20 - The Fintech Revenue Shock & Where The Money Actually Moved
10:40 - The Positive-Sum Math: Systematic Compounding vs Gambling

Derivatives were engineered as insurance contracts for institutions managing multi-thousand-crore portfolios—not as lottery tickets for household savings. This investigation reveals the institutional machinery behind market making, latency arbitrage, and why true wealth on Dalal Street is built in patience, not panic.

Golden Rule: The market always tempts with fast money, but compounding rewards long-term discipline.

#TheBullPrint #SEBI #StockMarketIndia #OptionTrading #JaneStreet #NSE #DalalStreet #FinanceDocumentary #TradingTruth"""

TAGS = [
    "#TheBullPrint", "#SEBI", "#StockMarketIndia", "#OptionTrading",
    "#DalalStreet", "#NSE", "#JaneStreet", "#HighFrequencyTrading",
    "#NiftyOptions", "#TradingScam", "#FinancialDocumentary", "#InvestingIndia"
]

def main():
    print("=" * 70)
    print("🚀 PUBLISHING 12-MINUTE MASTER DOCUMENTARY TO YOUTUBE")
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
