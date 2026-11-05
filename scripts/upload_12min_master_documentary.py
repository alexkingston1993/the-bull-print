"""
Dedicated Uploader for the Flagship 12-Minute Master Documentary:
'THE $32 BILLION ILLUSION: The Criminal Rise and Fall of FTX & Alameda Research'
Uploads to YouTube channel 'The Bull Print' as a Public video with custom 2K thumbnail.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

VIDEO_PATH = BASE_DIR / "output" / "the_32_billion_illusion_12min_master.mp4"
THUMBNAIL_PATH = BASE_DIR / "assets" / "approved_bundles" / "the-32-billion-illusion-ftx-alameda-12min" / "segment_01.jpg"

TITLE = "THE $32 BILLION ILLUSION: The Criminal Rise and Fall of FTX & Alameda Research"

DESCRIPTION = """Comprehensive forensic documentary on the $32,000,000,000 collapse of FTX and Alameda Research.

⏱️ CHAPTER TIMESTAMPS:
00:00 - Prologue: The $30M Bahamas Citadel & The Effective Altruism Deception
02:00 - Chapter 1: The Kimchi Premium & The Infinite Money Glitch
04:20 - Chapter 2: The Seduction of Wall Street, VC Billions & Capitol Hill
06:40 - Chapter 3: The Leaked Balance Sheet & The 72-Hour Bank Run
09:20 - Chapter 4 & Epilogue: The John Ray Forensic Verdict & 25-Year Prison Sentence

This investigative breakdown examines the quantitative arbitrage roots at Jane Street, the algorithmic mechanics of the FTT token flywheel, the hardcoded allow_negative_balance database exemption, and the timeless self-custody lessons for everyday investors.

Golden Codex: Not your keys, not your coins. Yield without custody is fiction. Always demand cryptographic proof of reserves."""

TAGS = [
    "#FTX", "#AlamedaResearch", "#SamBankmanFried", "#CryptoFraud",
    "#TheBullPrint", "#Documentary", "#ForensicFinance", "#Bitcoin",
    "#CryptoHistory", "#WallStreet", "#JohnRay", "#SequoiaCapital"
]

def main():
    print("=" * 65)
    print("🚀 PUBLISHING 12-MINUTE MASTER DOCUMENTARY TO YOUTUBE")
    print(f"   Video: {VIDEO_PATH.name} ({round(VIDEO_PATH.stat().st_size / 1024 / 1024, 1)} MB)")
    print(f"   Thumbnail: {THUMBNAIL_PATH.name}")
    print(f"   Privacy Status: PUBLIC")
    print("=" * 65)

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
        print("\n" + "=" * 65)
        print("🎉 SUCCESS! Video is LIVE & PUBLIC on YouTube:")
        print(f"   Video ID: {result.get('video_id')}")
        print(f"   Watch URL: {result.get('url')}")
        print("=" * 65)
    else:
        print(f"\n❌ Upload failed: {result.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
