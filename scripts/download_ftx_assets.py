#!/usr/bin/env python3
"""
scripts/download_ftx_assets.py
Curates and downloads authentic 1080p landscape documentary footage & photos from Pexels
for all 5 chapters of 'The $32 Billion Illusion' FTX documentary.
"""

import os
import requests
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.material import get_api_key

ASSETS_DIR = BASE_DIR / "output" / "ftx_documentary" / "scenes"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Curated high-impact search queries for each scene across 5 chapters
SCENE_QUERIES = {
    # Prologue: The Bahamas Citadel
    "c0_s1": {"query": "luxury penthouse twilight night", "type": "photo"},
    "c0_s2": {"query": "printing press newspaper printing", "type": "photo"},
    "c0_s3": {"query": "capitol hill congress hearing room", "type": "photo"},
    "c0_s4": {"query": "server room dark cybersecurity code", "type": "photo"},

    # Chapter 1: The Infinite Money Glitch
    "c1_s1": {"query": "stock trader computer charts dark office", "type": "photo"},
    "c1_s2": {"query": "cryptocurrency gold coin dark reflection", "type": "photo"},
    "c1_s3": {"query": "computer programming code screen dark", "type": "photo"},
    "c1_s4": {"query": "massive data center blue server lights", "type": "photo"},

    # Chapter 2: The Seduction of Wall Street
    "c2_s1": {"query": "basketball stadium arena night lights", "type": "photo"},
    "c2_s2": {"query": "luxury boardroom skyscraper night", "type": "photo"},
    "c2_s3": {"query": "washington dc government building classical columns", "type": "photo"},
    "c2_s4": {"query": "hollywood film set camera lights", "type": "photo"},

    # Chapter 3: The 72-Hour Bank Run
    "c3_s1": {"query": "financial documents paper confidential report", "type": "photo"},
    "c3_s2": {"query": "smartphone screen dark glowing", "type": "photo"},
    "c3_s3": {"query": "stock market crash red screen panic", "type": "photo"},
    "c3_s4": {"query": "empty courtroom federal judge bench", "type": "photo"},

    # Chapter 4 & Epilogue: The Verdict & Aftermath
    "c4_s1": {"query": "corporate lawyer office paperwork investigation", "type": "photo"},
    "c4_s2": {"query": "police car night emergency lights street", "type": "photo"},
    "c4_s3": {"query": "courtroom gavel justice wood bench", "type": "photo"},
    "c4_s4": {"query": "financial intelligence conference room night skyline", "type": "photo"},
}


def download_asset(scene_key: str, spec: dict):
    dest = ASSETS_DIR / f"{scene_key}.jpg"
    if dest.exists() and dest.stat().st_size > 50000:
        print(f"⏩ {scene_key} already exists.")
        return dest

    api_key = get_api_key("pexels_api_keys")
    headers = {"Authorization": api_key}
    
    url = f"https://api.pexels.com/v1/search?query={requests.utils.quote(spec['query'])}&per_page=5&orientation=landscape"
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            photos = r.json().get("photos", [])
            if photos:
                # Get the highest resolution (original or large2x)
                img_url = photos[0]["src"].get("large2x") or photos[0]["src"].get("original")
                img_r = requests.get(img_url, timeout=30)
                if img_r.status_code == 200:
                    dest.write_bytes(img_r.content)
                    print(f"✅ Downloaded {scene_key} ({spec['query']}) -> {dest.stat().st_size // 1024} KB")
                    return dest
    except Exception as e:
        print(f"⚠️ Error downloading {scene_key}: {e}")
    return None


def main():
    print("🚀 Downloading high-resolution 1080p landscape documentary stills from Pexels...")
    for sk, spec in SCENE_QUERIES.items():
        download_asset(sk, spec)
    print("🔥 All scene assets downloaded!")


if __name__ == "__main__":
    main()
