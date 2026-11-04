"""
⚡ HIGH-CTR THUMBNAIL FRAME STUDIO — The Bull Print
Automated Split-Section 9:16 High-CTR Background Frame Generator for YouTube Shorts.

Replaces legacy Playwright chart capturing with explosive, hyper-aesthetic 9:16 thumbnail frames.
- Splits a Short into dynamic visual sections (e.g. 6s per section -> 10 frames for a 60s short, 6 for 36s).
- Each split section uses its narrative script/beat to render an explosive high-CTR 1080x1920 thumbnail.
- Guarantees that WHICHEVER frame YouTube's Shorts algorithm picks as the auto-thumbnail,
  it displays a world-class, high-CTR, click-compelling thumbnail.
- Features:
    * 3D Extruded Metallic Typography (Gold, Silver, Crimson, Emerald, Solana Purple/Cyan).
    * Multi-layered glow auras, directional lighting, and drop shadows.
    * Glowing warning pills & multiplier badges ("99% LIQUIDATED", "MEV TRAP ⚠️", "EXPOSED!").
    * Procedural 3D scene elements: Neon candlestick lightning, glowing crypto tokens, laser grids, dark vignettes.
"""

import os
import math
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output"

# ---------------------------------------------------------------- Font Discovery
def _get_font(font_size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    candidate_paths = [
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/System/Library/Fonts/Supplemental/Arial Black.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for p in candidate_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, font_size)
            except Exception:
                continue
    return ImageFont.load_default()


# ---------------------------------------------------------------- Color Palettes
PALETTES = {
    "solana_purple": {
        "bg_top": (15, 6, 30),
        "bg_bot": (4, 1, 10),
        "glow_color": (153, 69, 255),      # Solana Purple #9945FF
        "accent_secondary": (20, 241, 149), # Solana Green #14F195
        "text_top": ((255, 255, 255), (200, 160, 255), (153, 69, 255)),
        "text_bot": ((255, 255, 255), (100, 255, 200), (20, 241, 149)),
        "pill_bg": (153, 69, 255),
        "pill_border": (255, 255, 255),
    },
    "blood_red": {
        "bg_top": (35, 5, 8),
        "bg_bot": (8, 1, 2),
        "glow_color": (255, 40, 40),
        "accent_secondary": (255, 140, 0),
        "text_top": ((255, 255, 255), (255, 180, 180), (255, 40, 40)),
        "text_bot": ((255, 255, 255), (255, 220, 100), (245, 158, 11)),
        "pill_bg": (220, 20, 30),
        "pill_border": (255, 80, 80),
    },
    "gold_bull": {
        "bg_top": (30, 20, 5),
        "bg_bot": (6, 5, 1),
        "glow_color": (250, 204, 21),
        "accent_secondary": (245, 158, 11),
        "text_top": ((255, 255, 255), (255, 235, 130), (250, 204, 21)),
        "text_bot": ((255, 255, 255), (226, 232, 240), (148, 163, 184)),
        "pill_bg": (217, 119, 6),
        "pill_border": (253, 224, 71),
    },
    "toxic_green": {
        "bg_top": (5, 28, 15),
        "bg_bot": (1, 8, 4),
        "glow_color": (16, 185, 129),
        "accent_secondary": (52, 211, 153),
        "text_top": ((255, 255, 255), (180, 255, 210), (16, 185, 129)),
        "text_bot": ((255, 255, 255), (255, 240, 120), (250, 204, 21)),
        "pill_bg": (5, 150, 90),
        "pill_border": (110, 231, 183),
    },
    "lightning_cyan": {
        "bg_top": (5, 20, 35),
        "bg_bot": (1, 5, 12),
        "glow_color": (14, 165, 233),
        "accent_secondary": (56, 189, 248),
        "text_top": ((255, 255, 255), (180, 230, 255), (14, 165, 233)),
        "text_bot": ((255, 255, 255), (255, 120, 120), (239, 68, 68)),
        "pill_bg": (2, 132, 199),
        "pill_border": (125, 211, 252),
    },
}

PALETTE_KEYS = list(PALETTES.keys())


def _draw_linear_gradient(draw: ImageDraw.ImageDraw, width: int, height: int, top_color: Tuple[int, int, int], bot_color: Tuple[int, int, int]):
    for y in range(height):
        factor = y / height
        r = int(top_color[0] + factor * (bot_color[0] - top_color[0]))
        g = int(top_color[1] + factor * (bot_color[1] - top_color[1]))
        b = int(top_color[2] + factor * (bot_color[2] - top_color[2]))
        draw.line([(0, y), (width, y)], fill=(r, g, b))


def _draw_atmospheric_grid_and_candlesticks(draw: ImageDraw.ImageDraw, width: int, height: int, theme: Dict[str, Any], seed: int = 42):
    rnd = random.Random(seed)
    grid_color = (*theme["glow_color"][:3], 24)
    # Background subtle perspective grid
    grid_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grid_overlay)
    
    # Horizontal grid lines
    for y in range(200, height - 100, 120):
        alpha = int(18 + 15 * math.sin(y / height * math.pi))
        gdraw.line([(0, y), (width, y)], fill=(*theme["glow_color"][:3], alpha), width=1)
    
    # Vertical grid lines
    for x in range(60, width, 120):
        gdraw.line([(x, 150), (x, height - 100)], fill=(*theme["glow_color"][:3], 15), width=1)
    
    # Dramatic falling/spiking candlesticks in background
    for i in range(16):
        cx = 70 + i * 62
        is_red = rnd.random() < 0.65
        candle_col = (255, 50, 50, 110) if is_red else (*theme["accent_secondary"][:3], 110)
        c_top = rnd.randint(height // 2 - 200, height // 2 + 350)
        c_height = rnd.randint(30, 180)
        wick_top = max(100, c_top - rnd.randint(20, 80))
        wick_bot = min(height - 100, c_top + c_height + rnd.randint(20, 80))
        
        # Draw wick
        gdraw.line([(cx, wick_top), (cx, wick_bot)], fill=candle_col, width=2)
        # Draw body
        gdraw.rectangle([(cx - 10, c_top), (cx + 10, c_top + c_height)], fill=candle_col)

    return grid_overlay


def _draw_radial_glow(width: int, height: int, center_x: int, center_y: int, radius: int, glow_color: Tuple[int, int, int]) -> Image.Image:
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    for r in range(radius, 0, -18):
        alpha = int(45 * (1.0 - (r / radius)) ** 1.8)
        bbox = [center_x - r, center_y - r, center_x + r, center_y + r]
        gdraw.ellipse(bbox, fill=(*glow_color, alpha))
    return glow


def _render_3d_metallic_line(
    canvas: Image.Image,
    text: str,
    pos_y: int,
    font: ImageFont.FreeTypeFont,
    gradient: Tuple[Tuple[int, int, int], Tuple[int, int, int], Tuple[int, int, int]],
    glow_color: Tuple[int, int, int],
    depth: int = 14,
) -> int:
    """
    Renders hyper-punchy 3D metallic extruded text with multi-pass drop shadow,
    bevel highlights, and vibrant neon outer glow.
    """
    width, height = canvas.size
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Calculate centered bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    t_w = bbox[2] - bbox[0]
    t_h = bbox[3] - bbox[1]
    pos_x = (width - t_w) // 2

    # 1. Outer Neon Glow
    glow_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    for offset in range(8, 0, -2):
        glow_draw.text((pos_x, pos_y), text, font=font, fill=(*glow_color, 25))
    glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(radius=10))
    canvas.alpha_composite(glow_overlay)

    # 2. Deep 3D Extrusion (Black to dark tone downward shadow)
    for d in range(depth, 0, -1):
        darkness = int(12 + 10 * (d / depth))
        draw.text((pos_x + d // 2, pos_y + d), text, font=font, fill=(darkness, darkness, darkness, 255))

    # 3. Text Body with Vertical Gradient
    text_mask = Image.new("L", (t_w + 20, t_h + 20), 0)
    tmask_draw = ImageDraw.Draw(text_mask)
    tmask_draw.text((10 - bbox[0], 10 - bbox[1]), text, font=font, fill=255)

    gradient_tile = Image.new("RGBA", (t_w + 20, t_h + 20))
    g_draw = ImageDraw.Draw(gradient_tile)
    for y in range(t_h + 20):
        f = y / max(1, t_h + 20)
        if f < 0.5:
            f2 = f * 2.0
            r = int(gradient[0][0] + f2 * (gradient[1][0] - gradient[0][0]))
            g = int(gradient[0][1] + f2 * (gradient[1][1] - gradient[0][1]))
            b = int(gradient[0][2] + f2 * (gradient[1][2] - gradient[0][2]))
        else:
            f2 = (f - 0.5) * 2.0
            r = int(gradient[1][0] + f2 * (gradient[2][0] - gradient[1][0]))
            g = int(gradient[1][1] + f2 * (gradient[2][1] - gradient[1][1]))
            b = int(gradient[1][2] + f2 * (gradient[2][2] - gradient[1][2]))
        g_draw.line([(0, y), (t_w + 20, y)], fill=(r, g, b, 255))

    gradient_tile.putalpha(text_mask)
    canvas.paste(gradient_tile, (pos_x - 10 + bbox[0], pos_y - 10 + bbox[1]), gradient_tile)

    # 4. Top Crisp Specular Bevel Line
    spec_draw = ImageDraw.Draw(canvas)
    spec_draw.text((pos_x, pos_y - 1), text, font=font, fill=(255, 255, 255, 140))

    return pos_y + t_h


def _draw_warning_pill(
    canvas: Image.Image,
    badge_text: str,
    pos_y: int,
    theme: Dict[str, Any],
) -> int:
    """Renders high-visibility floating pill badge with border glow."""
    width, _ = canvas.size
    font = _get_font(46, bold=True)
    draw = ImageDraw.Draw(canvas)
    
    bbox = draw.textbbox((0, 0), badge_text, font=font)
    t_w = bbox[2] - bbox[0]
    t_h = bbox[3] - bbox[1]
    
    pad_x, pad_y = 38, 16
    pill_w = t_w + pad_x * 2
    pill_h = t_h + pad_y * 2
    pos_x = (width - pill_w) // 2
    
    # Outer glow
    pill_glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    pg_draw = ImageDraw.Draw(pill_glow)
    pg_draw.rounded_rectangle(
        [(pos_x - 6, pos_y - 6), (pos_x + pill_w + 6, pos_y + pill_h + 6)],
        radius=pill_h // 2,
        fill=(*theme["glow_color"][:3], 90)
    )
    pill_glow = pill_glow.filter(ImageFilter.GaussianBlur(radius=8))
    canvas.alpha_composite(pill_glow)
    
    # Pill body
    p_draw = ImageDraw.Draw(canvas)
    p_draw.rounded_rectangle(
        [(pos_x, pos_y), (pos_x + pill_w, pos_y + pill_h)],
        radius=pill_h // 2,
        fill=(*theme["pill_bg"][:3], 240),
        outline=(*theme["pill_border"][:3], 255),
        width=3
    )
    # Text
    tx = pos_x + pad_x - bbox[0]
    ty = pos_y + pad_y - bbox[1]
    p_draw.text((tx, ty), badge_text, font=font, fill=(255, 255, 255, 255))
    
    return pos_y + pill_h


def _draw_central_3d_anchor(canvas: Image.Image, symbol_type: str, theme: Dict[str, Any], center_y: int = 1080):
    """
    Renders a dramatic central 3D graphic anchor:
    - 'solana_token': glowing purple/green cyber-orb with Solana rays.
    - 'skull_trap': neon warning skull with laser eyes.
    - 'burning_chart': sharp descending crimson candlestick waterfall.
    - 'bot_siphon': vortex with circulating crypto coins & dollar signs.
    """
    width, height = canvas.size
    cx = width // 2
    cy = center_y
    draw = ImageDraw.Draw(canvas)
    
    # Central glow base
    glow = _draw_radial_glow(width, height, cx, cy, 380, theme["glow_color"][:3])
    canvas.alpha_composite(glow)
    
    anchor_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    adraw = ImageDraw.Draw(anchor_overlay)
    
    if symbol_type in ("solana_token", "crypto_orb"):
        # Concentric glowing rings
        for r, alpha in [(220, 50), (180, 80), (140, 140), (100, 210)]:
            adraw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(*theme["accent_secondary"][:3], alpha), width=5)
        # 3D inner coin face
        adraw.ellipse([cx - 85, cy - 85, cx + 85, cy + 85], fill=(*theme["glow_color"][:3], 200), outline=(255, 255, 255, 240), width=4)
        # Solana 3 parallel slanted bars
        bar_col = (20, 241, 149, 255)
        for offset_y in (-35, 0, 35):
            adraw.polygon([
                (cx - 50, cy + offset_y - 8),
                (cx + 40, cy + offset_y - 8),
                (cx + 50, cy + offset_y + 8),
                (cx - 40, cy + offset_y + 8),
            ], fill=bar_col)
            
    elif symbol_type in ("skull_trap", "mev_bot"):
        # Mechanical MEV bot skull & crosshairs
        # Target crosshairs
        adraw.ellipse([cx - 160, cy - 160, cx + 160, cy + 160], outline=(255, 40, 40, 140), width=3)
        adraw.line([(cx - 200, cy), (cx + 200, cy)], fill=(255, 40, 40, 180), width=2)
        adraw.line([(cx, cy - 200), (cx, cy + 200)], fill=(255, 40, 40, 180), width=2)
        # Skull silhouette
        adraw.ellipse([cx - 90, cy - 110, cx + 90, cy + 40], fill=(220, 20, 30, 220), outline=(255, 255, 255, 255), width=4)
        adraw.rectangle([cx - 50, cy + 30, cx + 50, cy + 90], fill=(200, 15, 25, 220), outline=(255, 255, 255, 255), width=3)
        # Glowing eye sockets
        adraw.ellipse([cx - 55, cy - 40, cx - 15, cy], fill=(0, 0, 0, 255), outline=(255, 255, 0, 255), width=2)
        adraw.ellipse([cx + 15, cy - 40, cx + 55, cy], fill=(0, 0, 0, 255), outline=(255, 255, 0, 255), width=2)
        # Teeth lines
        for tx in (-30, -10, 10, 30):
            adraw.line([(cx + tx, cy + 40), (cx + tx, cy + 80)], fill=(255, 255, 255, 240), width=3)
            
    elif symbol_type in ("burning_chart", "liquidation"):
        # Downward cascading blood-red lightning crash
        points = [
            (cx - 200, cy - 180),
            (cx - 80, cy - 100),
            (cx - 120, cy - 20),
            (cx + 20, cy + 60),
            (cx - 30, cy + 110),
            (cx + 160, cy + 220),
        ]
        for w, a in [(12, 100), (6, 200), (2, 255)]:
            adraw.line(points, fill=(255, 50, 50, a), width=w)
        # Red warning crash arrow
        adraw.polygon([
            (cx + 160, cy + 220),
            (cx + 110, cy + 180),
            (cx + 180, cy + 170),
        ], fill=(255, 255, 255, 255))
        
    else:  # bot siphon vortex
        # Swirling particle vortex
        for i in range(36):
            ang = i * 10 * math.pi / 180
            dist = 40 + i * 4.5
            px = cx + int(dist * math.cos(ang))
            py = cy + int(dist * math.sin(ang) * 0.6)
            col = theme["accent_secondary"] if i % 2 == 0 else theme["glow_color"]
            adraw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(*col[:3], 200))

    canvas.alpha_composite(anchor_overlay)


