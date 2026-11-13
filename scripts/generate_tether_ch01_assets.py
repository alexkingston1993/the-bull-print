#!/usr/bin/env python3
"""
scripts/generate_tether_ch01_assets.py

Generates 12 distinct, native 16:9 (1920x1080) photorealistic Tether visual plates
and 4 U2Net neural cutouts inside remotion-engine/public/assets/episodes/tether_ch01/.
Zero FTX / SBF leftovers.
"""

import os
import sys
import numpy as np
import requests
from PIL import Image, ImageEnhance
import onnxruntime as ort

OUTPUT_DIR = "remotion-engine/public/assets/episodes/tether_ch01"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PEXELS_KEY = "2927GljrcuM0PxfFHrBTUfShGAHLL2LcVGbGhuQkxddHHTZ61NzP1sSb"
HEADERS = {"Authorization": PEXELS_KEY}
MODEL_PATH = os.path.expanduser("~/.u2net/u2net.onnx")

BG_SPECS = [
    {
        "filename": "bg_01_manhattan_treasury.jpg",
        "query": "manhattan financial district treasury building sunny columns",
        "grade": {"bright": 1.15, "contrast": 1.12, "sat": 1.25}, # SOLAR_EMPIRE
    },
    {
        "filename": "bg_02_cantor_trading_desk.jpg",
        "query": "stock broker trading desk multiple screens financial monitors office",
        "grade": {"bright": 1.12, "contrast": 1.15, "sat": 1.20}, # SOLAR_EMPIRE
    },
    {
        "filename": "bg_03_usdt_global_liquidity.jpg",
        "query": "digital network connection global lines cyan world technology",
        "grade": {"bright": 1.05, "contrast": 1.25, "sat": 1.35}, # HYPER_GROWTH
    },
    {
        "filename": "bg_04_nyse_floor_comparison.jpg",
        "query": "stock exchange traders crowd floor wall street bustling",
        "grade": {"bright": 1.08, "contrast": 1.18, "sat": 1.25}, # HYPER_GROWTH
    },
    {
        "filename": "bg_05_fortune_cover_backdrop.jpg",
        "query": "luxury boardroom glass skyscraper dark elegant studio background",
        "grade": {"bright": 0.95, "contrast": 1.20, "sat": 1.10}, # HIGH_STAKES_ARENA
    },
    {
        "filename": "bg_06_bvi_offshore_harbor.jpg",
        "query": "tropical caribbean harbor yachts luxury waterfront villas sunny",
        "grade": {"bright": 1.05, "contrast": 1.15, "sat": 1.25}, # HIGH_STAKES_ARENA
    },
    {
        "filename": "bg_07_cantor_vault_bullion.jpg",
        "query": "bank vault gold bars bullion high security safe deposit",
        "grade": {"bright": 0.98, "contrast": 1.22, "sat": 1.18}, # HIGH_STAKES_ARENA
    },
    {
        "filename": "bg_08_depeg_market_crash.jpg",
        "query": "financial market crash red graph stocks trading screen monitor",
        "grade": {"bright": 0.82, "contrast": 1.28, "sat": 1.15}, # FORENSIC_NOIR
    },
    {
        "filename": "bg_09_cyber_vault_siphon_base.jpg",
        "query": "dark server room cybersecurity data center neon blue red wires",
        "grade": {"bright": 0.78, "contrast": 1.30, "sat": 1.20}, # FORENSIC_NOIR
    },
    {
        "filename": "bg_10_global_trade_freeze.jpg",
        "query": "shipping cargo container terminal port night cranes industrial",
        "grade": {"bright": 0.75, "contrast": 1.25, "sat": 1.05}, # FORENSIC_NOIR
    },
    {
        "filename": "bg_11_manila_docket_desk_base.jpg",
        "query": "vintage wooden desk lamp dark detective case files documents",
        "grade": {"bright": 0.85, "contrast": 1.25, "sat": 1.10}, # FORENSIC_NOIR
    },
    {
        "filename": "bg_12_wall_street_shadow_corridor.jpg",
        "query": "dark moody corporate hallway executive office dusk dramatic",
        "grade": {"bright": 0.75, "contrast": 1.25, "sat": 1.05}, # FORENSIC_NOIR
    },
]

FG_SPECS = [
    {
        "filename": "fg_01_treasury_eagle.png",
        "query": "bronze eagle statue monument architecture sculpture",
    },
    {
        "filename": "fg_02_bloomberg_terminals.png",
        "query": "computer monitor financial charts stock market display",
    },
    {
        "filename": "fg_05_devasini_portrait.png",
        "query": "senior italian executive businessman dark tailored suit portrait confident",
    },
    {
        "filename": "fg_07_gold_and_tbills.png",
        "query": "gold bars bullion stack luxury closeup",
    },
]

