#!/usr/bin/env python3
"""
Viral YouTube Short: The $3 Billion/Day US Debt Spiral
Format: Vertical 9:16 (1080x1920)
Style: MagnatesMedia Visual & Kinetic 3D Typography Master

Features:
1. 100% Full Bleed Vertical 1080x1920 coverage with clean 35mm background plates.
2. Giant 3D Extruded Perspective Typography (Italic slant, multi-depth extrusion, crimson/gold).
3. Volumetric Neon Bloom / Atmospheric Aura radiating outward behind text.
4. Elastic Kinetic Slam Pop-In physics (1.40x -> 1.0x bounce) + camera drift / slow push-in.
5. Dynamic Neon Highlighter Badges (Stabilo-style marker box wiping over key facts).
6. Word-Level Animated Mobile Captions in the safe lower-third (Y = 1480).
7. 44.1kHz Stereo Christopher Narration + Ambient Tension Score Mux.
"""

import math
import os
import re
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path(__file__).resolve().parent.parent
BRAIN_DIR = Path("/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364")
AUDIO_FILE = BASE_DIR / "output" / "shorts" / "us_debt_master_audio.wav"
OUTPUT_DIR = BASE_DIR / "output" / "shorts"
OUTPUT_VIDEO = OUTPUT_DIR / "us_debt_spiral_magnates_short.mp4"
ARTIFACT_VIDEO = BRAIN_DIR / "us_debt_spiral_magnates_short.mp4"

CUTS = [
    {
        "id": 1,
        "start": 0.00,
        "end": 7.10,
        "plate": BRAIN_DIR / "us_debt_short_cut01_1794029669413.jpg",
        "lines": ["$3 BILLION", "PER DAY"],
        "badge": "US TREASURY REPORT",
        "badge_color": (255, 230, 0),    # Neon Yellow Marker
        "badge_text_col": (10, 10, 10),
        "text_color": (245, 25, 55),      # Crimson Red
        "bloom_color": (255, 30, 60),
        "pos": (90, 260),
        "font_size": 140,
    },
    {
        "id": 2,
        "start": 7.10,
        "end": 14.05,
        "plate": BRAIN_DIR / "us_debt_short_cut02_1794029763996.jpg",
        "lines": ["MORE THAN", "THE MILITARY"],
        "badge": "INTEREST: $1.05 TRILLION",
        "badge_color": (245, 30, 60),     # Glowing Red Marker
        "badge_text_col": (255, 255, 255),
        "text_color": (245, 30, 60),
        "bloom_color": (255, 40, 70),
        "pos": (70, 240),
        "font_size": 135,
    },
    {
        "id": 3,
        "start": 14.05,
        "end": 22.30,
        "plate": BRAIN_DIR / "us_debt_short_cut03_1794029799329.jpg",
        "lines": ["1.3 MILLION", "TROOPS"],
        "badge": "DEFENSE OUTSPENT BY DEBT",
        "badge_color": (255, 215, 0),    # Electric Gold Marker
        "badge_text_col": (10, 10, 10),
        "text_color": (255, 215, 0),
        "bloom_color": (255, 190, 30),
        "pos": (80, 240),
        "font_size": 140,
    },
    {
        "id": 4,
        "start": 22.30,
        "end": 29.58,
        "plate": BRAIN_DIR / "us_debt_short_cut04_1794029845830.jpg",
        "lines": ["PRINTING MONEY", "TO PAY DEBT"],
        "badge": "THE REFINANCING TRAP",
        "badge_color": (255, 230, 0),    # Neon Yellow
        "badge_text_col": (10, 10, 10),
        "text_color": (255, 60, 25),      # Fiery Amber Red
        "bloom_color": (255, 80, 30),
        "pos": (60, 250),
        "font_size": 125,
    },
    {
        "id": 5,
        "start": 29.58,
        "end": 33.95,
        "plate": BRAIN_DIR / "us_debt_short_cut05_1794029882087.jpg",
        "lines": ["BORROWING TO", "PAY BORROWING"],
        "badge": "THE COMPOUND TRAP",
        "badge_color": (245, 30, 60),
        "badge_text_col": (255, 255, 255),
        "text_color": (245, 25, 55),
        "bloom_color": (255, 35, 65),
        "pos": (70, 240),
        "font_size": 130,
    },
    {
        "id": 6,
        "start": 33.95,
        "end": 41.04,
        "plate": BRAIN_DIR / "us_debt_short_cut06_1794029924469.jpg",
        "lines": ["THE GREATEST", "PONZI SCHEME"],
        "badge": "YOUR DOLLARS FOOT THE BILL",
        "badge_color": (255, 215, 0),
        "badge_text_col": (10, 10, 10),
        "text_color": (255, 215, 0),     # Brilliant Gold
        "bloom_color": (255, 195, 30),
        "pos": (70, 240),
        "font_size": 130,
    },
]

