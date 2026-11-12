#!/usr/bin/env python3
"""
scripts/render_fii_rotation_viral_short_magnates.py
The Bull Print — Full MagnatesMedia 3D Kinetic Visual Studio Renderer for Viral Short:
Topic: "The ₹65,700 Cr FII Rotation: Why Wall Street Is Dumping Nvidia to Flood Indian Bluechips"

Signature Blueprint Compliance:
1. 20 Bespoke Kaggle GPU vertical plates (576x1024 native, upscaled full-bleed to 1080x1920)
2. Stacked 3D extruded perspective typography (forward shear 0.22, 16px extrusion shadow, Gaussian bloom r=28)
3. High-Contrast Tactical Highlighter Badges (MARKET ALERT, FII FLOOD, NVIDIA CRASH, etc.)
4. Lower-Third Word-Level Spoken Captions with active yellow word highlight in mobile safe zone (Y = 1480)
5. Smooth camera slow drift / zoom (1.00 -> 1.05)
6. ChristopherNeural voiceover + ducked ambient pulse BGM
"""

import os
import sys
import json
import math
import re
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import edge_tts
from app.services.magnates_visual_studio import precompute_cut_typography

OUTPUT_DIR = BASE_DIR / "output" / "viral_short_fii_rotation"
FRAMES_DIR = Path("/tmp/kaggle_viral_short_clean/frames")
AUDIO_FILE = OUTPUT_DIR / "narration_master.mp3"
TIMESTAMPS_FILE = OUTPUT_DIR / "word_timestamps.json"
FINAL_VIDEO = BASE_DIR / "output" / "the_fii_rotation_viral_short_master.mp4"
BGM_FILE = BASE_DIR / "assets" / "audio" / "bgm_pool" / "bed_01_subterranean_pulse.wav"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 20 Beats @ 3.0s Cadence = 60s
BEATS = [
    {
        "id": 1,
        "badge": "MARKET ALERT ⚠️",
        "lines": ["NVIDIA $159", "AFTER-HOURS CRASH"],
        "script": "In the last twenty-four hours, Wall Street suffered a massive shockwave."
    },
    {
        "id": 2,
        "badge": "BOARD INVESTIGATION",
        "lines": ["JENSEN HUANG", "UNDER SCRUTINY"],
        "script": "Nvidia shares plunged nine percent following leaked boardroom audit reports."
    },
    {
        "id": 3,
        "badge": "500B VANISH",
        "lines": ["AI BUBBLE", "LIQUIDITY DRAIN"],
        "script": "Over five hundred billion dollars in artificial intelligence value evaporated overnight."
    },
    {
        "id": 4,
        "badge": "DALAL STREET BREAKOUT",
        "lines": ["BSE SURGE", "8-MONTH HIGHS"],
        "script": "At the exact same time, Indian benchmark indices hit dramatic eight-month highs."
    },
    {
        "id": 5,
        "badge": "FOREIGN INFLOW",
        "lines": ["₹65,700 CRORE", "NOVEMBER FLOOD"],
        "script": "Foreign institutional investors pumped sixty-five thousand crore rupees into Indian blue chips."
    },
    {
        "id": 6,
        "badge": "WALL STREET RUN",
        "lines": ["ALGO SELLING", "TECH LIQUIDATION"],
        "script": "Wall Street hedge funds are aggressively dumping overheated Silicon Valley AI stocks."
    },
    {
        "id": 7,
        "badge": "MACRO ROTATION",
        "lines": ["CASH FLOW", "YIELD ARBITRAGE"],
        "script": "Capital is violently rotating from speculative software into tangible physical earnings."
    },
    {
        "id": 8,
        "badge": "EMERGING HAVEN",
        "lines": ["MUMBAI NARIMAN", "GLOBAL CAPITAL"],
        "script": "India has become global smart money's ultimate balance sheet refuge."
    },
    {
        "id": 9,
        "badge": "INSTITUTIONAL ACCUMULATION",
        "lines": ["HDFC & BAJAJ", "RECORD VOLUME"],
        "script": "Domestic heavyweights saw unprecedented foreign limit buy order absorption."
    },
    {
        "id": 10,
        "badge": "GLOBAL CONTRARIAN",
        "lines": ["EAST VS WEST", "THE SQUEEZE"],
        "script": "While Western tech indices cracked, Dalal Street absorbed every global shock."
    },
    {
        "id": 11,
        "badge": "HEDGE FUND AUDIT",
        "lines": ["OFFSHORE DESKS", "UNWINDING LEVERAGE"],
        "script": "Institutional prime brokers initiated emergency margin calls on semiconductor longs."
    },
    {
        "id": 12,
        "badge": "CHIP REALITY",
        "lines": ["FOUNDRY BOTTLENECK", "TSMC WARNING"],
        "script": "High-density compute hardware orders across Asia were quietly placed on review."
    },
    {
        "id": 13,
        "badge": "BANKING FORTRESS",
        "lines": ["CREDIT GROWTH", "EXPANDING MARGINS"],
        "script": "Indian banking balance sheets continue expanding at pristine double-digit compounding."
    },
    {
        "id": 14,
        "badge": "RETAIL EXPOSURE",
        "lines": ["CHASING PEAKS", "THE TRAP"],
        "script": "Retail traders who chased the American AI top are now trapped in deep drawdowns."
    },
    {
        "id": 15,
        "badge": "CONCENTRATION RISK",
        "lines": ["MAG 7 MONOLITH", "S&P EXPOSURE"],
        "script": "Seven mega-cap stocks carried the entire market into historic systemic fragility."
    },
    {
        "id": 16,
        "badge": "COMMODITY CUES",
        "lines": ["CRUDE $91", "INFLATION SINK"],
        "script": "Plunging Brent crude oil prices provided a massive macroeconomic tax break for India."
    },
    {
        "id": 17,
        "badge": "ORDER FLOW FOOTPRINT",
        "lines": ["LIMIT ABSORPTION", "BLOCK DEALS"],
        "script": "Foreign institutional desks executed massive block transactions before the opening bell."
    },
    {
        "id": 18,
        "badge": "VOLATILITY DIVERGENCE",
        "lines": ["VIX SPIKE", "NIFTY RESILIENCE"],
        "script": "Global volatility surged while domestic liquidity held the line with zero panic."
    },
    {
        "id": 19,
        "badge": "THE GREAT SHIFT",
        "lines": ["SMART MONEY", "NEW LEADERSHIP"],
        "script": "This is not a temporary dip; it is a generational realignment of global capital."
    },
    {
        "id": 20,
        "badge": "THE BULL PRINT VERDICT",
        "lines": ["FOLLOW THE FLOW", "SUBSCRIBE NOW"],
        "script": "Follow The Bull Print for institutional market intelligence before the crowd wakes up."
    }
]

