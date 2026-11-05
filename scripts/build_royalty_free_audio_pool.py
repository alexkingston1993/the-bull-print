"""
Comprehensive Royalty-Free & Zero-Attribution Audio Pool Generator
(scripts/build_royalty_free_audio_pool.py)

Generates a complete, multi-mood, zero-attribution music & SFX library
using pure Python DSP (numpy + scipy.io.wavfile) at 44.1 kHz, 16-bit PCM Stereo.

Mood Categories:
1. dark_investigative (MEV bots, shadow banking, crashes, exploits)
2. bullish_upbeat (Market rallies, breakouts, compounding wealth, growth)
3. witty_satire (Retail FOMO, meme coin mania, degen humor, irony)
4. neutral_educational (Balance sheets, SEBI rules, valuations, how-tos)
5. urgent_breaking (Flash crashes, emergency rate cuts, circuit breakers)

Supports:
- 60s seamless loops for Shorts
- 180s extended beds for Standard 3-minute videos
- 10 precision transition SFX across all emotional tones
"""

import os
import math
import numpy as np
from pathlib import Path
from scipy.io import wavfile

SAMPLE_RATE = 44100
BASE_DIR = Path(__file__).resolve().parent.parent
BGM_POOL = BASE_DIR / "assets" / "audio" / "bgm_pool"
SFX_POOL = BASE_DIR / "assets" / "audio" / "sfx_pool"


def save_wav(path: Path, audio: np.ndarray, peak_db: float = -1.5):
    peak = np.max(np.abs(audio))
    if peak > 0:
        target = 10.0 ** (peak_db / 20.0)
        audio = (audio / peak) * target
    int16_pcm = np.clip(audio * 32767.0, -32768, 32767).astype(np.int16)
    path.parent.mkdir(parents=True, exist_ok=True)
    wavfile.write(str(path), SAMPLE_RATE, int16_pcm)
    dur = len(audio) / SAMPLE_RATE
    print(f"✓ Saved: {path.relative_to(BASE_DIR)} ({dur:.1f}s, {path.stat().st_size / 1024:.1f} KB)")


# ─────────────────────────────────────────────────────────────
# 1. DARK & INVESTIGATIVE MOOD
# ─────────────────────────────────────────────────────────────

def gen_dark_subterranean(duration: float = 60.0) -> np.ndarray:
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    bpm = 65.0
    beat_dur = 60.0 / bpm
    phase = (t % beat_dur) / beat_dur
    pulse = np.exp(-4.0 * phase)
    sub = np.sin(2 * np.pi * 55.0 * t) * pulse * 0.75 + np.sin(2 * np.pi * 27.5 * t) * pulse * 0.4
    pad_l = (np.sin(2 * np.pi * 73.42 * t) + 0.5 * np.sin(2 * np.pi * 110.0 * t)) * 0.25
    pad_r = (np.sin(2 * np.pi * 73.80 * t) + 0.5 * np.sin(2 * np.pi * 110.2 * t)) * 0.25
    shimmer = np.sin(2 * np.pi * 0.1 * t) * np.random.normal(0, 0.02, len(t))
    return np.column_stack([sub + pad_l + shimmer, sub + pad_r - shimmer])


def gen_dark_quant_clockwork(duration: float = 60.0) -> np.ndarray:
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    bpm = 120.0
    beat_dur = 60.0 / bpm
    tick_phase = (t % (beat_dur / 2.0)) / (beat_dur / 2.0)
    tick = np.sin(2 * np.pi * 2800.0 * t) * np.exp(-35.0 * tick_phase) * 0.35
    drone_l = np.sin(2 * np.pi * 73.42 * t) * 0.35 + np.sin(2 * np.pi * 87.31 * t) * 0.25
    drone_r = np.sin(2 * np.pi * 73.50 * t) * 0.35 + np.sin(2 * np.pi * 110.0 * t) * 0.25
    return np.column_stack([drone_l + tick * 0.9, drone_r + tick * 0.3])


# ─────────────────────────────────────────────────────────────
# 2. BULLISH & UPBEAT MOOD (Breakouts, Compounding, Green Candles)
# ─────────────────────────────────────────────────────────────

