#!/usr/bin/env python3
"""
Batch Re-render and QC Audit for Viral Shorts 02 through 10.
Executes the continuous subpixel smooth zoom engine, produces master videos,
and executes the 3-pass Quality Control audit.
"""
import sys
import json
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.produce_and_qc_10_viral_shorts import SHORTS_SPEC, render_short_video, run_triple_check_qc

def main():
    print("=" * 80)
    print("🚀 BATCH RE-RENDERING SHORTS 02 THROUGH 10 (SMOOTH SUBPIXEL ZOOM ENGINE)")
    print("=" * 80)
    
    results = []
    
    # Render shorts 02 through 10 (index 1 to 9)
    for idx, item in enumerate(SHORTS_SPEC[1:], start=1):
        s_id = item["id"]
        print(f"\n🎬 [{idx+1}/10] Processing {s_id}: {item['title']}...")
        master_path = render_short_video(item, idx)
        
        print(f"🔍 Running 3-Pass QC Audit on {s_id}...")
        qc_res = run_triple_check_qc(item)
        results.append(qc_res)
        
        status = "PASSED" if qc_res["passed"] else "FAILED"
        print(f"👉 Result: {status} | Duration: {qc_res['duration']:.2f}s | Sync Delta: {qc_res['sync_delta']:.3f}s | Cadence: {qc_res['avg_cut_cadence']}s/cut ({qc_res['cuts_count']} cuts)")
        if not qc_res["passed"]:
            for err in qc_res["errors"]:
                print(f"   ❌ {err}")
                
    print("\n" + "=" * 80)
    print("📊 BATCH RE-RENDER & QC AUDIT COMPLETE")
    print("=" * 80)
    for r in results:
        st = "✅ PASSED" if r["passed"] else "❌ FAILED"
        print(f"{st} | {r['id']:<35} | {r['duration']:>5.2f}s | Delta: {r['sync_delta']:>5.3f}s | Cuts: {r['cuts_count']} ({r['avg_cut_cadence']}s/cut)")
        
    with open(ROOT / "output/viral_shorts_past24h/qc_audit_batch_02_10.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
