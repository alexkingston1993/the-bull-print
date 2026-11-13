#!/usr/bin/env python3
"""
THE LUNA EXTINCTION: 3-Cut Dynamic Micro-Motion Edition
Channel: The Bull Print (@thebullprint)

Eliminates static holds by executing 3 cinematic camera angle cuts per segment
from the single 2K master plate:
- Shot 1 (Wide Establishing): 1.0x -> 1.08x subtle push
- Shot 2 (Forensic Close-up Punch-in): Hard cut to 1.32x - 1.36x tight crop with slow drift
- Shot 3 (Re-frame / Pull-back): Hard cut to 1.15x -> 1.0x pull-back pan
Composites with Christopher Neural VO and 5-act modular cinematic score.
"""

import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRAMES_DIR = BASE_DIR / "output" / "luna_death_spiral_documentary" / "frames"
AUDIO_DIR = BASE_DIR / "output" / "luna_death_spiral_documentary" / "audio"
BGM_DIR = BASE_DIR / "assets" / "audio" / "bgm_pool"
WORK_DIR = BASE_DIR / "output" / "luna_death_spiral_documentary" / "rendered_dynamic_segments"
FINAL_OUT = BASE_DIR / "output" / "luna_death_spiral_documentary" / "the_luna_extinction_dynamic_cuts_12min_master.mp4"

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

def render_dynamic_segment(seg_num: int) -> Path:
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

    # Divide target_dur into 3 cinematic cuts
    dur1 = round(target_dur * 0.30, 2)
    dur2 = round(target_dur * 0.38, 2)
    dur3 = round(target_dur - dur1 - dur2, 2)

    frames1 = int(dur1 * 30)
    frames2 = int(dur2 * 30)
    frames3 = int(dur3 * 30)

    # Alternating punch-in focal points across segments
    if seg_num % 2 == 1:
        # Punch in center-left
        vf2_pos = "x='iw/3-(iw/zoom/3)':y='ih/2-(ih/zoom/2)'"
    else:
        # Punch in center-right
        vf2_pos = "x='(2*iw/3)-(2*iw/zoom/3)':y='ih/2-(ih/zoom/2)'"

    vf1 = f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,zoompan=z='min(zoom+0.0004,1.08)':d={frames1}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30,format=yuv420p"
    vf2 = f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,zoompan=z='1.34':d={frames2}:{vf2_pos}:s=1920x1080:fps=30,format=yuv420p"
    vf3 = f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,zoompan=z='max(1.14-0.0004,1.0)':d={frames3}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30,format=yuv420p"

    s1 = WORK_DIR / f"temp_{seg_num:02d}_s1.mp4"
    s2 = WORK_DIR / f"temp_{seg_num:02d}_s2.mp4"
    s3 = WORK_DIR / f"temp_{seg_num:02d}_s3.mp4"
    clist = WORK_DIR / f"temp_{seg_num:02d}_list.txt"

    # Fast multi-shot generation
    subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i", str(frame_path), "-vf", vf1, "-t", str(dur1), "-c:v", "libx264", "-preset", "ultrafast", str(s1)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i", str(frame_path), "-vf", vf2, "-t", str(dur2), "-c:v", "libx264", "-preset", "ultrafast", str(s2)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i", str(frame_path), "-vf", vf3, "-t", str(dur3), "-c:v", "libx264", "-preset", "ultrafast", str(s3)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    clist.write_text(f"file '{s1.resolve()}'\nfile '{s2.resolve()}'\nfile '{s3.resolve()}'\n")

    bgm_offset = ((seg_num - 1) % 7) * 19.5
    af = (
        f"[1:a]adelay=300|300,apad=pad_dur={target_dur}[vo_d];"
        f"[2:a]atrim=start={bgm_offset}:end={bgm_offset + target_dur},asetpts=PTS-STARTPTS,volume=0.12[bgm_d];"
        f"[vo_d][bgm_d]amix=inputs=2:duration=first[aout]"
    )

    cmd = [
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
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Cleanup temp cuts
    s1.unlink(missing_ok=True)
    s2.unlink(missing_ok=True)
    s3.unlink(missing_ok=True)
    clist.unlink(missing_ok=True)

    print(f"[{seg_num:02d}/36] 🎬 Rendered 3-Cut Dynamic Segment {out_mp4.name} (dur={target_dur}s, cuts: {dur1}s | {dur2}s | {dur3}s)")
    sys.stdout.flush()
    return out_mp4

def concatenate_master(seg_paths: list, out_path: Path):
    concat_list = WORK_DIR / "master_dynamic_concat_list.txt"
    with open(concat_list, "w") as f:
        for p in seg_paths:
            f.write(f"file '{p.resolve()}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(out_path)
    ]

    print("\nConcatenating all 36 segments into 3-Cut Dynamic Master Documentary...")
    sys.stdout.flush()
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg concat error: {res.stderr.decode()[-400:]}")

    dur = get_audio_duration(out_path)
    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"🎉 3-CUT DYNAMIC MASTER ASSEMBLED: {out_path.name}")
    print(f"   Duration: {int(dur // 60)}m {int(dur % 60)}s ({dur}s)")
    print(f"   Size: {size_mb:.2f} MB")
    print(f"   Total Cinematic Camera Angle Cuts: 108 Cuts (3 cuts per segment x 36 segments)")
    sys.stdout.flush()

def main():
    print("=" * 75)
    print("🎬 RENDERING: THE LUNA EXTINCTION (3-CUT DYNAMIC MICRO-MOTION EDITION)")
    print("=" * 75)
    sys.stdout.flush()

    rendered = []
    for i in range(1, 37):
        mp4 = render_dynamic_segment(i)
        rendered.append(mp4)

    concatenate_master(rendered, FINAL_OUT)
    print("\n✅ 3-CUT DYNAMIC MASTER COMPLETE: Ready for side-by-side review & swap!")

if __name__ == "__main__":
    main()
