"""
The Bull Print — Agent Aria Enhancement Pack
============================================

Drop-in additions to aria_healing.py / telegram_bot_service.py.
Each enhancement is self-contained and wired to existing class names.

INSTALLATION — add to telegram_bot_service.py imports:
    from app.services.aria_enhancements import (
        AriaPipelineCard, AriaApprovalGate, AriaCheckpointResume,
        AriaScheduleCard, AriaQuotaBurnRate, AriaShortsTracker,
    )

ENHANCEMENTS:
  1. AriaPipelineCard     — Live single-card run progress (edits same message in-place)
  2. AriaApprovalGate     — Thumbnail approval gate with 15-min auto-publish timer
  3. AriaCheckpointResume — Checkpoint-aware retry (only re-runs the failed step)
  4. AriaScheduleCard     — Today's slot schedule with IST countdown timers
  5. AriaQuotaBurnRate    — GitHub runner quota burn-rate projection (red/amber/green)
  6. AriaShortsTracker    — Tracks Shorts uploaded today vs daily 10-Short target
"""

import os
import json
import time
import datetime
import requests
import subprocess
import shutil
from typing import Dict, Optional, Any, Tuple

from loguru import logger
from app.config import config


# ─────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────────────────

def _bot_token() -> str:
    return os.getenv("TELEGRAM_BOT_TOKEN") or config.app.get("telegram_bot_token") or ""

def _chat_id() -> str:
    return str(os.getenv("TELEGRAM_CHAT_ID") or config.app.get("telegram_chat_id") or "")

def _gh_bin() -> str:
    for p in ["/usr/local/bin/gh", "/opt/homebrew/bin/gh"]:
        if os.path.exists(p):
            return p
    return shutil.which("gh") or "gh"

def _api(method: str, payload: dict, timeout: int = 12) -> dict:
    """Fire-and-forget Telegram Bot API call. Returns parsed JSON or {}."""
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{_bot_token()}/{method}",
            json=payload,
            timeout=timeout,
        )
        return r.json() if r.status_code == 200 else {}
    except Exception as e:
        logger.warning(f"[Aria Enhance] Telegram API error ({method}): {e}")
        return {}


# ═════════════════════════════════════════════════════════════════════════════
# ENHANCEMENT 1 — Live Pipeline Progress Card
# ═════════════════════════════════════════════════════════════════════════════

