#!/usr/bin/env python3
"""
The Bull Print: Authentic MagnatesMedia Viral Shorts Engine for Free Financial Tools
Architecture:
1. 1080x1920 Full Bleed 9:16 Vertical
2. Exactly 1 cut every 3.0s (12 cuts = 36.0s)
3. 35mm clean photographic background plates (zero text)
4. Camera dolly / push-in (1.00 -> 1.05)
5. 3D extruded kinetic typography (forward shear 0.22, 16px shadow, volumetric bloom, elastic slam pop-in)
6. Stabilo glowing tactical highlighter badges
7. Word-level animated mobile captions at Y = 1480 with active-word highlight
8. en-US-ChristopherNeural (-2Hz) + ducked tension BGM (-18 LUFS)
"""

import math
import os
import shutil
import subprocess
import asyncio
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path(__file__).resolve().parent.parent
BRAIN_DIR = Path("/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364")
BGM_POOL = BASE_DIR / "assets" / "audio" / "bgm_pool" / "dark_investigative" / "bed_01_subterranean_pulse.wav"
OUTPUT_DIR = BASE_DIR / "output" / "tool_videos"
FONT_IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"

# Tool 01 Specification: Emergency Runway Diagnostic
TOOL_01_SPEC = {
    "id": "Tool_01_Emergency_Runway_Diagnostic",
    "tool_key": "runway",
    "title": "Are You 1 Paycheck From Financial Ruin?",
    "link": "https://bullprintmedia.com/calculators.html?tool=runway",
    "script_sentences": [
        "If your salary stops tomorrow, how many days can you survive?",
        "Most professionals have less than forty-five days of liquid runway.",
        "One sudden layoff forces panic selling stocks at the absolute bottom.",
        "Or taking sixteen percent personal loans that trap you for years.",
        "We built the Emergency Runway Calculator to give you zero income clarity.",
        "Slide your bank balance, fixed deposits, and monthly mandatory burn.",
        "The quant engine instantly reveals your exact survival days.",
        "Under three months is a critical deficit.",
        "Six to twelve months is a fortified institutional safety moat.",
        "Stop flying blind with your finances.",
        "Use this tool one hundred percent free at bullprintmedia.com.",
        "Download your pre-filled wealth audit report today."
    ],
    "cuts": [
        {
            "id": 1, "start": 0.00, "end": 3.00,
            "plate_name": "clean_bg_cut01_1794027147675.jpg",
            "lines": ["ONE PAYCHECK", "FROM RUIN?"],
            "badge": "SURVIVAL BLIND SPOT",
            "badge_color": (239, 68, 68), "badge_text_col": (255, 255, 255),
            "text_color": (245, 25, 55), "bloom_color": (255, 30, 60),
            "pos": (80, 260), "font_size": 135
        },
        {
            "id": 2, "start": 3.00, "end": 6.00,
            "plate_name": "clean_bg_cut02_1794027147675.jpg",
            "lines": ["45 DAYS", "OF RUNWAY"],
            "badge": "76% OF WORKERS TRAPPED",
            "badge_color": (255, 215, 0), "badge_text_col": (10, 10, 10),
            "text_color": (255, 215, 0), "bloom_color": (255, 190, 30),
            "pos": (70, 250), "font_size": 130
        },
        {
            "id": 3, "start": 6.00, "end": 9.00,
            "plate_name": "clean_bg_cut03_1794027172678.jpg",
            "lines": ["PANIC SELLING", "AT THE BOTTOM"],
            "badge": "FORCED LIQUIDATION",
            "badge_color": (239, 68, 68), "badge_text_col": (255, 255, 255),
            "text_color": (245, 25, 55), "bloom_color": (255, 30, 60),
            "pos": (60, 240), "font_size": 125
        },
        {
            "id": 4, "start": 9.00, "end": 12.00,
            "plate_name": "clean_bg_cut04_1794027203194.jpg",
            "lines": ["16% DEBT", "INTEREST TRAP"],
            "badge": "EMERGENCY LOAN SPIRAL",
            "badge_color": (245, 158, 11), "badge_text_col": (10, 10, 10),
            "text_color": (245, 158, 11), "bloom_color": (255, 160, 20),
            "pos": (70, 250), "font_size": 130
        },
        {
            "id": 5, "start": 12.00, "end": 15.00,
            "plate_name": "clean_bg_cut05_1794027228097.jpg",
            "lines": ["EMERGENCY", "RUNWAY OS"],
            "badge": "THE SOLUTION",
            "badge_color": (0, 135, 90), "badge_text_col": (255, 255, 255),
            "text_color": (0, 220, 130), "bloom_color": (0, 180, 90),
            "pos": (80, 250), "font_size": 135
        },
        {
            "id": 6, "start": 15.00, "end": 18.00,
            "plate_name": "clean_bg_cut06_1794027252344.jpg",
            "lines": ["SLIDE YOUR", "MONTHLY BURN"],
            "badge": "INTERACTIVE MODEL",
            "badge_color": (0, 229, 255), "badge_text_col": (10, 10, 10),
            "text_color": (0, 229, 255), "bloom_color": (0, 200, 240),
            "pos": (70, 250), "font_size": 130
        },
        {
            "id": 7, "start": 18.00, "end": 21.00,
            "plate_name": "clean_bg_cut07_1794027281045.jpg",
            "lines": ["EXACT DAYS", "LEFT TO SURVIVE"],
            "badge": "QUANT ALGORITHM",
            "badge_color": (255, 215, 0), "badge_text_col": (10, 10, 10),
            "text_color": (255, 215, 0), "bloom_color": (255, 190, 30),
            "pos": (60, 250), "font_size": 125
        },
        {
            "id": 8, "start": 21.00, "end": 24.00,
            "plate_name": "12min_doc_plate_01.jpg",
            "lines": ["< 3 MONTHS", "CRITICAL RISK"],
            "badge": "DEFICIT WARNING",
            "badge_color": (239, 68, 68), "badge_text_col": (255, 255, 255),
            "text_color": (245, 25, 55), "bloom_color": (255, 30, 60),
            "pos": (80, 250), "font_size": 130
        },
        {
            "id": 9, "start": 24.00, "end": 27.00,
            "plate_name": "12min_doc_plate_02.jpg",
            "lines": ["12 MONTHS", "FORTIFIED MOAT"],
            "badge": "INVINCIBLE DEFENSE",
            "badge_color": (0, 135, 90), "badge_text_col": (255, 255, 255),
            "text_color": (0, 220, 130), "bloom_color": (0, 180, 90),
            "pos": (70, 250), "font_size": 130
        },
        {
            "id": 10, "start": 27.00, "end": 30.00,
            "plate_name": "12min_doc_plate_03.jpg",
            "lines": ["STOP FLYING", "BLIND TODAY"],
            "badge": "MASTER THE MATH",
            "badge_color": (255, 215, 0), "badge_text_col": (10, 10, 10),
            "text_color": (255, 215, 0), "bloom_color": (255, 190, 30),
            "pos": (80, 250), "font_size": 130
        },
        {
            "id": 11, "start": 30.00, "end": 33.00,
            "plate_name": "12min_doc_plate_04.jpg",
            "lines": ["100% FREE", "BULLPRINTMEDIA.COM"],
            "badge": "NO PAYWALL • FREE ACCESS",
            "badge_color": (0, 135, 90), "badge_text_col": (255, 255, 255),
            "text_color": (0, 220, 130), "bloom_color": (0, 180, 90),
            "pos": (60, 250), "font_size": 120
        },
        {
            "id": 12, "start": 33.00, "end": 36.00,
            "plate_name": "bull_print_banner_plate_1794211800384.jpg",
            "lines": ["GET YOUR WEALTH", "AUDIT REPORT"],
            "badge": "LINK IN DESCRIPTION",
            "badge_color": (255, 215, 0), "badge_text_col": (10, 10, 10),
            "text_color": (255, 215, 0), "bloom_color": (255, 190, 30),
            "pos": (50, 250), "font_size": 115
        }
    ],
    "captions": [
        (0.00, 3.00, ["If", "your", "salary", "stops", "tomorrow,"]),
        (3.00, 6.00, ["Most", "workers", "have", "under", "45", "days."]),
        (6.00, 9.00, ["A", "layoff", "forces", "panic", "selling", "stocks."]),
        (9.00, 12.00, ["Or", "taking", "16%", "emergency", "loans."]),
        (12.00, 15.00, ["We", "built", "the", "Runway", "Calculator."]),
        (15.00, 18.00, ["Slide", "your", "bank", "balance", "and", "burn."]),
        (18.00, 21.00, ["It", "reveals", "your", "exact", "survival", "days."]),
        (21.00, 24.00, ["Under", "3", "months", "is", "critical."]),
        (24.00, 27.00, ["12", "months", "is", "an", "invincible", "moat."]),
        (27.00, 30.00, ["Stop", "flying", "blind", "with", "money."]),
        (30.00, 33.00, ["Use", "this", "free", "at", "bullprintmedia.com."]),
        (33.00, 36.00, ["Download", "your", "wealth", "audit", "report."])
    ]
}

