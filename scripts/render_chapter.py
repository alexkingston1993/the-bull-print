#!/usr/bin/env python3
"""
Single-Command Chapter Pipeline Runner
Usage:
    python scripts/render_chapter.py --chapter 1 --mode short
    python scripts/render_chapter.py --chapter 1 --mode 16x9
"""

import os
import sys
import argparse
import subprocess

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description="Render parameterized chapter through Remotion")
    parser.add_argument("--chapter", type=int, default=1, help="Chapter number (1 to 12)")
    parser.add_argument("--mode", choices=["short", "16x9", "both"], default="16x9", help="Aspect ratio mode")
    parser.add_argument("--concurrency", type=int, default=6, help="Remotion render concurrency")
    parser.add_argument("--crf", type=int, default=16, help="H.264 CRF quality")
    args = parser.parse_args()

    remotion_dir = os.path.join(WORKSPACE_DIR, "remotion-engine")
    output_dir = os.path.join(WORKSPACE_DIR, "output")
    os.makedirs(output_dir, exist_ok=True)

    print(f"🎬 PARAMETERIZED REMOTION PIPELINE")
    print(f"   Chapter: {args.chapter:02d}")
    print(f"   Mode: {args.mode}")

    # Step 1: Generate chapter manifest
    print("\n📦 Generating Chapter Manifest...")
    gen_cmd = [
        os.path.join(WORKSPACE_DIR, ".venv", "bin", "python"),
        os.path.join(WORKSPACE_DIR, "scripts", "generate_chapter_manifest.py")
    ]
    res = subprocess.run(gen_cmd)
    if res.returncode != 0:
        print("❌ Failed to generate manifest")
        sys.exit(1)

    # Step 2: Render
    compositions = []
    if args.mode in ["16x9", "both"]:
        compositions.append(("ChapterMaster", f"../output/chapter_{args.chapter:02d}_master_16x9.mp4"))
    if args.mode in ["short", "both"]:
        compositions.append(("ChapterShortMaster", f"../output/chapter_{args.chapter:02d}_master_short.mp4"))

    for comp, out_file in compositions:
        print(f"\n🎥 Rendering composition: {comp} -> {out_file}")
        cmd = [
            "npx", "remotion", "render",
            "src/index.ts", comp, out_file,
            f"--codec=h264",
            f"--crf={args.crf}",
            f"--concurrency={args.concurrency}"
        ]
        render_res = subprocess.run(cmd, cwd=remotion_dir)
        if render_res.returncode != 0:
            print(f"❌ Failed rendering {comp}")
            sys.exit(render_res.returncode)

    print("\n✨ All renders completed successfully!")

if __name__ == "__main__":
    main()
