#!/usr/bin/env python3
"""
Synthesize Christopher Voiceover Audio for all 10 Trump Election YouTube Shorts
Channel: The Bull Print
Voice: en-US-ChristopherNeural (-2Hz Pitch)
"""

import asyncio
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import edge_tts
from output.trump_shorts.shorts_data import SHORTS

VOICE = "en-US-ChristopherNeural"
PITCH = "-2Hz"
RATE = "+3%" # slightly brisk pacing for viral shorts
AUDIO_DIR = BASE_DIR / "output" / "trump_shorts" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

async def synth_short(short_item):
    sid = short_item["id"]
    text = short_item["voiceover"]
    out_file = AUDIO_DIR / f"vo_short_{sid:02d}.mp3"
    communicate = edge_tts.Communicate(text, VOICE, pitch=PITCH, rate=RATE)
    await communicate.save(str(out_file))
    print(f"[{sid:02d}/10] Synthesized {out_file.name} ({out_file.stat().st_size} bytes)")

async def main():
    print("Synthesizing 10 voiceovers for Trump Election Shorts...")
    for item in SHORTS:
        await synth_short(item)
    print("All 10 Trump Shorts voiceover tracks ready!")

if __name__ == "__main__":
    asyncio.run(main())
