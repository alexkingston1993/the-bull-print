import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

QUERIES = [
    # Stock Market & Institutional Scams / Market Manipulation
    "indian stock market scam documentary",
    "how operators manipulate penny stocks india",
    "sebi options trading loss documentary",
    "yes bank collapse documentary",
    "harshad mehta ketan parekh market truth",
    "adani hindenburg saga deep dive documentary",
    "why 90 percent retail traders lose money in stock market",
    
    # Crypto & On-Chain Scandals / Heists
    "wazirx hack 2000 crore documentary",
    "terra luna do kwon collapse documentary",
    "crypto rug pull documentary",
    "bitcoin whale manipulation spoofing documentary",
    "bybit deribit liquidation cascade",
    
    # Insurance & Financial Traps
    "health insurance claim rejected documentary",
    "why cashless health insurance gets denied",
    "term insurance fraud investigation documentary",
    "bank mis-selling mutual fund insurance documentary"
]

candidates = []
seen_ids = set()

print(f"Executing viral outlier scan across {len(QUERIES)} target queries...")

for q in QUERIES:
    cmd = [
        ".venv/bin/yt-dlp",
        "--flat-playlist",
        "--dump-json",
        "--no-warnings",
        f"ytsearch8:{q}"
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=25)
        if res.returncode == 0 and res.stdout.strip():
            for line in res.stdout.strip().split("\n"):
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    vid_id = data.get("id")
                    if not vid_id or vid_id in seen_ids:
                        continue
                    seen_ids.add(vid_id)
                    
                    duration = data.get("duration") or 0
                    view_count = data.get("view_count") or 0
                    title = data.get("title") or ""
                    channel = data.get("channel") or data.get("uploader") or ""
                    
                    # Target 8 to 45 minutes
                    if 480 <= duration <= 2700 and view_count >= 50000:
                        candidates.append({
                            "id": vid_id,
                            "title": title,
                            "channel": channel,
                            "duration_sec": duration,
                            "duration_min": round(duration / 60.0, 1),
                            "view_count": view_count,
                            "query": q,
                            "url": f"https://www.youtube.com/watch?v={vid_id}"
                        })
                except Exception:
                    continue
    except Exception as e:
        print(f"Error scanning '{q}': {e}")

# Sort by view count descending
candidates.sort(key=lambda x: x["view_count"], reverse=True)
print(f"\nDiscovered {len(candidates)} high-velocity long-format candidates!")

# Save
Path("data").mkdir(exist_ok=True)
with open("data/viral_longform_harvest.json", "w") as f:
    json.dump(candidates, f, indent=2)

print(f"Saved to data/viral_longform_harvest.json")
for idx, c in enumerate(candidates[:15], 1):
    print(f"{idx}. [{c['view_count']:,} views] [{c['duration_min']}m] {c['channel']}: {c['title']} ({c['url']})")

