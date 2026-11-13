#!/usr/bin/env python3
"""
The Bull Print — Viral Short Video Compiler
Topic: "The ₹65,700 Cr FII Rotation: Why Wall Street Is Dumping Nvidia to Flood Indian Bluechips"
Format: 9:16 Vertical (1080x1920)
Cadence: Exactly 1 unique plate every 3.0s (20 clean Kaggle GPU vertical plates)
Voice: en-US-ChristopherNeural (-2Hz Pitch)
Output: output/the_fii_rotation_viral_short_master.mp4
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import edge_tts

SHORT_DIR = BASE_DIR / "output" / "viral_short_fii_rotation"
FRAMES_DIR = SHORT_DIR / "frames"
AUDIO_FILE = SHORT_DIR / "voiceover.mp3"
FINAL_MP4 = BASE_DIR / "output" / "the_fii_rotation_viral_short_master.mp4"
BGM_FILE = BASE_DIR / "assets" / "audio" / "bgm_pool" / "bed_01_subterranean_pulse.wav"

SHORT_DIR.mkdir(parents=True, exist_ok=True)
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

# 60-Second Viral Short Script across 20 beats (3.0s each)
SHORT_SCRIPT = (
    "In the last twenty-four hours, Wall Street suffered a seismic shockwave. "
    "Nvidia shares plummeted nine percent after hours to one hundred fifty-nine dollars amidst an emergency board investigation. "
    "Over five hundred billion dollars in artificial intelligence market value evaporated overnight. "
    "At the exact same time, ten thousand miles away, the Bombay Stock Exchange exploded to eight-month all-time highs. "
    "Foreign institutional investors have poured over sixty-five thousand seven hundred crore rupees into Indian blue chips this month alone. "
    "Global hedge funds are actively liquidating overheated American tech momentum to chase high-yield emerging market cash flows. "
    "As crude oil prices dropped to ninety-one dollars, India's macroeconomic balance sheet became Wall Street's ultimate liquidity refuge. "
    "The institutional rotation has begun. Smart money is taking profits at the top, leaving retail traders holding the bag. "
    "Follow The Bull Print for real forensic market intelligence before the crowd wakes up."
)

BEAT_HEADLINES = [
    ("MARKET ALERT ⚠️", "NVIDIA $159 CRASH"),
    ("BOARD PROBE", "EXECUTIVE AUDIT"),
    ("500B VANISH", "AI MARKET WIPEOUT"),
    ("GLOBAL PIVOT", "BSE ALL-TIME HIGH"),
    ("FOREIGN CAPITAL", "65,700 CR FLOOD"),
    ("WALL STREET EXIT", "INSTITUTIONAL RUN"),
    ("OIL RELIEF", "MACRO TAILWIND"),
    ("ROTATION TRAP", "SMART MONEY MOVE"),
    ("RETAIL EXPOSURE", "TOP TICK LIQUIDITY"),
    ("THE VERDICT", "THE BULL PRINT")
]

VOICE = "en-US-ChristopherNeural"
PITCH = "-2Hz"

def link_kaggle_vertical_frames():
    src_dir = Path("/tmp/kaggle_viral_short_clean/frames")
    for i in range(1, 21):
        src = src_dir / f"segment_{i:02d}.jpg"
        dst = FRAMES_DIR / f"beat_{i:02d}.jpg"
        if src.exists():
            subprocess.run(["cp", str(src), str(dst)], check=True)
    print(f"✓ Linked 20 clean vertical frames into {FRAMES_DIR}")

async def synth_voice():
    print("🎙️ Synthesizing Christopher voiceover for viral short...")
    comm = edge_tts.Communicate(SHORT_SCRIPT, VOICE, pitch=PITCH)
    await comm.save(str(AUDIO_FILE))
    print(f"✓ Short voiceover synthesized: {AUDIO_FILE.name}")

def render_short_video():
    cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(AUDIO_FILE)]
    total_dur = float(subprocess.check_output(cmd_dur).decode().strip())
    beat_dur = total_dur / 20.0

    print(f"🎬 Assembling 60s vertical short ({total_dur:.1f}s, 20 beats @ {beat_dur:.2f}s/beat)...")

    inputs = []
    for i in range(1, 21):
        inputs.extend(["-loop", "1", "-t", str(beat_dur), "-i", str(FRAMES_DIR / f"beat_{i:02d}.jpg")])

    inputs.extend(["-i", str(AUDIO_FILE)])
    inputs.extend(["-stream_loop", "-1", "-i", str(BGM_FILE)])

    # Video filter: scale & crop to 1080x1920 (9:16 vertical full-bleed)
    filter_complex = (
        "".join(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v{i}];" for i in range(20)) +
        "".join(f"[v{i}]" for i in range(20)) +
        "concat=n=20:v=1:a=0[vcat];"
        "[vcat]vignette=PI/5[vfinal];"
        "[20:a]volume=1.0[vo];"
        "[21:a]volume=0.12[bgm];"
        "[vo][bgm]amix=inputs=2:duration=first:dropout_transition=2[afinal]"
    )

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[vfinal]",
        "-map", "[afinal]",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", str(total_dur),
        str(FINAL_MP4)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"🏆 VIRAL SHORT COMPILED: {FINAL_MP4} ({FINAL_MP4.stat().st_size / 1e6:.1f} MB)")

async def main():
    link_kaggle_vertical_frames()
    await synth_voice()
    render_short_video()

if __name__ == "__main__":
    asyncio.run(main())

