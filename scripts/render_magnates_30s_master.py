#!/usr/bin/env python3
"""
scripts/render_magnates_30s_master.py
The Bull Print — 30-Second Authentic MagnatesMedia Documentary Engine.

Directives:
1. Exactly 30.0 seconds duration (900 frames @ 30 FPS).
2. Zero UI cards, zero slide decks, 100% full-bleed documentary cinematography.
3. Asymmetric kinetic typography with multi-layer drop shadows and glowing emphasis words.
4. Continuous Ken Burns creeping zooms, directional drift, and 2.35:1 cinematic letterbox bars.
5. Sound design: sub-bass braam drops, tension drone, and cinematic whoosh transients.
6. Automated VisualQACritic verification gate.
"""

import math
import os
import shutil
import subprocess
import sys
import wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.visual_qa_critic import VisualQACritic

OUTPUT_DIR = BASE_DIR / "output" / "magnates_30s"
FRAMES_DIR = OUTPUT_DIR / "frames"
AUDIO_DIR = OUTPUT_DIR / "audio"
SFX_DIR = OUTPUT_DIR / "sfx"
TEMP_SEGMENTS_DIR = OUTPUT_DIR / "temp_segments"

for d in [OUTPUT_DIR, FRAMES_DIR, AUDIO_DIR, SFX_DIR, TEMP_SEGMENTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FPS = 30
TOTAL_DURATION = 30.0

# 5 Freshly Generated 16:9 8K Documentary Scenes
SCENE_IMAGES = {
    1: Path("/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/magnates_bank_skyscraper_1793373161483.jpg"),
    2: Path("/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/magnates_trading_floor_1793373202602.jpg"),
    3: Path("/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/magnates_vault_trap_1793373236816.jpg"),
    4: Path("/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/magnates_quant_dump_1793373331514.jpg"),
    5: Path("/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/magnates_bull_hq_1793373359564.jpg"),
}

VOICEOVER_PATH = AUDIO_DIR / "voiceover_30s.mp3"

FONT_HEADING = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_MONO = "/System/Library/Fonts/Courier.dfont"
FONT_BODY = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def get_font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def apply_ken_burns(base_img: Image.Image, progress: float, zoom_start=1.0, zoom_end=1.12, pan_x=30, pan_y=15) -> Image.Image:
    """Smooth creeping camera zoom and directional drift."""
    zoom = zoom_start + (zoom_end - zoom_start) * progress
    w, h = base_img.size
    new_w = int(w * zoom)
    new_h = int(h * zoom)
    
    resized = base_img.resize((new_w, new_h), Image.Resampling.BILINEAR)
    
    offset_x = int((new_w - w) * 0.5 + pan_x * progress)
    offset_y = int((new_h - h) * 0.5 + pan_y * progress)
    
    offset_x = max(0, min(new_w - w, offset_x))
    offset_y = max(0, min(new_h - h, offset_y))
    
    return resized.crop((offset_x, offset_y, offset_x + w, offset_y + h))


def draw_cinematic_letterbox(img: Image.Image) -> Image.Image:
    """Documentary 2.35:1 matte letterbox."""
    draw = ImageDraw.Draw(img, "RGBA")
    bar_h = 56
    draw.rectangle([0, 0, WIDTH, bar_h], fill=(0, 0, 0, 255))
    draw.rectangle([0, HEIGHT - bar_h, WIDTH, HEIGHT], fill=(0, 0, 0, 255))
    return img


def draw_kinetic_typography(
    frame: Image.Image,
    eyebrow: str,
    headline: str,
    emphasis_word: str,
    subtext: str,
    accent_color: tuple = (16, 185, 129),
    position: str = "bottom-left",
    shutter_flash: float = 0.0
):
    """Pure asymmetrical kinetic typography over B-roll. Zero white cards."""
    if shutter_flash > 0:
        flash_alpha = int(180 * shutter_flash)
        flash = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, flash_alpha))
        frame = Image.alpha_composite(frame.convert("RGBA"), flash).convert("RGB")

    draw = ImageDraw.Draw(frame, "RGBA")
    
    font_eye = get_font(FONT_MONO, 22)
    font_head = get_font(FONT_HEADING, 64)
    font_emph = get_font(FONT_HEADING, 80)
    font_sub = get_font(FONT_BODY, 28)

    if position == "bottom-left":
        start_x = 100
        start_y = HEIGHT - 330
    elif position == "top-left":
        start_x = 100
        start_y = 120
    else:
        start_x = 100
        start_y = HEIGHT - 370

    # Eyebrow tag
    draw.line([(start_x, start_y + 12), (start_x + 36, start_y + 12)], fill=accent_color + (255,), width=4)
    draw.text((start_x + 50, start_y), eyebrow.upper(), font=font_eye, fill=accent_color + (255,))

    # Headline with diffuse multi-layer shadows
    head_y = start_y + 36
    for ox, oy in [(-3, -3), (3, 3), (-3, 3), (3, -3), (0, 6)]:
        draw.text((start_x + ox, head_y + oy), headline, font=font_head, fill=(0, 0, 0, 220))
    draw.text((start_x, head_y), headline, font=font_head, fill=(255, 255, 255, 255))

    # Emphasis Word (glowing accent)
    emph_y = head_y + 74
    for ox, oy in [(-4, -4), (4, 4), (-4, 4), (4, -4), (0, 8)]:
        draw.text((start_x + ox, emph_y + oy), emphasis_word, font=font_emph, fill=(0, 0, 0, 240))
    draw.text((start_x, emph_y), emphasis_word, font=font_emph, fill=accent_color + (255,))

    # Subtext
    sub_y = emph_y + 92
    for ox, oy in [(0, 3), (2, 2)]:
        draw.text((start_x + ox, sub_y + oy), subtext, font=font_sub, fill=(0, 0, 0, 220))
    draw.text((start_x, sub_y), subtext, font=font_sub, fill=(226, 232, 240, 255))

    return frame


