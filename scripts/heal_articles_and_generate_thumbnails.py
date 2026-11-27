#!/usr/bin/env python3
"""
Master Article Healer & Viral High-CTR Thumbnail Batch Generator
- Creates bespoke, high-CTR 1280x720 16:9 viral thumbnails for ALL articles
- Applies 4-Pillar Gold Standard (Distress Badge, 3D Block Kinetic Extrusion, Two-Tone Contrast, Vignette)
- Injects descriptive alt tags for 100% of images
- Cleans and converts any broken frame image tags into responsive YouTube embeds
- Syncs content/posts.json and public/content/posts.json
"""

import json
import os
import re
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
PUBLIC_EDITORIAL = ROOT / "public" / "assets" / "editorial"
PUBLIC_EDITORIAL.mkdir(parents=True, exist_ok=True)

# Select best bold font on macOS
FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf",
    "/System/Library/Fonts/Supplemental/Verdana Bold.ttf",
    "/System/Library/Fonts/Supplemental/Tahoma Bold.ttf"
]
SELECTED_FONT = next((f for f in FONT_CANDIDATES if os.path.exists(f)), None)

def get_font(size):
    if SELECTED_FONT:
        try:
            return ImageFont.truetype(SELECTED_FONT, size)
        except Exception:
            pass
    return ImageFont.load_default()

def get_fitted_font(text, max_w=980, max_size=88, min_size=42):
    dummy_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for size in range(max_size, min_size - 1, -4):
        font = get_font(size)
        bbox = dummy_draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_w:
            return font, size, w, bbox[3] - bbox[1]
    font = get_font(min_size)
    bbox = dummy_draw.textbbox((0, 0), text, font=font)
    return font, min_size, bbox[2] - bbox[0], bbox[3] - bbox[1]

def create_gradient_canvas(width=1280, height=720, color_theme="gold"):
    img = Image.new("RGB", (width, height), (10, 13, 19))
    draw = ImageDraw.Draw(img)
    
    theme_colors = {
        "gold": ((245, 158, 11), (255, 230, 0)),
        "red": ((220, 38, 38), (255, 60, 60)),
        "cyan": ((6, 182, 212), (6, 220, 255)),
        "green": ((16, 185, 129), (16, 235, 140)),
        "orange": ((234, 88, 12), (255, 140, 20))
    }
    glow_color, accent_color = theme_colors.get(color_theme, theme_colors["gold"])
    
    # Render subtle radial atmospheric glow
    cx, cy = width // 2, height // 3
    for r in range(420, 40, -30):
        alpha = int(40 * (1 - r / 420))
        box = [cx - r, cy - r, cx + r, cy + r]
        glow_fill = (
            int(glow_color[0] * alpha / 255),
            int(glow_color[1] * alpha / 255),
            int(glow_color[2] * alpha / 255)
        )
        draw.ellipse(box, fill=glow_fill)
        
    img = img.filter(ImageFilter.GaussianBlur(radius=28))
    draw = ImageDraw.Draw(img)
    
    # Financial grid lines
    grid_color = (22, 28, 40)
    for x in range(0, width, 80):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, 80):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)
        
    # Top & bottom cinematic vignette
    draw.rectangle([0, 0, width, int(height * 0.12)], fill=(6, 8, 12))
    draw.rectangle([0, int(height * 0.88), width, height], fill=(6, 8, 12))
    
    return img, accent_color

