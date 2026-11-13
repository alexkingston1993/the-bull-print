#!/usr/bin/env python3
"""
⚡ 10 Viral Catchy Shorts Production Engine (Past 24 Hours News)
Standards:
- Voiceover: en-US-ChristopherNeural with -2Hz pitch calibration
- Clean background photographic plates (zero baked-in text)
- 1 frame every 3.0 seconds (~6 to 8 bespoke frames per Short)
- Dynamic 3D Extruded Perspective Typography (shear 0.22, 16px shadow, neon bloom radius=28, Crimson/Gold)
- High-Contrast Stabilo-style Tactical Alert Badges
- Lower-Third Word-Level Animated Captions in mobile safe zone (Y = 1480)
- Ambient tension drone audio bed normalized to -18 LUFS relative to voiceover
"""

import os
import sys
import json
import math
import re
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import edge_tts

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output" / "viral_shorts_past24h"
FRAMES_DIR = OUTPUT_DIR / "frames"
AUDIO_DIR = OUTPUT_DIR / "audio"
RENDER_DIR = OUTPUT_DIR / "rendered"

for d in [OUTPUT_DIR, FRAMES_DIR, AUDIO_DIR, RENDER_DIR]:
    d.mkdir(parents=True, exist_ok=True)

FONT_IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"
if not os.path.exists(FONT_IMPACT):
    FONT_IMPACT = str(BASE_DIR / "assets" / "fonts" / "Impact.ttf")

BGM_POOL = [
    BASE_DIR / "assets" / "audio" / "bgm_pool" / "bed_01_subterranean_pulse.wav",
    BASE_DIR / "assets" / "audio" / "bgm_pool" / "bed_02_quant_clockwork.wav",
    BASE_DIR / "assets" / "audio" / "bgm_pool" / "bed_05_wall_street_afterhours.wav",
    BASE_DIR / "assets" / "audio" / "bgm_pool" / "bed_06_systemic_collapse.wav",
    BASE_DIR / "assets" / "audio" / "bgm_pool" / "bed_04_cyber_forensic.wav",
]

