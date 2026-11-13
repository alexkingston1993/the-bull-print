#!/usr/bin/env python3
"""
scripts/generate_prototype_short.py
Generates a prototype YouTube Short using the Persistent Flow AI Master Canvas architecture.
Compatible with all macOS/Linux FFmpeg builds (uses standard overlay filter).
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.local_christopher_tts import synthesize_christopher_voice

OUTPUT_DIR = BASE_DIR / "output" / "prototype"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FLOW_AI_MASTER = BASE_DIR / "assets" / "flow_ai_masters" / "sebi_rule_exposed.jpg"
CHART_IMAGE = BASE_DIR / "assets" / "charts" / "nifty_order_flow_absorption.png"
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

NARRATION_TEXT = (
    "Think the new SEBI F&O rules protect you? Look at the mathematical proof. "
    "With lot sizes doubled to fifteen lakhs and weekly expiries slashed to one per exchange, "
    "retail margin requirements have skyrocketed. "
    "Over ninety percent of option buyers bleed out from theta decay before ever seeing a profit. "
    "Do not trade blind. Follow The Bull Print for daily institutional edge."
)

SUBTITLE_PHRASES = [
    ("THINK SEBI RULES PROTECT YOU?", 2.5, 5.5),
    ("LOOK AT THE MATHEMATICAL PROOF", 5.5, 8.5),
    ("LOT SIZES DOUBLED TO 15 LAKHS", 8.5, 12.0),
    ("WEEKLY EXPIRIES SLASHED TO 1", 12.0, 15.5),
    ("MARGIN REQUIREMENTS SKYROCKETED", 15.5, 19.5),
    ("OVER 90% BLEED FROM THETA DECAY", 19.5, 24.0),
    ("BEFORE EVER SEEING A PROFIT", 24.0, 27.0),
    ("FOLLOW THE BULL PRINT FOR DAILY EDGE", 27.0, 30.2),
]


def build_chart_card(out_png: Path):
    """Creates a sleek, glassmorphic HUD chart card to overlay on the Flow AI canvas."""
    card_w, card_h = 980, 560
    card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)

    # 1. Glass backdrop with glowing emerald border
    draw.rounded_rectangle([0, 0, card_w - 1, card_h - 1], radius=20, fill=(11, 15, 25, 220), outline=(16, 185, 129, 230), width=3)

    # 2. Header banner badge
    draw.rounded_rectangle([16, 16, 480, 60], radius=10, fill=(6, 78, 59, 240))
    font_header = ImageFont.truetype(FONT_PATH, 20)
    draw.text((32, 26), "SEBI F&O MATH · ORDER FLOW", font=font_header, fill=(52, 211, 153))

    # 3. Live indicator dot
    draw.ellipse([454, 33, 464, 43], fill=(52, 211, 153))

    # 4. Paste chart inside
    if CHART_IMAGE.exists():
        chart = Image.open(CHART_IMAGE).convert("RGBA")
        chart = chart.resize((card_w - 36, card_h - 90), Image.Resampling.LANCZOS)
        card.paste(chart, (18, 72), chart)

    card.save(out_png)
    print(f"📊 Chart HUD card created: {out_png.name}")


def build_subtitle_cards(phrases: list, out_dir: Path) -> list:
    """Generates punchy, high-contrast Hormozi subtitle cards."""
    font = ImageFont.truetype(FONT_PATH, 54)
    res = []
    for idx, (text, start_t, end_t) in enumerate(phrases):
        img = Image.new("RGBA", (1080, 180), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Measure text
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (1080 - tw) // 2
        y = (180 - th) // 2

        # Draw semi-transparent pill backdrop for readability
        pill_pad = 24
        draw.rounded_rectangle(
            [x - pill_pad, y - 10, x + tw + pill_pad, y + th + 16],
            radius=16,
            fill=(0, 0, 0, 180),
            outline=(16, 185, 129, 180),
            width=2,
        )

        # Bold yellow text with black stroke
        stroke_w = 4
        for dx in range(-stroke_w, stroke_w + 1):
            for dy in range(-stroke_w, stroke_w + 1):
                draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0))

        # Main glowing fill
        fill_color = (255, 235, 59) if (idx % 2 == 0) else (56, 189, 248)
        draw.text((x, y), text, font=font, fill=fill_color)

        p = out_dir / f"sub_{idx:02d}.png"
        img.save(p)
        res.append((p, start_t, end_t))
    return res


async def main():
    print("🎬 Generating Prototype Short with Persistent Flow AI Master Canvas...")

    mp3_path = OUTPUT_DIR / "prototype_audio.mp3"
    out_mp4 = OUTPUT_DIR / "prototype_flow_ai_short.mp4"
    chart_card_png = OUTPUT_DIR / "chart_card.png"

    # 1. Synthesize Audio
    if not mp3_path.exists():
        synthesize_christopher_voice(NARRATION_TEXT, mp3_path)

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(mp3_path)],
        capture_output=True, text=True, check=True
    )
    duration = float(probe.stdout.strip())
    print(f"🎙️ Audio Ready: {duration:.2f} seconds")

    # 2. Build Graphics
    build_chart_card(chart_card_png)
    subs = build_subtitle_cards(SUBTITLE_PHRASES, OUTPUT_DIR)

    # 3. Assemble FFmpeg filter graph
    # Inputs:
    # 0: Flow AI Master
    # 1: Audio mp3
    # 2: Chart HUD card
    # 3..N: Subtitle PNGs

    inputs = [
        "-loop", "1", "-i", str(FLOW_AI_MASTER),
        "-i", str(mp3_path),
        "-loop", "1", "-i", str(chart_card_png),
    ]
    for p, _, _ in subs:
        inputs.extend(["-loop", "1", "-i", str(p)])

    # Filter chain
    # Base: Flow AI Master scaled to 1080x1920
    filter_parts = [
        "[0:v]scale=1080:1920,setsar=1,"
        "zoompan=z='min(zoom+0.00015,1.03)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30[bg]"
    ]

    # Overlay chart card at y=780 (below the 3D skull and title, leaving top 40% pristine!)
    # Fade in chart from t=3.5s onwards
    filter_parts.append("[bg][2:v]overlay=50:780:enable='gte(t,3.5)'[with_chart]")

    current_layer = "[with_chart]"
    for idx, (_, st, et) in enumerate(subs):
        in_idx = idx + 3
        next_layer = f"[v_sub_{idx}]"
        filter_parts.append(
            f"{current_layer}[{in_idx}:v]overlay=0:1440:enable='between(t,{st:.2f},{et:.2f})'{next_layer}"
        )
        current_layer = next_layer

    # Add neon progress bar at bottom
    hud_bar = f"drawbox=x=0:y=1896:w='min(1080\\,(t/{duration:.2f})*1080)':h=8:color=0x10B981@0.95:t=fill"
    badge = "drawbox=x=40:y=40:w=360:h=46:color=0x064E3B@0.85:t=fill"

    final_filter = ";".join(filter_parts) + f";{current_layer}{hud_bar},{badge}[final_v]"

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", final_filter,
        "-map", "[final_v]", "-map", "1:a",
        "-c:v", "h264_videotoolbox" if sys.platform == "darwin" else "libx264",
        "-b:v", "6500k",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-t", f"{duration:.2f}",
        str(out_mp4)
    ]

    print("⚙️ Executing FFmpeg Render...")
    subprocess.run(cmd, check=True)
    print(f"✅ Prototype Short successfully rendered: {out_mp4}")

    # 4. Extract Key Frames to inspect
    sample_times = [1.0, 5.0, 15.0, 25.0]
    for st in sample_times:
        f_out = OUTPUT_DIR / f"frame_{int(st)}s.jpg"
        subprocess.run(["ffmpeg", "-y", "-ss", f"{st:.1f}", "-i", str(out_mp4), "-vframes", "1", "-q:v", "2", str(f_out)], capture_output=True, check=True)
        print(f"📸 Extracted frame at t={st:.1f}s -> {f_out.name}")

if __name__ == "__main__":
    asyncio.run(main())
