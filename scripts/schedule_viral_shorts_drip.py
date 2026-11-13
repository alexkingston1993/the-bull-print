#!/usr/bin/env python3
"""
YouTube Shorts Drip-Feeding Scheduler (Viral Timetable)
Schedules Shorts 02 through 10 at peak audience engagement windows across the day.
"""
import sys
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.services.youtube_uploader import YouTubeUploader

# Timetable in IST (+05:30)
# Short 01 is already LIVE public (5uCdjiEr56Q)
SCHEDULE_SLOTS = [
    # (short_id, IST_date_str "YYYY-MM-DD HH:MM")
    ("short_02_nifty_reclaims_25000", "2026-11-10 15:30"),      # Closing bell surge
    ("short_03_fii_48000cr_buying", "2026-11-10 17:00"),        # FII daily flow recap
    ("short_04_sebi_mega_ipo_rush", "2026-11-10 18:30"),        # Evening commute / IPO alpha
    ("short_05_ongc_venezuela_takeover", "2026-11-10 20:00"),   # Geopolitics / energy desk
    ("short_06_rice_hoarding_mandate", "2026-11-10 21:30"),     # Inflation reality / kitchen economics
    ("short_07_crude_oil_crash_94", "2026-11-10 22:45"),        # Late night commodities / Wall St
    ("short_08_rupee_recovery_9393", "2026-11-11 08:00"),       # Pre-market morning forex
    ("short_09_us_cpi_rate_cut_countdown", "2026-11-11 10:30"), # Mid-morning global macro
    ("short_10_bitcoin_liquidity_rebound", "2026-11-11 13:00"), # Lunch break digital asset liquidity
]

def ist_to_utc_rfc3339(ist_str: str) -> str:
    """Converts 'YYYY-MM-DD HH:MM' in IST to RFC 3339 UTC string."""
    dt = datetime.strptime(ist_str, "%Y-%m-%d %H:%M")
    # IST is UTC + 5:30
    ist_tz = timezone(timedelta(hours=5, minutes=30))
    dt_ist = dt.replace(tzinfo=ist_tz)
    dt_utc = dt_ist.astimezone(timezone.utc)
    return dt_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")

def schedule_all_remaining():
    print("=" * 80)
    print("⏳ PREPARING VIRAL DRIP-FEED SCHEDULE FOR SHORTS 02 THROUGH 10")
    print("=" * 80)
    
    uploader = YouTubeUploader()
    upload_results = []
    
    for s_id, ist_slot in SCHEDULE_SLOTS:
        work_dir = ROOT / "output/viral_shorts_past24h" / s_id
        video_path = work_dir / "master_video.mp4"
        meta_path = work_dir / "METADATA.json"
        
        if not video_path.exists():
            print(f"⚠️ Video file not found: {video_path}")
            continue
            
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            
        utc_publish_at = ist_to_utc_rfc3339(ist_slot)
        print(f"\n📤 Scheduling {s_id}...")
        print(f"   Title: {meta['title']}")
        print(f"   Target Slot: {ist_slot} IST ({utc_publish_at} UTC)")
        
        res = uploader.upload_video(
            language="en",
            video_path=str(video_path),
            title=f"{meta['title']} #Shorts",
            description=meta["description"],
            tags=meta.get("tags", []),
            category_id="27", # Education / Finance
            is_short=True,
            publish_at=utc_publish_at,
            privacy_status="private"
        )
        
        if res.get("success"):
            vid_id = res.get("video_id")
            print(f"   ✅ Scheduled Successfully! Video ID: {vid_id}")
            print(f"   🔗 Scheduled URL: {res.get('url')}")
            
            # Post pinned comment if uploader supports it on scheduled videos
            try:
                uploader.post_pinned_comment("en", vid_id, meta["pinned_comment"])
                print(f"   📌 Pinned comment posted.")
            except Exception as e:
                print(f"   ℹ️ Pinned comment notice (scheduled video): {e}")
                
            upload_results.append({
                "id": s_id,
                "video_id": vid_id,
                "url": res.get("url"),
                "ist_slot": ist_slot,
                "utc_publish_at": utc_publish_at,
                "title": meta["title"]
            })
        else:
            print(f"   ❌ Upload failed: {res.get('error')}")
            
    # Save manifest
    manifest_path = ROOT / "output/viral_shorts_past24h/SCHEDULED_DRIP_MANIFEST.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(upload_results, f, indent=2)
        
    print("\n" + "=" * 80)
    print(f"🚀 DRIP SCHEDULE MANIFEST SAVED: {len(upload_results)} videos queued.")
    print("=" * 80)

if __name__ == "__main__":
    schedule_all_remaining()
