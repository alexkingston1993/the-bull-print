#!/usr/bin/env python3
"""
Export complete micro-beat visual prompt specifications for:
1. Doc 02: Missing 108 Beats (Segments 15 to 36)
2. Doc 03: Missing 156 Beats (Segments 05 Beat 5 to Segment 36 Beat 5)
Strictly adheres to:
- 16:9 Widescreen ratio
- Mass-audience language (Zero Dalal Street, Zero Smart Money)
- Clean plate visual prompts (Zero text, numbers, or watermarks)
"""

import sys
import importlib.util
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def export_doc02():
    p = BASE_DIR / "output" / "fii_exodus_documentary" / "chapters_script.py"
    spec = importlib.util.spec_from_file_location("mod", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)

    frames_dir = BASE_DIR / "output" / "fii_exodus_documentary" / "frames"
    existing = set(x.name for x in frames_dir.glob("*.jpg"))

    lines = [
        "# 🎬 DOC 02: THE ₹14,900 CRORE U-TURN (MISSING 108 BESPOKE BEATS)\n",
        "**Target Video**: Doc 02: *The ₹14,900 Crore U-Turn: How Foreign Investors Broke and Rescued the Indian Market*\n",
        "**Aspect Ratio**: 16:9 Widescreen\n",
        "**Aesthetic**: Cinematic 35mm film photography, documentary realism, deep chiaroscuro shadows, zero typography/text/watermarks.\n",
        "**Language Standard**: Mass-Audience Sanitized (Zero 'Dalal Street', Zero 'Smart Money').\n\n",
        "---\n\n"
    ]

    missing_count = 0
    for s in m.SEGMENTS:
        seg_beats = []
        for b in s["beats"]:
            fname = f"seg_{s['id']:02d}_beat_{b['beat_num']}.jpg"
            if fname not in existing:
                p_text = (
                    b["prompt"]
                    .replace("Dalal Street", "the Mumbai financial district")
                    .replace("dalal street", "the Mumbai financial district")
                    .replace("Smart Money", "big institutional buyers")
                    .replace("smart money", "big institutional buyers")
                )
                anchor = (
                    b["anchor_text"]
                    .replace("DALAL ST", "INDIAN MKT")
                    .replace("DALAL STREET", "INDIAN MKT")
                    .replace("SMART MONEY", "BIG FUNDS")
                )
                badge = (
                    b["badge_text"]
                    .replace("DALAL ST", "INDIAN MKT")
                    .replace("DALAL STREET", "INDIAN MKT")
                    .replace("SMART MONEY", "BIG FUNDS")
                )
                seg_beats.append({
                    "beat_num": b["beat_num"],
                    "fname": fname,
                    "anchor": anchor,
                    "badge": badge,
                    "desc": b["visual_description"],
                    "prompt": p_text
                })
                missing_count += 1

        if seg_beats:
            lines.append(f"## Segment {s['id']:02d}: {s['title']}\n\n")
            for item in seg_beats:
                lines.append(f"### Beat {item['beat_num']} — `{item['fname']}`\n")
                lines.append(f"- **Overlay Anchor**: `{item['anchor']}` | **Badge**: `[{item['badge']}]`\n")
                lines.append(f"- **Visual Concept**: {item['desc']}\n")
                lines.append(f"- **Flow AI Prompt**:\n```text\n{item['prompt']}\n```\n\n")

    out_file = BASE_DIR / "output" / "fii_exodus_documentary" / "DOC02_MISSING_108_BEATS.md"
    out_file.write_text("".join(lines), encoding="utf-8")
    print(f"✅ Doc 02 missing beats exported ({missing_count} beats): {out_file}")


