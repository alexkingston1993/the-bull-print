#!/usr/bin/env python3
"""
Master Documentary Full Production Renderer
Renders every single segment using the full visual engine:
- Dynamic 3D Extruded Perspective Typography (0.22 forward italic shear, 16px extrusion shadow, neon bloom)
- High-Contrast Stabilo Tactical Highlighter Badges (Mass audience language)
- Lower-Third Word-Level Animated Captions with glowing active word highlight
- Slow camera dolly drift (1.00 -> 1.05)
- Atmospheric cinematic vignette
- ChristopherNeural VO + 10% BGM bed (-18 LUFS)
- Merges into 12-minute master MP4
- Uploads to YouTube as PRIVATE
- Sends ARIA Telegram notification
"""

import sys
import json
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BGM_DIR = BASE_DIR / "assets" / "audio" / "bgm_pool"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.youtube_uploader import YouTubeUploader
from scripts.master_documentary_visual_engine import render_segment_with_visual_engine

DOC_SPECS = {
    "ai_bubble": {
        "title": "The $2.5 Trillion AI Wall: Why the AI Bubble Is Cracking",
        "description": "Nvidia, Microsoft, and OpenAI face a massive $2.5 Trillion infrastructure bottleneck. Inside Wall Street's AI panic and the reality behind datacenter scaling.\n\n#TheBullPrint #AIBubble #Nvidia #ArtificialIntelligence #TechStocks #WallStreet #Documentary",
        "tags": ["TheBullPrint", "AIBubble", "Nvidia", "ArtificialIntelligence", "TechStocks", "WallStreet", "Documentary"],
        "dir": BASE_DIR / "output" / "ai_bubble_documentary",
        "timing": BASE_DIR / "output" / "ai_bubble_documentary" / "timing_and_timestamps.json",
        "thumbnail": BASE_DIR / "output" / "thumbnails" / "thumb_ai_bubble_viral_ctr.jpg",
        "final_name": "the_ai_bubble_panic_12min_master.mp4"
    },
    "fii_exodus": {
        "title": "The ₹14,900 Crore U-Turn: How Foreign Investors Broke and Rescued the Indian Market",
        "description": "Foreign big institutional investors pulled ₹1.8 Lakh Crore from Indian stocks before making a massive comeback. Inside the global currency shifts and big money flows.\n\n#TheBullPrint #ForeignInvestors #IndianMarket #Nifty #StockMarketIndia #Documentary",
        "tags": ["TheBullPrint", "ForeignInvestors", "IndianMarket", "Nifty", "StockMarketIndia", "Documentary"],
        "dir": BASE_DIR / "output" / "fii_exodus_documentary",
        "timing": BASE_DIR / "output" / "fii_exodus_documentary" / "timing_and_timestamps.json",
        "thumbnail": BASE_DIR / "output" / "thumbnails" / "thumb_fii_exodus_viral_ctr.jpg",
        "final_name": "the_fii_exodus_12min_master.mp4"
    },
    "nuclear_ai": {
        "title": "Big Tech's Nuclear Secret: The Race for Atomic Megawatts",
        "description": "Microsoft, Amazon, and Google are purchasing nuclear reactors to feed power-hungry AI clusters. Inside the energy crisis threatening artificial intelligence.\n\n#TheBullPrint #NuclearEnergy #BigTech #AI #Microsoft #Amazon #EnergyCrisis #Documentary",
        "tags": ["TheBullPrint", "NuclearEnergy", "BigTech", "AI", "Microsoft", "Amazon", "EnergyCrisis", "Documentary"],
        "dir": BASE_DIR / "output" / "nuclear_ai_documentary",
        "timing": BASE_DIR / "output" / "nuclear_ai_documentary" / "timing_and_timestamps.json",
        "thumbnail": BASE_DIR / "output" / "thumbnails" / "thumb_nuclear_ai_viral_ctr.jpg",
        "final_name": "the_nuclear_ai_race_12min_master.mp4"
    }
}

CHAPTER_BGM = {
    range(1, 8): BGM_DIR / "bed_01_subterranean_pulse.wav",
    range(8, 15): BGM_DIR / "bed_02_quant_clockwork.wav",
    range(15, 22): BGM_DIR / "bed_06_systemic_collapse.wav",
    range(22, 29): BGM_DIR / "bed_03_offshore_noir.wav",
    range(29, 37): BGM_DIR / "bed_04_cyber_forensic.wav",
}

def get_bgm(seg_num: int) -> Path:
    for r, p in CHAPTER_BGM.items():
        if seg_num in r and p.exists():
            return p
    return BGM_DIR / "bed_01_subterranean_pulse.wav"

def send_telegram_alert(video_title: str, video_url: str, doc_key: str):
    tg_token = "8829963924:AAE7v_xEQXLmy3-YEx8kqMo2GRfnbnxf4GA"
    chat_id = "1126599043"
    msg = (
        f"🏆 <b>THE BULL PRINT - MASTER DOCUMENTARY (FULL 3D VISUAL ENGINE)</b>\n\n"
        f"🎬 <b>Title:</b> {video_title}\n"
        f"⚡ <b>Features:</b> Dynamic 3D Extruded Slanted Typography + Tactical Badges + Word-Level Animated Captions\n"
        f"⏱ <b>Standard:</b> 180 Plates @ 4.0s (16:9 Widescreen 1080p)\n"
        f"🔒 <b>Privacy:</b> PRIVATE\n"
        f"🔗 <b>YouTube Link:</b> {video_url}\n\n"
        f"✨ Produced with the full signature aesthetic."
    )
    import urllib.request, urllib.parse
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{tg_token}/sendMessage", data=data)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            pass
        print(f"📲 Telegram alert sent via ARIA for {doc_key}.")
    except Exception as e:
        print(f"⚠️ Telegram send error: {e}")

