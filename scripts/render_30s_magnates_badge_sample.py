#!/usr/bin/env python3
"""
30-Second MagnatesMedia Dynamic Anchor Badge & Animated Captions Master
The Bull Print (@thebullprint)

Features:
1. 100% Full Bleed Edge-to-Edge Frame Scaling (1920x1080, ZERO black void)
2. MagnatesMedia Pop-In Anchor Badges on every ~4.1s cut:
   - Spring ease-out scale pop (0.82 -> 1.05 -> 1.0) over first 9 frames (0.3s)
   - Organic sine-wave floating / breathing motion over hold
   - Frosted translucent glass pill with Electric Gold / Flame Crimson accent borders
3. Word-Level Animated Captions in Lower Third:
   - Floating translucent badge with active word highlight (Gold / Crimson)
4. Christopher Narration + 44.1kHz Stereo Score
"""

import math
import os
import re
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
FRAMES_DIR = BASE_DIR / "output" / "options_casino_documentary" / "frames"
AUDIO_FILE = BASE_DIR / "output" / "options_casino_documentary" / "sample_30s.wav"
OUTPUT_VIDEO = BASE_DIR / "output" / "options_casino_documentary" / "options_casino_30s_animated_badge_sample.mp4"
ARTIFACT_VIDEO = Path("/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364/options_casino_30s_animated_badge_sample.mp4")

# 7 Narrative Scene Beats across 30 Seconds (~4.2s per cut)
CUTS_DATA = [
    {
        "start": 0.00,
        "end": 4.40,
        "frame": "Software_engineer_viewing_crashi…_6a6843f4.jpg",
        "badge": "EXHIBIT 01 // 3:15 PM EXPIRY",
        "badge_accent": (245, 158, 11),  # Electric Gold
        "dot_color": (239, 68, 68),       # Recording Red
    },
    {
        "start": 4.40,
        "end": 8.50,
        "frame": "Retail_traders_buying_call_options_40d1a5ce.jpg",
        "badge": "RETAIL CALL MANIA",
        "badge_accent": (245, 158, 11),  # Electric Gold
        "dot_color": (245, 158, 11),
    },
    {
        "start": 8.50,
        "end": 13.00,
        "frame": "Digital_screen_showing_stop-loss…_2d3c5afb.jpg",
        "badge": "STOP-LOSS TRIGGERED",
        "badge_accent": (239, 68, 68),   # Flame Crimson
        "dot_color": (239, 68, 68),
    },
    {
        "start": 13.00,
        "end": 17.45,
        "frame": "Option_ticket_dissolving_into_smoke_9ee681d1.jpg",
        "badge": "VAPORIZED IN 90s",
        "badge_accent": (239, 68, 68),   # Flame Crimson
        "dot_color": (239, 68, 68),
    },
    {
        "start": 17.45,
        "end": 21.50,
        "frame": "Call_option_order_ticking_down_c2a58f3d.jpg",
        "badge": "OTM CALL // RS. 50 BUY",
        "badge_accent": (245, 158, 11),  # Electric Gold
        "dot_color": (245, 158, 11),
    },
    {
        "start": 21.50,
        "end": 25.65,
        "frame": "Trader_defeated_by_expired_option_e5c1bc6e.jpg",
        "badge": "VALUE: RS. 0.05 // WORTHLESS",
        "badge_accent": (239, 68, 68),   # Flame Crimson
        "dot_color": (239, 68, 68),
    },
    {
        "start": 25.65,
        "end": 30.08,
        "frame": "Digital_vortex_sucking_rupee_notes_95b570ec.jpg",
        "badge": "RS. 1.8 LAKH CR WEALTH TRANSFER",
        "badge_accent": (245, 158, 11),  # Electric Gold
        "dot_color": (239, 68, 68),
    },
]

# Exact Spoken Sentences with Word-Level Timings
SENTENCES_DATA = [
    (0.15, 4.40, ["It", "is", "3:15", "PM", "on", "a", "Thursday", "afternoon", "in", "Mumbai."]),
    (4.45, 10.15, ["A", "26-year-old", "software", "engineer", "sits", "frozen", "in", "front", "of", "a", "red-stained", "trading", "screen."]),
    (10.20, 17.40, ["His", "bank", "balance,", "built", "over", "four", "years", "of", "grueling", "corporate", "overtime,", "has", "just", "vaporized", "in", "ninety", "seconds."]),
    (17.45, 23.95, ["His", "out-of-the-money", "call", "option,", "bought", "for", "fifty", "rupees,", "drops", "to", "zero", "point", "zero", "five."]),
    (24.00, 25.65, ["Worthless."]),
    (25.70, 27.85, ["This", "is", "not", "bad", "luck."]),
    (27.90, 30.00, ["It", "is", "the", "greatest", "retail", "wealth", "transfer", "in", "Indian", "financial", "history."])
]

