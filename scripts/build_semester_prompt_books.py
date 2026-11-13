import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
COURSE_DIR = BASE_DIR / "output" / "course"
PROMPT_BOOKS_DIR = COURSE_DIR / "prompt_books"
PROMPT_BOOKS_DIR.mkdir(parents=True, exist_ok=True)

master_json = COURSE_DIR / "365_DAYS_COMPLETE_MICRO_BEATS_DIRECTORY.json"
with open(master_json, "r", encoding="utf-8") as f:
    master = json.load(f)

days = master["days"]

# Group by semester (each ~30 days)
semesters = [
    (1, 1, 30, "Foundations of Money, Cash Flow & Financial Statements"),
    (2, 31, 60, "Banking, Credit Architecture & Debt Optimization"),
    (3, 61, 90, "Fixed Income, Debt Markets & Sovereign Bonds"),
    (4, 91, 120, "Equity Markets & Fundamental Business Analysis"),
    (5, 121, 150, "Valuation Models (DCF, DDM, Multiples) & Margin of Safety"),
    (6, 151, 180, "Technical Analysis, Price Action & Market Microstructure"),
    (7, 181, 210, "Derivatives, Options Chain & Volatility Trading"),
    (8, 211, 240, "Mutual Funds, ETFs & Index Investing"),
    (9, 241, 270, "Real Estate, Alternate Assets & Commodity Supercycles"),
    (10, 271, 300, "Macroeconomics, Central Banking & Global Liquidity"),
    (11, 301, 330, "Tax Architecture, Estate Planning & Wealth Preservation"),
    (12, 331, 365, "Institutional Quantitative Systems & Algorithmic Portfolios")
]

for sem_num, start_d, end_d, sem_title in semesters:
    sem_days = [d for d in days if start_d <= d["day"] <= end_d]
    book_file = PROMPT_BOOKS_DIR / f"Semester_{sem_num:02d}_Days_{start_d:03d}_to_{end_d:03d}.md"
    
    with open(book_file, "w", encoding="utf-8") as f:
        f.write(f"# Semester {sem_num:02d}: {sem_title}\n")
        f.write(f"**Coverage**: Days {start_d:03d} to {end_d:03d} ({len(sem_days)} Videos) | **Cadence**: 1 Image Frame Per 4 Seconds\n\n")
        f.write("---\n\n")
        
        for d in sem_days:
            f.write(f"## Day {d['day']:03d}: {d['title']}\n")
            f.write(f"📁 **Folder**: `{d['folder_name']}` | **Total Frames Needed**: {d['total_beats']}\n\n")
            f.write("| Frame | Timestamp | Spoken Audio Excerpt | 3D Text | Prompt |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            for b in d["micro_beats"]:
                typo = " ".join(b["dynamic_3d_typography_overlay"]["lines"])
                f.write(f"| `{b['frame_filename']}` | `{b['timestamp']}` | {b['narration_audio_excerpt'][:35]}... | `{typo}` | {b['clean_35mm_photographic_prompt'][:65]}... |\n")
            
            f.write("\n### Full Image Prompts for Day {:03d}\n\n".format(d['day']))
            for b in d["micro_beats"]:
                f.write(f"#### Frame {b['beat']:02d} (`{b['frame_filename']}`) — [{b['timestamp']}]\n")
                f.write(f"- **Voice**: *\"{b['narration_audio_excerpt']}\"*\n")
                f.write(f"- **35mm Clean Photographic Plate (Zero Text)**:\n```\n{b['clean_35mm_photographic_prompt']}\n```\n")
                f.write(f"- **3D Kinetic Typography**: `{b['dynamic_3d_typography_overlay']['lines']}` ({b['dynamic_3d_typography_overlay']['color']})\n")
                f.write(f"- **Destination**: Drop image into `output/course/youtube_playlist_beginners_in_finance/{d['folder_name']}/frames/{b['frame_filename']}`\n\n")
            
            f.write("---\n\n")

print(f"✅ Generated all 12 Semester Prompt Books in {PROMPT_BOOKS_DIR}!")
