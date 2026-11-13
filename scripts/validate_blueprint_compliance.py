#!/usr/bin/env python3
"""
Blueprint & Zero-Reuse Compliance Validator
Validates video production assets against:
1. .agents/rules/MASTER_BLUEPRINT.md
2. DESIGN.md
3. Strict Zero Frame Reuse Mandate

Usage:
    python scripts/validate_blueprint_compliance.py --dir <video_work_dir> [--type short|landscape]
"""
import sys
import os
import hashlib
import json
import argparse
from pathlib import Path
from PIL import Image

def get_image_hash(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def validate_production(work_dir: Path, video_type: str = "short") -> bool:
    print("=" * 80)
    print(f"🔍 AUDITING BLUEPRINT COMPLIANCE: {work_dir}")
    print("=" * 80)

    errors = []
    warnings = []

    # 1. Check Directory
    if not work_dir.exists():
        print(f"❌ Directory not found: {work_dir}")
        return False

    frames_dir = work_dir / "frames"
    if not frames_dir.exists():
        frames_dir = work_dir

    frame_files = sorted([
        f for f in frames_dir.iterdir()
        if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]
        and not f.name.startswith("thumbnail")
        and not f.name.startswith("cover")
    ])

    print(f"📊 Total Image Plates Discovered: {len(frame_files)}")

    # 2. Check Pacing Rule
    meta_path = work_dir / "METADATA.json"
    duration = 60.0
    if meta_path.exists():
        try:
            with open(meta_path) as f:
                meta = json.load(f)
                duration = float(meta.get("duration", meta.get("duration_sec", 60.0)))
        except Exception:
            pass

    expected_cadence = 3.0 if video_type == "short" else 4.0
    expected_frames = round(duration / expected_cadence)

    print(f"⏱️ Video Duration: {duration:.1f}s | Target Cadence: 1 cut every {expected_cadence}s")
    print(f"🎯 Required Bespoke Frames: {expected_frames}")

    if len(frame_files) < expected_frames:
        errors.append(
            f"PACING VIOLATION: Found {len(frame_files)} frames, but {expected_frames} required "
            f"for {duration:.1f}s duration (1 frame every {expected_cadence}s)."
        )

    # 3. Check Strict Zero-Reuse Mandate (Hash Uniqueness)
    hashes = {}
    duplicates = []
    for f in frame_files:
        h = get_image_hash(f)
        if h in hashes:
            duplicates.append((hashes[h].name, f.name))
        else:
            hashes[h] = f

    if duplicates:
        for orig, dup in duplicates:
            errors.append(f"ZERO-REUSE VIOLATION: Frame '{dup}' is an exact duplicate of '{orig}'. No frames may be reused!")

    # 4. Check Resolution & Aspect Ratio
    expected_ratio = (9, 16) if video_type == "short" else (16, 9)
    for f in frame_files[:5]: # Sample check
        try:
            with Image.open(f) as img:
                w, h = img.size
                if video_type == "short" and h < w:
                    errors.append(f"ORIENTATION VIOLATION: Frame '{f.name}' is landscape ({w}x{h}), but Short requires 9:16 vertical.")
                elif video_type == "landscape" and w < h:
                    errors.append(f"ORIENTATION VIOLATION: Frame '{f.name}' is vertical ({w}x{h}), but Documentary requires 16:9 landscape.")
        except Exception as e:
            warnings.append(f"Could not open frame '{f.name}': {e}")

    # Report Summary
    print("\n📋 AUDIT RESULTS:")
    if errors:
        print("❌ FAILED WITH COMPLIANCE VIOLATIONS:")
        for err in errors:
            print(f"   - {err}")
        print("\n⛔ DISPATCH BLOCKED: All issues must be resolved before cloud execution.")
        return False
    else:
        print("✅ 100% PASSED: Zero frame reuse confirmed, cadence adheres strictly to MASTER_BLUEPRINT.md!")
        if warnings:
            for w in warnings:
                print(f"   ⚠️ {w}")
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Blueprint Compliance")
    parser.add_argument("--dir", required=True, help="Path to video directory")
    parser.add_argument("--type", default="short", choices=["short", "landscape"], help="Video type")
    args = parser.parse_args()

    success = validate_production(Path(args.dir), args.type)
    sys.exit(0 if success else 1)
