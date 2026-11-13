#!/usr/bin/env python3
"""
Render & Upload Short 01: The $2.5 Trillion AI Crash
Format: Vertical 9:16 (1080x1920)
Style: MagnatesMedia Visual & Kinetic 3D Typography
Privacy Status: PRIVATE
"""

import math
import os
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path(__file__).resolve().parent.parent
BRAIN_DIR = Path("/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364")
AUDIO_FILE = BASE_DIR / "output" / "shorts" / "short_01_audio.wav"
OUTPUT_DIR = BASE_DIR / "output" / "shorts"
OUTPUT_VIDEO = OUTPUT_DIR / "short_01_final.mp4"
ARTIFACT_VIDEO = BRAIN_DIR / "short_01_final.mp4"
THUMBNAIL_PATH = OUTPUT_DIR / "short_01_thumb.jpg"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

CUTS = [
    {
        "id": 1,
        "start": 0.00,
        "end": 7.20,
        "plate": BRAIN_DIR / "short01_cut01_1794064067928.jpg",
        "lines": ["$2.5 TRILLION", "WIPED OUT"],
        "badge": "NASDAQ CORRECTION",
        "badge_color": (255, 230, 0),
        "badge_text_col": (10, 10, 10),
        "text_color": (245, 25, 55),
        "bloom_color": (255, 30, 60),
        "pos": (80, 260),
        "font_size": 135,
    },
    {
        "id": 2,
        "start": 7.20,
        "end": 14.50,
        "plate": BRAIN_DIR / "short01_cut02_1794064112774.jpg",
        "lines": ["WORST DROP", "SINCE APRIL"],
        "badge": "-5.5% SINGLE-DAY PLUNGE",
        "badge_color": (245, 30, 60),
        "badge_text_col": (255, 255, 255),
        "text_color": (245, 30, 60),
        "bloom_color": (255, 40, 70),
        "pos": (70, 240),
        "font_size": 130,
    },
    {
        "id": 3,
        "start": 14.50,
        "end": 22.00,
        "plate": BRAIN_DIR / "short01_cut03_1794064154679.jpg",
        "lines": ["AI DATA CENTERS", "IN CROSSHAIRS"],
        "badge": "SUBSIDY INVESTIGATION",
        "badge_color": (255, 215, 0),
        "badge_text_col": (10, 10, 10),
        "text_color": (255, 215, 0),
        "bloom_color": (255, 190, 30),
        "pos": (60, 250),
        "font_size": 120,
    },
    {
        "id": 4,
        "start": 22.00,
        "end": 29.50,
        "plate": BRAIN_DIR / "short01_cut04_1794064198173.jpg",
        "lines": ["CAPITOL HILL", "GRIDLOCK"],
        "badge": "REGULATORY CLAMP",
        "badge_color": (255, 230, 0),
        "badge_text_col": (10, 10, 10),
        "text_color": (255, 60, 25),
        "bloom_color": (255, 80, 30),
        "pos": (80, 240),
        "font_size": 130,
    },
    {
        "id": 5,
        "start": 29.50,
        "end": 35.95,
        "plate": BRAIN_DIR / "short01_cut05_1794064254097.jpg",
        "lines": ["THE FREE PASS", "IS OVER"],
        "badge": "AI VALUATIONS RESET",
        "badge_color": (245, 30, 60),
        "badge_text_col": (255, 255, 255),
        "text_color": (245, 25, 55),
        "bloom_color": (255, 35, 65),
        "pos": (70, 240),
        "font_size": 130,
    },
]

CAPTION_CHUNKS = [
    (0.10, 2.80, ["In", "a", "single", "24-hour", "window,"]),
    (2.80, 4.80, ["$2.5", "Trillion", "dollars"]),
    (4.80, 7.20, ["evaporated", "from", "the", "Nasdaq."]),
    (7.20, 9.60, ["Tech", "shares", "plunged", "hard,"]),
    (9.60, 12.00, ["worst", "drop", "since", "April,"]),
    (12.00, 14.50, ["entering", "correction", "territory."]),
    (14.50, 17.00, ["The", "midterm", "elections", "sparked"]),
    (17.00, 19.50, ["fears", "of", "tough", "AI", "regulations"]),
    (19.50, 22.00, ["on", "hyperscale", "data", "centers."]),
    (22.00, 24.50, ["When", "Wall", "Street", "saw", "gridlock,"]),
    (24.50, 27.00, ["hedge", "funds", "rushed", "for"]),
    (27.00, 29.50, ["the", "exits", "simultaneously."]),
    (29.50, 32.50, ["The", "AI", "boom", "isn't", "dead."]),
    (32.50, 35.95, ["But", "the", "free", "pass", "is", "over."])
]

def load_and_prep_plate(path, w=1080, h=1920):
    im = Image.open(path).convert("RGB")
    scale = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    left = (im.width - w) // 2
    top = (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))