class AriaPipelineCard:
    """
    Sends ONE status card per pipeline run and edits it in-place as steps
    complete — zero message spam.

    Usage (cloud_orchestrator.py):
        card = AriaPipelineCard.new_card(slot_name="pre_market", run_id="39801234567")
        AriaPipelineCard.update_step(card["message_id"], "charts", "done", "3 charts captured")
        AriaPipelineCard.update_step(card["message_id"], "gemini", "done", "7,421 tokens")
        AriaPipelineCard.update_step(card["message_id"], "video", "running", "Kaggle T4…")
        AriaPipelineCard.update_step(card["message_id"], "video", "done", "8m 42s · 1080p")
        AriaPipelineCard.update_step(card["message_id"], "youtube", "done", "youtu.be/AbCdEfGhIj")
        AriaPipelineCard.finalize(card["message_id"])
    """

    STEPS = ["charts", "gemini", "thumbnail", "video", "youtube", "article", "indexing"]
    ICONS = {"pending": "⬜", "running": "🔄", "done": "✅", "warning": "⚠️", "failed": "❌"}
    _state: Dict[str, Dict] = {}

    @classmethod
    def _build_text(cls, slot: str, run_id: str, states: dict) -> str:
        lines = [
            "🛰️ *Agent Aria · Pipeline Live Card* 🕶️",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"⚡ *Slot:* `{slot}`   *Run:* `#{run_id}`",
            "",
        ]
        for step in cls.STEPS:
            s = states.get(step, {})
            icon = cls.ICONS.get(s.get("status", "pending"), "⬜")
            label = step.upper().replace("_", " ")
            note = f" — {s['note']}" if s.get("note") else ""
            lines.append(f"{icon} *{label}*{note}")
        elapsed = states.get("_elapsed", "")
        if elapsed:
            lines += ["", f"⏱ *Elapsed:* `{elapsed}`"]
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        return "\n".join(lines)

    @classmethod
    def new_card(cls, slot_name: str, run_id: str) -> dict:
        """Sends the initial pending card. Returns {"message_id": int}."""
        states = {s: {"status": "pending"} for s in cls.STEPS}
        states["_start_ts"] = time.time()
        text = cls._build_text(slot_name, run_id, states)
        result = _api("sendMessage", {"chat_id": _chat_id(), "text": text, "parse_mode": "Markdown"})
        msg_id = result.get("result", {}).get("message_id")
        if msg_id:
            cls._state[str(msg_id)] = {"slot": slot_name, "run_id": run_id, "steps": states}
        return {"message_id": msg_id}

    @classmethod
    def update_step(cls, message_id: int, step: str, status: str, note: str = "") -> None:
        """Edits the card in-place to update one step's status."""
        key = str(message_id)
        if key not in cls._state:
            return
        record = cls._state[key]
        record["steps"][step] = {"status": status, "note": note}
        elapsed_sec = int(time.time() - record["steps"].get("_start_ts", time.time()))
        m, s = divmod(elapsed_sec, 60)
        record["steps"]["_elapsed"] = f"{m}m {s:02d}s"
        text = cls._build_text(record["slot"], record["run_id"], record["steps"])
        _api("editMessageText", {
            "chat_id": _chat_id(), "message_id": message_id,
            "text": text, "parse_mode": "Markdown",
        })

    @classmethod
    def finalize(cls, message_id: int, success: bool = True) -> None:
        """Appends footer and attaches quick-action buttons."""
        key = str(message_id)
        if key not in cls._state:
            return
        record = cls._state[key]
        text = cls._build_text(record["slot"], record["run_id"], record["steps"])
        text += "\n✅ *ALL SYSTEMS NOMINAL — CONTENT LIVE!* 🚀☕" if success else \
                "\n❌ *PIPELINE HALTED — tap Heal & Relaunch below*"
        markup = {
            "inline_keyboard": [[
                {"text": "🌅 Next Slot",  "callback_data": f"run_slot:{record['slot']}"},
                {"text": "📊 Status",      "callback_data": "cb_status"},
                {"text": "💰 Revenue",     "callback_data": "view_revenue"},
            ]]
        } if success else {
            "inline_keyboard": [[
                {"text": "🩹 Heal & Relaunch", "callback_data": f"run_slot:{record['slot']}"},
                {"text": "📋 Full Log",          "callback_data": "cb_status"},
            ]]
        }
        _api("editMessageText", {
            "chat_id": _chat_id(), "message_id": message_id,
            "text": text, "parse_mode": "Markdown", "reply_markup": markup,
        })
        cls._state.pop(key, None)


# ═════════════════════════════════════════════════════════════════════════════
# ENHANCEMENT 2 — Human-in-the-Loop Thumbnail Approval Gate
# ═════════════════════════════════════════════════════════════════════════════

