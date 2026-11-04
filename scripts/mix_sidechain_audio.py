#!/usr/bin/env python3
"""
scripts/mix_sidechain_audio.py

Computes sidechain ducking volume curves based on word_timestamps.json:
- Whenever voiceover is actively speaking a word, background tracks duck by -3.5 dB (x0.67)
- In pauses between sentences, background tracks swell back to 1.0
- Preserves 300ms acoustic silence cut prior to the final courtroom verdict
"""

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TIMESTAMPS_PATH = BASE_DIR / "remotion-engine" / "public" / "assets" / "word_timestamps.json"
OUTPUT_CURVE_PATH = BASE_DIR / "remotion-engine" / "public" / "assets" / "audio_sidechain_curve.json"

def compute_sidechain_curve(fps=30, total_frames=1095):
    if not TIMESTAMPS_PATH.exists():
        print(f"[ERROR] Timestamps not found at {TIMESTAMPS_PATH}")
        return

    with open(TIMESTAMPS_PATH, "r", encoding="utf-8") as f:
        words = json.load(f)

    # Frame-by-frame speech activity mask
    is_speaking = [False] * total_frames
    for w in words:
        start_frame = int(w.get("startSec", 0) * fps)
        end_frame = int(w.get("endSec", 0) * fps) + 1
        for fr in range(max(0, start_frame), min(total_frames, end_frame)):
            is_speaking[fr] = True

    # 300ms silence cut right before gavel impact at frame 990 and final cut at 1080-1095
    # Frame 981 to 990 (300ms before 990)
    for fr in range(980, 990):
        is_speaking[fr] = False

    volume_curve = []
    # Smooth attack and release (2 frames attack, 4 frames release)
    current_vol = 1.0
    for fr in range(total_frames):
        # Target volume: 0.67 (-3.5 dB) if speaking, 0.0 in blackout (1080-1095), 1.0 in pauses
        if fr >= 1080:
            target = 0.0
        elif 980 <= fr < 990:
            target = 0.05 # acoustic breather
        elif is_speaking[fr]:
            target = 0.67 # ducked by -3.5dB
        else:
            target = 1.0 # swell in phrase gaps

        # Smooth interpolation
        current_vol += (target - current_vol) * 0.35
        volume_curve.append(round(current_vol, 3))

    with open(OUTPUT_CURVE_PATH, "w", encoding="utf-8") as f:
        json.dump(volume_curve, f)

    print(f"✅ Generated Sidechain Volume Curve: {OUTPUT_CURVE_PATH}")
    print(f"   Total frames: {len(volume_curve)}")
    print(f"   Average volume during speech: {sum(v for i, v in enumerate(volume_curve) if is_speaking[i]) / max(1, sum(is_speaking)):.2f}")

if __name__ == "__main__":
    compute_sidechain_curve()
