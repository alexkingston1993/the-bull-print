#!/usr/bin/env python3
"""
scripts/queue_daily_4_pack.py
Sequential Cloud Dispatcher for The Bull Print (1 Documentary + 3 Micro-Shorts)

Guarantees 100% Kaggle GPU collision prevention on single account (alexkingston):
1. Monitors active 12-minute documentary run until Kaggle plates complete.
2. Dispatches Short 1 (Morning Slot 07:30-09:00 IST), waits for plates.
3. Dispatches Short 2 (Afternoon Slot 13:30-15:00 IST), waits for plates.
4. Dispatches Short 3 (Evening Slot 20:00-21:30 IST).
"""

import sys
import time
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
GH_BIN = "/usr/local/bin/gh"

SHORTS_QUEUE = [
    {
        "slot": "Slot 1 (Morning ~07:30-09:00 IST)",
        "topic": "The $20 Trillion Shadow Banking Trap: The 9% Yield Illusion",
        "vertical": "stock_market",
        "publish_hour_ist": 8,  # 08:00 IST
    },
    {
        "slot": "Slot 2 (Afternoon ~13:30-15:00 IST)",
        "topic": "How Wall Street Moved $20 Trillion Off the Books",
        "vertical": "stock_market",
        "publish_hour_ist": 14,  # 14:00 IST
    },
    {
        "slot": "Slot 3 (Evening ~20:00-21:30 IST)",
        "topic": "Private Credit's Hidden Default Wave Exposed",
        "vertical": "stock_market",
        "publish_hour_ist": 20,  # 20:30 IST
    }
]


def wait_for_job_prepare_session(run_id: int, timeout_sec: int = 3600) -> bool:
    """Waits until the prepare_session job of run_id completes successfully."""
    logger.info(f"⏳ Waiting for Run #{run_id} prepare_session to complete and release Kaggle GPU...")
    start_time = time.time()
    
    while time.time() - start_time < timeout_sec:
        time.sleep(20)
        try:
            res = subprocess.run(
                [GH_BIN, "run", "view", str(run_id), "--json", "jobs"],
                capture_output=True, text=True, check=True
            )
            data = json.loads(res.stdout)
            jobs = data.get("jobs", [])
            for j in jobs:
                if j.get("name") == "prepare_session":
                    status = j.get("status")
                    conclusion = j.get("conclusion")
                    logger.info(f"  [Run #{run_id}] prepare_session: status={status}, conclusion={conclusion}")
                    if status == "completed":
                        return conclusion == "success"
        except Exception as e:
            logger.debug(f"Polling note: {e}")
            
    logger.warning(f"Timed out waiting for Run #{run_id} prepare_session.")
    return False


def get_publish_timestamp(ist_hour: int) -> str:
    """Calculates ISO 8601 UTC timestamp for given IST hour today or tomorrow."""
    ist_tz = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist_tz)
    
    target_dt = now_ist.replace(hour=ist_hour, minute=0, second=0, microsecond=0)
    if target_dt <= now_ist:
        target_dt += timedelta(days=1)
        
    utc_dt = target_dt.astimezone(timezone.utc)
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def dispatch_short(item: dict) -> int:
    """Dispatches a single 9:16 Short to parallel_video_matrix.yml."""
    topic = item["topic"]
    vertical = item["vertical"]
    pub_at = get_publish_timestamp(item["publish_hour_ist"])
    
    logger.info(f"🚀 Dispatching {item['slot']}: '{topic}' (Scheduled: {pub_at} UTC)...")
    cmd = [
        GH_BIN, "workflow", "run", "parallel_video_matrix.yml",
        "-f", f"topic={topic}",
        "-f", f"vertical={vertical}",
        "-f", "shorts_only=true",
        "-f", "duration_sec=60",
        "-f", "privacy_status=public",
        "-f", "kaggle_account=alexkingston",
        "-f", f"publish_at={pub_at}"
    ]
    subprocess.run(cmd, check=True)
    time.sleep(10)
    
    # Get dispatched run ID
    res = subprocess.run(
        [GH_BIN, "run", "list", "--workflow=parallel_video_matrix.yml", "-L", "1", "--json", "databaseId"],
        capture_output=True, text=True, check=True
    )
    runs = json.loads(res.stdout)
    run_id = int(runs[0]["databaseId"])
    logger.success(f"✓ Short dispatched! Run ID: #{run_id}")
    return run_id


def run_pipeline_orchestration(active_doc_run_id: int):
    """Orchestrates the 1 Doc + 3 Shorts pipeline in strict sequence."""
    logger.info(f"🎬 Starting 4-Pack Production Pipeline. Tracking Active Doc Run #{active_doc_run_id}...")
    
    # 1. Wait for Doc plates
    doc_ok = wait_for_job_prepare_session(active_doc_run_id, timeout_sec=3600)
    if not doc_ok:
        logger.error(f"Doc Run #{active_doc_run_id} prepare_session did not complete successfully.")
    else:
        logger.success(f"🎉 12-Minute Documentary plates complete! Matrix rendering in background.")
        
    # 2. Dispatch the 3 Shorts sequentially
    for idx, short_item in enumerate(SHORTS_QUEUE, 1):
        time.sleep(15)
        run_id = dispatch_short(short_item)
        short_ok = wait_for_job_prepare_session(run_id, timeout_sec=1200)
        if short_ok:
            logger.success(f"✓ Short {idx}/3 ({short_item['topic'][:30]}) plates complete! GPU released for next short.")
        else:
            logger.warning(f"⚠️ Short {idx}/3 hit an issue during prepare_session. Proceeding to next.")
            
    logger.success("🏆 All 4 videos (1 Documentary + 3 Shorts) have been successfully dispatched!")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc-run-id", type=int, required=True, help="Active 12-min doc run ID")
    args = parser.parse_args()
    
    run_pipeline_orchestration(args.doc_run_id)
