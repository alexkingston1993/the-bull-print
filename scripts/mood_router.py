#!/usr/bin/env python3
"""
scripts/mood_router.py

Autonomous Script Sentiment & Intra-Video Mood Router.
Analyzes documentary script narrative beats and generates:
remotion-engine/public/assets/scene_mood_map.json

Themes supported:
- SOLAR_EMPIRE: Sun-drenched, golden-hour, high-key, wealth, empire, luxury, visionary
- HYPER_GROWTH: Crisp modern studio, electric cyan & emerald, high-tech scaling, quantitative trading
- HIGH_STAKES_ARENA: Rich amber & cobalt, market wars, hostile takeovers
- FORENSIC_NOIR: Heavy chiaroscuro, cold shadows, crimson alert, criminal fraud, legal indictment
"""

import json
import os
import re

SCENE_MOOD_MAP_PATH = "remotion-engine/public/assets/scene_mood_map.json"

# Narrative timeline definition for our 36.5s documentary (30 FPS = 1095 frames)
DOCUMENTARY_BEATS = [
    {
        "beat": 1,
        "name": "Penthouse Paradise",
        "startFrame": 0,
        "endFrame": 165,
        "startSec": 0.0,
        "endSec": 5.5,
        "mood": "SOLAR_EMPIRE",
        "script": "High above the crystal-blue waters of Nassau, Bahamas, inside a thirty-million-dollar penthouse.",
        "promptModifier": "Bright sun-drenched golden-hour daytime architectural luxury penthouse overlooking vivid turquoise Caribbean water, gleaming glass windows, warm golden sunlight rays, high-key cinematic lighting, 8k documentary aesthetic",
        "audioProfile": "bright_acoustic"
    },
    {
        "beat": 2,
        "name": "Wall Street Apotheosis",
        "startFrame": 165,
        "endFrame": 345,
        "startSec": 5.5,
        "endSec": 11.5,
        "mood": "HYPER_GROWTH",
        "script": "A mathematical prodigy built what looked like the most secure financial empire on Earth.",
        "promptModifier": "Vivid modern high-tech trading floor, bright crisp studio daylight, glowing emerald and cyan financial data screens, sharp architectural glass, energetic commercial photography",
        "audioProfile": "electric_telemetry"
    },
    {
        "beat": 3,
        "name": "The Next J.P. Morgan & Forbes Cover",
        "startFrame": 345,
        "endFrame": 510,
        "startSec": 11.5,
        "endSec": 17.0,
        "mood": "SOLAR_EMPIRE",
        "script": "Hailed as the next J.P. Morgan, trusted with over sixteen billion dollars in customer deposits.",
        "promptModifier": "Gleaming gold bullion bars, crisp stacks of hundred-dollar bills, bright warm studio illumination, luxury wealth creation, golden hour reflection, immaculate high-key commercial lighting",
        "audioProfile": "bright_shutter"
    },
    {
        "beat": 4,
        "name": "Institutional Sequoia Wire",
        "startFrame": 510,
        "endFrame": 585,
        "startSec": 17.0,
        "endSec": 19.5,
        "mood": "HYPER_GROWTH",
        "script": "Silicon valley royalty poured in hundreds of millions in unvetted capital.",
        "promptModifier": "Crisp alabaster modern venture capital board, bright corporate daylight, sharp emerald confirmation badge, clean architectural lines",
        "audioProfile": "mechanical_strike"
    },
    {
        "beat": 5,
        "name": "The Siphon Exploit (The Dramatic Turn)",
        "startFrame": 585,
        "endFrame": 705,
        "startSec": 19.5,
        "endSec": 23.5,
        "mood": "FORENSIC_NOIR",
        "script": "There was only one problem: a hidden line of code was siphoning billions into a bottomless trading deficit.",
        "promptModifier": "Dark forensic cyber terminal, cracked 3D digital bank vault bleeding glowing red currency streams into a dark deficit abyss, crimson alert lighting, deep shadows",
        "audioProfile": "sub_bass_drop"
    },
    {
        "beat": 6,
        "name": "DOJ Criminal Subpoena Exhibit",
        "startFrame": 705,
        "endFrame": 885,
        "startSec": 23.5,
        "endSec": 29.5,
        "mood": "FORENSIC_NOIR",
        "script": "Allow negative balance. A secret exemption granting total immunity from liquidation.",
        "promptModifier": "Authentic weathered Manila case docket on dark mahogany desk, dramatic overhead detective lamp, red ink stamp CRITICAL EVIDENCE ADMITTED, yellow highlighter on indictment text",
        "audioProfile": "stamp_impact_decay"
    },
    {
        "beat": 7,
        "name": "Server Backdoor",
        "startFrame": 885,
        "endFrame": 990,
        "startSec": 29.5,
        "endSec": 33.0,
        "mood": "FORENSIC_NOIR",
        "script": "When the market turned, the money was already gone.",
        "promptModifier": "Dark cold server room corridor, blinking crimson and amber server rack LEDs, mist, high contrast crime investigation",
        "audioProfile": "tension_drone"
    },
    {
        "beat": 8,
        "name": "Courtroom Climax & Verdict",
        "startFrame": 990,
        "endFrame": 1095,
        "startSec": 33.0,
        "endSec": 36.5,
        "mood": "FORENSIC_NOIR",
        "script": "Guilty on all counts. A thirty-two billion dollar illusion erased forever.",
        "promptModifier": "Dark courtroom shadows, heavy justice gavel on dark oak bench, cold dramatic side spotlight, sub-bass blackout finish",
        "audioProfile": "gavel_slam_blackout"
    }
]

def generate_mood_map():
    os.makedirs(os.path.dirname(SCENE_MOOD_MAP_PATH), exist_ok=True)
    with open(SCENE_MOOD_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(DOCUMENTARY_BEATS, f, indent=2)
    print(f"✅ Generated Scene Mood Map at: {SCENE_MOOD_MAP_PATH}")
    print(f"   Total Beats: {len(DOCUMENTARY_BEATS)}")
    print(f"   Solar Empire Beats (Bright): Beats 1, 3 (Frames 0-165, 345-510)")
    print(f"   Hyper Growth Beats (Vivid Tech): Beats 2, 4 (Frames 165-345, 510-585)")
    print(f"   Dramatic Turn -> Forensic Noir: Beat 5 onwards (Frames 585-1095)")

if __name__ == "__main__":
    generate_mood_map()
