import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
COURSE_DIR = BASE_DIR / "output" / "course" / "youtube_playlist_beginners_in_finance"

folders = sorted([f for f in COURSE_DIR.iterdir() if f.is_dir() and f.name.startswith("Day_")], key=lambda x: x.name)
print(f"Scanning {len(folders)} day folders...")

complete_365_database = []
total_beats_count = 0

for folder in folders:
    beat_json = folder / "BEAT_PROMPTS_4S.json"
    if not beat_json.exists():
        continue
    with open(beat_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    total_beats_count += len(data.get("beats", []))
    complete_365_database.append({
        "day": data.get("day"),
        "title": data.get("title"),
        "folder_name": folder.name,
        "cadence": data.get("cadence", "1 frame every 4.0 seconds"),
        "total_beats": len(data.get("beats", [])),
        "micro_beats": data.get("beats", [])
    })

master_output = BASE_DIR / "output" / "course" / "365_DAYS_COMPLETE_MICRO_BEATS_DIRECTORY.json"
with open(master_output, "w", encoding="utf-8") as f:
    json.dump({
        "course_name": "The Bull Print: 365-Day Financial Freedom Masterclass",
        "total_days": len(complete_365_database),
        "total_micro_beats_all_videos": total_beats_count,
        "cadence": "1 image frame per 4 seconds",
        "days": complete_365_database
    }, f, indent=2)

print(f"✅ COMPLETE! Stored all {len(complete_365_database)} days and {total_beats_count} micro-beats into:")
print(f"👉 {master_output} (Size: {master_output.stat().st_size / (1024*1024):.2f} MB)")
