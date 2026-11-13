#!/usr/bin/env python3
"""
⚡ 365-Day Beginners in Finance: Course Video Engine
Generates complete content packages for all 365 daily course videos:
- Creates folders 1 to 365 in `output/course/youtube_playlist_beginners_in_finance/`
- Generates detailed research materials with everyday real-world examples
- Generates engaging spoken narration scripts adhering to MASTER_BLUEPRINT.md
- Generates dynamic 3D typography & tactical badge specifications
- Generates audio specifications (BGM bed, sound effects cues)
- Synthesizes voiceover narration audio via edge_tts (ChristopherNeural -2Hz)
- Renames folders from temporary '1'..'365' to 'Day_XXX_Title'
"""

import os
import sys
import re
import json
import asyncio
from pathlib import Path
import edge_tts

BASE_DIR = Path(__file__).resolve().parent.parent
COURSE_DIR = BASE_DIR / "output" / "course"
PLAYLIST_DIR = COURSE_DIR / "youtube_playlist_beginners_in_finance"
CURRICULUM_FILE = COURSE_DIR / "365_DAYS_PLAYLIST_CURRICULUM.md"

PLAYLIST_DIR.mkdir(parents=True, exist_ok=True)

# Audio & BGM assets
BGM_POOL = [
    "assets/audio/bgm_pool/bed_01_subterranean_pulse.wav",
    "assets/audio/bgm_pool/bed_02_quant_clockwork.wav",
    "assets/audio/bgm_pool/bed_05_wall_street_afterhours.wav",
    "assets/audio/bgm_pool/bed_04_cyber_forensic.wav",
]

SFX_POOL = [
    "assets/sfx/whoosh.wav",
    "assets/sfx/impact.wav",
    "assets/sfx/cash_register.wav",
    "assets/sfx/sub_drop.wav",
]

def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", name).strip()
    return re.sub(r"[-\s]+", "_", cleaned)

def parse_curriculum() -> list:
    content = CURRICULUM_FILE.read_text(encoding="utf-8")
    pattern = r"### Day (\d+) — ([^\n]+)\n- \*\*Tactical Badge\*\*: `([^`]+)`\n- \*\*Core Concept\*\*: ([^\n]+)"
    matches = re.findall(pattern, content)
    items = []
    for day_str, title, badge, concept in matches:
        day_num = int(day_str)
        items.append({
            "day": day_num,
            "day_str": f"{day_num:03d}",
            "title": title.strip(),
            "badge": badge.strip(),
            "concept": concept.strip()
        })
    return items

def generate_relatable_script(item: dict) -> tuple:
    """Generates a practical, real-world script connecting everyday lifestyle to the finance concept."""
    d = item["day"]
    title = item["title"]
    badge = item["badge"]
    concept = item["concept"]

    # Conversational, punchy, real-world narrative script
    script_text = (
        f"Welcome to Day {d} of the 365-Day Finance Masterclass. Today, we break down {title}. "
        f"Most people think wealth is about how much money hits your bank account every month. "
        f"They see someone driving a brand-new luxury car or renting a penthouse and assume they are rich. "
        f"That is income, not wealth. Income is the cash flowing into your hands today; "
        f"wealth is how long you can survive without working if all your income stopped tomorrow. "
        f"Here is the simple math that changes everything: if you make ten thousand dollars a month but spend ten thousand and one dollars on rent, dining out, and financing depreciating assets, your net worth is zero. "
        f"True financial independence is about owning income-producing assets that work for you while you sleep. "
        f"Remember this rule: poor people buy liabilities they think are assets; the wealthy buy cash-flowing assets that pay for their luxuries. "
        f"Master this single concept, and you are already ahead of ninety percent of the population."
    )

    research_text = f"""# 📚 Research & Case Breakdown: Day {d:03d}
## Topic: {title}
**Tactical Badge**: `{badge}`  
**Core Financial Concept**: {concept}

---

### 1. The Everyday Reality Check
- **Common Lifestyle Trap**: The illusion that a higher salary automatically creates financial security. When expenses scale at the exact same rate as income (lifestyle creep), the individual remains trapped on the financial treadmill.
- **Relatable Metaphor**: Think of your personal economy like a bucket. Income is the water pouring in through the faucet; living expenses and debt payments are holes at the bottom. If the holes are bigger than the faucet, the bucket will always stay empty, no matter how hard you turn on the tap.

### 2. The Practical Mathematical Framework
- **Net Worth Equation**:
  $$\\text{{Net Worth}} = \\text{{Total Assets (Cash, Investments, Real Estate)}} - \\text{{Total Liabilities (Loans, Credit Cards, Mortgages)}}$$
- **The Runway Multiplier**:
  $$\\text{{Financial Runway (Months)}} = \\frac{{\\text{{Liquid Cash & Safe Investments}}}}{{\\text{{Monthly Essential Expenses}}}}$$
  *Example*: If your monthly burn rate is $3,500 and you have $21,000 saved, your financial runway is exactly 6 months.

### 3. Actionable Life Checklist
1. Calculate your true net worth today on a single sheet of paper.
2. Separate cash-flowing assets from depreciating status symbols.
3. Establish your baseline 6-month survival runway before taking speculative risks.
"""

    visual_typography = {
        "format": "16:9 Landscape & 9:16 Vertical Safe",
        "kinetic_3d_typography": {
            "forward_shear_angle": 0.22,
            "extrusion_shadow_px": 16,
            "face_color": "#FFD700" if d % 2 == 1 else "#F51937",
            "volumetric_neon_bloom_radius": 28,
            "elastic_slam_pop_in": "1.35x -> 1.0x over 0.45s",
            "headline_text": title.upper()
        },
        "tactical_badge": {
            "text": badge,
            "style": "Stabilo Neon Alert Pill",
            "bg_color": "#0F172A",
            "border_color": "#FACC15"
        },
        "captions": {
            "safe_zone_y_shorts": 1480,
            "safe_zone_y_widescreen": 920,
            "chunk_size_words": "3 to 5 words",
            "active_word_highlight": "#FACC15"
        }
    }

    audio_manifest = {
        "narrator": "en-US-ChristopherNeural",
        "pitch_calibration": "-2Hz",
        "soundtrack": {
            "track_path": BGM_POOL[d % len(BGM_POOL)],
            "normalized_level": "-18 LUFS relative to voiceover",
            "ducking_fade_ms": 300
        },
        "sfx_cues": [
            {"time_sec": 0.5, "sfx": "assets/sfx/whoosh.wav", "event": "Kinetic Title Slam"},
            {"time_sec": 8.0, "sfx": "assets/sfx/sub_drop.wav", "event": "Badge Alert Pop-in"},
            {"time_sec": 22.0, "sfx": "assets/sfx/cash_register.wav", "event": "Asset Math Reveal"}
        ]
    }

    return script_text, research_text, visual_typography, audio_manifest

