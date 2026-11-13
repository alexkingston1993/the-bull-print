#!/usr/bin/env python3
"""
Generate High-Converting Viral CTR YouTube Thumbnails (1280x720, 16:9)
And upload them to YouTube for:
1. Doc 01: The $2.5 Trillion AI Wall: Why the AI Bubble Is Cracking (xMVcsq_f36U)
2. Luna: THE LUNA EXTINCTION: The $40 Billion Death Spiral That Broke Crypto (C-c3KJ6te2M)
"""

import sys
import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

THUMB_W = 1280
THUMB_H = 720

FONTS = [
    "/System/Library/Fonts/Supplemental/Impact.ttf",
    "/System/Library/Fonts/Impact.ttf",
    "/Library/Fonts/Impact.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/SFNS.ttf",
]
FONT_PATH = next((f for f in FONTS if os.path.exists(f)), None)

def draw_3d_text(
    draw: ImageDraw.Draw,
    pos: tuple,
    text: str,
    font: ImageFont.FreeTypeFont,
    face_color: tuple,
    extrusion_depth: int = 12,
    extrusion_color: tuple = (10, 10, 10, 240),
    stroke_width: int = 4,
    stroke_color: tuple = (0, 0, 0, 255)
):
    x, y = pos
    # Draw extrusion block
    for d in range(extrusion_depth, 0, -1):
        draw.text(
            (x + d, y + d),
            text,
            font=font,
            fill=extrusion_color,
            stroke_width=stroke_width,
            stroke_fill=stroke_color
        )
    # Draw face text
    draw.text(
        (x, y),
        text,
        font=font,
        fill=face_color,
        stroke_width=stroke_width,
        stroke_fill=stroke_color
    )

