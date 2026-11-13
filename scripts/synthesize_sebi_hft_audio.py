import asyncio
import os
import sys
from pathlib import Path
import edge_tts

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from output.sebi_hft_documentary.chapters_script import SEGMENTS

VOICE = "en-US-ChristopherNeural"
RATE = "+0%"
PITCH = "-2Hz"

AUDIO_DIR = BASE_DIR / "output" / "sebi_hft_documentary" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

async def synthesize_all():
    print(f"Synthesizing {len(SEGMENTS)} voiceover segments using {VOICE}...")
    for seg in SEGMENTS:
        seg_id = seg["id"]
        text = seg["voiceover"]
        out_file = AUDIO_DIR / f"vo_segment_{seg_id:02d}.mp3"
        print(f"[{seg_id:02d}/36] Synthesizing: {seg['title']} ({len(text.split())} words)...")
        
        communicate = edge_tts.Communicate(text, voice=VOICE, rate=RATE, pitch=PITCH)
        await communicate.save(str(out_file))
        
    print("\nAll 36 voiceover segments synthesized successfully!")

if __name__ == "__main__":
    asyncio.run(synthesize_all())