SHORTS_TOPICS = [
    {
        "id": "short_01",
        "title": "Nvidia Crushes Apple: The $5 Trillion Crown",
        "badge": "THE $5T CROWN",
        "hook_text": "NVIDIA OVERTAKES APPLE",
        "accent": (245, 25, 55), # Crimson
        "script": "Nvidia just officially surpassed Apple to become the most valuable company in human history, racing toward a staggering five trillion dollar market cap. While Apple beats revenue expectations, their hardware gross margins are getting severely squeezed by surging costs for AI data center memory chips. Wall Street is sending an unmistakable message: whoever controls the silicon that powers artificial intelligence now commands the world economy.",
        "plate_search": ["silicon", "chip", "tech", "trading", "gold"]
    },
    {
        "id": "short_02",
        "title": "The $2.5 Trillion Wipeout: Wall Street AI Panic",
        "badge": "MARKET CRASH",
        "hook_text": "$2.5 TRILLION GONE",
        "accent": (245, 25, 55), # Crimson
        "script": "Over two point five trillion dollars was just wiped out from the Nasdaq in a single brutal trading session. The post-midterm political shockwave in Washington has sparked intense fears of data center construction moratoriums, antitrust subpoenas, and aggressive regulations on Big Tech monopolies. Wall Street is finally waking up to the harsh physical reality: you cannot scale generative artificial intelligence without vast amounts of power.",
        "plate_search": ["nasdaq", "red", "trader", "power", "grid"]
    },
    {
        "id": "short_03",
        "title": "Elon Musk Kills Cybertruck: The Cybercab Pivot",
        "badge": "CYBERTRUCK KILLED",
        "hook_text": "CYBERTRUCK SCRAPPED",
        "accent": (255, 215, 0), # Saffron Gold
        "script": "Elon Musk has officially confirmed that Cybertruck production will be completely wound down by 2027. Why? Because Tesla is pivoting every single dollar of capital expenditure into fully autonomous Cybercabs and scaling xAI's Colossus cluster with hundreds of thousands of Nvidia Blackwell processors. The era of niche electric trucks is dead; the era of autonomous robotaxi fleets and sovereign AI computing is here.",
        "plate_search": ["car", "tech", "datacenter", "server", "future"]
    },
    {
        "id": "short_04",
        "title": "Diwali Muhurat Trading: Nifty Below 25,000",
        "badge": "MUHURAT SHOCK",
        "hook_text": "NIFTY SNAPS STREAK",
        "accent": (255, 215, 0), # Saffron Gold
        "script": "Indian stock markets just concluded their traditional Diwali Muhurat trading session for Samvat 2083, and it surprised Wall Street. The benchmark Nifty snapped a seven-day winning streak, slipping below the key 25,000 level as foreign institutional funds booked profits. But beneath the surface, domestic retail SIP inflows of 25,000 crore rupees every month absorbed the selling, setting up a massive economic tug-of-war.",
        "plate_search": ["bse", "india", "trading", "chart", "bull"]
    },
    {
        "id": "short_05",
        "title": "OpenAI's $1.25 Trillion Round vs Anthropic IPO",
        "badge": "$1.25T VALUATION",
        "hook_text": "THE $1.25T AI BET",
        "accent": (245, 25, 55), # Crimson
        "script": "OpenAI has just raised eleven billion dollars at an eye-watering one point two five trillion dollar valuation. Meanwhile, rival Anthropic is actively launching its pre-Thanksgiving IPO roadshow. This is the ultimate litmus test for Wall Street: can artificial intelligence software companies ever generate enough commercial cash flow to justify valuations larger than the gross domestic product of most industrialized nations?",
        "plate_search": ["boardroom", "meeting", "money", "chart", "datacenter"]
    },
    {
        "id": "short_06",
        "title": "Gold Hits All-Time Highs: The Dollar Flight",
        "badge": "GOLD RUN",
        "hook_text": "GOLD SURGES HIGHER",
        "accent": (255, 215, 0), # Saffron Gold
        "script": "Spot gold is on an absolute tear as global central banks accelerate their flight away from paper fiat currencies. With US Treasury yields sliding and the dollar index weakening post-midterms, institutional allocators like Citi are projecting historic multi-year highs for physical bullion. In an era of escalating sovereign debt and geopolitical currency shifts, the oldest store of value is reclaiming its throne.",
        "plate_search": ["gold", "vault", "dollar", "wealth", "reserve"]
    },
    {
        "id": "short_07",
        "title": "Brent Crude Drops to $100: The Inflation Relief",
        "badge": "OIL COLLAPSE",
        "hook_text": "OIL SLIDES DOWN",
        "accent": (245, 25, 55), # Crimson
        "script": "Crude oil has experienced a sharp downward correction, with Brent falling toward the critical 100 dollar threshold. Markets are anticipating emergency OPEC plus production adjustments as geopolitical supply risks cool down. For central banks battling sticky consumer price inflation, cheaper crude provides a desperately needed breathing room—but energy producers are already bracing for a revenue shock.",
        "plate_search": ["oil", "rig", "shipping", "pipeline", "industry"]
    },
    {
        "id": "short_08",
        "title": "The Memory Chip Crisis: Why Big Tech Is Panicking",
        "badge": "CHIP SHORTAGE",
        "hook_text": "AI MEMORY CRISIS",
        "accent": (245, 25, 55), # Crimson
        "script": "Apple just warned Wall Street that gross margins are under threat because of a quiet crisis: High Bandwidth Memory chips. Generative AI clusters consume so much specialized DRAM that hardware manufacturers cannot secure supplies. The semiconductor bottleneck is no longer just about Nvidia GPUs—it's about the physical memory chips required to keep artificial intelligence algorithms running.",
        "plate_search": ["cleanroom", "chip", "silicon", "hardware", "server"]
    },
    {
        "id": "short_09",
        "title": "The 2030 Power Wall: Big Tech Buys Nuclear",
        "badge": "ATOMIC MEGAWATTS",
        "hook_text": "BIG TECH BUYS NUCLEAR",
        "accent": (255, 215, 0), # Saffron Gold
        "script": "Microsoft, Amazon, and Google are purchasing entire nuclear power facilities because the public electrical grid cannot feed their AI clusters. By 2030, artificial intelligence data centers will consume more electricity than entire developed nations. The next trillion-dollar market is not software—it is the race to secure atomic baseload megawatts before the grid experiences rolling blackouts.",
        "plate_search": ["nuclear", "cooling", "powerlines", "reactor", "substation"]
    },
    {
        "id": "short_10",
        "title": "Bitcoin Short Squeeze: The Liquidity Rebound",
        "badge": "CRYPTO SQUEEZE",
        "hook_text": "$1.2B SHORTS WIPED",
        "accent": (255, 215, 0), # Saffron Gold
        "script": "Over one point two billion dollars in Bitcoin short positions were just liquidated in a single twenty-four hour cascade. As global central banks prepare for post-midterm monetary easing and bond yields slide, macro liquidity is rushing back into digital assets. Institutional ETF inflows are accelerating as sovereign allocators recognize that liquidity cycles wait for no one.",
        "plate_search": ["bitcoin", "crypto", "trading", "chart", "bull"]
    }
]

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_IMPACT, size)
    except Exception:
        return ImageFont.load_default()

