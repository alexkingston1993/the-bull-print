#!/usr/bin/env python3
"""
scripts/prepare_short_assets.py
Curates and downloads authentic portrait 9:16 documentary assets for the Short video,
copies newly generated AI portrait plates, and extracts transparent RGBA cutouts
using the local U2Net ONNX engine.
"""

import os
import shutil
import sys
from pathlib import Path
import requests
import numpy as np
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.material import get_api_key

SHORT_ASSETS_DIR = BASE_DIR / "remotion-engine" / "public" / "assets" / "short"
SHORT_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# 1. Source generated images
GENERATED_MAP = {
    "short_scene_1_penthouse.jpg": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/short_scene_1_penthouse_1793439768921.jpg",
    "short_scene_2_trading.jpg": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/short_scene_2_trading_1793439809089.jpg",
    "short_scene_3_vault.jpg": "/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/short_scene_3_vault_1793439853059.jpg",
}

# 2. Pexels portrait queries for remaining scenes
PEXELS_QUERIES = {
    "short_scene_4_corkboard.jpg": "investigation pinboard documents",
    "short_scene_5_desk.jpg": "dark wood vintage desk lamp paper",
    "short_scene_6_server.jpg": "data center server dark corridor blue lights",
    "short_scene_7_courtroom.jpg": "courtroom gavel justice wood bench",
}

def copy_generated_plates():
    print("=== COPYING FRESH GENERATED 9:16 PLATES ===")
    for dest_name, src_path in GENERATED_MAP.items():
        if os.path.exists(src_path):
            dest = SHORT_ASSETS_DIR / dest_name
            shutil.copy2(src_path, dest)
            print(f"[COPIED] {dest_name} ({os.path.getsize(dest) // 1024} KB)")
        else:
            print(f"[MISSING] {src_path}")

def download_pexels_portrait():
    print("=== DOWNLOADING PEXELS PORTRAIT ASSETS ===")
    api_key = get_api_key("pexels_api_keys")
    headers = {"Authorization": api_key}
    
    for filename, query in PEXELS_QUERIES.items():
        dest = SHORT_ASSETS_DIR / filename
        if dest.exists() and dest.stat().st_size > 50000:
            print(f"[EXISTS] {filename}")
            continue
            
        url = f"https://api.pexels.com/v1/search?query={requests.utils.quote(query)}&orientation=portrait&per_page=5"
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                photos = r.json().get("photos", [])
                if photos:
                    img_url = photos[0]["src"].get("original") or photos[0]["src"].get("large2x")
                    img_r = requests.get(img_url, timeout=30)
                    if img_r.status_code == 200:
                        dest.write_bytes(img_r.content)
                        # Crop or resize to 1080x1920 if needed
                        with Image.open(dest) as im:
                            w, h = im.size
                            # Center crop to 9:16
                            target_ratio = 9.0 / 16.0
                            current_ratio = w / h
                            if current_ratio > target_ratio:
                                new_w = int(h * target_ratio)
                                left = (w - new_w) // 2
                                im_cropped = im.crop((left, 0, left + new_w, h))
                            else:
                                new_h = int(w / target_ratio)
                                top = (h - new_h) // 2
                                im_cropped = im.crop((0, top, w, top + new_h))
                            im_final = im_cropped.resize((1080, 1920), Image.Resampling.LANCZOS)
                            im_final.save(dest, quality=92)
                        print(f"[DOWNLOADED & CROPPED] {filename} -> 1080x1920 ({dest.stat().st_size // 1024} KB)")
        except Exception as e:
            print(f"[ERROR] Failed {filename}: {e}")