def build_flow_ai_prompt(
    section: Dict[str, Any],
    vertical: str = "crypto",
    is_short: bool = True
) -> str:
    """
    Constructs an AI prompt using Google Flow AI's 5-Part Systematic Blueprint:
    [Format & Aspect Ratio] + [Core Subject & Metaphor] + [Lighting & Color Strategy] + [Typography & Text Overlay] + [Composition & Finish]
    Enforces the single focal point rule, extreme contrast, and concise 2-4 word text hook.
    Guarantees every prompt is unique to prevent asset reuse across shorts.
    """
    ratio = "vertical 9:16 YouTube Short thumbnail" if is_short else "horizontal 16:9 YouTube video thumbnail"
    fmt = f"A high CTR viral {ratio}"

    # Subject & Metaphor
    subject = str(section.get("visual_metaphor") or section.get("symbol_type") or "").lower()
    if any(k in subject for k in ("token", "solana", "coin", "orb")):
        subj_str = "a single dramatic visual focal point of a shattered glowing 3D Solana coin melting into an industrial cyber-reactor funnel with volumetric liquid energy"
    elif any(k in subject for k in ("bot", "skull", "cartel", "hacker")):
        subj_str = "a single dramatic visual focal point of a high-tech metallic cyborg skull with glowing red optical sockets and fiber-optic tentacle network wires draining liquidity"
    elif any(k in subject for k in ("trap", "sandwich", "crusher", "jaw")):
        subj_str = "a single dramatic visual focal point of a massive industrial steel hydraulic bear-trap jaw with yellow hazard warning stripes clamping down and crushing cryptocurrency tokens with flying embers"
    elif any(k in subject for k in ("chart", "dump", "slippage", "arrow", "waterfall")):
        subj_str = "a single dramatic visual focal point of an intense red neon laser trendline arrow violently smashing through a dark cracked grid floor with explosive sparks and debris"
    else:
        subj_str = f"a single dramatic visual focal point of a 3D physical object representing {section.get('headline_top', 'MARKET TRAP')} with intricate mechanical detail"

    # Lighting & Color Strategy
    lighting = "Dark obsidian background #060912 paired with vivid high-saturation neon accents, intense volumetric rim lighting, glowing candlestick laser beams, and floating spark embers"

    # Typography & Text Overlay (2-4 Words concise)
    top_hook = section.get("headline_top", "MARKET TRAP").strip()
    mid_hook = section.get("headline_mid", "EXPOSED!").strip()
    short_hook = f"{top_hook} {mid_hook}"[:28]
    typo = f"bold 3D extruded metallic typography reading '{short_hook}' in brushed silver chrome and incandescent molten gold with inner flame lighting, floating neon pill badge reading '{section.get('badge_text', 'ALERT [!]')}'"

    # Composition & Finish
    finish = "hyper-detailed 3D octane render, ultra-sharp compositing, extreme visual contrast, clean composition zones, 8k resolution, cinematic depth of field"

    return f"{fmt}, {subj_str}, {lighting}, {typo}, {finish}"


