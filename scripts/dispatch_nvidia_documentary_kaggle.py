#!/usr/bin/env python3
"""
The Bull Print — Autonomous 12-Minute Master Documentary Generator & Kaggle Cloud Dispatcher
Topic: "The Fall of Nvidia: The Secret Investigation That Shocked Wall Street"
Strict Blueprint Compliance:
- Format: 16:9 Landscape (1920x1080)
- Cadence: Exactly 1 bespoke frame every 4.0 seconds (180 frames = 720 seconds = 12 minutes)
- Zero Frame Reuse Mandate: 180 completely unique, non-repeating photographic prompts
- Zero Baked-in Text / Clean Plates
- Dispatched to Kaggle Dual-T4 GPU Runner (100% Cloud Execution)
"""

import sys
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.kaggle_image_worker import KaggleImageWorker

# 36 Narrative Segments (Each 20.0s = 5 bespoke frames @ 4.0s cadence = 180 frames)
ACTS = [
    {
        "act": "Act I: The 8:00 AM Freefall",
        "segments": [
            ("The Breaking Wire", "Wall Street architectural exchange floor, dramatic ambient red illumination, floor traders in sharp dark suits shouting in focused intensity, cinematic photorealistic 35mm, moody ambient lighting"),
            ("Jensen Resignation Alert", "Executive glass boardroom, leather chairs, an empty CEO seat with a lone polished titanium badge on dark mahogany, dramatic morning sunbeams"),
            ("The $500B Liquidity Vanish", "Abstract financial market atmospheric visualization, volumetric bokeh of crimson light beams across obsidian mirrored walls, deep financial tension"),
            ("Silicon Valley Shockwave", "Futuristic Silicon Valley enterprise headquarters exterior at dawn, geometric architectural glass panels reflecting dark storm clouds, cinematic angle"),
            ("Algo Cascades Triggered", "High-frequency server racks with amber status LED lights in a frozen dark cooling room, fiber-optic blue pulse"),
            ("Asian Foundry Turmoil", "Advanced semiconductor cleanroom, robotic mechanical wafer arms holding glowing silicon discs in amber safety lighting, sterile industrial atmosphere"),
            ("The Margin Calls Arrive", "Institutional trading desk, multiple glowing ambient glass monitors, half empty espresso cup, cinematic shadows and high contrast"),
        ]
    },
    {
        "act": "Act II: Inside the Boardroom Audit",
        "segments": [
            ("The Whistleblower Dossier", "Unmarked leather folder on brushed steel table, dramatic low key film noir lighting, sharp shadows"),
            ("Board of Directors Emergency Call", "Private executive dining room, silhouettes of senior directors in heated discussion, misty city skyline in background"),
            ("The Special Committee Formed", "Corporate legal team walking into corporate headquarters lobby, tailored dark suits, heavy architectural shadows"),
            ("Scrutiny of Dual Channels", "Industrial warehouse shipping bay filled with secure metal server flight cases, misty industrial docks at midnight"),
            ("The Executive Conflict", "Glass partition overlooking high-tech engineering laboratory, reflection of two corporate figures in serious dispute, cool cyan tones"),
            ("Audit Logs Unsealed", "Close-up of sleek enterprise server terminal hardware in deep emerald ambient glow, cool moody server room depth"),
            ("The Decision to Cut Ties", "Executive fountain pen resting on polished obsidian desk beside a sealed envelope under focused lamp, historical weight"),
        ]
    },
    {
        "act": "Act III: The Shadow Silicon Route",
        "segments": [
            ("Circumvention in the Desert", "Air cargo freight runway at midnight in desert transit hub, cargo pallets wrapped in protective thermal foil, runway floodlights"),
            ("The Broker Network", "Modern skyscraper luxury office in Singapore, neon city reflections on wet panoramic glass, discreet atmosphere"),
            ("National Security Alarms", "Washington DC government corridor at dusk, grand marble columns, dramatic high contrast shadows"),
            ("Congressional Intel Briefing", "Closed-door legislative committee room with brass microphones on polished walnut table, authoritative setting"),
            ("Tracing the Serial Numbers", "Macro shot of high performance silicon processor die under magnifying inspection glass, gold micro-circuitry pathways"),
            ("Customs Seizure at the Port", "Industrial shipping containers inspected under harsh port floodlights, giant cranes, cargo inspection bay"),
            ("The Secret Singapore Entity", "Front corporate office with frosted architectural glass and minimalist reception desk, dimly lit corporate intrigue"),
        ]
    },
    {
        "act": "Act IV: The S&P Concentration Trap",
        "segments": [
            ("The 7-Stock Monolith", "Giant glass architectural scale balancing one glowing golden geometric emblem against smaller obsidian stones, conceptual financial art"),
            ("The Passive Index Squeeze", "Wall Street bronze bull statue shrouded in early morning fog, dramatic atmospheric gloom, low angle heroic perspective"),
            ("Retail Retirement Accounts Exposed", "Quiet suburban home study at twilight, glowing laptop ambient light reflecting on person in contemplation, emotional human element"),
            ("Venture Capital Freezes", "Silicon Valley modern office courtyard, autumn leaves falling across minimalist concrete architecture, subdued mood"),
            ("Hyperscaler Scramble", "Massive enterprise data center interior, endless rows of illuminated server racks stretching to vanishing point"),
            ("The Power Draw Dilemma", "Electrical substation outside mega data center with high voltage electrical hum, industrial energy infrastructure"),
            ("Wall Street Analysts Capitulate", "Television broadcast studio setting, empty news desk bathed in blue and amber studio floodlights"),
        ]
    },
    {
        "act": "Act V: The Succession War & Future of AI",
        "segments": [
            ("The Interim Crown", "Empty executive corner office, rain droplets running down floor-to-ceiling panoramic glass, blurred city lights below"),
            ("Rival Chipmakers Circle", "Engineering design laboratory with clean silicon wafers under ultraviolet light, intense electric blue illumination"),
            ("Antitrust Inquiries Open", "Neoclassical government building facade with imposing stone pillars under heavy grey overcast skies"),
            ("The AI Bubble Reality Check", "Abstract financial hourglass where glowing golden micro-particles replace sand, cinematic 35mm depth of field"),
            ("TSMC Supply Chain Re-allocation", "Harbor port container terminal with massive container ships loading cargo under dawn sky"),
            ("OpenAI & Hyperscaler Fallout", "Empty modern conference room with glass partition reflecting neural network abstract geometric diagrams"),
            ("The New Dawn of Compute", "Golden sunrise breaking over Silicon Valley mountains, morning light illuminating tech campus buildings, cinematic conclusion"),
            ("The Bull Print Verdict", "High-contrast obsidian stone monolith with clean geometric golden engravings, majestic final frame"),
        ]
    }
]

