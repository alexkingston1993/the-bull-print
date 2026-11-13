#!/usr/bin/env python3
"""
scripts/harvest_christopher_ref.py

ONE-TIME GOLDEN REFERENCE HARVESTER:
Captures our master reference audio from edge-tts ONE TIME ONLY:
- Voice: en-US-ChristopherNeural
- Rate: -2%
- Pitch: -2Hz

Outputs:
- assets/voice_model/christopher_ref/ref_text.txt
- assets/voice_model/christopher_ref/christopher_master_24k.wav (24000Hz, 16-bit mono)
"""

import asyncio
import os
import subprocess
from pathlib import Path
import edge_tts

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "assets/voice_model/christopher_ref"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REF_TEXT = (
    "In the shadow of Wall Street, one hundred and ten billion dollars moved silently across "
    "offshore ledgers. Behind locked glass doors, executives engineered a financial machine "
    "that regulators never saw coming—until the entire system began to fracture."
)

TEXT_PATH = OUTPUT_DIR / "ref_text.txt"
RAW_MP3_PATH = OUTPUT_DIR / "raw_harvest.mp3"
WAV_24K_PATH = OUTPUT_DIR / "christopher_master_24k.wav"

VOICE = "en-US-ChristopherNeural"
RATE = "-2%"
PITCH = "-2Hz"

async def harvest():
    print(f"🎙️ Harvesting one-time golden reference for: {VOICE} ({RATE}, {PITCH})...")
    
    # 1. Write reference text
    TEXT_PATH.write_text(REF_TEXT, encoding="utf-8")
    print(f"  ✓ Reference text saved: {TEXT_PATH}")
    
    # 2. Synthesize via edge-tts
    communicate = edge_tts.Communicate(REF_TEXT, VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(str(RAW_MP3_PATH))
    print(f"  ✓ Raw audio harvested: {RAW_MP3_PATH}")
    
    # 3. Convert to 24000Hz 16-bit mono WAV
    cmd = [
        "ffmpeg", "-y",
        "-i", str(RAW_MP3_PATH),
        "-ar", "24000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        str(WAV_24K_PATH)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  ✓ Uncompressed 24k reference WAV generated: {WAV_24K_PATH}")
    
    # Probe duration
    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(WAV_24K_PATH)
    ], stdout=subprocess.PIPE, text=True, check=True)
    duration = float(probe.stdout.strip())
    print(f"  🎉 Golden reference harvest COMPLETE! Duration: {duration:.2f}s")

if __name__ == "__main__":
    asyncio.run(harvest())
