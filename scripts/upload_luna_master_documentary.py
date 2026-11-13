#!/usr/bin/env python3
"""
Dedicated Uploader for Video #4:
'THE LUNA EXTINCTION: The $40 Billion Death Spiral That Broke Crypto'
3-Cut Dynamic Micro-Motion Master Edition (108 Cuts, 5.7 Mbps Bitrate)
Channel: The Bull Print (@thebullprint)
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader
from app.services.compliance_shield import generate_global_compliance_footer

VIDEO_PATH = BASE_DIR / "output" / "luna_death_spiral_documentary" / "the_luna_extinction_dynamic_cuts_12min_master.mp4"
THUMBNAIL_PATH = BASE_DIR / "output" / "luna_death_spiral_documentary" / "frames" / "segment_01.jpg"

TITLE = "THE LUNA EXTINCTION: The $40 Billion Death Spiral That Broke Crypto"

DESCRIPTION = """The definitive forensic documentary on the catastrophic $40,000,000,000 collapse of Terra-Luna and UST in May 2022.

⏱️ CHAPTER TIMESTAMPS:
00:00 - Prologue: The 80-Cent De-Peg Fracture & Quant Warnings
01:00 - The Master Title: The $40 Billion Destruction of Wealth
01:40 - Chapter 1: The Two-Token Flywheel & The 20% Anchor Protocol Lie
03:40 - Chapter 2: The Coordinated Strike on Curve Pool 7 & The Soros Run
05:40 - Chapter 3: The Algorithmic Death Spiral (6.5 Trillion Token Hyper-Inflation)
07:40 - The Bitcoin Reserve Failure: 80,000 BTC Liquidated in Vain
09:00 - Chapter 4: The Global Contagion (Three Arrows Capital, Celsius & FTX)
10:40 - The Fall of Do Kwon: Montenegro Arrest & The SEC Forensic Verdict
11:40 - The 100-Year Rule: Math Without Sovereign Reserves Is Always Zero

This forensic breakdown deconstructs the algorithmic mint-and-burn mechanics of TerraUSD (UST) and LUNA, the flawed 20% yield subsidy funded by Terraform Labs' venture reserves, the microscopic timing of the $350 million Curve pool drain, and how an uncollateralized stablecoin triggered a multi-year crypto credit winter.

Golden Rule: An algorithm cannot create economic value out of thin air. Yield without tangible collateral is debt disguised as magic. Always verify reserves on-chain.

#TheBullPrint #LunaExtinction #TerraLuna #DoKwon #CryptoCrash #ForensicFinance #Documentary #Bitcoin #DeFi #AnchorProtocol #WallStreet #CryptoHistory
"""

TAGS = [
    "#TheBullPrint", "#TerraLuna", "#DoKwon", "#LunaCrash",
    "#CryptoCrash", "#ForensicFinance", "#Documentary", "#Bitcoin",
    "#DeFi", "#AnchorProtocol", "#AlgorithmicStablecoin", "#WallStreet"
]

def main():
    if not VIDEO_PATH.exists():
        print(f"❌ Error: Master video not found at {VIDEO_PATH}")
        sys.exit(1)

    print("=" * 75)
    print("🚀 PUBLISHING THE LUNA EXTINCTION (3-CUT DYNAMIC EDITION) TO YOUTUBE")
    print(f"   Video: {VIDEO_PATH.name} ({round(VIDEO_PATH.stat().st_size / 1024 / 1024, 1)} MB)")
    print(f"   Visual Pacing: 108 Cinematic Cuts across 36 Segments (3 cuts/segment)")
    print(f"   Thumbnail: {THUMBNAIL_PATH.name}")
    print(f"   Privacy: Public")
    print("=" * 75)

    full_description = DESCRIPTION + "\n\n" + generate_global_compliance_footer(
        target_countries=["US", "IN", "GB", "SG", "HK", "AE", "AU", "CA"],
        is_crypto=True,
        is_derivative=True
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
            "The collapse of Terra-Luna eradicated $40,000,000,000 in 72 hours, proving that algorithmic stabilization without verifiable reserves is mathematical suicide.\n\n"
            "Key takeaway: In every financial crisis, the mechanism designed to provide liquidity becomes the exact engine that accelerates liquidation.\n\n"
            "Which crypto collapse would you like our forensic desk to investigate next? Let us know in the comments."
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
                ("PLIFXZFrnw2Fc", "United States Macro"),
                ("PLIvFRmzd63Pw", "Singapore & Hong Kong Hubs"),
                ("PLDhTdRWRS2bo", "India Forensics")
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
