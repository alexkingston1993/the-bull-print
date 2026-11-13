#!/usr/bin/env python3
"""
Dedicated Uploader for Video #5:
'THE ₹10,000 CRORE CLAIM REJECTION MACHINE: The Inside Secrets of Indian Health Insurance'
Channel: The Bull Print
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

VIDEO_PATH = BASE_DIR / "output" / "health_insurance_scam_documentary" / "the_10000cr_health_insurance_scam_12min_master.mp4"
THUMBNAIL_PATH = BASE_DIR / "output" / "health_insurance_scam_documentary" / "frames" / "segment_01.jpg"

TITLE = "THE ₹10,000 CRORE CLAIM REJECTION MACHINE: The Inside Secrets of Indian Health Insurance"

DESCRIPTION = """Forensic investigation into the predatory machinery of Indian health insurance claim rejections, TPA conflict of interest, hospital dual-pricing, and how to use IRDAI rules and the Insurance Ombudsman to force 100% settlement.

⏱️ CHAPTER TIMESTAMPS:
00:00 - Prologue: The 2:00 AM Hospital Cashless Rejection Ambush
01:00 - The Master Title: The ₹10,000 Crore Claim Rejection Machine
02:20 - Trap #1: The Room Rent Sub-Limit & Proportional Deduction Slash
03:20 - Trap #2: The Consumables Blacklist & The 20% Cash Shock
03:40 - Trap #3: The Pre-Existing Disease Weapon & Bogus Nexus Lies
04:40 - The TPA Cartel: Profit Through Claim Repudiation
05:20 - The Private Hospital Dual-Pricing Cartel: 300% Markups
06:20 - The Senior Citizen Premium Trap: Forced Attrition at Age 65
07:00 - The IRDAI 2024 Master Circular: 100% Cashless & 3-Hour Discharge
08:00 - The 5-Year Moratorium Shield: Section 45 Incontestability
08:20 - The Insurance Ombudsman Weapon: Free Justice & 80% Win Rate
09:20 - The Policyholder's Battle Plan: Paper Trail & Itemized Bill Audit
10:20 - The Super Top-Up Hack & The Perfect Policy Blueprint
11:20 - The Bull Print Verdict: How to Protect Your Family's Health & Wealth

Every year across India, over ten thousand crore rupees in legitimate medical claims are slashed, delayed, or outright repudiated. This documentary exposes how room rent sub-limits silently halve your surgical claim, why insurers onboard without verification and scrutinize only at claim time, and the exact step-by-step legal protocol to win back every rupee.

Golden Rule: Never dispute an insurance claim on the phone. Move every interaction to writing, invoke Section 45 moratorium protections, and file directly with the Insurance Ombudsman if denied.

#TheBullPrint #HealthInsurance #HealthInsuranceIndia #IRDAI #ClaimRejection #InsuranceOmbudsman #FinancialLiteracy #ConsumerRights #Documentary"""

TAGS = [
    "#TheBullPrint", "#HealthInsurance", "#HealthInsuranceIndia", "#IRDAI",
    "#ClaimRejection", "#InsuranceOmbudsman", "#HospitalBills", "#TPA",
    "#ConsumerRights", "#FinancialLiteracy", "#MedicalInsurance", "#PersonalFinanceIndia"
]

def main():
    print("=" * 70)
    print("🚀 PUBLISHING HEALTH INSURANCE 12-MINUTE MASTER DOCUMENTARY TO YOUTUBE")
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