# Build 180 Bespoke Frames (5 distinct sub-frames for each segment)
MICRO_BEAT_MODIFIERS = [
    ("Establishing Angle", "wide cinematic establishing shot, expansive depth of field, atmospheric haze"),
    ("Forensic Detail", "macro close-up shot, intense focal clarity on textures and documents, dramatic side-lighting"),
    ("Human Drama", "medium dramatic framing, deep emotional tension, cinematic shadows across human expressions"),
    ("Institutional Scale", "towering low-angle perspective, grand architectural scale, authoritative corporate dominance"),
    ("Pivotal Climax", "striking high-contrast hero frame, volumetric light shafts, vivid colour grade, hyper-detailed 8K plate")
]

def generate_manifest():
    frames = []
    frame_id = 1
    
    for act in ACTS:
        for title, core_prompt in act["segments"]:
            for mod_name, mod_style in MICRO_BEAT_MODIFIERS:
                prompt = (
                    f"Cinematic 35mm photograph, {core_prompt}, {mod_style}, "
                    f"dark financial documentary aesthetic, obsidian and amber color grade, "
                    f"clean plate, zero text, zero letters, zero watermark, 8k resolution"
                )
                frames.append({
                    "id": frame_id,
                    "title": f"{title} - {mod_name}",
                    "prompt": prompt,
                    "cadence_sec": 4.0,
                    "aspect_ratio": "16:9"
                })
                frame_id += 1
                if frame_id > 180:
                    break
            if frame_id > 180:
                break
        if frame_id > 180:
            break
            
    return frames[:180]

if __name__ == "__main__":
    manifest = generate_manifest()
    print(f"Generated {len(manifest)} bespoke frames for 12-minute documentary.")
    manifest_path = BASE_DIR / "output" / "nvidia_shockwave_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest written to: {manifest_path}")

    # Dispatch to Kaggle Dual-T4 GPU Runner
    print("Connecting to Kaggle GPU Runner...")
    worker = KaggleImageWorker()
    success = worker.dispatch(manifest)
    if success:
        print("✓ Kaggle GPU Kernel dispatched successfully!")
    else:
        print("❌ Kaggle dispatch failed!")
        sys.exit(1)