def render_full_documentary(doc_key: str):
    config = DOC_SPECS.get(doc_key)
    if not config:
        raise ValueError(f"Unknown documentary key: {doc_key}")

    doc_dir = config["dir"]
    timing_file = config["timing"]
    final_out = doc_dir / config["final_name"]

    print("\n" + "=" * 65)
    print(f"🎬 RENDERING FULL 3D MASTER DOCUMENTARY: {config['title']}")
    print("=" * 65)

    with open(timing_file, "r") as f:
        timing_data = json.load(f)

    # Load full chapters script for voiceover text and mass audience language
    script_file = doc_dir / "chapters_script.py"
    vo_map = {}
    if script_file.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("chapters_mod", script_file)
        c_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(c_mod)
        for s in getattr(c_mod, "SEGMENTS", []):
            vo_map[s["id"]] = s.get("voiceover", "")

    work_dir = doc_dir / "rendered_segments_3d"
    work_dir.mkdir(parents=True, exist_ok=True)
    frames_dir = doc_dir / "frames"

    segments = timing_data["segments"]
    rendered_segments = []

    for seg_key in sorted(segments.keys(), key=lambda x: int(x)):
        seg_num = int(seg_key)
        seg_val = segments[seg_key]
        seg_out = work_dir / f"segment_{seg_num:02d}_3d.mp4"

        # Populate and sanitize voiceover for animated captions
        vo_raw = vo_map.get(seg_num, "")
        vo_clean = (
            vo_raw.replace("Dalal Street's", "The Indian market's")
            .replace("Dalal Street", "the Indian market")
            .replace("Smart Money", "big institutional buyers")
            .replace("smart money", "big institutional buyers")
        )
        seg_val["voiceover"] = vo_clean

        # Sanitize beats typography
        for b in seg_val.get("beats", []):
            if "anchor_text" in b:
                b["anchor_text"] = (
                    b["anchor_text"]
                    .replace("DALAL ST", "INDIAN MKT")
                    .replace("DALAL STREET", "INDIAN MKT")
                    .replace("SMART MONEY", "BIG FUNDS")
                )
            if "badge_text" in b:
                b["badge_text"] = (
                    b["badge_text"]
                    .replace("DALAL ST", "INDIAN MKT")
                    .replace("DALAL STREET", "INDIAN MKT")
                    .replace("SMART MONEY", "BIG FUNDS")
                )

        # Find voiceover file
        vo_candidates = [
            doc_dir / "audio" / f"vo_segment_{seg_num:02d}.mp3",
            doc_dir / "audio" / f"segment_{seg_num:02d}.mp3"
        ]
        audio_path = next((p for p in vo_candidates if p.exists()), None)
        if not audio_path:
            raise FileNotFoundError(f"Missing voiceover audio for segment {seg_num}")

        bgm_path = get_bgm(seg_num)

        if not seg_out.exists() or seg_out.stat().st_size < 100000:
            print(f"[{seg_num:02d}/36] ⏳ Rendering Segment {seg_num:02d} with 3D typography, badge, & captions...")
            render_segment_with_visual_engine(
                seg_data=seg_val,
                audio_path=audio_path,
                bgm_path=bgm_path,
                frames_dir=frames_dir,
                output_mp4=seg_out,
                seg_idx=seg_num
            )
        else:
            print(f"[{seg_num:02d}/36] ⏩ Segment {seg_num:02d} already rendered with 3D engine, skipping.")

        rendered_segments.append(seg_out)

    # Concat all 36 segments
    concat_list = work_dir / "concat_list_3d.txt"
    with open(concat_list, "w") as f:
        for p in rendered_segments:
            f.write(f"file '{p.resolve()}'\n")

    print(f"\nMerging all 36 segments into master documentary: {final_out}...")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(final_out)
    ]
    subprocess.run(cmd_concat, check=True)
    print(f"🎉 MASTER 12-MINUTE DOCUMENTARY COMPLETE: {final_out}")

    # Upload to YouTube ONLY if explicit approval flag passed
    if "--upload" in sys.argv:
        print(f"\n=======================================================")
        print(f"🚀 UPLOADING FULL MASTER DOCUMENTARY TO YOUTUBE (PRIVATE)")
        print(f"=======================================================")
        uploader = YouTubeUploader()
        thumb_path = config.get("thumbnail")
        thumb_str = str(thumb_path) if thumb_path and thumb_path.exists() else None

        res = uploader.upload_video(
            language="en",
            video_path=str(final_out),
            title=config["title"],
            description=config["description"],
            tags=config["tags"],
            privacy_status="private",
            thumbnail_path=thumb_str
        )

        if res.get("status") == "success" or res.get("success"):
            vid_id = res.get("video_id")
            vid_url = res.get("url") or f"https://youtu.be/{vid_id}"
            print(f"🎉 MASTER DOCUMENTARY UPLOADED (PRIVATE): {vid_url}")
            send_telegram_alert(config["title"], vid_url, doc_key)
            return True
        else:
            print(f"⚠️ Upload error: {res}")
            return False
    else:
        print(f"\n🛑 LOCAL RENDER ONLY: Skipping YouTube upload per approval directive.")
        print(f"✅ Master file saved on local disk: {final_out}")
        return True

if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "fii_exodus"
    render_full_documentary(key)

