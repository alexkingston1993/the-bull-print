"""
Master Video Engine for 12-Minute Standard YouTube Feature:
'THE $32 BILLION ILLUSION: The Criminal Rise and Fall of FTX & Alameda Research'
Duration: 36 Segments x 20.0s = 720.0 Seconds (12 Minutes)
Composites user's 36 2K master frames, Christopher voiceovers, and orchestral BGM beds.
"""

import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from scripts.generate_36_segment_dossier import SEGMENTS

FRAMES_DIR = BASE_DIR / "output" / "2026-11-05"
VO_DIR = BASE_DIR / "output" / "ftx_documentary" / "vo_36_segments"
BGM_DIR = BASE_DIR / "assets" / "audio" / "bgm_pool"
WORK_DIR = BASE_DIR / "output" / "ftx_documentary" / "rendered_segments"
WORK_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR = BASE_DIR / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FINAL_OUTPUT = OUT_DIR / "the_32_billion_illusion_12min_master.mp4"
PREVIEW_OUTPUT = OUT_DIR / "the_32_billion_illusion_preview_60s.mp4"

SEG_FILE_MAP = [
    (1, 'Penthouse_desk_with_glowing_term'),
    (2, 'Printing_presses_producing_busin'),
    (3, 'Laptop_displaying_video_game_gra'),
    (4, 'Congressional_hearing_room_with_'),
    (5, 'Beanbag_and_key_on_floor'),
    (6, 'Glowing_server_racks_in_darkness'),
    (7, 'Quantitative_trading_floor_monitors'),
    (8, 'Financial_districts_connected_by'),
    (9, 'Trading_terminal_displaying_cryp'),
    (10, 'Digital_token_spinning_on_glass'),
    (11, 'Gold_coin_balancing_on_cards'),
    (12, 'Cursor_blinking_on_computer_screen'),
    (13, 'Bank_vault_door_open'),
    (14, 'Futuristic_sports_arena_exterior'),
    (15, 'Television_studio_with_monitor_d'),
    (16, 'Corporate_boardroom_overlooking_'),
    (17, 'Venture_capital_manifesto_text_o'),
    (18, 'US_Capitol_campaign_cash_display'),
    (19, 'Legal_bill_marked_with_pen'),
    (20, 'Tech_founder_overlooking_ocean'),
    (21, 'Red_digital_domino_toppling_circuit'),
    (22, 'Green_liquid_draining_into_tank'),
    (23, 'Highlighting_confidential_financ'),
    (24, 'Smartphone_screen_displaying_liq'),
    (25, 'Traders_panicking_during_bank_run'),
    (26, 'Encrypted_messaging_app_capital_'),
    (27, 'Binance_walks_away_contract'),
    (28, 'Delaware_Federal_Bankruptcy_Cour'),
    (29, 'Veteran_bankruptcy_auditor_exami'),
    (30, 'Forensic_examination_of_corporat'),
    (31, 'Officers_escorting_suspect_into_'),
    (32, 'Courthouse_exterior_with_reporters'),
    (33, 'Witness_stand_in_courtroom'),
    (34, 'Judge_gavel_resting_on_bench'),
    (35, 'Security_key_in_glass_case'),
    (36, 'Bull_Print_office_financial_inte'),
]

CHAPTER_BGM = {
    range(1, 7): BGM_DIR / "bed_03_offshore_noir.wav",
    range(7, 14): BGM_DIR / "bed_02_quant_clockwork.wav",
    range(14, 21): BGM_DIR / "bed_05_wall_street_afterhours.wav",
    range(21, 29): BGM_DIR / "bed_06_systemic_collapse.wav",
    range(29, 37): BGM_DIR / "bed_04_cyber_forensic.wav",
}

def get_bgm_for_seg(seg_num: int) -> Path:
    for r, p in CHAPTER_BGM.items():
        if seg_num in r:
            return p
    return BGM_DIR / "bed_01_subterranean_pulse.wav"

def get_frame_for_seg(seg_num: int) -> Path:
    prefix = SEG_FILE_MAP[seg_num - 1][1]
    for f in FRAMES_DIR.glob("*.*"):
        if f.name.startswith(prefix):
            return f
    raise FileNotFoundError(f"Frame matching prefix {prefix} not found!")

def render_segment(seg_num: int, target_dur: float = 20.0) -> Path:
    out_mp4 = WORK_DIR / f"segment_{seg_num:02d}.mp4"
    if out_mp4.exists() and out_mp4.stat().st_size > 100000:
        return out_mp4

    img_path = get_frame_for_seg(seg_num)
    vo_path = VO_DIR / f"seg_{seg_num:02d}.mp3"
    bgm_path = get_bgm_for_seg(seg_num)

    # Subtle Ken Burns drift: scale 1.00 to 1.04 over 20s
    total_frames = int(target_dur * 30)
    
    # Complex filter:
    # 1. Video: scale, slow zoom drift, pad to 1920x1080
    # 2. Audio: Voice starts at 0.4s. BGM loops or plays ducked at -18dB. Combined with amix.
    vf = (
        f"scale=2752:1536,"
        f"zoompan=z='min(zoom+0.00006,1.04)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30,"
        f"format=yuv420p"
    )

    # BGM offset calculation: each segment takes 20s of its chapter BGM
    bgm_offset = ((seg_num - 1) % 7) * 20.0

    af = (
        f"[1:a]adelay=400|400,apad=pad_dur={target_dur}[vo];"
        f"[2:a]atrim=start={bgm_offset}:end={bgm_offset + target_dur},asetpts=PTS-STARTPTS,volume=0.12[bgm];"
        f"[vo][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(img_path),
        "-i", str(vo_path),
        "-stream_loop", "-1", "-i", str(bgm_path),
        "-filter_complex", f"[0:v]{vf}[vout];{af}",
        "-map", "[vout]", "-map", "[aout]",
        "-t", str(target_dur),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        str(out_mp4)
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        print(f"❌ Failed to render Segment {seg_num}: {res.stderr.decode()[-400:]}")
        sys.exit(1)
        
    print(f"✓ Rendered Seg {seg_num:02d} ({target_dur}s): {out_mp4.name} ({round(out_mp4.stat().st_size/1024/1024, 2)} MB)")
    return out_mp4

def concatenate_segments(seg_paths: list, output_file: Path):
    concat_list = WORK_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        for p in seg_paths:
            f.write(f"file '{p.resolve()}'\n")

    print(f"\n🎬 Concatenating {len(seg_paths)} segments into {output_file.name}...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(output_file)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        print(f"❌ Concat failed: {res.stderr.decode()[-400:]}")
        sys.exit(1)
    
    size_mb = round(output_file.stat().st_size / 1024 / 1024, 2)
    print(f"🏆 SUCCESS! Final Master Video Created: {output_file} ({size_mb} MB)")

def main():
    print("=" * 60)
    print("🎬 THE BULL PRINT — 12-MINUTE MASTER DOCUMENTARY ENGINE")
    print("   Total Segments: 36 | Duration: 720.0s (12:00)")
    print("=" * 60)

    # 1. Render all 36 segments
    seg_mp4s = []
    for s in range(1, 37):
        mp4 = render_segment(s, target_dur=20.0)
        seg_mp4s.append(mp4)

    # 2. Render 60s Preview (Segments 1, 2, 3)
    print("\n📦 Building 60-Second 3-Segment Preview...")
    concatenate_segments(seg_mp4s[:3], PREVIEW_OUTPUT)

    # 3. Concatenate all 36 segments into 12-minute master MP4
    concatenate_segments(seg_mp4s, FINAL_OUTPUT)

if __name__ == "__main__":
    main()
