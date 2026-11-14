#!/usr/bin/env python3
"""
Hourly Real-Time Viral Radar & Macro Breaking News Engine
scripts/hourly_viral_radar.py

Schedule: Runs every hour (0 * * * *).
Mission:
1. Scans real-time financial market movements and macro technology/cloud disruptions
   (e.g., Microsoft Outlook/365 global outage, banking payment gateway halts, extreme FII sweeps).
2. Gemini AI Judgement Call:
   - Evaluates whether the news is truly groundbreaking (Virality score >= 85).
   - Determines the exact number of emergency Ad-Hoc Shorts needed (1, 2, or 3).
   - Dynamically crafts the high-CTR angles for each Short.
3. Dispatches emergency Ad-Hoc production through the cloud matrix.
4. Ad-Hoc Exclusion: These emergency videos are completely separate from the scheduled 12 daily videos.
"""

import os
import sys
import json
import time
import shutil
import subprocess
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pathlib import Path
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

TG_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "8829963924:AAE7v_xEQXLmy3-YEx8kqMo2GRfnbnxf4GA"
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or "1126599043"
LEDGER_PATH = BASE_DIR / "output" / "adhoc_dispatches" / "radar_ledger.json"


def send_telegram_alert(message: str):
    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        return
    try:
        import requests
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TG_CHAT_ID, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": True}, timeout=10)
    except Exception as e:
        logger.warning(f"Telegram notice: {e}")


def get_gh_binary() -> str:
    for cand in ["/usr/local/bin/gh", "/usr/bin/gh", "/opt/homebrew/bin/gh"]:
        if Path(cand).exists():
            return cand
    return shutil.which("gh") or "gh"


