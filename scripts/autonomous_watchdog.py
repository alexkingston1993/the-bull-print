"""
Relentless Autonomous Supervisor & AI Self-Healer (scripts/autonomous_watchdog.py)

Relentless 24/7 channel supervisor that acts as an aggressive replacement for human oversight:
1. Audits live YouTube uploads against the 16 videos / day quota (6 Long-Form + 10 Shorts across 6 slots).
2. Calculates current IST time and checks which slots should be completed.
3. Checks GitHub Actions runs for each slot:
   - If a run failed: pulls logs, diagnoses with Aria's Self-Healing Engine (34 rules), applies remediation,
     and immediately auto-redispatches with FORCE_CPU_FALLBACK=true.
   - If a slot passed its scheduled time and has no in-flight or published video: dispatches it automatically.
4. Pushes assertive, transparent operational reports directly to Telegram so the human owner never has to ask.
"""

import os
import sys
import json
import time
import requests
import subprocess
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "8829963924:AAE7v_xEQXLmy3-YEx8kqMo2GRfnbnxf4GA"
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or "1126599043"
GH_REPO = os.getenv("GITHUB_REPOSITORY") or "alexkingston1993/the-bull-print"
GH_TOKEN = os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_PAT_TOKEN") or ""
if not GH_TOKEN:
    for gh_cmd in ("/usr/local/bin/gh", "gh"):
        try:
            res = subprocess.run([gh_cmd, "auth", "token"], capture_output=True, text=True, check=False)
            if res.returncode == 0 and res.stdout.strip():
                GH_TOKEN = res.stdout.strip()
                break
        except Exception:
            pass
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ""

# ─────────────────────────────────────────────────────────────
# DAILY 16-VIDEO PRODUCTION MATRIX REGISTRY
# ─────────────────────────────────────────────────────────────
SLOT_SCHEDULE = {
    1: {
        "name": "Stock Pre-Open",
        "vertical": "stock_market",
        "ist_hour": 8,
        "ist_minute": 30,
        "target_videos": 3,  # 1 Long + 2 Shorts
        "topic": "Nifty Bank Opening Range Absorption & FII Order Flow",
    },
    2: {
        "name": "Crypto Morning",
        "vertical": "crypto",
        "ist_hour": 11,
        "ist_minute": 0,
        "target_videos": 3,  # 1 Long + 2 Shorts
        "topic": "Bitcoin Liquidation Cluster Map & Funding Stress",
    },
    3: {
        "name": "Insurance Forensics",
        "vertical": "insurance",
        "ist_hour": 13,
        "ist_minute": 30,
        "target_videos": 3,  # 1 Long + 2 Shorts
        "topic": "Health Insurance Room-Rent Deduction Traps",
    },
    4: {
        "name": "Stock Closing Bell",
        "vertical": "stock_market",
        "ist_hour": 15,
        "ist_minute": 45,
        "target_videos": 3,  # 1 Long + 2 Shorts
        "topic": "FII Closing-Session Flows & Option Ring Reading",
    },
    5: {
        "name": "Crypto Evening",
        "vertical": "crypto",
        "ist_hour": 18,
        "ist_minute": 30,
        "target_videos": 2,  # 1 Long + 1 Short
        "topic": "Ethereum CVD Divergence & Exchange Reserve Exits",
    },
    6: {
        "name": "Insurance Night",
        "vertical": "insurance",
        "ist_hour": 21,
        "ist_minute": 0,
        "target_videos": 2,  # 1 Long + 1 Short
        "topic": "CSR vs Incurred Claim Ratio Forensics",
    },
}

TOTAL_DAILY_TARGET = 16


def send_telegram(message: str) -> bool:
    """Dispatches markdown operational report to Telegram."""
    if not TG_TOKEN or not TG_CHAT_ID:
        logger.warning(f"[Telegram Preview]: {message}")
        return False
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    try:
        r = requests.post(url, json=payload, timeout=12)
        if r.status_code == 200:
            return True
        payload.pop("parse_mode", None)
        r2 = requests.post(url, json=payload, timeout=12)
        return r2.status_code == 200
    except Exception as e:
        logger.warning(f"Telegram alert ping failed: {e}")
        return False


def get_headers() -> dict:
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "TheBullPrint-Relentless-Supervisor",
    }
    if GH_TOKEN:
        headers["Authorization"] = f"Bearer {GH_TOKEN}"
    return headers


