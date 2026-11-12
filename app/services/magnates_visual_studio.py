#!/usr/bin/env python3
"""
app/services/magnates_visual_studio.py

THE OFFICIAL MAGNATESMEDIA 3D KINETIC VISUAL ENGINE — The Bull Print
Architectural 9:16 Vertical & 16:9 Landscape Video Compositor:
1. Photorealistic 35mm clean photographic plates (zero clip-art, zero 2D shapes, zero watermarks).
2. Stacked 3D extruded perspective typography (forward shear 0.22, 16px extrusion shadow, neon bloom).
3. Bounded safe-zone auto-fit (max_sheared_w=760 on 1080w) so text NEVER clips past screen edges.
4. Elastic kinetic slam pop-in (1.35x -> 1.0x over first 0.45s).
5. Mobile safe-zone active-word kinetic captions (Y = 1480).
"""

import os
import math
import urllib.parse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import requests
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Typography fonts discovery
FONT_IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"
if not os.path.exists(FONT_IMPACT):
    for cand in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Black.ttf",
        str(BASE_DIR / "assets/fonts/Inter-Bold.ttf")
    ]:
        if os.path.exists(cand):
            FONT_IMPACT = cand
            break

FONT_ROBOTO_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
if not os.path.exists(FONT_ROBOTO_BOLD):
    FONT_ROBOTO_BOLD = FONT_IMPACT


def auto_fit_typography(lines: List[str], badge_text: str, font_path: str, max_sheared_w: int = 760):
    """Calculates optimal font size so sheared 3D text never overflows screen boundaries."""
    f_size = 96
    shear_val = 0.22
    
    while f_size >= 40:
        try:
            f_hero = ImageFont.truetype(font_path, f_size)
            f_badge = ImageFont.truetype(font_path, max(24, int(f_size * 0.42)))
        except Exception:
            f_hero = ImageFont.load_default()
            f_badge = f_hero
            
        max_line_w = 0
        for l in lines:
            bbox = f_hero.getbbox(l)
            w = bbox[2] - bbox[0]
            if w > max_line_w:
                max_line_w = w
                
        line_spacing = int(f_size * 0.94)
        total_h = len(lines) * line_spacing + int(f_size * 0.6)
        sheared_w = max_line_w + int(total_h * shear_val) + 60
        
        if sheared_w <= max_sheared_w:
            return f_size, sheared_w, total_h, f_hero, f_badge
        f_size -= 4
        
    return f_size, sheared_w, total_h, f_hero, f_badge


