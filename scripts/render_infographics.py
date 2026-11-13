import os
from PIL import Image, ImageDraw, ImageFont

def render_infographic(spec):
    width, height = 1200, 675
    img = Image.new('RGB', (width, height), color='#070B14')
    draw = ImageDraw.Draw(img)

    # Fonts
    font_arial = '/System/Library/Fonts/Supplemental/Arial.ttf'
    font_bold = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
    if not os.path.exists(font_bold):
        font_bold = font_arial

    f_brand = ImageFont.truetype(font_bold, 18)
    f_cat = ImageFont.truetype(font_bold, 13)
    f_title = ImageFont.truetype(font_bold, 36)
    f_subtitle = ImageFont.truetype(font_arial, 18)
    f_card_title = ImageFont.truetype(font_bold, 16)
    f_stat_val = ImageFont.truetype(font_bold, 34)
    f_stat_lbl = ImageFont.truetype(font_arial, 14)
    f_body = ImageFont.truetype(font_arial, 15)
    f_footer = ImageFont.truetype(font_arial, 12)

    # Accent color
    accent = spec.get('accent', '#00D09C')

    # Background ambient gradient / glow
    for y in range(height):
        # Subtle gradient from #070B14 to #0E1726
        factor = y / height
        r = int(7 + factor * 8)
        g = int(11 + factor * 12)
        b = int(20 + factor * 18)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Top border glow
    draw.rectangle([0, 0, width, 4], fill=accent)

    # Brand Header Bar
    # Logo pill
    draw.rounded_rectangle([50, 32, 230, 62], radius=6, fill='#0D192E', outline='#1E293B', width=1)
    draw.text((64, 38), "THE BULL PRINT", font=f_brand, fill='#FFFFFF')
    draw.ellipse([210, 44, 218, 52], fill=accent)

    # Category Pill
    cat_text = spec.get('category', 'MARKET FORENSICS').upper()
    cat_w = len(cat_text) * 9 + 24
    draw.rounded_rectangle([250, 34, 250 + cat_w, 60], radius=6, fill='#111F36', outline=accent, width=1)
    draw.text((262, 40), cat_text, font=f_cat, fill=accent)

    # Watermark / Standard ID
    draw.text((width - 240, 40), "RFC 9116 · SEBI EDU DISCLOSURE", font=f_footer, fill='#64748B')

    # Main Headline
    draw.text((50, 88), spec['title'], font=f_title, fill='#FFFFFF')
    draw.text((50, 136), spec['subtitle'], font=f_subtitle, fill='#94A3B8')

    # Horizontal Rule
    draw.line([(50, 172), (width - 50, 172)], fill='#1E293B', width=1)

    # 3 Stat / Metric Cards
    cards = spec.get('cards', [])
    card_w = (width - 100 - (len(cards) - 1) * 20) // len(cards) if cards else 340
    card_y = 195
    card_h = 160

    for i, c in enumerate(cards):
        cx = 50 + i * (card_w + 20)
        c_accent = c.get('color', accent)
        # Background card
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=10, fill='#0B1324', outline='#1E293B', width=1)
        # Accent top bar inside card
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + 4], radius=2, fill=c_accent)
        
        # Stat Value
        draw.text((cx + 20, card_y + 24), c['value'], font=f_stat_val, fill=c_accent)
        # Stat Label
        draw.text((cx + 20, card_y + 70), c['label'], font=f_card_title, fill='#F1F5F9')
        # Stat Description
        desc_lines = c.get('desc', '').split('\n')
        dy = card_y + 98
        for dl in desc_lines:
            draw.text((cx + 20, dy), dl, font=f_stat_lbl, fill='#94A3B8')
            dy += 20

    # Bottom Framework Box / Actionable Takeaway
    box_y = 380
    box_h = 220
    draw.rounded_rectangle([50, box_y, width - 50, box_y + box_h], radius=12, fill='#0B1324', outline='#1E293B', width=1)

    # Section badge
    takeaway_title = spec.get('framework_title', 'EXECUTIVE TAKEAWAY & FORENSIC PROTOCOL').upper()
    draw.rounded_rectangle([70, box_y + 18, 70 + len(takeaway_title)*9 + 20, box_y + 44], radius=4, fill='#162540', outline=accent, width=1)
    draw.text((80, box_y + 24), takeaway_title, font=f_cat, fill=accent)

    # 3 Bullet Key Takeaways
    bullets = spec.get('bullets', [])
    by = box_y + 60
    for b in bullets:
        draw.ellipse([75, by + 6, 83, by + 14], fill=accent)
        draw.text((95, by), b, font=f_body, fill='#E2E8F0')
        by += 38

    # Source & Canonical Footer
    draw.line([(50, height - 44), (width - 50, height - 44)], fill='#1E293B', width=1)
    source_text = spec.get('source', 'Source: The Bull Print Quantitative Telemetry · Public Regulatory Filings (SEBI/IRDAI/NSE)')
    draw.text((50, height - 32), source_text, font=f_footer, fill='#64748B')
    draw.text((width - 250, height - 32), "https://bullprintmedia.com", font=f_footer, fill=accent)

    return img

print("Renderer ready.")
