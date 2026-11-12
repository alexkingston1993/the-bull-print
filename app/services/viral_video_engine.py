"""
Viral Video Engine (app/services/viral_video_engine.py)
Unified Production Standard for High-CTR YouTube Shorts & Standard Videos.

Enforces:
1. Strict Segmentation Standards:
   - Shorts (9:16, 1080x1920): 1 high-CTR frame every 3 seconds (e.g., 30s = 10 frames, 36s = 12 frames, 60s = 20 frames).
   - Standard YouTube Videos (16:9, 2560x1440 2K Master): 1 high-CTR frame every 4 seconds, regardless of length (e.g., 12 min = 180 frames).

2. Google Flow AI 5-Part Prompt Blueprint:
   [Format & Aspect Ratio] + [Core Subject & Metaphor] + [Lighting & Color Strategy] + [Typography & Text Overlay] + [Composition & Finish]
   - Single dramatic visual focal point (physical/mechanical metaphor).
   - Extreme contrast (dark obsidian/black background + vibrant neon accents).
   - Concise 2-4 word bold 3D text hooks.
   - STRICT NON-REUSE: Never re-use existing frames across Shorts or Standard videos.

3. Frame-Accurate Word Captions:
   - Synchronized with speech audio using Whisper word-level timestamps.
   - Dynamic pop-on: ONLY the actively pronounced word appears on screen.
   - Zero words during voiceover pauses.
   - High-contrast, large-format typography in a floating obsidian glass pill with neon border.
   - CPU-native streaming via rawvideo pipe (zero external libass/drawtext dependencies).
"""

import os
import sys
import json
import math
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class VideoFormatConfig:
    """Calculates segmentation and visual geometry for any requested duration and format."""

    @staticmethod
    def get_rules(duration_seconds: float, is_short: bool = True) -> Dict[str, Any]:
        if is_short:
            width, height = 1080, 1920
            aspect_ratio = "9:16"
            frame_interval = 3.0
            num_frames = max(1, int(math.ceil(duration_seconds / 3.0)))
            standard_name = "SHORT_VERTICAL"
            
            caption_font_size = 92
            caption_y = 1530
            pill_padding_x = 36
            pill_padding_y = 18
            border_radius = 24
        else:
            width, height = 2560, 1440
            aspect_ratio = "16:9"
            frame_interval = 4.0
            num_frames = max(1, int(math.ceil(duration_seconds / 4.0)))
            standard_name = "STANDARD_LANDSCAPE"

            caption_font_size = 80
            caption_y = 1180
            pill_padding_x = 48
            pill_padding_y = 20
            border_radius = 20

        return {
            "standard_name": standard_name,
            "is_short": is_short,
            "width": width,
            "height": height,
            "aspect_ratio": aspect_ratio,
            "frame_interval": frame_interval,
            "expected_frames": num_frames,
            "caption_font_size": caption_font_size,
            "caption_y": caption_y,
            "pill_padding_x": pill_padding_x,
            "pill_padding_y": pill_padding_y,
            "border_radius": border_radius,
        }