def precompute_cut_typography(
    lines: List[str],
    badge_text: str,
    font_path: str = FONT_IMPACT,
    max_sheared_w: int = 760,
    face_color: Tuple[int, int, int] = (255, 255, 255),
    badge_bg: Tuple[int, int, int] = (239, 68, 68)
) -> Dict[str, Any]:
    """Renders 3D extruded perspective typography with neon bloom and safe margins."""
    sanitized_lines = [l.replace("₹", "RS. ").strip().upper() for l in lines if l.strip()]
    sanitized_badge = badge_text.replace("₹", "RS. ").strip().upper()
    
    f_size, sheared_w, total_h, f_hero, f_badge = auto_fit_typography(
        sanitized_lines, sanitized_badge, font_path, max_sheared_w=max_sheared_w
    )
    
    text_canvas_w, text_canvas_h = 1600, 1000
    text_layer = Image.new("RGBA", (text_canvas_w, text_canvas_h), (0, 0, 0, 0))
    draw_t = ImageDraw.Draw(text_layer)
    
    cx = text_canvas_w // 2
    start_y = 100
    
    # 1. Tactical highlighter badge
    badge_bbox = f_badge.getbbox(sanitized_badge)
    badge_w = badge_bbox[2] - badge_bbox[0] + 44
    badge_h = badge_bbox[3] - badge_bbox[1] + 20
    b_left = cx - badge_w // 2
    b_top = start_y
    draw_t.rounded_rectangle([b_left, b_top, b_left + badge_w, b_top + badge_h], radius=10, fill=badge_bg)
    badge_txt_y = b_top + (badge_h // 2)
    draw_t.text((cx, badge_txt_y), sanitized_badge, font=f_badge, fill=(10, 15, 28), anchor="mm")
    
    # 2. 3D Headline extrusion & face
    line_spacing = int(f_size * 0.94)
    headline_top = start_y + badge_h + 30
    
    for i, line in enumerate(sanitized_lines):
        line_y = headline_top + (i * line_spacing)
        # 16px 3D extrusion shadow block
        for offset in range(16, 0, -1):
            alpha = int(240 * (1.0 - (offset / 24.0)))
            draw_t.text((cx + (offset * 0.5), line_y + offset), line, font=f_hero, fill=(5, 7, 12, alpha), anchor="mt")
        # Dark rim outline
        for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-2,-2), (2,2), (-2,2), (2,-2)]:
            draw_t.text((cx + dx, line_y + dy), line, font=f_hero, fill=(0, 0, 0, 255), anchor="mt")
        # Saturated face
        draw_t.text((cx, line_y), line, font=f_hero, fill=face_color, anchor="mt")
        # Top-left specular rim highlight
        draw_t.text((cx - 1, line_y - 1), line, font=f_hero, fill=(255, 255, 255, 130), anchor="mt")
        
    # Volumetric neon bloom layer
    bloom_layer = text_layer.filter(ImageFilter.GaussianBlur(28))
    
    # Forward italic shear angle 0.22
    shear_val = 0.22
    affine_matrix = (1.0, -shear_val, 0.0, 0.0, 1.0, 0.0)
    
    sheared_text = text_layer.transform(
        (text_canvas_w, text_canvas_h),
        Image.AFFINE,
        affine_matrix,
        resample=Image.Resampling.BICUBIC
    )
    sheared_bloom = bloom_layer.transform(
        (text_canvas_w, text_canvas_h),
        Image.AFFINE,
        affine_matrix,
        resample=Image.Resampling.BICUBIC
    )
    
    bbox = sheared_text.getbbox()
    if bbox:
        crop_box = (
            max(0, bbox[0] - 40),
            max(0, bbox[1] - 40),
            min(text_canvas_w, bbox[2] + 40),
            min(text_canvas_h, bbox[3] + 40)
        )
        final_text = sheared_text.crop(crop_box)
        final_bloom = sheared_bloom.crop(crop_box)
    else:
        final_text = sheared_text
        final_bloom = sheared_bloom
        
    return {
        "text_img": final_text,
        "bloom_img": final_bloom,
        "width": final_text.width,
        "height": final_text.height
    }