def draw_hud_order_flow(frame: Image.Image, progress: float) -> Image.Image:
    """Asymmetrical algorithmic order flow HUD on trading monitor scene."""
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)

    font_hud_title = get_font(FONT_MONO, 20)
    font_hud_num = get_font(FONT_HEADING, 26)

    base_x = 1050
    base_y = 150
    odraw.rectangle([base_x - 20, base_y - 20, WIDTH - 80, base_y + 420], fill=(5, 10, 20, 150), outline=(239, 68, 68, 90), width=1)

    odraw.text((base_x, base_y), "INSTITUTIONAL BLOCK DISTRIBUTION // REAL-TIME", font=font_hud_title, fill=(239, 68, 68, 240))
    odraw.line([(base_x, base_y + 30), (WIDTH - 100, base_y + 30)], fill=(239, 68, 68, 120), width=1)

    lines = [
        ("FII BLOCK SELL 01", "4,500,000 SHARES", "$184.50 DUMP"),
        ("ALGO LIQUIDATION", "2,850,000 SHARES", "$183.20 DUMP"),
        ("DARK POOL ABSORPTION", "8,200,000 SHARES", "TRAP CONFIRMED"),
    ]

    curr_y = base_y + 50
    for idx, (label, vol, status) in enumerate(lines):
        if progress > (idx * 0.25):
            odraw.text((base_x, curr_y), label, font=font_hud_title, fill=(203, 213, 225, 230))
            odraw.text((base_x + 320, curr_y), vol, font=font_hud_num, fill=(248, 113, 113, 255))
            odraw.text((base_x, curr_y + 32), status, font=font_hud_title, fill=(239, 68, 68, 220))
            odraw.line([(base_x, curr_y + 60), (WIDTH - 100, curr_y + 60)], fill=(255, 255, 255, 15), width=1)
            curr_y += 75

    out = Image.alpha_composite(frame.convert("RGBA"), overlay)
    return out.convert("RGB")


