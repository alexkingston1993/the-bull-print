#!/usr/bin/env python3
"""
Build upgraded public/crypto.html (dual directory + single asset view)
and public/crypto-radar.html (new & upcoming crypto tracker).
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Read existing crypto.html to preserve styling and global navbar
with open(ROOT / 'public/crypto.html', 'r', encoding='utf-8') as f:
    orig_html = f.read()

print("Original crypto.html length:", len(orig_html))