def extract_cutouts():
    print("=== EXTRACTING 9:16 TRANSPARENT RGBA FOREGROUND CUTOUTS ===")
    import onnxruntime as ort
    
    model_path = os.path.expanduser("~/.u2net/u2net.onnx")
    if not os.path.exists(model_path):
        print(f"[ERROR] U2Net model not found at {model_path}")
        return
        
    session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
    input_name = session.get_inputs()[0].name
    
    cutout_targets = [
        ("short_scene_1_penthouse.jpg", "short_scene_1_fg.png", "salient"),
        ("short_scene_2_trading.jpg", "short_scene_2_fg.png", "salient"),
        ("short_scene_3_vault.jpg", "short_scene_3_fg.png", "foreground_table"),
        ("short_scene_6_server.jpg", "short_scene_6_fg.png", "foreground_depth"),
        ("short_scene_7_courtroom.jpg", "short_scene_7_fg.png", "foreground_depth")
    ]
    
    for in_name, out_name, mode in cutout_targets:
        in_path = SHORT_ASSETS_DIR / in_name
        out_path = SHORT_ASSETS_DIR / out_name
        
        if not in_path.exists():
            print(f"[SKIP] {in_name} not found")
            continue
            
        img = Image.open(in_path).convert("RGB")
        w, h = img.size
        
        # Ensure base image is exactly 1080x1920
        if (w, h) != (1080, 1920):
            img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
            img.save(in_path, quality=94)
            w, h = 1080, 1920
            
        img_np = np.array(img).astype(np.float32) / 255.0
        
        if mode == "salient":
            # Run U2Net for salient human/subject cutout
            resized = img.resize((320, 320), Image.Resampling.BILINEAR)
            arr = np.array(resized).astype(np.float32) / 255.0
            # Normalize with ImageNet stats
            arr = (arr - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
            arr = np.transpose(arr, (2, 0, 1))
            arr = np.expand_dims(arr, 0).astype(np.float32)
            
            pred = session.run(None, {input_name: arr})[0]
            mask = pred[0, 0]
            mask = (mask - mask.min()) / (mask.max() - mask.min() + 1e-8)
            mask_img = Image.fromarray((mask * 255).astype(np.uint8)).resize((w, h), Image.Resampling.BILINEAR)
            mask_arr = np.array(mask_img).astype(np.float32) / 255.0
            
            # Smooth threshold
            alpha = np.clip((mask_arr - 0.2) / 0.6, 0, 1)
            if in_name == "short_scene_1_penthouse.jpg":
                # Also include foreground dining table (y > 1420)
                y_coords = np.linspace(0, 1, h)[:, None]
                table_mask = np.repeat(np.clip((y_coords - 0.74) / 0.10, 0, 1), w, axis=1)
                alpha = np.clip(alpha + table_mask, 0, 1)
        elif mode == "foreground_table":
            # Foreground table with depth & luminance contouring
            y_coords = np.linspace(0, 1, h)[:, None]
            depth_weight = np.clip((y_coords - 0.55) / 0.15, 0.0, 1.0)
            gray = np.dot(img_np, [0.299, 0.587, 0.114])
            obj_signal = np.clip((gray - 0.08) / 0.22, 0.0, 1.0) * depth_weight
            base_floor = np.clip((y_coords - 0.72) / 0.12, 0.0, 1.0)
            alpha = np.clip(obj_signal * 0.75 + base_floor * 0.65, 0.0, 1.0)
            alpha = alpha * (y_coords > 0.52)
        else:
            # Foreground object contour for server / courtroom
            y_coords = np.linspace(0, 1, h)[:, None]
            depth_weight = np.clip((y_coords - 0.58) / 0.16, 0.0, 1.0)
            gray = np.dot(img_np, [0.299, 0.587, 0.114])
            obj_signal = np.clip((gray - 0.07) / 0.20, 0.0, 1.0) * depth_weight
            base_floor = np.clip((y_coords - 0.75) / 0.12, 0.0, 1.0)
            alpha = np.clip(obj_signal * 0.70 + base_floor * 0.70, 0.0, 1.0)
            alpha = alpha * (y_coords > 0.54)
            
        alpha_channel = (alpha * 255).astype(np.uint8)
        rgba = Image.fromarray(np.dstack([img_np * 255, alpha_channel]).astype(np.uint8))
        rgba.save(out_path, format="PNG")
        
        # Verify transparency ratio
        trans_ratio = np.mean(alpha_channel < 25)
        print(f"[CUTOUT READY] {out_name}: RGBA, {trans_ratio * 100:.1f}% transparent background")

if __name__ == "__main__":
    copy_generated_plates()
    download_pexels_portrait()
    extract_cutouts()
