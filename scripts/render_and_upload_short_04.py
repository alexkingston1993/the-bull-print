#!/usr/bin/env python3
"""
Render & Upload Short 04: The ₹14,900 Crore U-Turn: FIIs Rush Back to Dalal Street
Format: Vertical 9:16 (1080x1920)
Style: MagnatesMedia Visual & Kinetic 3D Typography
Privacy Status: PRIVATE
"""

import math
import os
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path(__file__).resolve().parent.parent
BRAIN_DIR = Path("/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364")
AUDIO_FILE = BASE_DIR / "output" / "shorts" / "short_04_audio.wav"
OUTPUT_DIR = BASE_DIR / "output" / "shorts"
OUTPUT_VIDEO = OUTPUT_DIR / "short_04_final.mp4"
ARTIFACT_VIDEO = BRAIN_DIR / "short_04_final.mp4"
THUMBNAIL_PATH = OUTPUT_DIR / "short_04_thumb.jpg"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

PLATES_DIR = BASE_DIR / "output" / "shorts" / "plates"

CUTS = [
    {
        "id": 1,
        "start": 0.00,
        "end": 3.00,
        "plate": PLATES_DIR / "short_04_cut_01.jpg",
        "lines": ["RETAIL GAVE UP", "ON DALAL ST"],
        "badge": "RETAIL SURRENDER",
        "badge_color": (255, 230, 0),
        "badge_text_col": (10, 10, 10),
        "text_color": (245, 25, 55),
        "bloom_color": (255, 30, 60),
        "pos": (80, 260),
        "font_size": 130,
    },
    {
        "id": 2,
        "start": 3.00,
        "end": 6.00,
        "plate": PLATES_DIR / "short_04_cut_02.jpg",
        "lines": ["FOREIGN FUNDS", "VIOLENT U-TURN"],
        "badge": "INSTITUTIONAL SHOCK",
        "badge_color": (245, 30, 60),
        "badge_text_col": (255, 255, 255),
        "text_color": (255, 215, 0),
        "bloom_color": (255, 190, 30),
        "pos": (70, 240),
        "font_size": 125,
    },
    {
        "id": 3,
        "start": 6.00,
        "end": 9.00,
        "plate": PLATES_DIR / "short_04_cut_03.jpg",
        "lines": ["₹14,900 CRORE", "PUMPED IN"],
        "badge": "RECORD INFLOW",
        "badge_color": (0, 230, 100),
        "badge_text_col": (10, 10, 10),
        "text_color": (0, 240, 120),
        "bloom_color": (0, 255, 130),
        "pos": (70, 240),
        "font_size": 130,
    },
    {
        "id": 4,
        "start": 9.00,
        "end": 12.00,
        "plate": PLATES_DIR / "short_04_cut_04.jpg",
        "lines": ["BIGGEST BUYING", "IN 7 MONTHS"],
        "badge": "7-MONTH RECORD",
        "badge_color": (245, 30, 60),
        "badge_text_col": (255, 255, 255),
        "text_color": (245, 25, 55),
        "bloom_color": (255, 30, 60),
        "pos": (70, 240),
        "font_size": 125,
    },
    {
        "id": 5,
        "start": 12.00,
        "end": 15.00,
        "plate": PLATES_DIR / "short_04_cut_05.jpg",
        "lines": ["NIFTY & SENSEX", "BREAKOUT RALLY"],
        "badge": "MARKET EXPLOSION",
        "badge_color": (0, 230, 100),
        "badge_text_col": (10, 10, 10),
        "text_color": (0, 240, 120),
        "bloom_color": (0, 255, 130),
        "pos": (70, 240),
        "font_size": 125,
    },
    {
        "id": 6,
        "start": 15.00,
        "end": 18.00,
        "plate": PLATES_DIR / "short_04_cut_06.jpg",
        "lines": ["RETAIL DUMPED", "AT THE BOTTOM"],
        "badge": "RETAIL PANIC",
        "badge_color": (245, 30, 60),
        "badge_text_col": (255, 255, 255),
        "text_color": (245, 25, 55),
        "bloom_color": (255, 30, 60),
        "pos": (80, 250),
        "font_size": 125,
    },
    {
        "id": 7,
        "start": 18.00,
        "end": 21.00,
        "plate": PLATES_DIR / "short_04_cut_07.jpg",
        "lines": ["SMART MONEY", "ACCUMULATING"],
        "badge": "SMART MONEY MOVE",
        "badge_color": (255, 230, 0),
        "badge_text_col": (10, 10, 10),
        "text_color": (255, 215, 0),
        "bloom_color": (255, 190, 30),
        "pos": (70, 240),
        "font_size": 130,
    },
    {
        "id": 8,
        "start": 21.00,
        "end": 24.00,
        "plate": PLATES_DIR / "short_04_cut_08.jpg",
        "lines": ["BANKING & TECH", "BLUECHIPS"],
        "badge": "TARGET SECTORS",
        "badge_color": (245, 30, 60),
        "badge_text_col": (255, 255, 255),
        "text_color": (255, 215, 0),
        "bloom_color": (255, 190, 30),
        "pos": (70, 240),
        "font_size": 125,
    },
    {
        "id": 9,
        "start": 24.00,
        "end": 27.00,
        "plate": PLATES_DIR / "short_04_cut_09.jpg",
        "lines": ["CHEAP VALUATION", "FIRE SALE"],
        "badge": "DISCOUNT HUNTING",
        "badge_color": (255, 230, 0),
        "badge_text_col": (10, 10, 10),
        "text_color": (255, 215, 0),
        "bloom_color": (255, 190, 30),
        "pos": (70, 240),
        "font_size": 125,
    },
    {
        "id": 10,
        "start": 27.00,
        "end": 30.00,
        "plate": PLATES_DIR / "short_04_cut_10.jpg",
        "lines": ["OUTFLOW IS NOT", "AN EXIT"],
        "badge": "GOLDEN LESSON",
        "badge_color": (245, 30, 60),
        "badge_text_col": (255, 255, 255),
        "text_color": (245, 25, 55),
        "bloom_color": (255, 30, 60),
        "pos": (80, 250),
        "font_size": 125,
    },
    {
        "id": 11,
        "start": 30.00,
        "end": 34.20,
        "plate": PLATES_DIR / "short_04_cut_11.jpg",
        "lines": ["FOLLOW THE", "SMART MONEY"],
        "badge": "THE VERDICT",
        "badge_color": (255, 230, 0),
        "badge_text_col": (10, 10, 10),
        "text_color": (255, 215, 0),
        "bloom_color": (255, 190, 30),
        "pos": (80, 250),
        "font_size": 130,
    },
]

