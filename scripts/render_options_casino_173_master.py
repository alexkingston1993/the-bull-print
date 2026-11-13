#!/usr/bin/env python3
"""
THE ZERO-DAY OPTIONS CASINO: Pure 173-Frame Cinematic Masterclass
Channel: The Bull Print (@thebullprint)

Features:
- Pure, clean hard cuts across 173 bespoke 2K frames (~4.0s per cut)
- ZERO artificial digital zooms, ZERO fake pans, ZERO cropping distortion
- ChristopherNeural master narration with balanced 5-act modular score
- Full 1080p Full HD broadcast-grade assembly
"""

import json
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRAMES_DIR = BASE_DIR / "output" / "options_casino_documentary" / "frames"
AUDIO_DIR = BASE_DIR / "output" / "options_casino_documentary" / "audio"
BGM_DIR = BASE_DIR / "assets" / "audio" / "bgm_pool"
WORK_DIR = BASE_DIR / "output" / "options_casino_documentary" / "rendered_173_segments"
FINAL_OUT = BASE_DIR / "output" / "options_casino_documentary" / "the_zero_day_options_casino_12min_master.mp4"
MAPPING_FILE = BASE_DIR / "output" / "options_casino_documentary" / "segment_frame_mapping.json"

WORK_DIR.mkdir(parents=True, exist_ok=True)

# 5 Acts / Chapter BGM assignments
CHAPTER_BGM = {
    range(1, 8): BGM_DIR / "bed_01_subterranean_pulse.wav",
    range(8, 15): BGM_DIR / "bed_02_quant_clockwork.wav",
    range(15, 22): BGM_DIR / "bed_06_systemic_collapse.wav",
    range(22, 29): BGM_DIR / "bed_03_offshore_noir.wav",
    range(29, 37): BGM_DIR / "bed_04_cyber_forensic.wav",
}

def get_bgm(seg_num: int) -> Path:
    for r, p in CHAPTER_BGM.items():
        if seg_num in r:
            return p
    return BGM_DIR / "bed_01_subterranean_pulse.wav"

def get_audio_duration(path: Path) -> float:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    out = subprocess.check_output(cmd).decode().strip()
    return float(out)

def render_segment(seg_num: int, frame_files: list, total_segments: int):
    out_mp4 = WORK_DIR / f"segment_{seg_num:02d}.mp4"
    if out_mp4.exists() and out_mp4.stat().st_size > 100000:
        print(f"[{seg_num:02d}/{total_segments}] ⏩ Segment {seg_num:02d} already rendered, skipping.")
        return out_mp4

    vo_path = AUDIO_DIR / f"vo_segment_{seg_num:02d}.mp3"
    bgm_path = get_bgm(seg_num)

    if not vo_path.exists():
        raise FileNotFoundError(f"Missing VO audio {vo_path}")

    vo_dur = get_audio_duration(vo_path)
    target_dur = max(20.0, round(vo_dur + 0.6, 1))

    # Cap at 5 frames per segment for ~4.0s pacing
    selected_frames = frame_files[:5]
    n_frames = len(selected_frames)
    cut_dur = round(target_dur / n_frames, 2)

    sub_cuts = []
    clist = WORK_DIR / f"temp_{seg_num:02d}_list.txt"
    clist_lines = []

    # Pure, clean scaling: NO zoompan, NO distortion
    vf_clean = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,format=yuv420p"

    for idx, f_name in enumerate(selected_frames):
        f_path = FRAMES_DIR / f_name
        sub_mp4 = WORK_DIR / f"temp_{seg_num:02d}_cut_{idx:02d}.mp4"
        
        # Last cut absorbs any rounding difference
        this_dur = cut_dur if idx < n_frames - 1 else round(target_dur - (cut_dur * (n_frames - 1)), 2)
        
        cmd_img = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(f_path),
            "-vf", vf_clean,
            "-t", str(this_dur),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
            "-pix_fmt", "yuv420p",
            str(sub_mp4)
        ]
        subprocess.run(cmd_img, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sub_cuts.append(sub_mp4)
        clist_lines.append(f"file '{sub_mp4.resolve()}'\n")

    clist.write_text("".join(clist_lines))

    # Clean audio mix: VO natural + 10% BGM bed
    bgm_offset = ((seg_num - 1) % 7) * 19.5
    af = (
        f"[1:a]apad=pad_dur={target_dur}[vo_d];"
        f"[2:a]atrim=start={bgm_offset}:end={bgm_offset + target_dur},asetpts=PTS-STARTPTS,volume=0.10[bgm_d];"
        f"[vo_d][bgm_d]amix=inputs=2:duration=first[aout]"
    )

    cmd_mux = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(clist),
        "-i", str(vo_path),
        "-stream_loop", "-1", "-i", str(bgm_path),
        "-filter_complex", af,
        "-map", "0:v", "-map", "[aout]",
        "-t", str(target_dur),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        str(out_mp4)
    ]
    subprocess.run(cmd_mux, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Cleanup temp sub-cuts
    for s in sub_cuts:
        s.unlink(missing_ok=True)
    clist.unlink(missing_ok=True)

    print(f"[{seg_num:02d}/{total_segments}] 🎬 Rendered Clean Segment {seg_num:02d}.mp4 (dur={target_dur}s, {n_frames} clean cuts @ ~{cut_dur}s)")
    return out_mp4

def main():
    if not MAPPING_FILE.exists():
        print(f"❌ Error: Mapping file not found at {MAPPING_FILE}")
        sys.exit(1)

    mapping = json.loads(MAPPING_FILE.read_text())
    total_segments = len(mapping)

    print("=" * 75)
    print("🎬 RENDERING: THE ZERO-DAY OPTIONS CASINO (PURE 173-FRAME MASTER)")
    print(f"   Architecture: Clean Hard Cuts (~4.0s per frame, ZERO digital zooms)")
    print(f"   Total Segments: {total_segments} | Resolution: 1080p Full HD")
    print("=" * 75)

    rendered_segments = []
    for sid_str, frames in mapping.items():
        sid = int(sid_str)
        seg_mp4 = render_segment(sid, frames, total_segments)
        rendered_segments.append(seg_mp4)

    print("\nConcatenating all 36 segments into Pure Master Documentary...")
    master_list = WORK_DIR / "final_concat_list.txt"
    with open(master_list, "w") as f:
        for seg in rendered_segments:
            f.write(f"file '{seg.resolve()}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(master_list),
        "-c", "copy",
        str(FINAL_OUT)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    dur = get_audio_duration(FINAL_OUT)
    size_mb = round(FINAL_OUT.stat().st_size / 1024 / 1024, 2)

    print(f"🎉 PURE 173-FRAME MASTER ASSEMBLED: {FINAL_OUT.name}")
    print(f"   Duration: {int(dur//60)}m {int(dur%60)}s ({dur}s)")
    print(f"   Size: {size_mb} MB")
    print(f"   Visual Standard: 100% Clean Cuts, Zero Digital Distortion")
    print("\n✅ ZERO-DAY OPTIONS CASINO MASTER COMPLETE!")

if __name__ == "__main__":
    main()