def render_angled_badge(badge_text, bg_color=(200, 30, 30), border_color=(255, 230, 0)):
    font = get_font(26)
    dummy_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbox = dummy_draw.textbbox((0, 0), badge_text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    bw, bh = tw + 40, th + 22
    badge_img = Image.new("RGBA", (bw + 20, bh + 20), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(badge_img)
    
    # Outer glowing border & background
    bdraw.rectangle([6, 6, bw + 6, bh + 6], fill=bg_color, outline=border_color, width=3)
    bdraw.text(((bw + 12 - tw) // 2, (bh + 12 - th) // 2 - 2), badge_text, font=font, fill=(255, 255, 255))
    
    # Rotate by -8 degrees
    rotated = badge_img.rotate(8, expand=True, resample=Image.BICUBIC)
    return rotated

def parse_post_metadata(post):
    title = post.get("title", "").strip()
    slug = post.get("slug", "").strip()
    categories = post.get("categories", [])
    cat_str = " ".join(categories).upper()
    upper = (title + " " + cat_str).upper()
    
    # Clean title
    clean = re.sub(r"202\d-\d{2}-\d{2}(-\d{4}-ist)?", "", title).strip()
    clean = re.sub(r"\(202\d\)", "", clean).strip()
    clean = re.sub(r"\s+", " ", clean)
    
    # Split title if colon exists
    colon_parts = clean.split(":")
    if len(colon_parts) > 1 and len(colon_parts[0].split()) >= 2:
        main_part = colon_parts[0].strip()
    else:
        main_part = clean
        
    theme = "gold"
    badge = "INSTITUTIONAL AUDIT"
    
    if any(k in upper for k in ["TAX", "115BBH", "194S", "ITR"]):
        theme = "red"
        badge = "SECTION 115BBH TAX AUDIT"
    elif any(k in upper for k in ["CRYPTO", "BITCOIN", "SOLANA", "RAYDIUM", "TOKEN", "DEFI", "MEMECOIN"]):
        theme = "cyan"
        badge = "CRYPTO DEFI FORENSICS"
    elif any(k in upper for k in ["SEBI", "REGULATION", "NOTICE", "F&O", "OPTIONS", "EXPIRY"]):
        theme = "orange"
        badge = "SEBI REGULATORY TRAP"
    elif any(k in upper for k in ["FII", "DII", "FOREIGN", "EXODUS", "LIQUIDATION", "OUTFLOW"]):
        theme = "red"
        badge = "FII LIQUIDATION ALERT"
    elif any(k in upper for k in ["TRENT", "ROCE", "DEBT", "BALANCE SHEET", "INDAS", "LEASE"]):
        theme = "gold"
        badge = "BALANCE SHEET FORENSICS"
    elif any(k in upper for k in ["NIFTY", "SENSEX", "BANKNIFTY", "DALAL STREET"]):
        theme = "green"
        badge = "DALAL STREET RADAR"
    elif any(k in upper for k in ["AI", "NVIDIA", "CHIP", "JENSEN"]):
        theme = "cyan"
        badge = "AI DISRUPTION WARNING"
    elif any(k in upper for k in ["GOLD", "SILVER", "COMMODITY"]):
        theme = "gold"
        badge = "COMMODITY MACRO ALERT"
    elif any(k in upper for k in ["INSURANCE", "IRDAI", "HEALTH"]):
        theme = "orange"
        badge = "IRDAI CLAIM AUDIT"
        
    words = main_part.split()
    if len(words) <= 2:
        l1 = words[0].upper()
        l2 = words[1].upper() if len(words) > 1 else "FORENSICS"
    elif len(words) <= 4:
        l1 = " ".join(words[:2]).upper()
        l2 = " ".join(words[2:]).upper()
    else:
        half = len(words) // 2
        l1 = " ".join(words[:min(half, 3)]).upper()
        l2 = " ".join(words[min(half, 3):min(len(words), 6)]).upper()
        
    return badge, l1, l2, theme

def generate_article_thumbnail(output_path, badge_text, line1_text, line2_text, theme="gold"):
    width, height = 1280, 720
    img, accent_rgb = create_gradient_canvas(width, height, color_theme=theme)
    draw = ImageDraw.Draw(img)
    
    # 1. Angled Distress Badge
    badge = render_angled_badge(badge_text)
    bx = (width - badge.width) // 2
    by = 75
    img.paste(badge, (bx, by), badge)
    
    # 2. Dynamic 3D Kinetic Typography
    font1, size1, w1, h1 = get_fitted_font(line1_text, max_w=980, max_size=88, min_size=42)
    font2, size2, w2, h2 = get_fitted_font(line2_text, max_w=980, max_size=88, min_size=42)
    
    x1 = (width - w1) // 2
    y1 = 220
    
    x2 = (width - w2) // 2
    y2 = y1 + h1 + 40
    
    # Draw Line 1 with 3D block extrusion
    for offset in range(18, 0, -2):
        draw.text((x1 + offset, y1 + offset), line1_text, font=font1, fill=(0, 0, 0))
    for dx in [-3, 0, 3]:
        for dy in [-3, 0, 3]:
            draw.text((x1 + dx, y1 + dy), line1_text, font=font1, fill=(12, 16, 24))
    draw.text((x1, y1), line1_text, font=font1, fill=accent_rgb)
    
    # Draw Line 2 with 3D block extrusion (White)
    for offset in range(18, 0, -2):
        draw.text((x2 + offset, y2 + offset), line2_text, font=font2, fill=(0, 0, 0))
    for dx in [-3, 0, 3]:
        for dy in [-3, 0, 3]:
            draw.text((x2 + dx, y2 + dy), line2_text, font=font2, fill=(12, 16, 24))
    draw.text((x2, y2), line2_text, font=font2, fill=(255, 255, 255))
    
    # 3. Institutional Footer
    footer_font = get_font(22)
    brand_text = "THE BULL PRINT • INSTITUTIONAL FORENSIC INTELLIGENCE"
    f_bbox = draw.textbbox((0, 0), brand_text, font=footer_font)
    fw = f_bbox[2] - f_bbox[0]
    draw.text(((width - fw) // 2, 650), brand_text, font=footer_font, fill=(148, 163, 184))
    
    # Save optimized JPEG
    # Save high-fidelity WebP (quality 92) and companion JPEG
    webp_path = output_path.with_suffix(".webp")
    img.save(webp_path, "WEBP", quality=92, method=6)
    jpg_path = output_path.with_suffix(".jpg")
    img.save(jpg_path, "JPEG", quality=92, optimize=True)

def heal_all_articles():
    posts_path = ROOT / "content" / "posts.json"
    public_posts_path = ROOT / "public" / "content" / "posts.json"
    
    with open(posts_path, "r", encoding="utf-8") as f:
        posts = json.load(f)
        
    print(f"Loaded {len(posts)} articles from content/posts.json.")
    
    healed_frames_count = 0
    generated_thumbnails_count = 0
    t0 = time.time()
    
    for idx, p in enumerate(posts):
        slug = p.get("slug")
        title = p.get("title", "")
        
        # 1. Parse metadata for thumbnail
        badge, l1, l2, theme = parse_post_metadata(p)
        thumb_filename = f"{slug}.webp"
        thumb_path = PUBLIC_EDITORIAL / thumb_filename
        
        # Generate thumbnail if not existing or if flagship
        if not thumb_path.exists() or thumb_path.stat().st_size == 0:
            generate_article_thumbnail(thumb_path, badge, l1, l2, theme)
            generated_thumbnails_count += 1
            
        # Update post coverImage and imageAlt
        p["coverImage"] = f"/assets/editorial/{thumb_filename}"
        p["imageAlt"] = f"{title} — The Bull Print Institutional Research"
        
        # 2. Heal broken frame tags inside body HTML
        html = p.get("html", "")
        if "/assets/frames/" in html:
            # Extract YouTube ID
            yt_url = p.get("youtubeUrl", "")
            match = re.search(r'(?:v=|\/|youtu\.be\/)([a-zA-Z0-9_-]{11})', yt_url)
            yt_id = match.group(1) if match else "X_jNao5hiVY"
            
            # Replace figure blocks
            clean_html = re.sub(
                r'<figure class="article-frame-container"[^>]*>.*?</figure>',
                '',
                html,
                flags=re.DOTALL
            )
            
            # Prepend responsive video embed
            embed_code = f'''
<div class="video-embed-container" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; margin: 32px 0; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 12px 36px rgba(0,0,0,0.6);">
    <iframe src="https://www.youtube.com/embed/{yt_id}" title="{title}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>
'''
            p["html"] = embed_code + clean_html
            healed_frames_count += 1
            print(f"[✓] Replaced broken frame images with YouTube embed in: {slug}")
            
    t1 = time.time()
    print(f"\nGenerated {generated_thumbnails_count} bespoke thumbnails in {t1 - t0:.2f} seconds.")
    print(f"Healed broken frames in {healed_frames_count} posts.")
    
    # Save back to content/posts.json and public/content/posts.json
    with open(posts_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    with open(public_posts_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
        
    print(f"[✓] Successfully updated {posts_path} and {public_posts_path}")

if __name__ == "__main__":
    heal_all_articles()
