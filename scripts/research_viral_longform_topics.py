import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Queries targeting high-retention 10-20 min finance deep dives, scams, and structural mechanics
QUERIES = [
    # Stock Market / Institutional Scandals / Traps
    "stock market scam documentary",
    "sebi f&o loss documentary",
    "how operators manipulate stock price",
    "hindenburg adani report documentary",
    "why retail traders lose money stock market",
    
    # Crypto / On-chain Scandals
    "crypto scam documentary",
    "terra luna crash documentary",
    "binance cz doj documentary",
    "bitcoin halving cycle truth",
    
    # Insurance / Banking Traps
    "health insurance scam india documentary",
    "why insurance claim gets rejected",
    "term insurance truth documentary"
]

results = []
print("Searching for long-format (10-30 min) high-performing videos...")

for q in QUERIES:
    print(f"--> Scanning query: {q}")
    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--flat-playlist",
        "--dump-json",
        "--no-warnings",
        f"ytsearch5:{q}"
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=20)
        if res.returncode == 0 and res.stdout.strip():
            for line in res.stdout.strip().split("\n"):
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    duration = data.get("duration") or 0
                    # Focus on long-format (600s - 3600s = 10 min - 60 min)
                    if duration >= 500:
                        results.append({
                            "id": data.get("id"),
                            "title": data.get("title"),
                            "uploader": data.get("uploader") or data.get("channel"),
                            "duration_min": round(duration / 60.0, 1),
                            "view_count": data.get("view_count") or 0,
                            "url": f"https://www.youtube.com/watch?v={data.get('id')}",
                            "query": q
                        })
                except Exception:
                    continue
    except Exception as e:
        print(f"Error for {q}: {e}")

print(f"Total long-format candidates found: {len(results)}")

# Write to file
Path("data").mkdir(exist_ok=True)
with open("data/longform_candidates.json", "w") as f:
    json.dump(results, f, indent=2)