VOICE = "en-US-ChristopherNeural"
PITCH = "-2Hz"
RATE = "+0%"

FONT_IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"
FONT_ROBOTO_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

async def synthesize_audio_and_timestamps():
    print("🎙️ Synthesizing Christopher narration & millisecond timestamps...")
    full_script = " ".join(b["script"] for b in BEATS)
    comm = edge_tts.Communicate(full_script, VOICE, pitch=PITCH, rate=RATE)

    sentences = []
    audio_bytes = bytearray()

    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio_bytes.extend(chunk["data"])
        elif chunk["type"] == "SentenceBoundary":
            start_ms = chunk["offset"] / 10000.0
            dur_ms = chunk["duration"] / 10000.0
            sentences.append({
                "text": chunk["text"],
                "start_ms": start_ms,
                "dur_ms": dur_ms,
                "end_ms": start_ms + dur_ms
            })

    with open(AUDIO_FILE, "wb") as f:
        f.write(audio_bytes)
    print(f"✓ Master audio synthesized: {AUDIO_FILE.name} ({len(audio_bytes)} bytes)")

    # Character-weighted word timestamps
    words_data = []
    for s in sentences:
        s_words = s["text"].split()
        if not s_words:
            continue
        weights = [max(len(re.sub(r'[^\w]', '', w)), 2) + (3 if w.endswith(',') else (4 if w.endswith('.') else 0)) for w in s_words]
        tot = sum(weights)
        curr = s["start_ms"]
        for idx, w in enumerate(s_words):
            dur = (weights[idx] / tot) * s["dur_ms"]
            words_data.append({
                "word": w.upper(),
                "clean": re.sub(r'[^\w]', '', w).upper(),
                "start": round(curr / 1000.0, 3),
                "end": round((curr + dur) / 1000.0, 3)
            })
            curr += dur

    with open(TIMESTAMPS_FILE, "w") as f:
        json.dump(words_data, f, indent=2)
    print(f"✓ Extracted {len(words_data)} word-level timestamps")
    return words_data