def render_short():
    W, H = 1080, 1920
    fps = 30
    total_duration = 35.95
    total_frames = int(total_duration * fps)

    font_impact = "/System/Library/Fonts/Supplemental/Impact.ttf"

    print("⏳ Preloading 5 vertical 9:16 background plates...")
    plates = {c["id"]: load_and_prep_plate(c["plate"], W, H) for c in CUTS}

    raw_video = OUTPUT_DIR / "temp_short_01.mp4"

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

    print(f"🎬 Rendering Short 01 ({total_frames} frames)...")

    for f_idx in range(total_frames):
        t = f_idx / fps

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

        # 2. Kinetic 3D Slam Physics
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

        # 3. 3D Kinetic Text Layer
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
            for d in range(16, 0, -2):
                shade = int(70 * (1.0 - d / 16.0))
                draw_t.text((25 + d, y_offset + d), line, font=f_hero, fill=(shade, 0, 0, alpha_anim), stroke_width=7, stroke_fill=(0, 0, 0, alpha_anim))
            draw_t.text((25, y_offset), line, font=f_hero, fill=(col_face[0], col_face[1], col_face[2], alpha_anim), stroke_width=5, stroke_fill=(15, 0, 5, alpha_anim))
            y_offset += line_spacing

        # Neon Highlighter Badge
        badge_text = curr_cut["badge"]
        b_len = int(draw_t.textlength(badge_text, font=f_badge))
        b_pad_x = 24
        b_h = int(64 * scale_anim)
        b_w = b_len + (b_pad_x * 2)
        b_y = y_offset + 14

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

        shear = 0.22
        m = [1, -shear, 0, 0, 1, 0]
        slanted_text = text_layer.transform((text_w + 140, text_h), Image.Transform.AFFINE, m, resample=Image.Resampling.BILINEAR)

        alpha_channel = slanted_text.split()[3]
        bloom_mask = alpha_channel.filter(ImageFilter.GaussianBlur(32))
        bloom_layer = Image.new("RGBA", slanted_text.size, (col_bloom[0], col_bloom[1], col_bloom[2], 0))
        bloom_layer.putalpha(bloom_mask)

        tx, ty = curr_cut["pos"]
        frame_canvas.alpha_composite(bloom_layer, (tx, ty))
        frame_canvas.alpha_composite(slanted_text, (tx, ty))

        # 4. Animated Mobile Captions
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

            pill_pad_x = 28
            pill_pad_y = 12
            draw_f.rounded_rectangle(
                [cap_x - pill_pad_x, cap_y - pill_pad_y, cap_x + total_cap_w + pill_pad_x, cap_y + 64 + pill_pad_y],
                radius=20,
                fill=(10, 10, 15, 215),
                outline=(245, 158, 11, 180) if (w_idx % 2 == 0) else (239, 68, 68, 180),
                width=3
            )

            curr_x = cap_x
            for idx, w in enumerate(words):
                if idx == w_idx:
                    draw_f.text((curr_x + 1, cap_y + 1), w, font=font_cap, fill=(0, 0, 0, 255))
                    draw_f.text((curr_x, cap_y), w, font=font_cap, fill=(255, 220, 20, 255), stroke_width=3, stroke_fill=(180, 20, 30, 255))
                elif idx < w_idx:
                    draw_f.text((curr_x, cap_y), w, font=font_cap, fill=(245, 245, 245, 230))
                else:
                    draw_f.text((curr_x, cap_y), w, font=font_cap, fill=(150, 150, 155, 160))
                curr_x += word_widths[idx] + space_w

        # Save thumbnail at t=2.5s
        if f_idx == int(2.5 * fps):
            frame_canvas.convert("RGB").save(THUMBNAIL_PATH)

        proc.stdin.write(frame_canvas.convert("RGB").tobytes())

        if f_idx % 90 == 0 or f_idx == total_frames - 1:
            pct = (f_idx + 1) / total_frames * 100
            print(f"  Frame {f_idx + 1}/{total_frames} ({pct:.1f}%) rendered...")

    proc.stdin.close()
    proc.wait()

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
    print(f"🎉 RENDER COMPLETE: {OUTPUT_VIDEO}")

def upload_to_youtube():
    print("\n" + "=" * 70)
    print("🚀 UPLOADING SHORT 01 TO YOUTUBE (PRIVATE)")
    print("=" * 70)

    title = "The $2.5 Trillion AI Crash: What Happened to Big Tech #Shorts"
    desc = """In a single 24-hour trading session, $2.5 Trillion in market value evaporated from the Nasdaq. Here is what triggered the tech panic post-midterms.

Subscribe to @TheBullPrint for daily macroeconomic intelligence and investigative breakdowns.

#TheBullPrint #TechStocks #Nasdaq #AI #StockMarket #Shorts"""
    tags = ["TheBullPrint", "TechStocks", "Nasdaq", "AI", "StockMarket", "Shorts"]

    uploader = YouTubeUploader()
    res = uploader.upload_video(
        language="en",
        video_path=str(OUTPUT_VIDEO),
        title=title,
        description=desc,
        tags=tags,
        category_id="25",
        privacy_status="private",
        is_short=True,
        thumbnail_path=str(THUMBNAIL_PATH) if THUMBNAIL_PATH.exists() else None,
        force_upload=True
    )

    if res.get("success"):
        vid_id = res.get("video_id")
        url = res.get("url") or f"https://www.youtube.com/shorts/{vid_id}"
        print(f"🎉 SHORT 01 IS UPLOADED (PRIVATE): {url} (ID: {vid_id})")
        return url, vid_id
    else:
        print(f"❌ Upload failed: {res.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    render_short()
    upload_to_youtube()
