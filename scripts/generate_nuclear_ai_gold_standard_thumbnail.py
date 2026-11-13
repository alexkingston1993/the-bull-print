#!/usr/bin/env python3
"""
Generate Viral CTR Thumbnail for Doc 03:
'Big Tech's Nuclear Secret: The Race for Atomic Megawatts'
Built strictly adhering to the 4-Pillar Gold Standard:
1. Split-Screen Tension: Left Blackout/Overheating Datacenter vs. Right Glowing Atomic Reactor & Megawatts
2. 3D Metallic Beveled Typography in Top-Center Safe Zone (Chrome White + Radiant Gold)
3. High-Friction Distress Stamp Badge: [POWER SHOCKER!] in lower left
4. Cinematic Spark Embers, Lightning Arcs & Volumetric Cherenkov Blue Lighting
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math

BASE_DIR = Path(__file__).resolve().parent.parent
FONT_DIR = BASE_DIR / "assets" / "fonts"
FONT_PATH = str(FONT_DIR / "Impact.ttf")

THUMB_W = 1280
THUMB_H = 720

def draw_3d_text(draw, pos, text, font, face_color=(255, 255, 255, 255), extrusion_color=(10, 15, 25, 255), extrusion_depth=16, stroke_width=6, stroke_color=(0, 0, 0, 255)):
    x, y = pos
    # Draw extrusion shadow layers downwards and right
    for i in range(extrusion_depth, 0, -1):
        offset_x = x + int(i * 0.8)
        offset_y = y + i
        draw.text((offset_x, offset_y), text, font=font, fill=extrusion_color, stroke_width=stroke_width, stroke_fill=extrusion_color)

    # Ambient black outline
    draw.text((x, y), text, font=font, fill=face_color, stroke_width=stroke_width + 2, stroke_fill=(0, 0, 0, 255))
    # Beveled face
    draw.text((x, y), text, font=font, fill=face_color, stroke_width=stroke_width, stroke_fill=stroke_color)


def create_nuclear_ai_thumbnail() -> Path:
    out_path = BASE_DIR / "output" / "thumbnails" / "thumb_nuclear_ai_viral_ctr.jpg"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Base Canvas
    im = Image.new("RGBA", (THUMB_W, THUMB_H), (10, 14, 22, 255))

    # Base plates if available
    cand_left = BASE_DIR / "output" / "nuclear_ai_documentary" / "frames" / "seg_01_beat_4.jpg"
    cand_right = BASE_DIR / "output" / "nuclear_ai_documentary" / "frames" / "seg_01_beat_2.jpg"

    # Split background:
    # Left side: Crisis / Datacenter thermal strain
    if cand_left.exists():
        im_l = Image.open(cand_left).convert("RGBA")
        im_l = im_l.resize((THUMB_W // 2 + 100, THUMB_H), Image.Resampling.LANCZOS)
        # Deep crimson/amber crisis grading
        enh = ImageEnhance.Color(im_l)
        im_l = enh.enhance(1.4)
        im.paste(im_l, (0, 0))

    # Right side: Power / Atomic energy
    if cand_right.exists():
        im_r = Image.open(cand_right).convert("RGBA")
        im_r = im_r.resize((THUMB_W // 2 + 100, THUMB_H), Image.Resampling.LANCZOS)
        enh = ImageEnhance.Brightness(im_r)
        im_r = enh.enhance(1.1)
        im.paste(im_r, (THUMB_W // 2 - 50, 0))

    # Gradient & Vignette Overlay
    grad = Image.new("RGBA", (THUMB_W, THUMB_H), (0, 0, 0, 0))
    d_grad = ImageDraw.Draw(grad)

    # Left crisis red/dark tint
    for x in range(THUMB_W // 2):
        factor = 1.0 - (x / (THUMB_W // 2))
        alpha = int(190 * (factor ** 0.9))
        d_grad.line([(x, 0), (x, THUMB_H)], fill=(130, 10, 20, alpha // 2))

    # Right atomic cyan tint
    for x in range(THUMB_W // 2, THUMB_W):
        factor = (x - THUMB_W // 2) / (THUMB_W // 2)
        alpha = int(120 * factor)
        d_grad.line([(x, 0), (x, THUMB_H)], fill=(0, 210, 255, alpha // 4))

    # Top dark vignette for typography legibility
    for y in range(260):
        factor = 1.0 - (y / 260.0)
        alpha = int(240 * (factor ** 1.1))
        d_grad.line([(0, y), (THUMB_W, y)], fill=(5, 8, 15, alpha))

    # Bottom dark vignette for badge legibility
    for y in range(THUMB_H - 180, THUMB_H):
        factor = (y - (THUMB_H - 180)) / 180.0
        alpha = int(220 * factor)
        d_grad.line([(0, y), (THUMB_W, y)], fill=(5, 8, 15, alpha))

    im = Image.alpha_composite(im, grad)

    # Electric Lightning / Energy Arcs Layer
    fx_layer = Image.new("RGBA", (THUMB_W, THUMB_H), (0, 0, 0, 0))
    d_fx = ImageDraw.Draw(fx_layer)

    # Slicing electric arc separating left and right
    split_pts = [
        (660, 0), (645, 150), (670, 280), (630, 420), (660, 560), (640, 720)
    ]
    for w, a in [(16, 50), (10, 100), (6, 180), (3, 255)]:
        d_fx.line(split_pts, fill=(0, 240, 255, a), width=w, joint="curve")

    # Upward bursting green/cyan candlestick breakout curve on the right
    chart_pts = [
        (720, 520), (810, 480), (890, 510), (980, 360),
        (1060, 380), (1140, 220), (1220, 130)
    ]
    for w, a in [(14, 60), (10, 120), (6, 200), (4, 255)]:
        d_fx.line(chart_pts, fill=(16, 225, 140, a), width=w, joint="curve")

    blur_fx = fx_layer.filter(ImageFilter.GaussianBlur(10))
    im = Image.alpha_composite(im, blur_fx)
    im = Image.alpha_composite(im, fx_layer)

    # Spark Embers on Right Side
    ember_layer = Image.new("RGBA", (THUMB_W, THUMB_H), (0, 0, 0, 0))
    d_emb = ImageDraw.Draw(ember_layer)
    import random
    random.seed(42)
    for _ in range(70):
        ex = random.randint(700, 1250)
        ey = random.randint(100, 680)
        er = random.randint(2, 5)
        d_emb.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(255, random.randint(180, 240), 50, random.randint(120, 255)))
    im = Image.alpha_composite(im, ember_layer)

    # 3D Metallic Typography (Top Center Safe Zone)
    draw = ImageDraw.Draw(im)
    f_huge = ImageFont.truetype(FONT_PATH, 115)
    f_badge = ImageFont.truetype(FONT_PATH, 34)

    # Line 1: BIG TECH'S (Chrome White Metallic Bevel)
    t1 = "BIG TECH'S"
    w1 = int(draw.textlength(t1, font=f_huge))
    x1 = (THUMB_W - w1) // 2
    draw_3d_text(draw, (x1, 55), t1, f_huge, face_color=(255, 255, 255, 255), extrusion_color=(20, 30, 45, 255), extrusion_depth=16, stroke_width=6)

    # Line 2: ATOMIC BET (Radiant Saffron Gold Bevel)
    t2 = "ATOMIC BET"
    w2 = int(draw.textlength(t2, font=f_huge))
    x2 = (THUMB_W - w2) // 2
    draw_3d_text(draw, (x2, 175), t2, f_huge, face_color=(255, 215, 0, 255), extrusion_color=(160, 90, 0, 255), extrusion_depth=16, stroke_width=6)

    # Specular Lens Glint on Text (Top corner of 'T')
    glint_x, glint_y = x2 + 10, 185
    draw.ellipse([glint_x - 12, glint_y - 12, glint_x + 12, glint_y + 12], fill=(255, 255, 255, 240))
    draw.line([(glint_x - 28, glint_y), (glint_x + 28, glint_y)], fill=(255, 255, 255, 220), width=3)
    draw.line([(glint_x, glint_y - 28), (glint_x, glint_y + 28)], fill=(255, 255, 255, 220), width=3)

    # Lower-Left Friction Distress Stamp Badge: [POWER SHOCKER!]
    bx, by = 60, 570
    badge_text = "POWER SHOCKER!"
    b_len = int(draw.textlength(badge_text, font=f_badge))
    # Outer distress border
    draw.rounded_rectangle([bx, by, bx + b_len + 40, by + 58], radius=8, fill=(215, 20, 35, 240), outline=(255, 255, 255, 220), width=3)
    # Inner dashed line effect
    draw.rounded_rectangle([bx + 4, by + 4, bx + b_len + 36, by + 54], radius=6, outline=(255, 255, 255, 160), width=1)
    draw.text((bx + 20, by + 10), badge_text, font=f_badge, fill=(255, 255, 255, 255))

    # Sub-callout on right side: "THE 2030 MEGAWATT RACE"
    sub_text = "THE 2030 MEGAWATT RACE"
    f_sub = ImageFont.truetype(FONT_PATH, 30)
    sw = int(draw.textlength(sub_text, font=f_sub))
    sx, sy = THUMB_W - sw - 70, 635
    draw.rounded_rectangle([sx - 16, sy - 6, sx + sw + 16, sy + 44], radius=8, fill=(10, 25, 35, 220), outline=(0, 220, 255, 200), width=2)
    draw.text((sx, sy), sub_text, font=f_sub, fill=(0, 240, 255, 255))

    im_rgb = im.convert("RGB")
    im_rgb.save(out_path, quality=98)
    print(f"✅ Generated Nuclear AI Gold Standard Thumbnail: {out_path}")
    return out_path

if __name__ == "__main__":
    create_nuclear_ai_thumbnail()
