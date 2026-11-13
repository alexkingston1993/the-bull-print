#!/usr/bin/env python3
"""
Dedicated Uploader for Video #2:
'THE ₹2,000 CRORE VAULT HEIST: The Inside Investigation of WazirX & India's Missing Crypto'
Channel: The Bull Print
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

VIDEO_PATH = BASE_DIR / "output" / "wazirx_heist_documentary" / "the_2000cr_wazirx_heist_12min_master.mp4"
THUMBNAIL_PATH = BASE_DIR / "output" / "wazirx_heist_documentary" / "frames" / "segment_01.jpg"

TITLE = "THE ₹2,000 CRORE HEIST: The Inside Investigation of WazirX & India's Missing Crypto"

DESCRIPTION = """Comprehensive forensic documentary investigating the ₹2,000 Crore ($234M) vault evacuation at WazirX, the multisig blind-signing failure, and the corporate blame war between Mumbai, Singapore, and Dubai.

⏱️ CHAPTER TIMESTAMPS:
00:00 - Prologue: The 10:00 AM Blackout & 45% Cold Vault Evacuation
01:20 - The 2021 Bull Run Mania & The Illusory Binance Acquisition
02:20 - The Architecture of Failure: 5-of-6 Multisig & Blind Signing
03:20 - July 18, 10:00 AM: The $234 Million Uniswap & SHIB Liquidity Dump
04:40 - The Corporate War: WazirX vs Liminal vs Binance Ownership
05:40 - The North Korean Trail: Lazarus Group & Tornado Cash Laundering
06:20 - The 55-45 Socialized Loss Outrage & Retail Street Protests
07:00 - The Singapore Section 64 Moratorium & The Trapped INR Cash
09:20 - The Regulatory Void & Why Proof of Reserves Failed
09:40 - The Hard Law: Not Your Keys, Not Your Coins & The Hardware Revolution

This investigative breakdown examines the technical anatomy of the 5-of-6 threshold signature exploit, the legal jurisdictional shielding under Singapore's Insolvency Act, and the fundamental rules of self-sovereign wealth in the digital era.

Golden Rule: Not your keys, not your coins. When you leave funds on a custodial exchange, you don't own cryptocurrency—you own a corporate IOU.

#TheBullPrint #WazirX #CryptoScam #WazirXHack #NischalShetty #Binance #LazarusGroup #BitcoinIndia #CryptoInvestigation"""

TAGS = [
    "#TheBullPrint", "#WazirX", "#WazirXHack", "#CryptoScam",
    "#NischalShetty", "#LiminalCustody", "#Binance", "#LazarusGroup",
    "#CryptoIndia", "#ForensicFinance", "#SelfCustody", "#Documentary"
]

def main():
    print("=" * 70)
    print("🚀 PUBLISHING WAZIRX 12-MINUTE MASTER DOCUMENTARY TO YOUTUBE")
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