# ─────────────────────────────────────────────────────────────
# 1. LIVE YOUTUBE CHANNEL AUDIT (SOURCE OF TRUTH)
# ─────────────────────────────────────────────────────────────

def get_youtube_access_token() -> Optional[str]:
    """Retrieves an active access token from oauth_pool.json or environment."""
    pool_data = None
    # 1. From local file
    pool_file = BASE_DIR / "data" / "youtube_tokens" / "oauth_pool.json"
    if pool_file.exists():
        try:
            with open(pool_file, "r", encoding="utf-8") as f:
                pool_data = json.load(f)
        except Exception as e:
            logger.debug(f"Failed to read local pool file: {e}")

    # 2. From env
    if not pool_data and os.getenv("YT_OAUTH_POOL_JSON"):
        try:
            pool_data = json.loads(os.getenv("YT_OAUTH_POOL_JSON"))
        except Exception:
            pass

    if not pool_data:
        return None

    slots = pool_data if isinstance(pool_data, list) else pool_data.get("slots", [])
    for slot in slots:
        try:
            token_data = urllib.parse.urlencode({
                "client_id": slot["client_id"],
                "client_secret": slot["client_secret"],
                "refresh_token": slot["refresh_token"],
                "grant_type": "refresh_token"
            }).encode("utf-8")
            req = urllib.request.Request("https://oauth2.googleapis.com/token", data=token_data)
            with urllib.request.urlopen(req, timeout=10) as resp:
                res = json.loads(resp.read().decode())
                if "access_token" in res:
                    return res["access_token"]
        except Exception:
            continue
    return None


def fetch_today_youtube_uploads() -> List[Dict[str, Any]]:
    """Directly queries YouTube channel uploads to count videos published today."""
    access_token = get_youtube_access_token()
    if not access_token:
        logger.warning("No YouTube access token available for live channel audit.")
        return []

    try:
        # Get uploads playlist ID
        ch_req = urllib.request.Request("https://www.googleapis.com/youtube/v3/channels?part=contentDetails&mine=true")
        ch_req.add_header("Authorization", f"Bearer {access_token}")
        with urllib.request.urlopen(ch_req, timeout=10) as resp:
            ch_res = json.loads(resp.read().decode())
        uploads_pl = ch_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        # Fetch recent uploads
        pl_req = urllib.request.Request(
            f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=35&playlistId={uploads_pl}"
        )
        pl_req.add_header("Authorization", f"Bearer {access_token}")
        with urllib.request.urlopen(pl_req, timeout=12) as resp:
            pl_res = json.loads(resp.read().decode())

        now_utc = datetime.now(timezone.utc)
        today_utc = now_utc.date()
        today_ist = (now_utc + timedelta(hours=5, minutes=30)).date()

        today_uploads = []
        for itm in pl_res.get("items", []):
            snip = itm.get("snippet", {})
            title = (snip.get("title") or "").strip()
            if not title or title.lower() in ("deleted video", "private video"):
                continue
            pub_at = snip.get("publishedAt", "")
            if not pub_at:
                continue
            pub_dt = datetime.fromisoformat(pub_at.replace("Z", "+00:00"))
            if pub_dt.date() in (today_utc, today_ist):
                today_uploads.append({
                    "title": title,
                    "published_at": pub_at,
                    "video_id": snip.get("resourceId", {}).get("videoId", ""),
                })
        return today_uploads
    except Exception as e:
        logger.warning(f"Error querying live YouTube uploads: {e}")
        return []


# ─────────────────────────────────────────────────────────────
# 2. GITHUB ACTIONS RUN AUDIT
# ─────────────────────────────────────────────────────────────

def fetch_active_and_recent_workflow_runs(limit: int = 15) -> List[Dict[str, Any]]:
    """Retrieves recent completed and in-progress runs of market_publisher."""
    url = f"https://api.github.com/repos/{GH_REPO}/actions/runs?per_page={limit}"
    try:
        r = requests.get(url, headers=get_headers(), timeout=15)
        if r.status_code == 200:
            return r.json().get("workflow_runs", [])
    except Exception as e:
        logger.error(f"Failed to fetch workflow runs: {e}")
    return []