RED_TRIGGER_WORDS = {"VAPORIZED", "ZERO", "WORTHLESS", "RED-STAINED", "LOSS", "CRASH", "BAD", "SLAUGHTER"}

def build_word_timeline():
    timeline = []
    for s_start, s_end, words in SENTENCES_DATA:
        s_dur = s_end - s_start
        weights = [max(len(re.sub(r"[^\w]", "", w)), 2) for w in words]
        total_wt = sum(weights)
        chunk_size = 4
        chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
        
        curr_t = s_start
        word_idx = 0
        for c in chunks:
            chunk_words_meta = []
            c_start = curr_t
            for w in c:
                w_wt = weights[word_idx]
                w_dur = (w_wt / total_wt) * s_dur
                clean = re.sub(r"[^\w\$\:\-]", "", w).upper()
                is_red = clean in RED_TRIGGER_WORDS
                chunk_words_meta.append({
                    "word": w,
                    "clean": clean,
                    "start": curr_t,
                    "end": curr_t + w_dur,
                    "is_red": is_red
                })
                curr_t += w_dur
                word_idx += 1
            c_end = curr_t
            timeline.append({
                "chunk_start": c_start,
                "chunk_end": c_end,
                "words": chunk_words_meta
            })
    return timeline

def load_full_bleed_frame(fpath: Path, target_w=1920, target_h=1080) -> Image.Image:
    im = Image.open(fpath).convert("RGB")
    scale = max(target_w / im.width, target_h / im.height)
    new_w = round(im.width * scale)
    new_h = round(im.height * scale)
    resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))

