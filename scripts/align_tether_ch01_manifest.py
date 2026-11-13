"""
scripts/align_tether_ch01_manifest.py

Generates word timestamps from chapter_01.mp3 using faster-whisper and builds
the complete 12-beat parameterized ChapterManifest for Tether Chapter 1.
"""

import json
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import math
from pathlib import Path

AUDIO_PATH = "remotion-engine/public/assets/tether/chapter_01.mp3"
MANIFEST_OUT = "remotion-engine/public/assets/active_chapter_manifest.json"
EPISODE_MANIFEST = "remotion-engine/public/assets/episodes/tether_ch01/tether_ch01_manifest.json"

FPS = 30
TOTAL_DURATION_SEC = 82.296
TOTAL_FRAMES = int(math.ceil(TOTAL_DURATION_SEC * FPS)) # 2469 frames

def extract_word_timestamps():
    print("[1/3] Extracting word timestamps with faster-whisper...")
    try:
        from faster_whisper import WhisperModel
        model_dir = "assets/voice_model/whisper_cache/models--Systran--faster-whisper-base.en/snapshots"
        snapshots = list(Path(model_dir).glob("*"))
        if snapshots:
            model_path = str(snapshots[0])
        else:
            model_path = "base.en"
        
        print(f"Loading Whisper from: {model_path}")
        model = WhisperModel(model_path, device="cpu", compute_type="int8")
        segments, info = model.transcribe(AUDIO_PATH, word_timestamps=True)
        
        words_list = []
        for segment in segments:
            for w in segment.words:
                cleaned_word = w.word.strip().upper()
                if cleaned_word:
                    words_list.append({
                        "word": cleaned_word,
                        "startSec": round(w.start, 3),
                        "endSec": round(w.end, 3),
                        "startFrame": int(round(w.start * FPS)),
                        "endFrame": int(round(w.end * FPS))
                    })
        print(f"Extracted {len(words_list)} word timestamps.")
        return words_list
    except Exception as e:
        print(f"Warning: Whisper extraction failed: {e}. Generating fallback sync intervals.")
        # Fallback word sync if whisper has issues
        sample_words = "RIGHT NOW IN THE DEEPEST PLUMBING OF GLOBAL FINANCE THERE IS A PRIVATE COMPANY WITH FEWER THAN ONE HUNDRED EMPLOYEES THAT HOLDS MORE UNITED STATES TREASURY BILLS THAN GERMANY AUSTRALIA OR THE UNITED ARAB EMIRATES".split()
        interval = TOTAL_DURATION_SEC / len(sample_words)
        return [
            {
                "word": w,
                "startSec": round(i * interval, 2),
                "endSec": round((i + 1) * interval, 2),
                "startFrame": int(i * interval * FPS),
                "endFrame": int((i + 1) * interval * FPS)
            }
            for i, w in enumerate(sample_words)
        ]

