#!/usr/bin/env python3
"""
Dedicated Uploader for Video #6:
'THE ZERO-DAY OPTIONS CASINO: The ₹1.8 Lakh Crore Retail Slaughter'
Pure 173-Frame Master Edition (100% Clean Cuts, Zero Digital Distortion)
Channel: The Bull Print (@thebullprint)
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader
from app.services.compliance_shield import generate_global_compliance_footer

VIDEO_PATH = BASE_DIR / "output" / "options_casino_documentary" / "the_zero_day_options_casino_12min_master.mp4"
THUMBNAIL_PATH = BASE_DIR / "output" / "options_casino_documentary" / "frames" / "segment_01.jpg"

TITLE = "THE ZERO-DAY OPTIONS CASINO: The ₹1.8 Lakh Crore Retail Slaughter"

DESCRIPTION = """Comprehensive forensic investigation into India's zero-day options explosion, SEBI's bombshell study revealing 93% retail losses, high-frequency quant predatory algorithms, finfluencer fake P&L scams, and the sovereign survival blueprint for everyday investors.

⏱️ CHAPTER TIMESTAMPS:
00:00 - Prologue: The 3:15 PM Expiry Zero & The ₹1.8 Lakh Crore Black Hole
01:00 - The Master Title Plate: The Zero-Day Options Casino
01:20 - Chapter 1: The 5-Expiry Week & India's ₹400 Trillion Volume Boom
02:20 - Chapter 2: The Quants: Theta Decay, Gamma Crush & Stop-Loss Hunting
03:40 - The Latency Trap: 300ns Co-Location Servers vs. 300ms Mobile 4G
04:40 - Chapter 3: The Finfluencer Illusion: Inspect Element & ₹20,000 Courses
06:00 - The SEBI Clampdown: Guru Raids, Frozen Accounts & Dopamine Loops
07:00 - Chapter 4: The House Always Wins: ₹5,000 Cr Brokerage Profits & STT
08:40 - SEBI's 7-Point Regulatory Mandate: Tripling Lot Sizes to ₹15 Lakhs
09:20 - Chapter 5: The Math of Recovery: Why -90% Requires +900% to Break Even
10:00 - The Sovereign Blueprint: Disabling F&O, Real Hedging & Index Compounding
11:40 - The Bull Print Verdict & The Fundamental Law of Dalal Street

According to market regulator SEBI, over one lakh eighty-one thousand crore rupees were incinerated by retail traders in equity derivatives over three financial years. This documentary breaks down the exact mathematical mechanics of why individual retail option buyers face nearly 100% ruin probability over time, and how to protect your family's financial future.

Golden Rule: The stock market is a device for transferring wealth from the impatient to the patient. Options were engineered as insurance contracts, not lottery tickets.

#TheBullPrint #OptionsTrading #SEBI #Nifty #BankNifty #StockMarketIndia #ZeroDayOptions #DalalStreet #FinancialLiteracy #ForensicFinance #Documentary
"""

TAGS = [
    "#TheBullPrint", "#OptionsTrading", "#SEBI", "#Nifty",
    "#BankNifty", "#StockMarketIndia", "#ZeroDayOptions", "#DalalStreet",
    "#Finfluencers", "#TradingLosses", "#Documentary", "#FinancialLiteracy"
]

def main():
    if not VIDEO_PATH.exists():
        print(f"❌ Error: Master video not found at {VIDEO_PATH}")
        sys.exit(1)

    print("=" * 75)
    print("🚀 PUBLISHING THE ZERO-DAY OPTIONS CASINO (PURE 173-FRAME MASTER)")
    print(f"   Video: {VIDEO_PATH.name} ({round(VIDEO_PATH.stat().st_size / 1024 / 1024, 1)} MB)")
    print(f"   Visual Standard: 173 Clean Cuts across 36 Segments (~4.1s per cut)")
    print(f"   Thumbnail: {THUMBNAIL_PATH.name}")
    print(f"   Privacy: Public")
    print("=" * 75)

    full_description = DESCRIPTION + "\n\n" + generate_global_compliance_footer(
        target_countries=["IN", "US", "GB", "SG", "AE", "AU", "CA"],
        is_derivative=True,
        is_crypto=False
    )

    uploader = YouTubeUploader()
    result = uploader.upload_video(
        language="en",
        video_path=str(VIDEO_PATH),
        title=TITLE,
        description=full_description,
        tags=TAGS,
        category_id="27", # Education
        privacy_status="public",
        is_short=False,
        thumbnail_path=str(THUMBNAIL_PATH),
        force_upload=True
    )

    if result.get("success"):
        video_id = result.get("video_id")
        watch_url = result.get("url")
        print("\n" + "=" * 75)
        print("🎉 SUCCESS! Video is LIVE & PUBLIC on YouTube:")
        print(f"   Video ID: {video_id}")
        print(f"   Watch URL: {watch_url}")
        print("=" * 75)

        # Pin investigative comment
        pinned_comment = (
            "📌 THE BULL PRINT FORENSIC ARCHIVE:\n"
            "According to SEBI, 93% of retail derivative traders lose money, suffering a cumulative slaughter of ₹1,81,000 Crore.\n\n"
            "Key takeaway: If your portfolio drops 90%, you need a 900% gain just to get back to zero. You cannot gamble your way out of a hole dug by gambling.\n\n"
            "What has your personal experience been with weekly expiries? Have you disabled your F&O segment yet? Join the discussion below."
        )
        try:
            uploader.post_pinned_comment(language="en", video_id=video_id, comment_text=pinned_comment)
            print("✅ Pinned forensic comment posted.")
        except Exception as e:
            print(f"⚠️ Could not post pinned comment: {e}")

        # Add to Playlists
        try:
            srv = uploader._get_service("en")
            target_playlists = [
                ("PLMuYPFbxOGyI", "100-Year Masterclasses"),
                ("PLDhTdRWRS2bo", "India Dalal Street Forensics"),
                ("PLIFXZFrnw2Fc", "United States Macro"),
                ("PLEeJcVwtfcKY", "Australia & NZ Corridors")
            ]
            for pl_id, pl_name in target_playlists:
                try:
                    srv.playlistItems().insert(
                        part="snippet",
                        body={
                            "snippet": {
                                "playlistId": pl_id,
                                "resourceId": {
                                    "kind": "youtube#video",
                                    "videoId": video_id
                                }
                            }
                        }
                    ).execute()
                    print(f"✅ Added to Playlist: {pl_name} ({pl_id})")
                except Exception as pl_err:
                    print(f"⚠️ Playlist {pl_name} note: {pl_err}")
        except Exception as e:
            print(f"⚠️ Playlist association error: {e}")

        return video_id
    else:
        print(f"\n❌ Upload failed: {result.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