def create_ai_bubble_thumbnail() -> Path:
    out_path = BASE_DIR / "output" / "thumbnails" / "thumb_ai_bubble_viral_ctr.jpg"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Base Plate: High-tech AI server / collapsing mountain plate
    candidates = [
        BASE_DIR / "output" / "ai_bubble_documentary" / "frames" / "seg_04_beat_2.jpg",
        BASE_DIR / "output" / "ai_bubble_documentary" / "frames" / "seg_02_beat_1.jpg",
        BASE_DIR / "output" / "ai_bubble_documentary" / "frames" / "seg_01_beat_3.jpg",
    ]
    bg_file = next((p for p in candidates if p.exists()), None)
    if bg_file:
        im = Image.open(bg_file).convert("RGBA")
        scale = max(THUMB_W / im.width, THUMB_H / im.height)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
        left = (im.width - THUMB_W) // 2
        top = (im.height - THUMB_H) // 2
        im = im.crop((left, top, left + THUMB_W, top + THUMB_H))
    else:
        im = Image.new("RGBA", (THUMB_W, THUMB_H), (15, 18, 25, 255))

    # Darken and enhance contrast for dramatic pop
    enhancer = ImageEnhance.Brightness(im)
    im = enhancer.enhance(0.70)
    contrast = ImageEnhance.Contrast(im)
    im = contrast.enhance(1.25)

    # 2. Add dramatic dark gradient overlay from left (where text sits)
    gradient = Image.new("RGBA", (THUMB_W, THUMB_H), (0, 0, 0, 0))
    d_grad = ImageDraw.Draw(gradient)
    for x in range(THUMB_W):
        # Heavy shadow on left 70% of screen
        factor = max(0.0, 1.0 - (x / (THUMB_W * 0.75)))
        alpha = int(220 * (factor ** 1.1))
        d_grad.line([(x, 0), (x, THUMB_H)], fill=(5, 8, 15, alpha))
    # Top and bottom vignette
    for y in range(160):
        alpha = int(180 * (1.0 - y / 160.0))
        d_grad.line([(0, y), (THUMB_W, y)], fill=(0, 0, 0, alpha))
    for y in range(THUMB_H - 160, THUMB_H):
        alpha = int(200 * ((y - (THUMB_H - 160)) / 160.0))
        d_grad.line([(0, y), (THUMB_W, y)], fill=(0, 0, 0, alpha))

    im = Image.alpha_composite(im, gradient)

    # 3. Draw Red Plunge Chart line on the right side
    chart_layer = Image.new("RGBA", (THUMB_W, THUMB_H), (0, 0, 0, 0))
    d_chart = ImageDraw.Draw(chart_layer)
    pts = [
        (750, 220), (830, 230), (900, 210), (980, 260),
        (1040, 240), (1090, 320), (1150, 480), (1220, 620)
    ]
    # Draw glowing red crash curve
    for w, a in [(14, 50), (10, 100), (6, 200), (4, 255)]:
        d_chart.line(pts, fill=(245, 25, 55, a), width=w, joint="curve")
    
    # Red glow bloom on chart
    blur_chart = chart_layer.filter(ImageFilter.GaussianBlur(10))
    im = Image.alpha_composite(im, blur_chart)
    im = Image.alpha_composite(im, chart_layer)

    # 4. Text and Badges (Left Heavy, Giant 3D Impact)
    draw = ImageDraw.Draw(im)

    f_badge = ImageFont.truetype(FONT_PATH, 32)
    f_huge = ImageFont.truetype(FONT_PATH, 122)
    f_sub = ImageFont.truetype(FONT_PATH, 44)

    # Tactical Highlighter Badge (Clean text, zero emoji boxes)
    badge_text = "WALL ST ALERT: $2.5T AT RISK"
    b_len = int(draw.textlength(badge_text, font=f_badge))
    bx, by = 60, 65
    draw.rounded_rectangle([bx, by, bx + b_len + 36, by + 50], radius=10, fill=(245, 25, 55, 240), outline=(255, 255, 255, 200), width=2)
    draw.text((bx + 18, by + 8), badge_text, font=f_badge, fill=(255, 255, 255, 255))

    # Giant 3D Extruded Title
    # Line 1: THE $2.5T (Saffron Gold)
    draw_3d_text(draw, (60, 140), "THE $2.5T", f_huge, face_color=(255, 215, 0, 255), extrusion_depth=16, stroke_width=6)
    # Line 2: AI LIE (Crisp White with Red Shadow)
    draw_3d_text(draw, (60, 265), "AI LIE", f_huge, face_color=(255, 255, 255, 255), extrusion_depth=16, extrusion_color=(180, 10, 30, 255), stroke_width=6)

    # Sub-Callout pill: "WALL STREET'S DIRTY SECRET"
    sub_pill_y = 415
    draw.rounded_rectangle([60, sub_pill_y, 60 + 550, sub_pill_y + 56], radius=12, fill=(15, 20, 30, 230), outline=(245, 158, 11, 230), width=3)
    draw.text((80, sub_pill_y + 6), "WALL STREET'S DIRTY SECRET", font=f_sub, fill=(255, 230, 0, 255))

    # Bottom stat badge: "-84% FREE CASH FLOW"
    stat_y = 500
    draw.rounded_rectangle([60, stat_y, 60 + 440, stat_y + 60], radius=12, fill=(220, 20, 40, 230), outline=(255, 255, 255, 200), width=2)
    draw.text((80, stat_y + 8), "CRASH: -84% DRAIN", font=ImageFont.truetype(FONT_PATH, 42), fill=(255, 255, 255, 255))

    # Convert to RGB and save high quality
    im_final = im.convert("RGB")
    im_final.save(out_path, quality=95)
    print(f"✅ AI Bubble Viral Thumbnail created: {out_path}")
    return out_path


