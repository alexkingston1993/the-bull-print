#!/usr/bin/env python3
"""
scripts/extract_short_verification_frames.py

Extracts key verification frames from output/remotion_magnates_short.mp4
for post-render audit of the 9:16 Vertical Short.
"""

import os
import subprocess
import sys

SHORT_TIMESTAMPS = [
    ("02.5", "short_frame_01_t02_5_penthouse.png", "Scene 1: Vertical 3-Layer Penthouse"),
    ("07.5", "short_frame_02_t07_5_trading.png", "Scene 2: Vertical 3-Layer Trading"),
    ("12.2", "short_frame_03_t12_2_vault.png", "Scene 3A: Vault Sandwich (No Guillotine)"),
    ("15.0", "short_frame_04_t15_0_forbes.png", "Scene 3B: 3D Forbes Cover (720px safe zone)"),
    ("18.2", "short_frame_05_t18_2_sequoia.png", "Scene 4A: Sequoia Card (860px safe zone, no collision)"),
    ("21.5", "short_frame_06_t21_5_flowchart.png", "Scene 4B: Live Ponzi Flowchart (Vertical 3-node stack)"),
    ("25.0", "short_frame_07_t25_0_subpoena.png", "Scene 5A: Pure DOM Subpoena Vertical"),
    ("28.0", "short_frame_08_t28_0_subpoena_stamp.png", "Scene 5B: Subpoena with Stamp Vertical"),
    ("31.0", "short_frame_09_t31_0_server.png", "Scene 6: Server Backdoor Sandwich (No Guillotine)"),
    ("35.0", "short_frame_10_t35_0_courtroom.png", "Scene 7: Courtroom Climax Vertical"),
]

def extract_short_frames(video_path="output/remotion_magnates_short.mp4", out_dir="output/guardrail_short_frames"):
    if not os.path.exists(video_path):
        print(f"[ERROR] Short video not found at: {video_path}")
        sys.exit(1)
        
    os.makedirs(out_dir, exist_ok=True)
    print(f"=== EXTRACTING SHORT VERIFICATION FRAMES FROM {video_path} ===")
    
    extracted = []
    for ts, fname, label in SHORT_TIMESTAMPS:
        out_path = os.path.join(out_dir, fname)
        cmd = [
            "ffmpeg", "-y",
            "-ss", ts,
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            out_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0 and os.path.exists(out_path):
            file_size = os.path.getsize(out_path)
            print(f"[OK] {ts}s -> {fname} ({file_size / 1024:.1f} KB) | {label}")
            extracted.append((ts, out_path, label))
        else:
            print(f"[FAIL] {ts}s -> {fname}: {result.stderr[-200:]}")
            
    print(f"\nSuccessfully extracted {len(extracted)}/10 short frames to {out_dir}/")
    return extracted

if __name__ == "__main__":
    extract_short_frames()
