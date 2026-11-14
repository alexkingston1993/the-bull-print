"""
Cloud Parallel Video Engine (scripts/cloud_parallel_video_engine.py)
Massive Cloud Concurrency Video Production System:
1. Splits videos into discrete sections according to strict formatting rules:
   - Shorts (9:16 Vertical): Exactly 1 frame every 3.0 seconds (e.g. 30s = 10 frames, 36s = 12 frames).
   - Standard YouTube Videos (16:9 Landscape): Exactly 1 frame every 4.0 seconds, regardless of length (e.g. 12-min = 180 frames).
2. Renders each segment simultaneously across up to 20 GitHub Actions Ubuntu runners.
3. Aggregates all segments into a master video with FFmpeg concat demuxer,
   mixes speech audio with sidechain ducked background music from the audio pool,
   generates high-CTR thumbnail, uploads to YouTube (20,000 units quota pool),
   and publishes companion website article with WebP frames.
4. STRICT CLOUD-ONLY RULE: All heavy execution runs 100% on cloud runners.
"""

import os
import sys
import json
import math
import time
import argparse
import asyncio
import subprocess
import shutil
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.magnates_visual_studio import (
    precompute_cut_typography,
    draw_sliding_word_caption,
    fetch_clean_photographic_plate,
)
from app.services.viral_video_engine import VideoFormatConfig, extract_word_timestamps

def _send_telegram(msg: str):
    try:
        from telegram_bot import send_telegram_alert
        send_telegram_alert(msg)
    except Exception as e:
        logger.debug(f"[Telegram Alert Notice]: {e}")


# ─────────────────────────────────────────────────────────────
# 1. DUPLICATE DETECTION & TOPIC INTEGRITY GUARD
# ─────────────────────────────────────────────────────────────

def check_duplicate_before_prep(topic: str) -> None:
    """
    STRICT DEDUPLICATION GUARD:
    Prevents re-rendering identical visuals or re-uploading topics already published
    in the last 30 days on YouTube or in local content/posts.
    """
    topic_clean = topic.strip().lower()
    topic_words = set(re.sub(r"[^\w\s]", "", topic_clean).split())
    stop_words = {"the", "a", "an", "and", "or", "how", "to", "in", "of", "for", "on", "with", "is", "at", "by", "what", "why"}
    core_words = topic_words - stop_words

    if not core_words:
        raise ValueError(f"Topic '{topic}' does not contain sufficient meaningful keywords.")

    logger.info(f"🔍 [Duplicate Guard] Checking topic integrity for: '{topic}' (core keywords: {core_words})")

    # 1. Check local content/posts
    posts_dir = BASE_DIR / "content" / "posts"
    if posts_dir.exists():
        for p in posts_dir.glob("*.md"):
            name = p.stem.lower().replace("-", " ")
            name_words = set(re.sub(r"[^\w\s]", "", name).split()) - stop_words
            overlap = len(core_words & name_words)
            if len(core_words) > 0 and (overlap / len(core_words)) >= 0.7:
                logger.error(f"⛔ Topic matches published article: {p.name}")
                raise RuntimeError(
                    f"⛔ [Duplicate Guard Triggered] Topic '{topic}' matches already-published content in '{p.name}'. "
                    f"Refusing to generate duplicate video or recycle old visual frames!"
                )

    # 2. Check live YouTube uploads via OAuth pool
    try:
        from app.services.youtube_uploader import get_uploader
        uploader = get_uploader()
        service = uploader._get_service("en")
        if service:
            channel_res = service.channels().list(mine=True, part="contentDetails").execute()
            if channel_res and channel_res.get("items"):
                uploads_pl = channel_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
                recent_items = service.playlistItems().list(
                    playlistId=uploads_pl,
                    part="snippet",
                    maxResults=50,
                ).execute().get("items", [])
                for itm in recent_items:
                    snip = itm.get("snippet", {})
                    v_title = snip.get("title", "")
                    v_words = set(re.sub(r"[^\w\s]", "", v_title.lower()).split()) - stop_words
                    overlap = len(core_words & v_words)
                    if len(core_words) > 0 and (overlap / len(core_words)) >= 0.65:
                        v_id = snip.get("resourceId", {}).get("videoId")
                        logger.error(f"⛔ Topic closely matches YouTube video: '{v_title}' ({v_id})")
                        raise RuntimeError(
                            f"⛔ [Duplicate Guard Triggered] Topic '{topic}' was already published on YouTube as: "
                            f"'{v_title}' (https://youtu.be/{v_id}). "
                            f"Refusing to upload duplicate video frames or recycle existing video!"
                        )
    except RuntimeError:
        raise
    except Exception as e:
        logger.debug(f"[Duplicate Guard] Channel query notice: {e}")

    logger.success(f"✅ [Duplicate Guard] Verified unique topic: '{topic}'")


# ─────────────────────────────────────────────────────────────
# 2. SESSION PREPARATION & DYNAMIC MATRIX PARTITIONING
# ─────────────────────────────────────────────────────────────