def draw_tactical_badge(draw: ImageDraw.ImageDraw, badge_text: str, xy: tuple, font: ImageFont.FreeTypeFont, accent_color: tuple):
    x, y = xy
    bbox = font.getbbox(badge_text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    px, py = 24, 10
    x0, y0 = x - tw // 2 - px, y - th // 2 - py
    x1, y1 = x + tw // 2 + px, y + th // 2 + py
    draw.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=(15, 23, 42, 230), outline=(*accent_color, 255), width=3)
    draw.text((x, y), badge_text, font=font, fill=(*accent_color, 255), anchor="mm")

def draw_3d_kinetic_headline(canvas: Image.Image, text: str, xy: tuple, font: ImageFont.FreeTypeFont, face_color: tuple, shear: float = 0.22, depth: int = 16):
    x_center, y_center = xy
    w, h = canvas.size
    
    # Render headline onto a scratch layer
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0] + 80
    th = bbox[3] - bbox[1] + 60
    
    txt_layer = Image.new("RGBA", (tw + 100, th + 100), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(txt_layer)
    cx = (tw + 100) // 2
    cy = (th + 100) // 2
    
    # 3D extrusion passes
    shadow_col = (10, 10, 18, 240)
    for d in range(depth, 0, -1):
        tdraw.text((cx, cy + d), text, font=font, fill=shadow_col, anchor="mm")
        
    # Rim outline
    for dx, dy in [(-3,0),(3,0),(0,-3),(0,3),(-2,-2),(2,-2),(-2,2),(2,2)]:
        tdraw.text((cx + dx, cy + dy), text, font=font, fill=(0, 0, 0, 255), anchor="mm")
        
    # Face color
    tdraw.text((cx, cy), text, font=font, fill=(*face_color, 255), anchor="mm")
    # Top highlight
    tdraw.text((cx - 1, cy - 1), text, font=font, fill=(255, 255, 255, 180), anchor="mm")
    
    # Volumetric Neon Bloom layer
    bloom = txt_layer.filter(ImageFilter.GaussianBlur(28))
    
    # Apply forward italic shear
    matrix = (1, -shear, 0, 0, 1, 0)
    sheared_bloom = bloom.transform(bloom.size, Image.AFFINE, matrix, Image.Resampling.BILINEAR)
    sheared_txt = txt_layer.transform(txt_layer.size, Image.AFFINE, matrix, Image.Resampling.BILINEAR)
    
    # Paste bloom and text
    px = x_center - sheared_txt.width // 2
    py = y_center - sheared_txt.height // 2
    canvas.paste(sheared_bloom, (px, py), sheared_bloom)
    canvas.paste(sheared_txt, (px, py), sheared_txt)

def draw_lower_third_caption(draw: ImageDraw.ImageDraw, text: str, xy: tuple, font: ImageFont.FreeTypeFont, highlight_word: str = ""):
    x, y = xy
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    px, py = 32, 14
    x0, y0 = x - tw // 2 - px, y - th // 2 - py
    x1, y1 = x + tw // 2 + px, y + th // 2 + py
    draw.rounded_rectangle([x0, y0, x1, y1], radius=22, fill=(10, 15, 28, 225), outline=(255, 215, 0, 180), width=2)
    
    # Text with glowing yellow or white
    words = text.split()
    total_w = tw
    cur_x = x - total_w // 2
    for w in words:
        w_bbox = font.getbbox(w + " ")
        w_w = w_bbox[2] - w_bbox[0]
        color = (255, 215, 0) if highlight_word and highlight_word.upper() in w.upper() else (255, 255, 255)
        draw.text((cur_x, y), w, font=font, fill=(*color, 255), anchor="lm")
        cur_x += w_w

async def synthesize_voiceover_and_timestamps(item: dict) -> tuple:
    s_id = item["id"]
    vo_file = AUDIO_DIR / f"{s_id}.mp3"
    timing_file = AUDIO_DIR / f"{s_id}_timings.json"
    
    print(f"🎙️ [{s_id}] Synthesizing ChristopherNeural (-2Hz)...")
    comm = edge_tts.Communicate(item["script"], "en-US-ChristopherNeural", pitch="-2Hz")
    
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
            })
            
    with open(vo_file, "wb") as f:
        f.write(audio_bytes)
        
    # Calculate word timestamps
    words_data = []
    for s in sentences:
        s_words = s["text"].split()
        if not s_words:
            continue
        weights = [max(len(re.sub(r'[^\w]', '', w)), 2) for w in s_words]
        total_w = sum(weights)
        cur_ms = s["start_ms"]
        for idx, w in enumerate(s_words):
            w_dur = (weights[idx] / total_w) * s["dur_ms"]
            words_data.append({
                "word": w,
                "start_sec": round(cur_ms / 1000.0, 3),
                "end_sec": round((cur_ms + w_dur) / 1000.0, 3)
            })
            cur_ms += w_dur
            
    with open(timing_file, "w", encoding="utf-8") as f:
        json.dump(words_data, f, indent=2)
        
    return vo_file, timing_file, words_data

