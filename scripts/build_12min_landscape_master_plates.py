"""
⚡ 12-MINUTE STANDARD LANDSCAPE (16:9) 3D MASTER PLATE COMPOSITOR — The Bull Print
Generates 1920x1080 cinematic master plates for 12-Minute Long-Format YouTube Documentaries.
Adheres strictly to Option A: 100% Photorealistic 3D Master Octane renders,
documentary 2.35:1 letterboxing, multi-pass 3D metallic typography, and forensic telemetry cards.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent

# Typography fonts
FONT_IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"
FONT_ARIAL_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_MONO = "/System/Library/Fonts/Courier.dfont"

def get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
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
    shadow_color: tuple = (10, 15, 25),
    extrude_color: tuple = (180, 83, 9),
    glow_color: tuple = (245, 158, 11),
    depth: int = 10,
    anchor: str = "la"
):
    x, y = xy
    w, h = canvas.size

    # 1. Ambient Glow
    glow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow_layer)
    g_draw.text((x, y + depth // 2), text, font=font, fill=(*glow_color, 200), anchor=anchor)
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(14))
    canvas.paste(glow_layer, (0, 0), glow_layer)

    # 2. Deep Shadow
    s_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(s_layer)
    s_draw.text((x + 4, y + depth + 6), text, font=font, fill=(0, 0, 0, 240), anchor=anchor)
    s_layer = s_layer.filter(ImageFilter.GaussianBlur(6))
    canvas.paste(s_layer, (0, 0), s_layer)

    # 3. 3D Extrusion
    draw = ImageDraw.Draw(canvas)
    for i in range(depth, 0, -1):
        ratio = i / depth
        r = int(extrude_color[0] * (1 - ratio * 0.7) + shadow_color[0] * (ratio * 0.7))
        g = int(extrude_color[1] * (1 - ratio * 0.7) + shadow_color[1] * (ratio * 0.7))
        b = int(extrude_color[2] * (1 - ratio * 0.7) + shadow_color[2] * (ratio * 0.7))
        draw.text((x, y + i), text, font=font, fill=(r, g, b, 255), anchor=anchor)

    # 4. Dark rim
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
        draw.text((x + dx, y + dy), text, font=font, fill=(10, 10, 15, 255), anchor=anchor)

    # 5. Face & Bevel Highlight
    draw.text((x, y), text, font=font, fill=(*face_color, 255), anchor=anchor)
    draw.text((x - 1, y - 1), text, font=font, fill=(255, 255, 255, 160), anchor=anchor)

def render_landscape_master_plate(
    base_image_path: str,
    eyebrow_text: str,
    headline_text: str,
    emphasis_text: str,
    subtext: str,
    minute_label: str,
    accent_color: tuple,
    output_path: Path
):
    target_w, target_h = 1920, 1080

    # 1. Load and conform base image to 1920x1080 (Lanczos)
    im = Image.open(base_image_path).convert("RGBA")
    w, h = im.size
    scale = max(target_w / w, target_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    im = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    im = im.crop((left, top, left + target_w, top + target_h))

    # 2. Cinematic 2.35:1 Letterbox Bars (54px top and bottom)
    draw = ImageDraw.Draw(im, "RGBA")
    bar_h = 54
    draw.rectangle([0, 0, target_w, bar_h], fill=(5, 7, 12, 255))
    draw.rectangle([0, target_h - bar_h, target_w, target_h], fill=(5, 7, 12, 255))

    # 3. Bottom Gradient Scrim for Editorial Typography Readability
    grad = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grad)
    for y in range(target_h - 480, target_h - bar_h):
        progress = (y - (target_h - 480)) / (480 - bar_h)
        alpha = int(240 * (progress ** 1.3))
        g_draw.line([(0, y), (target_w, y)], fill=(6, 9, 18, alpha))
    im = Image.alpha_composite(im, grad)

    # 4. Top-Right Minute Marker Badge (e.g. "MINUTE 01 // 12:00")
    font_badge = get_font(FONT_MONO, 22)
    badge_x, badge_y = target_w - 90, bar_h + 36
    draw_badge = ImageDraw.Draw(im, "RGBA")
    bbox = font_badge.getbbox(minute_label)
    bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pill_box = [badge_x - bw - 32, badge_y - 12, badge_x, badge_y + bh + 12]
    draw_badge.rounded_rectangle(pill_box, radius=14, fill=(10, 15, 28, 220), outline=(*accent_color, 240), width=2)
    draw_badge.text((badge_x - bw // 2 - 16, badge_y + bh // 2), minute_label, font=font_badge, fill=(*accent_color, 255), anchor="mm")

    # 5. Editorial Lower-Left Typography Stack
    start_x = 90
    start_y = target_h - 380

    # Eyebrow Category Tag
    font_eye = get_font(FONT_MONO, 24)
    draw_text = ImageDraw.Draw(im, "RGBA")
    draw_text.line([(start_x, start_y + 12), (start_x + 40, start_y + 12)], fill=(*accent_color, 255), width=4)
    draw_text.text((start_x + 54, start_y), eyebrow_text.upper(), font=font_eye, fill=(*accent_color, 255))

    # Line 1: White Headline
    font_head = get_font(FONT_ARIAL_BLACK, 62)
    head_y = start_y + 38
    draw_3d_extruded_text(
        im, headline_text, (start_x, head_y), font_head,
        face_color=(255, 255, 255), extrude_color=(40, 50, 70), glow_color=(15, 23, 42), depth=8, anchor="la"
    )

    # Line 2: Vibrant Accent Emphasis
    font_emph = get_font(FONT_IMPACT, 78)
    emph_y = head_y + 74
    draw_3d_extruded_text(
        im, emphasis_text, (start_x, emph_y), font_emph,
        face_color=accent_color, extrude_color=(int(accent_color[0]*0.6), int(accent_color[1]*0.6), int(accent_color[2]*0.6)),
        glow_color=accent_color, depth=10, anchor="la"
    )

    # Line 3: Subtext
    font_sub = get_font(FONT_ARIAL_BOLD, 26)
    sub_y = emph_y + 88
    for ox, oy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        draw_text.text((start_x + ox, sub_y + oy), subtext, font=font_sub, fill=(0, 0, 0, 240))
    draw_text.text((start_x, sub_y), subtext, font=font_sub, fill=(226, 232, 240, 255))

    # 6. High-end finish: Unsharp Mask for 4K clarity
    final_rgb = im.convert("RGB")
    final_rgb = final_rgb.filter(ImageFilter.UnsharpMask(radius=1.5, percent=125, threshold=2))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_rgb.save(output_path, "JPEG", quality=95, optimize=True)
    print(f"✅ Generated 16:9 Master Plate: {output_path.name} ({round(output_path.stat().st_size / 1024)} KB)")

# 12 Minutes = 12 Master Milestone Plates (1 per minute)
PLATES_12MIN = [
    {
        "minute": "MINUTE 01 // 12:00",
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/vivid_penthouse_16_9_1793451982917.jpg",
        "eyebrow": "PROLOGUE // NASSAU, THE BAHAMAS",
        "headline": "THE $30,000,000 CITADEL",
        "emphasis": "THE $32B ILLUSION",
        "subtext": "Behind locked doors, a thirty-year-old billionaire ran a secret financial empire.",
        "accent": (16, 185, 129), # Emerald
    },
    {
        "minute": "MINUTE 02 // 12:00",
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/forensic_desk_cinematic_1793426824114.jpg",
        "eyebrow": "MEDIA APOTHEOSIS // SILICON VALLEY",
        "headline": "THE FORBES SAVIOR",
        "emphasis": "THE NEXT J.P. MORGAN",
        "subtext": "Venture titans and politicians declared Sam Bankman-Fried the first future trillionaire.",
        "accent": (245, 158, 11), # Amber Gold
    },
    {
        "minute": "MINUTE 03 // 12:00",
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/server_backdoor_cinematic_1793426966255.jpg",
        "eyebrow": "CRIMINAL FORENSICS // EXHIBIT A",
        "headline": "THE SECRET BACKDOOR",
        "emphasis": "$8,000,000,000 DRAINED",
        "subtext": "A single line of raw JavaScript granted his private hedge fund unlimited customer cash.",
        "accent": (239, 68, 68), # Crimson
    },
    {
        "minute": "MINUTE 04 // 12:00",
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/siphon_hud_16_9_1793450307807.jpg",
        "eyebrow": "ALGORITHMIC MECHANICS // CHAPTER 1",
        "headline": "THE FTT TOKEN ENGINE",
        "emphasis": "INFINITE MONEY GLITCH",
        "subtext": "Minting billions in paper wealth out of thin air to borrow real customer US dollars.",
        "accent": (6, 182, 212), # Cyan
    },
    {
        "minute": "MINUTE 05 // 12:00",
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/trading_floor_cinematic_1793426887683.jpg",
        "eyebrow": "QUANT ARBITRAGE // ALAMEDA RESEARCH",
        "headline": "THE KIMCHI PREMIUM",
        "emphasis": "+30% DAILY SPREAD",
        "subtext": "From Jane Street to Tokyo: Printing $25,000,000 per month before building the exchange.",
        "accent": (16, 185, 129), # Emerald
    },
    {
        "minute": "MINUTE 06 // 12:00",
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/magnates_bull_hq_1793373359564.jpg",
        "eyebrow": "SUPER BOWL ADS & REAL ESTATE",
        "headline": "BUYING TRUST AT ANY COST",
        "emphasis": "$300,000,000 SPENT",
        "subtext": "Purchasing arena naming rights and celebrity endorsements to lure everyday savings.",
        "accent": (245, 158, 11), # Amber
    },
    {
        "minute": "MINUTE 07 // 12:00",
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/money_vault_cinematic_1793426936579.jpg",
        "eyebrow": "CONTAGION // THE BLACK HOLE",
        "headline": "TERRA LUNA IMPLOSION",
        "emphasis": "SECRET BAILOUT TRAP",
        "subtext": "When crypto lenders collapsed, Alameda secretly filled the hole with FTX deposits.",
        "accent": (239, 68, 68), # Crimson
    },
    {
        "minute": "MINUTE 08 // 12:00",
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/subpoena_manila_16_9_1793450341907.jpg",
        "eyebrow": "INVESTIGATIVE LEAK // COINDESK",
        "headline": "THE SMOKING GUN DOSSIER",
        "emphasis": "THE BALANCE SHEET LEAK",
        "subtext": "On November 2, the leaked balance sheet revealed Alameda was insolvent on paper.",
        "accent": (245, 158, 11), # Amber Gold
    },
    {
        "minute": "MINUTE 09 // 12:00",
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/vivid_vault_16_9_1793452083925.jpg",
        "eyebrow": "BANK RUN // 72 HOURS",
        "headline": "$6,000,000,000 WITHDRAWALS",
        "emphasis": "LIQUIDITY HALTED",
        "subtext": "Everyday retail investors scrambled to withdraw while exchange balances froze to zero.",
        "accent": (239, 68, 68), # Crimson
    },
    {
        "minute": "MINUTE 10 // 12:00",
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/subpoena_leak_paper_1793427044671.jpg",
        "eyebrow": "DEPARTMENT OF JUSTICE // INDICTMENT",
        "headline": "CHAPTER 11 BANKRUPTCY",
        "emphasis": "FEDERAL CHARGES FILED",
        "subtext": "John J. Ray III takes control: 'In 40 years, I have never seen such a complete failure.'",
        "accent": (6, 182, 212), # Cyan
    },
    {
        "minute": "MINUTE 11 // 12:00",
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/courtroom_reckoning_cinematic_1793427006464.jpg",
        "eyebrow": "MANHATTAN FEDERAL COURT // VERDICT",
        "headline": "GUILTY ON ALL COUNTS",
        "emphasis": "25 YEARS IMPRISONMENT",
        "subtext": "The fastest corporate rise and fall ends in federal prison for the former wunderkind.",
        "accent": (239, 68, 68), # Crimson
    },
    {
        "minute": "MINUTE 12 // 12:00",
        "base_image": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/investigation_corkboard_1793427126994.jpg",
        "eyebrow": "INVESTOR VERDICT // THE BULL PRINT",
        "headline": "NEVER TRUST EXCHANGES",
        "emphasis": "SELF-CUSTODY RULES",
        "subtext": "Not your keys, not your coins: The fundamental rule to protect generational family wealth.",
        "accent": (16, 185, 129), # Emerald
    },
]

def main():
    target_dir = BASE_DIR / "assets" / "approved_bundles" / "the-32-billion-illusion-ftx-alameda-12min"
    print(f"🚀 Generating 12 Bespoke 16:9 Landscape Master Plates in: {target_dir}")
    for idx, plate in enumerate(PLATES_12MIN):
        out_file = target_dir / f"master_plate_{idx+1:02d}.jpg"
        render_landscape_master_plate(
            base_image_path=plate["base_image"],
            eyebrow_text=plate["eyebrow"],
            headline_text=plate["headline"],
            emphasis_text=plate["emphasis"],
            subtext=plate["subtext"],
            minute_label=plate["minute"],
            accent_color=plate["accent"],
            output_path=out_file
        )

if __name__ == "__main__":
    main()