def generate_sfx_tracks():
    """Synthesizes documentary sound design: braam drops and tension bed."""
    sample_rate = 44100
    
    # 1. Sub-Bass Braam
    dur = 2.2
    n = int(sample_rate * dur)
    t = np.linspace(0, dur, n)
    freq = np.linspace(85, 45, n)
    braam = 0.7 * np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t)
    env = np.exp(-t * 1.5)
    wave_data = (braam * env * 32767).astype(np.int16)
    with wave.open(str(SFX_DIR / "braam_drop.wav"), "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(wave_data.tobytes())

    # 2. Ambient Tension Drone (30 seconds)
    n_tot = int(sample_rate * TOTAL_DURATION)
    tt = np.linspace(0, TOTAL_DURATION, n_tot)
    drone = 0.18 * np.sin(2 * np.pi * 55 * tt) + 0.08 * np.sin(2 * np.pi * 110 * tt)
    drone_data = (drone * 32767).astype(np.int16)
    with wave.open(str(SFX_DIR / "tension_drone_30s.wav"), "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(drone_data.tobytes())


def render_scene(scene_id: int, start_sec: float, end_sec: float, base_img_p: Path):
    """Renders individual scene segment."""
    dur = end_sec - start_sec
    total_frames = int(dur * FPS)
    seg_output = TEMP_SEGMENTS_DIR / f"seg_{scene_id}.mp4"
    
    base_raw = Image.open(base_img_p).convert("RGB")
    if base_raw.size != (WIDTH, HEIGHT):
        base_raw = ImageOps.fit(base_raw, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)

    temp_dir = FRAMES_DIR / f"scene_{scene_id}"
    temp_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎬 Rendering Scene {scene_id} ({start_sec}s -> {end_sec}s, {total_frames} frames)...")

    for i in range(total_frames):
        p = i / max(1, total_frames - 1)

        if scene_id == 1:
            frame = apply_ken_burns(base_raw, p, zoom_start=1.0, zoom_end=1.10, pan_x=35, pan_y=20)
            frame = draw_kinetic_typography(
                frame,
                eyebrow="WALL STREET FORENSIC ARTICLE // CHAPTER 01",
                headline="THE 30-SECOND SECRET",
                emphasis_word="THE SYSTEM CONCEALS",
                subtext="What happens behind closed doors when retail buyers flood the market.",
                accent_color=(16, 185, 129),
                position="bottom-left"
            )
        elif scene_id == 2:
            frame = apply_ken_burns(base_raw, p, zoom_start=1.02, zoom_end=1.14, pan_x=-30, pan_y=25)
            frame = draw_kinetic_typography(
                frame,
                eyebrow="NYSE ORDER FLOW AUDIT // RETAIL TRAP",
                headline="ALL-TIME HIGH BREAKOUTS",
                emphasis_word="THE LIQUIDITY BAIT",
                subtext="Retail traders buy the peak, convinced they are riding the rally.",
                accent_color=(245, 158, 11),
                position="bottom-left"
            )
        elif scene_id == 3:
            # Trap reveal with shutter flash at t=1.0s (frame 30)
            shutter = 1.0 - (abs(i - 30) / 10.0) if abs(i - 30) < 10 else 0.0
            frame = apply_ken_burns(base_raw, p, zoom_start=1.0, zoom_end=1.16, pan_x=25, pan_y=35)
            frame = draw_kinetic_typography(
                frame,
                eyebrow="INSTITUTIONAL VAULT // UNSEALED EVIDENCE",
                headline="WALKING INTO THE TRAP",
                emphasis_word="SMART MONEY ABSORPTION",
                subtext="Behind the headlines, billions in exit orders are loaded silently.",
                accent_color=(239, 68, 68),
                position="top-left",
                shutter_flash=shutter
            )
        elif scene_id == 4:
            frame = apply_ken_burns(base_raw, p, zoom_start=1.0, zoom_end=1.09, pan_x=-40, pan_y=-10)
            frame = draw_hud_order_flow(frame, p)
            frame = draw_kinetic_typography(
                frame,
                eyebrow="DARK POOL EXECUTION // BLOCK DUMP",
                headline="BILLIONS IN INVENTORY",
                emphasis_word="DUMPED IN SECONDS",
                subtext="Institutional desks use retail buying volume to liquidate massive positions.",
                accent_color=(239, 68, 68),
                position="bottom-left"
            )
        elif scene_id == 5:
            frame = apply_ken_burns(base_raw, p, zoom_start=1.0, zoom_end=1.08, pan_x=30, pan_y=15)
            frame = draw_kinetic_typography(
                frame,
                eyebrow="THE BULL PRINT // FINANCIAL INVESTIGATIONS",
                headline="DECODE SMART MONEY",
                emphasis_word="STOP BEING EXIT LIQUIDITY",
                subtext="Actionable institutional alpha & market truth. bullprintmedia.com",
                accent_color=(16, 185, 129),
                position="bottom-left"
            )

        frame = draw_cinematic_letterbox(frame)
        frame.save(temp_dir / f"f_{i:04d}.jpg", quality=95)

    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(temp_dir / "f_%04d.jpg"),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(seg_output)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return seg_output


def compile_30s_master():
    print("🚀 Compiling 30-Second MagnatesMedia Masterpiece...")
    generate_sfx_tracks()

    # Exact cue points matching voiceover_30s.mp3 (28.75s audio + 1.25s room tone pad)
    segments = [
        (1, 0.0, 6.0, SCENE_IMAGES[1]),
        (2, 6.0, 12.0, SCENE_IMAGES[2]),
        (3, 12.0, 18.0, SCENE_IMAGES[3]),
        (4, 18.0, 24.5, SCENE_IMAGES[4]),
        (5, 24.5, 30.0, SCENE_IMAGES[5]),
    ]

    seg_paths = []
    for s_id, start_t, end_t, img_p in segments:
        seg_p = render_scene(s_id, start_t, end_t, img_p)
        seg_paths.append(seg_p)

    concat_file = OUTPUT_DIR / "concat_list.txt"
    with open(concat_file, "w") as f:
        for p in seg_paths:
            f.write(f"file '{p.resolve()}'\n")

    video_only = OUTPUT_DIR / "video_concat.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(video_only)], check=True)

    master_mp4 = OUTPUT_DIR / "magnates_30s_official_master.mp4"

    cmd_mix = [
        "ffmpeg", "-y",
        "-i", str(video_only),
        "-i", str(VOICEOVER_PATH),
        "-i", str(SFX_DIR / "tension_drone_30s.wav"),
        "-i", str(SFX_DIR / "braam_drop.wav"),
        "-filter_complex", (
            "[1:a]volume=1.20[vo];"
            "[2:a]volume=0.35[drone];"
            "[3:a]adelay=0|0,volume=0.75[braam0];"
            "[3:a]adelay=12000|12000,volume=0.90[braam1];"
            "[vo][drone][braam0][braam1]amix=inputs=4:duration=first:dropout_transition=2[aout]"
        ),
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", "30.0",
        str(master_mp4)
    ]
    subprocess.run(cmd_mix, check=True)
    print(f"🔥 30-SECOND MASTERPIECE COMPILED: {master_mp4}")

    # Extract 5 milestone frames for Visual QA Critic inspection & user presentation
    milestones = [
        ("magnates_30s_01_skyscraper_3s.jpg", 3.0),
        ("magnates_30s_02_trading_floor_9s.jpg", 9.0),
        ("magnates_30s_03_vault_trap_15s.jpg", 15.0),
        ("magnates_30s_04_quant_dump_21s.jpg", 21.0),
        ("magnates_30s_05_brand_outro_27s.jpg", 27.0),
    ]

    critic = VisualQACritic()
    artifact_dir = Path("/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9")

    print("\n🔍 RUNNING AUTOMATED VISUAL QA CRITIC GATE (Threshold: Static Box <= 20%)...")
    for fname, ts in milestones:
        fpath = OUTPUT_DIR / fname
        cmd_extract = [
            "ffmpeg", "-y",
            "-ss", str(ts),
            "-i", str(master_mp4),
            "-vframes", "1",
            "-q:v", "2",
            str(fpath)
        ]
        subprocess.run(cmd_extract, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        shutil.copy(fpath, artifact_dir / fname)
        report = critic.inspect_frame(fpath)
        print(f"  Frame {fname} (t={ts}s): Passed={report.passed} | Score={report.score}/100 | Static Box Ratio={report.static_box_ratio*100:.1f}%")

    shutil.copy(master_mp4, artifact_dir / "magnates_30s_official_master.mp4")
    print("\n✅ All milestone frames and master video copied to artifacts.")


if __name__ == "__main__":
    compile_30s_master()