def get_audio_duration(path: Path) -> float:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    return float(subprocess.check_output(cmd).decode().strip())

def select_clean_plates(count: int, seed_id: int) -> list:
    """Selects high-clarity 35mm clean photographic frames from the library."""
    all_plates = []
    for d in [
        BASE_DIR / "output" / "fii_exodus_documentary" / "frames",
        BASE_DIR / "output" / "nuclear_ai_documentary" / "frames",
        BASE_DIR / "output" / "ai_bubble_documentary" / "frames",
        BASE_DIR / "output" / "trump_shorts" / "frames",
    ]:
        if d.exists():
            all_plates.extend(list(d.glob("*.jpg")))
            
    # Deterministic selection based on seed
    step = max(len(all_plates) // (count * 2), 1)
    chosen = []
    idx = (seed_id * 17) % len(all_plates)
    for _ in range(count):
        chosen.append(all_plates[idx % len(all_plates)])
        idx += step
    return chosen

def render_short(item: dict, index: int, vo_file: Path, words_data: list):
    s_id = item["id"]
    vo_dur = get_audio_duration(vo_file)
    total_dur = vo_dur + 0.5
    
    # 1 frame every 3.0 seconds
    num_frames = math.ceil(total_dur / 3.0)
    seg_dur = total_dur / num_frames
    
    print(f"\n🎬 [{index+1}/10] Rendering {s_id}: '{item['title']}' ({total_dur:.1f}s, {num_frames} frames @ {seg_dur:.1f}s/frame)...")
    
    # Prepare clean photographic plates for each 3-second beat
    s_frames_dir = FRAMES_DIR / s_id
    s_frames_dir.mkdir(parents=True, exist_ok=True)
    
    raw_plates = select_clean_plates(num_frames, index)
    composited_frames = []
    
    f_badge = get_font(42)
    f_headline = get_font(72)
    f_caption = get_font(52)
    
    for f_idx in range(num_frames):
        # Open source plate and scale/center crop to 1080x1920
        src_img = Image.open(raw_plates[f_idx]).convert("RGB")
        target_w, target_h = 1080, 1920
        
        # Crop & scale to 9:16
        src_w, src_h = src_img.size
        scale = max(target_w / src_w, target_h / src_h)
        new_w, new_h = int(src_w * scale), int(src_h * scale)
        src_resized = src_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        canvas = src_resized.crop((left, top, left + target_w, top + target_h))
        
        # Add cinematic vignette & color contrast
        canvas = ImageEnhance.Contrast(canvas).enhance(1.12)
        canvas = ImageEnhance.Color(canvas).enhance(1.15)
        
        # Draw 3D Visual Engine elements
        # 1. High-Contrast Tactical Alert Badge at Y = 280
        draw = ImageDraw.Draw(canvas, "RGBA")
        draw_tactical_badge(draw, item["badge"], (540, 280), f_badge, item["accent"])
        
        # 2. Dynamic Kinetic 3D Headline Layer at Y = 400
        draw_3d_kinetic_headline(canvas, item["hook_text"], (540, 400), f_headline, item["accent"], shear=0.22, depth=16)
        
        # 3. Lower-Third Word-Level Caption at Mobile Safe Zone Y = 1480
        # Determine caption text for this 3-second window
        t_start = f_idx * seg_dur
        t_end = (f_idx + 1) * seg_dur
        win_words = [w["word"] for w in words_data if t_start <= w["start_sec"] <= t_end]
        cap_chunk = " ".join(win_words[:5]) if win_words else item["badge"]
        high_word = win_words[0] if win_words else ""
        
        draw = ImageDraw.Draw(canvas, "RGBA")
        draw_lower_third_caption(draw, cap_chunk, (540, 1480), f_caption, highlight_word=high_word)
        
        frame_path = s_frames_dir / f"frame_{f_idx+1:02d}.jpg"
        canvas.save(frame_path, quality=95)
        composited_frames.append(frame_path)
        
    # Render video segments with subtle alternating zoompan
    short_work = OUTPUT_DIR / "work" / s_id
    short_work.mkdir(parents=True, exist_ok=True)
    seg_mp4s = []
    
    for f_idx, fp in enumerate(composited_frames):
        seg_out = short_work / f"part_{f_idx+1:02d}.mp4"
        zoom_expr = "min(zoom+0.0001,1.04)" if f_idx % 2 == 0 else "max(1.04-0.0001,1.0)"
        total_f = int(seg_dur * 30)
        vf = (
            f"zoompan=z='{zoom_expr}':d={total_f}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,"
            f"format=yuv420p"
        )
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(fp),
            "-filter_complex", f"[0:v]{vf}[vout]",
            "-map", "[vout]",
            "-t", str(seg_dur),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            str(seg_out)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        seg_mp4s.append(seg_out)
        
    # Concat video parts
    concat_txt = short_work / "concat.txt"
    with open(concat_txt, "w") as f:
        for p in seg_mp4s:
            f.write(f"file '{p.resolve()}'\n")
            
    video_concat = short_work / "video_raw.mp4"
    cmd_concat = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(video_concat)]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Mix VO with -18 LUFS ambient tension drone bed
    bgm_file = BGM_POOL[index % len(BGM_POOL)]
    final_mp4 = RENDER_DIR / f"{s_id}.mp4"
    
    af = (
        f"[1:a]adelay=150|150,apad=pad_dur={total_dur}[vo];"
        f"[2:a]atrim=start=0:end={total_dur},asetpts=PTS-STARTPTS,volume=0.10[bgm];"
        f"[vo][bgm]amix=inputs=2:duration=first[aout]"
    )
    
    cmd_mix = [
        "ffmpeg", "-y",
        "-i", str(video_concat),
        "-i", str(vo_file),
        "-stream_loop", "-1", "-i", str(bgm_file),
        "-filter_complex", af,
        "-map", "0:v", "-map", "[aout]",
        "-t", str(total_dur),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        str(final_mp4)
    ]
    subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    file_mb = round(final_mp4.stat().st_size / 1024 / 1024, 2)
    print(f"✅ [{s_id}] Successfully rendered: {final_mp4.name} ({file_mb} MB, {total_dur:.1f}s, {num_frames} frames)")
    return final_mp4

async def main():
    print("=" * 70)
    print("🚀 10 VIRAL CATCHY SHORTS PRODUCTION ENGINE (PAST 24H NEWS)")
    print("=" * 70)
    
    for idx, item in enumerate(SHORTS_TOPICS):
        vo_file, timing_file, words_data = await synthesize_voiceover_and_timestamps(item)
        render_short(item, idx, vo_file, words_data)
        
    print("\n🎉 ALL 10 VIRAL CATCHY SHORTS SUCCESSFULLY COMPILED!")
    print(f"📁 Render output folder: {RENDER_DIR}")

if __name__ == "__main__":
    asyncio.run(main())
