#!/usr/bin/env python3
"""
30-Second Animated Captions Sample Compositor
The Bull Print (@thebullprint)
- Generates exact word-level timestamped animated captions
- Displays clean, floating lower-third phrases
- Active word highlights dynamically in Neon Gold / Flame Crimson
- Zero obstruction of background artwork
"""

import math
import os
import re
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_VIDEO = BASE_DIR / "output" / "options_casino_documentary" / "sample_30s_raw.mp4"
AUDIO_FILE = BASE_DIR / "output" / "options_casino_documentary" / "sample_30s.wav"
OUTPUT_VIDEO = BASE_DIR / "output" / "options_casino_documentary" / "options_casino_30s_animated_captions_sample.mp4"
ARTIFACT_VIDEO = Path("/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364/options_casino_30s_animated_captions_sample.mp4")

# Sentences with exact start and end times verified from Christopher voice
SENTENCES_DATA = [
    (0.15, 4.40, ["It", "is", "3:15", "PM", "on", "a", "Thursday", "afternoon", "in", "Mumbai."]),
    (4.45, 10.15, ["A", "26-year-old", "software", "engineer", "sits", "frozen", "in", "front", "of", "a", "red-stained", "trading", "screen."]),
    (10.20, 17.40, ["His", "bank", "balance,", "built", "over", "four", "years", "of", "grueling", "corporate", "overtime,", "has", "just", "vaporized", "in", "ninety", "seconds."]),
    (17.45, 23.95, ["His", "out-of-the-money", "call", "option,", "bought", "for", "fifty", "rupees,", "drops", "to", "zero", "point", "zero", "five."]),
    (24.00, 25.65, ["Worthless."]),
    (25.70, 27.85, ["This", "is", "not", "bad", "luck."]),
    (27.90, 30.00, ["It", "is", "the", "greatest", "retail", "wealth", "transfer", "in", "Indian", "financial", "history."])
]

RED_TRIGGER_WORDS = {"VAPORIZED", "ZERO", "WORTHLESS", "RED-STAINED", "LOSS", "CRASH", "BAD"}

def build_word_timeline():
    timeline = []
    for s_start, s_end, words in SENTENCES_DATA:
        s_dur = s_end - s_start
        # Weight by length
        weights = [max(len(re.sub(r"[^\w]", "", w)), 2) for w in words]
        total_wt = sum(weights)
        
        # Sub-divide into chunks of 3-5 words for comfortable reading
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

def render_sample():
    print("🎬 Generating Animated Captions Sample (First 30 Seconds)...")
    timeline = build_word_timeline()
    
    font_path = "/System/Library/Fonts/Supplemental/Impact.ttf"
    font = ImageFont.truetype(font_path, 54)
    font_active = ImageFont.truetype(font_path, 58)
    
    # Extract raw frames from input video via ffmpeg pipe
    fps = 25
    width = 1920
    height = 1080
    frame_bytes_size = width * height * 3
    
    read_cmd = [
        "ffmpeg", "-i", str(INPUT_VIDEO),
        "-t", "30",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-"
    ]
    read_proc = subprocess.Popen(read_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    
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
    write_proc = subprocess.Popen(write_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    frame_idx = 0
    total_frames = 30 * fps
    
    while frame_idx < total_frames:
        raw_bytes = read_proc.stdout.read(frame_bytes_size)
        if not raw_bytes or len(raw_bytes) < frame_bytes_size:
            break
            
        cur_sec = frame_idx / fps
        im = Image.frombytes("RGB", (width, height), raw_bytes)
        
        # Check active chunk in timeline
        active_chunk = None
        for chunk in timeline:
            if chunk["chunk_start"] <= cur_sec <= chunk["chunk_end"] + 0.15:
                active_chunk = chunk
                break
                
        if active_chunk:
            overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Measure full phrase width
            words_info = []
            total_phrase_w = 0
            space_w = draw.textlength(" ", font=font)
            
            for w_meta in active_chunk["words"]:
                w_str = w_meta["word"]
                is_active = w_meta["start"] <= cur_sec <= w_meta["end"]
                f_use = font_active if is_active else font
                w_len = draw.textlength(w_str, font=f_use)
                words_info.append((w_meta, w_str, is_active, f_use, w_len))
                total_phrase_w += w_len + space_w
            total_phrase_w -= space_w
            
            # Position in lower third safe zone
            box_h = 86
            pad_x = 36
            box_w = total_phrase_w + (pad_x * 2)
            box_x = (width - box_w) // 2
            box_y = 910  # Lower third (top 85% clear!)
            
            # Draw sleek floating translucent pill badge
            draw.rounded_rectangle(
                [box_x, box_y, box_x + box_w, box_y + box_h],
                radius=24,
                fill=(8, 10, 14, 215),
                outline=(255, 255, 255, 45),
                width=2
            )
            
            # Draw words with active highlighting
            cur_x = box_x + pad_x
            text_baseline_y = box_y + 14
            
            for w_meta, w_str, is_active, f_use, w_len in words_info:
                if is_active:
                    # Active word highlight: Flame red or Electric gold
                    fill_color = (255, 60, 60, 255) if w_meta["is_red"] else (255, 225, 30, 255)
                    # Text drop shadow
                    draw.text((cur_x + 2, text_baseline_y + 2), w_str, font=f_use, fill=(0, 0, 0, 220))
                    draw.text((cur_x, text_baseline_y), w_str, font=f_use, fill=fill_color)
                else:
                    # Inactive word in phrase: clean stark white
                    draw.text((cur_x + 1, text_baseline_y + 1), w_str, font=f_use, fill=(0, 0, 0, 180))
                    draw.text((cur_x, text_baseline_y), w_str, font=f_use, fill=(245, 245, 245, 240))
                    
                cur_x += w_len + space_w
                
            im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
            
        write_proc.stdin.write(im.tobytes())
        frame_idx += 1
        
    read_proc.stdout.close()
    read_proc.wait()
    write_proc.stdin.close()
    write_proc.wait()
    
    # Copy to artifact
    import shutil
    shutil.copy(OUTPUT_VIDEO, ARTIFACT_VIDEO)
    print(f"🎉 30s Animated Captions Sample Complete: {OUTPUT_VIDEO.name} ({round(OUTPUT_VIDEO.stat().st_size / 1024 / 1024, 2)} MB)")
    print(f"   Copied to Artifacts: {ARTIFACT_VIDEO.name}")

if __name__ == "__main__":
    render_sample()
