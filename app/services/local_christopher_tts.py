#!/usr/bin/env python3
"""
app/services/local_christopher_tts.py

100% OFFLINE LOCAL CLONED TTS + FASTER-WHISPER ALIGNMENT ENGINE
- Zero server dependency, zero edge-tts runtime calls.
- Speaker reference: assets/voice_model/christopher_ref/christopher_master_24k.wav
- Broadcast mastering: Highpass 70Hz + 135Hz chest resonance EQ + gentle optical compression + -16 LUFS loudnorm.
- Frame-accurate word timestamps: faster-whisper base.en running 100% locally.
"""

import os
import re
import sys
import json
import shutil
import tempfile
import subprocess
from pathlib import Path
import numpy as np
import soundfile as sf

# Fix macOS duplicate OpenMP runtime initialization
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

BASE_DIR = Path(__file__).resolve().parent.parent.parent
REF_DIR = BASE_DIR / "assets/voice_model/christopher_ref"
DEFAULT_REF_WAV = REF_DIR / "christopher_master_24k.wav"
DEFAULT_REF_TEXT_FILE = REF_DIR / "ref_text.txt"
WHISPER_CACHE_DIR = BASE_DIR / "assets/voice_model/whisper_cache"

_TTS_INSTANCE = None
_WHISPER_INSTANCE = None

def get_tts_engine():
    """Initializes and returns cached offline XTTS-v2 zero-shot cloner."""
    global _TTS_INSTANCE
    if _TTS_INSTANCE is None:
        from TTS.api import TTS
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🎙️ Loading 100% local XTTS-v2 model on {device}...")
        _TTS_INSTANCE = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=(device == "cuda"))
    return _TTS_INSTANCE

def get_whisper_engine():
    """Initializes and returns cached offline faster-whisper model."""
    global _WHISPER_INSTANCE
    if _WHISPER_INSTANCE is None:
        from faster_whisper import WhisperModel
        print(f"⏱️ Loading 100% offline Faster-Whisper (base.en) from local cache...")
        _WHISPER_INSTANCE = WhisperModel(
            "base.en",
            device="cpu",
            compute_type="int8",
            download_root=str(WHISPER_CACHE_DIR),
            local_files_only=True
        )
    return _WHISPER_INSTANCE

def split_into_clauses(text: str) -> list[tuple[str, float]]:
    """
    Splits text into natural clauses with associated pause duration in seconds.
    Returns list of (clause_text, pause_after_sec).
    """
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    items = []
    
    for p_idx, p in enumerate(paragraphs):
        # Split sentences by period, exclamation, question mark, or semicolon
        sentences = re.split(r'(?<=[.!?])\s+', p)
        for s_idx, s in enumerate(sentences):
            s = s.strip()
            if not s:
                continue
            
            # If it's the last sentence in a paragraph, give 500ms pause, else 350ms
            is_last_in_para = (s_idx == len(sentences) - 1)
            pause = 0.50 if is_last_in_para else 0.35
            items.append((s, pause))
            
    return items

