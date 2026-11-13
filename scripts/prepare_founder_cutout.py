#!/usr/bin/env python3
"""
scripts/prepare_founder_cutout.py

Extracts the isolated founder portrait cutout (Sam Bankman-Fried in profile)
from the original penthouse plate using U2Net, applies a warm golden-hour rim filter
(brightness 1.15, contrast 1.10, warm amber specular lighting),
and saves it to:
1. remotion-engine/public/assets/short/short_founder_fg.png
2. remotion-engine/public/assets/cinematic/scene_founder_fg.png
"""

import os
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageEnhance

BASE_DIR = Path(__file__).resolve().parent.parent
BRAIN_DIR = Path("/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9")
SHORT_DIR = BASE_DIR / "remotion-engine" / "public" / "assets" / "short"
CINEMATIC_DIR = BASE_DIR / "remotion-engine" / "public" / "assets" / "cinematic"

SOURCE_IMAGE = BRAIN_DIR / "short_scene_1_penthouse_1793439768921.jpg"

def extract_founder():
    import onnxruntime as ort
    model_path = os.path.expanduser("~/.u2net/u2net.onnx")
    if not os.path.exists(model_path):
        print(f"[ERROR] U2Net model not found at {model_path}")
        return

    session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
    orig_img = Image.open(SOURCE_IMAGE).convert("RGB")
    w, h = orig_img.size

    # Preprocess 320x320
    img_320 = orig_img.resize((320, 320), Image.Resampling.BILINEAR)
    arr = np.array(img_320, dtype=np.float32) / 255.0
    arr = (arr - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    arr = np.transpose(arr, (2, 0, 1))
    arr = np.expand_dims(arr, 0).astype(np.float32)

    input_name = session.get_inputs()[0].name
    outs = session.run(None, {input_name: arr})
    d1 = outs[0][0, 0, :, :]
    d1 = (d1 - d1.min()) / (d1.max() - d1.min() + 1e-8)
    mask = Image.fromarray((d1 * 255).astype(np.uint8), mode='L').resize((w, h), Image.Resampling.BILINEAR)
    mask_arr = np.array(mask, dtype=np.float32) / 255.0

    # Founder is in the center/upper half (standing in profile looking out the window)
    # Clean thresholding to extract only human silhouette
    founder_mask = np.where(mask_arr > 0.35, np.clip(mask_arr * 1.4, 0, 1), 0.0)
    
    # Warm golden-hour grading for the founder
    enhancer_bright = ImageEnhance.Brightness(orig_img)
    warmed = enhancer_bright.enhance(1.18)
    enhancer_contrast = ImageEnhance.Contrast(warmed)
    warmed = enhancer_contrast.enhance(1.12)
    enhancer_color = ImageEnhance.Color(warmed)
    warmed = enhancer_color.enhance(1.25)

    r, g, b = warmed.split()
    final_alpha = (founder_mask * 255).astype(np.uint8)
    fg_rgba = Image.merge("RGBA", (r, g, b, Image.fromarray(final_alpha, mode='L')))

    # Save to short and cinematic
    short_out = SHORT_DIR / "short_founder_fg.png"
    fg_rgba.save(short_out, "PNG")
    print(f"[EXTRACTED] Founder Cutout -> {short_out.name} ({short_out.stat().st_size // 1024} KB)")

    # Also save as short_scene_1_fg.png so Scene 1 plane 3 uses it!
    short_scene_1_fg = SHORT_DIR / "short_scene_1_fg.png"
    fg_rgba.save(short_scene_1_fg, "PNG")
    print(f"[UPDATED] {short_scene_1_fg.name}")

    # 16:9 version
    cine_out = CINEMATIC_DIR / "scene_founder_fg.png"
    # Resize / pad to 16:9
    fg_cine = fg_rgba.resize((1920, 1080), Image.Resampling.LANCZOS)
    fg_cine.save(cine_out, "PNG")
    fg_cine.save(CINEMATIC_DIR / "scene_1_fg.png", "PNG")
    print(f"[EXTRACTED] 16:9 Founder Cutout -> {cine_out.name}")

if __name__ == "__main__":
    extract_founder()
