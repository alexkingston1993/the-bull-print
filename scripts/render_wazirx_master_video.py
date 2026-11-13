#!/usr/bin/env python3
"""
THE ₹2,000 CRORE VAULT HEIST: The Inside Investigation of WazirX & India's Missing Crypto
12-Minute Master Video Rendering Engine
Composites 36 2K frames, 36 Christopher voiceover tracks, and cinematic BGM suites with sidechain ducking.
"""

import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRAMES_DIR = BASE_DIR / "output" / "wazirx_heist_documentary" / "frames"
AUDIO_DIR = BASE_DIR / "output" / "wazirx_heist_documentary" / "audio"
BGM_DIR = BASE_DIR / "assets" / "audio" / "bgm_pool"
WORK_DIR = BASE_DIR / "output" / "wazirx_heist_documentary" / "rendered_segments"
FINAL_OUT = BASE_DIR / "output" / "wazirx_heist_documentary" / "the_2000cr_wazirx_heist_12min_master.mp4"

WORK_DIR.mkdir(parents=True, exist_ok=True)

# 5 Acts / Chapter BGM assignments
CHAPTER_BGM = {
    range(1, 8): BGM_DIR / "bed_03_offshore_noir.wav",
    range(8, 15): BGM_DIR / "bed_02_quant_clockwork.wav",
    range(15, 22): BGM_DIR / "bed_06_systemic_collapse.wav",
    range(22, 29): BGM_DIR / "bed_01_subterranean_pulse.wav",
    range(29, 37): BGM_DIR / "bed_04_cyber_forensic.wav",
}

def get_bgm(seg_num: int) -> Path:
    for r, p in CHAPTER_BGM.items():
        if seg_num in r:
            return p
    return BGM_DIR / "bed_03_offshore_noir.wav"

def get_audio_duration(path: Path) -> float:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    out = subprocess.check_output(cmd).decode().strip()
    return float(out)

def render_segment(seg_num: int) -> Path:
    out_mp4 = WORK_DIR / f"segment_{seg_num:02d}.mp4"
    frame_path = FRAMES_DIR / f"segment_{seg_num:02d}.jpg"
    vo_path = AUDIO_DIR / f"vo_segment_{seg_num:02d}.mp3"
    bgm_path = get_bgm(seg_num)

    if not frame_path.exists():
        raise FileNotFoundError(f"Missing frame {frame_path}")
    if not vo_path.exists():
        raise FileNotFoundError(f"Missing VO audio {vo_path}")

    vo_dur = get_audio_duration(vo_path)
    target_dur = max(20.0, round(vo_dur + 0.8, 1))
    total_frames = int(target_dur * 30)

    # Alternating Ken Burns: slow zoom in or slow zoom out
    if seg_num % 2 == 1:
        zoom_expr = "min(zoom+0.00008,1.04)"
    else:
        zoom_expr = "max(1.04-0.00008,1.0)"

    vf = (
        f"scale=1920:1080:force_original_aspect_ratio=decrease,"
        f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,"
        f"zoompan=z='{zoom_expr}':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30,"
        f"format=yuv420p"
    )

    bgm_offset = ((seg_num - 1) % 7) * 19.5
    af = (
        f"[1:a]adelay=300|300,apad=pad_dur={target_dur}[vo];"
        f"[2:a]atrim=start={bgm_offset}:end={bgm_offset + target_dur},asetpts=PTS-STARTPTS,volume=0.12[bgm];"
        f"[vo][bgm]amix=inputs=2:duration=first[aout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(frame_path),
        "-i", str(vo_path),
        "-stream_loop", "-1", "-i", str(bgm_path),
        "-filter_complex", f"[0:v]{vf}[vout];{af}",
        "-map", "[vout]", "-map", "[aout]",
        "-t", str(target_dur),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        str(out_mp4)
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg error on segment {seg_num}: {res.stderr.decode()[-400:]}")

    print(f"[{seg_num:02d}/36] Rendered {out_mp4.name} (dur={target_dur}s, size={out_mp4.stat().st_size // 1024} KB)")
    return out_mp4

def concatenate_master(seg_paths: list, out_path: Path):
    concat_list = WORK_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        for p in seg_paths:
            f.write(f"file '{p.resolve()}'\n")

    print(f"\nConcatenating {len(seg_paths)} segments into {out_path.name}...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(out_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg concat failed: {res.stderr.decode()[-400:]}")
    print(f"Master Video Successfully Assembled: {out_path} ({out_path.stat().st_size // (1024*1024)} MB)")

def main():
    print("=" * 70)
    print("STARTING WAZIRX 12-MINUTE MASTER VIDEO RENDERING PIPELINE")
    print("=" * 70)
    rendered = []
    for i in range(1, 37):
        p = render_segment(i)
        rendered.append(p)

    concatenate_master(rendered, FINAL_OUT)
    print("\nALL 36 SEGMENTS RENDERED AND WAZIRX MASTER VIDEO IS READY!")

if __name__ == "__main__":
    main()
