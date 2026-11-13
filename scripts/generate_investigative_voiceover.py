#!/usr/bin/env python3
"""
scripts/generate_investigative_voiceover.py
Generates high-retention British documentary voiceover with deliberate investigative pacing.
Voice: en-GB-RyanNeural
"""

import asyncio
import edge_tts
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output" / "magnates_editorial"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
VO_PATH = OUTPUT_DIR / "investigative_vo_36s.mp3"

SCRIPT = (
    "In November 2022, inside a thirty-million-dollar penthouse in the Bahamas, "
    "a thirty-year-old in cargo shorts ran a global financial empire. "
    "To Wall Street, Sam Bankman-Fried was the next J.P. Morgan. "
    "Profiled on the cover of Forbes. Backed by Sequoia. "
    "And trusted with sixteen billion dollars in customer deposits. "
    "There was only one problem. "
    "Deep inside the raw code of the trading engine, "
    "lay a single hidden backdoor. "
    "And by the time the music stopped, "
    "eight billion dollars in client money was gone."
)


async def main():
    print(f"🎙️ Synthesizing investigative documentary voiceover ({len(SCRIPT.split())} words)...")
    # -4% rate gives deliberate, authoritative documentary cadence
    communicate = edge_tts.Communicate(SCRIPT, voice="en-GB-RyanNeural", rate="-4%")
    await communicate.save(str(VO_PATH))
    print(f"✅ Voiceover saved: {VO_PATH.name}")


if __name__ == "__main__":
    asyncio.run(main())
