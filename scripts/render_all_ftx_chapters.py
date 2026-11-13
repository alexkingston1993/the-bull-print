#!/usr/bin/env python3
"""
scripts/render_all_ftx_chapters.py
Renders chapters 1 through 4, extracts milestone previews,
and compiles the final 12-minute master documentary: ftx_12min_master_documentary.mp4
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.render_ftx_chapter_modular import render_chapter, compile_12min_master

def main():
    print("🚀 Rendering remaining chapters 1 through 4...")
    for cid in range(1, 5):
        render_chapter(cid)
    
    print("\n🔥 All 5 chapters rendered! Compiling final 12-minute master documentary...")
    compile_12min_master()

if __name__ == "__main__":
    main()