def export_doc03():
    p = BASE_DIR / "output" / "nuclear_ai_documentary" / "chapters_script.py"
    spec = importlib.util.spec_from_file_location("mod", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)

    frames_dir = BASE_DIR / "output" / "nuclear_ai_documentary" / "frames"
    existing = set(x.name for x in frames_dir.glob("seg_*.jpg"))

    lines = [
        "# 🎬 DOC 03: BIG TECH'S NUCLEAR SECRET (ALL 180 BEATS SPECIFICATION)\n",
        "**Target Video**: Doc 03: *Big Tech's Nuclear Secret: The Race for Atomic Megawatts*\n",
        "**Aspect Ratio**: 16:9 Widescreen\n",
        "**Aesthetic**: Cinematic 35mm film photograph, documentary realism, eerie nuclear Cherenkov blue & amber datacenters, zero typography/text/watermarks.\n\n",
        "---\n\n"
    ]

    missing_count = 0
    for s in m.SEGMENTS:
        lines.append(f"## Segment {s['id']:02d}: {s['title']}\n\n")
        for b in s["beats"]:
            fname = f"seg_{s['id']:02d}_beat_{b['beat_num']}.jpg"
            status = "✅ (Already Exists)" if fname in existing else "⏳ (NEEDS GENERATION)"
            if fname not in existing:
                missing_count += 1
            lines.append(f"### Beat {b['beat_num']} — `{fname}` — {status}\n")
            lines.append(f"- **Overlay Anchor**: `{b['anchor_text']}` | **Badge**: `[{b['badge_text']}]`\n")
            lines.append(f"- **Visual Concept**: {b['visual_description']}\n")
            lines.append(f"- **Flow AI Prompt**:\n```text\n{b['prompt']}\n```\n\n")

    out_file = BASE_DIR / "output" / "nuclear_ai_documentary" / "DOC03_ALL_180_BEATS.md"
    out_file.write_text("".join(lines), encoding="utf-8")
    print(f"✅ Doc 03 all beats exported ({missing_count} missing beats): {out_file}")


def export_doc03_missing_112():
    p = BASE_DIR / "output" / "nuclear_ai_documentary" / "chapters_script.py"
    spec = importlib.util.spec_from_file_location("mod", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)

    lines = [
        "# 🎬 DOC 03: BIG TECH'S NUCLEAR SECRET (MISSING 112 BESPOKE BEATS)\n",
        "**Target Video**: Doc 03: *Big Tech's Nuclear Secret: The Race for Atomic Megawatts*\n",
        "**Aspect Ratio**: 16:9 Widescreen\n",
        "**Aesthetic**: Cinematic 35mm film photograph, documentary realism, eerie nuclear Cherenkov blue & amber datacenters, zero typography/text/watermarks.\n",
        "**Total Missing**: 112 Frames (Segment 14 Beat 4 through Segment 36 Beat 5)\n\n",
        "---\n\n"
    ]

    count = 0
    for s in m.SEGMENTS:
        seg_beats = []
        for b in s["beats"]:
            b_num_global = (s["id"] - 1) * 5 + b["beat_num"]
            if b_num_global > 68:
                fname = f"seg_{s['id']:02d}_beat_{b['beat_num']}.jpg"
                seg_beats.append({
                    "beat_num": b["beat_num"],
                    "fname": fname,
                    "anchor": b["anchor_text"],
                    "badge": b["badge_text"],
                    "desc": b["visual_description"],
                    "prompt": b["prompt"]
                })
                count += 1
        if seg_beats:
            lines.append(f"## Segment {s['id']:02d}: {s['title']}\n\n")
            for item in seg_beats:
                lines.append(f"### Beat {item['beat_num']} — `{item['fname']}`\n")
                lines.append(f"- **Overlay Anchor**: `{item['anchor']}` | **Badge**: `[{item['badge']}]`\n")
                lines.append(f"- **Visual Concept**: {item['desc']}\n")
                lines.append(f"- **Flow AI Prompt**:\n```text\n{item['prompt']}\n```\n\n")

    out_file = BASE_DIR / "output" / "nuclear_ai_documentary" / "DOC03_MISSING_112_BEATS.md"
    out_file.write_text("".join(lines), encoding="utf-8")
    print(f"✅ Doc 03 missing 112 beats exported ({count} beats): {out_file}")


if __name__ == "__main__":
    export_doc02()
    export_doc03()
    export_doc03_missing_112()

