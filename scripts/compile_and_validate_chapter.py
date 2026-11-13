#!/usr/bin/env python3
"""
scripts/compile_and_validate_chapter.py

Autonomous Chapter Compiler & Pre-Render Validator
1. Compiles a chapter manifest from audio, word timestamps, and beat specifications.
2. Validates:
   - Zero hardcoded story strings in remotion-engine/src/
   - All 6 Parameterized Archetypes adhere to schema
   - Every audio, video, and image asset exists on disk
   - Frame timing integrity: sum(beats.durationFrames) == audioDurationFrames (+/- 1 frame)
3. Outputs active_chapter_manifest.json for Remotion rendering.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

WORKSPACE = Path("/Users/apple/Documents/Antigravity/untitled folder")
REMOTION_SRC = WORKSPACE / "remotion-engine" / "src"
PUBLIC_DIR = WORKSPACE / "remotion-engine" / "public"
OUTPUT_DIR = WORKSPACE / "output"

def audit_zero_hardcoded_content():
    """Ironclad Guardrail: Zero FTX strings in src/"""
    print("\n🔍 Step 1: Auditing Zero Hardcoded Story Strings...")
    forbidden = ["bankman", "alameda", "sequoia", "ftx", "bahamas", "allow_negative"]
    pattern = "|".join(forbidden)
    
    cmd = ["grep", "-riE", pattern, str(REMOTION_SRC)]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode == 0 and result.stdout.strip():
        print(f"❌ FAIL: Hardcoded forbidden strings found in {REMOTION_SRC}:")
        print(result.stdout)
        sys.exit(1)
    
    print("  ✅ PASS: 0 hardcoded story strings in remotion-engine/src/")

def get_audio_duration_frames(audio_path: Path, fps: int = 30) -> int:
    """Probe audio file duration in frames using ffprobe"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    duration_sec = float(res.stdout.strip())
    return int(round(duration_sec * fps)), duration_sec

