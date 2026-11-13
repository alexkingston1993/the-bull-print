#!/usr/bin/env python3
"""
365-Day Finance Masterclass: Micro-Beat Generator (1 Image Frame Per 4 Seconds)
Generates:
1. BEAT_PROMPTS_4S.json in each day's folder (Days 001 to 365)
2. MICRO_BEAT_BREAKDOWN.md in each day's folder
3. Master directory: output/course/365_DAYS_COMPLETE_MICRO_BEATS_DIRECTORY.json
"""

import os
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
COURSE_DIR = BASE_DIR / "output" / "course" / "youtube_playlist_beginners_in_finance"

THEMATIC_PROMPT_STYLES = [
    "Cinematic 35mm film photograph, dramatic low-angle shot, dark corporate architectural interior, moody chiaroscuro lighting, anamorphic lens flare, Kodak Portra 400 color grading, zero text, zero numbers, clean photographic plate.",
    "Macro 35mm photograph of crisp textured paper currency and heavy gold bullion bars stacked on dark slate marble, dramatic rim lighting, soft focus depth of field, photorealistic, zero text, clean plate.",
    "Atmospheric cinematic shot of a modern glass skyscraper looking over a bustling metropolitan financial district at dusk, illuminated office windows, deep blue and amber tones, Hasselblad photography, clean plate.",
    "Cinematic close-up of a sleek black titanium luxury sports car parked in rain, reflection of city streetlights on wet asphalt, cinematic bokeh, hyper-detailed, zero text, zero letters, clean plate.",
    "Dramatic high-contrast photograph of an institutional trading desk with glowing ambient monitors reflecting off polished dark oak wood, Bloomberg terminal glow, cinematic shadows, clean plate.",
    "Macro photograph of an antique brass balance scale weighing a heavy solid gold coin against a stack of depreciating paper IOUs, dramatic studio spotlight, dark background, clean plate.",
    "Cinematic 35mm photograph of an hourglass with glowing luminous golden sand flowing steadily through narrow glass neck, dark moody atmosphere, shallow depth of field, clean plate.",
    "Dramatic cinematic wide shot of a solitary disciplined investor standing before towering steel bank vault doors swinging open, beams of volumetric golden light spilling out, clean plate."
]

TYPOGRAPHY_PALETTES = [
    {"col": "#FFD700", "bloom": "rgba(255,215,0,0.4)", "badge_bg": "#FFD700", "badge_text": "#000000"},
    {"col": "#F51937", "bloom": "rgba(245,25,55,0.4)", "badge_bg": "#F51937", "badge_text": "#FFFFFF"},
    {"col": "#00875A", "bloom": "rgba(0,135,90,0.4)", "badge_bg": "#00875A", "badge_text": "#FFFFFF"},
    {"col": "#00E5FF", "bloom": "rgba(0,229,255,0.4)", "badge_bg": "#00E5FF", "badge_text": "#000000"},
    {"col": "#F59E0B", "bloom": "rgba(245,158,11,0.4)", "badge_bg": "#F59E0B", "badge_text": "#000000"}
]

def extract_core_keywords(chunk, title):
    # Select 2-4 punchy high-impact words for 3D kinetic typography
    clean = re.sub(r'[^\w\s]', '', chunk.upper())
    words = [w for w in clean.split() if len(w) > 3 and w not in ["THIS", "THAT", "WITH", "HAVE", "FROM", "THEY", "YOUR", "WILL", "ABOUT", "WELCOME", "MASTERCLASS"]]
    if len(words) >= 2:
        return words[:2]
    title_words = [w for w in re.sub(r'[^\w\s]', '', title.upper()).split() if len(w) > 3]
    return title_words[:2] if len(title_words) >= 2 else ["QUANT", "ALPHA"]