def create_luna_thumbnail() -> Path:
    out_path = BASE_DIR / "output" / "thumbnails" / "thumb_luna_extinction_viral_ctr.jpg"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Base Plate: Candlestick crash / burning / algorithmic death spiral
    candidates = [
        BASE_DIR / "output" / "luna_death_spiral_documentary" / "frames" / "Candlestick_chart_crashing_to_zero_57bec3dc.jpg",
        BASE_DIR / "output" / "luna_death_spiral_documentary" / "frames" / "Algorithmic_stablecoin_death_spi…_67d3a834.jpg",
        BASE_DIR / "output" / "luna_death_spiral_documentary" / "frames" / "Crypto_house_of_cards_collapsing_f63026e3.jpg",
    ]
    bg_file = next((p for p in candidates if p.exists()), None)
    if bg_file:
        im = Image.open(bg_file).convert("RGBA")
        scale = max(THUMB_W / im.width, THUMB_H / im.height)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
        left = (im.width - THUMB_W) // 2
        top = (im.height - THUMB_H) // 2
        im = im.crop((left, top, left + THUMB_W, top + THUMB_H))
    else:
        im = Image.new("RGBA", (THUMB_W, THUMB_H), (20, 10, 12, 255))

    # Enhance contrast and saturation
    enhancer = ImageEnhance.Brightness(im)
    im = enhancer.enhance(0.65)
    contrast = ImageEnhance.Contrast(im)
    im = contrast.enhance(1.3)

    # 2. Gradient overlay
    gradient = Image.new("RGBA", (THUMB_W, THUMB_H), (0, 0, 0, 0))
    d_grad = ImageDraw.Draw(gradient)
    for x in range(THUMB_W):
        factor = max(0.0, 1.0 - (x / (THUMB_W * 0.72)))
        alpha = int(230 * (factor ** 1.1))
        d_grad.line([(x, 0), (x, THUMB_H)], fill=(12, 5, 8, alpha))
    for y in range(160):
        alpha = int(180 * (1.0 - y / 160.0))
        d_grad.line([(0, y), (THUMB_W, y)], fill=(0, 0, 0, alpha))
    for y in range(THUMB_H - 160, THUMB_H):
        alpha = int(200 * ((y - (THUMB_H - 160)) / 160.0))
        d_grad.line([(0, y), (THUMB_W, y)], fill=(0, 0, 0, alpha))

    im = Image.alpha_composite(im, gradient)

    # 3. Draw Blood-Red Collapse Line
    chart_layer = Image.new("RGBA", (THUMB_W, THUMB_H), (0, 0, 0, 0))
    d_chart = ImageDraw.Draw(chart_layer)
    pts = [
        (720, 180), (800, 190), (860, 160), (940, 220),
        (1000, 310), (1070, 480), (1140, 610), (1220, 660)
    ]
    for w, a in [(14, 60), (10, 120), (6, 220), (4, 255)]:
        d_chart.line(pts, fill=(255, 30, 40, a), width=w, joint="curve")
    
    blur_chart = chart_layer.filter(ImageFilter.GaussianBlur(12))
    im = Image.alpha_composite(im, blur_chart)
    im = Image.alpha_composite(im, chart_layer)

    # 4. Text and Badges (Clean text, zero emoji boxes)
    draw = ImageDraw.Draw(im)

    f_badge = ImageFont.truetype(FONT_PATH, 32)
    f_huge = ImageFont.truetype(FONT_PATH, 122)
    f_sub = ImageFont.truetype(FONT_PATH, 44)

    # Tactical Highlighter Badge
    badge_text = "CRYPTO CATASTROPHE: DEATH SPIRAL"
    b_len = int(draw.textlength(badge_text, font=f_badge))
    bx, by = 60, 65
    draw.rounded_rectangle([bx, by, bx + b_len + 36, by + 50], radius=10, fill=(245, 25, 55, 240), outline=(255, 255, 255, 200), width=2)
    draw.text((bx + 18, by + 8), badge_text, font=f_badge, fill=(255, 255, 255, 255))

    # Giant 3D Extruded Title
    # Line 1: $40 BILLION (Saffron Gold)
    draw_3d_text(draw, (60, 140), "$40 BILLION", f_huge, face_color=(255, 215, 0, 255), extrusion_depth=16, stroke_width=6)
    # Line 2: WIPED OUT (Crisp White with Crimson Shadow)
    draw_3d_text(draw, (60, 265), "WIPED OUT", f_huge, face_color=(255, 255, 255, 255), extrusion_depth=16, extrusion_color=(190, 15, 25, 255), stroke_width=6)

    # Callout pill: "$119 TO $0.00001 IN 72 HOURS"
    sub_pill_y = 415
    draw.rounded_rectangle([60, sub_pill_y, 60 + 580, sub_pill_y + 56], radius=12, fill=(15, 20, 30, 230), outline=(245, 158, 11, 230), width=3)
    draw.text((80, sub_pill_y + 6), "$119 TO $0.00001 IN 72 HOURS", font=f_sub, fill=(255, 230, 0, 255))

    # Bottom stat badge: "THE DO KWON EXTINCTION"
    stat_y = 500
    draw.rounded_rectangle([60, stat_y, 60 + 490, stat_y + 60], radius=12, fill=(220, 20, 40, 230), outline=(255, 255, 255, 200), width=2)
    draw.text((80, stat_y + 8), "COLLAPSE: HOW IT BROKE CRYPTO", font=ImageFont.truetype(FONT_PATH, 34), fill=(255, 255, 255, 255))

    im_final = im.convert("RGB")
    im_final.save(out_path, quality=95)
    print(f"✅ Luna Viral Thumbnail created: {out_path}")
    return out_path


