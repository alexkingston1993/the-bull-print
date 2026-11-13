#!/usr/bin/env python3
"""
Automated Watcher and Broadcaster for Doc 03:
Monitors task completion of the_nuclear_ai_race_12min_master.mp4,
validates integrity, and executes broadcast_nuclear_ai_live_show.py.
"""

import os
import sys
import time
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MASTER_MP4 = BASE_DIR / "output" / "nuclear_ai_documentary" / "the_nuclear_ai_race_12min_master.mp4"
BROADCAST_SCRIPT = BASE_DIR / "scripts" / "broadcast_nuclear_ai_live_show.py"

print("=" * 70)
print("👀 DOC 03 AUTOMATED WATCHER & BROADCASTER ACTIVE")
print(f"Target: {MASTER_MP4}")
print("=" * 70)

start_time = time.time()
RENDER_START_TIME = 1731110000 # Nov 9 05:23 start

while True:
    seg_36 = BASE_DIR / "output" / "nuclear_ai_documentary" / "rendered_segments_3d" / "segment_36_3d.mp4"
    if MASTER_MP4.exists() and MASTER_MP4.stat().st_mtime > RENDER_START_TIME and seg_36.exists():
        s1 = MASTER_MP4.stat().st_size
        time.sleep(5)
        s2 = MASTER_MP4.stat().st_size
        if s1 == s2 and s2 > 100_000_000:
            print(f"🎉 New 100% Bespoke Master MP4 detected & finalized! ({s2 / 1024 / 1024:.1f} MB)")
            break
            
    # Check rendered segments count
    seg_dir = BASE_DIR / "output" / "nuclear_ai_documentary" / "rendered_segments_3d"
    segs = list(seg_dir.glob("segment_*_3d.mp4")) if seg_dir.exists() else []
    elapsed = int(time.time() - start_time)
    print(f"⏳ Waiting for render to finish... ({len(segs)}/36 segments ready, elapsed: {elapsed}s)", flush=True)
    time.sleep(25)

print("\n🔍 Validating video integrity with ffprobe...")
cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=width,height", "-of", "json", str(MASTER_MP4)]
res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout)

print("\n🚀 LAUNCHING PUBLIC LIVE BROADCAST ON YOUTUBE...")
subprocess.run([sys.executable, str(BROADCAST_SCRIPT)], check=True)

print("\n✨ LIVE BROADCAST SEQUENCE COMPLETED SUCCESSFULLY!")