# ---------------------------------------------------------------- Core Frame Generator
def generate_high_ctr_section_frame(
    section: Dict[str, Any],
    vertical: str = "crypto",
    width: int = 1080,
    height: int = 1920,
    output_path: Optional[Path] = None,
) -> Path:
    """
    Renders a single 1080x1920 High-CTR Thumbnail frame for a specific video section.
    """
    if output_path is None:
        output_path = OUTPUT_DIR / f"frame_{section.get('section_index', 0):02d}.jpg"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. 🛡️ Google Flow AI Master Bank Injection (2K Benchmark Reference)
    idx = section.get("section_index", 0)
    master_banks = [
        BASE_DIR / "assets" / "flow_ai_masters" / "crypto_mev" / f"frame_{idx:02d}.jpg",
        OUTPUT_DIR / "solana_mev_short" / "frames" / "revamped frames" / f"frame_{idx:02d}.jpg",
    ]
    for mb in master_banks:
        if mb.exists():
            with Image.open(mb) as m_im:
                if m_im.size != (width, height):
                    m_im = m_im.resize((width, height), Image.Resampling.LANCZOS)
                m_im.convert("RGB").save(output_path, "JPEG", quality=98)
                logger.success(f"🎨 [Flow AI Master Injected] {mb.name} -> {output_path.name} (1080x1920)")
                return output_path

    theme_key = section.get("theme") or PALETTE_KEYS[section.get("section_index", 0) % len(PALETTE_KEYS)]
    theme = PALETTES.get(theme_key, PALETTES["solana_purple"])
    
    # 1. Base Gradient Canvas
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    _draw_linear_gradient(draw, width, height, theme["bg_top"], theme["bg_bot"])
    
    # 2. Atmospheric Candlestick Grid
    grid = _draw_atmospheric_grid_and_candlesticks(draw, width, height, theme, seed=section.get("section_index", 0) + 101)
    img.alpha_composite(grid)
    
    # 3. Dramatic Central 3D Graphic Anchor
    symbol = section.get("symbol_type", "solana_token")
    _draw_central_3d_anchor(img, symbol, theme, center_y=1120)
    
    # 4. Floating Warning Pill (Top Anchor)
    badge_text = section.get("badge_text", "WARNING ⚠️")
    _draw_warning_pill(img, badge_text, pos_y=220, theme=theme)
    
    # 5. Bold 3D Metallic Hook Typography (Headline Line 1)
    top_font = _get_font(108, bold=True)
    line1_text = section.get("headline_top", "SOLANA SIPHON").upper()
    next_y = _render_3d_metallic_line(
        img,
        line1_text,
        pos_y=350,
        font=top_font,
        gradient=theme["text_top"],
        glow_color=theme["glow_color"][:3],
        depth=14
    )
    
    # 6. High-Contrast Sub-Hook Typography (Headline Line 2)
    mid_font = _get_font(92, bold=True)
    line2_text = section.get("headline_mid", "99% LIQUIDATED").upper()
    _render_3d_metallic_line(
        img,
        line2_text,
        pos_y=next_y + 24,
        font=mid_font,
        gradient=theme["text_bot"],
        glow_color=theme["accent_secondary"][:3],
        depth=12
    )

    # 7. Lower Section Statistic / Math Badge
    lower_badge = section.get("lower_badge")
    if lower_badge:
        _draw_warning_pill(img, lower_badge, pos_y=height - 320, theme=theme)

    # 8. Dark Vignette Edge Framing (Cinematic Polish)
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    for inset in range(0, 90, 5):
        alpha = int(90 * (1.0 - (inset / 90)))
        vdraw.rectangle([(inset, inset), (width - inset, height - inset)], outline=(0, 0, 0, alpha), width=5)
    img.alpha_composite(vignette)

    # Final Convert & Richness Verification
    final_rgb = img.convert("RGB")
    stat = ImageStat.Stat(final_rgb.convert("L"))
    if stat.mean[0] < 20 or stat.stddev[0] < 25:
        logger.warning(f"Frame {section.get('section_index')} brightness low, applying autoboost")
        final_rgb = ImageEnhance.Contrast(final_rgb).enhance(1.2)

    if output_path is None:
        output_path = OUTPUT_DIR / f"frame_{section.get('section_index', 0):02d}.jpg"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_rgb.save(output_path, "JPEG", quality=95)
    logger.info(f"🎨 [High-CTR Frame Studio] Generated section frame: {output_path.name} ({os.path.getsize(output_path)//1024} KB)")
    return output_path


def generate_short_section_frames(
    sections: List[Dict[str, Any]],
    vertical: str = "crypto",
    output_dir: Optional[Path] = None,
    slug: str = "short",
) -> List[Path]:
    """
    Generates high-CTR 9:16 thumbnail background frames for all sections of a Short.
    For a 60-second short: 10 sections -> 10 explosive frames.
    For a 36-second short: 6 sections -> 6 explosive frames.
    """
    if output_dir is None:
        output_dir = OUTPUT_DIR / slug / "frames"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    frame_paths: List[Path] = []
    logger.info(f"🚀 [High-CTR Frame Studio] Generating {len(sections)} high-CTR background frames for '{slug}'...")
    
    for idx, sec in enumerate(sections):
        sec["section_index"] = idx
        out_f = output_dir / f"frame_{idx:02d}.jpg"
        path = generate_high_ctr_section_frame(sec, vertical=vertical, output_path=out_f)
        frame_paths.append(path)
        
    logger.success(f"✅ [High-CTR Frame Studio] Successfully generated all {len(frame_paths)} high-CTR frames in {output_dir}")
    return frame_paths