def generate_micro_beats_for_day(day_folder):
    script_file = day_folder / "script.json"
    if not script_file.exists():
        return None

    with open(script_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    day_num = data.get("day", 1)
    title = data.get("title", day_folder.name)
    script = data.get("script", "")
    badge = data.get("badge", "[QUANT WEALTH]")

    words = script.split()
    total_words = len(words)
    words_per_beat = max(8, round(total_words / 15))

    beats = []
    chunk_start = 0
    beat_num = 1

    while chunk_start < total_words:
        chunk_words = words[chunk_start:chunk_start + words_per_beat]
        chunk_text = " ".join(chunk_words)
        
        start_sec = (beat_num - 1) * 4
        end_sec = beat_num * 4
        
        palette = TYPOGRAPHY_PALETTES[(beat_num - 1) % len(TYPOGRAPHY_PALETTES)]
        photo_prompt = THEMATIC_PROMPT_STYLES[(beat_num - 1) % len(THEMATIC_PROMPT_STYLES)]
        typo_words = extract_core_keywords(chunk_text, title)

        # Context-specific prompt customization
        custom_prompt = (
            f"Cinematic 35mm photograph illustrating {title.lower()}, focused on {chunk_text[:60].lower()}... "
            f"{photo_prompt} STRICT PROHIBITION: Zero text, zero letters, zero numbers, zero typography, clean 35mm photographic plate."
        )

        beat_data = {
            "beat": beat_num,
            "frame_filename": f"frame_{beat_num:02d}.jpg",
            "timestamp": f"{start_sec//60:02d}:{start_sec%60:02d} - {end_sec//60:02d}:{end_sec%60:02d}",
            "narration_audio_excerpt": chunk_text,
            "clean_35mm_photographic_prompt": custom_prompt,
            "dynamic_3d_typography_overlay": {
                "lines": typo_words,
                "color": palette["col"],
                "volumetric_bloom": palette["bloom"],
                "forward_shear_angle": 0.22,
                "extrusion_depth_px": 16,
                "position": "center"
            },
            "stabilo_tactical_badge": {
                "text": f"DAY {day_num:03d} • BEAT {beat_num:02d} • {badge.replace('[','').replace(']','')}",
                "bg_color": palette["badge_bg"],
                "text_color": palette["badge_text"]
            }
        }
        beats.append(beat_data)
        
        chunk_start += words_per_beat
        beat_num += 1

    # 1. Save BEAT_PROMPTS_4S.json
    beats_json_path = day_folder / "BEAT_PROMPTS_4S.json"
    with open(beats_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "day": day_num,
            "title": title,
            "total_beats": len(beats),
            "cadence": "1 frame every 4.0 seconds",
            "beats": beats
        }, f, indent=2)

    # 2. Save MICRO_BEAT_BREAKDOWN.md
    md_path = day_folder / "MICRO_BEAT_BREAKDOWN.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Day {day_num:03d}: {title}\n")
        f.write(f"**Cadence**: 1 Image Frame Per 4 Seconds | **Total Beats**: {len(beats)} Frames\n\n")
        f.write("## Micro-Beat Execution Table\n\n")
        f.write("| Beat | Frame File | Timestamp | Narration Audio Excerpt | 3D Kinetic Words | Badge Tag |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for b in beats:
            words_joined = " ".join(b["dynamic_3d_typography_overlay"]["lines"])
            f.write(f"| Beat {b['beat']:02d} | `{b['frame_filename']}` | `{b['timestamp']}` | {b['narration_audio_excerpt'][:45]}... | **{words_joined}** | `{b['stabilo_tactical_badge']['text'][:25]}` |\n")

        f.write("\n\n## Complete Micro-Beat AI Image Prompts (Copy & Paste for Generation)\n\n")
        for b in beats:
            f.write(f"### Frame {b['beat']:02d} (`{b['frame_filename']}`) — [{b['timestamp']}]\n")
            f.write(f"- **Audio Narration**: *\"{b['narration_audio_excerpt']}\"*\n")
            f.write(f"- **35mm Clean Image Prompt**:\n```\n{b['clean_35mm_photographic_prompt']}\n```\n")
            f.write(f"- **3D Typography Layer**: `{b['dynamic_3d_typography_overlay']['lines']}` (Color: `{b['dynamic_3d_typography_overlay']['color']}`)\n")
            f.write(f"- **Target Destination**: Drop rendered image into `{day_folder.name}/frames/{b['frame_filename']}`\n\n")

    return {
        "day": day_num,
        "title": title,
        "folder": day_folder.name,
        "total_beats": len(beats),
        "beats": beats
    }

def process_all_365_days():
    folders = sorted([f for f in COURSE_DIR.iterdir() if f.is_dir() and f.name.startswith("Day_")], key=lambda x: x.name)
    print(f"Found {len(folders)} day folders to process...")

    master_directory = []
    for idx, folder in enumerate(folders, 1):
        res = generate_micro_beats_for_day(folder)
        if res:
            master_directory.append({
                "day": res["day"],
                "title": res["title"],
                "folder": res["folder"],
                "total_beats": res["total_beats"],
                "sample_beat_01_prompt": res["beats"][0]["clean_35mm_photographic_prompt"]
            })
        if idx % 50 == 0 or idx == len(folders):
            print(f"Processed {idx}/{len(folders)} days...")

    # Save Master Directory
    master_path = BASE_DIR / "output" / "course" / "365_DAYS_COMPLETE_MICRO_BEATS_DIRECTORY.json"
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master_directory, f, indent=2)

    print(f"\n🎉 Successfully generated micro-beat manifests for all {len(master_directory)} days!")
    print(f"Master directory saved to: {master_path}")

if __name__ == "__main__":
    process_all_365_days()
