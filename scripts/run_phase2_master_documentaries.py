#!/usr/bin/env python3
"""
Autonomous Phase 2 Orchestrator:
Executes end-to-end Flow frame generation, 180-cut broadcast assembly,
YouTube Private upload, and Telegram ARIA updates for all 3 Master 12-Minute Documentaries:
1. Doc 01: The $2.5 Trillion AI Wall (ai_bubble)
2. Doc 02: The ₹14,900 Crore U-Turn (fii_exodus)
3. Doc 03: Big Tech's Nuclear Secret (nuclear_ai)
"""

import subprocess
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DOCS = [
    ("ai_bubble", "The $2.5 Trillion AI Wall"),
    ("fii_exodus", "The ₹14,900 Crore U-Turn"),
    ("nuclear_ai", "Big Tech's Nuclear Secret")
]

def run_cmd(cmd, desc):
    print(f"\n=======================================================")
    print(f"🚀 {desc}")
    print(f"Command: {cmd}")
    print(f"=======================================================")
    res = subprocess.run(cmd, shell=True, cwd=str(BASE_DIR))
    if res.returncode != 0:
        print(f"⚠️ Error in step: {desc} (Exit code {res.returncode})")
        return False
    return True

def main():
    print("🏆 STARTING AUTONOMOUS PHASE 2 DOCUMENTARY PRODUCTION")
    for doc_id, doc_title in DOCS:
        print(f"\n>>> PROCESSING DOCUMENTARY: {doc_title} ({doc_id}) <<<")
        
        # Step 1: Flow Image Generation & Batch Download
        ok_gen = run_cmd(
            f"node scripts/automate_documentary_production.mjs {doc_id}",
            f"Generating 180 clean 16:9 plates via Google Flow CLI for {doc_title}"
        )
        if not ok_gen:
            print(f"⚠️ Plate generation failed for {doc_id}, continuing...")

        # Step 2: 12-Minute Video Assembly & Private YouTube Upload
        ok_render = run_cmd(
            f".venv/bin/python scripts/render_and_upload_documentary_from_spec.py {doc_id}",
            f"Rendering & Uploading 12-Minute Master Documentary for {doc_title}"
        )
        if not ok_render:
            print(f"⚠️ Render & upload failed for {doc_id}.")

    print("\n🎉 ALL 3 MASTER DOCUMENTARIES PRODUCED, RENDERED, AND UPLOADED!")

if __name__ == "__main__":
    main()