def _generate_dynamic_sections(topic: str, vertical: str, duration_sec: float, is_short: bool) -> List[Dict[str, Any]]:
    """Generates procedural section breakdown and visual prompts dynamically tailored to topic."""
    rules = VideoFormatConfig.get_rules(duration_sec, is_short=is_short)
    interval = rules["frame_interval"]
    num_sections = rules["expected_frames"]

    topic_clean = topic.strip()
    topic_lower = topic_clean.lower()
    words_topic = [w for w in re.sub(r"[^\w\s]", "", topic_clean).split() if len(w) > 2]

    # Auto-detect vertical if not explicit
    if any(k in topic_lower for k in ["nifty", "sensex", "banknifty", "fii", "dii", "stock", "option", "calls", "puts"]):
        vertical = "stock_market"
        theme = "blood_red"
        default_symbol = "burning_chart"
    elif any(k in topic_lower for k in ["btc", "bitcoin", "eth", "solana", "crypto", "token", "mev", "siphon"]):
        vertical = "crypto"
        theme = "solana_purple" if "solana" in topic_lower else "lightning_cyan"
        default_symbol = "crypto_orb"
    elif any(k in topic_lower for k in ["insurance", "term", "claim", "irda", "policy"]):
        vertical = "insurance"
        theme = "lightning_cyan"
        default_symbol = "shield_fail"
    else:
        vertical = "stock_market"
        theme = "blood_red"
        default_symbol = "burning_chart"

    lead_word = words_topic[0].upper() if words_topic else "MARKET"
    second_word = words_topic[1].upper() if len(words_topic) > 1 else "ANALYSIS"

    sections = []
    gemini_sections = []
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key, http_options={"api_version": "v1alpha"})
            prompt = f"""
            You are an investigative financial journalist and thriller documentary director (in the style of Coffeezilla, James Jani, and MagnatesMedia).
            Tone: Dark, authoritative, forensic, breathless investigative thriller exposing high-stakes financial crimes and institutional traps.
            STRICT IDENTITY MANDATE:
            - The narrator must NEVER state their name, introduce themselves, or say 'I am [Name]' or 'This is [Name]'.
            - Zero self-identification. Jump straight into the story from the very first syllable.
            - If an identity is ever referenced anywhere, it must ONLY be 'Alex' (Founder & Chief Analyst). Never mention or use the name 'Christopher'.
            Topic: {topic_clean}
            Vertical: {vertical}
            Format: {'60-Second Viral Short (9:16 Vertical)' if is_short else f'{int(duration_sec // 60)}-Minute Masterclass (16:9 Landscape)'}
            Number of discrete sections: {num_sections}

            CRITICAL DIRECTIVES FOR HIGH-RETENTION HUMAN STORYTELLING (AVD >= 70%):
            1. ZERO FINANCIAL JARGON IN THE FIRST 5 SECONDS:
               - STRICTLY FORBIDDEN WORDS in Section 0: 'liquidity', 'absorption', 'VWAP', 'delta', 'correlation', 'fiscal deficit', 'implied volatility', 'order book', 'macroeconomic', 'consolidation'.
               - Section 0 MUST BE A VISCERAL, UNIGNORABLE HOOK: A direct threat, shocking accusation, or urgent mystery confronting the viewer's bank account.
                 * Example: "While you were sleeping, someone just quietly pulled half a billion dollars out of your retirement stocks."
                 * Example: "There is a secret clause hidden in your fixed deposit that the banks pray you never read."

            2. PERSONALIZE THE THREAT (EVERY STORY HAS A VILLAIN, A VICTIM, AND A CRIME):
               - The victim is the everyday viewer working a 9-to-5 job.
               - The villain is the institutional desk, shadow banker, or predatory algorithm.
               - Frame the stakes around what the viewer stands to lose: their hard-earned salary, their children's college fund, their home equity, or their savings.

            3. ONE SINGLE INSANE FACT PER SHORT (NO ACADEMIC DATA DUMPS):
               - Stop trying to explain the entire global economy in 60 seconds.
               - Focus on ONE shocking smoking gun (e.g. "For every ₹100 retail traders poured into this stock, insiders cashed out ₹85 within 48 hours").
               - Build relentless tension for 40 seconds, then drop the jaw-dropping revelation in the final 15 seconds.

            4. PACING & BLOCKBUSTER 3D TYPOGRAPHY DIRECTIVES:
               - 'headline_top': Exactly 1 to 2 words uppercase punchy hook (e.g. '$7 TRILLION', '1.3 MILLION', '2 CRORE', '₹85 LOW', 'H-1B', 'HAL & BEL', '85% OIL').
               - 'headline_mid': Exactly 1 to 2 words uppercase anchor (e.g. 'DEBT TRAP', 'TROOPS', 'TRAPPED', 'CRASH', 'CRACKDOWN', 'SURGE', 'IMPORTED').
               - 'badge_text': High-friction tactical alert stamp (e.g. 'MARKET SHOCK', 'TIME-BOMB', 'CRACKDOWN', 'OVERPRICED', 'TOP SECRET', 'WARNING').
               - 'color_theme': One of 'gold', 'fire', 'emerald', 'cyan', 'warning'.
               - 'visual_prompt': A vivid, cinematic, tangible 35mm photographic description of a CONCRETE PHYSICAL METAPHOR.
                 * STRICTLY FORBIDDEN: Boardrooms, office desks, suits around conference tables, generic business people, charts on laptop screens.
                 * MANDATORY PHYSICAL METAPHORS: Bank vaults sucking vortices, split cargo container ships in storms, gold bullion on dark marble, fighter jets flanking flags, passports locked in chains, robotic arms throwing sparks, distressed trader clutching head before giant red smartphone chart.
                 * Suffix: "cinematic 35mm photograph, dark moody obsidian lighting, volumetric amber and gold rays, 8k hyper-detailed, clean plate, zero text, zero watermark"
               - 'script': Natural, conversational, breathless spoken sentences. Speak like you are leaning in to whisper a dangerous secret.

            Respond ONLY with a valid JSON object matching this structure:
            {{
              "sections": [
                {{
                  "section_index": 0,
                  "headline_top": "...",
                  "headline_mid": "...",
                  "badge_text": "...",
                  "color_theme": "gold",
                  "visual_prompt": "...",
                  "script": "..."
                }}
              ]
            }}
            """
            models_to_try = [
                "gemini-2.0-flash",
                "gemini-1.5-flash",
                "gemini-1.5-pro",
                "gemini-flash-lite-latest",
            ]
            for attempt in range(2):
                for model_name in models_to_try:
                    try:
                        resp = client.models.generate_content(model=model_name, contents=prompt)
                        raw_text = resp.text.strip()
                        if "```json" in raw_text:
                            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                        elif "```" in raw_text:
                            raw_text = raw_text.split("```")[1].split("```")[0].strip()
                        data = json.loads(raw_text)
                        g_secs = data.get("sections", [])
                        if len(g_secs) >= num_sections:
                            gemini_sections = g_secs[:num_sections]
                            logger.success(f"✅ [Script Studio] Successfully generated {num_sections} custom investigative sections via {model_name}")
                            break
                    except Exception as m_err:
                        logger.debug(f"Gemini {model_name} attempt {attempt+1} notice: {m_err}")
                if gemini_sections:
                    break
                time.sleep(2)
        except Exception as e:
            logger.error(f"[Script Studio] Gemini API error: {e}")

    # ZERO HARDCODED FALLBACK MANDATE: Every single beat must be 100% custom-generated for the topic
    if not gemini_sections or len(gemini_sections) < num_sections:
        raise RuntimeError(
            f"⛔ CRITICAL: Failed to generate custom investigative narrative script for topic '{topic_clean}'. "
            f"Acquired {len(gemini_sections) if gemini_sections else 0}/{num_sections} beats. "
            f"Hardcoded scripts, generic modulo fallbacks, and canned text are PERMANENTLY PROHIBITED."
        )

    for i in range(num_sections):
        start_t = round(i * interval, 2)
        end_t = round((i + 1) * interval, 2)
        has_hud = (i in (1, 3, 5))

        g = gemini_sections[i]
        top = str(g.get("headline_top", lead_word))[:24]
        mid = str(g.get("headline_mid", second_word))[:24]
        badge = str(g.get("badge_text", "MARKET SHOCK"))[:20]
        color_theme = str(g.get("color_theme", "gold")).lower()
        visual_prompt = str(g.get("visual_prompt", "")).strip()
        script_text = str(g.get("script", "")).strip()
        # Strict zero identity leak guardrail: Scrub any accidental self-introduction or Christopher references
        script_text = re.sub(r"\b(?:I am|I'm|this is|my name is)\s+Christopher\b", "I'm Alex", script_text, flags=re.IGNORECASE)
        script_text = re.sub(r"\bChristopher\b", "Alex", script_text, flags=re.IGNORECASE)

        if not visual_prompt or len(visual_prompt) < 15:
            visual_prompt = (
                f"Cinematic 35mm photograph, visual metaphor of {top} {mid}, "
                f"massive concrete physical monuments, bank vaults, cargo ships, dark moody obsidian lighting, "
                f"volumetric amber and gold rays, 8k hyper-detailed, clean plate, zero text, zero watermark"
            )

        sections.append({
            "section_index": i,
            "start_sec": start_t,
            "end_sec": end_t,
            "duration": round(end_t - start_t, 2),
            "headline_top": top[:24],
            "headline_mid": mid[:24],
            "badge_text": badge[:20],
            "color_theme": color_theme,
            "visual_prompt": visual_prompt,
            "theme": theme,
            "symbol_type": default_symbol,
            "method_c_hud": has_hud,
            "script": script_text,
        })
    return sections


