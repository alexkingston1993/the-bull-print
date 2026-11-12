#!/usr/bin/env python3
"""
Full Visual Engine Renderer for Master Documentaries (16:9 Widescreen, 1920x1080)
Applies the complete signature production standard:
- 3D Extruded Perspective Typography (0.22 forward italic shear, 16px extrusion shadow, neon bloom)
- High-Contrast Stabilo Tactical Highlighter Badges
- Lower-Third Word-Level Animated Captions with glowing active word highlight
- Slow camera dolly drift (1.00 -> 1.05)
- Atmospheric cinematic vignette
- ChristopherNeural VO + 10% BGM bed (-18 LUFS)
"""

import os
import sys
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.magnates_visual_studio import draw_sliding_word_caption
W, H = 1920, 1080
FPS = 25

font_impact = "/System/Library/Fonts/Supplemental/Impact.ttf"
font_arial_bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

def load_and_prep_plate(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGB")
    scale = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    left = (im.width - W) // 2
    top = (im.height - H) // 2
    return im.crop((left, top, left + W, top + H))

def get_audio_duration(path: Path) -> float:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    return float(subprocess.check_output(cmd).decode().strip())

def render_segment_with_visual_engine(
    seg_data: dict,
    audio_path: Path,
    bgm_path: Path,
    frames_dir: Path,
    output_mp4: Path,
    seg_idx: int
):
    target_dur = get_audio_duration(audio_path)
    total_frames = int(target_dur * FPS)
    beats = seg_data["beats"]
    n_beats = len(beats)

    # Preload plates for all beats in this segment
    plates = []
    for b in beats:
        b_num = b["beat_num"]
        p_path = frames_dir / f"seg_{seg_idx:02d}_beat_{b_num}.jpg"
        if not p_path.exists():
            raise FileNotFoundError(f"CRITICAL: Bespoke frame missing: {p_path}. Frame recycling is strictly prohibited.")
        plates.append(load_and_prep_plate(p_path))

    # Parse voiceover words for animated caption chunks (3-5 words each)
    vo_text = seg_data.get("voiceover", "")
    all_words = vo_text.split() if vo_text else []
    
    caption_chunks = []
    chunk_size = 4
    if all_words:
        n_chunks = math.ceil(len(all_words) / chunk_size)
        dur_per_chunk = target_dur / n_chunks
        for i in range(0, len(all_words), chunk_size):
            c_words = all_words[i:i + chunk_size]
            c_idx = i // chunk_size
            c_start = c_idx * dur_per_chunk
            c_end = (c_idx + 1) * dur_per_chunk
            caption_chunks.append((c_start, c_end, c_words))

    raw_mp4 = output_mp4.parent / f"raw_seg_{seg_idx:02d}.mp4"
    ff_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(raw_mp4)
    ]
    proc = subprocess.Popen(ff_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for f_idx in range(total_frames):
        t = f_idx / FPS

        # Determine active beat
        beat_dur = target_dur / n_beats
        b_idx = min(n_beats - 1, int(t / beat_dur))
        active_beat = beats[b_idx]
        beat_t = t - (b_idx * beat_dur)
        beat_progress = beat_t / beat_dur

        # 1. Camera Slow Dolly / Zoom (1.00 -> 1.05)
        zoom = 1.0 + 0.05 * beat_progress
        base_im = plates[b_idx]
        zw, zh = int(W * zoom), int(H * zoom)
        zoomed = base_im.resize((zw, zh), Image.Resampling.BILINEAR)
        zx = (zw - W) // 2
        zy = (zh - H) // 2
        frame = zoomed.crop((zx, zy, zx + W, zy + H)).convert("RGBA")

        # 2. Dark Atmospheric Vignette
        vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d_vig = ImageDraw.Draw(vignette)
        for y in range(350):
            alpha = int(180 * (1.0 - y / 350.0) ** 1.3)
            d_vig.line([(0, y), (W, y)], fill=(5, 5, 10, alpha))
        for y in range(H - 350, H):
            factor = (y - (H - 350)) / 350.0
            alpha = int(210 * (factor ** 1.2))
            d_vig.line([(0, y), (W, y)], fill=(0, 0, 5, alpha))
        frame = Image.alpha_composite(frame, vignette)

        # 3. Kinetic 3D Typography & Tactical Badge (Elastic slam over 0.35s)
        slam_dur = 0.35
        if beat_t < slam_dur:
            p_slam = beat_t / slam_dur
            scale_anim = 1.0 + 0.30 * ((1.0 - p_slam) ** 2) * math.cos(p_slam * math.pi * 2.5)
            alpha_anim = min(255, int(255 * (p_slam * 2.5)))
        else:
            scale_anim = 1.0
            alpha_anim = 255

        text_layer = Image.new("RGBA", (1300, 500), (0, 0, 0, 0))
        d_t = ImageDraw.Draw(text_layer)

        f_size = int(105 * scale_anim)
        f_hero = ImageFont.truetype(font_impact, f_size)
        f_badge = ImageFont.truetype(font_impact, int(36 * scale_anim))

        # Text & Badge definition
        anchor_text = active_beat.get("anchor_text", "MARKET REPORT").upper()
        # Split into 2 lines if longer than 16 chars
        if len(anchor_text) > 16 and " " in anchor_text:
            words_a = anchor_text.split()
            mid = len(words_a) // 2
            lines = [" ".join(words_a[:mid]), " ".join(words_a[mid:])]
        else:
            lines = [anchor_text]

        badge_text = active_beat.get("badge_text", "INTELLIGENCE REPORT").upper()
        badge_bg = (245, 25, 55)   # Crimson
        badge_fg = (255, 255, 255)
        col_face = (255, 215, 0)   # Saffron Gold
        col_bloom = (255, 180, 20)

        # Badge
        b_len = int(d_t.textlength(badge_text, font=f_badge))
        b_pad_x = 24
        b_h = int(54 * scale_anim)
        b_w = b_len + (b_pad_x * 2)
        b_y = 10
        d_t.rounded_rectangle([30, b_y, 30 + b_w, b_y + b_h], radius=10, fill=(0, 0, 0, int(alpha_anim * 0.8)))
        d_t.rounded_rectangle([30, b_y, 30 + b_w, b_y + b_h], radius=8, fill=badge_bg + (alpha_anim,))
        d_t.text((30 + b_pad_x, b_y + 8), badge_text, font=f_badge, fill=badge_fg + (alpha_anim,))

        # 3D Extruded Text with 16px extrusion
        curr_y = b_y + b_h + 18
        line_spacing = int(f_size * 0.95)
        for line in lines:
            for d in range(16, 0, -2):
                shade = int(50 * (1.0 - d / 16.0))
                d_t.text((30 + d, curr_y + d), line, font=f_hero, fill=(shade, shade // 2, 0, int(alpha_anim * 0.9)), stroke_width=6, stroke_fill=(0, 0, 0, int(alpha_anim * 0.9)))
            d_t.text((30, curr_y), line, font=f_hero, fill=col_face + (alpha_anim,), stroke_width=4, stroke_fill=(15, 0, 5, alpha_anim))
            curr_y += line_spacing

        # Shear Affine Transform (0.22 forward italic)
        shear = 0.22
        m = [1, -shear, 0, 0, 1, 0]
        slanted_text = text_layer.transform((1300 + 120, 500), Image.Transform.AFFINE, m, resample=Image.Resampling.BILINEAR)

        # Volumetric Neon Bloom
        alpha_ch = slanted_text.split()[3]
        bloom_mask = alpha_ch.filter(ImageFilter.GaussianBlur(28))
        bloom_layer = Image.new("RGBA", slanted_text.size, col_bloom + (0,))
        bloom_layer.putalpha(bloom_mask)

        # Composite onto frame
        pos_x, pos_y = 100, 140
        frame.alpha_composite(bloom_layer, (pos_x, pos_y))
        frame.alpha_composite(slanted_text, (pos_x, pos_y))

        # 4. Lower-Third Word-Level Animated Caption Pill (Safe Zone: Y = 920 with 2-line auto-wrap)
        active_chunk = None
        for c_start, c_end, c_words in caption_chunks:
            if c_start <= t <= c_end:
                active_chunk = (c_start, c_end, c_words)
                break

        if active_chunk:
            c_start, c_end, c_words = active_chunk
            n_cw = len(c_words)
            c_dur = c_end - c_start
            w_idx = int(((t - c_start) / max(0.01, c_dur)) * n_cw)
            w_idx = max(0, min(n_cw - 1, w_idx))
            active_w = c_words[w_idx]

            draw_sliding_word_caption(
                frame=frame,
                caption_text=c_words,
                active_word=active_w,
                font_path=font_arial_bold,
                y=920
            )

        proc.stdin.write(frame.convert("RGB").tobytes())

    proc.stdin.close()
    proc.wait()

    # Mux with ChristopherNeural VO + 10% BGM bed (-18 LUFS)
    bgm_offset = ((seg_idx - 1) % 7) * 19.5
    af = (
        f"[1:a]apad=pad_dur={target_dur}[vo_d];"
        f"[2:a]atrim=start={bgm_offset}:end={bgm_offset + target_dur},asetpts=PTS-STARTPTS,volume=0.10[bgm_d];"
        f"[vo_d][bgm_d]amix=inputs=2:duration=first[aout]"
    )
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", str(raw_mp4),
        "-i", str(audio_path),
        "-i", str(bgm_path),
        "-filter_complex", af,
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_mp4)
    ]
    subprocess.run(cmd_mux, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    raw_mp4.unlink(missing_ok=True)
    print(f"  🎬 Rendered Segment {seg_idx:02d} ({target_dur:.2f}s) with full 3D visual engine!")

if __name__ == "__main__":
    print("Master Documentary Visual Engine module loaded successfully.")