def render_sample():
    print("🎬 Generating 30-Second MagnatesMedia Sample with Animated Badges...")
    timeline = build_word_timeline()
    
    # Pre-scale all cut images to 100% full bleed edge-to-edge
    loaded_cut_images = []
    for cut in CUTS_DATA:
        fpath = FRAMES_DIR / cut["frame"]
        if not fpath.exists():
            raise FileNotFoundError(f"Missing frame {fpath}")
        img = load_full_bleed_frame(fpath)
        loaded_cut_images.append(img)
        print(f"   🖼️ Loaded full-bleed: {cut['frame'][:35]}... ({img.size})")

    font_path = "/System/Library/Fonts/Supplemental/Impact.ttf"
    font_badge = ImageFont.truetype(font_path, 36)
    font_cap = ImageFont.truetype(font_path, 54)
    font_cap_act = ImageFont.truetype(font_path, 58)

    fps = 25
    width, height = 1920, 1080
    total_duration = 30.08
    total_frames = int(total_duration * fps)

    write_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{width}x{height}",
        "-r", str(fps),
        "-i", "-",
        "-i", str(AUDIO_FILE),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(OUTPUT_VIDEO)
    ]
    proc = subprocess.Popen(write_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for f_idx in range(total_frames):
        cur_sec = f_idx / fps
        
        # 1. Determine active cut
        cut_idx = 0
        for idx, cut in enumerate(CUTS_DATA):
            if cut["start"] <= cur_sec < cut["end"] or idx == len(CUTS_DATA) - 1:
                cut_idx = idx
                if cur_sec < cut["end"]:
                    break
                    
        active_cut = CUTS_DATA[cut_idx]
        bg = loaded_cut_images[cut_idx].copy()
        
        # Frame index relative to this cut
        cut_frame_idx = int((cur_sec - active_cut["start"]) * fps)
        
        # 2. Calculate MagnatesMedia Pop-In Animation for the Badge
        if cut_frame_idx < 9:
            # First 9 frames (0.36s): Ease-out spring punch-in
            p = cut_frame_idx / 9.0
            scale = 0.82 + 0.18 * (1.0 - (1.0 - p)**3) + 0.05 * math.sin(p * math.pi)
            alpha = min(255, int(255 * (p * 1.35)))
            y_float = 0.0
        else:
            # Organic subtle breathing float over the remaining hold
            t_float = (cut_frame_idx - 9) / fps
            scale = 1.0 + 0.004 * math.sin(t_float * 3.5)
            y_float = 3.0 * math.sin(t_float * 2.0)
            alpha = 255

        # Create overlay layer
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # 3. DRAW DYNAMIC ANCHOR BADGE (Top-Left Safe Area)
        badge_text = active_cut["badge"]
        b_accent = active_cut["badge_accent"]
        b_dot = active_cut["dot_color"]

        base_box_w = int(draw.textlength(badge_text, font=font_badge) + 64)
        base_box_h = 56
        
        # Apply animated scale to badge dimensions
        box_w = int(base_box_w * scale)
        box_h = int(base_box_h * scale)
        box_x = 72
        box_y = int(60 + y_float)

        # Badge pill backing (Frosted translucent dark glass)
        pill_fill = (10, 14, 20, int(alpha * 0.90))
        border_col = (b_accent[0], b_accent[1], b_accent[2], int(alpha * 0.95))
        
        draw.rounded_rectangle(
            [box_x, box_y, box_x + box_w, box_y + box_h],
            radius=20,
            fill=pill_fill,
            outline=border_col,
            width=2
        )
        
        # Recording / HUD indicator dot
        dot_r = int(5 * scale)
        dot_cx = box_x + int(20 * scale)
        dot_cy = box_y + (box_h // 2)
        draw.ellipse(
            [dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r],
            fill=(b_dot[0], b_dot[1], b_dot[2], alpha)
        )
        
        # Badge Text
        # Scale font dynamically during pop-in
        curr_badge_font = ImageFont.truetype(font_path, max(24, int(36 * scale)))
        tx = box_x + int(36 * scale)
        ty = box_y + (box_h - int(36 * scale)) // 2 - 2
        
        # Text drop shadow + sharp white fill
        draw.text((tx + 2, ty + 2), badge_text, font=curr_badge_font, fill=(0, 0, 0, int(alpha * 0.85)))
        draw.text((tx, ty), badge_text, font=curr_badge_font, fill=(255, 255, 255, alpha))

        # 4. DRAW WORD-LEVEL ANIMATED CAPTIONS (Lower Third)
        active_chunk = None
        for chunk in timeline:
            if chunk["chunk_start"] <= cur_sec <= chunk["chunk_end"] + 0.15:
                active_chunk = chunk
                break

        if active_chunk:
            words_info = []
            total_phrase_w = 0
            space_w = draw.textlength(" ", font=font_cap)

            for w_meta in active_chunk["words"]:
                w_str = w_meta["word"]
                is_active = w_meta["start"] <= cur_sec <= w_meta["end"]
                f_use = font_cap_act if is_active else font_cap
                w_len = draw.textlength(w_str, font=f_use)
                words_info.append((w_meta, w_str, is_active, f_use, w_len))
                total_phrase_w += w_len + space_w
            total_phrase_w -= space_w

            cap_h = 86
            pad_x = 36
            cap_w = total_phrase_w + (pad_x * 2)
            cap_x = (width - cap_w) // 2
            cap_y = 910  # Lower third

            # Frosted pillbadge
            draw.rounded_rectangle(
                [cap_x, cap_y, cap_x + cap_w, cap_y + cap_h],
                radius=24,
                fill=(8, 10, 14, 215),
                outline=(255, 255, 255, 45),
                width=2
            )

            cur_x = cap_x + pad_x
            text_baseline_y = cap_y + 14

            for w_meta, w_str, is_active, f_use, w_len in words_info:
                if is_active:
                    fill_color = (255, 60, 60, 255) if w_meta["is_red"] else (255, 225, 30, 255)
                    draw.text((cur_x + 2, text_baseline_y + 2), w_str, font=f_use, fill=(0, 0, 0, 220))
                    draw.text((cur_x, text_baseline_y), w_str, font=f_use, fill=fill_color)
                else:
                    draw.text((cur_x + 1, text_baseline_y + 1), w_str, font=f_use, fill=(0, 0, 0, 180))
                    draw.text((cur_x, text_baseline_y), w_str, font=f_use, fill=(245, 245, 245, 240))
                cur_x += w_len + space_w

        # Composite overlay onto full bleed frame
        final_frame = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
        proc.stdin.write(final_frame.tobytes())

    proc.stdin.close()
    proc.wait()

    # Copy to artifacts
    import shutil
    shutil.copy(OUTPUT_VIDEO, ARTIFACT_VIDEO)
    size_mb = round(OUTPUT_VIDEO.stat().st_size / 1024 / 1024, 2)
    print(f"\n🎉 30s MagnatesMedia Sample Render Complete!")
    print(f"   Output: {OUTPUT_VIDEO.name} ({size_mb} MB)")
    print(f"   Artifact Copied: {ARTIFACT_VIDEO.name}")
    print(f"   Visual Standard: 100% Full-Bleed + Pop-In Anchor Badges + Synchronized Captions")

if __name__ == "__main__":
    render_sample()