def gen_bullish_emerald_breakout(duration: float = 60.0) -> np.ndarray:
    """124 BPM driving major-key synth pulse with bright arpeggiated melodic swells."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    bpm = 124.0
    beat_dur = 60.0 / bpm
    
    # Driving kick / pulse on quarters
    pulse_phase = (t % beat_dur) / beat_dur
    kick = np.sin(2 * np.pi * (110.0 * np.exp(-15.0 * pulse_phase) + 45.0) * t) * np.exp(-5.0 * pulse_phase) * 0.55
    
    # G major arpeggio (G3, B3, D4, G4: 196, 246.9, 293.66, 392 Hz)
    notes = [196.0, 246.94, 293.66, 392.0, 493.88, 392.0, 293.66, 246.94]
    step_dur = beat_dur / 2.0 # 8th notes
    step_idx = (t // step_dur).astype(int) % len(notes)
    step_phase = (t % step_dur) / step_dur
    arp_freq = np.array(notes)[step_idx]
    arp = (np.sin(2 * np.pi * arp_freq * t) + 0.3 * np.sin(2 * np.pi * arp_freq * 2 * t)) * np.exp(-8.0 * step_phase) * 0.35
    
    # Warm uplifting G-major pad (G2: 98Hz, D3: 146.8Hz, B3: 246.9Hz)
    pad = (np.sin(2 * np.pi * 98.0 * t) + 0.6 * np.sin(2 * np.pi * 146.83 * t) + 0.4 * np.sin(2 * np.pi * 246.94 * t)) * 0.25
    
    left = kick + arp * 0.9 + pad
    right = kick + arp * 0.6 + pad * 1.1
    return np.column_stack([left, right])


def gen_bullish_capital_compounder(duration: float = 60.0) -> np.ndarray:
    """Confident tech forward momentum with bright acoustic bell plucks."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    bpm = 110.0
    beat_dur = 60.0 / bpm
    
    # Pluck melody (E major: E3, G#3, B3, E4)
    plucks = [164.81, 207.65, 246.94, 329.63, 415.30, 329.63, 246.94, 207.65]
    step_dur = beat_dur / 2.0
    step_idx = (t // step_dur).astype(int) % len(plucks)
    step_phase = (t % step_dur) / step_dur
    f = np.array(plucks)[step_idx]
    bell = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2 * t) + 0.2 * np.sin(2 * np.pi * f * 3 * t)) * np.exp(-6.0 * step_phase) * 0.35
    
    # Deep rhythmic bassline
    bass_phase = (t % beat_dur) / beat_dur
    bass = np.sin(2 * np.pi * 82.41 * t) * np.exp(-3.0 * bass_phase) * 0.45
    
    return np.column_stack([bell * 0.85 + bass, bell * 1.0 + bass])


# ─────────────────────────────────────────────────────────────
# 3. WITTY & SATIRICAL MOOD (Retail FOMO, Meme Coins, Degens)
# ─────────────────────────────────────────────────────────────

def gen_witty_retail_fomo_bounce(duration: float = 60.0) -> np.ndarray:
    """Quirky pizzicato strings and playful swing rhythm for comedic/satirical segments."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    bpm = 128.0
    beat_dur = 60.0 / bpm
    
    # Offbeat pizzicato pluck (F#3, A3, C#4)
    step_dur = beat_dur / 2.0
    step_idx = (t // step_dur).astype(int) % 4
    step_phase = (t % step_dur) / step_dur
    
    # Playful bouncy notes
    notes = [185.0, 220.0, 277.18, 220.0]
    f = np.array(notes)[step_idx]
    pizz = np.sin(2 * np.pi * f * t) * np.exp(-18.0 * step_phase) * 0.45
    
    # Funky walking bassline on quarter beats
    bass_notes = [92.5, 110.0, 138.59, 110.0]
    b_idx = (t // beat_dur).astype(int) % 4
    b_freq = np.array(bass_notes)[b_idx]
    b_phase = (t % beat_dur) / beat_dur
    bass = np.sin(2 * np.pi * b_freq * t) * np.exp(-4.0 * b_phase) * 0.5
    
    # Playful woodblock percussion click on offbeats
    wood_click = np.where(step_idx % 2 == 1, np.sin(2 * np.pi * 1600.0 * t) * np.exp(-45.0 * step_phase) * 0.25, 0)
    
    left = pizz + bass + wood_click
    right = pizz * 0.7 + bass + wood_click * 1.2
    return np.column_stack([left, right])


# ─────────────────────────────────────────────────────────────
# 4. NEUTRAL & EDUCATIONAL MOOD (Balance Sheets, Data, Valuation)
# ─────────────────────────────────────────────────────────────

def gen_neutral_institutional_clarity(duration: float = 60.0) -> np.ndarray:
    """Minimalist warm electric piano Rhodes, clean corporate heartbeat, calm low-pass pad."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    bpm = 85.0
    beat_dur = 60.0 / bpm
    
    # Slow gentle Rhodes chords every 4 beats (3.0s)
    bar_dur = beat_dur * 4.0
    bar_phase = (t % bar_dur) / bar_dur
    chord_env = np.exp(-1.8 * bar_phase) * np.sin(np.pi * bar_phase)
    
    # C major 7th (C3: 130.8Hz, E3: 164.8Hz, G3: 196Hz, B3: 246.9Hz)
    chord_l = (np.sin(2 * np.pi * 130.81 * t) + 0.6 * np.sin(2 * np.pi * 164.81 * t) + 0.4 * np.sin(2 * np.pi * 196.0 * t)) * chord_env * 0.35
    chord_r = (np.sin(2 * np.pi * 131.0 * t) + 0.6 * np.sin(2 * np.pi * 196.0 * t) + 0.4 * np.sin(2 * np.pi * 246.94 * t)) * chord_env * 0.35
    
    # Gentle low-pass heartbeat
    pulse = np.sin(2 * np.pi * 65.4 * t) * np.exp(-6.0 * (t % beat_dur) / beat_dur) * 0.3
    
    return np.column_stack([chord_l + pulse, chord_r + pulse])


