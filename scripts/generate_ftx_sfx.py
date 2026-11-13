#!/usr/bin/env python3
"""
scripts/generate_ftx_sfx.py
Synthesizes documentary sound effects for the 12-minute FTX documentary:
- 50Hz sub-bass braams
- 55Hz low tension drones
- Chapter intro acoustic hits
"""

import numpy as np
import wave
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SFX_DIR = BASE_DIR / "output" / "ftx_documentary" / "sfx"
SFX_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE = 44100


def generate_braam():
    dur = 3.0
    n = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, n)
    freq = np.linspace(85, 45, n)
    braam = 0.75 * np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(4 * np.pi * freq * t)
    env = np.exp(-t * 1.2)
    data = (braam * env * 32767).astype(np.int16)
    with wave.open(str(SFX_DIR / "braam_drop.wav"), "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(data.tobytes())
    print("✅ Generated braam_drop.wav")


def generate_tension_drone(duration_sec=160.0):
    n = int(SAMPLE_RATE * duration_sec)
    t = np.linspace(0, duration_sec, n)
    drone = 0.16 * np.sin(2 * np.pi * 55 * t) + 0.08 * np.sin(2 * np.pi * 110 * t) + 0.04 * np.sin(2 * np.pi * 165 * t)
    data = (drone * 32767).astype(np.int16)
    with wave.open(str(SFX_DIR / "tension_drone_chapter.wav"), "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(data.tobytes())
    print("✅ Generated tension_drone_chapter.wav")


def generate_gavel_impact():
    dur = 1.2
    n = int(SAMPLE_RATE * dur)
    t = np.linspace(0, dur, n)
    punch = np.sin(2 * np.pi * 70 * t) * np.exp(-t * 15.0)
    wood = np.sin(2 * np.pi * 280 * t) * np.exp(-t * 25.0)
    noise = np.random.uniform(-0.25, 0.25, n) * np.exp(-t * 30.0)
    data = ((punch * 0.6 + wood * 0.3 + noise * 0.1) * 32767).astype(np.int16)
    with wave.open(str(SFX_DIR / "gavel_slam.wav"), "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(data.tobytes())
    print("✅ Generated gavel_slam.wav")


if __name__ == "__main__":
    generate_braam()
    generate_tension_drone()
    generate_gavel_impact()
