"""
⚡ HIGH-CTR THUMBNAIL FRAME STUDIO — The Bull Print
Architectural 16:9 Landscape & 9:16 Vertical High-CTR Background Frame Studio.
Zero static loops. Zero reference image bypasses. Pure dynamic rendering.

Guarantees:
1. Every segment renders a unique, topic-tailored, high-CTR visual plate with 3D typography and procedural graphics.
2. Aspect-ratio aware: Perfectly balanced for 16:9 Landscape (1920x1080) and 9:16 Vertical (1080x1920).
3. Zero reuse of static benchmark frames: All plates are procedurally synthesized on-the-fly per topic.
"""

import hashlib
import math
import os
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageStat
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
        str(BASE_DIR / "assets" / "fonts" / "Inter-Bold.ttf"),
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
    "insurance_navy": {
        "bg_top": (8, 18, 38),
        "bg_bot": (2, 5, 14),
        "glow_color": (37, 99, 235),       # Royal Blue #2563EB
        "accent_secondary": (56, 189, 248),# Sky Blue
        "text_top": ((255, 255, 255), (191, 219, 254), (59, 130, 246)),
        "text_bot": ((255, 255, 255), (254, 215, 170), (249, 115, 22)),
        "pill_bg": (29, 78, 216),
        "pill_border": (147, 197, 253),
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
    "solana_purple": {
        "bg_top": (18, 6, 32),
        "bg_bot": (5, 1, 12),
        "glow_color": (153, 69, 255),      # Solana Purple
        "accent_secondary": (20, 241, 149), # Solana Teal
        "text_top": ((255, 255, 255), (200, 160, 255), (153, 69, 255)),
        "text_bot": ((255, 255, 255), (100, 255, 200), (20, 241, 149)),
        "pill_bg": (153, 69, 255),
        "pill_border": (255, 255, 255),
    },
}

PALETTE_KEYS = list(PALETTES.keys())


def _draw_linear_gradient(
    draw: ImageDraw.ImageDraw,
    width: int,
    height: int,
    top_color: Tuple[int, int, int],
    bot_color: Tuple[int, int, int],
):
    for y in range(height):
        factor = y / max(1, height)
        r = int(top_color[0] + factor * (bot_color[0] - top_color[0]))
        g = int(top_color[1] + factor * (bot_color[1] - top_color[1]))
        b = int(top_color[2] + factor * (bot_color[2] - top_color[2]))
        draw.line([(0, y), (width, y)], fill=(r, g, b))


def _draw_atmospheric_grid_and_candlesticks(
    width: int,
    height: int,
    theme: Dict[str, Any],
    seed: int = 42,
    is_landscape: bool = False,
) -> Image.Image:
    rnd = random.Random(seed)
    grid_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grid_overlay)

    # 1. Subtle horizontal perspective grid
    h_step = int(height * 0.12)
    for y in range(int(height * 0.15), height - int(height * 0.08), h_step):
        alpha = int(18 + 15 * math.sin(y / height * math.pi))
        gdraw.line([(0, y), (width, y)], fill=(*theme["glow_color"][:3], alpha), width=1)

    # 2. Vertical grid lines
    v_step = int(width * 0.08)
    for x in range(v_step, width, v_step):
        gdraw.line([(x, int(height * 0.1)), (x, height - int(height * 0.05))], fill=(*theme["glow_color"][:3], 15), width=1)

    # 3. Candlesticks in background
    num_candles = 22 if is_landscape else 14
    c_step = width // (num_candles + 2)
    for i in range(num_candles):
        cx = int(c_step * (i + 1) + rnd.randint(-8, 8))
        is_red = rnd.random() < 0.60
        candle_col = (255, 50, 50, 95) if is_red else (*theme["accent_secondary"][:3], 95)
        
        base_y = height // 2
        c_top = rnd.randint(base_y - int(height * 0.18), base_y + int(height * 0.18))
        c_height = rnd.randint(int(height * 0.03), int(height * 0.12))
        wick_top = max(int(height * 0.08), c_top - rnd.randint(15, 60))
        wick_bot = min(height - int(height * 0.08), c_top + c_height + rnd.randint(15, 60))

        # Draw wick
        gdraw.line([(cx, wick_top), (cx, wick_bot)], fill=candle_col, width=2)
        # Draw body
        c_width = 8 if is_landscape else 10
        gdraw.rectangle([(cx - c_width, c_top), (cx + c_width, c_top + c_height)], fill=candle_col)

    return grid_overlay