def fetch_image_from_pexels(query):
    url = f"https://api.pexels.com/v1/search?query={requests.utils.quote(query)}&per_page=5"
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        raise RuntimeError(f"Pexels search failed ({r.status_code}) for '{query}'")
    photos = r.json().get("photos", [])
    if not photos:
        # Fallback to single word query
        first_word = query.split()[0]
        r = requests.get(f"https://api.pexels.com/v1/search?query={first_word}&per_page=5", headers=HEADERS, timeout=15)
        photos = r.json().get("photos", [])
    
    # Pick photo with highest resolution
    best_url = None
    max_res = 0
    for p in photos:
        w = p.get("width", 0)
        h = p.get("height", 0)
        if w * h > max_res:
            max_res = w * h
            best_url = p.get("src", {}).get("original") or p.get("src", {}).get("large2x")
    
    if not best_url and photos:
        best_url = photos[0].get("src", {}).get("large2x")
    
    img_resp = requests.get(best_url, timeout=30)
    img_resp.raise_for_status()
    import io
    return Image.open(io.BytesIO(img_resp.content)).convert("RGB")

def center_crop_16x9(im, target_w=1920, target_h=1080):
    w, h = im.size
    target_ratio = target_w / target_h
    current_ratio = w / h
    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        im = im.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        im = im.crop((0, top, w, top + new_h))
    return im.resize((target_w, target_h), Image.Resampling.LANCZOS)

def grade_image(im, grade):
    if "bright" in grade:
        im = ImageEnhance.Brightness(im).enhance(grade["bright"])
    if "contrast" in grade:
        im = ImageEnhance.Contrast(im).enhance(grade["contrast"])
    if "sat" in grade:
        im = ImageEnhance.Color(im).enhance(grade["sat"])
    return im

def run_u2net(img, session, input_name):
    orig_w, orig_h = img.size
    resized = img.resize((320, 320), Image.Resampling.BILINEAR)
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    arr = (np.array(resized).astype(np.float32) / 255.0 - mean) / std
    inp = np.expand_dims(np.transpose(arr, (2, 0, 1)), 0).astype(np.float32)
    outputs = session.run(None, {input_name: inp})
    mask = outputs[0][0, 0]
    mask = (mask - np.min(mask)) / (np.max(mask) - np.min(mask) + 1e-8)
    mask = (mask * 255).astype(np.uint8)
    mask_img = Image.fromarray(mask, mode="L").resize((orig_w, orig_h), Image.Resampling.BILINEAR)
    mask_arr = np.array(mask_img)
    # clean threshold
    mask_arr = np.where(mask_arr < 40, 0, mask_arr)
    # Smooth edges
    mask_arr = np.where(mask_arr > 210, 255, mask_arr)
    return Image.fromarray(mask_arr, mode="L")

def main():
    print("=== STEP 2: GENERATING TETHER CH01 ASSETS ===")
    
    # 1. Process Backgrounds
    for spec in BG_SPECS:
        dst = os.path.join(OUTPUT_DIR, spec["filename"])
        print(f"Fetching {spec['filename']} (query: {spec['query']})...")
        raw_img = fetch_image_from_pexels(spec["query"])
        cropped = center_crop_16x9(raw_img)
        graded = grade_image(cropped, spec["grade"])
        graded.save(dst, quality=95)
        lum = np.mean(np.array(graded.convert("L")))
        print(f" -> Saved {dst} (mean lum: {lum:.1f})")

    # 2. Process Foregrounds with U2Net
    print("\nLoading U2Net neural model for foreground cutouts...")
    session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name

    for spec in FG_SPECS:
        dst = os.path.join(OUTPUT_DIR, spec["filename"])
        print(f"Fetching FG {spec['filename']} (query: {spec['query']})...")
        raw_img = fetch_image_from_pexels(spec["query"])
        # Fit inside 1080p frame cleanly
        w, h = raw_img.size
        scale = 1080 / h
        scaled = raw_img.resize((int(w * scale), 1080), Image.Resampling.LANCZOS)
        
        mask = run_u2net(scaled, session, input_name)
        rgba = scaled.convert("RGBA")
        rgba.putalpha(mask)
        
        # Verify transparency ratio
        alpha_arr = np.array(mask)
        transparent_ratio = float(np.mean(alpha_arr < 30))
        print(f" -> Transparency ratio: {transparent_ratio:.2f}")
        assert 0.10 <= transparent_ratio <= 0.90, f"Cutout {spec['filename']} invalid transparency {transparent_ratio}"
        
        rgba.save(dst)
        print(f" -> Saved {dst}")

    print("\n[SUCCESS] All 16 Tether Chapter 1 assets generated and verified!")

if __name__ == "__main__":
    main()
