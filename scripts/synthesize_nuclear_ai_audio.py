#!/usr/bin/env python3
"""
Synthesize 36 Christopher Voiceover Tracks and Extract Beat Timestamps for:
Documentary 3: THE ENERGY GRID CHOKEHOLD: Why Big Tech Is Buying Nuclear Reactors for AI
Channel: The Bull Print (@thebullprint)
Narrator: en-US-ChristopherNeural (-2Hz Pitch)
"""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import edge_tts
from output.nuclear_ai_documentary.chapters_script import SEGMENTS

VOICE = "en-US-ChristopherNeural"
PITCH = "-2Hz"
RATE = "+0%"
AUDIO_DIR = BASE_DIR / "output" / "nuclear_ai_documentary" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TIMING_FILE = BASE_DIR / "output" / "nuclear_ai_documentary" / "timing_and_timestamps.json"

def get_audio_duration(path: Path) -> float:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    out = subprocess.check_output(cmd).decode().strip()
    return float(out)

async def synth_segment(seg):
    sid = seg["id"]
    text = seg["voiceover"]
    out_file = AUDIO_DIR / f"vo_segment_{sid:02d}.mp3"
    
    if out_file.exists() and out_file.stat().st_size > 10000:
        print(f"[{sid:02d}/36] ⏩ Already exists: {out_file.name}")
    else:
        communicate = edge_tts.Communicate(text, VOICE, pitch=PITCH, rate=RATE)
        await communicate.save(str(out_file))
        print(f"[{sid:02d}/36] ✅ Synthesized {out_file.name} ({out_file.stat().st_size} bytes)")
    
    dur = get_audio_duration(out_file)
    return sid, dur

async def main():
    print("🎙️ Synthesizing 36 voiceover segments for Documentary #3 (Nuclear AI)...")
    timings = {}
    total_dur = 0.0
    
    for seg in SEGMENTS:
        sid, dur = await synth_segment(seg)
        beat_dur = round(dur / 5.0, 3)
        beats_meta = []
        for b in seg["beats"]:
            b_num = b["beat_num"]
            b_start = round((b_num - 1) * beat_dur, 2)
            b_end = round(b_num * beat_dur, 2)
            beats_meta.append({
                "beat_num": b_num,
                "start": b_start,
                "end": b_end,
                "duration": beat_dur,
                "anchor_text": b["anchor_text"],
                "badge_text": b["badge_text"],
                "visual_description": b["visual_description"],
                "prompt": b["prompt"]
            })
            
        timings[sid] = {
            "title": seg["title"],
            "act": seg["act"],
            "duration": dur,
            "beat_duration": beat_dur,
            "beats": beats_meta
        }
        total_dur += dur
        await asyncio.sleep(0.15)

    meta = {
        "documentary_title": "THE ENERGY GRID CHOKEHOLD: Nuclear AI",
        "total_segments": len(SEGMENTS),
        "total_beats": len(SEGMENTS) * 5,
        "total_voiceover_duration_seconds": round(total_dur, 2),
        "total_voiceover_duration_minutes": round(total_dur / 60.0, 2),
        "segments": timings
    }

    with open(TIMING_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print("\n" + "="*60)
    print(f"🎉 ALL 36 SEGMENTS SYNTHESIZED & TIMESTAMPED FOR DOC #3!")
    print(f"Total Duration: {total_dur:.2f}s ({total_dur/60.0:.2f} minutes)")
    print(f"Saved Timings & Beats to: {TIMING_FILE}")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
