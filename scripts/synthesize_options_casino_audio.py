#!/usr/bin/env python3
"""
Synthesize 36 Christopher Voiceover Tracks for Video #6:
'THE ZERO-DAY OPTIONS CASINO: The ₹1.8 Lakh Crore Retail Slaughter'
"""

import asyncio
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import edge_tts
from output.options_casino_documentary.chapters_script import SEGMENTS

VOICE = "en-US-ChristopherNeural"
PITCH = "-2Hz"
RATE = "+0%"
AUDIO_DIR = BASE_DIR / "output" / "options_casino_documentary" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

async def synth_segment(seg):
    sid = seg["id"]
    text = seg["voiceover"]
    out_file = AUDIO_DIR / f"vo_segment_{sid:02d}.mp3"
    communicate = edge_tts.Communicate(text, VOICE, pitch=PITCH, rate=RATE)
    await communicate.save(str(out_file))
    print(f"[{sid:02d}/36] Synthesized {out_file.name} ({out_file.stat().st_size} bytes)")

async def main():
    print("Synthesizing 36 voiceovers for Options Casino documentary...")
    for seg in SEGMENTS:
        await synth_segment(seg)
    print("All 36 voiceover tracks ready!")

if __name__ == "__main__":
    asyncio.run(main())
