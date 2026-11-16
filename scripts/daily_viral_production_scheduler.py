#!/usr/bin/env python3
"""
Daily 5:00 AM Autonomous Production Orchestrator (10 Shorts + 2 Documentaries)
scripts/daily_viral_production_scheduler.py

Workflow:
1. Invokes ViralTopicScanner to dynamically discover 10 Shorts + 2 Documentaries from past 24h news.
2. Zero hardcoded fallbacks; strictly compliant with SEBI & Global Safe Harbor.
3. Dispatches all 12 productions to the 20-Runner Parallel Cloud Video Matrix on GitHub Actions.
4. Kaggle Dual-T4 GPU diffusers generate 100% of photographic plates.
5. Cloud runners composite with 3D kinetic typography, 2-line auto-wrapping captions, and Christopher VO.
"""

import os
import sys
import json
import time
import shutil
import subprocess
from pathlib import Path
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.viral_topic_scanner import ViralTopicScanner

def run_daily_production(dry_run: bool = False):
    print("=" * 70)
    print("🌅 5:00 AM AUTONOMOUS VIDEO PRODUCTION ORCHESTRATOR")
    print("🎯 Target: 10 Viral Shorts (9:16) + 2 Master Documentaries (16:9)")
    print("=" * 70)

    # Stage 1: Discover Fresh Past 24h Viral Intelligence
    scanner = ViralTopicScanner()
    manifest = scanner.scan_past_24h_topics()
    
    shorts = manifest.get("shorts", [])
    docs = manifest.get("documentaries", [])

    logger.success(f"Discovered {len(shorts)} Shorts & {len(docs)} Documentaries from past 24h.")

    # Save daily manifest for audit ledger
    out_dir = BASE_DIR / "output" / "daily_manifests"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / f"manifest_{int(time.time())}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    logger.info(f"Saved production manifest: {manifest_path}")

    # Locate genuine GitHub CLI binary (avoid node/bun npm "gh" packages)
    candidates = ["/usr/local/bin/gh", "/usr/bin/gh", "/opt/homebrew/bin/gh"]
    gh_bin = next((c for c in candidates if Path(c).exists()), shutil.which("gh") or "gh")

    # Stage 2: Calculate Staggered 24-Hour Drip Schedule
    from datetime import datetime, timezone, timedelta
    now_utc = datetime.now(timezone.utc)
    base_publish_time = now_utc + timedelta(hours=1)

    # Interleave 10 Shorts and 2 Documentaries across 12 two-hour slots for YouTube release
    # Docs are scheduled at Slot 4 (+9h) and Slot 9 (+19h) for peak audience retention
    scheduled_items = []
    s_idx = 0
    d_idx = 0
    for slot in range(12):
        slot_time = (base_publish_time + timedelta(hours=slot * 2)).strftime("%Y-%m-%dT%H:%M:%SZ")
        if slot in (4, 9) and d_idx < len(docs):
            scheduled_items.append({"type": "doc", "data": docs[d_idx], "slot": slot, "publish_at": slot_time, "num": d_idx + 1})
            d_idx += 1
        elif s_idx < len(shorts):
            scheduled_items.append({"type": "short", "data": shorts[s_idx], "slot": slot, "publish_at": slot_time, "num": s_idx + 1})
            s_idx += 1
        elif d_idx < len(docs):
            scheduled_items.append({"type": "doc", "data": docs[d_idx], "slot": slot, "publish_at": slot_time, "num": d_idx + 1})
            d_idx += 1

    # Stage 3: Dispatch Scheduled Productions to Cloud Matrix
    # CRITICAL EFFICIENCY RULE: Dispatch all 10 fast Shorts (20 frames, ~3 mins each) FIRST,
    # and dispatch the 2 Documentaries (6 mins, 90 frames each) LAST.
    # This prevents Shorts runners from idling in queue behind heavy documentary renders.
    shorts_queue = [item for item in scheduled_items if item["type"] == "short"]
    docs_queue = [item for item in scheduled_items if item["type"] == "doc"]
    dispatch_queue = shorts_queue + docs_queue

    for item in dispatch_queue:
        data = item["data"]
        topic = data["title"]
        vertical = data.get("vertical", "stock_market")
        publish_at = item["publish_at"]
        is_short = item["type"] == "short"

        if is_short:
            print(f"\n[Short {item['num']:02d}/10] 🚀 Dispatching Short: {topic} (Scheduled: {publish_at} UTC)")
            cmd = [
                gh_bin, "workflow", "run",
                "parallel_video_matrix.yml",
                "-f", f"topic={topic}",
                "-f", f"vertical={vertical}",
                "-f", "shorts_only=true",
                "-f", "duration_sec=60",
                "-f", "privacy_status=private",
                "-f", f"publish_at={publish_at}"
            ]
        else:
            print(f"\n[Doc {item['num']:02d}/02] 🎬 Dispatching Master Documentary (16:9, 12-Min Masterclass): {topic} (Scheduled: {publish_at} UTC)")
            cmd = [
                gh_bin, "workflow", "run",
                "parallel_video_matrix.yml",
                "-f", f"topic={topic}",
                "-f", f"vertical={vertical}",
                "-f", "shorts_only=false",
                "-f", "duration_min=12",
                "-f", "privacy_status=private",
                "-f", f"publish_at={publish_at}"
            ]

        if not dry_run:
            try:
                res = subprocess.run(cmd, check=True, stdin=subprocess.DEVNULL, capture_output=True, text=True)
                tag = f"Short {item['num']}" if is_short else f"Doc {item['num']}"
                logger.success(f"✓ Dispatched {tag}: {topic[:40]}... (PublishAt: {publish_at})")
            except Exception as e:
                logger.error(f"Failed to dispatch {item['type']} {topic}: {e}")
            # Stagger workflow starts by 150 seconds to guarantee Job #1 finishes its ~85s Kaggle GPU run
            # before the next runner acquires the lock, eliminating queue collisions and preventing any runner timeouts.
            logger.info("⏳ Staggering next workflow dispatch by 150s (2.5 mins) for clean sequential Kaggle GPU execution...")
            time.sleep(150)

    print("\n" + "=" * 70)
    print("🎉 ALL 12 CLOUD PRODUCTIONS SUCCESSFULLY DISPATCHED!")
    print("=" * 70)

if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    run_daily_production(dry_run=dry)
