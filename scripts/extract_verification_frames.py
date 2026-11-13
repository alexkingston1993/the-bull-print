#!/usr/bin/env python3
"""
scripts/extract_verification_frames.py

Extracts the 10 mandatory verification frames from output/remotion_magnates_master.mp4
using FFmpeg. Strictly for post-render audit and verification.
"""

import os
import subprocess
import sys

TIMESTAMPS = [
    ("02.5", "frame_01_t02_5_penthouse.png", "Scene 1: 3-Layer Penthouse Sandwich (text behind founder)"),
    ("07.5", "frame_02_t07_5_trading.png", "Scene 2: Trading Floor 3-Layer Sandwich"),
    ("12.2", "frame_03_t12_2_vault.png", "Scene 3A: Vault 3-Layer Sandwich (NEXT J.P. MORGAN)"),
    ("15.0", "frame_04_t15_0_forbes.png", "Scene 3B: 3D FORBES Magazine Cover slam"),
    ("18.2", "frame_05_t18_2_sequoia.png", "Scene 4A: SEQUOIA CAPITAL $210M Wire Card"),
    ("21.5", "frame_06_t21_5_flowchart.png", "Scene 4B: LivePonziFlowchart SVG pipes and deficit"),
    ("25.0", "frame_07_t25_0_subpoena_pre.png", "Scene 5A: Pure DOM Subpoena before stamp (100% legible)"),
    ("28.0", "frame_08_t28_0_subpoena_post.png", "Scene 5B: Pure DOM Subpoena highlighter + EVIDENCE ADMITTED"),
    ("31.0", "frame_09_t31_0_server.png", "Scene 6: Server Backdoor 3-Layer Sandwich"),
    ("35.0", "frame_10_t35_0_courtroom.png", "Scene 7: Courtroom Climax high-contrast scrim")
]

def extract_frames(video_path="output/remotion_magnates_master.mp4", out_dir="output/guardrail_frames"):
    if not os.path.exists(video_path):
        print(f"[ERROR] Master video not found at: {video_path}")
        sys.exit(1)
        
    os.makedirs(out_dir, exist_ok=True)
    print(f"=== EXTRACTING 10 MANDATORY VERIFICATION FRAMES FROM {video_path} ===")
    
    extracted = []
    for ts, fname, label in TIMESTAMPS:
        out_path = os.path.join(out_dir, fname)
        # Extract 1 frame at exact timestamp with ffmpeg
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
            
    print(f"\nSuccessfully extracted {len(extracted)}/10 verification frames to {out_dir}/")
    return extracted

if __name__ == "__main__":
    video = sys.argv[1] if len(sys.argv) > 1 else "output/remotion_magnates_master.mp4"
    extract_frames(video)