# ─────────────────────────────────────────────────────────────
# 5. URGENT & BREAKING NEWS MOOD (Flash Crashes, Alerts)
# ─────────────────────────────────────────────────────────────

def gen_urgent_flash_liquidation(duration: float = 60.0) -> np.ndarray:
    """Rapid 138 BPM ticking hi-hats, pounding cinematic timpani heartbeats, siren synth drone."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    bpm = 138.0
    beat_dur = 60.0 / bpm
    
    # Fast 16th-note tension ticks
    tick_dur = beat_dur / 4.0
    tick_phase = (t % tick_dur) / tick_dur
    tick = np.random.normal(0, 0.15, len(t)) * np.exp(-30.0 * tick_phase) * 0.35
    
    # Heavy cinematic heartbeat kick
    kick_phase = (t % beat_dur) / beat_dur
    kick = np.sin(2 * np.pi * (140.0 * np.exp(-18.0 * kick_phase) + 38.0) * t) * np.exp(-4.5 * kick_phase) * 0.65
    
    # Siren drone pitch modulation (alternating E2 / F2 tension)
    siren_mod = np.sin(2 * np.pi * 0.8 * t) * 6.0
    siren = np.sin(2 * np.pi * (82.41 + siren_mod) * t) * 0.25
    
    return np.column_stack([tick + kick + siren, tick * 0.7 + kick + siren * 1.1])


# ─────────────────────────────────────────────────────────────
# 6. EXPANDED PRECISION TRANSITION SFX (10 Versatile Sounds)
# ─────────────────────────────────────────────────────────────

def gen_sfx_upbeat_chime_pop() -> np.ndarray:
    """Bright melodic notification chime for positive reveals."""
    duration = 0.25
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    # G5 + C6 chime ping
    c1 = np.sin(2 * np.pi * 783.99 * t) * np.exp(-12.0 * t) * 0.6
    c2 = np.sin(2 * np.pi * 1046.50 * t) * np.exp(-10.0 * t) * 0.4
    chime = c1 + c2
    return np.column_stack([chime * 0.9, chime * 1.1])


def gen_sfx_comedic_slide_whistle() -> np.ndarray:
    """Subtle funny pitch drop for ironic or meme coin punchlines."""
    duration = 0.35
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    freq = 600.0 * np.exp(-6.0 * t) + 120.0
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    slide = np.sin(phase) * (1.0 - t / duration) * 0.5
    return np.column_stack([slide, slide])


def gen_sfx_cinematic_riser() -> np.ndarray:
    """1.2s swelling white noise riser building tension into a drop."""
    duration = 1.20
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    noise = np.random.normal(0, 0.4, len(t))
    env = (t / duration) ** 2.5
    tone_freq = 150.0 + 800.0 * (t / duration) ** 2
    phase = 2 * np.pi * np.cumsum(tone_freq) / SAMPLE_RATE
    riser = (noise * 0.6 + np.sin(phase) * 0.4) * env
    return np.column_stack([riser * 0.8, riser * 1.0])


def gen_sfx_paper_turn_flutter() -> np.ndarray:
    """Clean corporate document / report page turn for educational tables."""
    duration = 0.20
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    noise = np.random.normal(0, 0.35, len(t))
    env = np.sin(np.pi * (t / duration)) ** 3
    flutter = noise * env * np.sin(2 * np.pi * 18.0 * t)
    return np.column_stack([flutter * 0.9, flutter * 1.1])


def build_full_audio_pool():
    print("═══════════════════════════════════════════════════════════════")
    print("🚀 GENERATING COMPREHENSIVE MULTI-MOOD ROYALTY-FREE AUDIO POOL")
    print("═══════════════════════════════════════════════════════════════")

    # BGM Beds: 60s Shorts Loops + 180s Standard Video Beds
    tracks = [
        # Dark & Investigative
        ("dark_investigative/bed_01_subterranean_pulse.wav", gen_dark_subterranean, 60.0),
        ("dark_investigative/bed_02_quant_clockwork.wav", gen_dark_quant_clockwork, 60.0),
        ("dark_investigative/bed_02_quant_clockwork_180s.wav", gen_dark_quant_clockwork, 180.0), # Long format
        
        # Bullish & Upbeat
        ("bullish_upbeat/bed_02_capital_compounder.wav", gen_bullish_capital_compounder, 60.0),
        
        # Witty & Satire
        ("witty_satire/bed_01_retail_fomo_bounce.wav", gen_witty_retail_fomo_bounce, 60.0),
        
        # Neutral & Educational
        ("neutral_educational/bed_01_institutional_clarity.wav", gen_neutral_institutional_clarity, 60.0),
        ("neutral_educational/bed_01_institutional_clarity_180s.wav", gen_neutral_institutional_clarity, 180.0),
        
        # Urgent & Breaking
        ("urgent_breaking/bed_01_flash_liquidation.wav", gen_urgent_flash_liquidation, 60.0),
    ]

    for rel_path, func, dur in tracks:
        audio = func(duration=dur)
        save_wav(BGM_POOL / rel_path, audio, peak_db=-1.5)

    def sfx_01():
        t = np.linspace(0, 0.18, int(SAMPLE_RATE * 0.18), endpoint=False)
        w = np.random.normal(0, 1.0, len(t)) * (np.sin(np.pi * (t / 0.18)) ** 2) * np.exp(-15.0 * t)
        return np.column_stack([w * 0.8, w * 1.0])

    def sfx_02():
        t = np.linspace(0, 0.25, int(SAMPLE_RATE * 0.25), endpoint=False)
        phase = 2 * np.pi * np.cumsum(130.0 * np.exp(-12.0 * t) + 40.0) / SAMPLE_RATE
        thud = np.sin(phase) * np.exp(-10.0 * t)
        return np.column_stack([thud, thud])

    def sfx_03():
        t = np.linspace(0, 0.12, int(SAMPLE_RATE * 0.12), endpoint=False)
        c1 = np.exp(-80.0 * np.abs(t - 0.01)) * np.sin(2 * np.pi * 3200 * t)
        c2 = np.exp(-90.0 * np.abs(t - 0.045)) * np.sin(2 * np.pi * 2100 * t) * 0.7
        snap = c1 + c2
        return np.column_stack([snap * 0.9, snap * 1.1])

    def sfx_04():
        t = np.linspace(0, 0.09, int(SAMPLE_RATE * 0.09), endpoint=False)
        b1 = np.where(t < 0.035, np.sin(2 * np.pi * 1800 * t) * np.exp(-40.0 * t), 0)
        b2 = np.where(t >= 0.045, np.sin(2 * np.pi * 2400 * (t - 0.045)) * np.exp(-40.0 * (t - 0.045)), 0)
        return np.column_stack([(b1 + b2) * 0.85, (b1 + b2) * 1.0])

    def sfx_05():
        t = np.linspace(0, 0.15, int(SAMPLE_RATE * 0.15), endpoint=False)
        phase = 2 * np.pi * np.cumsum(800.0 * (1.0 - (t / 0.15) ** 2) + 60.0) / SAMPLE_RATE
        g = np.sin(phase) * np.exp(-6.0 * t)
        return np.column_stack([g, g])

    def sfx_06():
        t = np.linspace(0, 0.30, int(SAMPLE_RATE * 0.30), endpoint=False)
        glass = (np.sin(2 * np.pi * 880.0 * t) * np.exp(-9.0 * t) * 0.5 +
                 np.sin(2 * np.pi * 1320.0 * t) * np.exp(-12.0 * t) * 0.35 +
                 np.sin(2 * np.pi * 2200.0 * t) * np.exp(-18.0 * t) * 0.15)
        return np.column_stack([glass * 0.9, glass * 1.0])

    sfxs = [
        ("sfx_01_low_air_whoosh.wav", sfx_01),
        ("sfx_02_sub_thud_drop.wav", sfx_02),
        ("sfx_03_leica_shutter_snap.wav", sfx_03),
        ("sfx_04_terminal_data_chirp.wav", sfx_04),
        ("sfx_05_magnetic_tape_stop.wav", sfx_05),
        ("sfx_06_glass_resonator_hit.wav", sfx_06),
        ("sfx_07_upbeat_chime_pop.wav", gen_sfx_upbeat_chime_pop),
        ("sfx_08_comedic_slide_whistle.wav", gen_sfx_comedic_slide_whistle),
        ("sfx_09_cinematic_riser.wav", gen_sfx_cinematic_riser),
        ("sfx_10_paper_turn_flutter.wav", gen_sfx_paper_turn_flutter),
    ]
    for fname, func in sfxs:
        audio = func()
        save_wav(SFX_POOL / fname, audio, peak_db=-1.0)

    print("═══════════════════════════════════════════════════════════════")
    print("✨ COMPLETE: Multi-Mood BGM Library & 10 SFX Generated!")
    print("═══════════════════════════════════════════════════════════════")


if __name__ == "__main__":
    build_full_audio_pool()
