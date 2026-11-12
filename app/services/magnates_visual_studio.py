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
    """Draws word-level kinetic captions in mobile safe zone with yellow highlight on spoken word."""
    words = caption_text.split()
    if not words:
        return
        
    draw = ImageDraw.Draw(frame, "RGBA")
    clean_active = active_word.strip(".,!?:;\"'").upper() if active_word else ""
    
    match_idx = 0
    if clean_active:
        for idx, w in enumerate(words):
            if w.strip(".,!?:;\"'").upper() == clean_active:
                match_idx = idx
                break
                
    start_idx = max(0, match_idx - 1)
    visible_words = words[start_idx : start_idx + 4]
    
    try:
        font_c = ImageFont.truetype(font_path, 46)
    except Exception:
        font_c = ImageFont.load_default()
        
    word_boxes = []
    total_w = 0
    space_w = 16
    
    for w in visible_words:
        bbox = font_c.getbbox(w.upper())
        bw = bbox[2] - bbox[0]
        word_boxes.append((w.upper(), bw))
        total_w += bw
    total_w += space_w * (len(visible_words) - 1)
    
    pad_x, pad_y = 32, 18
    box_w = total_w + pad_x * 2
    box_h = 76
    box_left = (frame.width - box_w) // 2
    box_top = y - (box_h // 2)
    
    # Glassmorphic rounded pill backdrop
    draw.rounded_rectangle([box_left, box_top, box_left + box_w, box_top + box_h], radius=16, fill=(8, 12, 22, 220), outline=(52, 211, 153, 140), width=2)
    
    cur_x = box_left + pad_x
    text_y = box_top + (box_h // 2)
    
    for w_txt, bw in word_boxes:
        is_highlight = (clean_active and w_txt == clean_active) or (not clean_active and w_txt == visible_words[0].upper())
        fill_col = (250, 204, 21) if is_highlight else (241, 245, 249)
        draw.text((cur_x, text_y), w_txt, font=font_c, fill=fill_col, anchor="lm")
        cur_x += bw + space_w


def fetch_clean_photographic_plate(prompt: str, width: int = 1080, height: int = 1920, out_path: Optional[Path] = None) -> Image.Image:
    """Fetches a clean photographic plate, stripping any watermark badge via lossless crop & rescale."""
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&nologo=true&model=flux"
    try:
        resp = requests.get(url, timeout=35)
        if resp.status_code == 200 and len(resp.content) > 10000:
            import io
            raw_img = Image.open(io.BytesIO(resp.content)).convert("RGB")
            # Lossless crop bottom 6% where watermarks sit & Lanczos upscale to exact dimensions
            w, h = raw_img.size
            clean_img = raw_img.crop((0, 0, w, int(h * 0.94))).resize((width, height), Image.Resampling.LANCZOS)
            if out_path:
                clean_img.save(out_path, quality=95)
            return clean_img
    except Exception as e:
        logger.warning(f"Could not fetch cloud plate: {e}")
        
    # High-contrast photographic atmospheric fallback (pure cinematic dark gradient)
    img = Image.new("RGB", (width, height), (7, 11, 20))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        ratio = y / height
        r = int(7 + ratio * 15)
        g = int(11 + ratio * 18)
        b = int(20 + ratio * 32)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    if out_path:
        img.save(out_path, quality=95)
    return img
