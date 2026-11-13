#!/usr/bin/env python3
"""
THE ZERO-DAY OPTIONS CASINO: Complete 12-Minute Animated Captioned Masterclass
Channel: The Bull Print (@thebullprint)

Features:
- Pure clean hard cuts across all 173 bespoke 2K frames (~4.1s per cut)
- Exact word-level timestamped animated captions on every spoken word
- Active words highlighted dynamically in Electric Gold / Flame Crimson
- Floating lower-third frosted pill badge (preserving top 85% artwork)
- ChristopherNeural voiceover + 5-act modular score ducked at 10%
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
FRAMES_DIR = BASE_DIR / "output" / "options_casino_documentary" / "frames"
AUDIO_DIR = BASE_DIR / "output" / "options_casino_documentary" / "audio"
BGM_DIR = BASE_DIR / "assets" / "audio" / "bgm_pool"
WORK_DIR = BASE_DIR / "output" / "options_casino_documentary" / "rendered_captioned_segments"
FINAL_OUT = BASE_DIR / "output" / "options_casino_documentary" / "the_zero_day_options_casino_captioned_12min_master.mp4"
MAPPING_FILE = BASE_DIR / "output" / "options_casino_documentary" / "segment_frame_mapping.json"
TIMINGS_FILE = BASE_DIR / "output" / "options_casino_documentary" / "all_36_word_timings.json"

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

def render_captioned_segment(seg_num: int, frame_files: list, seg_chunks: list, total_segments: int):
    out_mp4 = WORK_DIR / f"segment_{seg_num:02d}_captioned.mp4"
    if out_mp4.exists() and out_mp4.stat().st_size > 500000:
        print(f"[{seg_num:02d}/{total_segments}] ⏩ Segment {seg_num:02d} already rendered, skipping.")
        return out_mp4

    vo_path = AUDIO_DIR / f"vo_segment_{seg_num:02d}.mp3"
    bgm_path = get_bgm(seg_num)

    vo_dur = get_audio_duration(vo_path)
    target_dur = max(20.0, round(vo_dur + 0.6, 1))

    # Preload and scale frames to full-bleed edge-to-edge (ZERO black bars / voids)
    selected_frames = frame_files[:5]
    n_frames = len(selected_frames)
    cut_dur = target_dur / n_frames

    loaded_images = []
    width, height = 1920, 1080
    for fname in selected_frames:
        fpath = FRAMES_DIR / fname
        im = Image.open(fpath).convert("RGB")
        # Full-bleed cover scale & center crop: ZERO black borders, fills 100% of 1920x1080
        scale = max(width / im.width, height / im.height)
        new_w = round(im.width * scale)
        new_h = round(im.height * scale)
        resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - width) // 2
        top = (new_h - height) // 2
        full_bleed = resized.crop((left, top, left + width, top + height))
        loaded_images.append(full_bleed)

    font_path = "/System/Library/Fonts/Supplemental/Impact.ttf"
    font = ImageFont.truetype(font_path, 54)
    font_active = ImageFont.truetype(font_path, 58)

    fps = 25
    total_frames = int(target_dur * fps)
    temp_video = WORK_DIR / f"temp_{seg_num:02d}_video.mp4"

    cmd_v = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{width}x{height}",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(temp_video)
    ]
    proc_v = subprocess.Popen(cmd_v, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for f_idx in range(total_frames):
        cur_sec = f_idx / fps
        # Determine background image
        img_idx = min(int(cur_sec / cut_dur), n_frames - 1)
        bg = loaded_images[img_idx].copy()

        # Find active caption chunk
        active_chunk = None
        for chunk in seg_chunks:
            if chunk["chunk_start"] <= cur_sec <= chunk["chunk_end"] + 0.12:
                active_chunk = chunk
                break

        if active_chunk:
            overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)

            words_info = []
            total_phrase_w = 0
            space_w = draw.textlength(" ", font=font)

            for w_meta in active_chunk["words"]:
                w_str = w_meta["word"]
                is_active = w_meta["start"] <= cur_sec <= w_meta["end"]
                f_use = font_active if is_active else font
                w_len = draw.textlength(w_str, font=f_use)
                words_info.append((w_meta, w_str, is_active, f_use, w_len))
                total_phrase_w += w_len + space_w
            total_phrase_w -= space_w

            # Position inside lower third of frame (same as 30s sample)
            box_h = 86
            pad_x = 36
            box_w = total_phrase_w + (pad_x * 2)
            box_x = (width - box_w) // 2
            box_y = 910

            draw.rounded_rectangle(
                [box_x, box_y, box_x + box_w, box_y + box_h],
                radius=24,
                fill=(8, 10, 14, 215),
                outline=(255, 255, 255, 45),
                width=2
            )

            cur_x = box_x + pad_x
            text_baseline_y = box_y + 14

            for w_meta, w_str, is_active, f_use, w_len in words_info:
                if is_active:
                    fill_color = (255, 60, 60, 255) if w_meta["is_red"] else (255, 225, 30, 255)
                    draw.text((cur_x + 2, text_baseline_y + 2), w_str, font=f_use, fill=(0, 0, 0, 220))
                    draw.text((cur_x, text_baseline_y), w_str, font=f_use, fill=fill_color)
                else:
                    draw.text((cur_x + 1, text_baseline_y + 1), w_str, font=f_use, fill=(0, 0, 0, 180))
                    draw.text((cur_x, text_baseline_y), w_str, font=f_use, fill=(245, 245, 245, 240))
                cur_x += w_len + space_w

            bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")

        proc_v.stdin.write(bg.tobytes())

    proc_v.stdin.close()
    proc_v.wait()

    # Audio muxing: Christopher Natural VO + 10% BGM bed
    bgm_offset = ((seg_num - 1) % 7) * 19.5
    af = (
        f"[1:a]apad=pad_dur={target_dur}[vo_d];"
        f"[2:a]atrim=start={bgm_offset}:end={bgm_offset + target_dur},asetpts=PTS-STARTPTS,volume=0.10[bgm_d];"
        f"[vo_d][bgm_d]amix=inputs=2:duration=first[aout]"
    )

    cmd_mux = [
        "ffmpeg", "-y",
        "-i", str(temp_video),
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
    temp_video.unlink(missing_ok=True)

    print(f"[{seg_num:02d}/{total_segments}] 🎬 Rendered Captioned Segment {seg_num:02d}.mp4 ({n_frames} clean cuts, {len(seg_chunks)} timed phrases)")
    return out_mp4

def main():
    mapping = json.loads(MAPPING_FILE.read_text())
    timings = json.loads(TIMINGS_FILE.read_text())
    total_segments = len(mapping)

    print("=" * 75)
    print("🎬 RENDERING: THE ZERO-DAY OPTIONS CASINO (ANIMATED CAPTION MASTER)")
    print(f"   Architecture: 173 Clean Cuts + Word-Level Animated Subtitles")
    print(f"   Resolution: 1080p Full HD | Total Segments: {total_segments}")
    print("=" * 75)

    rendered = []
    for sid in range(1, total_segments + 1):
        sid_str = str(sid)
        seg_mp4 = render_captioned_segment(sid, mapping[sid_str], timings[sid_str], total_segments)
        rendered.append(seg_mp4)

    print("\nConcatenating all 36 Captioned Segments into Final Master Documentary...")
    master_list = WORK_DIR / "final_concat_list.txt"
    with open(master_list, "w") as f:
        for seg in rendered:
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

    import shutil
    artifact_path = Path("/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364/the_zero_day_options_casino_captioned_12min_master.mp4")
    shutil.copy(FINAL_OUT, artifact_path)

    print(f"\n🎉 ANIMATED CAPTIONED MASTER COMPLETE: {FINAL_OUT.name}")
    print(f"   Duration: {int(dur//60)}m {int(dur%60)}s ({dur}s)")
    print(f"   Size: {size_mb} MB")
    print(f"   Artifact Copied: {artifact_path.name}")
    print(f"   Visual Standard: 100% Full Bleed Edge-to-Edge Cuts (ZERO Black Borders) + Synchronized Animated Captions")
    print("=" * 75)

if __name__ == "__main__":
    main()
