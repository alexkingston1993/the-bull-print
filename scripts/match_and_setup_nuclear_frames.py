#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import re
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent
frames_dir = BASE_DIR / "output" / "nuclear_ai_documentary" / "frames"
dl_dir = Path.home() / "Downloads"
script_path = BASE_DIR / "output" / "nuclear_ai_documentary" / "chapters_script.py"

spec = importlib.util.spec_from_file_location("mod", script_path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

all_beats = []
for s in m.SEGMENTS:
    for b in s["beats"]:
        all_beats.append({
            "target_fname": f"seg_{s['id']:02d}_beat_{b['beat_num']}.jpg",
            "desc": b["visual_description"],
            "prompt": b["prompt"],
            "seg_id": s["id"],
            "beat_num": b["beat_num"]
        })

print(f"Total expected beats for Doc 03: {len(all_beats)}")

# Find which beats already have seg_*.jpg
existing = {f.name: f for f in frames_dir.glob("seg_*.jpg")}
print(f"Already have named seg_*.jpg: {len(existing)}")

missing_beats = [b for b in all_beats if b["target_fname"] not in existing]
print(f"Missing beats to match: {len(missing_beats)}")

# Gather unmapped candidates from Downloads and frames_dir
candidates = []
# Flow AI downloads from today
for f in dl_dir.glob("*_2K.jpg"):
    candidates.append(f)
# Any unmapped files in frames_dir
for f in frames_dir.glob("*.jpg"):
    if not f.name.startswith("seg_"):
        candidates.append(f)

# Deduplicate candidates by name
cand_dict = {f.name: f for f in candidates}
candidates = list(cand_dict.values())
print(f"Total candidate files to match from: {len(candidates)}")

def tokenize(text):
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    stop = {"cinematic", "35mm", "film", "photograph", "wide", "16", "9", "ratio", "moody", "chiaroscuro",
            "lighting", "deep", "shadows", "authentic", "grain", "documentary", "realism", "completely",
            "clean", "frame", "with", "zero", "text", "words", "letters", "typography", "numbers", "watermarks",
            "2k", "jpg", "the", "a", "an", "and", "in", "of", "to", "for", "on", "at", "by", "near", "with"}
    return set(w for w in words if w not in stop)

# Build score matrix
scores = []
for i, mb in enumerate(missing_beats):
    desc_words = tokenize(mb["desc"]) | tokenize(mb["prompt"])
    prompt_words_list = [w for w in re.findall(r"[a-zA-Z0-9]+", mb["desc"].lower())]
    for j, f in enumerate(candidates):
        clean_name = f.stem.replace("…", "").replace("_2K", "").replace("_", " ")
        f_words = tokenize(clean_name)
        overlap = len(desc_words & f_words)
        score = overlap * 4
        # Bonus if filename words appear in first 10 words of prompt
        for w in f_words:
            if w in prompt_words_list[:12]:
                score += 6
        if score > 0:
            scores.append((score, i, j))

scores.sort(key=lambda x: x[0], reverse=True)
matched_beats = {}
used_files = set()

for score, b_idx, f_idx in scores:
    if b_idx in matched_beats or f_idx in used_files:
        continue
    matched_beats[b_idx] = (candidates[f_idx], score)
    used_files.add(f_idx)

print(f"\nGreedy match result: {len(matched_beats)} / {len(missing_beats)} beats matched.")

# Copy matched files to target_fname
copied = 0
for b_idx, mb in enumerate(missing_beats):
    if b_idx in matched_beats:
        f, sc = matched_beats[b_idx]
        target_path = frames_dir / mb["target_fname"]
        shutil.copy2(f, target_path)
        copied += 1
    else:
        print(f"❌ Missing match: {mb['target_fname']} | Desc: {mb['desc'][:60]}")

print(f"✅ Copied {copied} newly matched frames into {frames_dir}!")

# Final check
final_count = len(list(frames_dir.glob("seg_*.jpg")))
print(f"Current total named frames on disk: {final_count} / 180")
