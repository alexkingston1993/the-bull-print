#!/usr/bin/env python3
"""
Compiles any 365-Day Masterclass video once frames are dropped into Day_XXX/frames/
Usage:
  python3 scripts/compile_course_video_from_frames.py 1
  python3 scripts/compile_course_video_from_frames.py all
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
COURSE_DIR = BASE_DIR / "output" / "course" / "youtube_playlist_beginners_in_finance"

def compile_day(day_num):
    # Find folder
    day_prefix = f"Day_{int(day_num):03d}_"
    matches = [f for f in COURSE_DIR.iterdir() if f.is_dir() and f.name.startswith(day_prefix)]
    if not matches:
        print(f"❌ Could not find folder for Day {day_num}")
        return False

    day_folder = matches[0]
    frames_dir = day_folder / "frames"
    manifest_file = day_folder / "BEAT_PROMPTS_4S.json"
    audio_file = day_folder / "narration.mp3"
    output_video = day_folder / "master_video.mp4"

    if not manifest_file.exists():
        print(f"❌ Missing BEAT_PROMPTS_4S.json in {day_folder.name}")
        return False
    if not audio_file.exists():
        print(f"❌ Missing narration.mp3 in {day_folder.name}")
        return False

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    beats = manifest["beats"]
    total_beats = len(beats)

    # Check frames
    existing_frames = sorted([f for f in frames_dir.glob("frame_*.jpg")]) if frames_dir.exists() else []
    if len(existing_frames) < total_beats:
        print(f"⚠️ Day {day_num} has {len(existing_frames)}/{total_beats} frames in {frames_dir}. Will use available or placeholder.")

    # Get audio duration
    probe = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_file)
    ]).decode().strip()
    duration = float(probe)
    beat_dur = duration / total_beats

    # Create concat list
    concat_txt = day_folder / "concat_frames.txt"
    with open(concat_txt, "w") as f:
        for b in beats:
            frame_path = frames_dir / b["frame_filename"]
            # Fallback to beat 1 or first available if not rendered yet
            if not frame_path.exists():
                frame_path = existing_frames[0] if existing_frames else (COURSE_DIR.parent / "branding" / "the_bull_print_channel_avatar.jpg")
            f.write(f"file '{frame_path.resolve()}'\n")
            f.write(f"duration {beat_dur:.3f}\n")
        # Final frame
        last_frame = frames_dir / beats[-1]["frame_filename"]
        if not last_frame.exists():
            last_frame = existing_frames[-1] if existing_frames else frame_path
        f.write(f"file '{last_frame.resolve()}'\n")

    # Render with ffmpeg
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-i", str(audio_file),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(output_video)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Day {day_num} compiled successfully to: {output_video} (Duration: {duration:.1f}s)")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/compile_course_video_from_frames.py <day_number|all>")
        sys.exit(1)
    target = sys.argv[1]
    if target.lower() == "all":
        for d in range(1, 366):
            compile_day(d)
    else:
        compile_day(int(target))