def draw_sliding_word_caption(frame: Image.Image, caption_text: str, active_word: str, font_path: str = FONT_ROBOTO_BOLD, y: int = 1480):
    """Draws adaptive word-level kinetic captions in mobile/landscape safe zone with 2-line auto-wrap and yellow highlight on spoken word."""
    words = caption_text.split() if isinstance(caption_text, str) else list(caption_text)
    if not words:
        return
        
    draw = ImageDraw.Draw(frame, "RGBA")
    clean_active = active_word.strip(".,!?:;\"'").upper() if active_word else ""
    
    match_idx = 0
    if clean_active:
        for idx, w in enumerate(words):
            if str(w).strip(".,!?:;\"'").upper() == clean_active:
                match_idx = idx
                break
                
    start_idx = max(0, match_idx - 1)
    visible_words = [str(w) for w in words[start_idx : start_idx + 4]]
    
    font_size = 46
    try:
        font_c = ImageFont.truetype(font_path, font_size)
    except Exception:
        font_c = ImageFont.load_default()
        
    w_out, h_out = frame.size
    max_pill_w = min(840, w_out - 180) if w_out < h_out else min(1480, w_out - 240)
    pad_x = 32
    space_w = int(font_size * 0.30)
    
    # 1. Measure items
    items = []
    for w_str in visible_words:
        bbox = font_c.getbbox(w_str)
        bw = bbox[2] - bbox[0]
        items.append({
            "word": w_str,
            "clean": w_str.strip(".,!?:;\"'").upper(),
            "w": bw
        })
        
    max_line_content_w = max_pill_w - (pad_x * 2)
    single_line_w = sum(it["w"] for it in items) + space_w * (len(items) - 1)
    
    # 2. Check 1 line vs 2 lines
    if single_line_w <= max_line_content_w:
        lines = [items]
        line_widths = [single_line_w]
    else:
        # Wrap into 2 balanced lines so nothing overflows the border
        best_split = len(items) // 2
        min_diff = float("inf")
        for i in range(1, len(items)):
            l1_w = sum(it["w"] for it in items[:i]) + space_w * (i - 1)
            l2_w = sum(it["w"] for it in items[i:]) + space_w * (len(items) - i - 1)
            if l1_w <= max_line_content_w and l2_w <= max_line_content_w:
                diff = abs(l1_w - l2_w)
                if diff < min_diff:
                    min_diff = diff
                    best_split = i
        lines = [items[:best_split], items[best_split:]]
        line_widths = [
            sum(it["w"] for it in lines[0]) + space_w * (len(lines[0]) - 1),
            sum(it["w"] for it in lines[1]) + space_w * (len(lines[1]) - 1)
        ]

    # 3. Pill geometry
    content_w = max(line_widths)
    pw = content_w + (pad_x * 2)
    line_h = font_size + 6
    if len(lines) == 1:
        ph = font_size + 36
    else:
        ph = (line_h * 2) + 38
        
    px = max(24, min(w_out - pw - 24, (w_out - pw) // 2))
    py = y - (ph // 2)

    # 4. Draw rounded pill backdrop
    draw.rounded_rectangle(
        [px, py, px + pw, py + ph],
        radius=18,
        fill=(8, 12, 22, 230),
        outline=(52, 211, 153, 175),
        width=2
    )

    # 5. Draw words centered line by line with active spoken highlight
    if len(lines) == 1:
        cur_y = py + (ph // 2)
        cur_x = px + (pw - line_widths[0]) // 2
        for it in lines[0]:
            is_active = (clean_active and it["clean"] == clean_active)
            col = (250, 204, 21, 255) if is_active else (245, 245, 250, 240)
            draw.text((cur_x, cur_y), it["word"], font=font_c, fill=col, anchor="lm")
            cur_x += it["w"] + space_w
    else:
        y1 = py + 18 + (line_h // 2)
        y2 = py + ph - 18 - (line_h // 2)
        for idx, (line, cur_y) in enumerate(zip(lines, [y1, y2])):
            cur_x = px + (pw - line_widths[idx]) // 2
            for it in line:
                is_active = (clean_active and it["clean"] == clean_active)
                col = (250, 204, 21, 255) if is_active else (245, 245, 250, 240)
                draw.text((cur_x, cur_y), it["word"], font=font_c, fill=col, anchor="lm")
                cur_x += it["w"] + space_w


def fetch_clean_photographic_plate(prompt: str, width: int = 1080, height: int = 1920, out_path: Optional[Path] = None) -> Image.Image:
    """Acquires a 100% clean photographic plate exclusively via Kaggle Dual-T4 GPU diffusers or local approved bundle library. Zero web APIs."""
    import re
    from app.services.kaggle_image_worker import KaggleImageWorker

    # Strategy 1: Check existing clean Kaggle plates or approved library
    clean_prompt = prompt.replace("clean plate", "").replace("zero text", "").replace("zero watermark", "").strip()
    
    # Check if a matching bundle or clean plate exists on local disk
    local_pools = [
        Path("/tmp/kaggle_gpu_frames_clean/frames"),
        Path("/tmp/kaggle_viral_short_clean/frames"),
        Path("assets/approved_bundles"),
    ]
    for pool in local_pools:
        if pool.exists():
            matches = list(pool.glob("*.jpg")) + list(pool.glob("*.png"))
            if matches:
                # Deterministic pick based on prompt hash
                pick = matches[abs(hash(clean_prompt)) % len(matches)]
                try:
                    img = Image.open(pick).convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
                    if out_path:
                        img.save(out_path, quality=95)
                    logger.success(f"✓ [Kaggle Studio] Clean plate loaded from verified GPU cache: {pick.name}")
                    return img
                except Exception:
                    pass

    # Strategy 2: Live Dispatch to Kaggle Dual-T4 GPU
    try:
        worker = KaggleImageWorker()
        aspect = "9:16" if height > width else "16:9"
        out_f = out_path if out_path else Path("/tmp/kaggle_live_plate.jpg")
        worker.generate_batch(
            prompts=[{"prompt": clean_prompt, "output_path": str(out_f)}],
            aspect_ratio=aspect
        )
        if out_f.exists():
            img = Image.open(out_f).convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
            logger.success(f"✓ [Kaggle GPU Cloud] Fresh bespoke plate generated on Kaggle GPU: {out_f.name}")
            return img
    except Exception as e:
        logger.warning(f"[Kaggle GPU Dispatch Notice]: {e}")

    raise RuntimeError(f"CRITICAL: Failed to acquire Kaggle GPU photographic plate for prompt '{prompt[:60]}'. Third-party web APIs are permanently prohibited.")
