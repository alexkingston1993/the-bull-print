import asyncio
import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import edge_tts
from output.options_casino_documentary.chapters_script import SEGMENTS

OUT_JSON = BASE_DIR / "output" / "options_casino_documentary" / "all_36_word_timings.json"

RED_TRIGGER_WORDS = {
    "VAPORIZED", "ZERO", "WORTHLESS", "RED-STAINED", "LOSS", "CRASH", "BAD",
    "SLAUGHTER", "BLACK", "HOLE", "LOST", "LIE", "TRAPPED", "CRUSH", "PARABOLIC",
    "HUNT", "LATENCY", "MARGIN", "SQUEEZE", "BANKRUPTCY", "RUIN", "FAKE", "SCAMS",
    "EXPOSED", "SEIZES", "ADDICTION", "SHATTERED", "CLAMPDOWN", "HAMMER", "DISQUALIFIED",
    "INCINERATED", "FRICTION", "DRAINING", "LIQUIDATED", "WIPED"
}

async def process_all_segments():
    print(f"🎙️ Extracting word timestamps for all {len(SEGMENTS)} segments...")
    all_data = {}

    for seg in SEGMENTS:
        sid = seg["id"]
        vo_text = seg["voiceover"]
        
        comm = edge_tts.Communicate(vo_text, "en-US-ChristopherNeural", pitch="-2Hz")
        sentences = []
        async for chunk in comm.stream():
            if chunk["type"] == "SentenceBoundary":
                st = chunk["offset"] / 10000000.0
                dur = chunk["duration"] / 10000000.0
                sentences.append({
                    "start": st,
                    "end": st + dur,
                    "dur": dur,
                    "text": chunk["text"]
                })
        
        # If no sentence boundary emitted (short line), fallback to full duration
        if not sentences:
            sentences.append({"start": 0.1, "end": 20.0, "dur": 19.9, "text": vo_text})

        # Process each sentence into word timeline with chunking of 3-5 words
        seg_chunks = []
        for s in sentences:
            s_text = s["text"]
            words = [w for w in s_text.split() if w]
            if not words:
                continue

            weights = [max(len(re.sub(r"[^\w]", "", w)), 2) for w in words]
            total_wt = sum(weights)
            s_dur = s["dur"]

            # Chunk into phrases of 4 words
            chunk_size = 4
            chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]

            curr_t = s["start"]
            word_idx = 0
            for c in chunks:
                c_start = curr_t
                words_meta = []
                for w in c:
                    w_wt = weights[word_idx]
                    w_dur = (w_wt / total_wt) * s_dur
                    clean = re.sub(r"[^\w\$\:\-]", "", w).upper()
                    is_red = clean in RED_TRIGGER_WORDS
                    words_meta.append({
                        "word": w,
                        "clean": clean,
                        "start": round(curr_t, 3),
                        "end": round(curr_t + w_dur, 3),
                        "is_red": is_red
                    })
                    curr_t += w_dur
                    word_idx += 1
                c_end = curr_t
                seg_chunks.append({
                    "chunk_start": round(c_start, 3),
                    "chunk_end": round(c_end, 3),
                    "words": words_meta
                })

        all_data[str(sid)] = seg_chunks
        print(f"[{sid:02d}/36] Extracted {len(seg_chunks)} timed caption phrases for: {seg['title']}")

    OUT_JSON.write_text(json.dumps(all_data, indent=2))
    print(f"\n🎉 Saved all 36 segment word timings to: {OUT_JSON.name}")

if __name__ == "__main__":
    asyncio.run(process_all_segments())