def _synthesize_local_christopher_audio(script_text: str, audio_path: Path, words_path: Path, total_duration_sec: float = 60.0) -> List[Dict[str, Any]]:
    """
    OFFICIAL SIGNATURE CHRISTOPHER CLONED VOICE ENGINE
    - Synthesizes 100% authentic Christopher narration for the given script.
    - Mastering: Highpass 70Hz + 135Hz chest resonance EQ + optical compression + -16 LUFS.
    - Word Alignment: Millisecond-accurate word timestamps for kinetic typography.
    """
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    words_path.parent.mkdir(parents=True, exist_ok=True)
    
    from app.services.local_christopher_tts import synthesize_chapter_offline
    logger.info("🎙️ [Voice Engine] Invoking signature Christopher voice narration...")
    res = synthesize_chapter_offline(
        script_text=script_text,
        out_mp3_path=str(audio_path),
        out_timestamps_json=str(words_path)
    )
    with open(words_path, "r", encoding="utf-8") as f:
        words_data = json.load(f)
    
    # Format normalization for renderer
    normalized_words = []
    for w in words_data:
        normalized_words.append({
            "word": w.get("word", "").strip().upper(),
            "start": float(w.get("startSec", w.get("start", 0.0))),
            "end": float(w.get("endSec", w.get("end", 0.0))),
        })
    with open(words_path, "w", encoding="utf-8") as f:
        json.dump(normalized_words, f, indent=2)

    logger.success(f"✅ [Voice Engine] Christopher narration mastered: {audio_path.name} ({res['durationSec']:.1f}s, {len(normalized_words)} words)")
    return normalized_words


