#!/usr/bin/env python3
"""
Relentless Daily 16 Video Dispatcher for 'The Bull Print'.
Zero external dependencies (pure standard library).
Dispatches the 16-video daily production matrix (6 Long-Form + 10 Shorts)
across the 6 operational slots using exclusively the 20-runner parallel cloud matrix.

Strictly Christopher cloned voice. Dynamic visual plates per segment. Zero local compute.
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
GH_REPO = "alexkingston1993/the-bull-print"
GH_CLI = "/usr/local/bin/gh"

DAILY_16_SCHEDULE: List[Dict] = [
    # ── SLOT 1: STOCK PRE-OPEN (3 Videos) ──────────────────────────────────
    {
        "id": "s1_long",
        "slot": 1,
        "format": "long",
        "vertical": "stock_market",
        "topic": "Nifty Bank Opening Range Absorption & FII Order Flow",
        "duration_min": "3",
        "duration_sec": "60",
        "is_short": False,
        "already_live_url": "https://youtu.be/7-xTYDswMHk",
    },
    {
        "id": "s1_short1",
        "slot": 1,
        "format": "short",
        "vertical": "stock_market",
        "topic": "The 9:15 AM Institutional Opening Trap Exposed",
        "duration_min": "1",
        "duration_sec": "58",
        "is_short": True,
        "already_live_url": "https://youtu.be/j3rbEsPZONk",
    },
    {
        "id": "s1_short2",
        "slot": 1,
        "format": "short",
        "vertical": "stock_market",
        "topic": "Nifty 50 Liquidity Sweep Rules & Institutional Stop Hunts",
        "duration_min": "1",
        "duration_sec": "58",
        "is_short": True,
    },
    # ── SLOT 2: CRYPTO MORNING (3 Videos) ──────────────────────────────────
    {
        "id": "s2_long",
        "slot": 2,
        "format": "long",
        "vertical": "crypto",
        "topic": "Bitcoin Liquidation Cluster Map & Funding Stress Mechanics",
        "duration_min": "3",
        "duration_sec": "60",
        "is_short": False,
    },
    {
        "id": "s2_short1",
        "slot": 2,
        "format": "short",
        "vertical": "crypto",
        "topic": "Ethereum Gas Spike Front-Running Explained",
        "duration_min": "1",
        "duration_sec": "58",
        "is_short": True,
    },
    {
        "id": "s2_short2",
        "slot": 2,
        "format": "short",
        "vertical": "crypto",
        "topic": "Solana Orderbook Spread Compression & MEV Extraction",
        "duration_min": "1",
        "duration_sec": "58",
        "is_short": True,
    },
    # ── SLOT 3: INSURANCE FORENSICS (3 Videos) ─────────────────────────────
    {
        "id": "s3_long",
        "slot": 3,
        "format": "long",
        "vertical": "insurance",
        "topic": "Health Insurance Room-Rent Deduction Traps & Hidden Clauses",
        "duration_min": "3",
        "duration_sec": "60",
        "is_short": False,
    },
    {
        "id": "s3_short1",
        "slot": 3,
        "format": "short",
        "vertical": "insurance",
        "topic": "Co-Payment Clause Traps Exposed: What Hospitals Hide",
        "duration_min": "1",
        "duration_sec": "58",
        "is_short": True,
    },
    {
        "id": "s3_short2",
        "slot": 3,
        "format": "short",
        "vertical": "insurance",
        "topic": "Consumables Exclusion in Cashless Hospital Claims",
        "duration_min": "1",
        "duration_sec": "58",
        "is_short": True,
    },
    # ── SLOT 4: STOCK CLOSING BELL (3 Videos) ──────────────────────────────
    {
        "id": "s4_long",
        "slot": 4,
        "format": "long",
        "vertical": "stock_market",
        "topic": "FII Closing-Session Flows & Option Ring Reading",
        "duration_min": "3",
        "duration_sec": "60",
        "is_short": False,
    },
    {
        "id": "s4_short1",
        "slot": 4,
        "format": "short",
        "vertical": "stock_market",
        "topic": "VWAP Institutional Reclaim Patterns on 5-Minute Charts",
        "duration_min": "1",
        "duration_sec": "58",
        "is_short": True,
    },
    {
        "id": "s4_short2",
        "slot": 4,
        "format": "short",
        "vertical": "stock_market",
        "topic": "Gamma Squeeze Trigger Points in Weekly Expiry Trading",
        "duration_min": "1",
        "duration_sec": "58",
        "is_short": True,
    },
    # ── SLOT 5: CRYPTO EVENING (2 Videos) ──────────────────────────────────
    {
        "id": "s5_long",
        "slot": 5,
        "format": "long",
        "vertical": "crypto",
        "topic": "Ethereum CVD Divergence & Exchange Reserve Exits",
        "duration_min": "3",
        "duration_sec": "60",
        "is_short": False,
    },
    {
        "id": "s5_short1",
        "slot": 5,
        "format": "short",
        "vertical": "crypto",
        "topic": "Flash Loan Arbitrage Mechanics & On-Chain Slippage",
        "duration_min": "1",
        "duration_sec": "58",
        "is_short": True,
    },
    # ── SLOT 6: INSURANCE NIGHT (2 Videos) ─────────────────────────────────
    {
        "id": "s6_long",
        "slot": 6,
        "format": "long",
        "vertical": "insurance",
        "topic": "CSR vs Incurred Claim Ratio Forensics for Policyholders",
        "duration_min": "3",
        "duration_sec": "60",
        "is_short": False,
    },
    {
        "id": "s6_short1",
        "slot": 6,
        "format": "short",
        "vertical": "insurance",
        "topic": "Pre-Existing Disease 3-Year Moratorium Myth Unpacked",
        "duration_min": "1",
        "duration_sec": "58",
        "is_short": True,
    },
]


def log_info(msg: str):
    print(f"[\033[94mINFO\033[0m] {msg}", flush=True)


def log_success(msg: str):
    print(f"[\033[92mSUCCESS\033[0m] {msg}", flush=True)


def log_warn(msg: str):
    print(f"[\033[93mWARNING\033[0m] {msg}", flush=True)


def log_error(msg: str):
    print(f"[\033[91mERROR\033[0m] {msg}", flush=True)


def get_gh_token() -> str:
    """Retrieves GitHub PAT token from environment or gh auth token."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token and os.path.exists(GH_CLI):
        try:
            res = subprocess.run([GH_CLI, "auth", "token"], capture_output=True, text=True, check=True)
            token = res.stdout.strip()
        except Exception:
            pass
    return token or ""