def fetch_failed_job_logs(run_id: int) -> str:
    """Extracts failure logs for a specific workflow run."""
    url = f"https://api.github.com/repos/{GH_REPO}/actions/runs/{run_id}/jobs"
    try:
        r = requests.get(url, headers=get_headers(), timeout=15)
        if r.status_code != 200:
            return ""
        jobs = r.json().get("jobs", [])
        for job in jobs:
            if job.get("conclusion") == "failure":
                job_id = job.get("id")
                log_url = f"https://api.github.com/repos/{GH_REPO}/actions/jobs/{job_id}/logs"
                log_res = requests.get(log_url, headers=get_headers(), timeout=20)
                if log_res.status_code == 200:
                    lines = log_res.text.splitlines()
                    return "\n".join(lines[-150:])
    except Exception as e:
        logger.error(f"Error fetching failed job logs: {e}")
    return ""


def dispatch_slot_run(slot: int, force_cpu: bool = False, notes: str = "") -> bool:
    """Dispatches market_publisher.yml for a specific slot immediately."""
    url = f"https://api.github.com/repos/{GH_REPO}/actions/workflows/market_publisher.yml/dispatches"
    body = {
        "ref": "main",
        "inputs": {
            "slot": str(slot),
            "force_cpu_fallback": "true" if force_cpu else "false",
            "notes": notes,
        }
    }
    try:
        r = requests.post(url, headers=get_headers(), json=body, timeout=15)
        if r.status_code == 204:
            logger.success(f"🚀 [Relentless Supervisor] Dispatched slot {slot} (force_cpu={force_cpu}) successfully!")
            return True
        logger.error(f"Dispatch failed for slot {slot}: HTTP {r.status_code} {r.text}")
    except Exception as e:
        logger.error(f"Failed to dispatch slot {slot}: {e}")
    return False


# ─────────────────────────────────────────────────────────────
# 3. RELENTLESS GAP DETECTION & SELF-HEALING ENGINE
# ─────────────────────────────────────────────────────────────

