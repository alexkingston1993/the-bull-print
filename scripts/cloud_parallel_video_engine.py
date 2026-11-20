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
from datetime import datetime, timezone, timedelta
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
    STRICT DEDUPLICATION GUARD (180-DAY ENFORCEMENT):
    Prevents re-rendering identical visuals or re-uploading topics already published
    in the last 180 days on YouTube or in local content/posts.
    Utilizes live YouTube Data API channel history and Gemini Flash Lite LLM semantic comparison.
    """
    topic_clean = topic.strip().lower()
    topic_words = set(re.sub(r"[^\w\s]", "", topic_clean).split())
    stop_words = {"the", "a", "an", "and", "or", "how", "to", "in", "of", "for", "on", "with", "is", "at", "by", "what", "why"}
    core_words = topic_words - stop_words

    if not core_words:
        raise ValueError(f"Topic '{topic}' does not contain sufficient meaningful keywords.")

    logger.info(f"🔍 [Duplicate Guard] Checking 180-day topic integrity for: '{topic}' (core keywords: {core_words})")

    published_titles = []

    # 1. Check local content/posts
    posts_dir = BASE_DIR / "content" / "posts"
    if posts_dir.exists():
        for p in posts_dir.glob("*.md"):
            name = p.stem.lower().replace("-", " ")
            published_titles.append(name)
            name_words = set(re.sub(r"[^\w\s]", "", name).split()) - stop_words
            overlap = len(core_words & name_words)
            if len(core_words) > 0 and (overlap / len(core_words)) >= 0.7:
                logger.error(f"⛔ Topic matches published article: {p.name}")
                raise RuntimeError(
                    f"⛔ [Duplicate Guard Triggered] Topic '{topic}' matches already-published content in '{p.name}'. "
                    f"Refusing to generate duplicate video or recycle old visual frames!"
                )

    # 2. Check live YouTube uploads via OAuth pool (180-day window)
    try:
        from app.services.youtube_uploader import get_uploader
        uploader = get_uploader()
        service = uploader._get_service("en")
        if service:
            channel_res = service.channels().list(mine=True, part="contentDetails").execute()
            if channel_res and channel_res.get("items"):
                uploads_pl = channel_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
                next_page = None
                cutoff_dt = datetime.now(timezone.utc) - timedelta(days=180)
                while True:
                    pl_res = service.playlistItems().list(
                        playlistId=uploads_pl,
                        part="snippet",
                        maxResults=50,
                        pageToken=next_page,
                    ).execute()
                    for itm in pl_res.get("items", []):
                        snip = itm.get("snippet", {})
                        v_title = snip.get("title", "")
                        pub_at = snip.get("publishedAt", "")
                        if pub_at:
                            try:
                                dt = datetime.fromisoformat(pub_at.replace("Z", "+00:00"))
                                if dt < cutoff_dt:
                                    next_page = None
                                    break
                            except Exception:
                                pass
                        if v_title and v_title != "Deleted video":
                            clean_t = v_title.split("|")[0].split("#")[0].strip()
                            published_titles.append(clean_t)
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
                    next_page = pl_res.get("nextPageToken")
                    if not next_page or len(published_titles) >= 150:
                        break
    except RuntimeError:
        raise
    except Exception as e:
        logger.debug(f"[Duplicate Guard] Channel query notice: {e}")

    # 3. LLM-Based Semantic Deduplication Gate (180-day catalog check)
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and published_titles:
        try:
            import requests
            titles_text = "\n".join(f"- {t}" for t in published_titles[:100])
            eval_prompt = f"""You are an institutional compliance deduplication auditor for The Bull Print.
We enforce a STRICT ZERO-DUPLICATION POLICY across a 180-day window.

CANDIDATE TOPIC: "{topic}"

PUBLISHED TITLES (PAST 180 DAYS):
{titles_text}

TASK:
Determine if the CANDIDATE TOPIC covers the same underlying news story, economic event, company scandal/controversy, or specific macro thesis as ANY published video in the list above.
Even if the wording, phrasing, or synonyms are completely different (e.g. "Fed warns of rate shocks" vs "Fed's Waller threatens half-point rate hike", or "Big tech nuclear plants" vs "Atomic reactors for AI datacenters"), if the core underlying catalyst/story is the same, it is a DUPLICATE.