def _draw_radial_glow(
    width: int,
    height: int,
    center_x: int,
    center_y: int,
    radius: int,
    glow_color: Tuple[int, int, int],
) -> Image.Image:
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    num_steps = 10
    for i in range(num_steps, 0, -1):
        r = int(radius * (i / num_steps))
        alpha = int(45 * (1.0 - (i / num_steps)))
        gdraw.ellipse(
            [center_x - r, center_y - r, center_x + r, center_y + r],
            fill=(*glow_color, alpha),
        )
    return glow.filter(ImageFilter.GaussianBlur(radius=int(radius * 0.25)))


def _render_3d_metallic_line(
    canvas: Image.Image,
    text: str,
    pos_y: int,
    font: ImageFont.FreeTypeFont,
    gradient: Tuple[Tuple[int, int, int], Tuple[int, int, int], Tuple[int, int, int]],
    glow_color: Tuple[int, int, int],
    depth: int = 12,
    pos_x: Optional[int] = None,
) -> int:
    """Renders bold 3D metallic typography with specular bevels and outer glow."""
    width, height = canvas.size
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    bbox = draw.textbbox((0, 0), text, font=font)
    t_w = bbox[2] - bbox[0]
    t_h = bbox[3] - bbox[1]
    if pos_x is None:
        pos_x = (width - t_w) // 2

    # 1. Outer Neon Glow
    glow_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    for _ in range(3):
        glow_draw.text((pos_x, pos_y), text, font=font, fill=(*glow_color, 35))
    glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(radius=8))
    canvas.alpha_composite(glow_overlay)

    # 2. Deep 3D Extrusion
    for d in range(depth, 0, -1):
        darkness = int(10 + 8 * (d / depth))
        draw.text((pos_x + d // 2, pos_y + d), text, font=font, fill=(darkness, darkness, darkness, 255))

    # 3. Text Body with Vertical Gradient
    text_mask = Image.new("L", (t_w + 30, t_h + 30), 0)
    tmask_draw = ImageDraw.Draw(text_mask)
    tmask_draw.text((15 - bbox[0], 15 - bbox[1]), text, font=font, fill=255)

    gradient_tile = Image.new("RGBA", (t_w + 30, t_h + 30))
    g_draw = ImageDraw.Draw(gradient_tile)
    for y in range(t_h + 30):
        f = y / max(1, t_h + 30)
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
        g_draw.line([(0, y), (t_w + 30, y)], fill=(r, g, b, 255))

    gradient_tile.putalpha(text_mask)
    canvas.paste(gradient_tile, (pos_x - 15 + bbox[0], pos_y - 15 + bbox[1]), gradient_tile)

    # 4. Top Crisp Specular Bevel Line
    spec_draw = ImageDraw.Draw(canvas)
    spec_draw.text((pos_x, pos_y - 1), text, font=font, fill=(255, 255, 255, 130))

    return pos_y + t_h


def _draw_warning_pill(
    canvas: Image.Image,
    badge_text: str,
    pos_y: int,
    theme: Dict[str, Any],
    pos_x: Optional[int] = None,
    font_size: int = 42,
) -> int:
    """Renders high-visibility floating warning pill badge."""
    width, _ = canvas.size
    font = _get_font(font_size, bold=True)
    draw = ImageDraw.Draw(canvas)

    bbox = draw.textbbox((0, 0), badge_text, font=font)
    t_w = bbox[2] - bbox[0]
    t_h = bbox[3] - bbox[1]

    pad_x = int(font_size * 0.8)
    pad_y = int(font_size * 0.35)
    pill_w = t_w + pad_x * 2
    pill_h = t_h + pad_y * 2
    if pos_x is None:
        pos_x = (width - pill_w) // 2

    # Outer glow
    pill_glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    pg_draw = ImageDraw.Draw(pill_glow)
    pg_draw.rounded_rectangle(
        [(pos_x - 4, pos_y - 4), (pos_x + pill_w + 4, pos_y + pill_h + 4)],
        radius=pill_h // 2,
        fill=(*theme["glow_color"][:3], 90),
    )
    pill_glow = pill_glow.filter(ImageFilter.GaussianBlur(radius=6))
    canvas.alpha_composite(pill_glow)

    # Pill body
    p_draw = ImageDraw.Draw(canvas)
    p_draw.rounded_rectangle(
        [(pos_x, pos_y), (pos_x + pill_w, pos_y + pill_h)],
        radius=pill_h // 2,
        fill=(*theme["pill_bg"][:3], 240),
        outline=(*theme["pill_border"][:3], 255),
        width=3,
    )
    tx = pos_x + pad_x - bbox[0]
    ty = pos_y + pad_y - bbox[1]
    p_draw.text((tx, ty), badge_text, font=font, fill=(255, 255, 255, 255))

    return pos_y + pill_h


def _draw_central_3d_anchor(
    canvas: Image.Image,
    symbol_type: str,
    theme: Dict[str, Any],
    cx: int,
    cy: int,
    scale: float = 1.0,
):
    """
    Renders topic-tailored procedural 3D visual anchors:
    - 'insurance_shield': Security shield with medical cross & vault ring.
    - 'bull_breakout': Upward golden horns & green explosive breakout candlesticks.
    - 'orderbook_absorption': Depth-of-market ladder with bid/ask absorption brackets.
    - 'burning_chart': Downward jagged crash lightning trendline.
    - 'crypto_orb': Multi-ring cryptographic orb core.
    - 'mev_bot': Crosshair lock target.
    """
    width, height = canvas.size
    glow = _draw_radial_glow(width, height, cx, cy, int(320 * scale), theme["glow_color"][:3])
    canvas.alpha_composite(glow)

    anchor_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    adraw = ImageDraw.Draw(anchor_overlay)

    sym = symbol_type.lower()
    
    # ── 1. INSURANCE SECURITY SHIELD ──
    if any(k in sym for k in ("shield", "insurance", "policy", "hospital", "claim", "deduction")):
        # Outer metallic shield contour
        r = int(120 * scale)
        pts = [
            (cx - r, cy - int(r * 0.9)),
            (cx + r, cy - int(r * 0.9)),
            (cx + int(r * 0.85), cy + int(r * 0.2)),
            (cx, cy + int(r * 1.1)),
            (cx - int(r * 0.85), cy + int(r * 0.2)),
        ]
        # Shield glow outline
        adraw.polygon(pts, fill=(*theme["pill_bg"][:3], 210), outline=(255, 255, 255, 240))
        # Concentric security ring
        adraw.ellipse([cx - int(r*0.6), cy - int(r*0.4), cx + int(r*0.6), cy + int(r*0.8)], outline=(*theme["accent_secondary"][:3], 180), width=3)
        # Bold medical/audit cross
        cw = int(18 * scale)
        ch = int(60 * scale)
        adraw.rectangle([(cx - cw, cy - ch), (cx + cw, cy + ch)], fill=(255, 255, 255, 255))
        adraw.rectangle([(cx - ch, cy - cw), (cx + ch, cy + cw)], fill=(255, 255, 255, 255))

    # ── 2. STOCK MARKET BULL BREAKOUT & ORDER FLOW ──
    elif any(k in sym for k in ("bull", "breakout", "nifty", "opening_range", "absorption", "fii", "vwap", "gamma")):
        r = int(130 * scale)
        # Upward green candlestick staircase
        for i in range(5):
            bx = cx - r + int(i * (r * 0.45))
            by = cy + int(r * 0.5) - int(i * (r * 0.28))
            bw = int(22 * scale)
            bh = int(50 * scale)
            adraw.line([(bx + bw//2, by - 25), (bx + bw//2, by + bh + 25)], fill=(16, 185, 129, 255), width=3)
            adraw.rectangle([(bx, by), (bx + bw, by + bh)], fill=(16, 185, 129, 230), outline=(255, 255, 255, 220), width=2)
        # Golden trendline arrow shooting upward
        arrow_pts = [
            (cx - int(r * 0.9), cy + int(r * 0.6)),
            (cx + int(r * 0.2), cy - int(r * 0.2)),
            (cx + int(r * 0.9), cy - int(r * 0.8)),
        ]
        for w, a in [(10, 100), (5, 220), (2, 255)]:
            adraw.line(arrow_pts, fill=(250, 204, 21, a), width=w)
        # Arrowhead
        tip = arrow_pts[-1]
        adraw.polygon([tip, (tip[0] - 25, tip[1] + 5), (tip[0] - 5, tip[1] + 25)], fill=(255, 255, 255, 255))

    # ── 3. BURNING CHART / CRASH LIQUIDATION ──
    elif any(k in sym for k in ("burning", "crash", "liquidation", "dump", "fall")):
        r = int(120 * scale)
        points = [
            (cx - r, cy - int(r * 0.8)),
            (cx - int(r * 0.4), cy - int(r * 0.3)),
            (cx - int(r * 0.6), cy + int(r * 0.1)),
            (cx + int(r * 0.1), cy + int(r * 0.4)),
            (cx + int(r * 0.8), cy + int(r * 1.0)),
        ]
        for w, a in [(12, 100), (6, 200), (2, 255)]:
            adraw.line(points, fill=(255, 40, 40, a), width=w)
        tip = points[-1]
        adraw.polygon([tip, (tip[0] - 25, tip[1] - 8), (tip[0] - 8, tip[1] - 25)], fill=(255, 255, 255, 255))

    # ── 4. CRYPTO COIN & PROTOCOL ORB ──
    else:
        r = int(110 * scale)
        for rad, alpha in [(r, 60), (int(r * 0.75), 110), (int(r * 0.5), 200)]:
            adraw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=(*theme["accent_secondary"][:3], alpha), width=4)
        adraw.ellipse([cx - int(r*0.35), cy - int(r*0.35), cx + int(r*0.35), cy + int(r*0.35)], fill=(*theme["glow_color"][:3], 230), outline=(255, 255, 255, 240), width=3)

    canvas.alpha_composite(anchor_overlay)


# ---------------------------------------------------------------- Core Frame Generator
def generate_high_ctr_section_frame(
    section: Dict[str, Any],
    vertical: str = "stock_market",
    width: int = 1080,
    height: int = 1920,
    output_path: Optional[Path] = None,
) -> Path:
    """
    Renders an aspect-ratio aware High-CTR Thumbnail frame.
    Supports 16:9 Landscape (1920x1080) and 9:16 Portrait (1080x1920).
    Zero static reference image bypasses.
    """
    if output_path is None:
        output_path = OUTPUT_DIR / f"frame_{section.get('section_index', 0):02d}.jpg"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    is_landscape = width >= height

    # Palette Selection
    vert = (vertical or "stock_market").lower()
    default_theme = "insurance_navy" if "insur" in vert else ("gold_bull" if "stock" in vert else "solana_purple")
    theme_key = section.get("theme") or default_theme
    theme = PALETTES.get(theme_key, PALETTES.get(default_theme, list(PALETTES.values())[0]))

    # 1. Base Linear Gradient Canvas
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    _draw_linear_gradient(draw, width, height, theme["bg_top"], theme["bg_bot"])

    # 2. Atmospheric Candlestick & Grid Overlay
    seed = section.get("section_index", 0) * 17 + len(section.get("headline_top", ""))
    grid = _draw_atmospheric_grid_and_candlesticks(width, height, theme, seed=seed, is_landscape=is_landscape)
    img.alpha_composite(grid)

    # 3. Dynamic Section Layout
    badge_text = section.get("badge_text", "MARKET ALERT ⚠️")
    line1_text = section.get("headline_top", "MARKET ANALYSIS").upper()
    line2_text = section.get("headline_mid", "ORDER FLOW FORENSICS").upper()
    lower_badge = section.get("lower_badge")
    symbol = section.get("symbol_type") or ("bull_breakout" if "stock" in vert else ("insurance_shield" if "insur" in vert else "crypto_orb"))

    if is_landscape:
        # ── 16:9 LANDSCAPE BROADCAST LAYOUT (e.g. 1920x1080) ──
        # Left-anchored editorial typography, right-anchored central 3D graphic
        left_margin = int(width * 0.08)
        pill_y = int(height * 0.14)
        
        # Pill
        next_y = _draw_warning_pill(img, badge_text, pos_y=pill_y, theme=theme, pos_x=left_margin, font_size=int(height * 0.038))
        
        # Headline 1
        top_font = _get_font(int(height * 0.082), bold=True)
        next_y = _render_3d_metallic_line(
            img, line1_text, pos_y=next_y + 18, font=top_font,
            gradient=theme["text_top"], glow_color=theme["glow_color"][:3], depth=10, pos_x=left_margin
        )
        
        # Headline 2
        mid_font = _get_font(int(height * 0.068), bold=True)
        next_y = _render_3d_metallic_line(
            img, line2_text, pos_y=next_y + 14, font=mid_font,
            gradient=theme["text_bot"], glow_color=theme["accent_secondary"][:3], depth=8, pos_x=left_margin
        )
        
        # Lower Badge
        if lower_badge:
            _draw_warning_pill(img, lower_badge, pos_y=height - int(height * 0.18), theme=theme, pos_x=left_margin, font_size=int(height * 0.034))
        
        # Central 3D Graphic on the Right
        anchor_cx = int(width * 0.72)
        anchor_cy = int(height * 0.52)
        _draw_central_3d_anchor(img, symbol, theme, cx=anchor_cx, cy=anchor_cy, scale=1.35)

    else:
        # ── 9:16 VERTICAL HIGH-CTR SHORT LAYOUT (e.g. 1080x1920) ──
        # Centered top hook, central dramatic 3D anchor, lower statistic badge
        pill_y = int(height * 0.11)
        next_y = _draw_warning_pill(img, badge_text, pos_y=pill_y, theme=theme, font_size=46)

        # Headline 1
        top_font = _get_font(104, bold=True)
        next_y = _render_3d_metallic_line(
            img, line1_text, pos_y=next_y + 24, font=top_font,
            gradient=theme["text_top"], glow_color=theme["glow_color"][:3], depth=14
        )

        # Headline 2
        mid_font = _get_font(88, bold=True)
        _render_3d_metallic_line(
            img, line2_text, pos_y=next_y + 20, font=mid_font,
            gradient=theme["text_bot"], glow_color=theme["accent_secondary"][:3], depth=12
        )

        # Central 3D Graphic Anchor
        anchor_cx = width // 2
        anchor_cy = int(height * 0.58)
        _draw_central_3d_anchor(img, symbol, theme, cx=anchor_cx, cy=anchor_cy, scale=1.1)

        # Lower Section Statistic Badge
        if lower_badge:
            _draw_warning_pill(img, lower_badge, pos_y=height - int(height * 0.16), theme=theme, font_size=42)

    # 4. Cinematic Dark Vignette Edge Framing
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    max_inset = int(min(width, height) * 0.08)
    for inset in range(0, max_inset, 6):
        alpha = int(85 * (1.0 - (inset / max_inset)))
        vdraw.rectangle([(inset, inset), (width - inset, height - inset)], outline=(0, 0, 0, alpha), width=6)
    img.alpha_composite(vignette)

    # 5. Contrast & Brightness Verification Gate
    final_rgb = img.convert("RGB")
    stat = ImageStat.Stat(final_rgb.convert("L"))
    if stat.mean[0] < 20 or stat.stddev[0] < 25:
        logger.warning(f"Frame {section.get('section_index')} brightness low, applying autoboost")
        final_rgb = ImageEnhance.Contrast(final_rgb).enhance(1.2)

    final_rgb.save(output_path, "JPEG", quality=95)
    logger.info(f"🎨 [Frame Studio] Rendered {width}x{height} plate: {output_path.name} ({os.path.getsize(output_path)//1024} KB)")
    return output_path