def synthesize_chapter_offline(
    script_text: str,
    out_mp3_path: str,
    out_timestamps_json: str,
    reference_wav: str = None
) -> dict:
    """
    Synthesizes script_text completely offline, masters audio, and writes word timestamps.
    """
    out_mp3 = Path(out_mp3_path).resolve()
    out_timestamps = Path(out_timestamps_json).resolve()
    out_mp3.parent.mkdir(parents=True, exist_ok=True)
    out_timestamps.parent.mkdir(parents=True, exist_ok=True)
    
    ref_wav_path = Path(reference_wav) if reference_wav else DEFAULT_REF_WAV
    if not ref_wav_path.exists():
        raise FileNotFoundError(f"Missing master golden reference audio at: {ref_wav_path}")
        
    clauses = split_into_clauses(script_text)
    print(f"🎙️ Synthesizing {len(clauses)} clauses with local Christopher voice clone...")
    
    tts = get_tts_engine()
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        clause_wavs = []
        sr = 24000
        
        for idx, (clause, pause_sec) in enumerate(clauses):
            print(f"  [{idx+1}/{len(clauses)}] ({len(clause.split())} words) {clause[:45]}...")
            clause_out = tmp_path / f"clause_{idx:03d}.wav"
            
            # Run local offline zero-shot synthesis
            tts.tts_to_file(
                text=clause,
                speaker_wav=str(ref_wav_path),
                language="en",
                file_path=str(clause_out),
                split_sentences=False
            )
            
            # Read generated audio
            data, cur_sr = sf.read(str(clause_out))
            if cur_sr != sr:
                import soxr
                data = soxr.resample(data, cur_sr, sr)
                
            clause_wavs.append(data)
            
            # Append pause silence
            pause_samples = int(pause_sec * sr)
            if pause_samples > 0:
                clause_wavs.append(np.zeros(pause_samples, dtype=np.float32))
                
        # Concatenate full raw audio
        combined_audio = np.concatenate(clause_wavs, axis=0)
        raw_combined_wav = tmp_path / "raw_master.wav"
        sf.write(str(raw_combined_wav), combined_audio, sr)
        
        # Broadcast mastering chain via local ffmpeg
        print("🎛️ Applying broadcast documentary mastering chain (EQ, Compression, Loudnorm)...")
        master_cmd = [
            "ffmpeg", "-y",
            "-i", str(raw_combined_wav),
            "-af", (
                "highpass=f=70,"
                "equalizer=f=135:width_type=o:width=1.4:g=2.8,"
                "acompressor=threshold=-18dB:ratio=3:attack=5:release=85,"
                "loudnorm=I=-16:TP=-1.5:LRA=11"
            ),
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            str(out_mp3)
        ]
        subprocess.run(master_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    print(f"  ✓ Mastered audio written: {out_mp3}")
    
    # Run Faster-Whisper for millisecond word timestamps in an isolated process to prevent macOS OpenMP collision
    print("⏱️ Extracting word-level alignment timestamps via offline Faster-Whisper...")
    whisper_script = (
        "import os, sys, json\n"
        "os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'\n"
        "from faster_whisper import WhisperModel\n"
        "mp3_path = sys.argv[1]\n"
        "json_path = sys.argv[2]\n"
        "cache_dir = sys.argv[3]\n"
        "model = WhisperModel('base.en', device='cpu', compute_type='int8', download_root=cache_dir, local_files_only=True)\n"
        "segments, _ = model.transcribe(mp3_path, word_timestamps=True, language='en')\n"
        "words_data = []\n"
        "for seg in segments:\n"
        "    for w in seg.words:\n"
        "        clean = w.word.strip()\n"
        "        if clean:\n"
        "            words_data.append({\n"
        "                'word': clean,\n"
        "                'startSec': round(float(w.start), 3),\n"
        "                'endSec': round(float(w.end), 3),\n"
        "                'startFrame': int(round(float(w.start) * 30)),\n"
        "                'endFrame': int(round(float(w.end) * 30))\n"
        "            })\n"
        "with open(json_path, 'w', encoding='utf-8') as f:\n"
        "    json.dump(words_data, f, indent=2)\n"
        "print(f'ALIGNED_WORDS:{len(words_data)}')\n"
    )
    
    sub_res = subprocess.run(
        [sys.executable, "-c", whisper_script, str(out_mp3), str(out_timestamps), str(WHISPER_CACHE_DIR)],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    
    with open(out_timestamps, "r", encoding="utf-8") as f:
        words_data = json.load(f)
        
    print(f"  ✓ Word timestamps saved ({len(words_data)} words): {out_timestamps}")
    
    # Measure duration and LUFS
    probe_dur = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(out_mp3)
    ], stdout=subprocess.PIPE, text=True, check=True)
    dur_sec = float(probe_dur.stdout.strip())
    
    return {
        "durationSec": dur_sec,
        "totalWords": len(words_data),
        "mp3Path": str(out_mp3),
        "timestampsPath": str(out_timestamps)
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: local_christopher_tts.py <script_text> <out_mp3> <out_json>")
        sys.exit(1)
    synthesize_chapter_offline(sys.argv[1], sys.argv[2], sys.argv[3])
