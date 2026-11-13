#!/usr/bin/env python3
"""
Synthesize 36 voiceover audio segments for Video 5: The Health Insurance Claim Rejection Machine using edge-tts.
Narrator: en-US-ChristopherNeural (-2Hz Pitch)
"""

import asyncio
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from output.health_insurance_scam_documentary.chapters_script import SEGMENTS
import edge_tts

AUDIO_DIR = Path("output/health_insurance_scam_documentary/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

async def synth_segment(seg):
    seg_id = seg["id"]
    text = seg["voiceover"]
    out_file = AUDIO_DIR / f"vo_segment_{seg_id:02d}.mp3"
    
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-ChristopherNeural",
        rate="+0%",
        pitch="-2Hz"
    )
    await communicate.save(str(out_file))
    print(f"[{seg_id:02d}/36] Synthesized {out_file.name} ({out_file.stat().st_size} bytes)")

async def main():
    print(f"Synthesizing {len(SEGMENTS)} voiceovers for Health Insurance documentary...")
    for seg in SEGMENTS:
        await synth_segment(seg)
    print("All 36 voiceover tracks ready!")

if __name__ == "__main__":
    asyncio.run(main())
