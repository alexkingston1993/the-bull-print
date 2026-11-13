"""
🎬 Captioned Short Video Renderer — The Bull Print
Exact Word-by-Word Spoken Timestamp Pop-on Dynamic Subtitle Compositor.

Features:
- Reads word-level timestamps from Whisper JSON.
- Only the currently pronounced word appears on screen in the lower-third zone.
- Zero other words visible during non-speech pauses.
- High-contrast, large, mobile-optimized typography (88-96pt Impact) with 3D drop shadow and floating neon glass pill.
- Color highlights:
  * Standard words: Vivid Mint Green (#14F195)
  * Power/impact words: Electric Gold / Flame Red (#FACC15 / #FF3B30)
- Pipes frames directly into FFmpeg H.264 at constant 25 fps.
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output" / "solana_mev_short"
FRAMES_DIR = OUTPUT_DIR / "frames"

AUDIO_FILE = OUTPUT_DIR / "solana-mev-bot-siphon.mp3"
TIMESTAMPS_FILE = OUTPUT_DIR / "word_timestamps.json"
OUTPUT_CAPTIONED_MP4 = OUTPUT_DIR / "solana-mev-bot-siphon_60s_captioned.mp4"

POWER_WORDS = {
    "SOLANA", "MEMECOIN", "DOWN", "FORTY", "PERCENT", "WHALE", "DUMP",
    "MEV", "SANDWICH", "BOT", "BOTS", "BRUTAL", "MATH", "FIVE", "SLIPPAGE",
    "FRONT-RUN", "FRONT-RUNS", "VALIDATOR", "BRIBE", "PRIORITY", "INSTANTLY",
    "DUMPS", "NINETY-TWO", "THOUSAND", "WALLETS", "BLED", "DRY", "TWENTY",
    "SEARCHER", "JITO", "BUNDLES", "TELEGRAM", "COMPETE", "WRONG", "COIN",
    "BLIND", "SIPHON", "SURVIVE", "ZERO", "POINT", "PRIVATE", "RPCS",
    "FORENSIC", "ARTICLE", "EDGE", "LIQUIDATED", "TRAP", "EXPOSED"
}


def load_and_preprocess_timestamps(json_path: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        raw_words = json.load(f)

    processed = []
    for i, w in enumerate(raw_words):
        cleaned = re.sub(r"[^\w\s-]", "", w["word"]).strip().upper()
        if not cleaned:
            continue
        start = float(w["start"])
        end = float(w["end"])
        # Minimum hold time of 0.22s for human visual perception
        next_start = float(raw_words[i + 1]["start"]) if i + 1 < len(raw_words) else end + 1.0
        effective_end = min(next_start, max(end, start + 0.22))
        
        is_power = cleaned in POWER_WORDS
        processed.append({
            "word": cleaned,
            "start": start,
            "end": effective_end,
            "is_power": is_power
        })
    return processed


def render_captioned_video():
    logger.info("🚀 Starting Word-by-Word Dynamic Captioned Short Render...")
    
    words_data = load_and_preprocess_timestamps(TIMESTAMPS_FILE)
    logger.info(f"Loaded {len(words_data)} timed words.")

    # Load 10 background frames into memory
    frame_files = sorted(FRAMES_DIR.glob("frame_*.jpg"))
    if not frame_files or len(frame_files) < 10:
        raise RuntimeError(f"Expected 10 frames in {FRAMES_DIR}, found {len(frame_files)}")

    backgrounds = []
    for ff in frame_files:
        im = Image.open(ff).convert("RGB")
        if im.size != (1080, 1920):
            im = im.resize((1080, 1920), Image.Resampling.LANCZOS)
        backgrounds.append(im)
    logger.info("Loaded and normalized all 10 background frames.")

    # Setup fonts
    font_path = "/System/Library/Fonts/Supplemental/Impact.ttf"
    if not os.path.exists(font_path):
        font_path = "/Library/Fonts/Arial.ttf"
    
    font_normal = ImageFont.truetype(font_path, 88)
    font_power = ImageFont.truetype(font_path, 98)

    fps = 25
    total_duration = 59.76
    total_frames = int(total_duration * fps)  # 1494 frames
    sec_per_bg = total_duration / len(backgrounds)

    # Initialize FFmpeg pipeline
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", "1080x1920",
        "-r", str(fps),
        "-i", "-",
        "-i", str(AUDIO_FILE),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "17",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-shortest",
        str(OUTPUT_CAPTIONED_MP4)
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    logger.info(f"Rendering {total_frames} frames via FFmpeg rawvideo pipe...")

    # Pre-render word cache to avoid recomputing fonts/pill on consecutive frames
    word_cache = {}

    def get_word_overlay(word_text: str, is_power: bool) -> Image.Image:
        cache_key = (word_text, is_power)
        if cache_key in word_cache:
            return word_cache[cache_key]

        font = font_power if is_power else font_normal
        dummy = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(dummy)
        bbox = draw.textbbox((0, 0), word_text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        cx = 1080 // 2
        cy = 1530

        px = cx - tw // 2
        py = cy - th // 2

        pad_x = 42 if is_power else 36
        pad_y = 18 if is_power else 16
        pill_box = [(px - pad_x, py - pad_y), (px + tw + pad_x, py + th + pad_y)]

        overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        
        # 1. Glow
        border_col = (250, 204, 21) if is_power else (20, 241, 149)
        glow_col = (*border_col, 130)
        gdraw = ImageDraw.Draw(overlay)
        gdraw.rounded_rectangle(
            [(px - pad_x - 8, py - pad_y - 8), (px + tw + pad_x + 8, py + th + pad_y + 8)],
            radius=26,
            fill=glow_col
        )
        overlay = overlay.filter(ImageFilter.GaussianBlur(10))

        # 2. Pill body
        pdraw = ImageDraw.Draw(overlay)
        pdraw.rounded_rectangle(
            pill_box,
            radius=22,
            fill=(6, 10, 18, 235),
            outline=(*border_col, 255),
            width=4 if is_power else 3
        )

        # 3. 3D Drop shadow on text
        for d in range(5, 0, -1):
            pdraw.text((px + d, py + d), word_text, font=font, fill=(0, 0, 0, 240))

        # 4. Text foreground
        text_fill = (255, 235, 120, 255) if is_power else (255, 255, 255, 255)
        pdraw.text((px, py), word_text, font=font, fill=text_fill)

        word_cache[cache_key] = overlay
        return overlay

    for frame_idx in range(total_frames):
        t = frame_idx / float(fps)
        bg_idx = min(len(backgrounds) - 1, int(t / sec_per_bg))
        
        # Base frame copy
        canvas = backgrounds[bg_idx].copy()
        cdraw = ImageDraw.Draw(canvas)

        # Find active word at timestamp t
        active_word_item = None
        for w in words_data:
            if w["start"] <= t < w["end"]:
                active_word_item = w
                break

        if active_word_item:
            # Composite word pill
            overlay = get_word_overlay(active_word_item["word"], active_word_item["is_power"])
            canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
            cdraw = ImageDraw.Draw(canvas)

        # Animated bottom progress bar
        bar_w = int((t / total_duration) * 1080)
        cdraw.rectangle([(0, 1894), (1080, 1902)], fill=(20, 241, 149, 70))
        cdraw.rectangle([(0, 1894), (bar_w, 1902)], fill=(20, 241, 149, 255))

        # Stream raw RGB bytes to ffmpeg
        proc.stdin.write(canvas.tobytes())

        if frame_idx % 200 == 0 or frame_idx == total_frames - 1:
            pct = (frame_idx / total_frames) * 100
            logger.info(f"Progress: {frame_idx}/{total_frames} frames ({pct:.1f}%) | Time: {t:.2f}s | Word: {active_word_item['word'] if active_word_item else '-'}")

    proc.stdin.close()
    stderr = proc.stderr.read().decode()
    proc.wait()

    if proc.returncode != 0:
        logger.error(f"FFmpeg error: {stderr}")
        raise RuntimeError("FFmpeg encoding failed.")

    logger.success(f"🎉 Captioned Video Rendered Successfully: {OUTPUT_CAPTIONED_MP4} ({OUTPUT_CAPTIONED_MP4.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    render_captioned_video()