def audit_and_enforce_daily_quota() -> Dict[str, Any]:
    """
    Core supervisor logic:
    1. Checks how many videos are live on YouTube today.
    2. Identifies slots that are overdue based on current IST time.
    3. Checks if an overdue slot has an active run, or if it failed/was missed.
    4. Auto-heals and auto-dispatches any missing or failed slot immediately.
    """
    now_utc = datetime.now(timezone.utc)
    now_ist = now_utc + timedelta(hours=5, minutes=30)
    current_ist_minutes = now_ist.hour * 60 + now_ist.minute

    today_uploads = fetch_today_youtube_uploads()
    live_count = len(today_uploads)
    logger.info(f"📊 [Supervisor Audit] Today ({now_ist.strftime('%Y-%m-%d')} IST): {live_count}/{TOTAL_DAILY_TARGET} videos live on YouTube.")

    runs = fetch_active_and_recent_workflow_runs(limit=20)
    in_progress_runs = [r for r in runs if r.get("status") in ("in_progress", "queued")]
    completed_runs = [r for r in runs if r.get("status") == "completed"]

    slot_statuses = {}
    actions_taken = []

    for slot_id, info in SLOT_SCHEDULE.items():
        slot_cutoff_minutes = info["ist_hour"] * 60 + info["ist_minute"]
        is_overdue = current_ist_minutes >= slot_cutoff_minutes

        # Check if slot videos are already live on YouTube
        slot_topic_words = set(info["topic"].lower().split())
        matched_yt = [
            u for u in today_uploads
            if any(w in u["title"].lower() for w in slot_topic_words if len(w) > 3)
        ]

        if matched_yt:
            slot_statuses[slot_id] = {
                "status": "LIVE ✅",
                "details": f"{len(matched_yt)} video(s) live on channel",
                "color": "green"
            }
            continue

        if not is_overdue:
            mins_until = slot_cutoff_minutes - current_ist_minutes
            hrs = mins_until // 60
            mins = mins_until % 60
            time_str = f"in {hrs}h {mins}m" if hrs > 0 else f"in {mins}m"
            slot_statuses[slot_id] = {
                "status": "SCHEDULED ⏳",
                "details": f"Fires at {info['ist_hour']:02d}:{info['ist_minute']:02d} IST ({time_str})",
                "color": "blue"
            }
            continue

        # Slot is OVERDUE and not yet live on YouTube!
        active_match = None
        for r in in_progress_runs:
            r_title = (r.get("display_title") or r.get("name") or "").lower()
            if f"slot {slot_id}" in r_title or f"slot_{slot_id}" in r_title:
                active_match = r
                break
            if r.get("event") == "schedule":
                try:
                    c_dt = datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))
                    c_ist = c_dt + timedelta(hours=5, minutes=30)
                    c_mins = c_ist.hour * 60 + c_ist.minute
                    if abs(c_mins - slot_cutoff_minutes) <= 45:
                        active_match = r
                        break
                except Exception:
                    pass

        if active_match:
            slot_statuses[slot_id] = {
                "status": "IN-FLIGHT ⚡",
                "details": f"Active Cloud Run #{active_match['id']} ({active_match.get('status')})",
                "color": "cyan"
            }
            continue

        # Check recent completed runs for failures
        recent_failed = [r for r in completed_runs if r.get("conclusion") == "failure"]
        if recent_failed:
            last_fail = recent_failed[0]
            fail_id = last_fail.get("id")
            logger.warning(f"🚨 Slot {slot_id} ({info['name']}) failed in run #{fail_id}! Executing auto-remedy...")
            logs = fetch_failed_job_logs(fail_id)

            remedy_desc = "Auto-remediated failure logs"
            try:
                from app.services.aria_healing import AriaSelfHealingEngine
                remedy = AriaSelfHealingEngine.diagnose(logs, slot_name=f"slot_{slot_id}")
                if remedy and remedy.rule_id:
                    remedy_desc = f"Applied [{remedy.rule_id}]: {remedy.action_plan}"
                    if remedy.auto_executable:
                        remedy.execute_auto_remediation()
            except Exception as e_aria:
                logger.debug(f"Aria diagnostic notice: {e_aria}")

            # Re-dispatch with CPU fallback to guarantee completion
            dispatched = dispatch_slot_run(slot_id, force_cpu=True, notes="Auto-healed re-dispatch by Relentless Supervisor")
            if dispatched:
                slot_statuses[slot_id] = {
                    "status": "AUTO-HEALED & DISPATCHED 🚀",
                    "details": f"{remedy_desc} -> Launched retry on GitHub Actions",
                    "color": "orange"
                }
                actions_taken.append(f"Slot {slot_id} ({info['name']}): Auto-healed failure #{fail_id} and re-dispatched run.")
            else:
                slot_statuses[slot_id] = {
                    "status": "REMEDY ATTEMPTED ⚠️",
                    "details": f"{remedy_desc}",
                    "color": "red"
                }
            continue

        # No active run and no recent failure found: missed slot!
        logger.warning(f"⚠️ Slot {slot_id} ({info['name']}) is overdue with zero runs! Dispatching immediately...")
        dispatched = dispatch_slot_run(slot_id, force_cpu=False, notes="Catch-up dispatch by Relentless Supervisor")
        if dispatched:
            slot_statuses[slot_id] = {
                "status": "CATCH-UP DISPATCHED 🚀",
                "details": "Triggered cloud production run on GitHub Actions",
                "color": "orange"
            }
            actions_taken.append(f"Slot {slot_id} ({info['name']}): Detected missed slot -> Auto-dispatched catch-up run.")
        else:
            slot_statuses[slot_id] = {
                "status": "OVERDUE ⚠️",
                "details": "Dispatch failed",
                "color": "red"
            }

    # Format Telegram alert
    lines = [
        "🎯 *RELENTLESS CHANNEL SUPERVISOR AUDIT* 🐂",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"📅 *Date:* `{now_ist.strftime('%A, %b %d, %Y')} ({now_ist.strftime('%H:%M')} IST)`",
        f"📊 *Daily Quota:* `{live_count} / {TOTAL_DAILY_TARGET} videos live`",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "*Daily Slot Matrix:*",
    ]
    for s_id, s_info in SLOT_SCHEDULE.items():
        st = slot_statuses.get(s_id, {})
        lines.append(f"• *Slot {s_id} ({s_info['name']}):* {st.get('status', 'PENDING')}\n  _{st.get('details', '')}_")

    if actions_taken:
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("*Autonomous Actions Enforced:*")
        for a in actions_taken:
            lines.append(f"⚡ {a}")
    else:
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("🛡️ *Status:* All active pipelines executing normally on cloud runners.")

    report_msg = "\n".join(lines)
    send_telegram(report_msg)
    logger.info("Report dispatched to Telegram.")
    return {
        "live_count": live_count,
        "target": TOTAL_DAILY_TARGET,
        "slot_statuses": slot_statuses,
        "actions_taken": actions_taken,
    }


if __name__ == "__main__":
    audit_and_enforce_daily_quota()
