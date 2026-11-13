#!/usr/bin/env python3
"""
MagnatesMedia Exact Visual & Kinetic 3D Typography Master - 30-Second Sample
Documentary: The Zero-Day Options Casino
Channel: The Bull Print (@thebullprint)

Matches the exact aesthetic of MagnatesMedia ('The INSANE Truth About YouTube' - https://youtu.be/Qbe0I3X6R-o):
1. Clean 35mm / 3D Cinematic Background Plates (100% full bleed, zero baked-in text).
2. Giant 3D Extruded Perspective Typography (Italic slant, multi-depth extrusion, saturated crimson/gold).
3. Intense Volumetric Neon Bloom / Atmospheric Aura radiating outward behind text.
4. Elastic Kinetic Slam Pop-In physics (1.38x -> 1.0x bounce) + camera drift / slow dolly.
5. Authentic Neon Highlighter Badges (Stabilo-style marker box over key stats).
6. Cinematic 2.35:1 Letterbox Bars (75px top and bottom).
7. Lower-Third Word-Level Animated Captions synchronized to Christopher narration.
8. 44.1kHz Stereo Narration + Score Audio Mux.
"""

import math
import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path(__file__).resolve().parent.parent
BRAIN_DIR = Path("/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364")
AUDIO_FILE = BASE_DIR / "output" / "options_casino_documentary" / "sample_30s.wav"
OUTPUT_DIR = BASE_DIR / "output" / "options_casino_documentary"
OUTPUT_VIDEO = OUTPUT_DIR / "options_casino_30s_magnates_exact_sample.mp4"
ARTIFACT_VIDEO = BRAIN_DIR / "options_casino_30s_magnates_exact_sample.mp4"

# 7 Narrative Scene Beats across 30.08 Seconds
CUTS = [
    {
        "id": 1,
        "start": 0.00,
        "end": 4.40,
        "plate": BRAIN_DIR / "clean_bg_cut01_1794022641757.jpg",
        "lines": ["ZERO AT", "3:15 PM"],
        "badge": "90-SECOND WIPE",
        "badge_color": (255, 230, 0),    # Neon Yellow Marker
        "badge_text_col": (10, 10, 10),
        "text_color": (245, 25, 55),      # Crimson Red
        "bloom_color": (255, 30, 60),
        "pos": (120, 140),
        "font_size": 135,
    },
    {
        "id": 2,
        "start": 4.40,
        "end": 8.50,
        "plate": BRAIN_DIR / "clean_bg_cut02_1794027147675.jpg",
        "lines": ["HOW RETAIL", "WAS TRAPPED"],
        "badge": "ZERO-DAY EXPIRY",
        "badge_color": (245, 30, 60),     # Glowing Red Marker
        "badge_text_col": (255, 255, 255),
        "text_color": (245, 30, 60),
        "bloom_color": (255, 40, 70),
        "pos": (120, 140),
        "font_size": 130,
    },
    {
        "id": 3,
        "start": 8.50,
        "end": 13.00,
        "plate": BRAIN_DIR / "clean_bg_cut03_1794027172678.jpg",
        "lines": ["STOP-LOSS", "TRIGGERED"],
        "badge": "HFT ALGORITHMS",
        "badge_color": (255, 215, 0),    # Electric Gold Marker
        "badge_text_col": (10, 10, 10),
        "text_color": (245, 30, 60),
        "bloom_color": (255, 30, 60),
        "pos": (120, 140),
        "font_size": 130,
    },
    {
        "id": 4,
        "start": 13.00,
        "end": 17.45,
        "plate": BRAIN_DIR / "clean_bg_cut04_1794027203194.jpg",
        "lines": ["VAPORIZED", "IN 90 SECONDS"],
        "badge": "4 YEARS OF SAVINGS",
        "badge_color": (255, 230, 0),    # Neon Yellow
        "badge_text_col": (10, 10, 10),
        "text_color": (255, 60, 20),      # Fiery Amber Red
        "bloom_color": (255, 80, 30),
        "pos": (120, 140),
        "font_size": 125,
    },
    {
        "id": 5,
        "start": 17.45,
        "end": 21.50,
        "plate": BRAIN_DIR / "clean_bg_cut05_1794027228097.jpg",
        "lines": ["THE RS. 50", "CALL OPTION"],
        "badge": "OUT-OF-THE-MONEY",
        "badge_color": (245, 30, 60),
        "badge_text_col": (255, 255, 255),
        "text_color": (255, 200, 20),     # Electric Gold
        "bloom_color": (255, 180, 20),
        "pos": (120, 140),
        "font_size": 130,
    },
    {
        "id": 6,
        "start": 21.50,
        "end": 25.65,
        "plate": BRAIN_DIR / "clean_bg_cut06_1794027252344.jpg",
        "lines": ["WORTHLESS."],
        "badge": "RS. 0.05 PER CONTRACT",
        "badge_color": (245, 30, 60),
        "badge_text_col": (255, 255, 255),
        "text_color": (245, 20, 50),
        "bloom_color": (255, 30, 60),
        "pos": (140, 160),
        "font_size": 160,
    },
    {
        "id": 7,
        "start": 25.65,
        "end": 30.08,
        "plate": BRAIN_DIR / "clean_bg_cut07_1794027281045.jpg",
        "lines": ["RS. 1.8 LAKH", "CRORE"],
        "badge": "MASS WEALTH TRANSFER",
        "badge_color": (255, 220, 0),
        "badge_text_col": (10, 10, 10),
        "text_color": (255, 215, 0),     # Brilliant Gold
        "bloom_color": (255, 200, 30),
        "pos": (120, 140),
        "font_size": 140,
    },
]

