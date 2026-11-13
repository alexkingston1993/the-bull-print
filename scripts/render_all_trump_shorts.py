#!/usr/bin/env python3
"""
Render Engine for 10 Trump Election YouTube Shorts (9:16 Vertical 1080x1920)
Composites 6 bespoke 9:16 frames switching every ~6s, Christopher voiceover, and ducked cinematic BGM.
"""

import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TRUMP_DIR = BASE_DIR / "output" / "trump_shorts"
FRAMES_BASE = TRUMP_DIR / "frames"
AUDIO_DIR = TRUMP_DIR / "audio"
BGM_POOL = BASE_DIR / "assets" / "audio" / "bgm_pool"
RENDER_DIR = TRUMP_DIR / "rendered"
WORK_DIR = TRUMP_DIR / "work"

RENDER_DIR.mkdir(parents=True, exist_ok=True)
WORK_DIR.mkdir(parents=True, exist_ok=True)

BGM_TRACKS = [
    BGM_POOL / "bed_01_subterranean_pulse.wav",
    BGM_POOL / "bed_02_quant_clockwork.wav",
    BGM_POOL / "bed_05_wall_street_afterhours.wav",
    BGM_POOL / "bed_06_systemic_collapse.wav",
    BGM_POOL / "bed_04_cyber_forensic.wav",
]

def get_audio_duration(path: Path) -> float:
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    out = subprocess.check_output(cmd).decode().strip()
    return float(out)

def render_single_short(short_id: int) -> Path:
    s_str = f"short_{short_id:02d}"
    frames_dir = FRAMES_BASE / s_str
    vo_path = AUDIO_DIR / f"vo_short_{short_id:02d}.mp3"
    out_final = RENDER_DIR / f"trump_short_{short_id:02d}.mp4"
    bgm_path = BGM_TRACKS[(short_id - 1) % len(BGM_TRACKS)]

    if not vo_path.exists():
        raise FileNotFoundError(f"Missing VO track: {vo_path}")

    vo_dur = get_audio_duration(vo_path)
    total_dur = round(vo_dur + 0.6, 2)
    seg_dur = round(total_dur / 6.0, 3)

    print(f"\n[{short_id:02d}/10] Rendering {s_str} (Duration: {total_dur}s, ~{seg_dur}s/frame)...")

    seg_files = []
    short_work = WORK_DIR / s_str
    short_work.mkdir(parents=True, exist_ok=True)

    for i in range(1, 7):
        frame_file = frames_dir / f"seg_{i:02d}.jpg"
        if not frame_file.exists():
            raise FileNotFoundError(f"Missing frame {frame_file}")

        seg_out = short_work / f"part_{i:02d}.mp4"
        total_frames = int(seg_dur * 30)

        # Alternating subtle vertical zoompan in 9:16
        if i % 2 == 1:
            zoom_expr = "min(zoom+0.00008,1.04)"
        else:
            zoom_expr = "max(1.04-0.00008,1.0)"

        vf = (
            f"scale=1080:1920:force_original_aspect_ratio=decrease,"
            f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2,"
            f"zoompan=z='{zoom_expr}':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,"
            f"format=yuv420p"
        )

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(frame_file),
            "-filter_complex", f"[0:v]{vf}[vout]",
            "-map", "[vout]",
            "-t", str(seg_dur),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            str(seg_out)
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg frame render failed: {res.stderr.decode()[-300:]}")
        seg_files.append(seg_out)

    # Concat the 6 video parts
    concat_list = short_work / "concat.txt"
    with open(concat_list, "w") as f:
        for sf in seg_files:
            f.write(f"file '{sf.resolve()}'\n")

    video_concat_raw = short_work / "video_raw.mp4"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(video_concat_raw)
    ]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Mix audio (VO + Ducked BGM) and combine with video
    af = (
        f"[1:a]adelay=200|200,apad=pad_dur={total_dur}[vo];"
        f"[2:a]atrim=start=0:end={total_dur},asetpts=PTS-STARTPTS,volume=0.12[bgm];"
        f"[vo][bgm]amix=inputs=2:duration=first[aout]"
    )

    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(video_concat_raw),
        "-i", str(vo_path),
        "-stream_loop", "-1", "-i", str(bgm_path),
        "-filter_complex", af,
        "-map", "0:v", "-map", "[aout]",
        "-t", str(total_dur),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        str(out_final)
    ]
    res_final = subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res_final.returncode != 0:
        raise RuntimeError(f"Final mix error: {res_final.stderr.decode()[-300:]}")

    print(f"✅ Rendered Short {short_id:02d}: {out_final.name} ({round(out_final.stat().st_size / 1024 / 1024, 2)} MB, {total_dur}s)")
    return out_final

def main():
    print("=" * 70)
    print("🚀 RENDERING ALL 10 TRUMP ELECTION SHORTS (9:16 VERTICAL)")
    print("=" * 70)
    for i in range(1, 11):
        render_single_short(i)
    print("\n🎉 ALL 10 TRUMP ELECTION SHORTS SUCCESSFULLY RENDERED!")

if __name__ == "__main__":
    main()
