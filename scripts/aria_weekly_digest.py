#!/usr/bin/env python3
"""
scripts/aria_weekly_digest.py
Dispatches the weekly performance and operational digest via Agent ARIA on Telegram.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.aria_enhancements import AriaWeeklyDigest

if __name__ == "__main__":
    print("Dispatching ARIA Weekly Executive Digest...")
    digest_text = AriaWeeklyDigest.generate_digest()
    print("-" * 50)
    print(digest_text)
    print("-" * 50)
    AriaWeeklyDigest.send_weekly_digest()
