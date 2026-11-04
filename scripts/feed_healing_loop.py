#!/usr/bin/env python3
"""
The Bull Print - Autonomous Continuous Learning Feedback Loop
scripts/feed_healing_loop.py

Feeds any bug fix or discovered runtime exception directly into Agent Aria's
Self-Healing Cognitive Vault (app/config/healing_vault.json).

Usage:
  # Feed a specific bug fix:
  python scripts/feed_healing_loop.py --pattern "No module named 'xyz'" --action "pip install xyz" --exec "pip install xyz"

  # Sync all historical or recent bug fixes from git commits:
  python scripts/feed_healing_loop.py --sync-git

  # Display the current cognitive knowledge vault report:
  python scripts/feed_healing_loop.py --report

  # Test diagnose an error log against all learned rules:
  python scripts/feed_healing_loop.py --diagnose "FileNotFoundError: Missing rendered segment..."
"""

import sys
import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.aria_healing import AriaSelfHealingEngine


def main():
    parser = argparse.ArgumentParser(description="Aria Autonomous Continuous Learning Feedback Loop")
    parser.add_argument("--pattern", type=str, help="Regex / signature pattern of the bug")
    parser.add_argument("--action", type=str, help="Prescribed remediation action plan")
    parser.add_argument("--domain", type=str, default="runner_dependencies", help="Failure domain")
    parser.add_argument("--exec", type=str, dest="auto_exec", help="Auto-executable shell command (e.g. pip install ...)")
    parser.add_argument("--component", type=str, default="Pipeline Component", help="Failed component name")
    parser.add_argument("--cause", type=str, default="Discovered operational defect", help="Root cause explanation")
    parser.add_argument("--sync-git", action="store_true", help="Ingest bug fixes from repository git commits")
    parser.add_argument("--report", action="store_true", help="Show full knowledge vault telemetry report")
    parser.add_argument("--diagnose", type=str, help="Diagnose an error snippet against all learned rules")
    parser.add_argument("--persist-git", action="store_true", help="Commit and push updated knowledge vault to origin main")

    args = parser.parse_args()

    if args.pattern and args.action:
        rule = AriaSelfHealingEngine.feed_bug_fix(
            signature_pattern=args.pattern,
            action_plan=args.action,
            domain=args.domain,
            root_cause=args.cause,
            failed_component=args.component,
            auto_executable=args.auto_exec,
            learned_from="feed_healing_loop CLI",
            severity="HIGH"
        )
        print(f"\n✅ [Aria Continuous Learning] Learned Bug Fix Rule: {rule.get('rule_id')}")
        print(json.dumps(rule, indent=2))
        if args.persist_git:
            AriaSelfHealingEngine.persist_to_git(f"chore(healing): learn bug fix {rule.get('rule_id')}")

    elif args.sync_git:
        new_rules = AriaSelfHealingEngine.sync_from_git_commits(limit=100)
        print(f"\n🔄 [Aria Git Sync] Complete: Learned {len(new_rules)} new rules from git commits.")
        for r in new_rules:
            print(f" • [{r.get('rule_id')}] {r.get('domain')}: {r.get('action_plan')}")
        if args.persist_git and new_rules:
            AriaSelfHealingEngine.persist_to_git(f"chore(healing): ingest {len(new_rules)} fixes from git history")

    elif args.diagnose:
        remedy = AriaSelfHealingEngine.diagnose(args.diagnose)
        print(f"\n🩺 [Aria Diagnosis Result]:")
        print(f" • Domain: {remedy.domain.value}")
        print(f" • Rule ID: {remedy.rule_id or 'Auto-Learned'}")
        print(f" • Root Cause: {remedy.root_cause}")
        print(f" • Action: {remedy.action_plan}")
        print(f" • Auto-Executable: {remedy.auto_executable}")

    elif args.report:
        print("\n" + AriaSelfHealingEngine.get_learning_report())

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