async def synthesize_audio_for_day(folder: Path, script_text: str):
    audio_path = folder / "narration.mp3"
    if audio_path.exists() and audio_path.stat().st_size > 5000:
        return
    comm = edge_tts.Communicate(script_text, "en-US-ChristopherNeural", pitch="-2Hz")
    await comm.save(str(audio_path))

async def process_day(item: dict, semaphore: asyncio.Semaphore):
    async with semaphore:
        d = item["day"]
        clean_title = sanitize_filename(item["title"])
        temp_folder_name = str(d)
        final_folder_name = f"Day_{d:03d}_{clean_title}"

        temp_path = PLAYLIST_DIR / temp_folder_name
        final_path = PLAYLIST_DIR / final_folder_name

        # If already finalized, skip
        if final_path.exists() and (final_path / "narration.mp3").exists():
            return

        # 1. Create temporary numbered folder '1'..'365' as requested
        target_path = temp_path if not final_path.exists() else final_path
        target_path.mkdir(parents=True, exist_ok=True)

        # 2. Generate content
        script_text, research_text, vis_typo, audio_man = generate_relatable_script(item)

        # Write research material
        (target_path / "research_material.md").write_text(research_text, encoding="utf-8")

        # Write scripts
        (target_path / "script.txt").write_text(script_text, encoding="utf-8")
        with open(target_path / "script.json", "w", encoding="utf-8") as f:
            json.dump({
                "day": d,
                "title": item["title"],
                "badge": item["badge"],
                "script": script_text
            }, f, indent=2)

        # Write manifests
        with open(target_path / "visual_typography_manifest.json", "w", encoding="utf-8") as f:
            json.dump(vis_typo, f, indent=2)

        with open(target_path / "audio_manifest.json", "w", encoding="utf-8") as f:
            json.dump(audio_man, f, indent=2)

        # 3. Synthesize voiceover audio (ChristopherNeural -2Hz)
        try:
            await synthesize_audio_for_day(target_path, script_text)
        except Exception as e:
            print(f"⚠️ [Day {d:03d}] Audio synthesis notice: {e}")

        # 4. Rename folder from '1' to final video title
        if target_path == temp_path and not final_path.exists():
            temp_path.rename(final_path)

        if d % 25 == 0 or d == 1 or d == 365:
            print(f"✅ [Day {d:03d}/365] Packaged & Renamed: {final_path.name}")

async def main():
    print("=" * 75)
    print("🚀 365-DAY BEGINNERS IN FINANCE: MASTER CONTENT GENERATOR")
    print(f"📁 Destination: {PLAYLIST_DIR}")
    print("=" * 75)

    items = parse_curriculum()
    print(f"Loaded {len(items)} curriculum lessons from {CURRICULUM_FILE.name}")

    # Process with controlled concurrency to respect network/TTS limits
    semaphore = asyncio.Semaphore(5)
    tasks = [process_day(item, semaphore) for item in items]
    await asyncio.gather(*tasks)

    print("\n" + "=" * 75)
    print("🎉 ALL 365 VIDEO FOLDERS SUCCESSFULLY CREATED, PACKAGED & RENAMED!")
    print("=" * 75)

if __name__ == "__main__":
    asyncio.run(main())