def create_fii_exodus_thumbnail() -> Path:
    out_path = BASE_DIR / "output" / "thumbnails" / "thumb_fii_exodus_viral_ctr.jpg"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Base Plate: BSE Tower / Stock Market at dusk
    candidates = [
        BASE_DIR / "output" / "fii_exodus_documentary" / "frames" / "seg_01_beat_1.jpg",
        BASE_DIR / "output" / "fii_exodus_documentary" / "frames" / "seg_04_beat_2.jpg",
        BASE_DIR / "output" / "fii_exodus_documentary" / "frames" / "seg_02_beat_1.jpg",
    ]
    bg_file = next((p for p in candidates if p.exists()), None)
    if bg_file:
        im = Image.open(bg_file).convert("RGBA")
        scale = max(THUMB_W / im.width, THUMB_H / im.height)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
        left = (im.width - THUMB_W) // 2
        top = (im.height - THUMB_H) // 2
        im = im.crop((left, top, left + THUMB_W, top + THUMB_H))
    else:
        im = Image.new("RGBA", (THUMB_W, THUMB_H), (15, 18, 25, 255))

    enhancer = ImageEnhance.Brightness(im)
    im = enhancer.enhance(0.70)
    contrast = ImageEnhance.Contrast(im)
    im = contrast.enhance(1.25)

    gradient = Image.new("RGBA", (THUMB_W, THUMB_H), (0, 0, 0, 0))
    d_grad = ImageDraw.Draw(gradient)
    for x in range(THUMB_W):
        factor = max(0.0, 1.0 - (x / (THUMB_W * 0.72)))
        alpha = int(225 * (factor ** 1.1))
        d_grad.line([(x, 0), (x, THUMB_H)], fill=(8, 10, 18, alpha))
    for y in range(160):
        alpha = int(180 * (1.0 - y / 160.0))
        d_grad.line([(0, y), (THUMB_W, y)], fill=(0, 0, 0, alpha))
    for y in range(THUMB_H - 160, THUMB_H):
        alpha = int(200 * ((y - (THUMB_H - 160)) / 160.0))
        d_grad.line([(0, y), (THUMB_W, y)], fill=(0, 0, 0, alpha))

    im = Image.alpha_composite(im, gradient)

    # 3. Draw Green Comeback V-Shape Chart Line
    chart_layer = Image.new("RGBA", (THUMB_W, THUMB_H), (0, 0, 0, 0))
    d_chart = ImageDraw.Draw(chart_layer)
    pts = [
        (720, 260), (790, 310), (860, 440), (940, 560),
        (1010, 540), (1080, 380), (1150, 260), (1220, 180)
    ]
    for w, a in [(14, 60), (10, 120), (6, 220), (4, 255)]:
        d_chart.line(pts, fill=(16, 185, 129, a), width=w, joint="curve")
    
    blur_chart = chart_layer.filter(ImageFilter.GaussianBlur(12))
    im = Image.alpha_composite(im, blur_chart)
    im = Image.alpha_composite(im, chart_layer)

    # 4. Text and Badges (Mass audience terms strictly enforced)
    draw = ImageDraw.Draw(im)

    f_badge = ImageFont.truetype(FONT_PATH, 32)
    f_huge = ImageFont.truetype(FONT_PATH, 122)
    f_sub = ImageFont.truetype(FONT_PATH, 44)

    # Tactical Highlighter Badge
    badge_text = "INDIAN MARKET: FII COMEBACK"
    b_len = int(draw.textlength(badge_text, font=f_badge))
    bx, by = 60, 65
    draw.rounded_rectangle([bx, by, bx + b_len + 36, by + 50], radius=10, fill=(245, 25, 55, 240), outline=(255, 255, 255, 200), width=2)
    draw.text((bx + 18, by + 8), badge_text, font=f_badge, fill=(255, 255, 255, 255))

    # Giant 3D Extruded Title
    # Line 1: ₹14,900 CR (Saffron Gold)
    draw_3d_text(draw, (60, 140), "RS.14,900 CR", f_huge, face_color=(255, 215, 0, 255), extrusion_depth=16, stroke_width=6)
    # Line 2: U-TURN (Crisp White with Green/Emerald Shadow)
    draw_3d_text(draw, (60, 265), "U-TURN", f_huge, face_color=(255, 255, 255, 255), extrusion_depth=16, extrusion_color=(10, 140, 90, 255), stroke_width=6)

    # Callout pill: "FOREIGN FUNDS CRUSHED BY RETAIL"
    sub_pill_y = 415
    draw.rounded_rectangle([60, sub_pill_y, 60 + 580, sub_pill_y + 56], radius=12, fill=(15, 20, 30, 230), outline=(245, 158, 11, 230), width=3)
    draw.text((80, sub_pill_y + 6), "FOREIGN FUNDS MET THEIR MATCH", font=f_sub, fill=(255, 230, 0, 255))

    # Bottom stat badge: "HOW RETAIL TRADERS SAVED NIFTY"
    stat_y = 500
    draw.rounded_rectangle([60, stat_y, 60 + 520, stat_y + 60], radius=12, fill=(16, 185, 129, 230), outline=(255, 255, 255, 200), width=2)
    draw.text((80, stat_y + 8), "REVERSAL: HOW RETAIL SAVED NIFTY", font=ImageFont.truetype(FONT_PATH, 34), fill=(255, 255, 255, 255))

    im_final = im.convert("RGB")
    im_final.save(out_path, quality=95)
    print(f"✅ FII Exodus Viral Thumbnail created: {out_path}")
    return out_path


def upload_thumbnail_to_youtube(video_id: str, thumb_path: Path):
    from googleapiclient.http import MediaFileUpload
    print(f"\n🚀 Uploading thumbnail {thumb_path.name} to YouTube video {video_id}...")
    uploader = YouTubeUploader()
    service = uploader._get_service("en")
    res = service.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(str(thumb_path), mimetype="image/jpeg")
    ).execute()
    print(f"🎉 Thumbnail successfully set on YouTube for {video_id}!")
    return res

if __name__ == "__main__":
    t1 = create_ai_bubble_thumbnail()
    t2 = create_luna_thumbnail()
    t3 = create_fii_exodus_thumbnail()

    if "--upload" in sys.argv:
        # Video 1: AI Wall
        upload_thumbnail_to_youtube("xMVcsq_f36U", t1)
        # Video 2: Luna
        upload_thumbnail_to_youtube("C-c3KJ6te2M", t2)