def get_audio_dur(path: Path) -> float:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    return float(subprocess.check_output(cmd).decode().strip())

def render_magnates_short():
    total_dur = get_audio_dur(AUDIO_FILE)
    fps = 25
    total_frames = int(math.ceil(total_dur * fps))
    n_beats = len(BEATS)
    beat_dur = total_dur / n_beats
    w_out, h_out = 1080, 1920

    print(f"🎬 Rendering full Magnates 3D Visual Studio Short ({total_dur:.1f}s, {total_frames} frames)...")

    with open(TIMESTAMPS_FILE) as f:
        words = json.load(f)

    # Pre-load the 20 clean Kaggle vertical plates
    plates = []
    for i in range(1, 21):
        p_file = FRAMES_DIR / f"segment_{i:02d}.jpg"
        if not p_file.exists():
            p_file = FRAMES_DIR / f"segment_{i}.jpg"
        im = Image.open(p_file).convert("RGB")
        # Upscale clean plate full-bleed to 1080x1920
        scale = max(w_out / im.width, h_out / im.height)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
        left = (im.width - w_out) // 2
        top = (im.height - h_out) // 2
        plates.append(im.crop((left, top, left + w_out, top + h_out)))

    # Pre-compute 3D Kinetic Typography for each of the 20 beats
    typo_cache = []
    for b in BEATS:
        t_data = precompute_cut_typography(
            lines=b["lines"],
            badge_text=b["badge"],
            font_path=FONT_IMPACT,
            max_sheared_w=int(w_out * 0.78),
            face_color=(255, 215, 0),       # Saffron Gold
            badge_bg=(245, 25, 55)          # Crimson
        )
        typo_cache.append(t_data)

    font_caption = ImageFont.truetype(FONT_ROBOTO_BOLD, 52)

    # Launch FFmpeg Rawvideo Pipe
    raw_mp4 = OUTPUT_DIR / "raw_video.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{w_out}x{h_out}",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        str(raw_mp4)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for f_idx in range(total_frames):
        t = f_idx / fps
        b_idx = min(n_beats - 1, int(t / beat_dur))
        beat = BEATS[b_idx]
        b_t = t - (b_idx * beat_dur)
        p_beat = b_t / beat_dur

        # 1. Camera Slow Zoom / Dolly Drift (1.00 -> 1.05)
        zoom = 1.0 + (0.05 * p_beat)
        zw, zh = int(w_out * zoom), int(h_out * zoom)
        base = plates[b_idx].resize((zw, zh), Image.Resampling.BILINEAR)
        zx = (zw - w_out) // 2
        zy = (zh - h_out) // 2
        frame = base.crop((zx, zy, zx + w_out, zy + h_out)).convert("RGBA")

        # 2. Dark Atmospheric Vignette (Top 400px and Bottom 500px for safe zones)
        vig = Image.new("RGBA", (w_out, h_out), (0, 0, 0, 0))
        d_vig = ImageDraw.Draw(vig)
        for y in range(420):
            alpha = int(190 * (1.0 - y / 420.0) ** 1.3)
            d_vig.line([(0, y), (w_out, y)], fill=(5, 5, 12, alpha))
        for y in range(h_out - 500, h_out):
            factor = (y - (h_out - 500)) / 500.0
            alpha = int(220 * (factor ** 1.2))
            d_vig.line([(0, y), (w_out, y)], fill=(3, 4, 8, alpha))
        frame = Image.alpha_composite(frame, vig)

        # 3. Dynamic 3D Kinetic Typography Slam (Elastic pop-in 1.35x -> 1.0x over first 0.38s)
        slam_dur = 0.38
        if b_t < slam_dur:
            p_slam = b_t / slam_dur
            scale_slam = 1.0 + (0.35 * ((1.0 - p_slam) ** 2) * math.cos(p_slam * math.pi * 2.5))
        else:
            scale_slam = 1.0

        t_data = typo_cache[b_idx]
        tw, th = t_data["width"], t_data["height"]
        if abs(scale_slam - 1.0) > 0.01:
            cw, ch = max(10, int(tw * scale_slam)), max(10, int(th * scale_slam))
            t_img = t_data["text_img"].resize((cw, ch), Image.Resampling.BILINEAR)
            b_img = t_data["bloom_img"].resize((cw, ch), Image.Resampling.BILINEAR)
        else:
            t_img, b_img = t_data["text_img"], t_data["bloom_img"]
            cw, ch = tw, th

        paste_x = (w_out - cw) // 2
        paste_y = int(h_out * 0.16) - (ch // 2)
        frame.paste(b_img, (paste_x, paste_y), b_img)
        frame.paste(t_img, (paste_x, paste_y), t_img)

        # 4. Lower-Third Word-Level Animated Caption Pill (Safe Zone: Y = 1480)
        # Find active spoken word
        active_w = None
        for w in words:
            if w["start"] <= t <= w["end"]:
                active_w = w
                break

        # Display 3-4 word cluster surrounding active word with 2-line auto-wrapping
        if active_w:
            w_idx = words.index(active_w)
            chunk_start = max(0, w_idx - 1)
            chunk_end = min(len(words), chunk_start + 4)
            cluster = words[chunk_start:chunk_end]
            draw_sliding_word_caption(
                frame=frame,
                caption_text=[item["word"] for item in cluster],
                active_word=active_w["word"],
                font_path=FONT_ROBOTO_BOLD,
                y=1480
            )

        proc.stdin.write(frame.convert("RGB").tobytes())

        if f_idx % 150 == 0:
            print(f"  Frame {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%) rendered...")

    proc.stdin.close()
    proc.wait()
    print("✓ Video frame stream rendered successfully.")

    # Audio Muxing: Christopher Voiceover + Ducked Subterranean Pulse BGM (-18 LUFS)
    print("🎛️ Mastering final audio mix (VO + -18 LUFS BGM)...")
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_mp4),
        "-i", str(AUDIO_FILE),
        "-stream_loop", "-1",
        "-i", str(BGM_FILE),
        "-filter_complex",
        "[1:a]volume=1.0[vo];[2:a]volume=0.12[bgm];[vo][bgm]amix=inputs=2:duration=first:dropout_transition=2[afinal]",
        "-map", "0:v",
        "-map", "[afinal]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(FINAL_VIDEO)
    ]
    subprocess.run(mix_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"🏆 SIGNATURE VIRAL SHORT MASTER COMPILED: {FINAL_VIDEO} ({FINAL_VIDEO.stat().st_size / 1e6:.1f} MB)")

async def main():
    await synthesize_audio_and_timestamps()
    render_magnates_short()

if __name__ == "__main__":
    asyncio.run(main())