class AriaApprovalGate:
    """
    Before Kaggle renders the full video, Aria sends the thumbnail + title
    for your approval. Auto-approves after 15 minutes if no action taken.

    Wire in process_updates():
        elif data.startswith("approve_thumb:"):
            AriaApprovalGate.handle_callback(chat_id, data.split(":", 1)[1], "approved")
        elif data.startswith("regen_thumb:"):
            AriaApprovalGate.handle_callback(chat_id, data.split(":", 1)[1], "regenerate")
        elif data.startswith("edit_title:"):
            AriaApprovalGate.pending_title_edit[data.split(":", 1)[1]] = chat_id
    """

    AUTO_APPROVE_SECS = 15 * 60
    _decisions: Dict[str, Optional[str]] = {}
    pending_title_edit: Dict[str, Any] = {}

    @classmethod
    def ask(cls, title: str, thumb_path: str, compliance_ok: bool, slug: str,
            timeout: int = None) -> Tuple[str, str]:
        """Sends thumbnail to Telegram. Blocks until approved or auto-approved. Returns (title, thumb_path)."""
        timeout = timeout or cls.AUTO_APPROVE_SECS
        cls._decisions[slug] = None
        badge = "✅ SEBI Compliant" if compliance_ok else "⚠️ COMPLIANCE ALERT"
        caption = (
            f"🎨 *Thumbnail & Title Preview* — `{slug}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📝 *Title:* {title}\n"
            f"🛡️ *Compliance:* {badge}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"_Auto-approves in {timeout // 60} minutes if no action taken._"
        )
        markup = {"inline_keyboard": [
            [{"text": "✅ Approve & Publish", "callback_data": f"approve_thumb:{slug}"},
             {"text": "🎨 Regen Thumbnail",   "callback_data": f"regen_thumb:{slug}"}],
            [{"text": "✏️ Edit Title",         "callback_data": f"edit_title:{slug}"}],
        ]}
        if os.path.exists(thumb_path):
            with open(thumb_path, "rb") as f:
                try:
                    requests.post(
                        f"https://api.telegram.org/bot{_bot_token()}/sendPhoto",
                        data={"chat_id": _chat_id(), "caption": caption,
                              "parse_mode": "Markdown", "reply_markup": json.dumps(markup)},
                        files={"photo": f}, timeout=20,
                    )
                except Exception as e:
                    logger.warning(f"[ApprovalGate] Photo send failed: {e}")
                    _api("sendMessage", {"chat_id": _chat_id(), "text": caption,
                                          "parse_mode": "Markdown", "reply_markup": markup})
        else:
            _api("sendMessage", {"chat_id": _chat_id(), "text": caption,
                                  "parse_mode": "Markdown", "reply_markup": markup})

        deadline = time.time() + timeout
        while time.time() < deadline:
            decision = cls._decisions.get(slug)
            if decision == "approved":
                logger.info(f"[ApprovalGate] '{slug}' manually approved.")
                return title, thumb_path
            if decision == "regenerate":
                _api("sendMessage", {"chat_id": _chat_id(),
                                      "text": "🔄 *Aria:* Regenerating thumbnail — reply with 3 new words, Boss! ✏️",
                                      "parse_mode": "Markdown"})
                word_deadline = time.time() + 180
                while time.time() < word_deadline:
                    new_words = cls._decisions.get(f"{slug}_new_words")
                    if new_words:
                        return new_words, thumb_path
                    time.sleep(3)
                break
            time.sleep(5)

        _api("sendMessage", {"chat_id": _chat_id(),
                               "text": f"⏱️ *Aria:* Auto-approving `{slug}` — no action in {timeout // 60}m. Launching GPU render now! 🚀",
                               "parse_mode": "Markdown"})
        logger.info(f"[ApprovalGate] '{slug}' auto-approved after timeout.")
        return title, thumb_path

    @classmethod
    def handle_callback(cls, chat_id: Any, slug: str, decision: str) -> None:
        cls._decisions[slug] = decision
        msgs = {"approved": "✅ *Approved!* Dispatching to Kaggle GPU now — Aria's on it! 🚀",
                "regenerate": "🎨 *Noted, Boss!* Fresh 3-word thumbnail options incoming…"}
        _api("sendMessage", {"chat_id": chat_id, "text": msgs.get(decision, "Got it!"),
                               "parse_mode": "Markdown"})

    @classmethod
    def handle_new_title_text(cls, slug: str, text: str) -> None:
        cls._decisions[f"{slug}_new_words"] = text.strip()
        cls.pending_title_edit.pop(slug, None)
        _api("sendMessage", {"chat_id": _chat_id(),
                               "text": f"✏️ *Title updated:* `{text.strip()}`\nRegenerating thumbnail… ⚡",
                               "parse_mode": "Markdown"})


# ═════════════════════════════════════════════════════════════════════════════
# ENHANCEMENT 3 — Checkpoint-Aware Resume
# ═════════════════════════════════════════════════════════════════════════════

class AriaCheckpointResume:
    """
    Writes state/pipeline_checkpoint.json after each major step.
    On failure, Aria shows exactly where it stopped and offers to resume
    from ONLY the failed step (skipping Playwright + Gemini + Kaggle rerun).

    Usage (cloud_orchestrator.py):
        AriaCheckpointResume.mark("charts",    slug, {"files": captured_charts})
        AriaCheckpointResume.mark("gemini",    slug, {"tokens": 7421})
        AriaCheckpointResume.mark("thumbnail", slug, {"path": str(yt_thumb)})
        AriaCheckpointResume.mark("video",     slug, {"duration": "8m42s"})
        AriaCheckpointResume.mark("youtube",   slug, {"video_id": yt_video_id})
        AriaCheckpointResume.mark("article",   slug, {"url": live_url})

    Wire in generate_reply():
        if lower in ["/checkpoint", "last checkpoint", "where did it stop"]:
            return AriaCheckpointResume.status_card_with_markup()
    """

    CHECKPOINT_PATH = "state/pipeline_checkpoint.json"

    @classmethod
    def _load(cls) -> dict:
        try:
            if os.path.exists(cls.CHECKPOINT_PATH):
                with open(cls.CHECKPOINT_PATH, "r") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    @classmethod
    def _save(cls, data: dict) -> None:
        os.makedirs(os.path.dirname(cls.CHECKPOINT_PATH), exist_ok=True)
        with open(cls.CHECKPOINT_PATH, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def mark(cls, step: str, slug: str, meta: dict = None) -> None:
        data = cls._load()
        data.setdefault(slug, {})
        data[slug][step] = {"status": "done", "ts": datetime.datetime.utcnow().isoformat(), "meta": meta or {}}
        data["_latest_slug"] = slug
        data["_latest_step"] = step
        cls._save(data)
        logger.info(f"[Checkpoint] ✅ {slug}/{step} marked complete.")

    @classmethod
    def get_resume_step(cls, slug: str) -> Optional[str]:
        order = ["charts", "gemini", "thumbnail", "video", "youtube", "article", "indexing"]
        data = cls._load().get(slug, {})
        for step in order:
            if step not in data or data[step].get("status") != "done":
                return step
        return None

    @classmethod
    def status_card(cls) -> str:
        data = cls._load()
        slug = data.get("_latest_slug", "")
        if not slug:
            return "📭 *Aria:* No checkpoint data yet — fresh start on next trigger! ☕"
        steps = data.get(slug, {})
        order = ["charts", "gemini", "thumbnail", "video", "youtube", "article", "indexing"]
        icons = {"done": "✅", "running": "🔄", "failed": "❌"}
        lines = ["🔖 *AGENT ARIA: CHECKPOINT STATUS* ⚡", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                 f"📂 *Slug:* `{slug}`"]
        for s in order:
            if s in steps:
                status = steps[s].get("status", "done")
                ts = steps[s].get("ts", "")[:16].replace("T", " ")
                lines.append(f"{icons.get(status, '✅')} *{s.upper()}* — `{ts} UTC`")
            else:
                lines.append(f"⬜ *{s.upper()}* — pending")
        resume_from = cls.get_resume_step(slug)
        if resume_from:
            lines += ["━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                      f"🎯 *Resume From:* `{resume_from}` — tap below to skip already-done steps!"]
        else:
            lines += ["━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "🎉 *All steps complete!*"]
        return "\n".join(lines)

    @classmethod
    def status_card_with_markup(cls) -> Tuple[str, Optional[dict]]:
        data = cls._load()
        slug = data.get("_latest_slug", "")
        resume_from = cls.get_resume_step(slug) if slug else None
        card = cls.status_card()
        markup = None
        if resume_from and slug:
            markup = {"inline_keyboard": [[
                {"text": f"▶️ Resume from {resume_from.upper()}",
                 "callback_data": f"resume_from:{slug}:{resume_from}"},
                {"text": "🔄 Full Restart", "callback_data": "run_slot:pre_market"},
            ]]}
        return card, markup


# ═════════════════════════════════════════════════════════════════════════════
# ENHANCEMENT 4 — Today's Schedule Card with IST Countdown
# ═════════════════════════════════════════════════════════════════════════════

class AriaScheduleCard:
    """
    /schedule or /today — all 6 slots in IST with countdown to next slot
    and one-tap trigger buttons.
    """

    SLOTS = [
        {"name": "pre_market",     "label": "Stock Pre-Open",     "utc_h": 3,  "utc_m": 0,  "vertical": "stock_market"},
        {"name": "crypto_morning", "label": "Crypto Morning",     "utc_h": 5,  "utc_m": 30, "vertical": "crypto"},
        {"name": "insurance_lunch","label": "Insurance Lunch",    "utc_h": 8,  "utc_m": 0,  "vertical": "insurance"},
        {"name": "market_close",   "label": "Stock Closing Bell", "utc_h": 10, "utc_m": 15, "vertical": "stock_market"},
        {"name": "crypto_evening", "label": "Crypto Evening",     "utc_h": 13, "utc_m": 0,  "vertical": "crypto"},
        {"name": "insurance_night","label": "Insurance Night",    "utc_h": 15, "utc_m": 30, "vertical": "insurance"},
    ]

    @classmethod
    def build_card(cls) -> str:
        now_utc = datetime.datetime.utcnow()
        ist_offset = datetime.timedelta(hours=5, minutes=30)
        now_ist = now_utc + ist_offset
        lines = [
            "📅 *AGENT ARIA: TODAY'S PRODUCTION SCHEDULE* 🎬",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"🕐 *Current IST:* `{now_ist.strftime('%H:%M')}` on `{now_ist.strftime('%a %d %b')}`",
            "",
        ]
        next_found = False
        for slot in cls.SLOTS:
            slot_utc = now_utc.replace(hour=slot["utc_h"], minute=slot["utc_m"], second=0, microsecond=0)
            slot_ist = slot_utc + ist_offset
            ist_str = slot_ist.strftime("%H:%M IST")
            if slot_utc > now_utc and not next_found:
                mins_left = int((slot_utc - now_utc).total_seconds() // 60)
                status = f"🔜 *NEXT* in {mins_left}m"
                next_found = True
            elif slot_utc <= now_utc:
                status = "✅ Done"
            else:
                status = "⏳ Queued"
            lines.append(f"{status} — `{ist_str}` · *{slot['label']}* (`{slot['vertical']}`)")
        lines += ["", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                  "💡 Tap a slot to trigger early → `/run <slot_name>`"]
        return "\n".join(lines)

    @classmethod
    def build_card_with_markup(cls) -> Tuple[str, dict]:
        markup = {"inline_keyboard": [
            [{"text": "🌅 Pre-Market",  "callback_data": "run_slot:pre_market"},
             {"text": "🔔 Closing Bell","callback_data": "run_slot:market_close"}],
            [{"text": "₿ Crypto AM",   "callback_data": "run_slot:crypto_morning"},
             {"text": "🌙 Crypto PM",  "callback_data": "run_slot:crypto_evening"}],
        ]}
        return cls.build_card(), markup


# ═════════════════════════════════════════════════════════════════════════════
# ENHANCEMENT 5 — GitHub Runner Quota Burn-Rate Projector
# ═════════════════════════════════════════════════════════════════════════════

class AriaQuotaBurnRate:
    """
    /burnrate — projects whether the 2,000-min/month free quota will last,
    with a visual bar and red/amber/green verdict.
    """

    MONTHLY_QUOTA = 2000
    EST_MIN_PER_DAY = 17.5  # 6 slots × ~3 min avg on GHA Ubuntu runner

    @classmethod
    def build_card(cls) -> str:
        now = datetime.datetime.utcnow()
        day = now.day
        try:
            if now.month == 12:
                days_in_month = 31
            else:
                days_in_month = (datetime.date(now.year, now.month + 1, 1) - datetime.timedelta(days=1)).day
        except Exception:
            days_in_month = 30

        consumed = min(round(day * cls.EST_MIN_PER_DAY), cls.MONTHLY_QUOTA)
        remaining = cls.MONTHLY_QUOTA - consumed
        pct = (consumed / cls.MONTHLY_QUOTA) * 100
        projected = consumed + (days_in_month - day) * cls.EST_MIN_PER_DAY

        if projected > cls.MONTHLY_QUOTA * 0.95:
            verdict = "🔴 *RED ALERT:* Projected to HIT ceiling before month-end! Reduce slot count or upgrade to GitHub Teams (3,000 min)."
        elif projected > cls.MONTHLY_QUOTA * 0.80:
            verdict = "🟡 *AMBER:* On pace to consume ~80%+ of quota. Watch scheduling closely."
        else:
            verdict = "🟢 *GREEN:* Quota runway healthy — full 16-video/day cadence sustainable all month! ☕🚀"

        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        lines = [
            "📊 *AGENT ARIA: QUOTA BURN-RATE PROJECTOR* ⏱️",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"📅 *Billing Cycle:* `{now.strftime('%B %Y')}` (Day {day} of {days_in_month})",
            f"🎁 *Monthly Free Quota:* `2,000 minutes`",
            "",
            f"`[{bar}]` `{pct:.1f}%`",
            "",
            f"⚙️ *Est. Consumed:*         `{consumed} min`",
            f"📉 *Remaining:*             `{remaining} min`",
            f"🔮 *Projected Total (EOM):* `{int(projected)} min`",
            f"💡 *Burn Rate:*             `~{cls.EST_MIN_PER_DAY} min/day` (6 slots × ~3 min avg)",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            verdict,
        ]
        return "\n".join(lines)


# ═════════════════════════════════════════════════════════════════════════════
# ENHANCEMENT 6 — Daily Shorts Tracker (10-Short target)
# ═════════════════════════════════════════════════════════════════════════════

class AriaShortsTracker:
    """
    /shorts — how many 9:16 Shorts published today vs the 10-Short daily target.
    Primary: YouTube Data API v3. Fallback: GitHub Actions run count.
    """

    DAILY_TARGET = 10

    @classmethod
    def _count_yt_shorts(cls) -> int:
        try:
            from googleapiclient.discovery import build
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request as GRequest

            raw = os.getenv("YT_OAUTH_POOL_JSON") or json.dumps({
                "client_id":     os.getenv("YT_CLIENT_ID", ""),
                "client_secret": os.getenv("YT_CLIENT_SECRET", ""),
                "refresh_token": os.getenv("YT_REFRESH_TOKEN", ""),
                "token_uri":     "https://oauth2.googleapis.com/token",
            })
            slots = json.loads(raw)
            if isinstance(slots, dict):
                slots = [slots]

            today_start = datetime.datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"

            total = 0
            for slot in slots[:1]:
                creds = Credentials(
                    token=None,
                    refresh_token=slot.get("refresh_token"),
                    token_uri=slot.get("token_uri", "https://oauth2.googleapis.com/token"),
                    client_id=slot.get("client_id"),
                    client_secret=slot.get("client_secret"),
                )
                creds.refresh(GRequest())
                yt = build("youtube", "v3", credentials=creds)
                resp = yt.search().list(
                    part="snippet", forMine=True, type="video",
                    publishedAfter=today_start, maxResults=50, videoDuration="short",
                ).execute()
                total += len(resp.get("items", []))
            return total
        except Exception as e:
            logger.warning(f"[ShortsTracker] YT API failed: {e}")
            return -1

    @classmethod
    def _count_from_gha(cls) -> int:
        try:
            res = subprocess.run(
                [_gh_bin(), "run", "list", "-R", "alexkingston1993/the-bull-print",
                 "-L", "20", "--json", "conclusion,updatedAt,name"],
                capture_output=True, text=True, timeout=12,
            )
            if res.returncode != 0:
                return -1
            data = json.loads(res.stdout)
            today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
            return sum(
                1 for r in data
                if r.get("conclusion") == "success"
                and r.get("updatedAt", "").startswith(today)
                and "short" in r.get("name", "").lower()
            )
        except Exception:
            return -1

    @classmethod
    def build_card(cls) -> str:
        count = cls._count_yt_shorts()
        source = "YouTube API"
        if count < 0:
            count = cls._count_from_gha()
            source = "GitHub Actions"
        if count < 0:
            count, source = 0, "estimated"

        remaining = max(0, cls.DAILY_TARGET - count)
        pct = min(100, int((count / cls.DAILY_TARGET) * 100))
        bar = "📹" * int(pct / 5) + "⬜" * (20 - int(pct / 5))

        if count >= cls.DAILY_TARGET:
            verdict = "🏆 *DAILY SHORTS TARGET HIT!* 10/10 Shorts live — algorithm feed fully stoked! 🔥"
        elif count >= 7:
            verdict = f"🟡 *Almost there!* {remaining} more Shorts to go — trigger `/run crypto_evening` or `/run insurance_night` next."
        else:
            verdict = f"📈 {remaining} Shorts remaining for today. Slots still queued — Aria's on it! ☕"

        lines = [
            "📹 *AGENT ARIA: DAILY SHORTS TRACKER* 🎬",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"🎯 *Daily Target:* `{cls.DAILY_TARGET} Shorts`   *Source:* `{source}`",
            "",
            f"`[{bar}]`",
            "",
            f"✅ *Published Today:* `{count} / {cls.DAILY_TARGET}` Shorts",
            f"⏳ *Remaining:*       `{remaining}`",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            verdict,
        ]
        return "\n".join(lines)

    @classmethod
    def build_card_with_markup(cls) -> Tuple[str, dict]:
        markup = {"inline_keyboard": [[
            {"text": "▶️ Crypto Evening",  "callback_data": "run_slot:crypto_evening"},
            {"text": "▶️ Insurance Night", "callback_data": "run_slot:insurance_night"},
        ]]}
        return cls.build_card(), markup
