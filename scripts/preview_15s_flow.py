#!/usr/bin/env python3
"""
15-Second Side-by-Side Voice Comparison & Visual Broadcast Preview
Voice Shootout: en-US-AndrewMultilingualNeural vs en-US-ChristopherNeural
Features:
- Dynamic sentence-role prosody contours (Hook +2%, Bridge +0%, Climax -6%/-2Hz)
- Punctuation-snapped 180ms J-cuts (. , ... thought boundaries)
- Financial pronunciation normalizer ($1.8B -> 1.8 billion dollars, 16% -> 16 percent, Fed)
- Relaxed silenceremove (0.42s / -50dB) preserving natural comma breaths & sentence periods
- Real Kaggle SDXL plates (frame_00, frame_01, frame_02)
- 3D Kinetic Headline Typography + Top-Left Telemetry HUD
- Safe-Zone 4-Word Active Captions (Electric Gold #FFD700 / Neon Cyan #00F0FF)
- Sidechain Ducking + Sub-Drop Transitions + 35mm Grain/Vignette + -14 LUFS
"""
import os
import sys
import re
import math
import asyncio
import subprocess
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.magnates_visual_studio import precompute_cut_typography
from app.services.local_christopher_tts import normalize_for_tts

OUT_DIR = Path("/tmp/tbp_15s_preview")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Properly punctuated 3-sentence script with natural human cadence
SENTENCES = [
    "Retail investors are chasing a seven trillion dollar tech rally across Wall Street.",
    "Below the surface, however, sovereign bond desks just drained 1.8 billion dollars in overnight liquidity,",
    "exposing a sixteen percent credit fault line... that the Fed can no longer hide."
]

RAW_FULL_SCRIPT = " ".join(SENTENCES)

# Visual beat configurations
BEAT_CONFIGS = [
    {
        "lines": ["$7 TRILLION", "TECH TRAP"],
        "badge": "MARKET ALERT",
        "theme": "warning",
        "chapter": "CH.01 // CAPITAL ROTATION",
        "source": "FED LIQUIDITY DESK // NY-FED.ORG",
    },
    {
        "lines": ["$1.8 BILLION", "DRAIN"],
        "badge": "LIQUIDITY CRUNCH",
        "theme": "cyan",
        "chapter": "CH.02 // SHADOW LIQUIDITY",
        "source": "DTCC SETTLEMENT FLOWS // BLOOMBERG",
    },
    {
        "lines": ["16% CRACK", "FAULT LINE"],
        "badge": "CENTRAL BANKS",
        "theme": "fire",
        "chapter": "CH.03 // CREDIT VOLATILITY",
        "source": "BIS QUARTERLY REVIEW // BASEL III",
    },
]