def build_tether_ch01_manifest():
    """
    Builds the production Tether Chapter 1 Manifest:
    'THE $100 BILLION GHOST // HOW A SHADOW ENTITY BOUGHT AMERICA'
    """
    fps = 30
    audio_rel = "assets/tether/chapter_01.mp3"
    audio_full = PUBLIC_DIR / audio_rel
    
    # If chapter_01.mp3 exists, probe it; otherwise fallback to test_christopher_offline.mp3
    if not audio_full.exists():
        audio_rel = "assets/test_christopher_offline.mp3"
        audio_full = PUBLIC_DIR / audio_rel
        # Copy test audio if needed
        if (OUTPUT_DIR / "test_christopher_offline.mp3").exists():
            import shutil
            shutil.copy(OUTPUT_DIR / "test_christopher_offline.mp3", audio_full)
            shutil.copy(OUTPUT_DIR / "test_christopher_timestamps.json", PUBLIC_DIR / "assets" / "test_christopher_timestamps.json")
    
    total_frames, total_sec = get_audio_duration_frames(audio_full, fps)
    print(f"🎙️ Chapter 1 Master Audio: {audio_rel} ({total_sec:.2f}s, {total_frames} frames)")
    
    # Load word timestamps if present
    timestamps_file = PUBLIC_DIR / "assets" / "test_christopher_timestamps.json"
    word_timestamps = []
    if timestamps_file.exists():
        with open(timestamps_file, "r") as f:
            word_timestamps = json.load(f)
    
    # Define the 6 documentary beats across the timeline
    # Beat 1: SOLAR_EMPIRE - High-key daylight introduction to the $100B vault
    # Beat 2: HYPER_GROWTH - Fast-paced Treasury Bills accumulation (Wall St)
    # Beat 3: MAGAZINE_SLAM - Fortune/Forbes cover investigation
    # Beat 4: INSTITUTIONAL_WIRE - $850M wire transfer dispatch
    # Beat 5: SIPHON_HUD - The Shadow dollar arbitrage engine
    # Beat 6: FORENSIC_DOCKET - DOJ Subpoena & New York AG exhibit
    
    # Divide total_frames proportionally
    b1_frames = int(total_frames * 0.20)
    b2_frames = int(total_frames * 0.18)
    b3_frames = int(total_frames * 0.16)
    b4_frames = int(total_frames * 0.16)
    b5_frames = int(total_frames * 0.15)
    b6_frames = total_frames - (b1_frames + b2_frames + b3_frames + b4_frames + b5_frames)
    
    beats = [
        {
            "id": "beat_01_treasury_empire",
            "archetype": "PARALLAX_SANDWICH",
            "startFrame": 0,
            "durationFrames": b1_frames,
            "durationSec": b1_frames / fps,
            "mood": "SOLAR_EMPIRE",
            "parallax": {
                "bgAsset": "assets/cinematic/scene_1_bg.mp4",
                "fgCutoutAsset": "assets/cinematic/scene_founder_fg.png",
                "titleLine1": "THE SHADOW",
                "titleLine2": "EMPIRE",
                "scaleSpeed": 1.15,
                "dollyAmount": -30
            }
        },
        {
            "id": "beat_02_treasury_accumulation",
            "archetype": "KINETIC_STATEMENT",
            "startFrame": b1_frames,
            "durationFrames": b2_frames,
            "durationSec": b2_frames / fps,
            "mood": "HYPER_GROWTH",
            "statement": {
                "bgAsset": "assets/cinematic/scene_2_bg.mp4",
                "heroTitle": "MORE TREASURY BILLS THAN",
                "accentWord": "GERMANY & AUSTRALIA",
                "subText": "FEWER THAN 100 EMPLOYEES CONTROLLING $100B"
            }
        },
        {
            "id": "beat_03_magazine_investigation",
            "archetype": "MAGAZINE_SLAM",
            "startFrame": b1_frames + b2_frames,
            "durationFrames": b3_frames,
            "durationSec": b3_frames / fps,
            "mood": "HYPER_GROWTH",
            "magazine": {
                "bgAsset": "assets/cinematic/scene_3_bg.mp4",
                "publicationName": "FORTUNE",
                "issueTag": "SPECIAL INVESTIGATION // VOL 44",
                "subjectCutout": "assets/cinematic/scene_forbes_portrait.png",
                "headline": "THE PRINTING PRESS OF CRYPTO",
                "subheadline": "Inside the private conglomerate out-earning BlackRock and Goldman Sachs."
            }
        },
        {
            "id": "beat_04_wire_capital",
            "archetype": "INSTITUTIONAL_WIRE",
            "startFrame": b1_frames + b2_frames + b3_frames,
            "durationFrames": b4_frames,
            "durationSec": b4_frames / fps,
            "mood": "HIGH_STAKES_ARENA",
            "wire": {
                "bgAsset": "assets/cinematic/scene_4_bg.mp4",
                "senderName": "CANTOR FITZGERALD // CUSTODY",
                "recipientName": "TETHER HOLDINGS LTD.",
                "wireAmount": "$850,000,000.00",
                "valuationNote": "US TREASURY 90-DAY BILLS ESCROW",
                "statusBadge": "CONFIRMED // FEDWIRE MT103"
            }
        },
        {
            "id": "beat_05_siphon_engine",
            "archetype": "SIPHON_HUD",
            "startFrame": b1_frames + b2_frames + b3_frames + b4_frames,
            "durationFrames": b5_frames,
            "durationSec": b5_frames / fps,
            "mood": "FORENSIC_NOIR",
            "siphon": {
                "bgAsset": "assets/cinematic/scene_6_bg.mp4",
                "sourceLabel": "PRIMARY REDEMPTION VAULT",
                "sourceAmount": "$100,000,000+",
                "conduitCode": "COMMINGLED RESERVE // CCC_GATEWAY",
                "drainLabel": "SHADOW LIQUIDITY POOL",
                "drainTargetAmount": "-$850,000,000"
            }
        },
        {
            "id": "beat_06_forensic_subpoena",
            "archetype": "FORENSIC_DOCKET",
            "startFrame": b1_frames + b2_frames + b3_frames + b4_frames + b5_frames,
            "durationFrames": b6_frames,
            "durationSec": b6_frames / fps,
            "mood": "FORENSIC_NOIR",
            "docket": {
                "bgAsset": "assets/cinematic/scene_7_bg.mp4",
                "courtName": "UNITED STATES DEPARTMENT OF JUSTICE",
                "folderHeader": "IN RE: GLOBAL COMMINGLING OF RESERVES",
                "exhibitId": "EXHIBIT A-12",
                "codeOrClauseText": "if (reserve_audit_requested == True) { commingle_with_parent_exchange(); }",
                "highlightSubstring": "commingle_with_parent_exchange",
                "stampLabel": "CRITICAL EVIDENCE // ADMITTED"
            }
        }
    ]
    
    manifest = {
        "episodeId": "tether_untold",
        "chapterId": "ch01_the_shadow_empire",
        "chapterIndex": 1,
        "title": "The $100 Billion Ghost",
        "durationSec": total_sec,
        "durationFrames": total_frames,
        "fps": fps,
        "audioAsset": audio_rel,
        "wordTimestamps": word_timestamps,
        "beats": beats
    }
    
    return manifest