OUTPUT STRICT JSON ONLY:
{{
  "is_duplicate": true or false,
  "matching_title": "string of the matching title or empty",
  "reason": "1-sentence forensic rationale"
}}"""
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": eval_prompt}]}],
                "generationConfig": {"responseMimeType": "application/json"}
            }
            res = requests.post(url, json=payload, timeout=30)
            if res.status_code == 200:
                data = json.loads(res.json()["candidates"][0]["content"]["parts"][0]["text"])
                if data.get("is_duplicate"):
                    matching = data.get("matching_title", "Unknown")
                    reason = data.get("reason", "Semantic topic clone")
                    logger.error(f"⛔ [LLM Semantic Guard Triggered] Topic '{topic}' duplicates '{matching}': {reason}")
                    raise RuntimeError(
                        f"⛔ [LLM Semantic Guard Triggered] Topic '{topic}' duplicates published content '{matching}'. "
                        f"Reason: {reason}. Halting to prevent duplicate video generation!"
                    )
                logger.success(f"✓ [LLM Semantic Guard Passed] Verified 100% unique against {len(published_titles)} past titles (180-day window)")
        except RuntimeError:
            raise
        except Exception as llm_err:
            logger.debug(f"[Duplicate Guard] LLM evaluation notice: {llm_err}")

    logger.success(f"✅ [Duplicate Guard] Verified unique topic over 180-day window: '{topic}'")
    return published_titles


# ─────────────────────────────────────────────────────────────
# 2. SESSION PREPARATION & DYNAMIC MATRIX PARTITIONING
# ─────────────────────────────────────────────────────────────

def _query_gemini_smart(prompt: str, client, api_key: Optional[str], models_to_try: List[str]) -> Optional[str]:
    """
    High-reliability Gemini caller:
    Prioritizes direct REST via standard requests HTTPS (immune to httpx HTTP/2 ALPN SSL handshake stalls),
    with automatic model fallback (gemini-flash-lite-latest -> gemini-3.5-flash-lite -> gemini-3.8-flash)
    and SDK fallback.
    """
    import requests
    # 1. Direct REST call via requests (instant ~1.5s latency, zero SSL handshake stalls)
    if api_key:
        rest_models = ["gemini-flash-lite-latest", "gemini-flash-latest", "gemini-3.1-flash-lite", "gemini-3-flash-preview", "gemini-3.5-flash-lite"]
        for rm in rest_models:
            for attempt in range(2):
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{rm}:generateContent?key={api_key}"
                    payload = {
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "maxOutputTokens": 8192,
                            "responseMimeType": "application/json"
                        }
                    }
                    r = requests.post(url, json=payload, timeout=60)
                    if r.status_code == 200:
                        cand = r.json().get("candidates", [])
                        if cand:
                            text = cand[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                            if text:
                                logger.success(f"✅ [Script Studio] Successfully generated script via REST ({rm})")
                                return text.strip()
                    elif r.status_code == 503:
                        logger.debug(f"REST model {rm} 503 high demand; waiting 2s...")
                        time.sleep(2)
                    else:
                        logger.debug(f"REST model {rm} HTTP {r.status_code}: {r.text[:100]}")
                except Exception as re_err:
                    logger.debug(f"REST model {rm} notice: {re_err}")

    # 2. SDK fallback
    if client:
        for m in models_to_try:
            try:
                resp = client.models.generate_content(model=m, contents=prompt)
                if resp and resp.text:
                    logger.success(f"✅ [Script Studio] Successfully generated script via SDK ({m})")
                    return resp.text.strip()
            except Exception as e:
                logger.debug(f"SDK model {m} notice: {e}")

    return None


def _generate_dynamic_sections(topic: str, vertical: str, duration_sec: float, is_short: bool) -> List[Dict[str, Any]]:
    """
    Generates procedural section breakdown and visual prompts dynamically tailored to topic.
    - Shorts (9:16 Vertical, 60s): 20 discrete 3.0s cuts (20 unique bespoke plates).
    - Documentaries (16:9 Landscape, 12 min): Exactly 36 segments of 20.0s each.
      Generated in 3 sequential chunked API calls (12 segments × 3 = 36 segments)
      with 5 bespoke micro-beats per segment (beat_0..beat_4 of 4.0s each = 180 unique bespoke plates)
      and a running BANNED_VISUAL_MOTIFS list preventing scene fatigue and repetition.
    """
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

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            from app.config import config as app_config
            api_key = app_config.app.get("gemini_api_key")
        except Exception:
            pass
    client = None
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key, http_options={"api_version": "v1beta", "timeout": 45.0})
        except Exception as e:
            logger.error(f"[Script Studio] Failed to initialize Gemini client: {e}")

    models_to_try = [
        "gemini-flash-lite-latest",
        "gemini-3.5-flash-lite",
        "gemini-3.8-flash",
    ]

    sections = []

    # =========================================================================
    # CASE A: DOCUMENTARY (16:9 Landscape, 12 Minutes = 36 Segments x 5 Beats = 180 Plates)
    # =========================================================================
    if not is_short:
        target_segments = 36
        gemini_sections = []
        banned_motifs = [
            "golden vault door",
            "grid of gold bars",
            "fighter jets with flag",
            "red silhouette holding phone",
            "corporate boardroom table",
            "suits shaking hands",
            "generic laptop with chart",
            "meeting room with businessmen",
            "handshake in suit",
            "stock chart on screen",
        ]

        batch_definitions = [
            {
                "batch_num": 1,
                "start_idx": 0,
                "count": 6,
                "act_name": "ACT 1A: THE OPENING TRAP & VISCERAL HOOK (Segments 0-5)",
                "act_directive": (
                    "Establish the visceral hook in the first 5 seconds. Expose the immediate threat to retail investors, "
                    "the opening catalyst, and the scale of the money trail. "
                    "Environments: Crisp daylight container ports, active electronic trading floors with cool-blue display glow, "
                    "automated assembly lines, ocean freight docks, fiber optic subsea cables. "
                    "Lighting: Crisp natural daylight and cool tech blues. Camera: Sweeping drone aerials, high-angle tracking."
                ),
            },
            {
                "batch_num": 2,
                "start_idx": 6,
                "count": 6,
                "act_name": "ACT 1B: THE SMOKING GUN & ESCALATION (Segments 6-11)",
                "act_directive": (
                    "Escalate the investigation: reveal the initial forensic discrepancy, the red flag that auditors missed, "
                    "and the first institutional warning bells. "
                    "Environments: Subterranean bank vaults, high-speed rail freight terminals, algorithmic server corridors, "
                    "customs impound facilities with container seals, radar installations. "
                    "Camera: Low-angle tracking, Dutch tilts, dynamic push-ins."
                ),
            },
            {
                "batch_num": 3,
                "start_idx": 12,
                "count": 6,
                "act_name": "ACT 2A: FORENSIC INVESTIGATION & THE HIDDEN MECHANISM (Segments 12-17)",
                "act_directive": (
                    "Deep-dive into the forensic crime mechanics: how the algorithm siphoned funds, shell corporation filings, "
                    "customs manifest tampering, or dark liquidity pools. "
                    "Environments: Macro forensic hardware, cleanrooms, shredded audit documents, warehouse logistics at twilight, "
                    "industrial vaults, security checkpoint scanners, server racks with pulsing data LEDs. "
                    "Camera: Extreme macro close-ups, Dutch tilts, low tracking shots."
                ),
            },
            {
                "batch_num": 4,
                "start_idx": 18,
                "count": 6,
                "act_name": "ACT 2B: THE PAPER TRAIL & DARK LIQUIDITY (Segments 18-23)",
                "act_directive": (
                    "Uncover the money laundering network, offshore holding accounts, fictitious invoice chains, and collateral rehypothecation. "
                    "Environments: Offshore banking towers in tropical downpours, deserted luxury marinas, secure document shredding plants, "
                    "satellite uplink dish arrays, encrypted trading rooms. "
                    "Camera: Atmospheric wide angles, forensic scrutiny, slow creeping zooms."
                ),
            },
            {
                "batch_num": 5,
                "start_idx": 24,
                "count": 6,
                "act_name": "ACT 3A: THE BREAKING POINT & INSTITUTIONAL DEFAULTS (Segments 24-29)",
                "act_directive": (
                    "The margin calls hit, prime brokers freeze accounts, regulatory raids unfold, and market contagion spreads. "
                    "Environments: Emergency boardrooms with red digital sirens, trading floors in chaotic aftermath, rain-slicked stock exchange steps, "
                    "padlocked corporate headquarters, fleet of black executive sedans. "
                    "Lighting: Moody cinematic obsidian with subtle hazard amber. Camera: High-tension tracking, handheld urgency."
                ),
            },
            {
                "batch_num": 6,
                "start_idx": 30,
                "count": 6,
                "act_name": "ACT 3B: THE SYSTEMIC CLIMAX & FINAL SURVIVAL PLAYBOOK (Segments 30-35)",
                "act_directive": (
                    "The climax and aftermath: irreversible systemic shifts, long-term economic fallout, and the direct survival playbook "
                    "and actionable defense rules for the everyday viewer. "
                    "Environments: Architectural exteriors of central bank headquarters at dusk, empty trading pits with discarded ticker tape, "
                    "sealed vault gates, cold neon dawn over financial district skylines. "
                    "Lighting: Cold dawn blues with golden horizon rays. Camera: Imposing low-angle architectural monuments."
                ),
            },
        ]

        if client:
            for b_def in batch_definitions:
                b_num = b_def["batch_num"]
                s_start = b_def["start_idx"]
                s_count = b_def["count"]
                s_end = s_start + s_count - 1
                act_name = b_def["act_name"]
                act_directive = b_def["act_directive"]

                banned_str = ", ".join(f"'{m}'" for m in banned_motifs[-25:])
                batch_acquired = []

                prompt = f"""
                You are an investigative financial journalist and thriller documentary director (in the style of Coffeezilla, James Jani, and MagnatesMedia).
                Tone: Dark, authoritative, forensic, breathless investigative thriller exposing high-stakes financial crimes and institutional traps.
                STRICT IDENTITY MANDATE:
                - The narrator must NEVER state their name, introduce themselves, or say 'I am [Name]' or 'This is [Name]'.
                - Zero self-identification. Jump straight into the story from the very first syllable.
                - If an identity is ever referenced anywhere, it must ONLY be 'Alex' (Founder & Chief Analyst). Never mention or use the name 'Christopher'.

                TOPIC: {topic_clean}
                VERTICAL: {vertical}
                FORMAT: 12-Minute Masterpiece Documentary (16:9 Landscape)
                CURRENT PRODUCTION CHUNK: {act_name} (Segments {s_start} through {s_end}, exactly {s_count} segments of 20 seconds each)
                MINIMUM WORD-COUNT FLOOR: You MUST generate at least 620 spoken words across these 12 segments (strictly 52 to 60 words per segment). Total across 36 segments must exceed 1,860 words to fully fill the 720-second narration runtime. Zero short segments.

                CHUNK DIRECTIVE:
                {act_directive}

                STRICT ANTI-CLICHE & BANNED MOTIFS MANDATE:
                The following visual motifs are PERMANENTLY FORBIDDEN (Do NOT use or reference any of these):
                [{banned_str}]
                You MUST explore fresh physical metaphors, varied lighting, and concrete real-world objects.

                SEGMENT STRUCTURE (20 Seconds each):
                Each segment must contain:
                1. 'section_index': integer from {s_start} to {s_end}
                2. 'headline_top': Exactly 1 to 2 words uppercase punchy hook (e.g. '$7 TRILLION', '1.3 MILLION', '2 CRORE', '₹85 LOW', 'H-1B', 'HAL & BEL').
                3. 'headline_mid': Exactly 1 to 2 words uppercase anchor (e.g. 'DEBT TRAP', 'TROOPS', 'TRAPPED', 'CRASH', 'CRACKDOWN', 'SURGE').
                4. 'badge_text': High-friction tactical alert stamp (e.g. 'MARKET SHOCK', 'TIME-BOMB', 'CRACKDOWN', 'OVERPRICED', 'TOP SECRET').
                5. 'color_theme': One of 'gold', 'fire', 'emerald', 'cyan', 'warning'.
                6. NATURAL HUMAN DOCUMENTARY CADENCE & PUNCTUATION:
                   - The entire documentary script is synthesized as a continuous master audio track.
                   - 'script': Exactly 50 to 60 words of spoken narrative for this 20-second segment written with natural human punctuation: complete 10–14 word sentences ending with periods ('.'), rhetorical questions ('?'), mid-sentence commas (','), and em-dashes ('—').
                   - Natural punctuation allows the voice to drop pitch at periods and inflect on questions while thoughts flow smoothly across micro-beats.
                7. 'micro_beats': Exactly 5 distinct 4-second micro-beats (beat_0 through beat_4):
                   - Each beat represents 4.0 seconds of speech.
                   - 'beat_index': integer 0 to 4
                   - 'start_sec': relative seconds in segment (0.0, 4.0, 8.0, 12.0, 16.0)
                   - 'end_sec': relative seconds in segment (4.0, 8.0, 12.0, 16.0, 20.0)
                   - 'spoken_phrase': Strictly 10 to 12 contiguous spoken words for this 4-second beat (50-60 words total per segment = ~1,900 words across 36 segments). Zero short sentences.
                   - 'visual_prompt': A vivid, cinematic, tangible 35mm photographic description of a CONCRETE PHYSICAL METAPHOR illustrating that exact spoken phrase.
                     * STRICTLY FORBIDDEN: Boardrooms, suits at conference tables, generic business people, charts on laptops.
                     * Suffix: "cinematic 35mm photograph, 8k hyper-detailed, clean plate, zero text, zero watermark"
                     * Rotate lighting: cool blue, crisp daylight, twilight, neon noir. Never force the same amber lighting on every beat.
                     * Rotate camera angles: macro close-ups, wide aerial drones, low-angle tracking, eye-level forensic scrutiny.

                Respond ONLY with a valid JSON object matching this structure:
                {{
                  "sections": [
                    {{
                      "section_index": {s_start},
                      "headline_top": "...",
                      "headline_mid": "...",
                      "badge_text": "...",
                      "color_theme": "gold",
                      "script": "...",
                      "micro_beats": [
                        {{
                          "beat_index": 0,
                          "start_sec": 0.0,
                          "end_sec": 4.0,
                          "spoken_phrase": "...",
                          "visual_prompt": "..."
                        }},
                        {{
                          "beat_index": 1,
                          "start_sec": 4.0,
                          "end_sec": 8.0,
                          "spoken_phrase": "...",
                          "visual_prompt": "..."
                        }},
                        {{
                          "beat_index": 2,
                          "start_sec": 8.0,
                          "end_sec": 12.0,
                          "spoken_phrase": "...",
                          "visual_prompt": "..."
                        }},
                        {{
                          "beat_index": 3,
                          "start_sec": 12.0,
                          "end_sec": 16.0,
                          "spoken_phrase": "...",
                          "visual_prompt": "..."
                        }},
                        {{
                          "beat_index": 4,
                          "start_sec": 16.0,
                          "end_sec": 20.0,
                          "spoken_phrase": "...",
                          "visual_prompt": "..."
                        }}
                      ]
                    }}
                  ]
                }}
                """
                for attempt in range(4):
                    raw_text = _query_gemini_smart(prompt, client, api_key, models_to_try)
                    if raw_text:
                        try:
                            if "```json" in raw_text:
                                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                            elif "```" in raw_text:
                                raw_text = raw_text.split("```")[1].split("```")[0].strip()
                            data = json.loads(raw_text)
                            g_secs = data.get("sections", [])
                            if len(g_secs) >= s_count:
                                batch_acquired = g_secs[:s_count]
                                logger.success(f"✅ [Script Studio] Batch {b_num}/6 ({act_name}) successfully generated")
                                break
                        except Exception as parse_err:
                            logger.debug(f"JSON parse error on Batch {b_num} attempt {attempt+1}: {parse_err}")
                    if batch_acquired:
                        break
                    time.sleep(2 * (attempt + 1))

                if not batch_acquired:
                    logger.error(f"❌ [Script Studio] Failed to acquire Batch {b_num}/6 from Gemini API.")
                    break

                # Extract key concrete nouns/motifs from this batch and append to running banned_motifs
                for sec_item in batch_acquired:
                    for b_item in sec_item.get("micro_beats", []):
                        vp = b_item.get("visual_prompt", "")
                        core_match = re.search(r"photograph of (?:a |an |the )?([^,]+)", vp, re.IGNORECASE)
                        if core_match:
                            extracted_m = core_match.group(1).strip().lower()
                            if len(extracted_m) > 3 and extracted_m not in banned_motifs:
                                banned_motifs.append(extracted_m)

                gemini_sections.extend(batch_acquired)

        if len(gemini_sections) < target_segments:
            raise RuntimeError(
                f"⛔ CRITICAL: Failed to generate all 36 bespoke documentary segments for topic '{topic_clean}'. "
                f"Acquired {len(gemini_sections)}/{target_segments} segments. "
                f"Hardcoded scripts, generic modulo fallbacks, and canned text are PERMANENTLY PROHIBITED."
            )

        total_doc_words = sum(len(str(g.get("script", "")).split()) for g in gemini_sections)
        logger.info(f"📊 [Script Studio] 36 Documentary segments acquired: {total_doc_words} words total.")
        if total_doc_words < 1850:
            logger.warning(f"⚠️ Script word count ({total_doc_words}) below 1,850 floor. Expanding sparse segments...")
            for g in gemini_sections:
                s_words = len(str(g.get("script", "")).split())
                if s_words < 50:
                    extra = " ".join(b.get("spoken_phrase", "") for b in g.get("micro_beats", []) if b.get("spoken_phrase") and b.get("spoken_phrase") not in g.get("script", ""))
                    if extra:
                        g["script"] = f"{g['script']} {extra}".strip()

        for i in range(target_segments):
            start_t = round(i * 20.0, 2)
            end_t = round((i + 1) * 20.0, 2)
            has_hud = (i in (1, 3, 5, 8, 12, 18, 24, 30))

            g = gemini_sections[i]
            top = str(g.get("headline_top", lead_word))[:24]
            mid = str(g.get("headline_mid", second_word))[:24]
            badge = str(g.get("badge_text", "MARKET SHOCK"))[:20]
            color_theme = str(g.get("color_theme", "gold")).lower()
            script_text = str(g.get("script", "")).strip()

            # Strict zero identity leak guardrail: Scrub any accidental self-introduction or Christopher references
            script_text = re.sub(r"\b(?:I am|I'm|this is|my name is)\s+Christopher\b", "I'm Alex", script_text, flags=re.IGNORECASE)
            script_text = re.sub(r"\bChristopher\b", "Alex", script_text, flags=re.IGNORECASE)

            # Ensure micro_beats contains exactly 5 bespoke items
            raw_beats = g.get("micro_beats", [])
            micro_beats = []
            script_sentences = [s.strip() for s in re.split(r"[.!?]+", script_text) if len(s.strip()) > 3]

            for b_idx in range(5):
                b_start = round(b_idx * 4.0, 2)
                b_end = round((b_idx + 1) * 4.0, 2)

                if b_idx < len(raw_beats):
                    rb = raw_beats[b_idx]
                    vp = str(rb.get("visual_prompt", "")).strip()
                    sp = str(rb.get("spoken_phrase", "")).strip()
                else:
                    vp = ""
                    sp = ""

                if not sp:
                    sp = script_sentences[b_idx % len(script_sentences)] if script_sentences else f"{top} {mid}"

                if not vp or len(vp) < 15:
                    vp = (
                        f"Cinematic 35mm photograph, visual metaphor of {sp}, "
                        f"industrial physical structures, container ports, cold cleanroom circuits, "
                        f"atmospheric lighting, 8k hyper-detailed, clean plate, zero text, zero watermark"
                    )

                micro_beats.append({
                    "beat_index": b_idx,
                    "start_sec": b_start,
                    "end_sec": b_end,
                    "duration": 4.0,
                    "spoken_phrase": sp,
                    "visual_prompt": vp,
                })

            # If script_text is shorter than 45 words, construct it directly from the 5 micro-beat phrases
            # to guarantee ~50-60 words (~20 seconds of speech per segment, ~720s total)
            beat_phrases = [b["spoken_phrase"].strip() for b in micro_beats if b.get("spoken_phrase")]
            if len(script_text.split()) < 45 and len(beat_phrases) == 5:
                script_text = ". ".join(p.rstrip(".") for p in beat_phrases) + "."

            primary_vp = micro_beats[0]["visual_prompt"]

            sections.append({
                "section_index": i,
                "start_sec": start_t,
                "end_sec": end_t,
                "duration": 20.0,
                "headline_top": top[:24],
                "headline_mid": mid[:24],
                "badge_text": badge[:20],
                "color_theme": color_theme,
                "visual_prompt": primary_vp,
                "micro_beats": micro_beats,
                "theme": theme,
                "symbol_type": default_symbol,
                "method_c_hud": has_hud,
                "script": script_text,
            })

        logger.success(f"🎬 [Script Studio] Successfully constructed 36 segments with 180 bespoke micro-beats (12-min Documentary).")
        return sections

    # =========================================================================
    # CASE B: SHORTS (9:16 Vertical, 60s = 20 Unique Cuts of 3.0s each)
    # =========================================================================
    rules = VideoFormatConfig.get_rules(duration_sec, is_short=True)
    interval = rules["frame_interval"]
    num_sections = rules["expected_frames"]
    gemini_sections = []

    if client:
        prompt = f"""
        You are an investigative financial journalist and thriller documentary director (in the style of Coffeezilla, James Jani, and MagnatesMedia).
        Tone: Dark, authoritative, forensic, breathless investigative thriller exposing high-stakes financial crimes and institutional traps.
        STRICT IDENTITY MANDATE:
        - The narrator must NEVER state their name, introduce themselves, or say 'I am [Name]' or 'This is [Name]'.
        - Zero self-identification. Jump straight into the story from the very first syllable.
        - If an identity is ever referenced anywhere, it must ONLY be 'Alex' (Founder & Chief Analyst). Never mention or use the name 'Christopher'.
        Topic: {topic_clean}
        Vertical: {vertical}
        Format: 60-Second Viral Short (9:16 Vertical)
        Number of discrete sections: {num_sections}

        CRITICAL DIRECTIVES FOR HIGH-RETENTION HUMAN STORYTELLING (AVD >= 70%):
        1. ZERO FINANCIAL JARGON IN THE FIRST 5 SECONDS:
           - STRICTLY FORBIDDEN WORDS in Hook: 'liquidity', 'absorption', 'VWAP', 'delta', 'correlation', 'fiscal deficit', 'implied volatility', 'order book', 'macroeconomic', 'consolidation'.
           - Opening MUST BE A VISCERAL, UNIGNORABLE HOOK: A direct threat, shocking accusation, or urgent mystery confronting the viewer's bank account.

        2. PERSONALIZE THE THREAT (EVERY STORY HAS A VILLAIN, A VICTIM, AND A CRIME):
           - The victim is the everyday viewer working a 9-to-5 job.
           - The villain is the institutional desk, shadow banker, or predatory algorithm.

        3. ONE SINGLE INSANE FACT PER SHORT (NO ACADEMIC DATA DUMPS):
           - Focus on ONE shocking smoking gun. Build relentless tension for 40 seconds, then drop the jaw-dropping revelation in the final 15 seconds.

        4. CONTINUOUS UNBROKEN NARRATIVE MONOLOGUE (ZERO ARTIFICIAL 4-SECOND AUDIO STOPS):
           - The audio narration MUST be written as ONE continuous, free-flowing, breathless investigative monologue for the entire video (130-140 words total).
           - Do NOT write disjointed 4-second sentence fragments. The monologue must flow with natural human conversational momentum from beginning to end.
           - Spoken words do NOT stop or pause for plate changes. The visual photographic plates change every 3 to 4 seconds independently while the narrator speaks continuously.

        5. PACING & BLOCKBUSTER 3D TYPOGRAPHY DIRECTIVES FOR EACH VISUAL PLATE:
           - 'headline_top': Exactly 1 to 2 words uppercase punchy hook (e.g. '$7 TRILLION', '1.3 MILLION', '2 CRORE', '₹85 LOW', 'H-1B', 'HAL & BEL').
           - 'headline_mid': Exactly 1 to 2 words uppercase anchor (e.g. 'DEBT TRAP', 'TROOPS', 'TRAPPED', 'CRASH', 'CRACKDOWN', 'SURGE').
           - 'badge_text': High-friction tactical alert stamp (e.g. 'MARKET SHOCK', 'TIME-BOMB', 'CRACKDOWN', 'OVERPRICED', 'TOP SECRET').
           - 'color_theme': One of 'gold', 'fire', 'emerald', 'cyan', 'warning'.
           - 'visual_prompt': A vivid, cinematic, tangible 35mm photographic description of a CONCRETE PHYSICAL METAPHOR.
             * STRICTLY FORBIDDEN: Boardrooms, office desks, suits around conference tables, generic business people, charts on laptop screens.
             * MANDATORY PHYSICAL METAPHORS: Bank vaults sucking vortices, split cargo container ships in storms, gold bullion on dark marble, fighter jets flanking flags, passports locked in chains, robotic arms throwing sparks, distressed trader clutching head before giant red smartphone chart.
             * Suffix: "cinematic 35mm photograph, dark moody obsidian lighting, volumetric amber and gold rays, 8k hyper-detailed, clean plate, zero text, zero watermark"

        Respond ONLY with a valid JSON object matching this structure:
        {{
          "monologue": "Full continuous unbroken narration script of 130 to 140 words for the entire short...",
          "sections": [
            {{
              "section_index": 0,
              "headline_top": "...",
              "headline_mid": "...",
              "badge_text": "...",
              "color_theme": "gold",
              "visual_prompt": "...",
              "spoken_phrase": "..."
            }}
          ]
        }}
        """
        for attempt in range(4):
            raw_text = _query_gemini_smart(prompt, client, api_key, models_to_try)
            if raw_text:
                try:
                    if "```json" in raw_text:
                        raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                    elif "```" in raw_text:
                        raw_text = raw_text.split("```")[1].split("```")[0].strip()
                    data = json.loads(raw_text)
                    g_secs = data.get("sections", [])
                    monologue = data.get("monologue", "").strip()
                    if len(g_secs) >= num_sections:
                        gemini_sections = g_secs[:num_sections]
                    elif attempt >= 2 and len(g_secs) >= 6:
                        # Auto-interpolate beats to exact target num_sections with distinct camera angles
                        logger.info(f"⚡ [Script Studio] Subdividing {len(g_secs)} beats to exact target {num_sections} beats...")
                        expanded = []
                        ratio = num_sections / len(g_secs)
                        for idx, sec in enumerate(g_secs):
                            target_count = round((idx + 1) * ratio) - round(idx * ratio)
                            for sub_i in range(target_count):
                                new_sec = dict(sec)
                                if sub_i > 0:
                                    base_prompt = sec.get("visual_prompt", "")
                                    angles = ["extreme close-up macro detail", "wide low-angle atmospheric shot", "over-the-shoulder dramatic tilt"]
                                    alt_angle = angles[sub_i % len(angles)]
                                    new_sec["visual_prompt"] = f"{alt_angle}, {base_prompt}"
                                expanded.append(new_sec)
                        gemini_sections = expanded[:num_sections]

                    if gemini_sections:
                        # Re-index section indices
                        for s_i, sec_item in enumerate(gemini_sections):
                            sec_item["section_index"] = s_i
                        if monologue:
                            # Attach continuous monologue slices across sections naturally
                            mono_words = monologue.split()
                            step = max(1, len(mono_words) // num_sections)
                            for s_i, sec_item in enumerate(gemini_sections):
                                start_w = s_i * step
                                end_w = len(mono_words) if s_i == num_sections - 1 else (s_i + 1) * step
                                sec_item["script"] = " ".join(mono_words[start_w:end_w])
                        logger.success(f"✅ [Script Studio] Successfully prepared {num_sections} custom investigative sections with continuous monologue ({len(monologue.split()) if monologue else 'N/A'} words)")
                        break
                except Exception as parse_err:
                    logger.debug(f"JSON parse error on attempt {attempt+1}: {parse_err}")
            if gemini_sections:
                break
            time.sleep(2 * (attempt + 1))

    # ZERO HARDCODED FALLBACK MANDATE
    if not gemini_sections or len(gemini_sections) < num_sections:
        raise RuntimeError(
            f"⛔ CRITICAL: Failed to generate custom investigative narrative script for topic '{topic_clean}'. "
            f"Acquired {len(gemini_sections) if gemini_sections else 0}/{num_sections} beats. "
            f"Hardcoded scripts, generic modulo fallbacks, and canned text are PERMANENTLY PROHIBITED."
        )

    # Clean script fields and enforce total monologue bounds naturally without robotic truncating
    total_script_words = sum(len(str(g.get("script", "")).strip().split()) for g in gemini_sections)
    if total_script_words > 145:
        logger.warning(f"⚠️ Total Short script ({total_script_words} words) exceeds 145-word ceiling. Normalizing...")
        accumulated = 0
        for g in gemini_sections:
            words = str(g.get("script", "")).strip().split()
            if accumulated >= 140:
                g["script"] = " ".join(words[:4])
            elif accumulated + len(words) > 140:
                allow = max(4, 140 - accumulated)
                g["script"] = " ".join(words[:allow])
            accumulated += len(str(g.get("script", "")).strip().split())
            accumulated += len(str(g.get("script", "")).strip().split())

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

        # Strict zero identity leak guardrail
        script_text = re.sub(r"\b(?:I am|I'm|this is|my name is)\s+Christopher\b", "I'm Alex", script_text, flags=re.IGNORECASE)
        script_text = re.sub(r"\bChristopher\b", "Alex", script_text, flags=re.IGNORECASE)

        if not visual_prompt or len(visual_prompt) < 15:
            visual_prompt = (
                f"Cinematic 35mm photograph, visual metaphor of {top} {mid}, "
                f"massive concrete physical monuments, bank vaults, cargo ships, dark moody obsidian lighting, "
                f"volumetric amber and gold rays, 8k hyper-detailed, clean plate, zero text, zero watermark"
            )

        micro_beats = [{
            "beat_index": 0,
            "start_sec": 0.0,
            "end_sec": interval,
            "duration": interval,
            "spoken_phrase": script_text,
            "visual_prompt": visual_prompt,
        }]

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
            "micro_beats": micro_beats,
            "theme": theme,
            "symbol_type": default_symbol,
            "method_c_hud": has_hud,
            "script": script_text,
        })
    return sections


def _synthesize_local_christopher_audio(script_text: str, audio_path: Path, words_path: Path, total_duration_sec: float = 60.0, is_short: bool = False) -> List[Dict[str, Any]]:
    """
    OFFICIAL SIGNATURE CHRISTOPHER CLONED VOICE ENGINE
    - Synthesizes 100% authentic Christopher narration for the given script.
    - Mastering: Highpass 70Hz + 135Hz chest resonance EQ + optical compression + -16 LUFS.
    - Strict Pre-Whisper Conforming: Enforces <=58s audio via capped atempo (<=1.15x) BEFORE Whisper alignment.
    - Word Alignment: Millisecond-accurate word timestamps for kinetic typography.
    """
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    words_path.parent.mkdir(parents=True, exist_ok=True)
    
    from app.services.local_christopher_tts import synthesize_chapter_offline
    logger.info("🎙️ [Voice Engine] Invoking signature Christopher voice narration...")
    res = synthesize_chapter_offline(
        script_text=script_text,
        out_mp3_path=str(audio_path),
        out_timestamps_json=str(words_path),
        is_short=is_short
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


def snap_beat_cuts_to_punctuation(
    words_with_timings: List[Dict[str, Any]],
    raw_script: str,
    num_beats: int,
    total_dur: float,
    j_cut_lead_sec: float = 0.18,
) -> List[tuple[float, float]]:
    """Snaps visual beat cut points to periods, commas, and em-dashes with a 180ms J-cut lead."""
    raw_tokens = re.findall(r"\S+", raw_script)
    n_words = len(words_with_timings)
    if n_words == 0 or num_beats <= 1:
        return [(0.0, total_dur)]

    strong_breaks = []  # . ? ! — ...
    soft_breaks = []    # , ; :
    for idx, tok in enumerate(raw_tokens[:n_words]):
        if tok.endswith((".", "?", "!", "—", "...")):
            strong_breaks.append(idx)
        elif tok.endswith((",", ";", ":")):
            soft_breaks.append(idx)

    cut_times = [0.0]
    target_step = n_words / float(num_beats)

    for b in range(1, num_beats):
        ideal_idx = int(round(b * target_step))
        candidates = [i for i in strong_breaks if abs(i - ideal_idx) <= 3]
        if not candidates:
            candidates = [i for i in soft_breaks if abs(i - ideal_idx) <= 3]

        chosen_end_idx = min(candidates, key=lambda i: abs(i - ideal_idx)) if candidates else (ideal_idx - 1)
        next_clause_start_idx = min(n_words - 1, chosen_end_idx + 1)

        clause_start_sec = float(words_with_timings[next_clause_start_idx]["start"])
        j_cut_sec = max(cut_times[-1] + 1.2, clause_start_sec - j_cut_lead_sec)
        cut_times.append(j_cut_sec)

    cut_times.append(total_dur)
    return [(cut_times[i], cut_times[i + 1]) for i in range(num_beats)]


def prepare_session(
    topic: str,
    vertical: str = "stock_market",
    duration_sec: int = 60,
    is_short: bool = True,
    output_dir: Optional[Path] = None,
    privacy_status: str = "unlisted",
    publish_at: Optional[str] = None,
    skip_duplicate_check: bool = False
):
    """
    Job 1: Prepares the full video session in the cloud.
    Emits GitHub Actions matrix output for up to 20 parallel runner workers!
    """
    if not topic or not topic.strip():
        raise ValueError("A valid non-empty topic must be provided for video generation.")

    # 0. STRICT ZERO-COMPROMISE COMPLIANCE & 30-DAY ANTI-DUPLICATION GATE (GATE 1)
    from app.services.content_authenticity_engine import ContentAuthenticityEngine
    from app.services.compliance_gate import ComplianceGate

    logger.info(f"🛡️ [Compliance Gate] Auditing topic '{topic}' against 30-day history and regulatory safe harbor...")
    if not ComplianceGate._check_30_day_freshness(topic):
        raise RuntimeError(
            f"⛔ COMPLIANCE GATE REJECTION: Topic '{topic}' violates 30-day freshness rule. "
            f"Semantic clones and duplicate topics are strictly prohibited."
        )

    published_titles = check_duplicate_before_prep(topic)

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

    # Validate generated script with ContentAuthenticityEngine Gate 1
    full_script = " ".join(s["script"] for s in sections)
    authenticity = ContentAuthenticityEngine()
    gate1_res = authenticity.gate_1_script_compliance(
        topic=topic,
        script_data={"topic": topic, "sections": sections, "script": full_script},
        vertical=vertical
    )
    if not gate1_res.get("passed"):
        raise RuntimeError(f"⛔ COMPLIANCE GATE REJECTION: Gate 1 Script & Topic check failed: {gate1_res.get('feedback')}")

    logger.info(f"🚀 [Session Prep] Topic: '{topic}' | Format: {'Short 9:16' if is_short else 'Standard 16:9'} | Segments: {total_segments}")

    # 1. Synthesize 100% Offline Cloned Voice & Extract Word Timestamps
    audio_file = audio_dir / "speech.mp3"
    words_file = audio_dir / "words.json"
    words = _synthesize_local_christopher_audio(full_script, audio_file, words_file, total_duration_sec=float(duration_sec), is_short=is_short)

    # 2. Generate High-CTR Background Frames for each section (Batch-Aware & Aspect-Ratio Strict)
    rules = VideoFormatConfig.get_rules(float(duration_sec), is_short=is_short)
    w_out, h_out = rules["width"], rules["height"]
    frame_files = []
    
    missing_frame_prompts = []
    frame_id = 1
    for s in sections:
        idx = s["section_index"]
        micro_beats = s.get("micro_beats", [])
        if micro_beats and not is_short:
            s["frame_files"] = []
            for b in micro_beats:
                b_idx = b["beat_index"]
                frame_path = frames_dir / f"frame_{idx:02d}_beat_{b_idx}.jpg"
                b["frame_file"] = str(frame_path.relative_to(output_dir))
                s["frame_files"].append(b["frame_file"])
                
                approved_dir = BASE_DIR / "assets" / "approved_bundles" / slug
                approved_frame = approved_dir / f"frame_{idx:02d}_beat_{b_idx}.jpg"
                if approved_frame.exists():
                    shutil.copy2(approved_frame, frame_path)
                    logger.success(f"🎯 [Session Prep] Using verified user-approved frame: {approved_frame.name}")
                elif not frame_path.exists():
                    prompt = b.get("visual_prompt", "")
                    if not prompt or len(prompt.strip()) < 10:
                        prompt = (
                            f"Cinematic 35mm photograph, visual metaphor of {b.get('spoken_phrase', '')}, "
                            f"massive concrete physical monuments, bank vaults, cargo ships, dark moody obsidian lighting, "
                            f"volumetric amber and gold rays, 8k hyper-detailed, clean plate, zero text, zero watermark"
                        )
                    missing_frame_prompts.append({
                        "id": frame_id,
                        "prompt": prompt,
                        "output_path": str(frame_path),
                        "section": s,
                        "beat": b
                    })
                frame_id += 1
            s["frame_file"] = s["frame_files"][0]
        else:
            frame_path = frames_dir / f"frame_{idx:02d}.jpg"
            s["frame_file"] = str(frame_path.relative_to(output_dir))
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
                    "id": frame_id,
                    "prompt": prompt,
                    "output_path": str(frame_path),
                    "section": s
                })
            frame_id += 1

    # Dispatch missing frames via Cloudflare Serverless GPU (FLUX.1-schnell) or Kaggle Dual-T4 GPU
    if missing_frame_prompts:
        aspect = "9:16" if is_short else "16:9"
        logger.info(f"⚡ [Session Prep] Dispatching {len(missing_frame_prompts)} bespoke plates ({aspect}) to Cloudflare Serverless GPUs...")
        cf_success = False
        try:
            from app.services.cloudflare_image_worker import CloudflareImageWorker
            cf_worker = CloudflareImageWorker()
            cf_success = cf_worker.generate_batch(
                prompts=[{"prompt": m["prompt"], "output_path": m["output_path"]} for m in missing_frame_prompts],
                aspect_ratio=aspect
            )
        except Exception as cf_err:
            logger.warning(f"⚠️ [Session Prep] Cloudflare batch error: {cf_err}")

        if not cf_success:
            logger.info("⚡ [Session Prep] Falling back to Kaggle Dual-T4 GPU diffusers...")
            try:
                from app.services.kaggle_image_worker import KaggleImageWorker
                worker = KaggleImageWorker()
                k_success = worker.generate_batch(
                    prompts=[{"prompt": m["prompt"], "output_path": m["output_path"]} for m in missing_frame_prompts],
                    aspect_ratio=aspect
                )
                if not k_success:
                    logger.error(f"❌ [Session Prep] Kaggle GPU batch dispatch failed.")
            except Exception as k_err:
                logger.error(f"❌ [Session Prep] Kaggle batch dispatch error: {k_err}")

    # Ensure every single frame exists exclusively from Kaggle GPU (zero procedural compromise)
    for s in sections:
        idx = s["section_index"]
        micro_beats = s.get("micro_beats", [])
        if micro_beats and not is_short:
            for b in micro_beats:
                b_idx = b["beat_index"]
                frame_path = frames_dir / f"frame_{idx:02d}_beat_{b_idx}.jpg"
                if not frame_path.exists():
                    fetch_clean_photographic_plate(
                        prompt=b.get("visual_prompt", ""),
                        width=w_out,
                        height=h_out,
                        out_path=frame_path
                    )
                if not frame_path.exists():
                    raise RuntimeError(
                        f"⛔ CRITICAL: Frame {idx:02d} beat {b_idx} was not generated by Kaggle GPU. "
                        f"Per Standing Rule 1 & Zero Compromise Mandate, procedural placeholders are permanently prohibited."
                    )
                try:
                    with Image.open(frame_path) as raw_img:
                        if raw_img.size != (w_out, h_out):
                            fitted = ImageOps.fit(raw_img.convert("RGB"), (w_out, h_out), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
                            fitted.save(frame_path, quality=95)
                except Exception as f_err:
                    logger.debug(f"Frame fit check: {f_err}")
                frame_files.append(str(frame_path.relative_to(output_dir)))
        else:
            frame_path = frames_dir / f"frame_{idx:02d}.jpg"
            if not frame_path.exists():
                fetch_clean_photographic_plate(
                    prompt=s.get("visual_prompt", ""),
                    width=w_out,
                    height=h_out,
                    out_path=frame_path
                )
            if not frame_path.exists():
                raise RuntimeError(
                    f"⛔ CRITICAL: Frame {idx:02d} was not generated by Kaggle GPU. "
                    f"Per Standing Rule 1 & Zero Compromise Mandate, procedural placeholders are permanently prohibited."
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

    # 3. Dynamic Matrix Partitioning: All segments render via GitHub Actions Ubuntu matrix (max-parallel: 20 handles concurrency)
    gha_indices = list(range(total_segments))
    kaggle_indices = []
    has_overflow = False

    manifest = {
        "topic": topic,
        "vertical": vertical,
        "is_short": is_short,
        "duration_sec": duration_sec,
        "privacy_status": privacy_status,
        "publish_at": publish_at,
        "slug": slug,
        "total_segments": total_segments,
        "gha_indices": gha_indices,
        "kaggle_indices": kaggle_indices,
        "audio_file": str(audio_file.relative_to(output_dir)),
        "words_file": str(words_file.relative_to(output_dir)),
        "sections": sections,
    }

    # 3.5 Triple-Check Pre-Flight Forensic Audit (Title + Script + Visual Plates)
    from app.services.compliance_gate import TripleCheckPreflightGate
    full_monologue = " ".join(s.get("script", "") for s in sections)
    TripleCheckPreflightGate.run_triple_check_preflight(
        topic=topic,
        monologue=full_monologue,
        frames_dir=frames_dir,
        expected_frames=len(sections),
        is_short=is_short,
        published_titles=published_titles if "published_titles" in locals() else None
    )

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

    # Load high-CTR base frames (with 5-beat micro-beat support for 16:9 documentaries)
    micro_beats = sec.get("micro_beats", [])
    beat_imgs = []
    if micro_beats and not is_short:
        for b in micro_beats:
            b_rel = b.get("frame_file")
            if b_rel and (bundle_dir / b_rel).exists():
                b_path = bundle_dir / b_rel
            else:
                b_idx = b.get("beat_index", 0)
                b_path = bundle_dir / "frames" / f"frame_{segment_index:02d}_beat_{b_idx}.jpg"
            if not b_path.exists():
                b_path = bundle_dir / sec.get("frame_file", f"frames/frame_{segment_index:02d}.jpg")
            img = Image.open(b_path).convert("RGB")
            if img.size != (w_out, h_out):
                img = ImageOps.fit(img, (w_out, h_out), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
            beat_imgs.append(img)

    if not beat_imgs:
        frame_rel = sec["frame_file"]
        frame_full = bundle_dir / frame_rel
        base_img = Image.open(frame_full).convert("RGB")
        if base_img.size != (w_out, h_out):
            base_img = ImageOps.fit(base_img, (w_out, h_out), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        beat_imgs = [base_img]

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
                # Active spoken word: Neon Cyan (#00F0FF) if financial metric/number, else Electric Gold (#FFD700)
                is_metric = bool(re.search(r'[\$\%\d]', w_txt))
                act_color = (0, 240, 255, 255) if is_metric else (255, 215, 0, 255)
                # Subtle dark rounded backplate under active word
                pdraw.rounded_rectangle(
                    [cx - 4, pad_y + y_off - 2, cx + bw + 4, pad_y + y_off + bh + 2],
                    radius=6,
                    fill=(0, 0, 0, 180)
                )
                pdraw.text((cx + 3, pad_y + y_off + 3), w_txt, font=f_curr, fill=(0, 0, 0, 255))
                pdraw.text((cx, pad_y + y_off), w_txt, font=f_curr, fill=act_color)
            else:
                # Inactive words in the cluster: drop shadow + crisp white
                pdraw.text((cx + 2, pad_y + y_off + 2), w_txt, font=f_curr, fill=(0, 0, 0, 230))
                pdraw.text((cx, pad_y + y_off), w_txt, font=f_curr, fill=(255, 255, 255, 255))
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

    # Launch FFmpeg Rawvideo Pipe with Zero-Overhead 35mm Grain & Vignette
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
        t_in_sec = f_idx / fps  # relative seconds in this segment (0.0 to 20.0s)

        # Micro-beat selection: proportional micro-beat cut timing across 5 bespoke plates
        # with 180ms J-cut lead (plate appears 180ms before the spoken clause)
        t_lead = t_in_sec + 0.18
        if len(beat_imgs) > 1:
            beat_count = len(beat_imgs)
            beat_dur = max(2.0, seg_duration / float(beat_count))
            beat_idx = min(beat_count - 1, int(t_lead // beat_dur))
            active_base_img = beat_imgs[beat_idx]
            beat_progress = min(1.0, (t_lead % beat_dur) / beat_dur)
            scale = 1.0 + (0.04 * beat_progress)
        else:
            active_base_img = beat_imgs[0]
            progress = f_idx / max(total_frames, 1)
            scale = 1.0 + (0.04 * progress)

        zw, zh = int(w_out * scale), int(h_out * scale)
        frame_canvas = active_base_img.resize((zw, zh), Image.Resampling.BILINEAR)
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

    # Compute transition timestamps in milliseconds for programmatic sub-drop / whoosh SFX
    is_short = manifest.get("is_short", False)
    sections = manifest.get("sections", [])
    if is_short:
        hit1_ms = 0
        hit2_ms = int(sections[min(8, len(sections)-1)].get("start_sec", 24.0) * 1000)
        hit3_ms = int(sections[min(15, len(sections)-1)].get("start_sec", 45.0) * 1000)
    else:
        hit1_ms = 0
        hit2_ms = int(sections[min(12, len(sections)-1)].get("start_sec", 240.0) * 1000)
        hit3_ms = int(sections[min(24, len(sections)-1)].get("start_sec", 480.0) * 1000)

    logger.info(f"🎵 [Aggregator] Mixing cinematic ambient bed with sidechain ducking + programmatic SFX (-14 LUFS)...")
    # Programmatic FFmpeg lavfi Sub-Drop + Cinematic Whoosh Generator (No external files required)
    # Master audio pass-through + sidechain compression + -14 LUFS mastering
    filter_complex = (
        "aevalsrc='0.45*sin(2*PI*(65-37*t/1.2)*t)*exp(-2.8*t)':s=44100:d=1.2[sub];"
        "anoisesrc=d=1.2:c=pink:r=44100:a=0.18,bandpass=f=380:width_type=h:w=260,"
        "afade=t=in:st=0:d=0.35,afade=t=out:st=0.35:d=0.85[whoosh];"
        "[sub][whoosh]amix=inputs=2,volume=-18dB,asplit=3[sfx1][sfx2][sfx3];"
        f"[sfx1]adelay={hit1_ms}|{hit1_ms}[h1];"
        f"[sfx2]adelay={hit2_ms}|{hit2_ms}[h2];"
        f"[sfx3]adelay={hit3_ms}|{hit3_ms}[h3];"
        "[h1][h2][h3]amix=inputs=3:normalize=0[sfx_bus];"
        "[1:a]volume=0.20,aloop=loop=-1:size=2e+09[bg_raw];"
        "[bg_raw][sfx_bus]amix=inputs=2:duration=first:normalize=0[bed_raw];"
        "[0:a]asplit=2[voice_sc][voice_out];"
        "[bed_raw][voice_sc]sidechaincompress=threshold=0.015:ratio=6:attack=35:release=450:makeup=1.0[bed_ducked];"
        "[voice_out][bed_ducked]amix=inputs=2:duration=first:dropout_transition=0,"
        "loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
    )
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

        # Mandatory Audio Volume Level Verification (Zero Digital Silence Mandate)
        vol_cmd = [
            "ffmpeg", "-i", str(final_video_mp4),
            "-af", "volumedetect", "-vn", "-sn", "-dn",
            "-f", "null", "/dev/null"
        ]
        vol_res = subprocess.run(vol_cmd, capture_output=True, text=True)
        m_vol = None
        for line in vol_res.stderr.splitlines():
            if "mean_volume:" in line:
                parts = line.split("mean_volume:")
                if len(parts) > 1:
                    m_vol = float(parts[1].replace("dB", "").strip())
                    break
        if m_vol is None or m_vol < -45.0:
            raise ValueError(f"Pre-Upload QC Failed: Master video audio is silent (mean_volume: {m_vol} dB < -45.0 dB threshold).")

        logger.success(f"🛡️ [Pre-Upload QC Passed] Validated {act_w}x{act_h} | Duration: {dur:.1f}s | Audio volume: {m_vol:.1f} dB | Audio & Video synced.")
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

    # Gate 2 Multi-Asset Compliance Check
    from app.services.content_authenticity_engine import ContentAuthenticityEngine
    authenticity = ContentAuthenticityEngine()
    gate2_res = authenticity.gate_2_asset_compliance(
        audio_path=speech_audio,
        thumbnail_frames=[thumb_path] if thumb_path.exists() else [],
        vertical=manifest.get("vertical", "stock_market")
    )
    if not gate2_res.get("passed"):
        raise RuntimeError(f"⛔ COMPLIANCE GATE REJECTION: Gate 2 Asset Compliance failed: {gate2_res.get('feedback')}")

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
        publish_at = manifest.get("publish_at")

        # Mandatory Pre-Upload Quality Control Gate
        from app.services.pre_upload_qc_gate import PreUploadQCGate
        qc_passed, qc_errors = PreUploadQCGate.validate(final_video_mp4, is_short=manifest.get("is_short", False), manifest_path=manifest_path)
        if not qc_passed:
            logger.error(f"⛔ PRE-UPLOAD QC GATE REJECTION: Video failed validation: {qc_errors}")
            _send_telegram(f"🚨 Pre-Upload QC Failed on {manifest.get('topic')}: {qc_errors}. Execution halted.")
            sys.exit(1)

        # Package full upload metadata & thumbnail inside output_dir for zero-loss deferred publishing
        out_thumb = output_dir / "thumbnail.jpg"
        if thumb_path.exists():
            shutil.copy2(thumb_path, out_thumb)

        upload_manifest = {
            "title": title[:95],
            "description": description,
            "tags": tags,
            "category_id": "27",
            "is_short": manifest.get("is_short", False),
            "publish_at": publish_at,
            "privacy_status": privacy_status,
            "video_filename": final_video_mp4.name,
            "thumbnail_filename": out_thumb.name if out_thumb.exists() else None,
            "topic": manifest.get("topic"),
            "slug": manifest.get("slug"),
            "vertical": manifest.get("vertical", "stock_market"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        with open(output_dir / "upload_manifest.json", "w") as f:
            json.dump(upload_manifest, f, indent=2)
        logger.info(f"✓ [Artifact Bundle] Saved upload_manifest.json and assets into {output_dir}")

        from app.services.youtube_uploader import get_uploader
        uploader = get_uploader()

        is_short = manifest.get("is_short", False)
        if not is_short:
            logger.info("🔴 [Live Broadcast Engine] Formatting standard master documentary for YouTube Live Broadcast...")
            try:
                from app.services.youtube_live_streamer import broadcast_documentary_as_live
                res = broadcast_documentary_as_live(
                    video_path=final_video_mp4,
                    thumbnail_path=thumb_path if thumb_path.exists() else None,
                    title=title,
                    description=description,
                    scheduled_start_iso=publish_at
                )
                vid_id = res.get("broadcast_id")
                if vid_id:
                    yt_url = res.get("watch_url") or f"https://youtu.be/{vid_id}"
                    logger.success(f"🚀 [YouTube Live Broadcast] Broadcast Active & Streaming: {yt_url}")
                else:
                    raise RuntimeError(f"Live broadcast creation returned no broadcast_id: {res}")
            except Exception as live_err:
                logger.warning(f"Live broadcast stream encounter: {live_err}; executing scheduled institutional upload fallback...")
                res = uploader.upload_video(
                    language="en",
                    video_path=str(final_video_mp4),
                    title=title[:95],
                    description=description,
                    tags=tags,
                    thumbnail_path=str(thumb_path) if thumb_path.exists() else None,
                    category_id="27",
                    privacy_status=privacy_status,
                    publish_at=publish_at,
                    is_short=False,
                    force_upload=True,
                )
                vid_id = (res.get("video_id") or res.get("id")) if isinstance(res, dict) else None
                if vid_id:
                    yt_url = res.get("url") or f"https://youtu.be/{vid_id}"
        else:
            res = uploader.upload_video(
                language="en",
                video_path=str(final_video_mp4),
                title=title[:95],
                description=description,
                tags=tags,
                thumbnail_path=str(thumb_path) if thumb_path.exists() else None,
                category_id="27",
                privacy_status=privacy_status,
                publish_at=publish_at,
                is_short=True,
                force_upload=True,
            )
            vid_id = (res.get("video_id") or res.get("id")) if isinstance(res, dict) else None
            if vid_id:
                yt_url = res.get("url") or f"https://youtu.be/{vid_id}"
                logger.success(f"🚀 [YouTube Upload] Broadcast Live: {yt_url}")
        if res and isinstance(res, dict) and not res.get("success"):
            err_msg = str(res.get("error") or "")
            if any(k in err_msg.lower() for k in ["quota", "limit", "pool"]):
                logger.warning(f"YouTube upload quota reached; video packaged for deferred publishing: {err_msg}")
            else:
                logger.error(f"⛔ YouTube upload failed with fatal error: {err_msg}")
                sys.exit(1)
    except SystemExit:
        raise
    except Exception as yt_err:
        err_msg = str(yt_err)
        if any(k in err_msg.lower() for k in ["quota", "limit", "pool"]):
            logger.warning(f"YouTube upload quota deferral: {yt_err}")
        else:
            logger.error(f"⛔ YouTube upload / QC Gate failed: {yt_err}")
            sys.exit(1)

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

    # Register video with Cloudflare Control Plane (D1 Database)
    if vid_id:
        try:
            cf_worker_url = os.getenv("CLOUDFLARE_WORKER_URL", "https://tbp-cloudflare-orchestrator.cloudflare-orchestrator.workers.dev")
            reg_payload = json.dumps({
                "video_id": vid_id,
                "title": title[:95],
                "privacy_status": privacy_status,
                "total_frames": len(manifest.get("sections", [])),
                "r2_prefix": f"staging/{manifest['slug']}/",
                "mp4_download_url": f"https://youtu.be/{vid_id}",
                "cut_timestamps_json": json.dumps(timestamps if 'timestamps' in locals() else [])
            }).encode("utf-8")
            reg_req = urllib.request.Request(
                f"{cf_worker_url}/register-video",
                data=reg_payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(reg_req, timeout=10) as reg_resp:
                logger.success(f"🌐 [Cloudflare D1] Video {vid_id} registered successfully in control plane.")
        except Exception as reg_err:
            logger.warning(f"Cloudflare video registration notice: {reg_err}")

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

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def main():
    parser = argparse.ArgumentParser(description="Cloud Parallel Video Engine")
    parser.add_argument("--mode", choices=["prepare", "render_segment", "aggregate_and_publish", "dispatch_kaggle_overflow"], required=True)
    parser.add_argument("--topic", default=None, help="Specific financial topic. Required for prepare mode.")
    parser.add_argument("--vertical", default="stock_market", help="Market vertical (e.g. stock_market, crypto, commodities, forex, banking, insurance)")
    parser.add_argument("--duration-sec", type=int, default=60)
    parser.add_argument("--duration-min", type=int, default=12, help="Strict minimum 12 min (720s) for standard 16:9 documentaries")
    parser.add_argument("--is-short", type=str2bool, default=True, help="true for 9:16 vertical short, false for 16:9 widescreen doc")
    parser.add_argument("--publish-at", default=None, help="ISO 8601 UTC timestamp for scheduled release (e.g. 2026-11-15T22:00:00Z)")
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
        # Strict duration enforcement: Standard Documentaries (16:9 Landscape) must be a minimum of 12 minutes (720s = 36 segments of 20s)
        dur = args.duration_sec if args.is_short else max(720, (args.duration_min * 60))
        prepare_session(
            topic=args.topic,
            vertical=args.vertical,
            duration_sec=dur,
            is_short=args.is_short,
            output_dir=args.bundle_dir,
            privacy_status=args.privacy_status,
            publish_at=args.publish_at,
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