def load_dispatched_ledger() -> List[str]:
    if not LEDGER_PATH.exists():
        return []
    try:
        with open(LEDGER_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("dispatched_topics", [])
    except Exception:
        return []


def save_dispatched_ledger(topics: List[str]):
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    existing = load_dispatched_ledger()
    updated = list(set(existing + topics))
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump({"last_updated": datetime.now(timezone.utc).isoformat(), "dispatched_topics": updated}, f, indent=2)


def evaluate_breaking_signals_via_gemini() -> Optional[Dict[str, Any]]:
    """Invokes Gemini AI to scan breaking news and make a high-stakes editorial judgement call."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            from app.config import config
            api_key = config._cfg.get("app", {}).get("gemini_api_key")
        except Exception:
            pass

    if not api_key:
        logger.error("GEMINI_API_KEY not configured. Cannot evaluate breaking viral signals.")
        return None

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    prompt = f"""
    You are the Senior Intelligence Director for 'The Bull Print' high-velocity financial news network.
    Current Time: {now_str}.
    
    MISSION:
    Scan the current world financial, economic, and macro-technology landscape for GROUNDBREAKING EVENTS occurring right now or within the past 2 hours.
    
    EXAMPLES OF GROUNDBREAKING EVENTS:
    - Major Tech/Cloud infrastructure failures (e.g. Microsoft Outlook/365 down, AWS global disruption, CrowdStrike kernel halts impacting stock exchanges and banking).
    - Black swan financial alerts (emergency central bank rate hikes/cuts, sudden currency peg collapses, trading halts on major indices).
    - Sudden institutional shockwaves (FII flash dumps > ₹5,000 Cr, mega corporate fraud/regulatory raids, crude oil sudden ±5% swings).
    
    EDITORIAL JUDGEMENT:
    1. Is there an active event that retail investors, traders, and tech professionals MUST know immediately?
    2. Decide IF an emergency Ad-Hoc Short should be triggered right now.
    3. If YES, decide HOW MANY Shorts are needed (1, 2, or at most 3) to cover different angles (e.g., Short 1 on the immediate outage/crash, Short 2 on the financial/corporate collateral damage).
    4. Provide concrete physical visual metaphor guidelines (bank vaults, server racks in sparks, dark skyscrapers in rain, split ships; ZERO suits or conference tables).
    
    Strictly adhere to SEBI & Global Safe Harbor: Zero stock tips, strictly investigative and educational.
    
    OUTPUT FORMAT:
    Respond ONLY with a valid JSON object matching this schema:
    {{
      "is_groundbreaking": true,
      "virality_score": 92,
      "event_summary": "Microsoft Outlook and 365 services crash globally, paralyzing institutional trading desks and corporate communications.",
      "recommended_shorts_count": 2,
      "shorts": [
        {{
          "topic": "Microsoft Outlook Down: Global Trading Desks Paralyzed",
          "vertical": "stock_market",
          "hook_text": "$3T TECH OUTAGE",
          "badge": "CRITICAL OUTAGE",
          "angle": "How cloud centralization leaves institutional banks and traders completely blind during market hours."
        }},
        {{
          "topic": "The Hidden Cost of Cloud Monopolies: When Outlook Crashes",
          "vertical": "stock_market",
          "hook_text": "CLOUD MONOPOLY",
          "badge": "SYSTEMIC RISK",
          "angle": "Why single-point cloud failures cost global businesses $1.2B per hour."
        }}
      ]
    }}
    If there is NO groundbreaking event right now, set "is_groundbreaking": false and "shorts": [].
    """

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        for model in ["gemini-flash-lite-latest", "gemini-3.8-flash", "gemini-2.5-pro"]:
            try:
                resp = client.models.generate_content(model=model, contents=prompt)
                raw = resp.text.strip()
                if "```json" in raw:
                    raw = raw.split("```json")[1].split("```")[0].strip()
                elif "```" in raw:
                    raw = raw.split("```")[1].split("```")[0].strip()
                data = json.loads(raw)
                logger.success(f"✅ [Viral Radar] Gemini {model} assessment completed. Groundbreaking: {data.get('is_groundbreaking')}")
                return data
            except Exception as e:
                logger.debug(f"Attempt with {model} failed: {e}")
    except Exception as e:
        logger.error(f"[Viral Radar] Gemini evaluation error: {e}")

    return None


def run_viral_radar():
    logger.info("📡 [Viral Radar] Scanning live global market & macro tech signals...")
    evaluation = evaluate_breaking_signals_via_gemini()

    if not evaluation:
        logger.info("Radar scan yielded no data.")
        return

    is_groundbreaking = evaluation.get("is_groundbreaking", False)
    virality_score = evaluation.get("virality_score", 0)
    shorts = evaluation.get("shorts", [])

    if not is_groundbreaking or virality_score < 85 or not shorts:
        logger.info(f"Market within normal operational thresholds (Virality: {virality_score}/100). No Ad-Hoc production required.")
        return

    summary = evaluation.get("event_summary", "Breaking Market Event")
    count = min(len(shorts), 3)
    logger.success(f"🚨 [BREAKING RADAR DETECTED] {summary}")
    logger.info(f"Gemini recommends {count} Ad-Hoc Short(s). Virality: {virality_score}/100.")

    dispatched_history = load_dispatched_ledger()
    gh_bin = get_gh_binary()
    newly_dispatched = []

    for idx, s in enumerate(shorts[:count], 1):
        topic = s.get("topic", "")
        vertical = s.get("vertical", "stock_market")

        # Duplicate check against historical ad-hoc dispatches
        if any(topic.lower() == d.lower() for d in dispatched_history):
            logger.info(f"Topic already dispatched previously: {topic}. Skipping.")
            continue

        logger.info(f"\n🚀 [Ad-Hoc Short {idx}/{count}] Dispatching: {topic}")
        cmd = [
            gh_bin, "workflow", "run",
            "parallel_video_matrix.yml",
            "--repo", "alexkingston1993/the-bull-print",
            "-f", f"topic={topic}",
            "-f", f"vertical={vertical}",
            "-f", "shorts_only=true",
            "-f", "duration_sec=60",
            "-f", "privacy_status=public"
        ]
        try:
            res = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.success(f"✓ Dispatched to Cloud Matrix: {topic}")
            newly_dispatched.append(topic)
            time.sleep(3)
        except Exception as e:
            logger.error(f"Failed to dispatch Ad-Hoc Short: {e}")

    if newly_dispatched:
        save_dispatched_ledger(newly_dispatched)
        send_telegram_alert(
            f"⚡ *The Bull Print BREAKING RADAR ALERT*\n\n"
            f"🚨 *Macro Event*: {summary}\n"
            f"🔥 *Virality Score*: `{virality_score}/100`\n"
            f"🎬 *Ad-Hoc Shorts Dispatched* ({len(newly_dispatched)}):\n"
            + "\n".join(f"• `{t}`" for t in newly_dispatched)
            + f"\n\n*Note*: These are independent Ad-Hoc productions and do not consume the daily 12-video quota."
        )


def main():
    logger.info("=" * 70)
    logger.info("📡 THE BULL PRINT REAL-TIME HOURLY VIRAL RADAR")
    logger.info("=" * 70)
    run_viral_radar()


if __name__ == "__main__":
    main()

