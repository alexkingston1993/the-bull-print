"""
Synthesizes Christopher Voiceover for all 36 Segments of the 12-Minute Documentary.
Voice: en-US-ChristopherNeural
Output: output/ftx_documentary/vo_36_segments/seg_01.mp3 to seg_36.mp3
"""

import asyncio
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import edge_tts
from scripts.generate_36_segment_dossier import SEGMENTS

VOICE = "en-US-ChristopherNeural"
OUT_DIR = Path("output/ftx_documentary/vo_36_segments")
OUT_DIR.mkdir(parents=True, exist_ok=True)

async def synth_segment(seg_info):
    seg_num = seg_info["seg"]
    text = seg_info["script"]
    out_file = OUT_DIR / f"seg_{seg_num:02d}.mp3"
    
    if out_file.exists() and out_file.stat().st_size > 1000:
        return seg_num, out_file, "Cached"
        
    comm = edge_tts.Communicate(text, VOICE, rate="+0%", pitch="+0Hz")
    await comm.save(str(out_file))
    return seg_num, out_file, "Generated"

async def main():
    print(f"🎙️ Synthesizing 36 Voiceover Segments with {VOICE}...")
    tasks = [synth_segment(s) for s in SEGMENTS]
    results = await asyncio.gather(*tasks)
    for seg_num, path, status in sorted(results, key=lambda x: x[0]):
        size_kb = round(path.stat().st_size / 1024, 1)
        print(f"✓ Seg {seg_num:02d} ({status}): {path.name} ({size_kb} KB)")
    print(f"\n✅ All 36 Voiceover Segments Ready in {OUT_DIR}!")

if __name__ == "__main__":
    asyncio.run(main())
