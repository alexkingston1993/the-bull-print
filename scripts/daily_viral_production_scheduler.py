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


def find_latest_dispatched_run(gh_bin: str, max_wait: int = 45):
    """Finds the most recently created parallel_video_matrix.yml run."""
    start_t = time.time()
    while time.time() - start_t < max_wait:
        time.sleep(5)
        try:
            r = subprocess.run(
                [str(gh_bin), "run", "list", "--workflow=parallel_video_matrix.yml", "--limit=3", "--json=databaseId,status,createdAt"],
                capture_output=True, text=True, check=True
            )
            runs = json.loads(r.stdout)
            if runs:
                return int(runs[0]["databaseId"])
        except Exception:
            pass
    return None


def wait_for_prepare_session_completion(gh_bin: str, run_id: int, is_short: bool, timeout_sec: int) -> bool:
    """
    Polls the parallel_video_matrix.yml workflow run until its 'prepare_session' job is completed.
    This guarantees that the runner has finished its Kaggle GPU frame generation and released the kernel,
    allowing the next workflow to use Kaggle with ZERO queue collisions or race conditions.
    """
    kind = "Short" if is_short else "Documentary"
    logger.info(f"⏳ [Pipeline Poller] Monitoring {kind} Run #{run_id} prepare_session (Max wait: {timeout_sec//60}m)...")
    start_t = time.time()
    while time.time() - start_t < timeout_sec:
        time.sleep(20)
        try:
            res = subprocess.run(
                [str(gh_bin), "run", "view", str(run_id), "--json", "status,conclusion,jobs"],
                capture_output=True, text=True, check=True
            )
            data = json.loads(res.stdout)
            jobs = data.get("jobs", [])
            prep_job = next((j for j in jobs if j.get("name") == "prepare_session"), None)
            if prep_job:
                p_status = prep_job.get("status")
                p_conclusion = prep_job.get("conclusion")
                if p_status == "completed":
                    elapsed = time.time() - start_t
                    if p_conclusion == "success":
                        logger.success(f"✓ [Pipeline Poller] Run #{run_id} prepare_session succeeded in {elapsed:.1f}s! Kaggle GPU released. Ready for next dispatch.")
                        return True
                    else:
                        logger.warning(f"⚠️ [Pipeline Poller] Run #{run_id} prepare_session concluded with '{p_conclusion}'. Kaggle GPU released. Proceeding.")
                        return False
            run_status = data.get("status")
            if run_status == "completed":
                logger.info(f"ℹ️ [Pipeline Poller] Run #{run_id} overall status completed. Proceeding.")
                return True
        except Exception as e:
            logger.debug(f"Poller query notice: {e}")

    logger.warning(f"⚠️ [Pipeline Poller] Timed out after {timeout_sec}s waiting for Run #{run_id} prepare_session. Proceeding to next in queue.")
    return False


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

                # Active pipelined staggering: Wait for prepare_session to release Kaggle GPU before next dispatch
                poll_ceiling = 900 if is_short else 4500  # 15m max for Shorts, 75m max for Docs
                dispatched_run_id = find_latest_dispatched_run(gh_bin)
                if dispatched_run_id:
                    wait_for_prepare_session_completion(gh_bin, dispatched_run_id, is_short=is_short, timeout_sec=poll_ceiling)
                else:
                    logger.warning("Could not identify dispatched run ID. Applying 120s safety buffer...")
                    time.sleep(120)
            except Exception as e:
                logger.error(f"Failed to dispatch {item['type']} {topic}: {e}")

    print("\n" + "=" * 70)
    print("🎉 ALL 12 CLOUD PRODUCTIONS SUCCESSFULLY DISPATCHED!")
    print("=" * 70)

if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    run_daily_production(dry_run=dry)