def dispatch_item(item: Dict, privacy_status: str = "unlisted") -> bool:
    """Dispatches a single video item to GitHub Actions parallel_video_matrix."""
    shorts_only = "true" if item["is_short"] else "false"
    topic = item["topic"]
    vertical = item["vertical"]
    duration_sec = item.get("duration_sec", "60")
    duration_min = item.get("duration_min", "3")

    log_info(
        f"🚀 Dispatching [{item['id']}] Slot {item['slot']} ({item['format'].upper()}): "
        f"'{topic}' [{vertical}]"
    )

    # Method A: System GitHub CLI (/usr/local/bin/gh)
    if os.path.exists(GH_CLI):
        cmd = [
            GH_CLI, "workflow", "run", "parallel_video_matrix.yml",
            "-f", f"topic={topic}",
            "-f", f"vertical={vertical}",
            "-f", f"shorts_only={shorts_only}",
            "-f", f"duration_sec={duration_sec}",
            "-f", f"duration_min={duration_min}",
            "-f", f"privacy_status={privacy_status}",
        ]
        try:
            res = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True, check=True)
            log_success(f"✓ Queued successfully via gh CLI: {item['id']}")
            return True
        except subprocess.CalledProcessError as e:
            log_warn(f"gh CLI dispatch error: {e.stderr.strip() if e.stderr else e.stdout.strip()}")

    # Method B: Pure Python urllib REST API fallback
    token = get_gh_token()
    if not token:
        log_error("No GitHub token found to dispatch workflow.")
        return False

    url = f"https://api.github.com/repos/{GH_REPO}/actions/workflows/parallel_video_matrix.yml/dispatches"
    payload = json.dumps({
        "ref": "main",
        "inputs": {
            "topic": topic,
            "vertical": vertical,
            "shorts_only": shorts_only,
            "duration_sec": duration_sec,
            "duration_min": duration_min,
            "privacy_status": privacy_status,
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
            "User-Agent": "TheBullPrint-Relentless-Dispatcher",
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            if resp.status == 204:
                log_success(f"✓ Queued successfully via REST API: {item['id']}")
                return True
            log_error(f"Failed dispatch {item['id']}: HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        log_error(f"HTTPError dispatching {item['id']}: {e.code} - {e.read().decode('utf-8')}")
    except Exception as e:
        log_error(f"Exception dispatching {item['id']}: {e}")
    return False


def get_active_runs_count() -> int:
    """Returns the number of currently active/in_progress matrix runs."""
    if not os.path.exists(GH_CLI):
        return 0
    try:
        res = subprocess.run(
            [GH_CLI, "run", "list", "--workflow=parallel_video_matrix.yml", "--status=in_progress", "--json", "id"],
            capture_output=True, text=True, check=True
        )
        runs = json.loads(res.stdout)
        return len(runs)
    except Exception:
        return 0


def main():
    parser = argparse.ArgumentParser(description="Daily 16 Video Production Dispatcher")
    parser.add_argument("--all", action="store_true", help="Dispatch all 16 items (skipping already live items)")
    parser.add_argument("--slot", type=int, choices=[1, 2, 3, 4, 5, 6], help="Dispatch only items for a specific slot")
    parser.add_argument("--format", choices=["long", "short"], help="Filter by format")
    parser.add_argument("--batch-size", type=int, default=3, help="Max concurrent workflow dispatches at once")
    parser.add_argument("--delay-sec", type=int, default=15, help="Delay between dispatches to allow runner scaling")
    parser.add_argument("--privacy", default="unlisted", choices=["public", "unlisted", "private"])
    parser.add_argument("--status", action="store_true", help="Print schedule overview and current live status")
    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("🎬 THE BULL PRINT - DAILY 16 CLOUD VIDEO DISPATCHER")
    print("=" * 70 + "\n")

    items_to_run = []
    for item in DAILY_16_SCHEDULE:
        if args.slot and item["slot"] != args.slot:
            continue
        if args.format and item["format"] != args.format:
            continue
        items_to_run.append(item)

    if args.status or not (args.all or args.slot or args.format):
        print(f"Total Daily Schedule: {len(DAILY_16_SCHEDULE)} videos (6 Long-form + 10 Shorts)\n")
        completed = 0
        for item in DAILY_16_SCHEDULE:
            live = item.get("already_live_url")
            status_str = f"✅ LIVE: {live}" if live else "⏳ PENDING"
            if live:
                completed += 1
            print(f"  Slot {item['slot']} [{item['format'].upper():5s}] {item['id']:10s} | {item['topic'][:45]:45s} | {status_str}")
        print(f"\nProgress: {completed}/{len(DAILY_16_SCHEDULE)} completed today.")
        if not (args.all or args.slot or args.format):
            print("\nUse --all to dispatch remaining items, or --slot <N> to run a specific slot.")
            return

    # Dispatch pending items
    dispatched = 0
    for item in items_to_run:
        if item.get("already_live_url") and not getattr(args, "force", False):
            log_info(f"⏭ Skipping already verified live item: {item['id']} ({item.get('already_live_url')})")
            continue

        # Throttling to prevent runner contention
        active = get_active_runs_count()
        while active >= args.batch_size:
            log_info(f"⏳ {active} workflows active in cloud matrix. Waiting 30s before dispatching next...")
            time.sleep(30)
            active = get_active_runs_count()

        success = dispatch_item(item, privacy_status=args.privacy)
        if success:
            dispatched += 1
            if args.delay_sec > 0:
                time.sleep(args.delay_sec)

    log_success(f"🏁 Finished dispatch pass! {dispatched} new workflow(s) dispatched to Cloud Matrix.")


if __name__ == "__main__":
    main()