def load_and_prep_plate(path, w=1080, h=1920):
    if not path.exists():
        # Fallback to any existing plate
        fallback = list(BRAIN_DIR.glob("*.jpg"))[0]
        path = fallback
    im = Image.open(path).convert("RGB")
    scale = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    left = (im.width - w) // 2
    top = (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))

async def generate_voice(text, out_path):
    import edge_tts
    comm = edge_tts.Communicate(text, "en-US-ChristopherNeural", rate="-2%")
    await comm.save(str(out_path))

def build_tool_short(spec):
    tool_folder = OUTPUT_DIR / spec["id"]
    tool_folder.mkdir(parents=True, exist_ok=True)
    voice_file = tool_folder / "christopher_voice.mp3"
    raw_video = tool_folder / "raw_frames.mp4"
    final_short = tool_folder / "master_video_magnates.mp4"

    full_narration = " ".join(spec["script_sentences"])

    # 1. Synthesize ChristopherNeural
    print(f"🎙️ Synthesizing ChristopherNeural (-2Hz) for {spec['id']}...")
    asyncio.run(generate_voice(full_narration, voice_file))

    # 2. Preload plates
    W, H = 1080, 1920
    fps = 30
    total_duration = 36.0
    total_frames = int(total_duration * fps)

    print("🖼️ Preloading 12 clean 35mm photographic background plates...")
    plates = {}
    for c in spec["cuts"]:
        plate_p = BRAIN_DIR / c["plate_name"]
        plates[c["id"]] = load_and_prep_plate(plate_p, W, H)

    # 3. Stream frames to ffmpeg
    print(f"🎬 Rendering {total_frames} frames ({total_duration}s) with MagnatesMedia kinetic 3D engine...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p", str(raw_video)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for f_idx in range(total_frames):
        t = f_idx / fps

        curr_cut = spec["cuts"][-1]
        for c in spec["cuts"]:
            if c["start"] <= t < c["end"]:
                curr_cut = c
                break

        cut_t = t - curr_cut["start"]
        cut_duration = curr_cut["end"] - curr_cut["start"]
        cut_progress = cut_t / cut_duration

        # Camera Dolly (1.00 -> 1.05)
        zoom = 1.0 + 0.05 * cut_progress
        base_im = plates[curr_cut["id"]]
        zw, zh = int(W * zoom), int(H * zoom)
        zoomed = base_im.resize((zw, zh), Image.Resampling.BILINEAR)
        zx = (zw - W) // 2
        zy = (zh - H) // 2
        frame_canvas = zoomed.crop((zx, zy, zx + W, zy + H)).convert("RGBA")

        # Kinetic Slam Pop-In (0.28s)
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

        # 3D Extruded Slanted Text Layer
        text_w, text_h = 1000, 650
        text_layer = Image.new("RGBA", (text_w, text_h), (0, 0, 0, 0))
        draw_t = ImageDraw.Draw(text_layer)

        f_size = int(curr_cut["font_size"] * scale_anim)
        f_hero = ImageFont.truetype(FONT_IMPACT, f_size)
        f_badge = ImageFont.truetype(FONT_IMPACT, int(46 * scale_anim))

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

        # Stabilo Marker Badge
        badge_text = curr_cut["badge"]
        b_len = int(draw_t.textlength(badge_text, font=f_badge))
        b_pad_x = 22
        b_h = int(60 * scale_anim)
        b_w = b_len + (b_pad_x * 2)
        b_y = y_offset + 14

        wipe_p = 1.0 if cut_t >= 0.40 else ((cut_t - 0.15) / 0.25 if cut_t >= 0.15 else 0.0)
        if wipe_p > 0.05:
            active_bw = int(b_w * wipe_p)
            bg_col = curr_cut["badge_color"]
            draw_t.rectangle([25, b_y, 25 + active_bw, b_y + b_h], fill=(bg_col[0], bg_col[1], bg_col[2], int(alpha_anim * 0.94)))
            if wipe_p > 0.4:
                b_text_col = curr_cut["badge_text_col"]
                draw_t.text((25 + b_pad_x, b_y + 8), badge_text, font=f_badge, fill=(b_text_col[0], b_text_col[1], b_text_col[2], alpha_anim))

        # Forward Italic Shear (0.22)
        m = [1, -0.22, 0, 0, 1, 0]
        slanted_text = text_layer.transform((text_w + 140, text_h), Image.Transform.AFFINE, m, resample=Image.Resampling.BILINEAR)

        # Volumetric Neon Bloom
        alpha_channel = slanted_text.split()[3]
        bloom_mask = alpha_channel.filter(ImageFilter.GaussianBlur(32))
        bloom_layer = Image.new("RGBA", slanted_text.size, (col_bloom[0], col_bloom[1], col_bloom[2], 0))
        bloom_layer.putalpha(bloom_mask)

        tx, ty = curr_cut["pos"]
        frame_canvas.alpha_composite(bloom_layer, (tx, ty))
        frame_canvas.alpha_composite(slanted_text, (tx, ty))

        # Mobile Word-Level Captions at Y = 1480
        draw_f = ImageDraw.Draw(frame_canvas)
        active_chunk = None
        for c_start, c_end, words in spec["captions"]:
            if c_start <= t <= c_end:
                active_chunk = (c_start, c_end, words)
                break

        if active_chunk:
            c_start, c_end, words = active_chunk
            n_words = len(words)
            c_dur = c_end - c_start
            w_idx = int(((t - c_start) / max(0.01, c_dur)) * n_words)
            w_idx = max(0, min(n_words - 1, w_idx))

            font_cap = ImageFont.truetype(FONT_IMPACT, 52)
            word_widths = [draw_f.textlength(w, font=font_cap) for w in words]
            space_w = draw_f.textlength(" ", font=font_cap)
            total_cap_w = sum(word_widths) + space_w * (n_words - 1)

            cap_x = (W - total_cap_w) // 2
            cap_y = 1480

            pill_pad_x = 24
            pill_pad_y = 10
            draw_f.rounded_rectangle(
                [cap_x - pill_pad_x, cap_y - pill_pad_y, cap_x + total_cap_w + pill_pad_x, cap_y + 60 + pill_pad_y],
                radius=18,
                fill=(10, 10, 15, 215),
                outline=(255, 215, 0, 180) if (w_idx % 2 == 0) else (239, 68, 68, 180),
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

        proc.stdin.write(frame_canvas.convert("RGB").tobytes())

        if f_idx % 90 == 0 or f_idx == total_frames - 1:
            print(f"  Frame {f_idx + 1}/{total_frames} rendered...")

    proc.stdin.close()
    proc.wait()

    # 4. Audio Mux: Christopher voice + BGM ducked at -18 LUFS (volume=0.18)
    print("🎵 Muxing Christopher voice with ducked ambient tension soundtrack...")
    mux_cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
        "-i", str(voice_file),
        "-i", str(BGM_POOL),
        "-filter_complex",
        "[2:a]volume=0.16[bgm];[1:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(final_short)
    ]
    subprocess.run(mux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    if raw_video.exists():
        raw_video.unlink()

    # Copy to original master_video.mp4 destination
    shutil.copy(final_short, tool_folder / "master_video.mp4")
    print(f"🎉 SUCCESS! MagnatesMedia Master Short generated: {final_short}")

if __name__ == "__main__":
    build_tool_short(TOOL_01_SPEC)