def build_manifest(words):
    print("[2/3] Constructing 12-beat parameterized ChapterManifest...")
    
    # 12 beats spanning 2469 frames (~205.75 frames per beat)
    # Timing calibrated to the narration milestones:
    # 00:00 - 00:08 (0 - 240 frames): Intro Treasury Bills / Shadow Empire
    # 00:08 - 00:15 (240 - 450 frames): Germany & Australia comparison
    # 00:15 - 00:22 (450 - 660 frames): $110B USDT supply
    # 00:22 - 00:29 (660 - 870 frames): More volume than Visa & NYSE
    # 00:29 - 00:36 (870 - 1080 frames): Fortune Magazine / Giancarlo Devasini
    # 00:36 - 00:43 (1080 - 1290 frames): Caribbean offshore haven
    # 00:43 - 00:51 (1290 - 1530 frames): Cantor Fitzgerald $110B custody wire
    # 00:51 - 00:58 (1530 - 1740 frames): The terrifying question / de-peg crash
    # 00:58 - 01:06 (1740 - 1980 frames): Siphon HUD / Redemption conduit
    # 01:06 - 01:12 (1980 - 2160 frames): Global trade freeze & margin calls
    # 01:12 - 01:18 (2160 - 2340 frames): Forensic Docket DOJ subpoena
    # 01:18 - 01:22.3 (2340 - 2469 frames): Forensic money trail outro
    
    beat_timings = [
        (0, 240),
        (240, 210),
        (450, 210),
        (660, 210),
        (870, 210),
        (1080, 210),
        (1290, 240),
        (1530, 210),
        (1740, 240),
        (1980, 180),
        (2160, 180),
        (2340, TOTAL_FRAMES - 2340)
    ]
    
    beats = [
        # Beat 1: The Shadow Empire (Parallax Sandwich)
        {
            "id": "beat_01_treasury_empire",
            "archetype": "PARALLAX_SANDWICH",
            "startFrame": beat_timings[0][0],
            "durationFrames": beat_timings[0][1],
            "durationSec": beat_timings[0][1] / FPS,
            "mood": "SOLAR_EMPIRE",
            "parallax": {
                "bgAsset": "assets/episodes/tether_ch01/bg_01_manhattan_treasury.jpg",
                "fgCutoutAsset": "assets/episodes/tether_ch01/fg_01_treasury_eagle.png",
                "titleLine1": "THE SHADOW",
                "titleLine2": "EMPIRE",
                "scaleSpeed": 1.12,
                "dollyAmount": -25
            }
        },
        # Beat 2: More Treasuries Than Nations (Kinetic Statement)
        {
            "id": "beat_02_treasury_accumulation",
            "archetype": "KINETIC_STATEMENT",
            "startFrame": beat_timings[1][0],
            "durationFrames": beat_timings[1][1],
            "durationSec": beat_timings[1][1] / FPS,
            "mood": "HYPER_GROWTH",
            "statement": {
                "bgAsset": "assets/episodes/tether_ch01/bg_02_cantor_trading_desk.jpg",
                "heroTitle": "MORE TREASURY BILLS THAN",
                "accentWord": "GERMANY & AUSTRALIA",
                "subText": "FEWER THAN 100 EMPLOYEES CONTROLLING $110B"
            }
        },
        # Beat 3: $110B Global Liquidity (Kinetic Statement)
        {
            "id": "beat_03_usdt_supply",
            "archetype": "KINETIC_STATEMENT",
            "startFrame": beat_timings[2][0],
            "durationFrames": beat_timings[2][1],
            "durationSec": beat_timings[2][1] / FPS,
            "mood": "HYPER_GROWTH",
            "statement": {
                "bgAsset": "assets/episodes/tether_ch01/bg_03_usdt_global_liquidity.jpg",
                "heroTitle": "$110,000,000,000",
                "accentWord": "CIRCULATING SUPPLY",
                "subText": "SETTLING $60B+ IN DAILY BLOCKCHAIN TRANSFERS"
            }
        },
        # Beat 4: More Volume Than Visa & NYSE (Kinetic Statement)
        {
            "id": "beat_04_nyse_volume",
            "archetype": "KINETIC_STATEMENT",
            "startFrame": beat_timings[3][0],
            "durationFrames": beat_timings[3][1],
            "durationSec": beat_timings[3][1] / FPS,
            "mood": "HIGH_STAKES_ARENA",
            "statement": {
                "bgAsset": "assets/episodes/tether_ch01/bg_04_nyse_floor_comparison.jpg",
                "heroTitle": "MORE DAILY VOLUME THAN",
                "accentWord": "VISA & THE NYSE",
                "subText": "THE LARGEST SYNTHETIC DOLLAR PIPELINE ON EARTH"
            }
        },
        # Beat 5: Fortune Magazine Investigation (Magazine Slam)
        {
            "id": "beat_05_fortune_investigation",
            "archetype": "MAGAZINE_SLAM",
            "startFrame": beat_timings[4][0],
            "durationFrames": beat_timings[4][1],
            "durationSec": beat_timings[4][1] / FPS,
            "mood": "HIGH_STAKES_ARENA",
            "magazine": {
                "bgAsset": "assets/episodes/tether_ch01/bg_05_fortune_cover_backdrop.jpg",
                "publicationName": "FORTUNE",
                "issueTag": "SPECIAL FORENSIC REPORT // VOL. 110",
                "subjectCutout": "assets/episodes/tether_ch01/fg_05_devasini_portrait.png",
                "headline": "THE PRINTING PRESS OF CRYPTO",
                "subheadline": "Inside Giancarlo Devasini's Private Empire Out-Earning BlackRock and Goldman Sachs."
            }
        },
        # Beat 6: Caribbean Offshore Inception (Parallax Sandwich)
        {
            "id": "beat_06_bvi_offshore",
            "archetype": "PARALLAX_SANDWICH",
            "startFrame": beat_timings[5][0],
            "durationFrames": beat_timings[5][1],
            "durationSec": beat_timings[5][1] / FPS,
            "mood": "SOLAR_EMPIRE",
            "parallax": {
                "bgAsset": "assets/episodes/tether_ch01/bg_06_bvi_offshore_harbor.jpg",
                "titleLine1": "CARIBBEAN",
                "titleLine2": "OFFSHORE HAVEN",
                "scaleSpeed": 1.15,
                "dollyAmount": -30
            }
        },
        # Beat 7: Cantor Fitzgerald Custody Wire (Institutional Wire)
        {
            "id": "beat_07_cantor_custody_wire",
            "archetype": "INSTITUTIONAL_WIRE",
            "startFrame": beat_timings[6][0],
            "durationFrames": beat_timings[6][1],
            "durationSec": beat_timings[6][1] / FPS,
            "mood": "SOLAR_EMPIRE",
            "wire": {
                "bgAsset": "assets/episodes/tether_ch01/bg_07_cantor_vault_bullion.jpg",
                "senderName": "CANTOR FITZGERALD // PRIMARY DEALER",
                "recipientName": "TETHER HOLDINGS LTD.",
                "wireAmount": "$110,000,000,000.00",
                "valuationNote": "US TREASURY 90-DAY BILLS DIRECT CUSTODY",
                "statusBadge": "CONFIRMED // FEDWIRE MT103"
            }
        },
        # Beat 8: Market De-Peg Crash Threat (Kinetic Statement)
        {
            "id": "beat_08_depeg_question",
            "archetype": "KINETIC_STATEMENT",
            "startFrame": beat_timings[7][0],
            "durationFrames": beat_timings[7][1],
            "durationSec": beat_timings[7][1] / FPS,
            "mood": "FORENSIC_NOIR",
            "statement": {
                "bgAsset": "assets/episodes/tether_ch01/bg_08_depeg_market_crash.jpg",
                "heroTitle": "WHAT HAPPENS IF THE",
                "accentWord": "MONEY ISN'T THERE?",
                "subText": "DE-PEGGING FROM $1.00 TO ZERO CRASHES THE ECOSYSTEM"
            }
        },
        # Beat 9: Siphon HUD / Redemption Engine (Siphon Flowchart HUD)
        {
            "id": "beat_09_cyber_siphon",
            "archetype": "SIPHON_HUD",
            "startFrame": beat_timings[8][0],
            "durationFrames": beat_timings[8][1],
            "durationSec": beat_timings[8][1] / FPS,
            "mood": "FORENSIC_NOIR",
            "siphon": {
                "bgAsset": "assets/episodes/tether_ch01/bg_09_cyber_vault_siphon_base.jpg",
                "sourceLabel": "PRIMARY USDT RESERVES",
                "sourceAmount": "$110,000,000,000",
                "conduitCode": "INSTITUTIONAL REDEMPTION // CANTOR_ESCROW",
                "drainLabel": "SHADOW LIQUIDITY DRAIN",
                "drainTargetAmount": "-$10,000,000,000"
            }
        },
        # Beat 10: Global Trade Freeze (Kinetic Statement)
        {
            "id": "beat_10_trade_freeze",
            "archetype": "KINETIC_STATEMENT",
            "startFrame": beat_timings[9][0],
            "durationFrames": beat_timings[9][1],
            "durationSec": beat_timings[9][1] / FPS,
            "mood": "FORENSIC_NOIR",
            "statement": {
                "bgAsset": "assets/episodes/tether_ch01/bg_10_global_trade_freeze.jpg",
                "heroTitle": "GLOBAL LIQUIDITY FREEZE",
                "accentWord": "MARGIN CALLS ON WALL ST",
                "subText": "LATIN AMERICA, AFRICA & ASIA SUPPLY CHAINS HALTED"
            }
        },
        # Beat 11: Forensic Docket DOJ Subpoena (Legal Docket Subpoena)
        {
            "id": "beat_11_forensic_docket",
            "archetype": "FORENSIC_DOCKET",
            "startFrame": beat_timings[10][0],
            "durationFrames": beat_timings[10][1],
            "durationSec": beat_timings[10][1] / FPS,
            "mood": "FORENSIC_NOIR",
            "docket": {
                "bgAsset": "assets/episodes/tether_ch01/bg_11_manila_docket_desk_base.jpg",
                "folderHeader": "IN RE: GLOBAL COMMINGLING OF RESERVES",
                "courtName": "UNITED STATES DEPARTMENT OF JUSTICE",
                "exhibitId": "EXHIBIT T-110",
                "codeOrClauseText": "if (reserve_audit_requested == True) { commingle_with_parent_exchange(); }",
                "highlightSubstring": "commingle_with_parent_exchange",
                "stampLabel": "CRITICAL EVIDENCE // ADMITTED"
            }
        },
        # Beat 12: Forensic Money Trail Outro (Parallax Sandwich)
        {
            "id": "beat_12_money_trail",
            "archetype": "PARALLAX_SANDWICH",
            "startFrame": beat_timings[11][0],
            "durationFrames": beat_timings[11][1],
            "durationSec": beat_timings[11][1] / FPS,
            "mood": "FORENSIC_NOIR",
            "parallax": {
                "bgAsset": "assets/episodes/tether_ch01/bg_12_wall_street_shadow_corridor.jpg",
                "titleLine1": "THE FORENSIC",
                "titleLine2": "MONEY TRAIL",
                "scaleSpeed": 1.10,
                "dollyAmount": -20
            }
        }
    ]
    
    manifest = {
        "episodeId": "tether_untold",
        "chapterId": "ch01_the_shadow_empire",
        "chapterIndex": 1,
        "title": "The $110 Billion Shadow Engine",
        "durationSec": TOTAL_DURATION_SEC,
        "durationFrames": TOTAL_FRAMES,
        "fps": FPS,
        "audioAsset": "assets/tether/chapter_01.mp3",
        "ambientAsset": "assets/cinematic/sub_bass_pulse.mp3",
        "wordTimestamps": words,
        "beats": beats
    }
    
    return manifest

def main():
    words = extract_word_timestamps()
    manifest = build_manifest(words)
    
    os.makedirs(os.path.dirname(MANIFEST_OUT), exist_ok=True)
    os.makedirs(os.path.dirname(EPISODE_MANIFEST), exist_ok=True)
    
    with open(MANIFEST_OUT, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f" -> Saved active manifest: {MANIFEST_OUT}")
    
    with open(EPISODE_MANIFEST, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f" -> Saved episode manifest: {EPISODE_MANIFEST}")
    
    print("\n[3/3] Manifest Verification:")
    print(f"Total Beats: {len(manifest['beats'])}")
    print(f"Total Frames: {manifest['durationFrames']} ({manifest['durationSec']}s)")
    print(f"Total Words Synchronized: {len(words)}")
    print("Beats breakdown:")
    for b in manifest["beats"]:
        print(f" - {b['id']} | Archetype: {b['archetype']} | Frames: {b['startFrame']}-{b['startFrame']+b['durationFrames']} | Mood: {b['mood']}")

if __name__ == "__main__":
    main()
