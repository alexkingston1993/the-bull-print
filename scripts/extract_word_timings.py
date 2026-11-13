#!/usr/bin/env python3
"""
scripts/extract_word_timings.py
Generates word-level timestamps (word_timestamps.json) by streaming SentenceBoundary
metadata from edge-tts and performing character/phoneme-weighted alignment for every word.
"""

import asyncio
import json
import re
from pathlib import Path
import edge_tts

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_JSON = BASE_DIR / "remotion-engine" / "public" / "assets" / "word_timestamps.json"
OUTPUT_AUDIO = BASE_DIR / "remotion-engine" / "public" / "audio" / "narration.mp3"

OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_AUDIO.parent.mkdir(parents=True, exist_ok=True)

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

VOICE = "en-GB-RyanNeural"
RATE = "-4%"


async def main():
    print(f"🎙️ Generating narration and word-level timestamps ({len(SCRIPT.split())} words)...")
    communicate = edge_tts.Communicate(SCRIPT, VOICE, rate=RATE)

    sentences = []
    audio_bytes = bytearray()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes.extend(chunk["data"])
        elif chunk["type"] == "SentenceBoundary":
            start_ms = chunk["offset"] / 10000.0
            dur_ms = chunk["duration"] / 10000.0
            text = chunk["text"]
            sentences.append({
                "text": text,
                "start_ms": start_ms,
                "dur_ms": dur_ms,
                "end_ms": start_ms + dur_ms
            })

    # Save audio file
    with open(OUTPUT_AUDIO, "wb") as f:
        f.write(audio_bytes)
    print(f"✅ Audio written to: {OUTPUT_AUDIO.name} ({len(audio_bytes)} bytes)")

    # Now calculate exact word timings
    words_data = []
    for s in sentences:
        s_text = s["text"]
        s_words = s_text.split()
        if not s_words:
            continue

        # Weight each word by character count + bonus for punctuation pause
        weights = []
        for w in s_words:
            w_clean = re.sub(r"[^\w]", "", w)
            wt = max(len(w_clean), 2)
            if w.endswith(",") or w.endswith(";"):
                wt += 3 # Pause weighting
            elif w.endswith(".") or w.endswith("!") or w.endswith("?"):
                wt += 4 # Sentence end pause
            weights.append(wt)

        total_weight = sum(weights)
        curr_ms = s["start_ms"]

        for idx, w in enumerate(s_words):
            word_dur = (weights[idx] / total_weight) * s["dur_ms"]
            # Deduct slight gap for word separation
            active_dur = max(word_dur * 0.88, 120.0)
            words_data.append({
                "word": w,
                "clean": re.sub(r"[^\w\$\-]", "", w),
                "startMs": round(curr_ms, 2),
                "endMs": round(curr_ms + active_dur, 2),
                "startSec": round(curr_ms / 1000.0, 3),
                "endSec": round((curr_ms + active_dur) / 1000.0, 3),
                # Trigger words get highlighted in Remotion
                "isTrigger": any(kw in w.upper() for kw in [
                    "$30", "MILLION", "BAHAMAS", "EMPIRE", "WALL", "STREET",
                    "JP", "MORGAN", "FORBES", "SEQUOIA", "$16", "BILLION",
                    "DEPOSITS", "PROBLEM", "BACKDOOR", "$8", "GONE", "VANISHED"
                ])
            })
            curr_ms += word_dur

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(words_data, f, indent=2)

    print(f"✅ Extracted {len(words_data)} word-level timestamps into: {OUTPUT_JSON.name}")
    print(f"   First word: '{words_data[0]['word']}' at {words_data[0]['startMs']}ms")
    print(f"   Last word: '{words_data[-1]['word']}' at {words_data[-1]['startMs']}ms")


if __name__ == "__main__":
    asyncio.run(main())
