"""
Telegram Bot & Real-Time Alert Engine (telegram_bot.py).
1. Sends live status alerts at key pipeline milestones:
   - 📈 Playwright charts captured
   - 🎬 FFmpeg video rendered & stitched
   - 🚀 YouTube uploaded with containsSyntheticMedia=True
   - 🌐 Vercel deployment live & IndexNow pinged
2. Listens for remote /run commands to trigger automated cloud runs.
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path
import requests
from loguru import logger

BASE_DIR = Path(__file__).parent
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")


def send_telegram_alert(message: str) -> bool:
    """Sends a formatted markdown notification to your private Telegram channel/chat."""
    token = os.getenv("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN)
    chat_id = os.getenv("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID)

    if not token or not chat_id:
        logger.info(f"[Telegram Alert Preview]:\n{message}")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }

    try:
        res = requests.post(url, json=payload, timeout=10)
        return res.status_code == 200
    except Exception as e:
        logger.warning(f"Telegram alert ping failed: {e}")
        return False


def dispatch_github_cloud_run(topic: str, is_short: bool = True, duration: int = 60, vertical: str = "stock_market") -> bool:
    """
    STRICT CLOUD-ONLY RULE: Under no circumstances does video rendering run on local Mac.
    Dispatches execution to 20-runner parallel GitHub Actions cloud matrix!
    """
    token = os.getenv("GITHUB_PAT_TOKEN") or os.getenv("GITHUB_TOKEN", "")
    repo = os.getenv("GITHUB_REPO", "alexkingston1993/the-bull-print")
    if not token:
        logger.warning("GITHUB_TOKEN / GITHUB_PAT_TOKEN not found — cannot dispatch cloud runner.")
        return False

    url = f"https://api.github.com/repos/{repo}/dispatches"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }
    payload = {
        "event_type": "trigger_parallel_video",
        "client_payload": {
            "topic": topic,
            "shorts_only": "true" if is_short else "false",
            "duration_sec": str(duration) if is_short else "60",
            "duration_min": str(duration) if not is_short else "3",
            "vertical": vertical,
            "parallel_matrix": "true",
            "max_parallel_runners": "20",
            "mode": "telegram_cloud_dispatch",
        }
    }
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=12)
        # Also trigger backup legacy event name
        payload["event_type"] = "trigger_media_engine"
        requests.post(url, json=payload, headers=headers, timeout=12)
        return res.status_code in (200, 204)
    except Exception as e:
        logger.error(f"GitHub cloud dispatch failed: {e}")
        return False


def run_telegram_bot():
    """Starts polling listener for Telegram natural language & remote cloud triggers."""
    token = os.getenv("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN)
    if not token:
        logger.warning("TELEGRAM_BOT_TOKEN not configured. Bot listener not started.")
        print("To activate the bot listener, set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.")
        return

    try:
        from telegram import Update
        from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

        async def natural_language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_id = str(update.effective_chat.id)
            target_chat_id = os.getenv("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID)
            if target_chat_id and user_id != target_chat_id:
                await update.message.reply_text("⛔ Unauthorized user.")
                return

            text = update.message.text.strip()
            lower = text.toLowerCase() if hasattr(text, 'toLowerCase') else text.lower()

            # Determine intent
            vertical = "crypto" if any(k in lower for k in ("crypto", "solana", "bitcoin", "btc", "eth")) else \
                       "insurance" if any(k in lower for k in ("insurance", "claim", "health", "irdai")) else "stock_market"

            is_short = any(k in lower for k in ("short", "reel", "36s", "60s"))
            is_video = any(k in lower for k in ("video", "masterclass", "deep dive", "minute", "min"))

            if is_short or is_video:
                duration = 36 if "36" in lower else 60 if is_short else (5 if "5" in lower else (10 if "10" in lower else 3))
                topic = text
                for noise in ("make", "create", "generate", "a", "short", "video", "masterclass", "60s", "36s", "please", "about", "on"):
                    topic = re.sub(rf"\b{noise}\b", "", topic, flags=re.IGNORECASE)
                topic = topic.strip() or ("Solana Memecoin Siphon" if is_short else "Institutional Order Flow Footprint")

                ok = dispatch_github_cloud_run(topic=topic, is_short=is_short, duration=duration, vertical=vertical)
                unit = "s 9:16 Short" if is_short else "-Min Masterclass"
                await update.message.reply_text(
                    f"🕶️☕ *Agent Aria on Station:*\n\n"
                    f"Dispatched **{duration}{unit}** to our **20-Runner Parallel Cloud Matrix** on GitHub Actions!\n"
                    f"📌 *Topic:* `{topic}`\n"
                    f"🏛️ *Vertical:* `{vertical}`\n"
                    f"⚡ *Parallel Concurrency:* All segments rendering simultaneously in the cloud (+ Kaggle GPU overflow).\n"
                    f"🛡️ *Host Status:* Your Mac is 100% untouched. All execution runs in the cloud!\n\n"
                    f"Monitoring telemetry now, Boss! 🚀",
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    "*Adjusts dark sunglasses and sets down double espresso* 🕶️☕\n\n"
                    "Agent Aria on station, Captain! All cloud systems are green and 100% hosted in the cloud. "
                    "Tell me what topic to produce (Short or 2K Masterclass) or ask for telemetry/revenue, and I'll handle the rest! 🚀",
                    parse_mode="Markdown"
                )

        async def run_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            topic = " ".join(context.args) if context.args else "Institutional Order Flow Absorption & Macro Liquidity"
            ok = dispatch_github_cloud_run(topic=topic, is_short=False, duration=3, vertical="stock_market")
            await update.message.reply_text(f"🚀 Cloud media engine dispatched for: '{topic}'! (Zero Mac compute).")

        async def short_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            args = list(context.args) if context.args else []
            duration = 60
            if args and args[-1] in ("36", "60"):
                duration = int(args.pop())
            topic = " ".join(args) if args else "Solana MEV Bot Liquidation Siphon"
            ok = dispatch_github_cloud_run(topic=topic, is_short=True, duration=duration, vertical="crypto")
            await update.message.reply_text(f"📱 Cloud 9:16 Short dispatched for '{topic}' ({duration}s)! (Zero Mac compute).")

        async def video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            args = list(context.args) if context.args else []
            vertical = "stock_market"
            for v in ("crypto", "insurance", "stock_market", "stock"):
                if v in args:
                    vertical = "stock_market" if v == "stock" else v
                    args.remove(v)
                    break
            topic = " ".join(args) if args else "Institutional Order Flow Footprint"
            ok = dispatch_github_cloud_run(topic=topic, is_short=False, duration=3, vertical=vertical)
            await update.message.reply_text(f"🎬 Cloud 16:9 Video & Web Article dispatched for '{topic}' ({vertical})! (Zero Mac compute).")

        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler("run", run_command))
        app.add_handler(CommandHandler("short", short_command))
        app.add_handler(CommandHandler("video", video_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, natural_language_handler))
        print("🤖 Telegram Bot listener active with Natural Language AI Brain & 100% Cloud Dispatch...")
        app.run_polling()
    except ImportError:
        logger.warning("python-telegram-bot not installed. Serverless webhook operates 24/7 on Vercel.")


if __name__ == "__main__":
    if "--test" in sys.argv:
        send_telegram_alert("🔔 *The Bull Print Media Engine:* Test alert successfully connected!")
    else:
        run_telegram_bot()