# Spoken Sentences with Word-Level Timings
SENTENCES = [
    (0.15, 4.40, ["It", "is", "3:15", "PM", "on", "a", "Thursday", "afternoon", "in", "Mumbai."]),
    (4.45, 10.15, ["A", "26-year-old", "software", "engineer", "sits", "frozen", "in", "front", "of", "a", "red-stained", "trading", "screen."]),
    (10.20, 17.40, ["His", "bank", "balance,", "built", "over", "four", "years", "of", "grueling", "corporate", "overtime,", "has", "just", "vaporized", "in", "ninety", "seconds."]),
    (17.45, 23.95, ["His", "out-of-the-money", "call", "option,", "bought", "for", "fifty", "rupees,", "drops", "to", "zero", "point", "zero", "five."]),
    (24.00, 25.65, ["Worthless."]),
    (25.70, 27.85, ["This", "is", "not", "bad", "luck."]),
    (27.90, 30.00, ["It", "is", "the", "greatest", "retail", "wealth", "transfer", "in", "Indian", "financial", "history."])
]

def load_and_prep_plate(path, w=1920, h=1080):
    im = Image.open(path).convert("RGB")
    scale = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    left = (im.width - w) // 2
    top = (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))

def render_magnates_sample():
    W, H = 1920, 1080
    fps = 30
    total_duration = 30.08
    total_frames = int(total_duration * fps)

    font_impact = "/System/Library/Fonts/Supplemental/Impact.ttf"
    font_caption = "/System/Library/Fonts/Helvetica.ttc"

    # Preload background plates
    print("⏳ Preloading clean 35mm background plates...")
    plates = {}
    for cut in CUTS:
        plates[cut["id"]] = load_and_prep_plate(cut["plate"], W, H)

    # Temporary raw video file before audio mux
    raw_video = OUTPUT_DIR / "temp_magnates_video.mp4"

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

    print(f"🎬 Rendering {total_frames} frames ({total_duration:.1f}s) in MagnatesMedia exact visual style...")

    for f_idx in range(total_frames):
        t = f_idx / fps

        # Find current cut
        curr_cut = CUTS[-1]
        for c in CUTS:
            if c["start"] <= t < c["end"]:
                curr_cut = c
                break

        # Cut-relative time
        cut_t = t - curr_cut["start"]
        cut_duration = curr_cut["end"] - curr_cut["start"]
        cut_progress = cut_t / cut_duration

        # 1. Camera Slow Dolly / Zoom (1.00 -> 1.045)
        zoom = 1.0 + 0.045 * cut_progress
        base_im = plates[curr_cut["id"]]
        zw, zh = int(W * zoom), int(H * zoom)
        zoomed = base_im.resize((zw, zh), Image.Resampling.BILINEAR)
        zx = (zw - W) // 2
        zy = (zh - H) // 2
        frame_canvas = zoomed.crop((zx, zy, zx + W, zy + H)).convert("RGBA")

        # 2. Kinetic 3D Slam Physics for Text
        # Slam in first 9 frames (0.3s): 1.38x down to 1.0x with elastic rebound bounce
        slam_duration = 0.30
        if cut_t < slam_duration:
            p = cut_t / slam_duration
            # Elastic overshoot equation
            scale_anim = 1.0 + 0.38 * ((1.0 - p) ** 2) * math.cos(p * math.pi * 2.5)
            alpha_anim = min(255, int(255 * (p * 2.0)))
            shake_y = int(5.0 * (1.0 - p) * math.sin(p * math.pi * 4))
        else:
            p_hold = cut_t - slam_duration
            scale_anim = 1.0 + 0.015 * cut_progress
            alpha_anim = 255
            shake_y = int(2.0 * math.sin(p_hold * 2.5))

        # 3. Render 3D Extruded Slanted Text & Highlighter Marker
        text_w, text_h = 1300, 750
        text_layer = Image.new("RGBA", (text_w, text_h), (0, 0, 0, 0))
        draw_t = ImageDraw.Draw(text_layer)

        f_size = int(curr_cut["font_size"] * scale_anim)
        f_hero = ImageFont.truetype(font_impact, f_size)
        f_badge = ImageFont.truetype(font_impact, int(52 * scale_anim))

        y_offset = 20 + shake_y
        line_spacing = int(f_size * 0.98)
        col_face = curr_cut["text_color"]
        col_bloom = curr_cut["bloom_color"]

        for line in curr_cut["lines"]:
            # 3D Extrusion Pass (depth 16px down-right)
            for d in range(16, 0, -2):
                shade = int(70 * (1.0 - d / 16.0))
                draw_t.text((30 + d, y_offset + d), line, font=f_hero, fill=(shade, 0, 0, alpha_anim), stroke_width=6, stroke_fill=(0, 0, 0, alpha_anim))
            # Text Front Face
            draw_t.text((30, y_offset), line, font=f_hero, fill=(col_face[0], col_face[1], col_face[2], alpha_anim), stroke_width=4, stroke_fill=(15, 0, 5, alpha_anim))
            y_offset += line_spacing

        # Neon Highlighter Marker Badge
        badge_text = curr_cut["badge"]
        b_len = int(draw_t.textlength(badge_text, font=f_badge))
        b_pad_x = 28
        b_h = int(68 * scale_anim)
        b_w = b_len + (b_pad_x * 2)
        b_y = y_offset + 12

        # Highlighter wipe progress (wipes from left to right in 0.2s after slam)
        if cut_t < 0.20:
            wipe_p = 0.0
        elif cut_t < 0.45:
            wipe_p = (cut_t - 0.20) / 0.25
        else:
            wipe_p = 1.0

        if wipe_p > 0.05:
            active_bw = int(b_w * wipe_p)
            bg_col = curr_cut["badge_color"]
            draw_t.rectangle([30, b_y, 30 + active_bw, b_y + b_h], fill=(bg_col[0], bg_col[1], bg_col[2], int(alpha_anim * 0.92)))
            # If wipe is mostly done, draw badge text
            if wipe_p > 0.4:
                b_text_col = curr_cut["badge_text_col"]
                draw_t.text((30 + b_pad_x, b_y + 8), badge_text, font=f_badge, fill=(b_text_col[0], b_text_col[1], b_text_col[2], alpha_anim))

        # Apply Italic Slant / Shear (forward slant = 0.22)
        shear = 0.22
        m = [1, -shear, 0, 0, 1, 0]
        slanted_text = text_layer.transform((text_w + 150, text_h), Image.Transform.AFFINE, m, resample=Image.Resampling.BILINEAR)

        # Generate Volumetric Bloom / Outer Glow
        alpha_channel = slanted_text.split()[3]
        bloom_mask = alpha_channel.filter(ImageFilter.GaussianBlur(32))
        bloom_layer = Image.new("RGBA", slanted_text.size, (col_bloom[0], col_bloom[1], col_bloom[2], 0))
        bloom_layer.putalpha(bloom_mask)

        # Composite Bloom and Text onto Frame
        tx, ty = curr_cut["pos"]
        frame_canvas.alpha_composite(bloom_layer, (tx, ty))
        frame_canvas.alpha_composite(slanted_text, (tx, ty))

        # 4. Lower-Third Word-Level Animated Captions
        active_sent = None
        for s_start, s_end, words in SENTENCES:
            if s_start <= t <= s_end + 0.3:
                active_sent = (s_start, s_end, words)
                break

        draw_f = ImageDraw.Draw(frame_canvas)

        if active_sent:
            s_start, s_end, words = active_sent
            n_words = len(words)
            s_dur = s_end - s_start
            w_idx = int(((t - s_start) / max(0.01, s_dur)) * n_words)
            w_idx = max(0, min(n_words - 1, w_idx))

            font_cap = ImageFont.truetype(font_impact, 44)
            # Calculate total caption width
            word_widths = [draw_f.textlength(w, font=font_cap) for w in words]
            space_w = draw_f.textlength(" ", font=font_cap)
            total_caption_w = sum(word_widths) + space_w * (n_words - 1)

            # Cap max width to prevent line overflow
            cap_x = (W - total_caption_w) // 2
            cap_y = 915

            # Translucent dark pill background
            pill_pad = 20
            draw_f.rounded_rectangle(
                [cap_x - pill_pad, cap_y - 8, cap_x + total_caption_w + pill_pad, cap_y + 54],
                radius=14,
                fill=(10, 10, 15, 210),
                outline=(245, 158, 11, 160) if (w_idx % 2 == 0) else (239, 68, 68, 160),
                width=2
            )

            # Draw words with active pop highlight
            curr_x = cap_x
            for idx, w in enumerate(words):
                if idx == w_idx:
                    # Active Word: Glowing Gold or White-Hot with Red stroke
                    draw_f.text((curr_x + 1, cap_y + 1), w, font=font_cap, fill=(0, 0, 0, 255))
                    draw_f.text((curr_x, cap_y), w, font=font_cap, fill=(255, 220, 20, 255), stroke_width=2, stroke_fill=(180, 20, 30, 255))
                elif idx < w_idx:
                    # Spoken words: Crisp White
                    draw_f.text((curr_x, cap_y), w, font=font_cap, fill=(240, 240, 240, 220))
                else:
                    # Upcoming words: Muted Grey
                    draw_f.text((curr_x, cap_y), w, font=font_cap, fill=(150, 150, 155, 160))
                curr_x += word_widths[idx] + space_w

        # 5. Cinematic 2.35:1 Letterbox Bars (75px top, 75px bottom)
        draw_f.rectangle([0, 0, W, 75], fill=(0, 0, 0, 255))
        draw_f.rectangle([0, H - 75, W, H], fill=(0, 0, 0, 255))

        # Write frame to ffmpeg
        proc.stdin.write(frame_canvas.convert("RGB").tobytes())

        if f_idx % 60 == 0 or f_idx == total_frames - 1:
            pct = (f_idx + 1) / total_frames * 100
            print(f"  Frame {f_idx + 1}/{total_frames} ({pct:.1f}%) rendered...")

    proc.stdin.close()
    proc.wait()
    print("✅ Video frames rendered to temporary video file!")

    # 6. Mux with 44.1kHz Stereo Narration + Score Audio
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

    # Clean up temp raw video
    if raw_video.exists():
        raw_video.unlink()

    # Copy to artifacts directory
    shutil.copy(OUTPUT_VIDEO, ARTIFACT_VIDEO)
    print(f"🎉 MASTER 30s MAGNATES SAMPLE COMPLETE: {OUTPUT_VIDEO}")
    print(f"📁 Copied to artifact: {ARTIFACT_VIDEO}")

if __name__ == "__main__":
    render_magnates_sample()