# 2. Synthesize audio with dynamic prosody contours per voice
async def synthesize_voice_track(voice_id: str, tag: str) -> tuple[Path, list[dict], float, list[float]]:
    """Synthesizes the 3-sentence script with dynamic prosody contours and extracts word timings."""
    import edge_tts
    print(f"\n🎙️ Synthesizing voice track for '{voice_id}' ({tag})...")
    raw_mp3 = OUT_DIR / f"raw_{tag}.mp3"
    clean_wav = OUT_DIR / f"master_{tag}.wav"

    audio_bytes = bytearray()
    words_data = []
    sentence_cut_times = [0.0]
    cumulative_offset_sec = 0.0

    for idx, sent in enumerate(SENTENCES):
        # Dynamic prosody contours per sentence role:
        if idx == 0:
            rate, pitch = "+2%", "+0Hz"      # Authoritative hook
        elif idx == len(SENTENCES) - 1:
            rate, pitch = "-6%", "-2Hz"      # Deliberate climax reveal slowdown
        else:
            rate, pitch = "+0%", "+0Hz"      # Conversational bridge

        norm_sent = normalize_for_tts(sent)
        comm = edge_tts.Communicate(norm_sent, voice=voice_id, rate=rate, pitch=pitch)

        sent_audio = bytearray()
        sent_dur_sec = 0.0

        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                sent_audio.extend(chunk["data"])
            elif chunk["type"] == "SentenceBoundary":
                sent_dur_sec = float(chunk["duration"]) / 10_000_000.0

        if not sent_audio:
            continue

        audio_bytes.extend(sent_audio)

        # Distribute word timings within sentence
        disp_words = [w.strip() for w in re.findall(r"[\w\$%\.\,\-]+", sent) if w.strip()]
        if sent_dur_sec <= 0.1:
            sent_dur_sec = max(0.5, len(disp_words) * 0.38)

        char_counts = [max(1, len(w)) for w in disp_words]
        total_chars = sum(char_counts)
        word_start = cumulative_offset_sec

        for w_i, dw in enumerate(disp_words):
            w_prop = char_counts[w_i] / float(total_chars)
            w_dur = max(0.18, w_prop * sent_dur_sec)
            w_end = round(word_start + w_dur, 3)
            words_data.append({
                "word": dw.upper(),
                "start": round(word_start, 3),
                "end": w_end
            })
            has_break = dw.endswith(",") or dw.endswith("—") or dw.endswith("...")
            word_start = w_end + (0.16 if has_break else 0.02)

        # Natural 0.38s inter-sentence period breath pause
        cumulative_offset_sec = max(cumulative_offset_sec + sent_dur_sec, word_start) + 0.38
        sentence_cut_times.append(round(cumulative_offset_sec, 3))

    with open(raw_mp3, "wb") as f:
        f.write(audio_bytes)

    # Master audio: Relaxed silenceremove preserving natural comma breaths (~0.25s) & periods (~0.38s)
    filter_chain = (
        "silenceremove=start_periods=1:start_silence=0.03:start_threshold=-50dB:"
        "stop_periods=-1:stop_duration=0.42:stop_threshold=-50dB,"
        "highpass=f=70,"
        "equalizer=f=135:width_type=o:width=1.4:g=2.8,"
        "acompressor=threshold=-18dB:ratio=3:attack=5:release=85"
    )
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(raw_mp3),
        "-af", filter_chain,
        "-ar", "44100", "-ac", "2",
        str(clean_wav)
    ], check=True)

    # Probe duration
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(clean_wav)],
        stdout=subprocess.PIPE, text=True, check=True
    )
    final_dur = float(probe.stdout.strip())
    print(f"   ✅ Mastered '{tag}' vocal track: {final_dur:.2f}s ({len(words_data)} words)")
    return clean_wav, words_data, final_dur, sentence_cut_times


