#!/usr/bin/env python3
"""
scripts/fetch_cinematic_broll.py

Fetches real 1080p moving video B-roll loops from Pexels API for all documentary scenes.
Converts and grades them into:
1. remotion-engine/public/assets/cinematic/scene_{1,2,3,4,6,7}_bg.mp4 (1920x1080 landscape)
2. remotion-engine/public/assets/short/short_scene_{1,2,3,4,6,7}_bg.mp4 (1080x1920 portrait)
"""

import os
import subprocess
import requests

PEXELS_KEY = "2927GljrcuM0PxfFHrBTUfShGAHLL2LcVGbGhuQkxddHHTZ61NzP1sSb"
HEADERS = {"Authorization": PEXELS_KEY}

SCENE_QUERIES = [
    (1, "penthouse", "luxury penthouse night city skyline storm"),
    (2, "trading", "stock market ticker trading floor display"),
    (3, "vault", "bank vault dark money cash gold"),
    (4, "corkboard", "detective investigation corkboard papers office"),
    (6, "server", "server rack lights blinking data center dark"),
    (7, "courtroom", "courtroom gavel law books justice dark")
]

CACHE_DIR = "storage/broll_raw"
CINEMATIC_DIR = "remotion-engine/public/assets/cinematic"
SHORT_DIR = "remotion-engine/public/assets/short"

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(CINEMATIC_DIR, exist_ok=True)
os.makedirs(SHORT_DIR, exist_ok=True)

def search_and_download(query, label):
    raw_path = os.path.join(CACHE_DIR, f"{label}_raw.mp4")
    if os.path.exists(raw_path) and os.path.getsize(raw_path) > 100000:
        print(f"[CACHE HIT] Raw video exists: {raw_path}")
        return raw_path

    url = f"https://api.pexels.com/videos/search?query={requests.utils.quote(query)}&per_page=5"
    r = requests.get(url, headers=HEADERS, timeout=20)
    if r.status_code != 200:
        print(f"[FAIL] Pexels search failed ({r.status_code}) for: {query}")
        return None

    data = r.json()
    videos = data.get("videos", [])
    if not videos:
        print(f"[WARN] No videos found for '{query}', trying fallback...")
        fallback_query = query.split()[0]
        r = requests.get(f"https://api.pexels.com/videos/search?query={fallback_query}&per_page=5", headers=HEADERS)
        videos = r.json().get("videos", [])
        if not videos:
            return None

    best_file = None
    for v in videos:
        for f in v.get("video_files", []):
            w = f.get("width", 0)
            h = f.get("height", 0)
            if w >= 1280 or h >= 1280:
                best_file = f.get("link")
                break
        if best_file:
            break

    if not best_file and videos:
        best_file = videos[0]["video_files"][0]["link"]

    print(f"[DOWNLOADING] {label} from {best_file[:60]}...")
    resp = requests.get(best_file, stream=True, timeout=30)
    with open(raw_path, "wb") as f_out:
        for chunk in resp.iter_content(chunk_size=65536):
            if chunk:
                f_out.write(chunk)

    print(f"[SAVED] {raw_path} ({os.path.getsize(raw_path) / (1024*1024):.2f} MB)")
    return raw_path

def process_loop(raw_path, out_landscape, out_portrait):
    # Process 16:9 Landscape: 1920x1080, loopable 8-second segment, color graded (contrast 1.1, dark tint, blur 2px for midground)
    filter_16_9 = (
        "scale=1920:1080:force_original_aspect_ratio=increase,"
        "crop=1920:1080,"
        "eq=contrast=1.15:brightness=-0.08:saturation=0.9,"
        "gblur=sigma=1.5"
    )
    cmd_16_9 = [
        "ffmpeg", "-y",
        "-ss", "1.0",
        "-t", "8.0",
        "-i", raw_path,
        "-vf", filter_16_9,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-an",
        out_landscape
    ]
    subprocess.run(cmd_16_9, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Process 9:16 Portrait: 1080x1920, loopable 8-second segment
    filter_9_16 = (
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        "eq=contrast=1.15:brightness=-0.08:saturation=0.9,"
        "gblur=sigma=1.5"
    )
    cmd_9_16 = [
        "ffmpeg", "-y",
        "-ss", "1.0",
        "-t", "8.0",
        "-i", raw_path,
        "-vf", filter_9_16,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-an",
        out_portrait
    ]
    subprocess.run(cmd_9_16, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    print("=== FETCHING REAL 1080p MOVING B-ROLL VIDEO LOOPS ===")
    for sc_id, label, query in SCENE_QUERIES:
        print(f"\nProcessing Scene {sc_id} ({label}): query='{query}'")
        raw = search_and_download(query, label)
        if raw and os.path.exists(raw):
            out_land = os.path.join(CINEMATIC_DIR, f"scene_{sc_id}_bg.mp4")
            out_port = os.path.join(SHORT_DIR, f"short_scene_{sc_id}_bg.mp4")
            process_loop(raw, out_land, out_port)
            print(f"  -> Generated: {out_land} ({os.path.getsize(out_land)/(1024*1024):.2f} MB)")
            print(f"  -> Generated: {out_port} ({os.path.getsize(out_port)/(1024*1024):.2f} MB)")
        else:
            print(f"  [ERROR] Failed to obtain video for {label}")

    print("\n✅ All real moving video background loops successfully generated!")

if __name__ == "__main__":
    main()