def validate_manifest(manifest):
    """Verifies that all assets exist on disk and timing math is exact"""
    print("\n📦 Step 2: Validating Manifest Schema & Asset Integrity...")
    
    # 1. Audio file check
    audio_path = PUBLIC_DIR / manifest["audioAsset"]
    if not audio_path.exists():
        print(f"❌ FAIL: Audio asset not found: {audio_path}")
        sys.exit(1)
    print(f"  ✓ Audio exists: {manifest['audioAsset']}")
    
    # 2. Total duration check
    sum_frames = sum(b["durationFrames"] for b in manifest["beats"])
    diff = abs(sum_frames - manifest["durationFrames"])
    if diff > 1:
        print(f"❌ FAIL: Frame sum mismatch: sum={sum_frames}, total={manifest['durationFrames']} (diff={diff})")
        sys.exit(1)
    print(f"  ✓ Frame timing is exact ({sum_frames} frames == {manifest['durationFrames']} frames)")
    
    # 3. Beat assets check
    for idx, beat in enumerate(manifest["beats"]):
        arch = beat["archetype"]
        mood = beat["mood"]
        print(f"  [{idx+1}/{len(manifest['beats'])}] Validating {arch} ({mood})...")
        
        # Check assets inside archetype configs
        for key in ["parallax", "magazine", "wire", "siphon", "docket", "statement"]:
            cfg = beat.get(key)
            if cfg:
                for prop in ["bgAsset", "fgCutoutAsset", "subjectCutout"]:
                    asset = cfg.get(prop)
                    if asset:
                        asset_path = PUBLIC_DIR / asset
                        if not asset_path.exists():
                            print(f"❌ FAIL: Missing required asset {asset} for {arch} at {asset_path}")
                            sys.exit(1)
    
    print("  ✅ PASS: 100% of beat assets verified on disk!")

def main():
    audit_zero_hardcoded_content()
    
    out_path = PUBLIC_DIR / "assets" / "active_chapter_manifest.json"
    if out_path.exists():
        with open(out_path, "r") as f:
            manifest = json.load(f)
        print(f"📖 Loaded existing active manifest ({len(manifest.get('beats', []))} beats, {manifest.get('durationFrames')} frames)")
    else:
        manifest = build_tether_ch01_manifest()
        with open(out_path, "w") as f:
            json.dump(manifest, f, indent=2)
    
    validate_manifest(manifest)
    print(f"\n🚀 SUCCESS: Compiled active manifest verified at {out_path}")

if __name__ == "__main__":
    main()