CAPTION_CHUNKS = [
    (0.10, 2.50, ["Just", "when", "retail", "gave", "up,"]),
    (2.50, 4.80, ["foreign", "funds", "pulled", "a"]),
    (4.80, 7.00, ["violent", "U-turn", "on", "Dalal", "Street."]),
    (7.00, 9.40, ["In", "a", "single", "session,"]),
    (9.40, 11.80, ["foreign", "funds", "pumped"]),
    (11.80, 14.00, ["₹14,900", "Crore", "into", "bluechips."]),
    (14.00, 16.50, ["It", "marks", "the", "largest"]),
    (16.50, 18.80, ["one-day", "frenzy", "in", "7", "months,"]),
    (18.80, 21.00, ["sparking", "a", "massive", "rally."]),
    (21.00, 23.50, ["While", "retail", "panicked,"]),
    (23.50, 25.80, ["smart", "money", "scooped", "up"]),
    (25.80, 28.00, ["banking", "and", "tech", "leaders."]),
    (28.00, 31.00, ["Never", "mistake", "temporary", "outflows"]),
    (31.00, 34.20, ["for", "a", "permanent", "exit."])
]

def load_and_prep_plate(path, w=1080, h=1920):
    img = Image.open(path).convert("RGB")
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    return img.crop((left, top, left + w, top + h))

def get_fonts():
    bold_candidates = [
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/Library/Fonts/Impact.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
    ]
    sub_candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    bold_path = next((p for p in bold_candidates if os.path.exists(p)), None)
    sub_path = next((p for p in sub_candidates if os.path.exists(p)), None)
    return bold_path, sub_path

