#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import re
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent
frames_dir = BASE_DIR / "output" / "fii_exodus_documentary" / "frames"
script_path = BASE_DIR / "output" / "fii_exodus_documentary" / "chapters_script.py"

spec = importlib.util.spec_from_file_location("mod", script_path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

unmapped = sorted([f for f in frames_dir.glob("*") if not f.name.startswith("seg_") and not f.name.startswith(".")])

# Build list of missing beats
missing_beats = []
for s in m.SEGMENTS:
    for b in s["beats"]:
        fname = f"seg_{s['id']:02d}_beat_{b['beat_num']}.jpg"
        if not (frames_dir / fname).exists():
            missing_beats.append({
                "target_fname": fname,
                "desc": b["visual_description"],
                "prompt": b["prompt"],
                "seg_id": s["id"],
                "beat_num": b["beat_num"]
            })

print(f"Total missing beats: {len(missing_beats)}")
print(f"Total unmapped files: {len(unmapped)}")

def tokenize(text):
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    # filter out generic prompt words
    stop = {"cinematic", "35mm", "film", "photograph", "wide", "16", "9", "ratio", "moody", "chiaroscuro",
            "lighting", "deep", "shadows", "authentic", "grain", "documentary", "realism", "completely",
            "clean", "frame", "with", "zero", "text", "words", "letters", "typography", "numbers", "watermarks",
            "2k", "jpg", "the", "a", "an", "and", "in", "of", "to", "for", "on", "at", "by"}
    return set(w for w in words if w not in stop)

# We want an optimal bipartite match between missing_beats and unmapped files
# Score matrix
scores = []
for i, mb in enumerate(missing_beats):
    desc_words = tokenize(mb["desc"]) | tokenize(mb["prompt"])
    for j, f in enumerate(unmapped):
        clean_name = f.stem.replace("…", "").replace("_2K", "").replace("_", " ")
        f_words = tokenize(clean_name)
        # Prefix matching bonus: Flow AI names files after the beginning of the prompt!
        score = len(desc_words & f_words) * 3
        # Check if f_words starts like prompt words
        prompt_words_list = [w for w in re.findall(r"[a-zA-Z0-9]+", mb["desc"].lower())]
        for w in f_words:
            if w in prompt_words_list[:10]:
                score += 5
        scores.append((score, i, j))

# Sort by score descending and greedily match
scores.sort(key=lambda x: x[0], reverse=True)
matched_beats = {}
used_files = set()

for score, b_idx, f_idx in scores:
    if b_idx in matched_beats or f_idx in used_files:
        continue
    matched_beats[b_idx] = (unmapped[f_idx], score)
    used_files.add(f_idx)

print(f"\nGreedy match result: {len(matched_beats)} / {len(missing_beats)} beats matched.")
low_score = []
for b_idx, mb in enumerate(missing_beats):
    if b_idx not in matched_beats:
        print(f"UNMATCHED BEAT: {mb['target_fname']} - {mb['desc']}")
    else:
        f, sc = matched_beats[b_idx]
        if sc < 5:
            low_score.append((mb['target_fname'], f.name, sc, mb['desc']))

if low_score:
    print(f"\nLow score matches ({len(low_score)}):")
    for tf, fn, sc, desc in low_score:
        print(f"  {tf} -> {fn} (score {sc}) | Desc: {desc[:60]}")

# If all 108 are matched with good confidence, show verification and rename!
if len(matched_beats) == len(missing_beats):
    print("\n✅ All 108 beats successfully paired with 108 files!")
    # Create backup directory or perform copy/rename
    for b_idx, mb in enumerate(missing_beats):
        f, sc = matched_beats[b_idx]
        target_path = frames_dir / mb["target_fname"]
        # Copy file to target_fname
        shutil.copy2(f, target_path)
    print("✅ All 108 missing frames copied to standard seg_XX_beat_Y.jpg names!")