def render_broadcast_video(
    tag: str,
    voice_label: str,
    clean_wav: Path,
    words_list: list[dict],
    total_duration: float,
    sentence_cuts: list[float],
    out_mp4: Path,
    plates: list[Image.Image],
    font_file: str
):
    print(f"\n🎬 Rendering visual broadcast MP4 for {voice_label} -> {out_mp4.name}...")
    w_out, h_out = 1080, 1920
    fps = 30
    total_frames = int(math.ceil(total_duration * fps))

    # Precompute 3D Typography
    typo_layers = []
    for bc in BEAT_CONFIGS:
        t = precompute_cut_typography(
            lines=bc["lines"],
            badge_text=bc["badge"],
            max_sheared_w=950,
            color_theme=bc["theme"]
        )
        typo_layers.append(t)

    # Precompute 4-word safe-zone captions (Y = 1305)
    chunk_size = 4
    cached_chunk_pills = {}
    total_words_count = len(words_list)

    for w_global_idx in range(total_words_count):
        chunk_start_idx = (w_global_idx // chunk_size) * chunk_size
        chunk_words_slice = words_list[chunk_start_idx : chunk_start_idx + chunk_size]
        active_in_chunk = w_global_idx - chunk_start_idx
        words_text_list = [item["word"] for item in chunk_words_slice]

        max_allowed_w = 870
        base_size = 48

        while base_size >= 24:
            try:
                f_norm = ImageFont.truetype(font_file, base_size)
                f_act = ImageFont.truetype(font_file, int(base_size * 1.22))
            except Exception:
                f_norm = ImageFont.load_default()
                f_act = f_norm

            wb_list = []
            for i, w_txt in enumerate(words_text_list):
                f_curr = f_act if i == active_in_chunk else f_norm
                bbox = f_curr.getbbox(w_txt)
                bw = bbox[2] - bbox[0]
                bh = bbox[3] - bbox[1]
                wb_list.append((w_txt, bw, bh, f_curr))

            spacing = int(base_size * 0.32)
            row_w = sum(b[1] for b in wb_list) + spacing * max(len(wb_list) - 1, 0)
            if row_w <= max_allowed_w or base_size <= 24:
                break
            base_size -= 2

        pad_x = 24
        pad_y = 14
        max_h = max(b[2] for b in wb_list) if wb_list else 36
        pw = row_w + pad_x * 2
        ph = max_h + pad_y * 2

        pill = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        pdraw = ImageDraw.Draw(pill)

        pdraw.rounded_rectangle(
            [0, 0, pw - 1, ph - 1],
            radius=18,
            fill=(6, 10, 20, 235),
            outline=(20, 241, 149, 210),
            width=2
        )

        cx = pad_x
        for i, (w_txt, bw, bh, f_curr) in enumerate(wb_list):
            y_off = (max_h - bh) // 2
            if i == active_in_chunk:
                is_metric = bool(re.search(r'[\$\%\d]', w_txt))
                act_color = (0, 240, 255, 255) if is_metric else (255, 215, 0, 255)
                pdraw.rounded_rectangle(
                    [cx - 4, pad_y + y_off - 2, cx + bw + 4, pad_y + y_off + bh + 2],
                    radius=6,
                    fill=(0, 0, 0, 180)
                )
                pdraw.text((cx + 2, pad_y + y_off + 2), w_txt, font=f_curr, fill=(0, 0, 0, 255))
                pdraw.text((cx, pad_y + y_off), w_txt, font=f_curr, fill=act_color)
            else:
                pdraw.text((cx + 2, pad_y + y_off + 2), w_txt, font=f_curr, fill=(0, 0, 0, 230))
                pdraw.text((cx, pad_y + y_off), w_txt, font=f_curr, fill=(255, 255, 255, 255))
            cx += bw + spacing

        cached_chunk_pills[w_global_idx] = (pill, pw, ph)

    # Vignettes
    vignette_top = Image.new("RGBA", (w_out, int(h_out * 0.38)), (0, 0, 0, 0))
    d_vt = ImageDraw.Draw(vignette_top)
    for vy in range(vignette_top.height):
        valpha = int(185 * (1.0 - (vy / vignette_top.height) ** 1.3))
        d_vt.line([(0, vy), (w_out, vy)], fill=(5, 8, 15, valpha))

    vignette_bot = Image.new("RGBA", (w_out, int(h_out * 0.28)), (0, 0, 0, 0))
    d_vb = ImageDraw.Draw(vignette_bot)
    for vy in range(vignette_bot.height):
        valpha = int(190 * ((vy / vignette_bot.height) ** 1.2))
        d_vb.line([(0, vy), (w_out, vy)], fill=(5, 8, 15, valpha))

    hud_font_sm = ImageFont.truetype(font_file, 20)
    hud_font_tc = ImageFont.truetype(font_file, 22)

    # Punctuation-Snapped 180ms J-Cut Transition Times
    # Beat 0: 0.0s to (Sentence 1 start - 0.18s)
    # Beat 1: (Sentence 1 start - 0.18s) to (Sentence 2 start - 0.18s)
    # Beat 2: (Sentence 2 start - 0.18s) to total_duration
    j_cut_lead = 0.18
    beat_cuts = [0.0]
    if len(sentence_cuts) >= 3:
        cut1 = max(1.5, sentence_cuts[1] - j_cut_lead)
        cut2 = max(cut1 + 2.0, sentence_cuts[2] - j_cut_lead)
        beat_cuts.extend([cut1, cut2, total_duration])
    else:
        beat_cuts = [0.0, 5.0, 10.0, total_duration]

    print(f"   ✂️ Punctuation-snapped J-cut transitions: Beat 0: 0.0s-{beat_cuts[1]:.2f}s | Beat 1: {beat_cuts[1]:.2f}s-{beat_cuts[2]:.2f}s | Beat 2: {beat_cuts[2]:.2f}s-{beat_cuts[3]:.2f}s")

    raw_video_tmp = OUT_DIR / f"temp_{tag}.mp4"
    documentary_grade_vf = (
        "format=yuv420p,"
        "eq=contrast=1.06:brightness=-0.02:saturation=0.92:gamma=0.96,"
        "vignette=angle=PI/5:mode=forward,"
        "noise=c0s=6:c0f=t+u"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{w_out}x{h_out}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-vf", documentary_grade_vf,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-tune", "grain",
        "-crf", "19",
        "-an",
        str(raw_video_tmp)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    dissolve_frames = 4

    for f_idx in range(total_frames):
        t_sec = f_idx / fps

        # Determine active beat based on punctuation-snapped cuts
        if t_sec < beat_cuts[1]:
            beat_idx = 0
            b_start, b_end = beat_cuts[0], beat_cuts[1]
        elif t_sec < beat_cuts[2]:
            beat_idx = 1
            b_start, b_end = beat_cuts[1], beat_cuts[2]
        else:
            beat_idx = 2
            b_start, b_end = beat_cuts[2], beat_cuts[3]

        bc = BEAT_CONFIGS[beat_idx]
        b_dur = max(1.0, b_end - b_start)
        t_in_beat = max(0.0, t_sec - b_start)

        # Sub-pixel cosine-eased Ken Burns
        p_zoom = 0.5 * (1.0 - math.cos(math.pi * (t_in_beat / b_dur)))
        scale = 1.0 + (0.045 * p_zoom)

        curr_plate = plates[beat_idx]
        zw, zh = int(w_out * scale), int(h_out * scale)
        base_canvas = curr_plate.resize((zw, zh), Image.Resampling.BICUBIC)
        cx, cy = (zw - w_out) // 2, (zh - h_out) // 2
        base_canvas = base_canvas.crop((cx, cy, cx + w_out, cy + h_out))

        # Optical dissolve check at next cut
        if beat_idx < 2:
            time_to_next = beat_cuts[beat_idx + 1] - t_sec
            frames_to_next = int(time_to_next * fps)
            if 0 <= frames_to_next < dissolve_frames:
                blend_alpha = (dissolve_frames - frames_to_next) / float(dissolve_frames)
                next_plate = plates[beat_idx + 1]
                next_scaled = next_plate.resize((int(w_out * 1.005), int(h_out * 1.005)), Image.Resampling.BICUBIC)
                next_cropped = next_scaled.crop((0, 0, w_out, h_out))
                brightened = ImageEnhance.Brightness(base_canvas).enhance(1.04)
                base_canvas = Image.blend(brightened, next_cropped, blend_alpha)

        # Atmospheric grading
        frame_canvas = ImageEnhance.Contrast(base_canvas).enhance(1.12)
        frame_canvas = ImageEnhance.Color(frame_canvas).enhance(1.15)
        frame_canvas.paste(vignette_top, (0, 0), vignette_top)
        frame_canvas.paste(vignette_bot, (0, h_out - vignette_bot.height), vignette_bot)

        # 3D Kinetic Headline Slam Pop-In (1.35x -> 1.0x over first 0.40s)
        slam_dur = 0.40
        if t_in_beat < slam_dur:
            sp = t_in_beat / slam_dur
            scale_slam = 1.0 + (0.35 * (1.0 - math.sin(sp * math.pi / 2.0)))
        else:
            scale_slam = 1.0

        typo = typo_layers[beat_idx]
        tw, th = typo["width"], typo["height"]
        if abs(scale_slam - 1.0) > 0.01:
            cur_w = max(10, int(tw * scale_slam))
            cur_h = max(10, int(th * scale_slam))
            t_img = typo["text_img"].resize((cur_w, cur_h), Image.Resampling.BILINEAR)
            b_img = typo["bloom_img"].resize((cur_w, cur_h), Image.Resampling.BILINEAR)
        else:
            t_img, b_img = typo["text_img"], typo["bloom_img"]
            cur_w, cur_h = tw, th

        paste_x = (w_out - cur_w) // 2
        paste_y = int(h_out * 0.18) - (cur_h // 2)
        frame_canvas.paste(b_img, (paste_x, paste_y), b_img)
        frame_canvas.paste(t_img, (paste_x, paste_y), t_img)

        # Top-Left Telemetry HUD (X=64, Y=124)
        hud_draw = ImageDraw.Draw(frame_canvas)
        hud_x, hud_y = 64, 124

        dot_pulse = 0.5 + 0.5 * math.sin(2 * math.pi * t_sec * 1.5)
        dot_alpha = int(140 + 115 * dot_pulse)
        hud_draw.ellipse([hud_x, hud_y + 4, hud_x + 10, hud_y + 14], fill=(0, 240, 255, dot_alpha))
        hud_draw.text((hud_x + 18, hud_y), f"{bc['chapter']} // {voice_label.upper()}", font=hud_font_sm, fill=(240, 245, 255, 235))

        bar_w = 200
        hud_draw.line([(hud_x, hud_y + 28), (hud_x + bar_w, hud_y + 28)], fill=(40, 48, 65, 180), width=3)
        prog_w = int(bar_w * min(1.0, t_sec / total_duration))
        if prog_w > 0:
            hud_draw.line([(hud_x, hud_y + 28), (hud_x + prog_w, hud_y + 28)], fill=(255, 215, 0, 255), width=3)

        mins = int(t_sec // 60)
        secs = int(t_sec % 60)
        centisecs = int((t_sec * 100) % 100)
        hud_draw.text((hud_x, hud_y + 36), f"TC {mins:02d}:{secs:02d}.{centisecs:02d}", font=hud_font_tc, fill=(0, 240, 255, 220))
        hud_draw.text((hud_x, hud_y + 64), bc["source"], font=hud_font_sm, fill=(160, 175, 195, 190))

        # Safe-Zone 4-Word Kinetic Captions (Y = 1305)
        cap_y = 1305
        active_w_idx = None
        for idx, w in enumerate(words_list):
            if w["start"] <= t_sec <= w["end"]:
                active_w_idx = idx
                break
            elif w["start"] > t_sec:
                if idx > 0 and (t_sec - words_list[idx - 1]["end"]) < 0.40:
                    active_w_idx = idx - 1
                break

        if active_w_idx is None and words_list:
            if t_sec < words_list[0]["start"]:
                active_w_idx = 0
            elif t_sec >= words_list[-1]["end"]:
                active_w_idx = total_words_count - 1

        if active_w_idx is not None and active_w_idx in cached_chunk_pills:
            pill_img, pw, ph = cached_chunk_pills[active_w_idx]
            cap_px = (w_out - pw) // 2
            cap_py = cap_y - (ph // 2)
            frame_canvas.paste(pill_img, (cap_px, cap_py), pill_img)

        proc.stdin.write(frame_canvas.tobytes())

    proc.stdin.close()
    proc.wait()

    # Audio Filtergraph (Sidechain Ducking + Sub-Drops + -14 LUFS)
    cut1_ms = int(beat_cuts[1] * 1000)
    filter_complex = (
        f"aevalsrc='0.12*sin(2*PI*73.41*t)+0.08*sin(2*PI*110*t)+0.05*sin(2*PI*146.83*t)':s=44100:d={total_duration},"
        "lowpass=f=280[bg_raw];"
        "aevalsrc='0.45*sin(2*PI*(65-37*t/1.2)*t)*exp(-2.8*t)':s=44100:d=1.2[sub];"
        "anoisesrc=d=1.2:c=pink:r=44100:a=0.15,bandpass=f=380:width_type=h:w=260,"
        "afade=t=in:st=0:d=0.3,afade=t=out:st=0.3:d=0.9[whoosh];"
        "[sub][whoosh]amix=inputs=2,volume=-16dB,asplit=2[s1][s2];"
        f"[s1]adelay=0|0[h1];[s2]adelay={cut1_ms}|{cut1_ms}[h2];"
        "[h1][h2]amix=inputs=2:normalize=0[sfx];"
        "[bg_raw][sfx]amix=inputs=2:duration=first:normalize=0[bed];"
        "[1:a]asplit=2[sc][v_out];"
        "[bed][sc]sidechaincompress=threshold=0.015:ratio=6:attack=35:release=450[bed_ducked];"
        "[v_out][bed_ducked]amix=inputs=2:duration=first:dropout_transition=0,"
        "loudnorm=I=-14:TP=-1.5:LRA=11[a_master]"
    )

    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(raw_video_tmp),
        "-i", str(clean_wav),
        "-filter_complex", filter_complex,
        "-map", "0:v", "-map", "[a_master]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(out_mp4)
    ], check=True)

    if raw_video_tmp.exists():
        raw_video_tmp.unlink()

    print(f"   🏆 Finished: {out_mp4}")


def main():
    print("=" * 65)
    print("🎙️ The Bull Print Broadcast Prosody & Voice Shootout")
    print("   Comparing: AndrewMultilingualNeural vs ChristopherNeural")
    print("=" * 65)

    # Load 3 Kaggle SDXL plates
    plate_paths = [
        Path("/tmp/tbp_plates/frames/frame_00.jpg"),
        Path("/tmp/tbp_plates/frames/frame_01.jpg"),
        Path("/tmp/tbp_plates/frames/frame_02.jpg"),
    ]
    plates = []
    for p in plate_paths:
        if not p.exists():
            raise FileNotFoundError(f"Missing plate: {p}")
        img = Image.open(p).convert("RGB")
        if img.size != (1080, 1920):
            img = ImageOps.fit(img, (1080, 1920), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        plates.append(img)

    font_file = None
    for cand in [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        str(BASE_DIR / "assets" / "fonts" / "ArialBold.ttf"),
    ]:
        if os.path.exists(cand):
            font_file = cand
            break

    # Voice 1: AndrewMultilingualNeural (Next-Gen Multilingual Voice)
    andrew_wav, andrew_words, andrew_dur, andrew_cuts = asyncio.run(
        synthesize_voice_track("en-US-AndrewMultilingualNeural", "andrew")
    )
    andrew_mp4 = OUT_DIR / "preview_andrew_multilingual.mp4"
    render_broadcast_video(
        tag="andrew",
        voice_label="Andrew Multilingual",
        clean_wav=andrew_wav,
        words_list=andrew_words,
        total_duration=andrew_dur,
        sentence_cuts=andrew_cuts,
        out_mp4=andrew_mp4,
        plates=plates,
        font_file=font_file
    )

    # Voice 2: ChristopherNeural (Master Wall Street Narrator with Relaxed Silence)
    chris_wav, chris_words, chris_dur, chris_cuts = asyncio.run(
        synthesize_voice_track("en-US-ChristopherNeural", "christopher")
    )
    chris_mp4 = OUT_DIR / "preview_christopher_natural.mp4"
    render_broadcast_video(
        tag="christopher",
        voice_label="Christopher Natural",
        clean_wav=chris_wav,
        words_list=chris_words,
        total_duration=chris_dur,
        sentence_cuts=chris_cuts,
        out_mp4=chris_mp4,
        plates=plates,
        font_file=font_file
    )

    # Pop open both previews side by side
    print("\n🚀 Opening both preview MP4s on macOS...")
    try:
        subprocess.run(["open", str(andrew_mp4), str(chris_mp4)], check=True)
        print("   ✅ Both players launched successfully.")
    except Exception as e:
        print(f"   ⚠️ Could not launch player: {e}")


if __name__ == "__main__":
    main()
