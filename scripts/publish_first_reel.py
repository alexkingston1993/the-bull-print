#!/usr/bin/env python3
"""
Publishes Short #1 (FwrVEOSmQyg) to Instagram Reels with Meta Resumable Upload.
"""
import os
import sys
import json
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Load .env into os.environ
env_path = Path(".env")
if env_path.exists():
    for line in open(env_path):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

from app.services.instagram_reels_publisher import build_instagram_seo_caption, publish_local_mp4_reel

title = "CoreWeave’s High-Stakes Debt vs. Nvidia’s Discipline | The Bull Print"
synopsis = "CoreWeave leveraged $7.5 billion in debt collateralized directly by Nvidia H100 GPUs, exposing a fragile circular liquidity loop between hyperscalers and GPU hardware suppliers."
vid_id = "FwrVEOSmQyg"
mp4_path = "output/FwrVEOSmQyg.mp4"

print("Generating SEO/AI Caption...")
caption = build_instagram_seo_caption(
    title=title,
    synopsis=synopsis,
    youtube_video_id=vid_id,
    tags=["CoreWeave", "Nvidia", "AIChips", "DebtLoop"]
)
print("Generated Caption:\n", caption)
print("---")

print("Publishing to Instagram Reels (@thebullprint)...")
res = publish_local_mp4_reel(video_path=mp4_path, caption=caption)
print("Instagram Publish Result:", json.dumps(res, indent=2))

if res.get("success"):
    media_id = res["media_id"]
    permalink = res.get("permalink", f"https://www.instagram.com/reel/{media_id}/")
    now = int(time.time())

    # Update Cloudflare D1
    cf_token = os.getenv("CLOUDFLARE_API_TOKEN")
    cf_account = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    db_id = "f54ea399-d524-45d9-8974-bf4edfb4741a"
    sql = f"UPDATE videos SET ig_status = 'PUBLISHED', ig_media_id = '{media_id}', ig_scheduled_epoch = {now} WHERE video_id = '{vid_id}';"
    url = f"https://api.cloudflare.com/client/v4/accounts/{cf_account}/d1/database/{db_id}/raw"
    data = json.dumps({"sql": sql}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {cf_token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            d1_res = json.loads(resp.read().decode())
            print("D1 Updated:", d1_res.get("success"))
    except Exception as d1_err:
        print("D1 Update Error:", d1_err)

    # Telegram Alert via ARIA
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    tg_chat = os.getenv("TELEGRAM_CHAT_ID")
    if tg_token and tg_chat:
        tg_text = (
            f"📸 *[INSTAGRAM REEL LIVE ON @thebullprint]* 🚀\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🎬 *Reel:* [{title}]({permalink})\n"
            f"🆔 *Media ID:* `{media_id}`\n"
            f"🔗 *Link Hub:* https://tbp-cloudflare-orchestrator.cloudflare-orchestrator.workers.dev/links\n"
            f"▶️ *YouTube:* https://youtu.be/{vid_id}\n"
            f"✨ *Engine:* Meta Resumable Upload + Gemini 2.5 Flash SEO Captions"
        )
        tg_url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
        tg_data = json.dumps({"chat_id": tg_chat, "text": tg_text, "parse_mode": "Markdown"}).encode("utf-8")
        tg_req = urllib.request.Request(tg_url, data=tg_data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(tg_req) as tg_resp:
                print("Telegram Alert Sent!")
        except Exception as tg_err:
            print("Telegram Alert Error:", tg_err)
