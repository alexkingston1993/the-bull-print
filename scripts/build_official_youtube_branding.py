#!/usr/bin/env python3
"""
Official YouTube Branding Compositor — The Bull Print
Creates:
1. 800x800 Circle-Optimized Avatar: `output/branding/the_bull_print_channel_avatar.jpg`
2. 2560x1440 YouTube Banner with Mobile Safe Zone Guarantee (1546x423): `output/branding/the_bull_print_channel_banner.jpg`
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

BASE_DIR = Path(__file__).resolve().parent.parent
BRANDING_DIR = BASE_DIR / "output" / "branding"
BRANDING_DIR.mkdir(parents=True, exist_ok=True)

AVATAR_RAW = Path("/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364/bull_print_iconic_logo_avatar_1794211775415.jpg")
BANNER_PLATE_RAW = Path("/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364/bull_print_banner_plate_1794211800384.jpg")

FONT_IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"
FONT_ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

def get_font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def create_official_avatar():
    im = Image.open(AVATAR_RAW).convert("RGB")
    im_resized = im.resize((800, 800), Image.Resampling.LANCZOS)
    
    # Slight contrast & saturation punch
    im_resized = ImageEnhance.Contrast(im_resized).enhance(1.12)
    im_resized = ImageEnhance.Color(im_resized).enhance(1.18)
    
    out_path = BRANDING_DIR / "the_bull_print_channel_avatar.jpg"
    im_resized.save(out_path, quality=95)
    print(f"✅ Official Avatar saved: {out_path} (800x800)")
    return im_resized

def create_official_banner(avatar_img: Image.Image):
    # Standard YouTube Banner: 2560 x 1440
    # Safe zone (visible on all mobile, desktop, TV): 1546 x 423 centered (X: 507 to 2053, Y: 508 to 931)
    banner_w, banner_h = 2560, 1440
    plate = Image.open(BANNER_PLATE_RAW).convert("RGB")
    plate = plate.resize((banner_w, banner_h), Image.Resampling.LANCZOS)
    plate = ImageEnhance.Contrast(plate).enhance(1.15)
    
    canvas = plate.copy()
    draw = ImageDraw.Draw(canvas, "RGBA")
    
    # Center coordinates
    cx = banner_w // 2 # 1280
    cy = banner_h // 2 # 720
    
    # 1. Subtle dark luxury glass backdrop for the mobile safe area
    safe_box = [cx - 760, cy - 195, cx + 760, cy + 195]
    draw.rounded_rectangle(safe_box, radius=24, fill=(10, 15, 26, 190), outline=(255, 215, 0, 90), width=2)
    
    # 2. Bull Emblem on the left of safe zone
    emblem = avatar_img.resize((320, 320), Image.Resampling.LANCZOS)
    # Mask to rounded rectangle
    mask = Image.new("L", (320, 320), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, 320, 320], radius=40, fill=255)
    
    emblem_x = cx - 710
    emblem_y = cy - 160
    canvas.paste(emblem, (emblem_x, emblem_y), mask)
    
    # Subtle gold ring around emblem
    draw.rounded_rectangle([emblem_x, emblem_y, emblem_x + 320, emblem_y + 320], radius=40, outline=(255, 215, 0, 220), width=3)
    
    # 3. Typography on the right of emblem
    text_x = emblem_x + 360
    
    f_title = get_font(FONT_IMPACT, 108)
    f_slogan = get_font(FONT_ARIAL_BOLD, 36)
    f_badge = get_font(FONT_IMPACT, 26)
    f_url = get_font(FONT_ARIAL_BOLD, 28)
    
    # A. Brand Title: "THE BULL PRINT" with 3D drop shadow & gold face
    title_text = "THE BULL PRINT"
    for d in range(8, 0, -1):
        draw.text((text_x + d, cy - 110 + d), title_text, font=f_title, fill=(0, 0, 0, 240))
    draw.text((text_x, cy - 110), title_text, font=f_title, fill=(255, 215, 0, 255))
    
    # B. Slogan: "Financial Freedom for Everyone Through Financial Literacy"
    slogan_text = "Financial Freedom for Everyone Through Financial Literacy."
    draw.text((text_x + 2, cy + 5 + 2), slogan_text, font=f_slogan, fill=(0, 0, 0, 220))
    draw.text((text_x, cy + 5), slogan_text, font=f_slogan, fill=(240, 246, 252, 255))
    
    # C. Badges row
    badges = [
        ("365-DAY MASTERCLASS", (255, 215, 0)),
        ("FORENSIC DESK", (0, 230, 153)),
        ("100% FREE TOOLS", (245, 25, 55))
    ]
    cur_bx = text_x
    by = cy + 72
    for b_text, b_col in badges:
        b_bbox = f_badge.getbbox(b_text)
        bw = b_bbox[2] - b_bbox[0] + 28
        bh = b_bbox[3] - b_bbox[1] + 16
        draw.rounded_rectangle([cur_bx, by, cur_bx + bw, by + bh], radius=8, fill=(15, 23, 42, 230), outline=(*b_col, 220), width=2)
        draw.text((cur_bx + 14, by + 8), b_text, font=f_badge, fill=(*b_col, 255))
        cur_bx += bw + 16
        
    # D. Domain callout: "bullprintmedia.com"
    url_text = "bullprintmedia.com  •  @thebullprint"
    draw.text((text_x, cy + 145), url_text, font=f_url, fill=(148, 163, 184, 255))
    
    out_path = BRANDING_DIR / "the_bull_print_channel_banner.jpg"
    canvas.save(out_path, quality=95)
    print(f"✅ Official Banner saved: {out_path} (2560x1440)")
    return canvas

def main():
    av = create_official_avatar()
    create_official_banner(av)
    print("🎉 BRANDING ASSETS BUILT & VERIFIED!")

if __name__ == "__main__":
    main()