def render_frame(t, cut, plates, bold_font_path, sub_font_path):
    W, H = 1080, 1920
    base_plate = plates[cut["id"]]
    
    cut_t = t - cut["start"]
    cut_dur = cut["end"] - cut["start"]
    progress = max(0.0, min(1.0, cut_t / cut_dur))
    zoom = 1.0 + 0.05 * progress
    
    zw = int(W * zoom)
    zh = int(H * zoom)
    frame = base_plate.resize((zw, zh), Image.Resampling.BILINEAR)
    x_crop = (zw - W) // 2
    y_crop = (zh - H) // 2
    frame = frame.crop((x_crop, y_crop, x_crop + W, y_crop + H))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_ov = ImageDraw.Draw(overlay)
    
    for y in range(450):
        alpha = int(170 * (1.0 - y / 450.0) ** 1.3)
        d_ov.line([(0, y), (W, y)], fill=(5, 5, 10, alpha))
    for y in range(H - 650, H):
        factor = (y - (H - 650)) / 650.0
        alpha = int(220 * (factor ** 1.2))
        d_ov.line([(0, y), (W, y)], fill=(0, 0, 5, alpha))

    slam_dur = 0.45
    if cut_t < slam_dur:
        p_slam = cut_t / slam_dur
        scale_anim = 1.35 - 0.35 * (math.sin(p_slam * math.pi * 0.5) ** 2)
        alpha_text = min(255, int(255 * (p_slam / 0.3)))
    else:
        scale_anim = 1.00
        alpha_text = 255

    text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f_size = cut["font_size"]
    title_font = ImageFont.truetype(bold_font_path, f_size)
    badge_font = ImageFont.truetype(sub_font_path, 34)

    bx, by = cut["pos"]
    
    badge_text = cut["badge"]
    bb = badge_font.getbbox(badge_text)
    bw = (bb[2] - bb[0]) + 44
    bh = (bb[3] - bb[1]) + 20
    b_x1, b_y1 = bx, by - bh - 24
    b_x2, b_y2 = b_x1 + bw, b_y1 + bh
    
    d_text = ImageDraw.Draw(text_layer)
    d_text.rounded_rectangle([b_x1 - 3, b_y1 - 3, b_x2 + 3, b_y2 + 3], radius=10, fill=(0, 0, 0, 160))
    d_text.rounded_rectangle([b_x1, b_y1, b_x2, b_y2], radius=8, fill=cut["badge_color"] + (alpha_text,))
    d_text.text((b_x1 + 22, b_y1 + 10), badge_text, font=badge_font, fill=cut["badge_text_col"] + (alpha_text,))

    line_spacing = int(f_size * 0.95)
    curr_y = by

    ext_depth = 16
    for line in cut["lines"]:
        for d in range(ext_depth, 0, -2):
            shade = max(10, 40 - d * 2)
            d_text.text((bx + d, curr_y + d), line, font=title_font, fill=(shade, shade, shade, int(alpha_text * 0.9)))
        
        for ox in [-4, -2, 0, 2, 4]:
            for oy in [-4, -2, 0, 2, 4]:
                if ox != 0 or oy != 0:
                    d_text.text((bx + ox, curr_y + oy), line, font=title_font, fill=(0, 0, 0, alpha_text))
        
        d_text.text((bx, curr_y), line, font=title_font, fill=cut["text_color"] + (alpha_text,))
        curr_y += line_spacing

    bloom_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_bloom = ImageDraw.Draw(bloom_layer)
    curr_y = by
    for line in cut["lines"]:
        d_bloom.text((bx, curr_y), line, font=title_font, fill=cut["bloom_color"] + (180,))
        curr_y += line_spacing
    bloom_layer = bloom_layer.filter(ImageFilter.GaussianBlur(radius=28))

    frame.paste(overlay, (0, 0), overlay)
    frame.paste(bloom_layer, (0, 0), bloom_layer)
    frame.paste(text_layer, (0, 0), text_layer)

    caption_draw = ImageDraw.Draw(frame)
    cap_font = ImageFont.truetype(sub_font_path, 46)
    
    active_chunk = None
    for c_start, c_end, words in CAPTION_CHUNKS:
        if c_start <= t <= c_end:
            active_chunk = (c_start, c_end, words)
            break
            
    if active_chunk:
        c_start, c_end, words = active_chunk
        tot_dur = c_end - c_start
        w_dur = tot_dur / max(1, len(words))
        active_w_idx = int((t - c_start) / w_dur)
        active_w_idx = max(0, min(len(words) - 1, active_w_idx))

        full_text = " ".join(words)
        bbox = cap_font.getbbox(full_text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        cap_x = (W - tw) // 2
        cap_y = 1480

        pad_x, pad_y = 30, 16
        caption_draw.rounded_rectangle(
            [cap_x - pad_x, cap_y - pad_y, cap_x + tw + pad_x, cap_y + th + pad_y],
            radius=16,
            fill=(10, 10, 15, 210),
            outline=(0, 230, 100, 120),
            width=2
        )

        curr_word_x = cap_x
        for i, word in enumerate(words):
            w_bbox = cap_font.getbbox(word + " ")
            w_width = w_bbox[2] - w_bbox[0]
            
            if i == active_w_idx:
                col = (0, 240, 120) if "14,900" in word or "U-turn" in word else (255, 230, 0)
                caption_draw.text((curr_word_x + 2, cap_y + 2), word, font=cap_font, fill=(0, 0, 0))
                caption_draw.text((curr_word_x, cap_y), word, font=cap_font, fill=col)
            else:
                col = (240, 240, 245)
                caption_draw.text((curr_word_x, cap_y), word, font=cap_font, fill=col)
                
            curr_word_x += w_width

    return frame

def main():
    print("=" * 70)
    print("🎬 RENDERING SHORT 04: The ₹14,900 Crore U-Turn")
    print("=" * 70)

    bold_font, sub_font = get_fonts()
    if not bold_font or not sub_font:
        raise FileNotFoundError("Missing required TrueType fonts.")

    print("⏳ Preloading 5 vertical 9:16 background plates...")
    plates = {}
    for cut in CUTS:
        cid = cut["id"]
        p_path = cut["plate"]
        if not p_path.exists():
            raise FileNotFoundError(f"Missing plate for Cut {cid}: {p_path}")
        plates[cid] = load_and_prep_plate(p_path)

    first_thumb = render_frame(1.2, CUTS[0], plates, bold_font, sub_font)
    first_thumb.save(THUMBNAIL_PATH, quality=95)
    print(f"📸 Saved Custom High-CTR Thumbnail -> {THUMBNAIL_PATH}")

    fps = 30
    total_dur = 34.20
    total_frames = int(fps * total_dur)
    w, h = 1080, 1920

    raw_video = OUTPUT_DIR / "temp_short_04_raw.mp4"

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{w}x{h}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(raw_video)
    ]

    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    print(f"🎬 Rendering Short 04 ({total_frames} frames)...")
    for f_idx in range(total_frames):
        t = f_idx / fps
        active_cut = CUTS[0]
        for c in CUTS:
            if c["start"] <= t <= c["end"]:
                active_cut = c
                break

        img = render_frame(t, active_cut, plates, bold_font, sub_font)
        proc.stdin.write(img.tobytes())

        if f_idx % 90 == 0 or f_idx == total_frames - 1:
            pct = (f_idx / total_frames) * 100
            print(f"  Frame {f_idx+1}/{total_frames} ({pct:.1f}%) rendered...")

    proc.stdin.close()
    proc.wait()

    print("🎵 Muxing with master stereo narration and soundtrack...")
    mux_cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
        "-i", str(AUDIO_FILE),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(OUTPUT_VIDEO)
    ]
    subprocess.run(mux_cmd, check=True)
    shutil.copy2(OUTPUT_VIDEO, ARTIFACT_VIDEO)
    raw_video.unlink(missing_ok=True)
    print(f"🎉 RENDER COMPLETE: {OUTPUT_VIDEO}")

    print("\n" + "=" * 70)
    print("🚀 UPLOADING SHORT 04 TO YOUTUBE (PRIVATE)")
    print("=" * 70)
    uploader = YouTubeUploader()
    title = "The ₹14,900 Crore U-Turn: FIIs Rush Back to Dalal Street #Shorts"
    desc = """Foreign institutional investors execute their biggest single-day buying spree in 7 months, pumping ₹14,900 crore into Indian bluechips.

Subscribe to @TheBullPrint for daily financial intelligence and macroeconomic breakdowns.

#TheBullPrint #DalalStreet #FII #Sensex #Nifty50 #IndianStockMarket #Shorts"""
    tags = ["TheBullPrint", "DalalStreet", "FII", "Sensex", "Nifty50", "IndianStockMarket", "Shorts"]

    res = uploader.upload_video(
        language="en",
        video_path=str(OUTPUT_VIDEO),
        title=title,
        description=desc,
        tags=tags,
        category_id="25",
        privacy_status="private",
        is_short=True,
        thumbnail_path=str(THUMBNAIL_PATH) if THUMBNAIL_PATH.exists() else None,
        force_upload=True
    )

    if res.get("success"):
        vid_id = res.get("video_id")
        url = res.get("url") or f"https://www.youtube.com/shorts/{vid_id}"
        print(f"🎉 SHORT 04 IS UPLOADED (PRIVATE): {url} (ID: {vid_id})")
        
        # Dispatch Telegram notification via ARIA
        try:
            import requests
            tg_token = "8829963924:AAE7v_xEQXLmy3-YEx8kqMo2GRfnbnxf4GA"
            tg_chat_id = "1126599043"
            msg = f"✅ *ARIA Task Complete: Short 04*\n\n*{title}*\n• 11 Micro-Beat Cuts (1 frame every 3.0s)\n• 2048px Google Flow 35mm photographic plates\n• MagnatesMedia 3D forward-sheared typography & tactical badges\n• Uploaded to YouTube (Private): {url}"
            requests.post(f"https://api.telegram.org/bot{tg_token}/sendMessage", json={"chat_id": tg_chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
            print("📲 Telegram alert sent via ARIA.")
        except Exception as e:
            print(f"Telegram notice warning: {e}")

        return url, vid_id
    else:
        print(f"❌ Upload failed: {res.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
