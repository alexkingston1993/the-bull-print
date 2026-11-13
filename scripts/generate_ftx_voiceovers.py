#!/usr/bin/env python3
"""
scripts/generate_ftx_voiceovers.py
Generates edge-tts voiceovers for all 5 chapters of the 12-minute documentary.
Voice: en-GB-RyanNeural with deliberate documentary pacing.
"""

import asyncio
import edge_tts
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from output.ftx_documentary.chapters_script import CHAPTERS

AUDIO_DIR = BASE_DIR / "output" / "ftx_documentary" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "en-GB-RyanNeural"
RATE = "+0%"


async def generate_chapter_audio(ch_id: int, text: str):
    out_file = AUDIO_DIR / f"chapter_{ch_id}_vo.mp3"
    print(f"🎙️ Generating Voiceover for Chapter {ch_id} ({len(text.split())} words)...")
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(str(out_file))
    print(f"✅ Chapter {ch_id} audio saved to: {out_file.name}")


async def main():
    for ch_id, ch_data in CHAPTERS.items():
        await generate_chapter_audio(ch_id, ch_data["text"])
    print("🔥 All 5 Chapter Voiceovers Generated Successfully!")


if __name__ == "__main__":
    asyncio.run(main())
