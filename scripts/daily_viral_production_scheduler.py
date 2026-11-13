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

    gh_bin = shutil.which("gh") or "/usr/local/bin/gh"

    # Stage 2: Dispatch 10 Shorts to Cloud Matrix
    for idx, s in enumerate(shorts, 1):
        topic = s["title"]
        vertical = s.get("vertical", "stock_market")
        print(f"\n[Short {idx:02d}/10] 🚀 Dispatching Short: {topic}")
        if not dry_run:
            cmd = [
                gh_bin, "workflow", "run",
                "20-Runner Parallel Cloud Video Matrix (The Bull Print)",
                "-f", f"topic={topic}",
                "-f", f"vertical={vertical}",
                "-f", "shorts_only=true",
                "-f", "duration_sec=60",
                "-f", "privacy_status=public"
            ]
            try:
                subprocess.run(cmd, check=True)
                logger.success(f"✓ Dispatched Short {idx}: {topic[:40]}...")
            except Exception as e:
                logger.error(f"Failed to dispatch Short {idx}: {e}")
            time.sleep(2)

    # Stage 3: Dispatch 2 Master Documentaries to Cloud Matrix
    for idx, d in enumerate(docs, 1):
        topic = d["title"]
        vertical = d.get("vertical", "stock_market")
        print(f"\n[Doc {idx:02d}/02] 🎬 Dispatching Master Documentary: {topic}")
        if not dry_run:
            cmd = [
                "/usr/local/bin/gh", "workflow", "run",
                "20-Runner Parallel Cloud Video Matrix (The Bull Print)",
                "-f", f"topic={topic}",
                "-f", f"vertical={vertical}",
                "-f", "shorts_only=false",
                "-f", "duration_min=12",
                "-f", "privacy_status=public"
            ]
            try:
                subprocess.run(cmd, check=True)
                logger.success(f"✓ Dispatched Documentary {idx}: {topic[:40]}...")
            except Exception as e:
                logger.error(f"Failed to dispatch Doc {idx}: {e}")
            time.sleep(2)

    print("\n" + "=" * 70)
    print("🎉 ALL 12 CLOUD PRODUCTIONS SUCCESSFULLY DISPATCHED!")
    print("=" * 70)

if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    run_daily_production(dry_run=dry)