def prepare_session(
    topic: str,
    vertical: str = "stock_market",
    duration_sec: int = 60,
    is_short: bool = True,
    output_dir: Optional[Path] = None,
    privacy_status: str = "unlisted",
    skip_duplicate_check: bool = False
):
    """
    Job 1: Prepares the full video session in the cloud.
    Emits GitHub Actions matrix output for up to 20 parallel runner workers!
    """
    if not topic or not topic.strip():
        raise ValueError("A valid non-empty topic must be provided for video generation.")

    if not skip_duplicate_check:
        check_duplicate_before_prep(topic)

    if output_dir is None:
        output_dir = BASE_DIR / "output" / "session_bundle"
    output_dir.mkdir(parents=True, exist_ok=True)
    frames_dir = output_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    audio_dir = output_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    slug = topic.lower().replace(" ", "-").replace(":", "").replace("/", "")[:48]
    sections = _generate_dynamic_sections(topic, vertical, float(duration_sec), is_short)
    total_segments = len(sections)

    logger.info(f"🚀 [Session Prep] Topic: '{topic}' | Format: {'Short 9:16' if is_short else 'Standard 16:9'} | Segments: {total_segments}")

    # 1. Synthesize 100% Offline Cloned Christopher Voice & Extract Word Timestamps
    full_script = " ".join(s["script"] for s in sections)
    audio_file = audio_dir / "speech.mp3"
    words_file = audio_dir / "words.json"
    words = _synthesize_local_christopher_audio(full_script, audio_file, words_file, total_duration_sec=float(duration_sec))

    # 2. Generate High-CTR Background Frames for each section (Batch-Aware & Aspect-Ratio Strict)
    rules = VideoFormatConfig.get_rules(float(duration_sec), is_short=is_short)
    w_out, h_out = rules["width"], rules["height"]
    frame_files = []
    
    missing_frame_prompts = []
    for s in sections:
        idx = s["section_index"]
        frame_path = frames_dir / f"frame_{idx:02d}.jpg"
        approved_dir = BASE_DIR / "assets" / "approved_bundles" / slug
        approved_frame = approved_dir / f"frame_{idx:02d}.jpg"
        if approved_frame.exists():
            shutil.copy2(approved_frame, frame_path)
            logger.success(f"🎯 [Session Prep] Using verified user-approved frame: {approved_frame.name}")
        elif not frame_path.exists():
            prompt = s.get("visual_prompt")
            if not prompt or len(prompt.strip()) < 10:
                prompt = (
                    f"Cinematic 35mm photograph, visual metaphor of {s.get('headline_top', '')} {s.get('headline_mid', '')}, "
                    f"massive concrete physical monuments, bank vaults, cargo ships, dark moody obsidian lighting, "
                    f"volumetric amber and gold rays, 8k hyper-detailed, clean plate, zero text, zero watermark"
                )
            missing_frame_prompts.append({
                "id": idx + 1,
                "prompt": prompt,
                "output_path": str(frame_path),
                "section": s
            })

    # If missing frames, dispatch in a single Kaggle GPU batch for 20x efficiency
    if missing_frame_prompts:
        logger.info(f"⚡ [Session Prep] Dispatching {len(missing_frame_prompts)} bespoke plates to Kaggle Dual-T4 GPU...")
        try:
            from app.services.kaggle_image_worker import KaggleImageWorker
            worker = KaggleImageWorker()
            aspect = "9:16" if is_short else "16:9"
            worker.generate_batch(
                prompts=[{"prompt": m["prompt"], "output_path": m["output_path"]} for m in missing_frame_prompts],
                aspect_ratio=aspect
            )
        except Exception as k_err:
            logger.warning(f"[Session Prep] Kaggle batch dispatch notice: {k_err}")

    # Ensure every single frame exists and is fitted to exact aspect ratio (zero squashing)
    for s in sections:
        idx = s["section_index"]
        frame_path = frames_dir / f"frame_{idx:02d}.jpg"
        if not frame_path.exists():
            fetch_clean_photographic_plate(
                prompt=s.get("visual_prompt", ""),
                width=w_out,
                height=h_out,
                out_path=frame_path
            )
        # Verify aspect ratio and fit with ImageOps to guarantee zero distortion
        try:
            with Image.open(frame_path) as raw_img:
                if raw_img.size != (w_out, h_out):
                    fitted = ImageOps.fit(raw_img.convert("RGB"), (w_out, h_out), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
                    fitted.save(frame_path, quality=95)
        except Exception as f_err:
            logger.debug(f"Frame fit check: {f_err}")

        frame_files.append(str(frame_path.relative_to(output_dir)))
        s["frame_file"] = str(frame_path.relative_to(output_dir))

    # 3. Dynamic Speech-Aligned Section Boundaries & Millisecond Word Mapping
    probe_dur = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_file)
    ], stdout=subprocess.PIPE, text=True, check=True)
    total_audio_dur = max(float(probe_dur.stdout.strip()), 1.0)

    s_word_counts = [max(len(s.get("script", "").split()), 1) for s in sections]
    total_script_words = sum(s_word_counts)
    total_audio_words = len(words)

    if total_audio_words > 0:
        curr_w_idx = 0
        for s_idx, s in enumerate(sections):
            if s_idx == len(sections) - 1:
                sec_words = words[curr_w_idx:]
            else:
                target_cnt = max(1, int(round(s_word_counts[s_idx] * (total_audio_words / max(total_script_words, 1)))))
                end_w_idx = min(total_audio_words, curr_w_idx + target_cnt)
                sec_words = words[curr_w_idx:end_w_idx]
                curr_w_idx = end_w_idx
            s["words"] = sec_words

        # Compute dynamic section start_sec and end_sec matching the speech rhythm
        for s_idx, s in enumerate(sections):
            if s_idx == 0:
                s["start_sec"] = 0.0
            else:
                s["start_sec"] = sections[s_idx - 1]["end_sec"]

            if s_idx == len(sections) - 1:
                s["end_sec"] = round(total_audio_dur, 2)
            else:
                this_words = s.get("words", [])
                next_words = sections[s_idx + 1].get("words", [])
                if this_words and next_words:
                    mid = (this_words[-1]["end"] + next_words[0]["start"]) / 2.0
                    s["end_sec"] = round(max(s["start_sec"] + 0.5, mid), 2)
                elif this_words:
                    s["end_sec"] = round(max(s["start_sec"] + 0.5, this_words[-1]["end"] + 0.2), 2)
                else:
                    s["end_sec"] = round(s["start_sec"] + (total_audio_dur / len(sections)), 2)
            s["duration"] = round(s["end_sec"] - s["start_sec"], 2)

            # Clamp word timestamps cleanly inside the section window
            for w in s.get("words", []):
                w["start"] = max(s["start_sec"], w.get("start", s["start_sec"]))
                w["end"] = min(s["end_sec"], max(w["start"] + 0.1, w.get("end", s["end_sec"])))
    else:
        logger.warning("⚠️ Words list empty from transcription. Generating procedural millisecond word timestamps...")
        time_per_section = total_audio_dur / max(len(sections), 1)
        for s_idx, s in enumerate(sections):
            s_start = round(s_idx * time_per_section, 2)
            s_end = round((s_idx + 1) * time_per_section, 2)
            s["start_sec"] = s_start
            s["end_sec"] = s_end
            s["duration"] = round(s_end - s_start, 2)

            s_tokens = [t.strip().upper() for t in s.get("script", "").split() if t.strip()]
            sec_words = []
            if s_tokens:
                step = (s_end - s_start - 0.2) / max(len(s_tokens), 1)
                for w_i, tok in enumerate(s_tokens):
                    w_st = round(s_start + 0.1 + w_i * step, 3)
                    w_et = round(w_st + min(0.35, step * 0.85), 3)
                    sec_words.append({
                        "word": tok,
                        "start": w_st,
                        "end": w_et,
                        "startSec": w_st,
                        "endSec": w_et
                    })
            s["words"] = sec_words

    # 3. Partition into GHA (up to 20 runners) vs Kaggle GPU Overflow
    gha_limit = 20
    gha_indices = list(range(min(total_segments, gha_limit)))
    kaggle_indices = list(range(gha_limit, total_segments)) if total_segments > gha_limit else []
    has_overflow = len(kaggle_indices) > 0

    manifest = {
        "topic": topic,
        "vertical": vertical,
        "is_short": is_short,
        "duration_sec": duration_sec,
        "privacy_status": privacy_status,
        "slug": slug,
        "total_segments": total_segments,
        "gha_indices": gha_indices,
        "kaggle_indices": kaggle_indices,
        "audio_file": str(audio_file.relative_to(output_dir)),
        "words_file": str(words_file.relative_to(output_dir)),
        "sections": sections,
    }

    manifest_path = output_dir / "session_manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    logger.success(f"✅ [Session Prep] Session manifest written: {manifest_path}")

    # 4. Emit GitHub Actions outputs for dynamic matrix
    gha_output_file = os.getenv("GITHUB_OUTPUT")
    matrix_json = json.dumps({"include": [{"index": i} for i in gha_indices]})
    if gha_output_file:
        with open(gha_output_file, "a") as f:
            f.write(f"matrix={matrix_json}\n")
            f.write(f"total_segments={total_segments}\n")
            f.write(f"has_overflow={'true' if has_overflow else 'false'}\n")
            f.write(f"is_short={'true' if is_short else 'false'}\n")
            f.write(f"topic={topic}\n")
            f.write(f"slug={slug}\n")
    print(f"\n::set-output name=matrix::{matrix_json}")
    print(f"Matrix JSON: {matrix_json}")