def extract_word_timestamps(audio_path: str, cache_json_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Extracts word-level timestamps with start and end times in seconds using faster-whisper.
    Returns list of dicts: [{"word": "SOLANA", "start": 0.12, "end": 0.48}, ...]
    """
    if cache_json_path and os.path.exists(cache_json_path):
        try:
            with open(cache_json_path, "r") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    logger.info(f"Loaded {len(data)} cached word timestamps from {cache_json_path}")
                    return data
        except Exception as e:
            logger.warning(f"Failed to read timestamp cache: {e}")

    logger.info(f"Transcribing audio with Whisper for word-level timestamps: {audio_path}")
    from faster_whisper import WhisperModel
    model = WhisperModel("base.en", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_path, word_timestamps=True)

    words = []
    for seg in segments:
        if seg.words:
            for w in seg.words:
                cleaned_word = w.word.strip().upper()
                if cleaned_word:
                    words.append({
                        "word": cleaned_word,
                        "start": round(w.start, 3),
                        "end": round(w.end, 3),
                    })

    if cache_json_path:
        os.makedirs(os.path.dirname(os.path.abspath(cache_json_path)), exist_ok=True)
        with open(cache_json_path, "w") as f:
            json.dump(words, f, indent=2)
        logger.info(f"Saved {len(words)} word timestamps to {cache_json_path}")

    return words


def get_audio_duration(audio_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())


def render_captioned_stream(
    frame_paths: List[str],
    audio_path: str,
    words: List[Dict[str, Any]],
    output_path: str,
    is_short: bool = True,
    fps: int = 25,
) -> str:
    """
    Assembles video frames and dynamically overlays active spoken-word captions
    synchronized to speech timestamps.
    Streams directly to FFmpeg rawvideo pipe for universal compatibility.
    """
    total_duration = get_audio_duration(audio_path)
    rules = VideoFormatConfig.get_rules(total_duration, is_short=is_short)
    w_out, h_out = rules["width"], rules["height"]
    total_frames = int(math.ceil(total_duration * fps))

    logger.info(f"Rendering {rules['standard_name']}: {w_out}x{h_out} @ {fps}fps ({total_duration:.2f}s, {total_frames} frames)")
    logger.info(f"Loaded {len(frame_paths)} background frames. Segmentation interval: {rules['frame_interval']}s")

    # Pre-load and resize background frames to target resolution
    loaded_frames = []
    for fp in frame_paths:
        im = Image.open(fp).convert("RGB")
        if im.size != (w_out, h_out):
            im = im.resize((w_out, h_out), Image.Resampling.LANCZOS)
        loaded_frames.append(im)

    if not loaded_frames:
        raise ValueError("No valid background frames provided!")

    # Load high-contrast display font
    font_size = rules["caption_font_size"]
    font_candidates = [
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
        str(BASE_DIR / "assets" / "fonts" / "Inter-Bold.ttf"),
    ]
    font = None
    for cand in font_candidates:
        if os.path.exists(cand):
            try:
                font = ImageFont.truetype(cand, font_size)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()

    # Pre-render caption pill overlays for unique words
    power_keywords = {
        "SOLANA", "BOT", "MEV", "SANDWICH", "SLIPPAGE", "LOSS", "FORTY", "PERCENT",
        "LIQUIDITY", "JITO", "TIP", "EXTRACTED", "CARTEL", "DRAIN", "BLEED", "TRAP",
        "WHALE", "DUMP", "FRONT-RUNS", "PRIVATE", "RPC", "PROTECTED", "TRADERS", "PROFIT"
    }

    cache_pill: Dict[str, Tuple[Image.Image, int, int]] = {}
    for item in words:
        raw_word = item["word"]
        if raw_word in cache_pill:
            continue
        
        display_word = raw_word
        bbox = font.getbbox(display_word)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        px = rules["pill_padding_x"]
        py = rules["pill_padding_y"]
        pill_w = text_w + px * 2
        pill_h = text_h + py * 2

        # Create transparent pill layer
        pill = Image.new("RGBA", (pill_w, pill_h), (0, 0, 0, 0))
        pdraw = ImageDraw.Draw(pill)

        is_power = any(pk in display_word for pk in power_keywords)
        border_color = (250, 204, 21, 230) if is_power else (20, 241, 149, 230) # Gold or Mint
        glow_color = (250, 204, 21, 60) if is_power else (20, 241, 149, 60)
        bg_fill = (5, 8, 15, 220) # Obsidian glass

        # Outer glow border
        pdraw.rounded_rectangle([0, 0, pill_w - 1, pill_h - 1], radius=rules["border_radius"], fill=bg_fill, outline=glow_color, width=3)
        # Inner sharp border
        pdraw.rounded_rectangle([2, 2, pill_w - 3, pill_h - 3], radius=rules["border_radius"] - 2, outline=border_color, width=2)

        # Drop shadow for text
        tx = px - bbox[0]
        ty = py - bbox[1]
        pdraw.text((tx + 3, ty + 3), display_word, font=font, fill=(0, 0, 0, 220))
        # Foreground text
        text_color = (255, 255, 255, 255) if not is_power else (255, 240, 150, 255)
        pdraw.text((tx, ty), display_word, font=font, fill=text_color)

        cache_pill[raw_word] = (pill, pill_w, pill_h)

    # Launch FFmpeg rawvideo pipe
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    temp_mp4 = output_path + ".tmp.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{w_out}x{h_out}",
        "-r", str(fps),
        "-i", "-", # Pipe input
        "-i", audio_path,
        "-c:v", "libx264",
        "-profile:v", "high",
        "-level", "4.2",
        "-pix_fmt", "yuv420p", # Universal compatibility
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        temp_mp4
    ]

    pipe_proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    try:
        for f_idx in range(total_frames):
            cur_time = f_idx / fps

            # Select background frame based on segmentation interval
            frame_idx = min(int(cur_time // rules["frame_interval"]), len(loaded_frames) - 1)
            frame_img = loaded_frames[frame_idx].copy()

            # Find actively spoken word (strictly active - disappears during pauses)
            active_word = None
            for w in words:
                if w["start"] <= cur_time <= w["end"]:
                    active_word = w["word"]
                    break

            if active_word and active_word in cache_pill:
                pill, pill_w, pill_h = cache_pill[active_word]
                paste_x = (w_out - pill_w) // 2
                paste_y = rules["caption_y"]
                frame_img.paste(pill, (paste_x, paste_y), pill)

            # Write raw bytes to ffmpeg
            pipe_proc.stdin.write(frame_img.tobytes())

        pipe_proc.stdin.close()
        stderr_out = pipe_proc.stderr.read()
        pipe_proc.wait()

        if pipe_proc.returncode != 0:
            raise RuntimeError(f"FFmpeg pipeline failed with code {pipe_proc.returncode}: {stderr_out.decode('utf-8', errors='ignore')}")

        if os.path.exists(output_path):
            os.remove(output_path)
        os.rename(temp_mp4, output_path)

        logger.success(f"✓ Successfully rendered captioned video: {output_path} ({os.path.getsize(output_path) / (1024*1024):.2f} MB)")
        return output_path

    except Exception as e:
        if pipe_proc.poll() is None:
            pipe_proc.kill()
        if os.path.exists(temp_mp4):
            os.remove(temp_mp4)
        raise e