# Spoken Sentences partitioned into mobile caption chunks (3-5 words each)
# Each chunk has start_t, end_t, words_list
CAPTION_CHUNKS = [
    # Sentence 1 (0.1 - 7.1s)
    (0.10, 2.40, ["At", "this", "exact", "second,"]),
    (2.40, 4.60, ["the", "United", "States", "is", "paying"]),
    (4.60, 7.10, ["three", "billion", "dollars", "every", "day..."]),
    # Sentence 2 (7.1 - 14.05s)
    (7.10, 9.40, ["That", "means", "servicing", "debt"]),
    (9.40, 11.80, ["now", "officially", "costs", "more"]),
    (11.80, 14.05, ["than", "the", "entire", "U.S.", "military."]),
    # Sentence 3 (14.05 - 22.3s)
    (14.05, 16.50, ["Every", "aircraft", "carrier,"]),
    (16.50, 19.20, ["every", "jet,", "and", "all", "troops"]),
    (19.20, 22.30, ["cost", "less", "than", "the", "interest."]),
    # Sentence 4 (22.3 - 29.58s)
    (22.30, 25.10, ["And", "here", "is", "the", "catch."]),
    (25.10, 27.40, ["To", "pay", "that", "interest,"]),
    (27.40, 29.58, ["they", "issue", "brand", "new", "debt."]),
    # Sentence 5 (29.58 - 33.95s)
    (29.58, 31.80, ["Borrowing", "money", "to", "pay"]),
    (31.80, 33.95, ["the", "interest", "already", "owed."]),
    # Sentence 6 (33.95 - 41.04s)
    (33.95, 36.80, ["The", "largest", "Ponzi", "scheme"]),
    (36.80, 38.90, ["in", "human", "history."]),
    (38.90, 41.04, ["And", "your", "dollars", "foot", "the", "bill."])
]

def load_and_prep_plate(path, w=1080, h=1920):
    im = Image.open(path).convert("RGB")
    scale = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    left = (im.width - w) // 2
    top = (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))

