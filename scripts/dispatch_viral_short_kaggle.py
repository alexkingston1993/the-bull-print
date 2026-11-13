#!/usr/bin/env python3
"""
The Bull Print — Viral Short Dispatcher to Kaggle GPU
Topic: "The ₹65,700 Cr FII Rotation: Why Wall Street Is Dumping Nvidia to Flood Indian Bluechips"
Format: 9:16 Vertical (576x1024)
Cadence: Exactly 1 unique plate every 3.0s (20 frames for 60s)
100% Kaggle GPU (Tesla T4) Execution
"""

import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.kaggle_image_worker import KaggleImageWorker

TOPIC = "The ₹65,700 Cr FII Rotation: Why Wall Street Is Dumping Nvidia to Flood Indian Bluechips"
SLUG = "fii-rotation-nvidia-dump"

FRAMES_CONFIG = [
    (1, "Nvidia $159 Selloff", "Wall Street architectural exchange floor at dusk, dramatic ambient crimson red lighting, floor traders in dark tailored suits in focused intensity, cinematic photorealistic 35mm, moody ambient lighting"),
    (2, "Boardroom Panic", "Silhouettes of corporate executives in glass boardroom overlooking storm clouds, polished obsidian conference table, cool cyan shadows"),
    (3, "The Algo Liquidation", "High frequency server racks in dark server vault, amber and blue status indicator lights pulsating, atmospheric cold haze"),
    (4, "Dalal Street Awakening", "Aerial low-angle shot of Mumbai Bombay Stock Exchange building at golden dawn, sunlight breaking over historic financial district, grand scale"),
    (5, "Foreign Capital Flood", "Abstract conceptual financial art, massive streams of golden molten light flowing across obsidian terrain, high contrast, cinematic depth"),
    (6, "Wall Street Order Book", "Institutional trading desk, multi-screen glass monitors in soft amber bokeh, half-empty espresso cup, dramatic side-lighting"),
    (7, "The Yield Spread Shift", "Abstract glowing geometric scale balancing a titanium microchip against a glowing golden brick, clean minimalist composition"),
    (8, "Emerging Market Suction", "Panoramic skyline of Mumbai Nariman Point waterfront at sunrise, modern corporate high-rises reflecting golden morning rays"),
    (9, "Bluechip Heavyweight Accumulation", "High-end corporate banking headquarters lobby, marble pillars, sharp directional light shafts, deep architectural shadows"),
    (10, "The 8-Month High Breakout", "Wall Street bronze bull statue contrasted against Mumbai financial district architecture, dramatic mist, heroic low angle"),
    (11, "Hedge Fund Liquidity Trap", "Private luxury investment office in Singapore, floor-to-ceiling glass, blurred neon city reflections, contemplative mood"),
    (12, "Semiconductor Cleanroom Reality", "Robotic wafer fabrication arm holding silicon disc under amber cleanroom lighting, sterile industrial tech environment"),
    (13, "Indian Banking Sector Engine", "Sleek modern institutional bank vault door with heavy steel locking bolts, dramatic industrial illumination, obsidian tones"),
    (14, "Retail Chasing the Top", "Suburban living room at dusk, person illuminated by glowing laptop screen analyzing market charts, human emotional tension"),
    (15, "The S&P Concentration Risk", "Monolithic dark architectural tower casting long shadow over financial avenue, volumetric fog, dramatic film noir look"),
    (16, "Currency & Crude Arbitrage", "Ocean oil tanker silhouette cruising through calm deep ocean at twilight, industrial port lights glowing in distance"),
    (17, "Institutional Limit Orders", "Macro close-up shot of polished corporate fountain pen resting on dark leather desk organizer, cinematic shallow focus"),
    (18, "The Mid-Day Volatility Surge", "Dynamic trading room corridor with glass partitions reflecting subtle amber and blue glow, motion blur of passing professionals"),
    (19, "Smart Money Positioning", "Modern conference room with expansive whiteboard showing abstract financial flow diagrams, evening sky outside panoramic windows"),
    (20, "The Bull Print Verdict", "Majestic obsidian stone monolith engraved with clean geometric golden emblem, volumetric rays of light, grand final frame")
]

def build_manifest():
    manifest = []
    for f_id, title, prompt in FRAMES_CONFIG:
        full_prompt = (
            f"Cinematic 35mm photograph, {prompt}, "
            f"vertical 9:16 composition, high aesthetic documentary quality, "
            f"obsidian and golden amber color grade, clean plate, zero text, zero letters, zero watermark, 8k resolution"
        )
        manifest.append({
            "id": f_id,
            "title": title,
            "prompt": full_prompt,
            "aspect_ratio": "9:16",
            "width": 576,
            "height": 1024,
            "cadence_sec": 3.0
        })
    return manifest

if __name__ == "__main__":
    manifest = build_manifest()
    print(f"Generated {len(manifest)} bespoke 9:16 vertical frames for viral Short.")
    manifest_path = BASE_DIR / "output" / "viral_short_fii_rotation_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest written to: {manifest_path}")

    # Dispatch to Kaggle GPU
    print("Dispatching to Kaggle Dual-T4 GPU Runner...")
    worker = KaggleImageWorker()
    success = worker.dispatch(manifest)
    if success:
        print("✓ Viral Short successfully dispatched to Kaggle GPU Runner!")
    else:
        print("❌ Failed to dispatch to Kaggle GPU!")
        sys.exit(1)

