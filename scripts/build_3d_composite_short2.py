"""
⚡ 3D HYBRID COMPOSITOR — The Bull Print
Generates 1080x1920 3D photorealistic master plates for YouTube Shorts.
Combines genuine 3D Octane master renders with multi-pass 3D extruded metallic typography,
ambient bloom glow, and neon warning pills. Zero flat 2D lines or boxes.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

BASE_DIR = Path(__file__).resolve().parent.parent

# Typography fonts
FONT_IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"
FONT_ARIAL_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

def get_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    for path in [FONT_IMPACT, FONT_ARIAL_BLACK]:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_3d_extruded_text(
    canvas: Image.Image,
    text: str,
    xy: tuple,
    font: ImageFont.FreeTypeFont,
    face_color: tuple = (255, 255, 255),
    shadow_color: tuple = (15, 23, 42),
    extrude_color: tuple = (180, 83, 9),
    glow_color: tuple = (245, 158, 11),
    depth: int = 12,
    glow_radius: int = 16,
    bevel_highlight: bool = True
):
    """
    Renders multi-pass 3D extruded metallic typography with ambient bloom glow.
    """
    x, y = xy
    w, h = canvas.size

    # 1. Ambient Glow (Rendered to alpha layer and blurred)
    glow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.text((x, y + depth // 2), text, font=font, fill=(*glow_color, 220), anchor="mm")
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(glow_radius))
    canvas.paste(glow_layer, (0, 0), glow_layer)

    # 2. Deep Drop Shadow
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.text((x + 6, y + depth + 8), text, font=font, fill=(0, 0, 0, 240), anchor="mm")
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(8))
    canvas.paste(shadow_layer, (0, 0), shadow_layer)

    # 3. 3D Extrusion Layers (Bottom to Top with Shading)
    draw = ImageDraw.Draw(canvas)
    for i in range(depth, 0, -1):
        ratio = i / depth
        # Gradient between extrude_color and shadow_color
        r = int(extrude_color[0] * (1 - ratio * 0.7) + shadow_color[0] * (ratio * 0.7))
        g = int(extrude_color[1] * (1 - ratio * 0.7) + shadow_color[1] * (ratio * 0.7))
        b = int(extrude_color[2] * (1 - ratio * 0.7) + shadow_color[2] * (ratio * 0.7))
        draw.text((x, y + i), text, font=font, fill=(r, g, b, 255), anchor="mm")

    # 4. Front Face (Metallic fill with dark outline)
    # Dark rim outline
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
        draw.text((x + dx, y + dy), text, font=font, fill=(10, 10, 15, 255), anchor="mm")

    # Pure Face
    draw.text((x, y), text, font=font, fill=(*face_color, 255), anchor="mm")

    # 5. Top Bevel Chrome Highlight (1px up/left offset)
    if bevel_highlight:
        draw.text((x - 1, y - 1), text, font=font, fill=(255, 255, 255, 180), anchor="mm")

def draw_neon_pill(
    canvas: Image.Image,
    text: str,
    xy: tuple,
    font: ImageFont.FreeTypeFont,
    pill_color: tuple = (239, 68, 68),
    bg_color: tuple = (15, 23, 42, 220)
):
    """
    Renders an ultra-crisp neon glass warning badge pill.
    """
    x, y = xy
    draw = ImageDraw.Draw(canvas, "RGBA")
    bbox = font.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 28, 14
    box = [x - tw // 2 - pad_x, y - th // 2 - pad_y, x + tw // 2 + pad_x, y + th // 2 + pad_y]

    # Pill background
    draw.rounded_rectangle(box, radius=24, fill=bg_color, outline=(*pill_color, 255), width=3)
    # Pill text
    draw.text((x, y), text, font=font, fill=(*pill_color, 255), anchor="mm")

def render_composite_frame(
    base_image_path: str,
    badge_text: str,
    headline_line1: str,
    headline_line2: str,
    metric_text: str,
    theme: str,
    output_path: Path
):
    """
    Composites a 1080x1920 3D photorealistic master frame.
    """
    # 1. Load and conform base image to 1080x1920
    im = Image.open(base_image_path).convert("RGBA")
    w, h = im.size
    target_w, target_h = 1080, 1920

    # Center crop / scale to fill target
    scale = max(target_w / w, target_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    im = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    im = im.crop((left, top, left + target_w, top + target_h))

    # 2. Add cinematic top & bottom gradient overlays
    # Top overlay is solid dark from y=0 to y=520, smoothly fading to transparent by y=680
    grad = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grad)
    for y in range(680):
        if y <= 500:
            alpha = 255
        else:
            alpha = int(255 * (1 - ((y - 500) / 180) ** 1.4))
        g_draw.line([(0, y), (target_w, y)], fill=(6, 9, 18, alpha))

    # Bottom overlay for metric data card (solid dark behind card)
    for y in range(1580, target_h):
        if y >= 1650:
            alpha = 255
        else:
            alpha = int(255 * (((y - 1580) / 70) ** 1.2))
        g_draw.line([(0, y), (target_w, y)], fill=(6, 9, 18, alpha))
    im = Image.alpha_composite(im, grad)

    # 3. Theme color definitions
    if theme == "crimson_fire":
        pill_col = (239, 68, 68)      # Neon red
        face_col = (255, 241, 242)     # Pearl silver
        extrude_col = (185, 28, 28)    # Deep red
        glow_col = (220, 38, 38)       # Red bloom
        metric_col = (252, 165, 165)
    elif theme == "electric_gold":
        pill_col = (245, 158, 11)     # Amber gold
        face_col = (254, 240, 138)     # Bright gold
        extrude_col = (180, 83, 9)     # Bronze
        glow_col = (245, 158, 11)      # Gold bloom
        metric_col = (253, 230, 138)
    elif theme == "cyan_cyber":
        pill_col = (6, 182, 212)       # Electric cyan
        face_col = (207, 250, 254)     # Ice white
        extrude_col = (14, 116, 144)   # Deep cyan
        glow_col = (6, 182, 212)       # Cyan bloom
        metric_col = (165, 243, 252)
    else: # emerald_surge
        pill_col = (16, 185, 129)      # Emerald green
        face_col = (209, 250, 229)     # Mint pearl
        extrude_col = (4, 120, 87)     # Deep emerald
        glow_col = (16, 185, 129)      # Green bloom
        metric_col = (167, 243, 208)

    # 4. Badge / Warning Pill (y = 190)
    font_badge = get_font(36)
    draw_neon_pill(im, badge_text, (target_w // 2, 190), font_badge, pill_color=pill_col)

    # 5. 3D Extruded Metallic Headlines (y = 300 and 410)
    font_head = get_font(105)
    draw_3d_extruded_text(
        im, headline_line1, (target_w // 2, 305), font_head,
        face_color=face_col, extrude_color=extrude_col, glow_color=glow_col, depth=14
    )
    draw_3d_extruded_text(
        im, headline_line2, (target_w // 2, 415), font_head,
        face_color=face_col, extrude_color=extrude_col, glow_color=glow_col, depth=14
    )

    # 6. Lower Data Metric Banner (y = 1720)
    font_metric_lbl = get_font(30)
    font_metric_val = get_font(44)
    card_w, card_h = 880, 130
    cx, cy = target_w // 2, 1720
    card_box = [cx - card_w // 2, cy - card_h // 2, cx + card_w // 2, cy + card_h // 2]
    
    # Glass backdrop for metric card
    card_draw = ImageDraw.Draw(im, "RGBA")
    card_draw.rounded_rectangle(card_box, radius=20, fill=(10, 15, 30, 230), outline=(*pill_col, 220), width=3)
    card_draw.text((cx, cy - 24), "INSTITUTIONAL FOOTPRINT SIGNAL", font=font_metric_lbl, fill=(148, 163, 184, 255), anchor="mm")
    card_draw.text((cx, cy + 24), metric_text, font=font_metric_val, fill=(*metric_col, 255), anchor="mm")

    # 7. Convert to RGB and apply Unsharp Mask for 8K-like crispness
    final_rgb = im.convert("RGB")
    final_rgb = final_rgb.filter(ImageFilter.UnsharpMask(radius=1.5, percent=130, threshold=2))

    # Save high quality JPEG
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_rgb.save(output_path, "JPEG", quality=95, optimize=True)
    print(f"✅ Generated 3D Master Plate: {output_path.name} ({round(output_path.stat().st_size / 1024)} KB)")

SECTIONS = [
    {
        "index": 0,
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/siphon_hud_concept_1793450023460.jpg",
        "badge_text": "[!] INSTITUTIONAL TRAP",
        "headline_line1": "LIQUIDITY POOL",
        "headline_line2": "SUPPORT BREACHED",
        "metric_text": "24,500 BREAKDOWN >> TRAP ACTIVE",
        "theme": "crimson_fire",
    },
    {
        "index": 1,
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/short_scene_2_trading_1793439809089.jpg",
        "badge_text": "[ALERT] STOP-LOSS HUNT",
        "headline_line1": "SWEEP TRIGGERED",
        "headline_line2": "STOPS HUNTED",
        "metric_text": "EXECUTION TIME: 120ms MASS FLUSH",
        "theme": "electric_gold",
    },
    {
        "index": 2,
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/vivid_trading_9_16_1793452007846.jpg",
        "badge_text": "[ABSORPTION] LIMIT WALL",
        "headline_line1": "DELTA COLLAPSE",
        "headline_line2": "-45,000 CONTRACTS",
        "metric_text": "INSTITUTIONAL ABSORPTION DETECTED",
        "theme": "cyan_cyber",
    },
    {
        "index": 3,
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/short_scene_3_vault_1793439853059.jpg",
        "badge_text": "[TRAP] RETAIL EXIT",
        "headline_line1": "FALSE BREAKDOWN",
        "headline_line2": "90% LIQUIDATED",
        "metric_text": "PANIC SELLERS SERVE AS EXIT LIQUIDITY",
        "theme": "crimson_fire",
    },
    {
        "index": 4,
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/vivid_vault_9_16_1793452060059.jpg",
        "badge_text": "[REVERSAL] SHORT SQUEEZE",
        "headline_line1": "V-SHAPE SURGE",
        "headline_line2": "+180 PTS SQUEEZE",
        "metric_text": "TRAPPED SHORTS FORCED TO COVER",
        "theme": "emerald_surge",
    },
    {
        "index": 5,
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/short_scene_1_penthouse_1793439768921.jpg",
        "badge_text": "[VERDICT] INSTITUTIONAL RULE",
        "headline_line1": "FOLLOW FOOTPRINTS",
        "headline_line2": "NEVER BREAKOUTS",
        "metric_text": "TRADE WITH THE WHALES OR BECOME FOOD",
        "theme": "electric_gold",
    },
]

def main():
    target_dir = BASE_DIR / "assets" / "approved_bundles" / "nifty-50-liquidity-sweep-rules-&-institutional-s"
    print(f"🚀 Generating 6 Bespoke 3D Master Plates in: {target_dir}")
    for sec in SECTIONS:
        out_file = target_dir / f"frame_{sec['index']:02d}.jpg"
        render_composite_frame(
            base_image_path=sec["base_image"],
            badge_text=sec["badge_text"],
            headline_line1=sec["headline_line1"],
            headline_line2=sec["headline_line2"],
            metric_text=sec["metric_text"],
            theme=sec["theme"],
            output_path=out_file
        )

if __name__ == "__main__":
    main()