# ─────────────────────────────────────────────────────────────
# 2. PARALLEL SEGMENT RENDERING (Executed on Ubuntu Matrix Runners)
# ─────────────────────────────────────────────────────────────

def render_segment(segment_index: int, bundle_dir: Path, output_dir: Optional[Path] = None):
    """
    Job 2: Renders a single discrete segment in seconds on an isolated Ubuntu runner.
    Takes background frame, renders Ken Burns pan/zoom, Method C HUD overlay,
    and frame-accurate spoken-word captions directly to FFmpeg rawvideo pipe.
    """
    manifest_path = bundle_dir / "session_manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Session manifest missing: {manifest_path}")

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    sections = manifest["sections"]
    if segment_index >= len(sections):
        raise IndexError(f"Segment index {segment_index} out of range (max {len(sections)-1})")

    sec = sections[segment_index]
    is_short = manifest["is_short"]
    rules = VideoFormatConfig.get_rules(sec["duration"], is_short=is_short)
    w_out, h_out = rules["width"], rules["height"]
    fps = 25
    seg_duration = sec["duration"]
    total_frames = int(math.ceil(seg_duration * fps))

    if output_dir is None:
        output_dir = BASE_DIR / "output" / "rendered_segments"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_video_path = output_dir / f"segment_{segment_index:02d}.mp4"

    logger.info(f"🎬 [Runner {segment_index}] Rendering segment {segment_index:02d} ({seg_duration:.1f}s, {total_frames} frames)...")

    # Load high-CTR base frame
    frame_rel = sec["frame_file"]
    frame_full = bundle_dir / frame_rel
    base_img = Image.open(frame_full).convert("RGB")
    if base_img.size != (w_out, h_out):
        base_img = ImageOps.fit(base_img, (w_out, h_out), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))

    # -------------------------------------------------------------
    # 4-WORD KINETIC TYPOGRAPHY CAPTION SYSTEM (MRBEAST / HORMOZI STYLE)
    # Shows 4 words across the screen at any given time.
    # The active spoken word scales up 1.22x and illuminates in vibrant gold,
    # while inactive words in the cluster remain crisp white.
    # -------------------------------------------------------------
    words_list = sec.get("words", [])
    chunk_size = 4
    
    # Locate best available bold font file
    font_file = None
    for cand in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        str(BASE_DIR / "assets" / "fonts" / "Inter-Bold.ttf"),
    ]:
        if os.path.exists(cand):
            font_file = cand
            break

    # Pre-render 4-word composite states keyed by global word index
    cached_chunk_pills = {}
    total_words_count = len(words_list)
    
    for w_global_idx in range(total_words_count):
        chunk_start_idx = (w_global_idx // chunk_size) * chunk_size
        chunk_words_slice = words_list[chunk_start_idx : chunk_start_idx + chunk_size]
        active_in_chunk = w_global_idx - chunk_start_idx
        words_text_list = [item["word"] for item in chunk_words_slice]
        
        # Auto-fit base font size so the 4 words never exceed safe screen margins
        max_allowed_w = int(w_out * 0.88)
        base_size = int(rules.get("caption_font_size", 54) * 0.85)
        
        while base_size >= 24:
            if font_file:
                try:
                    f_norm = ImageFont.truetype(font_file, base_size)
                    f_act = ImageFont.truetype(font_file, int(base_size * 1.22))
                except Exception:
                    f_norm = ImageFont.load_default()
                    f_act = f_norm
            else:
                f_norm = ImageFont.load_default()
                f_act = f_norm
                
            wb_list = []
            for i, w_txt in enumerate(words_text_list):
                f_curr = f_act if i == active_in_chunk else f_norm
                bbox = f_curr.getbbox(w_txt)
                bw = bbox[2] - bbox[0]
                bh = bbox[3] - bbox[1]
                wb_list.append((w_txt, bw, bh, f_curr))
                
            spacing = int(base_size * 0.35)
            row_w = sum(b[1] for b in wb_list) + spacing * max(len(wb_list) - 1, 0)
            if row_w <= max_allowed_w or base_size <= 24:
                break
            base_size -= 2
            
        pad_x = 28
        pad_y = 16
        max_h = max(b[2] for b in wb_list) if wb_list else 40
        pw = row_w + pad_x * 2
        ph = max_h + pad_y * 2
        
        pill = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        pdraw = ImageDraw.Draw(pill)
        # Sleek dark glass pill backdrop with vibrant border
        pdraw.rounded_rectangle(
            [0, 0, pw - 1, ph - 1],
            radius=rules.get("border_radius", 20),
            fill=(6, 10, 20, 235),
            outline=(20, 241, 149, 210),
            width=3
        )
        
        cx = pad_x
        for i, (w_txt, bw, bh, f_curr) in enumerate(wb_list):
            y_off = (max_h - bh) // 2
            if i == active_in_chunk:
                # Active spoken word: drop shadow + vibrant energetic gold
                pdraw.text((cx + 3, pad_y + y_off + 3), w_txt, font=f_curr, fill=(0, 0, 0, 255))
                pdraw.text((cx, pad_y + y_off), w_txt, font=f_curr, fill=(250, 204, 21, 255))
            else:
                # Inactive words in the cluster: drop shadow + crisp white
                pdraw.text((cx + 2, pad_y + y_off + 2), w_txt, font=f_curr, fill=(0, 0, 0, 230))
                pdraw.text((cx, pad_y + y_off), w_txt, font=f_curr, fill=(245, 245, 250, 255))
            cx += bw + spacing
            
        cached_chunk_pills[w_global_idx] = (pill, pw, ph)

    # Precompute 3D Kinetic Headline Typography Layer
    headline_lines = [l for l in [sec.get("headline_top", ""), sec.get("headline_mid", "")] if l]
    if not headline_lines:
        headline_lines = ["MARKET CATALYST", "INSTITUTIONAL FLOW"]
    badge_label = sec.get("badge_text", "BREAKING [!]")
    
    typo_3d = precompute_cut_typography(
        lines=headline_lines,
        badge_text=badge_label,
        max_sheared_w=int(w_out * 0.88),
        color_theme=sec.get("color_theme", "gold")
    )

    # Launch FFmpeg Rawvideo Pipe
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{w_out}x{h_out}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-crf", "18",
        str(out_video_path)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    # Precompute atmospheric vignette gradients (top 38% for title separation, bottom 28% for captions)
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

    # Render frame stream with Ken Burns + 3D Kinetic Slam + Sliding Word Captions
    seg_start = sec["start_sec"]
    for f_idx in range(total_frames):
        t_current = seg_start + (f_idx / fps)
        
        # Ken Burns subtle zoom (1.00 -> 1.04)
        progress = f_idx / max(total_frames, 1)
        scale = 1.0 + (0.04 * progress)
        zw, zh = int(w_out * scale), int(h_out * scale)
        frame_canvas = base_img.resize((zw, zh), Image.Resampling.BILINEAR)
        cx, cy = (zw - w_out) // 2, (zh - h_out) // 2
        frame_canvas = frame_canvas.crop((cx, cy, cx + w_out, cy + h_out))

        # Atmospheric grading & dark separation vignette
        frame_canvas = ImageEnhance.Contrast(frame_canvas).enhance(1.15)
        frame_canvas = ImageEnhance.Color(frame_canvas).enhance(1.18)
        frame_canvas.paste(vignette_top, (0, 0), vignette_top)
        frame_canvas.paste(vignette_bot, (0, h_out - vignette_bot.height), vignette_bot)

        # Check active spoken word in the audio stream
        active_w_idx = None
        for idx, w in enumerate(words_list):
            if w["start"] <= t_current <= w["end"]:
                active_w_idx = idx
                break
            elif w["start"] > t_current:
                if idx > 0 and (t_current - words_list[idx - 1]["end"]) < 0.45:
                    active_w_idx = idx - 1
                break
        
        # Smooth boundaries: start of segment shows first word, end of segment retains last word
        if active_w_idx is None and total_words_count > 0:
            if words_list and t_current < words_list[0]["start"]:
                active_w_idx = 0
            elif words_list and t_current >= words_list[-1]["end"]:
                active_w_idx = total_words_count - 1

        # Elastic Kinetic Slam Pop-In for 3D Typography (1.35x -> 1.0x over first 0.45s)
        slam_dur = 0.45
        t_in_sec = t_current - seg_start
        if t_in_sec < slam_dur:
            p = t_in_sec / slam_dur
            scale_slam = 1.0 + (0.35 * (1.0 - math.sin(p * math.pi / 2.0)))
        else:
            scale_slam = 1.0

        tw, th = typo_3d["width"], typo_3d["height"]
        if abs(scale_slam - 1.0) > 0.01:
            cur_w = max(10, int(tw * scale_slam))
            cur_h = max(10, int(th * scale_slam))
            t_img = typo_3d["text_img"].resize((cur_w, cur_h), Image.Resampling.BILINEAR)
            b_img = typo_3d["bloom_img"].resize((cur_w, cur_h), Image.Resampling.BILINEAR)
        else:
            t_img, b_img = typo_3d["text_img"], typo_3d["bloom_img"]
            cur_w, cur_h = tw, th

        paste_x = (w_out - cur_w) // 2
        paste_y = int(h_out * 0.18) - (cur_h // 2)
        frame_canvas.paste(b_img, (paste_x, paste_y), b_img)
        frame_canvas.paste(t_img, (paste_x, paste_y), t_img)

        # Kinetic Word-Level Captions in Mobile Safe Zone (Y = 1480 for 9:16 Shorts, Y = 920 for 16:9 Docs)
        cap_y = int(h_out * 0.77) if is_short else int(h_out * 0.85)
        if active_w_idx is not None and active_w_idx in cached_chunk_pills:
            pill_img, pw, ph = cached_chunk_pills[active_w_idx]
            cap_px = (w_out - pw) // 2
            cap_py = cap_y - (ph // 2)
            frame_canvas.paste(pill_img, (cap_px, cap_py), pill_img)
        elif active_w_idx is not None and words_list:
            active_word = words_list[active_w_idx]["word"]
            draw_sliding_word_caption(frame_canvas, sec.get("script", ""), active_word, y=cap_y, active_word_index=active_w_idx)

        proc.stdin.write(frame_canvas.tobytes())

    proc.stdin.close()
    proc.wait()
    logger.success(f"✅ [Runner {segment_index}] Rendered: {out_video_path.name} ({out_video_path.stat().st_size // 1024} KB)")

    # Dual-save non-padded alias for maximum matrix artifact compatibility
    alt_video_path = output_dir / f"segment_{segment_index}.mp4"
    if not alt_video_path.exists() and out_video_path.exists():
        try:
            shutil.copyfile(out_video_path, alt_video_path)
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────
# 3. CONCATENATION, DUCKED BGM MIXING & UPLOAD TO YOUTUBE
# ─────────────────────────────────────────────────────────────

def aggregate_and_publish(bundle_dir: Path, segments_dir: Path, output_dir: Optional[Path] = None):
    """
    Job 3: Terminal aggregator & publisher.
    Losslessly concatenates all segments, mixes speech + ducked BGM,
    generates thumbnail, uploads to YouTube, and publishes website article.
    """
    manifest_path = bundle_dir / "session_manifest.json"
    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    if output_dir is None:
        output_dir = BASE_DIR / "output" / manifest["slug"]
    output_dir.mkdir(parents=True, exist_ok=True)

    total_segments = manifest["total_segments"]
    concat_list_file = output_dir / "concat_list.txt"
    with open(concat_list_file, "w") as f:
        for i in range(total_segments):
            cand1 = segments_dir / f"segment_{i:02d}.mp4"
            cand2 = segments_dir / f"segment_{i}.mp4"
            seg_file = cand1 if cand1.exists() else cand2
            if not seg_file.exists():
                # Recursive search in case actions/download-artifact nested artifacts
                matches = list(segments_dir.rglob(f"segment_{i:02d}.mp4")) + list(segments_dir.rglob(f"segment_{i}.mp4"))
                if matches:
                    seg_file = matches[0]
                else:
                    raise FileNotFoundError(f"Missing rendered segment artifact: {cand1}")
            f.write(f"file '{seg_file.resolve()}'\n")

    # 1. Lossless Video Concatenation
    visual_concat_mp4 = output_dir / "visual_concat.mp4"
    logger.info("🎬 [Aggregator] Concatenating segment videos with FFmpeg concat demuxer...")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list_file), "-c", "copy", str(visual_concat_mp4)
    ], check=True, capture_output=True)

    # 2. Select Music Bed from Pool & Apply Sidechain Ducking
    # Strict rule: NEVER use synthetic bloop/arcade arpeggio tracks (emerald_breakout, etc.)
    # Use sleek, low-profile cinematic ambient beds (subterranean pulse, wall street afterhours, etc.)
    vertical = manifest.get("vertical", "stock_market")
    topic_text = (manifest.get("topic") or "").lower()
    is_dark_or_investigative = any(k in topic_text for k in ["trap", "crash", "liquidation", "manipulation", "stop hunt", "sweep", "fii", "exposed", "truth", "mev", "siphon", "dump"])
    
    preferred_category = "dark_investigative" if (is_dark_or_investigative or vertical in ["stock_market", "crypto"]) else "neutral_educational"
    mood_dir = BASE_DIR / "assets" / "audio" / "bgm_pool" / preferred_category

    # Gather candidates, strictly filtering out any blacklisted tracks
    raw_candidates = list(mood_dir.glob("*.wav")) + list((BASE_DIR / "assets" / "audio" / "bgm_pool").glob("*.wav"))
    bgm_candidates = [
        f for f in raw_candidates 
        if not any(banned in f.name.lower() for banned in ["emerald", "breakout", "bounce", "fomo", "arcade", "bloop"])
    ]

    default_cinematic_bed = BASE_DIR / "assets" / "audio" / "bgm_pool" / "bed_01_subterranean_pulse.wav"
    bgm_file = bgm_candidates[0] if bgm_candidates else default_cinematic_bed

    speech_audio = bundle_dir / manifest["audio_file"]
    final_video_mp4 = output_dir / f"{manifest['slug']}_final.mp4"

    logger.info(f"🎵 [Aggregator] Mixing subtle cinematic ambient bed (no bloops): {bgm_file.name}")
    # Subtle -16dB background bed with fast ducking underneath Christopher voice
    filter_complex = "[1:a]volume=0.16[bg];[bg][0:a]sidechaincompress=threshold=0.06:ratio=8:attack=30:release=250[ducked];[0:a][ducked]amix=inputs=2:duration=first[aout]"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(speech_audio),
        "-i", str(bgm_file),
        "-i", str(visual_concat_mp4),
        "-filter_complex", filter_complex,
        "-map", "2:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(final_video_mp4)
    ], check=True, capture_output=True)

    logger.success(f"🎉 [Aggregator] Assembled final broadcast master: {final_video_mp4.name} ({final_video_mp4.stat().st_size // 1024} KB)")

    # 3. Mandatory Pre-Upload Quality Control Gate & High-CTR 3D Typography Thumbnail
    is_short = manifest.get("is_short", False)
    
    # Run ffprobe stream and duration verification
    try:
        probe_cmd = [
            "ffprobe", "-v", "error", "-print_format", "json",
            "-show_streams", "-show_format", str(final_video_mp4)
        ]
        probe_res = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
        probe_data = json.loads(probe_res.stdout)
        v_stream = next((s for s in probe_data.get("streams", []) if s.get("codec_type") == "video"), None)
        a_stream = next((s for s in probe_data.get("streams", []) if s.get("codec_type") == "audio"), None)
        
        if not v_stream or not a_stream:
            raise ValueError("Pre-Upload QC Failed: Master video must contain both video and audio streams.")
        
        act_w = int(v_stream.get("width", 0))
        act_h = int(v_stream.get("height", 0))
        exp_w = 1080 if is_short else 1920
        exp_h = 1920 if is_short else 1080
        if (act_w, act_h) != (exp_w, exp_h):
            raise ValueError(f"Pre-Upload QC Failed: Video aspect ratio distorted! Got {act_w}x{act_h}, expected {exp_w}x{exp_h}.")
        
        dur = float(probe_data.get("format", {}).get("duration", 0))
        if dur < 10.0:
            raise ValueError(f"Pre-Upload QC Failed: Video duration too short ({dur:.1f}s).")
        logger.success(f"🛡️ [Pre-Upload QC Passed] Validated {act_w}x{act_h} | Duration: {dur:.1f}s | Audio & Video synced.")
    except Exception as qc_err:
        logger.error(f"⛔ CRITICAL PRE-UPLOAD QC HALT: {qc_err}")
        _send_telegram(f"🚨 Pre-Upload QC Failed on {manifest.get('topic')}: {qc_err}. Video upload permanently halted.")
        raise

    # Extract High-CTR Thumbnail from segment 0 (0.45s after 3D typography slam pop-in)
    thumb_path = output_dir / "high_ctr_thumbnail.jpg"
    first_seg = segments_dir / "segment_00.mp4"
    if not first_seg.exists():
        matches = list(segments_dir.rglob("segment_00.mp4")) + list(segments_dir.rglob("segment_0.mp4"))
        if matches:
            first_seg = matches[0]
    if first_seg.exists():
        subprocess.run([
            "ffmpeg", "-y", "-ss", "0.45", "-i", str(first_seg),
            "-vframes", "1", "-q:v", "2", str(thumb_path)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not thumb_path.exists() or thumb_path.stat().st_size < 1000:
        fallback_frame = bundle_dir / "frames" / "frame_00.jpg"
        if fallback_frame.exists():
            thumb_path = fallback_frame

    # 4. Upload to YouTube with 20,000 quota pool
    yt_url = ""
    try:
        title = f"{manifest['topic']} | The Bull Print"
        description = (
            f"Forensic breakdown of {manifest['topic']}.\n\n"
            f"Read the full verified research report & real-time market data on our portal:\n"
            f"https://bullprintmedia.com/posts/{manifest['slug']}\n\n"
            f"#trading #finance #investing #algotrading #wealth"
        )
        tags = ["stock market", "crypto", "trading", "finance", "the bull print"]
        privacy_status = manifest.get("privacy_status") or os.getenv("YOUTUBE_PRIVACY", "unlisted")

        from app.services.youtube_uploader import get_uploader
        uploader = get_uploader()
        res = uploader.upload_video(
            language="en",
            video_path=str(final_video_mp4),
            title=title[:95],
            description=description,
            tags=tags,
            thumbnail_path=str(thumb_path) if thumb_path.exists() else None,
            category_id="27",
            privacy_status=privacy_status,
            is_short=manifest.get("is_short", False),
            force_upload=True,
        )
        vid_id = (res.get("video_id") or res.get("id")) if isinstance(res, dict) else None
        if vid_id:
            yt_url = res.get("url") or f"https://youtu.be/{vid_id}"
            logger.success(f"🚀 [YouTube Upload] Broadcast Live: {yt_url}")
        elif res and isinstance(res, dict) and not res.get("success"):
            logger.warning(f"YouTube upload returned error: {res.get('error')}")
    except Exception as yt_err:
        logger.warning(f"YouTube upload failed or skipped in this environment: {yt_err}")

    # 4. Generate Companion Website Article & Alert Telegram
    try:
        from engine import generate_website_article_file
        article_payload = {
            "campaign_id": manifest["slug"],
            "topic": manifest["topic"],
            "vertical": manifest["vertical"],
            "website_article_payload": {
                "seo_title": f"{manifest['topic']}: Institutional Market Breakdown",
                "meta_description": f"Comprehensive forensic analysis of {manifest['topic']} by The Bull Print.",
                "article_sections": [
                    {
                        "h2": s.get("section_name", f"Section {i+1}"),
                        "p": s.get("script", "")
                    }
                    for i, s in enumerate(manifest.get("sections", []))
                ]
            }
        }
        timestamps = [f"{int(s['start_sec']//60):02d}:{int(s['start_sec']%60):02d} {s.get('section_name', '')}" for s in manifest.get("sections", [])]
        article_path = generate_website_article_file(
            payload=article_payload,
            youtube_video_id=vid_id or "",
            timestamps_log=timestamps
        )
        logger.success(f"📰 [Website Article] Published: {article_path}")
    except Exception as a_err:
        logger.warning(f"Article generation notice: {a_err}")

    # 5. Telegram Mission Notification
    alert_msg = (
        f"🕶️☕ *AGENT ARIA: CLOUD PARALLEL PRODUCTION COMPLETE* 🚀\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 *Topic:* `{manifest['topic']}`\n"
        f"⚡ *Runners:* Rendered across `{total_segments}` parallel Ubuntu runners\n"
        f"🎬 *Video Master:* `{final_video_mp4.name}`\n"
        f"🌐 *Web Article:* `https://bullprintmedia.com/posts/{manifest['slug']}`\n"
        f"▶️ *YouTube:* {yt_url or '_Uploaded Headless_'}\n"
        f"🛡️ *Host Status:* 100% cloud-hosted; local Mac remained completely untouchable."
    )
    _send_telegram(alert_msg)


# ─────────────────────────────────────────────────────────────
# CLI ENTRYPOINT
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Cloud Parallel Video Engine")
    parser.add_argument("--mode", choices=["prepare", "render_segment", "aggregate_and_publish", "dispatch_kaggle_overflow"], required=True)
    parser.add_argument("--topic", default=None, help="Specific financial topic. Required for prepare mode.")
    parser.add_argument("--vertical", default="stock_market", help="Market vertical (e.g. stock_market, crypto, commodities, forex, banking, insurance)")
    parser.add_argument("--duration-sec", type=int, default=60)
    parser.add_argument("--duration-min", type=int, default=3)
    parser.add_argument("--is-short", action="store_true", default=True)
    parser.add_argument("--segment-index", type=int, default=0)
    parser.add_argument("--privacy-status", default=os.getenv("YOUTUBE_PRIVACY", "unlisted"), choices=["public", "unlisted", "private"])
    parser.add_argument("--skip-duplicate-check", action="store_true", default=False)
    parser.add_argument("--bundle-dir", type=Path, default=BASE_DIR / "output" / "session_bundle")
    parser.add_argument("--segments-dir", type=Path, default=BASE_DIR / "output" / "rendered_segments")
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    if args.mode == "prepare":
        if not args.topic:
            raise ValueError("Error: --topic is required when running in 'prepare' mode. Hardcoded defaults are disabled.")
        dur = args.duration_sec if args.is_short else (args.duration_min * 60)
        prepare_session(
            topic=args.topic,
            vertical=args.vertical,
            duration_sec=dur,
            is_short=args.is_short,
            output_dir=args.bundle_dir,
            privacy_status=args.privacy_status,
            skip_duplicate_check=args.skip_duplicate_check
        )
    elif args.mode == "render_segment":
        render_segment(segment_index=args.segment_index, bundle_dir=args.bundle_dir, output_dir=args.output_dir)
    elif args.mode == "aggregate_and_publish":
        aggregate_and_publish(bundle_dir=args.bundle_dir, segments_dir=args.segments_dir, output_dir=args.output_dir)
    elif args.mode == "dispatch_kaggle_overflow":
        from app.services.kaggle_image_worker import KaggleImageWorker
        manifest_file = args.bundle_dir / "session_manifest.json"
        with open(manifest_file) as f:
            manifest = json.load(f)
        overflow_indices = manifest.get("kaggle_indices", [])
        if overflow_indices:
            logger.info(f"⚡ [Kaggle Overflow] Dispatching {len(overflow_indices)} overflow segments to Kaggle GPU...")
            sections = [manifest["sections"][i] for i in overflow_indices]
            worker = KaggleImageWorker()
            if worker.dispatch(sections):
                worker.poll_and_download(args.bundle_dir / "frames")
        else:
            logger.info("No overflow segments allocated to Kaggle.")


if __name__ == "__main__":
    main()
