#!/usr/bin/env python3
"""
Render & Upload Short 03: The October Jobs Shocker: Why 165,000 Jobs Broke Wall Street
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
AUDIO_FILE = BASE_DIR / "output" / "shorts" / "short_03_audio.wav"
OUTPUT_DIR = BASE_DIR / "output" / "shorts"
OUTPUT_VIDEO = OUTPUT_DIR / "short_03_final.mp4"
ARTIFACT_VIDEO = BRAIN_DIR / "short_03_final.mp4"
THUMBNAIL_PATH = OUTPUT_DIR / "short_03_thumb.jpg"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader

PLATES_DIR = BASE_DIR / "output" / "shorts" / "plates"

CUTS = [
    {
        "id": 1,
        "start": 0.00,
        "end": 3.00,
        "plate": PLATES_DIR / "short_03_cut_01.jpg",
        "lines": ["65,000 JOBS", "EXPECTED"],
        "badge": "WALL STREET SHOCK",
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
        "plate": PLATES_DIR / "short_03_cut_02.jpg",
        "lines": ["165,000 JOBS", "EXPLODED"],
        "badge": "OCTOBER SURPRISE",
        "badge_color": (245, 30, 60),
        "badge_text_col": (255, 255, 255),
        "text_color": (255, 215, 0),
        "bloom_color": (255, 190, 30),
        "pos": (70, 240),
        "font_size": 130,
    },
    {
        "id": 3,
        "start": 6.00,
        "end": 9.00,
        "plate": PLATES_DIR / "short_03_cut_03.jpg",
        "lines": ["UNEMPLOYMENT", "FALLS TO 4.1%"],
        "badge": "LABOR MARKET",
        "badge_color": (255, 230, 0),
        "badge_text_col": (10, 10, 10),
        "text_color": (255, 215, 0),
        "bloom_color": (255, 190, 30),
        "pos": (70, 240),
        "font_size": 125,
    },
    {
        "id": 4,
        "start": 9.00,
        "end": 12.00,
        "plate": PLATES_DIR / "short_03_cut_04.jpg",
        "lines": ["WAGE GROWTH", "ACCELERATES"],
        "badge": "INFLATION RISK",
        "badge_color": (245, 30, 60),
        "badge_text_col": (255, 255, 255),
        "text_color": (245, 25, 55),
        "bloom_color": (255, 30, 60),
        "pos": (80, 250),
        "font_size": 125,
    },
    {
        "id": 5,
        "start": 12.00,
        "end": 15.00,
        "plate": PLATES_DIR / "short_03_cut_05.jpg",
        "lines": ["SHOULD BE", "CELEBRATION?"],
        "badge": "BULL TRAP",
        "badge_color": (255, 230, 0),
        "badge_text_col": (10, 10, 10),
        "text_color": (255, 215, 0),
        "bloom_color": (255, 190, 30),
        "pos": (80, 240),
        "font_size": 130,
    },
    {
        "id": 6,
        "start": 15.00,
        "end": 18.00,
        "plate": PLATES_DIR / "short_03_cut_06.jpg",
        "lines": ["BOND MARKET", "IN HORROR"],
        "badge": "SELL-OFF TRIGGERED",
        "badge_color": (245, 30, 60),
        "badge_text_col": (255, 255, 255),
        "text_color": (245, 25, 55),
        "bloom_color": (255, 30, 60),
        "pos": (80, 250),
        "font_size": 130,
    },
    {
        "id": 7,
        "start": 18.00,
        "end": 21.00,
        "plate": PLATES_DIR / "short_03_cut_07.jpg",
        "lines": ["TREASURY YIELDS", "RUSH TO 4.9%"],
        "badge": "YIELD SPIKE",
        "badge_color": (255, 230, 0),
        "badge_text_col": (10, 10, 10),
        "text_color": (255, 215, 0),
        "bloom_color": (255, 190, 30),
        "pos": (60, 240),
        "font_size": 120,
    },
    {
        "id": 8,
        "start": 21.00,
        "end": 24.00,
        "plate": PLATES_DIR / "short_03_cut_08.jpg",
        "lines": ["POWELL'S", "DILEMMA"],
        "badge": "FED TRAPPED",
        "badge_color": (245, 30, 60),
        "badge_text_col": (255, 255, 255),
        "text_color": (245, 25, 55),
        "bloom_color": (255, 30, 60),
        "pos": (80, 260),
        "font_size": 135,
    },
    {
        "id": 9,
        "start": 24.00,
        "end": 27.00,
        "plate": PLATES_DIR / "short_03_cut_09.jpg",
        "lines": ["NO RATE CUTS", "IN SIGHT"],
        "badge": "RATE FREEZE",
        "badge_color": (255, 230, 0),
        "badge_text_col": (10, 10, 10),
        "text_color": (255, 215, 0),
        "bloom_color": (255, 190, 30),
        "pos": (80, 250),
        "font_size": 130,
    },
    {
        "id": 10,
        "start": 27.00,
        "end": 30.00,
        "plate": PLATES_DIR / "short_03_cut_10.jpg",
        "lines": ["DEBT-FUELED", "STOCKS CRACK"],
        "badge": "DEBT SPIRAL",
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
        "end": 33.00,
        "plate": PLATES_DIR / "short_03_cut_11.jpg",
        "lines": ["GOOD NEWS", "IS BAD NEWS"],
        "badge": "PARADOX",
        "badge_color": (255, 230, 0),
        "badge_text_col": (10, 10, 10),
        "text_color": (255, 215, 0),
        "bloom_color": (255, 190, 30),
        "pos": (80, 250),
        "font_size": 130,
    },
    {
        "id": 12,
        "start": 33.00,
        "end": 36.74,
        "plate": PLATES_DIR / "short_03_cut_12.jpg",
        "lines": ["WELCOME TO", "MODERN FINANCE"],
        "badge": "THE REALITY",
        "badge_color": (245, 30, 60),
        "badge_text_col": (255, 255, 255),
        "text_color": (245, 25, 55),
        "bloom_color": (255, 30, 60),
        "pos": (70, 250),
        "font_size": 125,
    },
]

CAPTION_CHUNKS = [
    (0.10, 2.50, ["Wall", "Street", "expected"]),
    (2.50, 4.80, ["65,000", "new", "jobs."]),
    (4.80, 7.50, ["Instead,", "165,000", "exploded."]),
    (7.50, 10.00, ["Unemployment", "fell", "to", "4.1%"]),
    (10.00, 12.50, ["and", "wages", "surged", "fast."]),
    (12.50, 15.00, ["Should", "be", "celebration", "time."]),
    (15.00, 17.50, ["Instead,", "bond", "markets"]),
    (17.50, 20.00, ["reacted", "in", "horror."]),
    (20.00, 22.50, ["Treasury", "yields", "spiked"]),
    (22.50, 25.50, ["towards", "4.9%", "as", "investors"]),
    (25.50, 29.50, ["realized", "no", "rate", "cuts", "ahead."]),
    (29.50, 33.00, ["In", "modern", "finance,"]),
    (33.00, 36.74, ["good", "news", "is", "terrifying", "news."])
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
    
    # 1. Subtle camera drift (1.00 -> 1.05 zoom)
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

    # Dark atmospheric cinematic grade
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_ov = ImageDraw.Draw(overlay)
    
    # Top and bottom dark vignettes
    for y in range(450):
        alpha = int(170 * (1.0 - y / 450.0) ** 1.3)
        d_ov.line([(0, y), (W, y)], fill=(5, 5, 10, alpha))
    for y in range(H - 650, H):
        factor = (y - (H - 650)) / 650.0
        alpha = int(220 * (factor ** 1.2))
        d_ov.line([(0, y), (W, y)], fill=(0, 0, 5, alpha))

    # 2. Kinetic Elastic Slam for Hero 3D Typography (0.0s to 0.45s)
    slam_dur = 0.45
    if cut_t < slam_dur:
        p_slam = cut_t / slam_dur
        scale_anim = 1.35 - 0.35 * (math.sin(p_slam * math.pi * 0.5) ** 2)
        alpha_text = min(255, int(255 * (p_slam / 0.3)))
    else:
        scale_anim = 1.00
        alpha_text = 255

    # Render 3D typography onto dedicated high-res layer
    text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f_size = cut["font_size"]
    title_font = ImageFont.truetype(bold_font_path, f_size)
    badge_font = ImageFont.truetype(sub_font_path, 34)

    bx, by = cut["pos"]
    
    # Render Badge
    badge_text = cut["badge"]
    bb = badge_font.getbbox(badge_text)
    bw = (bb[2] - bb[0]) + 44
    bh = (bb[3] - bb[1]) + 20
    b_x1, b_y1 = bx, by - bh - 24
    b_x2, b_y2 = b_x1 + bw, b_y1 + bh
    
    d_text = ImageDraw.Draw(text_layer)
    # Badge glow
    d_text.rounded_rectangle([b_x1 - 3, b_y1 - 3, b_x2 + 3, b_y2 + 3], radius=10, fill=(0, 0, 0, 160))
    d_text.rounded_rectangle([b_x1, b_y1, b_x2, b_y2], radius=8, fill=cut["badge_color"] + (alpha_text,))
    d_text.text((b_x1 + 22, b_y1 + 10), badge_text, font=badge_font, fill=cut["badge_text_col"] + (alpha_text,))

    # Render Stacked 3D Extruded Text with Forward Shear
    line_spacing = int(f_size * 0.95)
    curr_y = by

    # 16-px 3D extrusion block
    ext_depth = 16
    for line in cut["lines"]:
        # Extrusion shadow passes
        for d in range(ext_depth, 0, -2):
            shade = max(10, 40 - d * 2)
            d_text.text((bx + d, curr_y + d), line, font=title_font, fill=(shade, shade, shade, int(alpha_text * 0.9)))
        
        # Heavy outer stroke
        for ox in [-4, -2, 0, 2, 4]:
            for oy in [-4, -2, 0, 2, 4]:
                if ox != 0 or oy != 0:
                    d_text.text((bx + ox, curr_y + oy), line, font=title_font, fill=(0, 0, 0, alpha_text))
        
        # Face text
        d_text.text((bx, curr_y), line, font=title_font, fill=cut["text_color"] + (alpha_text,))
        curr_y += line_spacing

    # Volumetric Neon Bloom Behind Text
    bloom_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_bloom = ImageDraw.Draw(bloom_layer)
    curr_y = by
    for line in cut["lines"]:
        d_bloom.text((bx, curr_y), line, font=title_font, fill=cut["bloom_color"] + (180,))
        curr_y += line_spacing
    bloom_layer = bloom_layer.filter(ImageFilter.GaussianBlur(radius=28))

    # Composite overlays
    frame.paste(overlay, (0, 0), overlay)
    frame.paste(bloom_layer, (0, 0), bloom_layer)
    frame.paste(text_layer, (0, 0), text_layer)

    # 3. Dynamic Word-Level Captions in Safe Zone (Y=1460 to 1540)
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

        # Background pill box
        pad_x, pad_y = 30, 16
        caption_draw.rounded_rectangle(
            [cap_x - pad_x, cap_y - pad_y, cap_x + tw + pad_x, cap_y + th + pad_y],
            radius=16,
            fill=(10, 10, 15, 210),
            outline=(255, 215, 0, 120),
            width=2
        )

        # Word-by-word rendering with active glowing highlight
        curr_word_x = cap_x
        for i, word in enumerate(words):
            w_bbox = cap_font.getbbox(word + " ")
            w_width = w_bbox[2] - w_bbox[0]
            
            if i == active_w_idx:
                col = (255, 230, 0) # Glowing Gold Active Word
                # Drop shadow on active word
                caption_draw.text((curr_word_x + 2, cap_y + 2), word, font=cap_font, fill=(0, 0, 0))
                caption_draw.text((curr_word_x, cap_y), word, font=cap_font, fill=col)
            else:
                col = (240, 240, 245) # Clean White
                caption_draw.text((curr_word_x, cap_y), word, font=cap_font, fill=col)
                
            curr_word_x += w_width

    return frame

def main():
    print("=" * 70)
    print("🎬 RENDERING SHORT 03: The October Jobs Shocker")
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

    # Save thumbnail from first frame
    first_thumb = render_frame(1.2, CUTS[0], plates, bold_font, sub_font)
    first_thumb.save(THUMBNAIL_PATH, quality=95)
    print(f"📸 Saved Custom High-CTR Thumbnail -> {THUMBNAIL_PATH}")

    # Render video stream directly into ffmpeg pipe
    fps = 30
    total_dur = 36.74
    total_frames = int(fps * total_dur)
    w, h = 1080, 1920

    raw_video = OUTPUT_DIR / "temp_short_03_raw.mp4"

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

    print(f"🎬 Rendering Short 03 ({total_frames} frames)...")
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

    # Mux with master audio
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

    # Upload to YouTube as Private
    print("\n" + "=" * 70)
    print("🚀 UPLOADING SHORT 03 TO YOUTUBE (PRIVATE)")
    print("=" * 70)
    uploader = YouTubeUploader()
    title = "The October Jobs Shocker: Why 165,000 Jobs Broke Wall Street #Shorts"
    desc = """Wall Street was expecting 65,000 new jobs. Instead, the economy exploded with 165,000. Why great economic news triggered a massive bond market sell-off.

Subscribe to @TheBullPrint for daily financial intelligence and macroeconomic breakdowns.

#TheBullPrint #USEconomy #JobsReport #FederalReserve #InterestRates #BondMarket #Shorts"""
    tags = ["TheBullPrint", "USEconomy", "JobsReport", "FederalReserve", "InterestRates", "BondMarket", "Shorts"]

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
        print(f"🎉 SHORT 03 IS UPLOADED (PRIVATE): {url} (ID: {vid_id})")
        
        # Dispatch Telegram notification via ARIA
        try:
            import requests
            tg_token = "8829963924:AAE7v_xEQXLmy3-YEx8kqMo2GRfnbnxf4GA"
            tg_chat_id = "1126599043"
            msg = f"✅ *ARIA Task Complete: Short 03*\n\n*{title}*\n• 12 Micro-Beat Cuts (1 frame every 3.0s)\n• 2048px Google Flow 35mm photographic plates\n• MagnatesMedia 3D forward-sheared typography & tactical badges\n• Uploaded to YouTube (Private): {url}"
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
