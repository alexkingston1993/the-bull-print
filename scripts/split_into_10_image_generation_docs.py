import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
COURSE_DIR = BASE_DIR / "output" / "course"
OUT_DIR = COURSE_DIR / "10_image_generation_documents"
OUT_DIR.mkdir(parents=True, exist_ok=True)

master_json = COURSE_DIR / "365_DAYS_COMPLETE_MICRO_BEATS_DIRECTORY.json"
with open(master_json, "r", encoding="utf-8") as f:
    master = json.load(f)

days = master["days"]
total_days = len(days)

# 10 roughly equal chunks
# Days 1 to 365 split into 10 parts:
# P1: 1-37 (37 days)
# P2: 38-74 (37 days)
# P3: 75-111 (37 days)
# P4: 112-147 (36 days)
# P5: 148-183 (36 days)
# P6: 184-219 (36 days)
# P7: 220-256 (37 days)
# P8: 257-292 (36 days)
# P9: 293-328 (36 days)
# P10: 329-365 (37 days)

chunks = [
    (1, 1, 37),
    (2, 38, 74),
    (3, 75, 111),
    (4, 112, 147),
    (5, 148, 183),
    (6, 184, 219),
    (7, 220, 256),
    (8, 257, 292),
    (9, 293, 328),
    (10, 329, 365)
]

for part_num, start_d, end_d in chunks:
    part_days = [d for d in days if start_d <= d["day"] <= end_d]
    doc_file = OUT_DIR / f"Document_{part_num:02d}_Days_{start_d:03d}_to_{end_d:03d}.md"
    
    total_beats_part = sum(d["total_beats"] for d in part_days)
    
    with open(doc_file, "w", encoding="utf-8") as f:
        f.write(f"# Image Generation Batch — Document {part_num:02d} / 10\n\n")
        f.write(f"**Coverage**: Days {start_d:03d} to {end_d:03d} ({len(part_days)} Videos)\n")
        f.write(f"**Total Frames to Render in this Document**: **{total_beats_part} Frames**\n")
        f.write(f"**Style Rule**: Clean 35mm photographic plates (Zero baked-in text, zero numbers, zero letters).\n\n")
        f.write("---\n\n")
        
        # Table of contents for this part
        f.write("## Index of Videos in this Document\n\n")
        for d in part_days:
            f.write(f"- [Day {d['day']:03d}: {d['title']}](#day-{d['day']:03d}-{d['title'].lower().replace(' ', '-').replace('(', '').replace(')', '').replace('&', '').replace(',', '').replace(':', '')}) ({d['total_beats']} frames) -> Destination: `{d['folder_name']}/frames/`\n")
        f.write("\n---\n\n")
        
        # Detailed prompts for each day
        for d in part_days:
            f.write(f"## Day {d['day']:03d}: {d['title']}\n")
            f.write(f"📁 **Destination Folder**: `output/course/youtube_playlist_beginners_in_finance/{d['folder_name']}/frames/`\n")
            f.write(f"🎯 **Total Beats**: {d['total_beats']} frames (1 every 4.0s)\n\n")
            
            for b in d["micro_beats"]:
                f.write(f"### [ ] Frame {b['beat']:02d} — `{b['frame_filename']}` [{b['timestamp']}]\n")
                f.write(f"- **Audio Narration Cue**: *\"{b['narration_audio_excerpt']}\"*\n")
                f.write(f"- **Clean 35mm Prompt (Copy & Paste)**:\n```\n{b['clean_35mm_photographic_prompt']}\n```\n")
                f.write(f"- **Save As**: `{b['frame_filename']}` into `{d['folder_name']}/frames/`\n\n")
            
            f.write("---\n\n")

print(f"🎉 Generated all 10 Image Generation Documents in: {OUT_DIR}")