def render_viral_short():
    W, H = 1080, 1920
    fps = 30
    total_duration = 41.04
    total_frames = int(total_duration * fps)

    font_impact = "/System/Library/Fonts/Supplemental/Impact.ttf"

    print("⏳ Preloading 6 vertical 9:16 background plates...")
    plates = {}
    for cut in CUTS:
        plates[cut["id"]] = load_and_prep_plate(cut["plate"], W, H)

    raw_video = OUTPUT_DIR / "temp_us_debt_short.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264", "-preset", "medium", "-crf", "17",
        "-pix_fmt", "yuv420p",
        str(raw_video)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"🎬 Rendering {total_frames} frames ({total_duration:.1f}s) of Vertical 9:16 Viral Short...")

    for f_idx in range(total_frames):
        t = f_idx / fps

        # Find current cut
        curr_cut = CUTS[-1]
        for c in CUTS:
            if c["start"] <= t < c["end"]:
                curr_cut = c
                break

        cut_t = t - curr_cut["start"]
        cut_duration = curr_cut["end"] - curr_cut["start"]
        cut_progress = cut_t / cut_duration

        # 1. Camera Slow Dolly / Zoom (1.00 -> 1.05)
        zoom = 1.0 + 0.05 * cut_progress
        base_im = plates[curr_cut["id"]]
        zw, zh = int(W * zoom), int(H * zoom)
        zoomed = base_im.resize((zw, zh), Image.Resampling.BILINEAR)
        zx = (zw - W) // 2
        zy = (zh - H) // 2
        frame_canvas = zoomed.crop((zx, zy, zx + W, zy + H)).convert("RGBA")

        # 2. Kinetic 3D Slam Physics for Text
        # Fast slam pop-in (0.28s) with elastic rebound overshoot
        slam_duration = 0.28
        if cut_t < slam_duration:
            p = cut_t / slam_duration
            scale_anim = 1.0 + 0.40 * ((1.0 - p) ** 2) * math.cos(p * math.pi * 2.5)
            alpha_anim = min(255, int(255 * (p * 2.0)))
            shake_y = int(6.0 * (1.0 - p) * math.sin(p * math.pi * 4))
        else:
            p_hold = cut_t - slam_duration
            scale_anim = 1.0 + 0.015 * cut_progress
            alpha_anim = 255
            shake_y = int(2.5 * math.sin(p_hold * 2.2))

        # 3. Render 3D Extruded Slanted Text & Highlighter Marker
        text_w, text_h = 1000, 650
        text_layer = Image.new("RGBA", (text_w, text_h), (0, 0, 0, 0))
        draw_t = ImageDraw.Draw(text_layer)

        f_size = int(curr_cut["font_size"] * scale_anim)
        f_hero = ImageFont.truetype(font_impact, f_size)
        f_badge = ImageFont.truetype(font_impact, int(48 * scale_anim))

        y_offset = 20 + shake_y
        line_spacing = int(f_size * 0.96)
        col_face = curr_cut["text_color"]
        col_bloom = curr_cut["bloom_color"]

        for line in curr_cut["lines"]:
            # Multi-pass 3D Extrusion Shadow (16px down-right)
            for d in range(16, 0, -2):
                shade = int(70 * (1.0 - d / 16.0))
                draw_t.text((25 + d, y_offset + d), line, font=f_hero, fill=(shade, 0, 0, alpha_anim), stroke_width=7, stroke_fill=(0, 0, 0, alpha_anim))
            # Text Front Face
            draw_t.text((25, y_offset), line, font=f_hero, fill=(col_face[0], col_face[1], col_face[2], alpha_anim), stroke_width=5, stroke_fill=(15, 0, 5, alpha_anim))
            y_offset += line_spacing

        # Neon Highlighter Marker Badge
        badge_text = curr_cut["badge"]
        b_len = int(draw_t.textlength(badge_text, font=f_badge))
        b_pad_x = 24
        b_h = int(64 * scale_anim)
        b_w = b_len + (b_pad_x * 2)
        b_y = y_offset + 14

        # Highlighter wipe effect (left to right in 0.22s)
        if cut_t < 0.20:
            wipe_p = 0.0
        elif cut_t < 0.44:
            wipe_p = (cut_t - 0.20) / 0.24
        else:
            wipe_p = 1.0

        if wipe_p > 0.05:
            active_bw = int(b_w * wipe_p)
            bg_col = curr_cut["badge_color"]
            draw_t.rectangle([25, b_y, 25 + active_bw, b_y + b_h], fill=(bg_col[0], bg_col[1], bg_col[2], int(alpha_anim * 0.94)))
            if wipe_p > 0.4:
                b_text_col = curr_cut["badge_text_col"]
                draw_t.text((25 + b_pad_x, b_y + 8), badge_text, font=f_badge, fill=(b_text_col[0], b_text_col[1], b_text_col[2], alpha_anim))

        # Apply Italic Slant / Shear (forward slant = 0.22)
        shear = 0.22
        m = [1, -shear, 0, 0, 1, 0]
        slanted_text = text_layer.transform((text_w + 140, text_h), Image.Transform.AFFINE, m, resample=Image.Resampling.BILINEAR)

        # Volumetric Neon Bloom
        alpha_channel = slanted_text.split()[3]
        bloom_mask = alpha_channel.filter(ImageFilter.GaussianBlur(32))
        bloom_layer = Image.new("RGBA", slanted_text.size, (col_bloom[0], col_bloom[1], col_bloom[2], 0))
        bloom_layer.putalpha(bloom_mask)

        # Composite Bloom + Text onto frame
        tx, ty = curr_cut["pos"]
        frame_canvas.alpha_composite(bloom_layer, (tx, ty))
        frame_canvas.alpha_composite(slanted_text, (tx, ty))

        # 4. Word-Level Animated Mobile Captions (Lower-Third Safe Area: Y = 1480)
        active_chunk = None
        for c_start, c_end, words in CAPTION_CHUNKS:
            if c_start <= t <= c_end + 0.15:
                active_chunk = (c_start, c_end, words)
                break

        draw_f = ImageDraw.Draw(frame_canvas)

        if active_chunk:
            c_start, c_end, words = active_chunk
            n_words = len(words)
            c_dur = c_end - c_start
            w_idx = int(((t - c_start) / max(0.01, c_dur)) * n_words)
            w_idx = max(0, min(n_words - 1, w_idx))

            font_cap = ImageFont.truetype(font_impact, 54)
            word_widths = [draw_f.textlength(w, font=font_cap) for w in words]
            space_w = draw_f.textlength(" ", font=font_cap)
            total_cap_w = sum(word_widths) + space_w * (n_words - 1)

            cap_x = (W - total_cap_w) // 2
            cap_y = 1480

            # Frosted glass mobile pill
            pill_pad_x = 28
            pill_pad_y = 12
            draw_f.rounded_rectangle(
                [cap_x - pill_pad_x, cap_y - pill_pad_y, cap_x + total_cap_w + pill_pad_x, cap_y + 64 + pill_pad_y],
                radius=20,
                fill=(10, 10, 15, 215),
                outline=(245, 158, 11, 180) if (w_idx % 2 == 0) else (239, 68, 68, 180),
                width=3
            )

            # Draw words with dynamic punchy highlight
            curr_x = cap_x
            for idx, w in enumerate(words):
                if idx == w_idx:
                    # Active Word: Glowing Gold with Crimson stroke
                    draw_f.text((curr_x + 1, cap_y + 1), w, font=font_cap, fill=(0, 0, 0, 255))
                    draw_f.text((curr_x, cap_y), w, font=font_cap, fill=(255, 220, 20, 255), stroke_width=3, stroke_fill=(180, 20, 30, 255))
                elif idx < w_idx:
                    # Spoken words: Crisp White
                    draw_f.text((curr_x, cap_y), w, font=font_cap, fill=(245, 245, 245, 230))
                else:
                    # Upcoming words: Muted Grey
                    draw_f.text((curr_x, cap_y), w, font=font_cap, fill=(150, 150, 155, 160))
                curr_x += word_widths[idx] + space_w

        # Write frame to ffmpeg
        proc.stdin.write(frame_canvas.convert("RGB").tobytes())

        if f_idx % 90 == 0 or f_idx == total_frames - 1:
            pct = (f_idx + 1) / total_frames * 100
            print(f"  Frame {f_idx + 1}/{total_frames} ({pct:.1f}%) rendered...")

    proc.stdin.close()
    proc.wait()
    print("✅ Video frames rendered successfully!")

    # 5. Mux with 44.1kHz Stereo Narration + Ambient Tension Score
    print("🎵 Muxing with master stereo narration and soundtrack...")
    mux_cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
        "-i", str(AUDIO_FILE),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(OUTPUT_VIDEO)
    ]
    subprocess.run(mux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    if raw_video.exists():
        raw_video.unlink()

    shutil.copy(OUTPUT_VIDEO, ARTIFACT_VIDEO)
    print(f"🎉 MASTER VIRAL SHORT COMPLETE: {OUTPUT_VIDEO}")
    print(f"📁 Copied to artifact: {ARTIFACT_VIDEO}")

if __name__ == "__main__":
    render_viral_short()
