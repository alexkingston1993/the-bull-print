#!/usr/bin/env python3
"""
scripts/prepare_native_16x9_assets.py

Creates strictly native 16:9 widescreen assets for the landscape master:
1. scene_1_fg.png & scene_founder_fg.png:
   - 1920x1080 transparent RGBA canvas
   - Preserves 100% natural 1:1 aspect ratio of the founder (NO HORIZONTAL SQUEEZE OR STRETCH)
   - Positions founder in the right third of the frame (x=1200, bottom=1080) looking out over the window
2. scene_forbes_portrait.png:
   - Clean, centered portrait cutout of Sam Bankman-Fried for the Forbes magazine cover
"""

import os
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageEnhance

BASE_DIR = Path(__file__).resolve().parent.parent
BRAIN_DIR = Path("/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9")
CINEMATIC_DIR = BASE_DIR / "remotion-engine" / "public" / "assets" / "cinematic"

SOURCE_IMAGE = BRAIN_DIR / "short_scene_1_penthouse_1793439768921.jpg"

def build_native_16x9_founder():
    import onnxruntime as ort
    model_path = os.path.expanduser("~/.u2net/u2net.onnx")
    if not os.path.exists(model_path):
        print(f"[ERROR] U2Net model not found at {model_path}")
        return

    session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
    orig_img = Image.open(SOURCE_IMAGE).convert("RGB")
    orig_w, orig_h = orig_img.size

    # Run U2Net
    img_320 = orig_img.resize((320, 320), Image.Resampling.BILINEAR)
    arr = np.array(img_320, dtype=np.float32) / 255.0
    arr = (arr - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    arr = np.transpose(arr, (2, 0, 1))
    arr = np.expand_dims(arr, 0).astype(np.float32)

    input_name = session.get_inputs()[0].name
    outs = session.run(None, {input_name: arr})
    d1 = outs[0][0, 0, :, :]
    d1 = (d1 - d1.min()) / (d1.max() - d1.min() + 1e-8)
    mask = Image.fromarray((d1 * 255).astype(np.uint8), mode='L').resize((orig_w, orig_h), Image.Resampling.BILINEAR)
    mask_arr = np.array(mask, dtype=np.float32) / 255.0

    # Founder silhouette threshold
    founder_mask = np.where(mask_arr > 0.35, np.clip(mask_arr * 1.4, 0, 1), 0.0)

    # Warm golden-hour grading
    warmed = ImageEnhance.Brightness(orig_img).enhance(1.18)
    warmed = ImageEnhance.Contrast(warmed).enhance(1.12)
    warmed = ImageEnhance.Color(warmed).enhance(1.25)

    r, g, b = warmed.split()
    final_alpha = (founder_mask * 255).astype(np.uint8)
    isolated_founder = Image.merge("RGBA", (r, g, b, Image.fromarray(final_alpha, mode='L')))

    # Crop to bounding box of the founder
    bbox = isolated_founder.getbbox()
    if bbox:
        cropped_founder = isolated_founder.crop(bbox)
        cw, ch = cropped_founder.size
        print(f"[FOUNDER BBOX] {cw}x{ch}")

        # 1. Scaled for 16:9 Scene 1 (Height = 960px, aspect ratio 100% preserved)
        target_h = 960
        scale = target_h / float(ch)
        target_w = int(cw * scale)
        scaled_founder = cropped_founder.resize((target_w, target_h), Image.Resampling.LANCZOS)

        canvas_16x9 = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
        pos_x = 1220
        pos_y = 1080 - target_h + 20
        canvas_16x9.paste(scaled_founder, (pos_x, pos_y), scaled_founder)

        out_path = CINEMATIC_DIR / "scene_1_fg.png"
        canvas_16x9.save(out_path, "PNG")
        canvas_16x9.save(CINEMATIC_DIR / "scene_founder_fg.png", "PNG")
        print(f"✅ Generated Native 16:9 Founder Plate: {out_path} ({canvas_16x9.size})")

        # 2. Centered Forbes Portrait (for cover placement)
        forbes_portrait = cropped_founder.resize((450, int(ch * (450.0 / cw))), Image.Resampling.LANCZOS)
        forbes_out = CINEMATIC_DIR / "scene_forbes_portrait.png"
        forbes_portrait.save(forbes_out, "PNG")
        print(f"✅ Generated Centered Forbes Portrait: {forbes_out}")

if __name__ == "__main__":
    build_native_16x9_founder()
