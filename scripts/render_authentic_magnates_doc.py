#!/usr/bin/env python3
"""
scripts/render_authentic_magnates_doc.py
The Bull Print — Authentic MagnatesMedia Documentary Engine.

BUILT FROM SCRATCH — ZERO CORPORATE SLIDES, ZERO FLAT CARDS.
Replicates the genuine MagnatesMedia / Johnny Harris documentary style:
1. 3D Camera & Multi-Plane Parallax: Continuous cinematic camera glide (dolly zoom, tilt, camera shake).
2. Physical Investigation Props:
   - Aged newspaper clippings with halftone texture
   - Polaroid photo cutouts with Scotch tape strips
   - Authentic wrinkled legal contract with IRDAI watermark
   - Wet-ink Sharpie strike-through & fluorescent highlighter sweep
   - Distressed red rubber stamp ("REJECTED / 50% SLASHED") that slams down with camera shake
   - Pinned evidence damage board with red forensic strings
3. Film Atmosphere: Subtle film grain, lens vignette, anamorphic glow.
4. Cinematic Sound Design: Synchronized sub-bass drops, whooshes, and stamp thuds.
"""

import os
import sys
import math
import subprocess
import wave
from pathlib import Path
from typing import Tuple, List, Dict, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

OUTPUT_DIR = BASE_DIR / "output" / "authentic_magnates"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = OUTPUT_DIR / "temp_segments"
TEMP_DIR.mkdir(parents=True, exist_ok=True)
SFX_DIR = OUTPUT_DIR / "sfx"
SFX_DIR.mkdir(parents=True, exist_ok=True)

# macOS System Fonts
FONT_EDITORIAL_SERIF = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
FONT_HEAVY_SANS = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_CONDENSED = "/System/Library/Fonts/Supplemental/Impact.ttf"
FONT_MONO = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"
FONT_BODY = "/System/Library/Fonts/Helvetica.ttc"

for f_check, fb in [
    (FONT_EDITORIAL_SERIF, "/System/Library/Fonts/Times.ttc"),
    (FONT_HEAVY_SANS, "/Library/Fonts/Arial Bold.ttf"),
    (FONT_CONDENSED, FONT_HEAVY_SANS),
]:
    if not Path(f_check).exists():
        f_check = fb


# ==============================================================================
# 1. 3D PERSPECTIVE MATHEMATICS & CAMERA RIG
# ==============================================================================

def find_perspective_coeffs(
    source_coords: List[Tuple[float, float]],
    target_coords: List[Tuple[float, float]]
) -> List[float]:
    matrix = []
    for p1, p2 in zip(target_coords, source_coords):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])
    A = np.matrix(matrix, dtype=float)
    B = np.array(source_coords).reshape(8)
    res = np.dot(np.linalg.pinv(A), B)
    return np.array(res).reshape(8).tolist()


def project_3d_plane(
    img: Image.Image,
    dest_center: Tuple[int, int],
    yaw: float = 0.0,
    pitch: float = 0.0,
    roll: float = 0.0,
    z_depth: float = 0.0,
    scale: float = 1.0,
    canvas_size: Tuple[int, int] = (1920, 1080),
    focal_length: float = 1200.0,
    shadow_offset: Tuple[int, int] = (25, 35),
    shadow_blur: int = 24,
    shadow_alpha: int = 140
) -> Tuple[Image.Image, Image.Image]:
    """
    Projects a 2D image into 3D space with perspective warp and realistic directional shadow.
    """
    w, h = img.size
    cw, ch = canvas_size
    cx, cy = dest_center

    hw, hh = (w * scale) / 2.0, (h * scale) / 2.0
    corners = np.array([
        [-hw, -hh, 0.0],
        [ hw, -hh, 0.0],
        [ hw,  hh, 0.0],
        [-hw,  hh, 0.0]
    ], dtype=float)

    rad_yaw = math.radians(yaw)
    rad_pitch = math.radians(pitch)
    rad_roll = math.radians(roll)

    # 3D Rotation Matrix
    Ry = np.array([
        [ math.cos(rad_yaw), 0, math.sin(rad_yaw)],
        [ 0,                 1, 0                ],
        [-math.sin(rad_yaw), 0, math.cos(rad_yaw)]
    ])
    Rx = np.array([
        [1, 0,                   0                  ],
        [0, math.cos(rad_pitch), -math.sin(rad_pitch)],
        [0, math.sin(rad_pitch),  math.cos(rad_pitch)]
    ])
    Rz = np.array([
        [math.cos(rad_roll), -math.sin(rad_roll), 0],
        [math.sin(rad_roll),  math.cos(rad_roll), 0],
        [0,                   0,                  1]
    ])
    R = Rz @ Rx @ Ry

    rotated = (R @ corners.T).T
    rotated[:, 2] += z_depth

    projected = []
    for x, y, z in rotated:
        dist = max(10.0, focal_length + z)
        factor = focal_length / dist
        projected.append((cx + x * factor, cy + y * factor))

    src_coords = [(0, 0), (w, 0), (w, h), (0, h)]
    coeffs = find_perspective_coeffs(src_coords, projected)

    warped = img.transform(canvas_size, Image.Transform.PERSPECTIVE, coeffs, Image.Resampling.BICUBIC)

    # Directional Drop Shadow
    shadow = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_poly = [(p[0] + shadow_offset[0], p[1] + shadow_offset[1]) for p in projected]
    shadow_draw.polygon(shadow_poly, fill=(5, 8, 17, shadow_alpha))
    shadow = shadow.filter(ImageFilter.BoxBlur(max(2, shadow_blur // 2)))

    return warped, shadow


# ==============================================================================
# 2. PHYSICAL INVESTIGATION PROPS & ASSETS GENERATOR
# ==============================================================================

_CACHED_DESK = None

def get_dark_investigation_desk(w: int = 1920, h: int = 1080) -> Image.Image:
    global _CACHED_DESK
    if _CACHED_DESK is None:
        _CACHED_DESK = create_dark_investigation_desk(w, h)
    return _CACHED_DESK.copy()

def create_dark_investigation_desk(w: int = 1920, h: int = 1080) -> Image.Image:
    """
    Creates a dark, moody mahogany desk surface with natural wood grain,
    ambient lighting falloff, and cinematic vignette.
    """
    desk = Image.new("RGBA", (w, h), (10, 14, 22, 255))
    draw = ImageDraw.Draw(desk)

    for y in range(0, h, 140):
        draw.line([(0, y), (w, y)], fill=(18, 24, 38, 255), width=2)
        draw.line([(0, y + 1), (w, y + 1)], fill=(5, 8, 14, 255), width=1)

    arr = np.array(desk)
    noise = np.random.normal(0, 4, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    desk = Image.fromarray(arr)

    # Volumetric spotlight falloff from top center
    spot = Image.new("L", (w, h), 0)
    s_draw = ImageDraw.Draw(spot)
    for r in range(800, 0, -40):
        alpha = int(90 * (1.0 - r / 800.0))
        s_draw.ellipse([(w // 2 - r, -100 - r // 2), (w // 2 + r, 500 + r // 2)], fill=alpha)
    spot = spot.filter(ImageFilter.BoxBlur(45))

    spot_layer = Image.new("RGBA", (w, h), (245, 230, 200, 0))
    spot_layer.putalpha(spot)
    desk = Image.alpha_composite(desk, spot_layer)

    # Vignette
    vignette = Image.new("L", (w, h), 0)
    v_draw = ImageDraw.Draw(vignette)
    for r in range(950, 400, -50):
        alpha = int(220 * ((r - 400) / 550.0))
        v_draw.rectangle([w // 2 - r, h // 2 - r // 2, w // 2 + r, h // 2 + r // 2], outline=alpha, width=50)
    vignette = vignette.filter(ImageFilter.BoxBlur(40))
    v_mask = Image.new("RGBA", (w, h), (3, 5, 10, 0))
    v_mask.putalpha(vignette)
    desk = Image.alpha_composite(desk, v_mask)

    return desk


def create_aged_newspaper_clipping(
    headline: str = "INSURERS POST RECORD 98.4% CLAIM SETTLEMENTS",
    subhead: str = "Regulator reviews policyholder retention metrics as health premiums surge nationwide",
    w: int = 1200,
    h: int = 680,
    strike_progress: float = 0.0
) -> Image.Image:
    """
    Creates an authentic aged financial newspaper clipping with halftone newsprint texture,
    masthead, column dividers, barcode, and wet-ink red marker strike-through.
    """
    # Aged newsprint paper
    base = np.full((h, w, 3), [238, 232, 218], dtype=np.float32)
    noise = np.random.normal(0, 6, (h, w, 3))
    paper = np.clip(base + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(paper).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Newspaper Masthead
    f_mast = ImageFont.truetype(FONT_EDITORIAL_SERIF, 32)
    f_date = ImageFont.truetype(FONT_MONO, 14)
    draw.text((50, 35), "THE FINANCIAL CHRONICLE", font=f_mast, fill=(20, 20, 20))
    draw.text((w - 280, 45), "SPECIAL INVESTIGATION · ISSUE 4,892", font=f_date, fill=(80, 80, 80))
    draw.line([(50, 80), (w - 50, 80)], fill=(40, 40, 40), width=3)
    draw.line([(50, 86), (w - 50, 86)], fill=(40, 40, 40), width=1)

    # Big Headline
    f_head = ImageFont.truetype(FONT_CONDENSED, 64)
    draw.text((50, 110), headline, font=f_head, fill=(15, 15, 15))

    # Subhead
    f_sub = ImageFont.truetype(FONT_EDITORIAL_SERIF, 22)
    draw.text((50, 195), subhead, font=f_sub, fill=(50, 50, 50))
    draw.line([(50, 240), (w - 50, 240)], fill=(180, 180, 180), width=1)

    # 3-Column Micro-text simulation
    col_w = (w - 160) // 3
    f_col = ImageFont.truetype(FONT_BODY, 15)
    lorem = (
        "According to public disclosures released under IRDAI guidelines, health insurers reported an aggregate "
        "Claim Settlement Ratio exceeding ninety-eight percent. However, industry insiders note that standard ratios "
        "count claim volumes rather than total rupee payouts, concealing room rent sub-limits and proportionate bill slashes."
    )
    for col_idx in range(3):
        cx = 50 + col_idx * (col_w + 30)
        draw.text((cx, 260), f"NEW DELHI — SECTION {col_idx+1}\n\n{lorem}", font=f_col, fill=(60, 60, 60))
        if col_idx < 2:
            draw.line([(cx + col_w + 15, 255), (cx + col_w + 15, 480)], fill=(200, 200, 200), width=1)

    # Giant 98.4% Callout Graphic inside the newspaper
    draw.rounded_rectangle([(50, 490), (w - 50, 630)], radius=12, fill=(225, 218, 200), outline=(180, 170, 150), width=2)
    f_big = ImageFont.truetype(FONT_HEAVY_SANS, 84)
    f_lbl = ImageFont.truetype(FONT_MONO, 20)
    draw.text((80, 505), "PUBLISHED METRIC:", font=f_lbl, fill=(80, 80, 80))
    draw.text((80, 530), "98.4% CLAIM SETTLEMENT", font=f_big, fill=(18, 24, 38))

    # Real Wet-Ink Red Sharpie Strike-Through
    if strike_progress > 0.01:
        # Multi-stroke textured marker
        x1, y1 = 70, 590
        target_x2 = w - 80
        target_y2 = 535
        curr_x2 = int(x1 + (target_x2 - x1) * strike_progress)
        curr_y2 = int(y1 + (target_y2 - y1) * strike_progress)

        for off, alpha in [(-3, 140), (0, 240), (3, 180), (-6, 70), (6, 90)]:
            draw.line([(x1, y1 + off), (curr_x2, curr_y2 + off)], fill=(220, 38, 38, alpha), width=12)

    return img


def create_forensic_contract_prop(
    highlight_prog: float = 0.0,
    stamp_prog: float = 0.0,
    w: int = 1350,
    h: int = 780
) -> Image.Image:
    """
    Creates an authentic legal contract schedule on ivory parchment with
    micro-printed clauses, fluorescent green highlighter sweep, and heavy red rubber stamp.
    """
    base = np.full((h, w, 3), [248, 245, 238], dtype=np.float32)
    noise = np.random.normal(0, 5, (h, w, 3))
    paper = np.clip(base + noise, 0, 255).astype(np.uint8)
    doc = Image.fromarray(paper).convert("RGBA")
    draw = ImageDraw.Draw(doc)

    f_pol = ImageFont.truetype(FONT_MONO, 18)
    f_sec = ImageFont.truetype(FONT_HEAVY_SANS, 26)
    f_body = ImageFont.truetype(FONT_BODY, 21)
    f_bold = ImageFont.truetype(FONT_HEAVY_SANS, 22)

    # Document Header & IRDAI Watermark
    draw.text((60, 40), "SCHEDULE II · STANDARD POLICY TERMS & CONDITIONS", font=f_pol, fill=(120, 120, 120))
    draw.text((60, 75), "SECTION 4: REIMBURSEMENT LIMITS & SUB-LIMIT DEDUCTIONS", font=f_sec, fill=(15, 23, 42))
    draw.line([(60, 118), (w - 60, 118)], fill=(200, 195, 185), width=2)

    draw.text(
        (60, 138),
        "4.1 General Hospitalization: Company indemnifies medically necessary expenses subject to sub-limits herein.",
        font=f_body,
        fill=(80, 80, 80)
    )

    # --- PROGRESSIVE FLUORESCENT HIGHLIGHTER SWEEP ---
    hl_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    hl_draw = ImageDraw.Draw(hl_layer)

    line_len = w - 120
    hl_width = int(line_len * highlight_prog)

    if hl_width > 0:
        # Line 1: Green fluorescent marker
        w1 = min(hl_width, line_len)
        hl_draw.rounded_rectangle([(55, 205), (55 + w1, 248)], radius=6, fill=(52, 211, 153, 160))
        # Line 2: Green fluorescent marker
        if hl_width > line_len * 0.3:
            w2 = min(int((hl_width - line_len * 0.3) * 1.5), line_len)
            hl_draw.rounded_rectangle([(55, 255), (55 + w2, 298)], radius=6, fill=(52, 211, 163, 160))
        # Line 3: Amber fluorescent marker (The Trap)
        if hl_width > line_len * 0.6:
            w3 = min(int((hl_width - line_len * 0.6) * 2.0), int(line_len * 0.92))
            hl_draw.rounded_rectangle([(55, 305), (55 + w3, 348)], radius=6, fill=(245, 158, 11, 175))

    doc = Image.alpha_composite(doc, hl_layer)
    draw = ImageDraw.Draw(doc)

    # Clause 4.2 Exact Policy Wording
    draw.text((60, 212), "Clause 4.2 Room Rent Sub-Limit & Proportionate Deduction:", font=f_bold, fill=(10, 15, 28))
    draw.text((60, 262), "Room boarding and nursing charges shall not exceed 1.0% of Sum Insured per day.", font=f_bold, fill=(10, 15, 28))
    draw.text((60, 312), "ALL associated surgical, diagnostic, and doctor fees shall be slashed in direct proportion.", font=f_bold, fill=(10, 15, 28))

    draw.text(
        (60, 380),
        "4.3 Formula: Payout = [Allowed Room Rate / Actual Room Rate] x (Surgeon + ICU + Diagnostic Fees)\n"
        "IRDAI Regulatory Notice: Proportionate deductions apply to entire invoice, excluding only fixed MRP medicines.",
        font=f_body,
        fill=(90, 90, 90)
    )

    # --- DISTRESSED RED RUBBER STAMP ("50% SLASHED / REJECTED") ---
    if stamp_prog > 0.01:
        stamp_w, stamp_h = 580, 180
        stamp = Image.new("RGBA", (stamp_w, stamp_h), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(stamp)

        # Distressed ink border
        s_draw.rounded_rectangle([(8, 8), (stamp_w - 8, stamp_h - 8)], radius=16, outline=(220, 38, 38, 240), width=6)
        s_draw.rounded_rectangle([(18, 18), (stamp_w - 18, stamp_h - 18)], radius=12, outline=(220, 38, 38, 160), width=2)

        f_stamp_big = ImageFont.truetype(FONT_HEAVY_SANS, 48)
        f_stamp_sub = ImageFont.truetype(FONT_MONO, 20)
        s_draw.text((36, 32), "50% BILL SLASHED", font=f_stamp_big, fill=(220, 38, 38, 255))
        s_draw.text((38, 98), "PROPORTIONATE PENALTY APPLIED", font=f_stamp_sub, fill=(185, 28, 28, 255))
        s_draw.text((38, 128), "UNDERWRITING EXCLUSION: ROOM UPGRADE", font=f_stamp_sub, fill=(185, 28, 28, 220))

        # Rotate stamp by -11 degrees
        stamp_rot = stamp.rotate(11, resample=Image.Resampling.BICUBIC, expand=True)
        
        # Scale with physical impact spring
        stamp_scale = 1.0 + (1.0 - min(1.0, stamp_prog)) * 0.4
        sw_final = int(stamp_rot.width * stamp_scale)
        sh_final = int(stamp_rot.height * stamp_scale)
        stamp_scaled = stamp_rot.resize((sw_final, sh_final), Image.Resampling.BICUBIC)

        doc.paste(stamp_scaled, (w - sw_final - 80, 430 - (sh_final - stamp_rot.height) // 2), stamp_scaled)

    return doc


def create_evidence_ledger_prop(
    row_progress: float = 1.0,
    w: int = 1450,
    h: int = 760
) -> Image.Image:
    """
    Creates an investigation evidence board itemizing the Rs. 10 Lakh damage ledger.
    """
    base = np.full((h, w, 3), [18, 24, 38], dtype=np.float32)
    noise = np.random.normal(0, 4, (h, w, 3))
    board = np.clip(base + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(board).convert("RGBA")
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(FONT_HEAVY_SANS, 34)
    f_sub = ImageFont.truetype(FONT_BODY, 22)
    f_th = ImageFont.truetype(FONT_MONO, 18)
    f_td = ImageFont.truetype(FONT_BODY, 21)
    f_bold = ImageFont.truetype(FONT_HEAVY_SANS, 22)

    draw.text((50, 40), "FORENSIC DAMAGE AUDIT · RS. 10,00,000 HOSPITAL BILL", font=f_title, fill=(248, 250, 252))
    draw.text((50, 85), "Live Actuarial breakdown after Clause 4.2 room sub-limit trigger", font=f_sub, fill=(148, 163, 184))
    draw.line([(50, 125), (w - 50, 125)], fill=(51, 65, 85), width=2)

    # Columns
    draw.rounded_rectangle([(40, 140), (w - 40, 190)], radius=8, fill=(30, 41, 59))
    cols = [(60, "BILL COMPONENT"), (490, "INVOICE"), (780, "PENALTY FORMULA"), (1140, "INSURER"), (1330, "OUT-OF-POCKET")]
    for cx, lbl in cols:
        draw.text((cx, 154), lbl, font=f_th, fill=(203, 213, 225))

    rows = [
        ("Surgeon & Anaesthetist Fees", "Rs. 4,00,000", "0.50x (Room Rent Cut)", "Rs. 2,00,000", "Rs. 2,00,000", (239, 68, 68)),
        ("Operation Theatre Charges", "Rs. 2,50,000", "0.50x (Room Rent Cut)", "Rs. 1,25,000", "Rs. 1,25,000", (239, 68, 68)),
        ("Diagnostic MRI / CT / Labs", "Rs. 1,50,000", "0.50x (Room Rent Cut)", "Rs. 75,000", "Rs. 75,000", (239, 68, 68)),
        ("Room Rent (Rs. 10K/day x 8)", "Rs. 80,000", "Rs. 5,000/day Sub-Limit", "Rs. 40,000", "Rs. 40,000", (239, 68, 68)),
        ("Pharmacy Consumables", "Rs. 1,20,000", "Excluded Non-Medical Items", "Rs. 72,000", "Rs. 48,000", (245, 158, 11)),
    ]

    for i, (item, inv, form, ins, out, c_loss) in enumerate(rows):
        if row_progress > (i * 0.18):
            ry = 205 + i * 65
            draw.rounded_rectangle([(40, ry), (w - 40, ry + 56)], radius=8, fill=(15, 23, 42) if i % 2 == 0 else (24, 32, 50))
            draw.text((60, ry + 16), item, font=f_td, fill=(248, 250, 252))
            draw.text((490, ry + 16), inv, font=f_bold, fill=(248, 250, 252))
            draw.text((780, ry + 16), form, font=f_td, fill=(248, 113, 113) if "Cut" in form else (251, 191, 36))
            draw.text((1140, ry + 16), ins, font=f_bold, fill=(52, 211, 153))
            draw.text((1330, ry + 16), out, font=f_bold, fill=c_loss)

    # Big Final Impact Ribbon
    if row_progress > 0.8:
        draw.rounded_rectangle([(40, 560), (w - 40, 710)], radius=16, fill=(11, 17, 32), outline=(16, 185, 129), width=3)
        draw.text((70, 585), "TOTAL CLAIM: Rs. 10,00,000", font=ImageFont.truetype(FONT_HEAVY_SANS, 32), fill=(255, 255, 255))
        draw.text((580, 585), "INSURER: Rs. 5,12,000 (51.2%)", font=ImageFont.truetype(FONT_HEAVY_SANS, 30), fill=(52, 211, 153))
        draw.text((1080, 585), "LOSS: Rs. 4,88,000", font=ImageFont.truetype(FONT_HEAVY_SANS, 32), fill=(239, 68, 68))
        draw.text((70, 645), "A minor Rs. 5,000 room upgrade caused an instantaneous Rs. 4,88,000 personal financial loss.", font=f_sub, fill=(203, 213, 225))

    return img


# ==============================================================================
# 3. SOUND DESIGN SYNTHESIZER (CINEMATIC SFX)
# ==============================================================================

def generate_cinematic_soundtrack(out_wav: Path, base_voiceover_wav: Path):
    """
    Synthesizes deep cinematic sub-bass braams, whooshes, and stamp thuds,
    mixing them directly into Arjun's studio voiceover track.
    """
    sample_rate = 44100

    # Load voiceover
    with wave.open(str(base_voiceover_wav), 'r') as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        raw_audio = wf.readframes(n_frames)

    voice_data = np.frombuffer(raw_audio, dtype=np.int16).astype(np.float32) / 32768.0

    # Total duration in samples
    total_samples = len(voice_data)
    master_mix = voice_data.copy()

    def add_sfx(audio_snippet: np.ndarray, start_sec: float, volume: float = 0.8):
        start_idx = int(start_sec * sample_rate)
        end_idx = min(total_samples, start_idx + len(audio_snippet))
        snip_len = end_idx - start_idx
        if snip_len > 0:
            master_mix[start_idx:end_idx] += audio_snippet[:snip_len] * volume

    # 1. Sub-bass Hit Generator
    def make_sub_bass(duration=1.4, f_start=85, f_end=35):
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        freq = np.linspace(f_start, f_end, len(t))
        phase = 2 * np.pi * np.cumsum(freq) / sample_rate
        env = np.exp(-3.2 * t)
        wave_sig = np.sin(phase) + 0.3 * np.sin(2 * phase)
        return np.tanh(wave_sig * 1.5) * env

    # 2. Whoosh Generator
    def make_whoosh(duration=0.6):
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        noise = np.random.normal(0, 1, len(t))
        env = np.sin(np.pi * t / duration) ** 2
        return noise * env * 0.4

    # 3. Stamp Thud Generator
    def make_stamp(duration=0.5):
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        thud = np.sin(2 * np.pi * 65 * t) * np.exp(-14.0 * t)
        click = np.random.normal(0, 0.4, len(t)) * np.exp(-45.0 * t)
        return (thud * 0.85 + click * 0.45)

    sub_bass = make_sub_bass()
    whoosh = make_whoosh()
    stamp = make_stamp()

    # Place SFX at exact dramatic beats
    add_sfx(sub_bass, 0.2, volume=0.7)    # Hook sub-bass hit
    add_sfx(whoosh, 6.2, volume=0.5)      # Transition to newspaper
    add_sfx(sub_bass, 8.2, volume=0.8)    # Marker strike & 61.2% slam
    add_sfx(whoosh, 12.8, volume=0.5)     # Dive into contract
    add_sfx(stamp, 17.2, volume=0.95)     # Violent 50% REJECTED stamp hit!
    add_sfx(sub_bass, 17.3, volume=0.7)   # Sub-bass tail after stamp
    add_sfx(whoosh, 19.8, volume=0.5)     # Transition to ledger
    add_sfx(sub_bass, 27.5, volume=0.75)  # Outro brand reveal

    # Normalize audio to prevent clipping
    max_val = np.max(np.abs(master_mix))
    if max_val > 0.98:
        master_mix = master_mix / max_val * 0.96

    final_int16 = (master_mix * 32767).astype(np.int16)

    with wave.open(str(out_wav), 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(final_int16.tobytes())

    print(f"🎵 Master Cinematic Soundtrack mixed with SFX: {out_wav.name}")
    return out_wav


# ==============================================================================
# 4. SCENE-BY-SCENE COMPOSITORS (GENUINE MAGNATESMEDIA STYLE)
# ==============================================================================

def render_magnates_scene_1(t_rel: float, dur: float = 6.5) -> Image.Image:
    """
    Scene 1: The Investigation Room Hook (0.0 - 6.5s)
    Camera creeps forward in 3D across the investigation desk.
    Polaroid cutout of hospital billing counter is taped to the surface.
    Bold cinematic typography types onto the desk in metallic gold & teal.
    """
    cw, ch = 1920, 1080
    p_cam = t_rel / dur
    cam_z = -40.0 + p_cam * 60.0  # Slow continuous push-in

    desk = get_dark_investigation_desk(cw, ch)

    # Title: "THE 98% ILLUSION" directly on the desk in 3D perspective
    title_canvas = Image.new("RGBA", (1400, 450), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(title_canvas)

    f_tag = ImageFont.truetype(FONT_MONO, 22)
    f_h1 = ImageFont.truetype(FONT_EDITORIAL_SERIF, 72)
    f_h2 = ImageFont.truetype(FONT_HEAVY_SANS, 96)
    f_desc = ImageFont.truetype(FONT_BODY, 26)

    t_draw.text((30, 20), "FORENSIC CLAIMS INVESTIGATION · ARTICLE #402", font=f_tag, fill=(16, 185, 129))
    t_draw.text((30, 65), "THE 98% SETTLEMENT", font=f_h1, fill=(248, 250, 252))
    
    # Glowing Emerald / Gold text
    for off in [(-3, 0), (3, 0), (0, -3), (0, 3)]:
        t_draw.text((30 + off[0], 155 + off[1]), "MARKETING ILLUSION", font=f_h2, fill=(16, 185, 129, 60))
    t_draw.text((30, 155), "MARKETING ILLUSION", font=f_h2, fill=(52, 211, 153))

    t_draw.text(
        (30, 280),
        "Why public Claim Settlement Ratios conceal the brutal mathematical reality\nof Incurred Claim Math and legal room rent exclusions.",
        font=f_desc,
        fill=(203, 213, 225)
    )

    warped_title, title_shadow = project_3d_plane(
        title_canvas,
        dest_center=(cw // 2 - 100, 320),
        yaw=14.0 - p_cam * 6.0,
        pitch=-6.0 + p_cam * 3.0,
        z_depth=cam_z,
        scale=1.0,
        canvas_size=(cw, ch),
        shadow_blur=20,
        shadow_alpha=120
    )

    desk = Image.alpha_composite(desk, title_shadow)
    desk = Image.alpha_composite(desk, warped_title)

    # Polaroid photo cutout pinned at the right edge
    pol_w, pol_h = 480, 540
    pol = Image.new("RGBA", (pol_w, pol_h), (250, 248, 242, 255))
    p_draw = ImageDraw.Draw(pol)
    p_draw.rectangle([(20, 20), (pol_w - 20, 420)], fill=(30, 40, 55))
    
    # Hospital counter icon / photo representation
    p_draw.text((40, 180), "[ EVIDENCE PHOTO: HOSPITAL BILLING ]", font=ImageFont.truetype(FONT_MONO, 18), fill=(200, 215, 230))
    p_draw.text((40, 450), "EXHIBIT A: ADMISSION DESK", font=ImageFont.truetype(FONT_MONO, 18), fill=(40, 40, 40))
    p_draw.text((40, 485), "Date: 14 Oct 2024 · Sub-limit warning", font=ImageFont.truetype(FONT_BODY, 16), fill=(100, 100, 100))

    # Yellow Scotch tape strip holding top of polaroid
    tape = Image.new("RGBA", (180, 45), (250, 220, 140, 190))
    pol.paste(tape, ((pol_w - 180) // 2, 5), tape)

    warped_pol, pol_shadow = project_3d_plane(
        pol,
        dest_center=(1520, 680),
        yaw=-16.0 + p_cam * 5.0,
        pitch=8.0,
        roll=-5.0,
        z_depth=cam_z + 20.0,
        scale=0.95,
        canvas_size=(cw, ch),
        shadow_blur=28,
        shadow_alpha=160
    )

    desk = Image.alpha_composite(desk, pol_shadow)
    desk = Image.alpha_composite(desk, warped_pol)

    return desk


def render_magnates_scene_2(t_rel: float, dur: float = 6.5) -> Image.Image:
    """
    Scene 2: The Newspaper Headline & Marker Strike (6.5 - 13.0s)
    Camera glides down onto an authentic newspaper headline.
    At t = 1.7s, a red wet-ink marker violently strikes through "98.4%".
    At t = 2.2s, the real metric "61.2% ICR" slams in with spring bounce.
    """
    cw, ch = 1920, 1080
    p_cam = t_rel / dur
    cam_z = -20.0 + p_cam * 40.0

    desk = get_dark_investigation_desk(cw, ch)

    # Strike progress starts at t = 1.6s
    strike_p = max(0.0, min(1.0, (t_rel - 1.6) / 0.55))

    paper = create_aged_newspaper_clipping(
        headline="INSURERS REPORT RECORD 98.4% CLAIM SETTLEMENT",
        subhead="Official figures conceal volume bias as high-value surgical claims face repudiation",
        strike_progress=strike_p
    )

    warped_paper, p_shadow = project_3d_plane(
        paper,
        dest_center=(cw // 2 - 120, ch // 2 - 20),
        yaw=12.0 - p_cam * 6.0,
        pitch=-7.0 + p_cam * 4.0,
        roll=-2.0,
        z_depth=cam_z,
        scale=1.0,
        canvas_size=(cw, ch),
        shadow_blur=26,
        shadow_alpha=160
    )

    desk = Image.alpha_composite(desk, p_shadow)
    desk = Image.alpha_composite(desk, warped_paper)

    # At t = 2.0s, the real metric "61.2% ICR" slams down at the right
    if t_rel > 2.0:
        p_slam = min(1.0, (t_rel - 2.0) / 0.7)
        # Spring bounce
        bounce = 1.0 - math.exp(-7.0 * p_slam) * math.cos(9.0 * p_slam) if p_slam < 1.0 else 1.0

        card_w, card_h = 560, 440
        icr_card = Image.new("RGBA", (card_w, card_h), (11, 17, 32, 250))
        c_draw = ImageDraw.Draw(icr_card)
        c_draw.rounded_rectangle([(0, 0), (card_w, card_h)], radius=20, outline=(16, 185, 129), width=3)

        c_draw.text((40, 35), "ACTUARIAL TRUTH:", font=ImageFont.truetype(FONT_MONO, 18), fill=(248, 113, 113))
        c_draw.text((40, 70), "Incurred Claim Ratio", font=ImageFont.truetype(FONT_EDITORIAL_SERIF, 32), fill=(255, 255, 255))
        
        # Giant 61.2%
        f_giant = ImageFont.truetype(FONT_HEAVY_SANS, 120)
        c_draw.text((40, 115), "61.2%", font=f_giant, fill=(52, 211, 153))

        c_draw.rounded_rectangle([(40, 275), (card_w - 40, 335)], radius=10, fill=(6, 78, 59, 240), outline=(16, 185, 129), width=2)
        c_draw.text((60, 292), "HIGH SURGERY DENIAL ZONE (<65%)", font=ImageFont.truetype(FONT_HEAVY_SANS, 20), fill=(167, 243, 208))
        c_draw.text((40, 360), "Rupees paid out vs total premium collected.\nClaims above Rs. 10 Lakh hit massive haircuts.", font=ImageFont.truetype(FONT_BODY, 18), fill=(203, 213, 225))

        warped_icr, icr_shadow = project_3d_plane(
            icr_card,
            dest_center=(1520, 520),
            yaw=-14.0,
            pitch=6.0,
            roll=2.0,
            z_depth=cam_z + 30.0,
            scale=0.7 + bounce * 0.3,
            canvas_size=(cw, ch),
            shadow_blur=32,
            shadow_alpha=180
        )

        desk = Image.alpha_composite(desk, icr_shadow)
        desk = Image.alpha_composite(desk, warped_icr)

    return desk


def render_magnates_scene_3(t_rel: float, dur: float = 7.0) -> Image.Image:
    """
    Scene 3: The Contract Forensic Dive (13.0 - 20.0s)
    Camera performs a dramatic macro dive onto Clause 4.2.
    Fluorescent green and amber highlighters sweep across the exact clause.
    At t = 4.2s, a heavy distressed red rubber stamp ("50% SLASHED") SLAMS down
    accompanied by camera shake!
    """
    cw, ch = 1920, 1080
    p_cam = t_rel / dur

    # Camera shake triggered on stamp hit (t = 4.2s)
    shake_x, shake_y = 0.0, 0.0
    if 4.2 <= t_rel <= 5.0:
        shake_intensity = (1.0 - (t_rel - 4.2) / 0.8) * 14.0
        shake_x = math.sin(t_rel * 75.0) * shake_intensity
        shake_y = math.cos(t_rel * 65.0) * shake_intensity

    # Continuous macro dive
    cam_scale = 0.95 + p_cam * 0.2
    cam_yaw = 15.0 - p_cam * 8.0
    cam_pitch = -8.0 + p_cam * 5.0

    desk = get_dark_investigation_desk(cw, ch)

    # Highlighter progress (0.8s to 3.8s)
    hl_prog = max(0.0, min(1.0, (t_rel - 0.8) / 3.0))

    # Stamp progress (triggers at t = 4.2s)
    stamp_prog = max(0.0, min(1.0, (t_rel - 4.2) / 0.5))

    contract = create_forensic_contract_prop(
        highlight_prog=hl_prog,
        stamp_prog=stamp_prog
    )

    warped_doc, doc_shadow = project_3d_plane(
        contract,
        dest_center=(int(cw // 2 + shake_x), int(ch // 2 + shake_y)),
        yaw=cam_yaw,
        pitch=cam_pitch,
        roll=-1.0,
        z_depth=0.0,
        scale=cam_scale,
        canvas_size=(cw, ch),
        shadow_blur=28,
        shadow_alpha=170
    )

    desk = Image.alpha_composite(desk, doc_shadow)
    desk = Image.alpha_composite(desk, warped_doc)

    return desk


def render_magnates_scene_4(t_rel: float, dur: float = 8.0) -> Image.Image:
    """
    Scene 4: The Rupee Crime Ledger & Evidence Board (20.0 - 28.0s)
    Shows the step-by-step breakdown of how a Rs. 10 Lakh bill is slashed
    into an out-of-pocket loss of Rs. 4,88,000.
    """
    cw, ch = 1920, 1080
    p_cam = t_rel / dur
    cam_z = -15.0 + p_cam * 35.0

    desk = get_dark_investigation_desk(cw, ch)

    # Row entrance progress
    row_prog = max(0.0, min(1.0, t_rel / 3.5))

    ledger = create_evidence_ledger_prop(row_progress=row_prog)

    warped_ledger, l_shadow = project_3d_plane(
        ledger,
        dest_center=(cw // 2, ch // 2),
        yaw=-10.0 + p_cam * 4.0,
        pitch=5.0 - p_cam * 2.0,
        roll=1.0,
        z_depth=cam_z,
        scale=1.0,
        canvas_size=(cw, ch),
        shadow_blur=30,
        shadow_alpha=160
    )

    desk = Image.alpha_composite(desk, l_shadow)
    desk = Image.alpha_composite(desk, warped_ledger)

    return desk


def render_magnates_scene_5(t_rel: float, dur: float = 10.38) -> Image.Image:
    """
    Scene 5: The Verdict & The Bull Print Brand Monolith (28.0 - 38.38s)
    Dramatic camera pull-back revealing the full investigation desk bathed in warm volumetric light.
    The Bull Print metallic gold & emerald brand monolith shines with institutional alpha badges.
    """
    cw, ch = 1920, 1080
    p_cam = t_rel / dur
    cam_z = 25.0 - p_cam * 35.0

    desk = get_dark_investigation_desk(cw, ch)

    # Brand Title Card
    brand_w, brand_h = 1300, 600
    brand_card = Image.new("RGBA", (brand_w, brand_h), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(brand_card)

    f_title = ImageFont.truetype(FONT_HEAVY_SANS, 110)
    f_sub = ImageFont.truetype(FONT_EDITORIAL_SERIF, 32)
    f_mono = ImageFont.truetype(FONT_MONO, 24)

    # Metallic Gold & Emerald Emboss
    title_text = "THE BULL PRINT"
    b_draw.text((54, 74), title_text, font=f_title, fill=(0, 0, 0, 180))
    b_draw.text((50, 70), title_text, font=f_title, fill=(245, 158, 11))
    b_draw.line([(50, 200), (brand_w - 50, 200)], fill=(16, 185, 129), width=6)

    b_draw.text((50, 225), "MATHEMATICAL CLARITY · INSTITUTIONAL ALPHA · MARKET TRUTH", font=f_sub, fill=(248, 250, 252))

    # 3 Institutional Pillars
    pillars = [
        ("01 · FINE PRINT AUDITS", "Exposing insurance sub-limits &\nactuarial repudiation traps"),
        ("02 · ORDER FLOW FORENSICS", "Tracking FII block accumulation &\nsmart money footprints"),
        ("03 · ACTUARIAL CALCULATORS", "Free mathematical tools &\narticles at bullprintmedia.com"),
    ]
    p_w = 380
    for i, (p_title, p_desc) in enumerate(pillars):
        px = 50 + i * (p_w + 30)
        b_draw.rounded_rectangle([(px, 300), (px + p_w, 480)], radius=16, fill=(15, 23, 42, 230), outline=(16, 185, 129), width=2)
        b_draw.text((px + 24, 325), p_title, font=f_mono, fill=(52, 211, 153))
        b_draw.text((px + 24, 375), p_desc, font=ImageFont.truetype(FONT_BODY, 20), fill=(203, 213, 225))

    # Portal Link Pill
    b_draw.rounded_rectangle([(320, 520), (980, 580)], radius=14, fill=(16, 185, 129), outline=(255, 255, 255, 200), width=2)
    b_draw.text((360, 538), "ACCESS ALL articles: bullprintmedia.com", font=f_mono, fill=(15, 23, 42))

    warped_brand, b_shadow = project_3d_plane(
        brand_card,
        dest_center=(cw // 2, ch // 2 - 20),
        yaw=0.0,
        pitch=0.0,
        roll=0.0,
        z_depth=cam_z,
        scale=1.0,
        canvas_size=(cw, ch),
        shadow_blur=35,
        shadow_alpha=160
    )

    desk = Image.alpha_composite(desk, b_shadow)
    desk = Image.alpha_composite(desk, warped_brand)

    return desk


# ==============================================================================
# 5. MASTER VIDEO COMPILER
# ==============================================================================

def render_segment(
    fg_fn,
    duration: float,
    out_mp4: Path,
    fps: int = 30
):
    num_frames = int(duration * fps)
    vcodec = "h264_videotoolbox" if sys.platform == "darwin" else "libx264"

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo", "-s", "1920x1080", "-pix_fmt", "rgba", "-r", str(fps), "-i", "-",
        "-r", str(fps),
        "-c:v", vcodec,
        "-b:v", "9000k",
        "-pix_fmt", "yuv420p",
        str(out_mp4)
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    for f in range(num_frames):
        t_rel = f / float(fps)
        frame = fg_fn(t_rel, duration)
        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()

    if proc.returncode != 0:
        err = proc.stderr.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"FFmpeg error: {err}")

    return out_mp4


def main():
    print("🎬 === Building Authentic MagnatesMedia Documentary (100% From Scratch) ===")

    base_audio = BASE_DIR / "output" / "magnates_test" / "master_soundtrack.wav"
    master_sfx_audio = SFX_DIR / "magnates_master_soundtrack_sfx.wav"
    out_master_mp4 = OUTPUT_DIR / "authentic_magnates_38s_sample.mp4"
    artifacts_dir = Path("/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9")

    # 1. Synthesize and mix cinematic SFX into master audio
    generate_cinematic_soundtrack(master_sfx_audio, base_audio)

    # 2. Render all 5 authentic scenes
    scene_defs = [
        ("scene1_investigation_hook", render_magnates_scene_1, 6.5),
        ("scene2_newspaper_strike", render_magnates_scene_2, 6.5),
        ("scene3_contract_forensics", render_magnates_scene_3, 7.0),
        ("scene4_damage_ledger", render_magnates_scene_4, 8.0),
        ("scene5_brand_verdict", render_magnates_scene_5, 10.38),
    ]

    segment_files = []
    for tag, fn, dur in scene_defs:
        seg_p = TEMP_DIR / f"{tag}.mp4"
        print(f"🎬 Compiling authentic MagnatesMedia scene: {tag} ({dur:.2f}s)...")
        render_segment(fn, dur, seg_p, fps=30)
        segment_files.append(seg_p)

    # 3. Concatenate and mux with master audio
    concat_txt = TEMP_DIR / "concat.txt"
    concat_txt.write_text("\n".join(f"file '{p.name}'" for p in segment_files), encoding="utf-8")

    cmd_mux = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-i", str(master_sfx_audio),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "256k",
        "-shortest",
        str(out_master_mp4)
    ]
    subprocess.run(cmd_mux, check=True, cwd=str(TEMP_DIR))
    print(f"🔥 MASTER MAGNATESMEDIA DOCUMENTARY COMPILED: {out_master_mp4.name} ({out_master_mp4.stat().st_size / (1024*1024):.1f} MB)")

    # 4. Extract 5 milestone inspection frames
    milestones = [
        ("magnates_real_01_hook_5s.jpg", 5.0),
        ("magnates_real_02_newspaper_strike_10s.jpg", 10.0),
        ("magnates_real_03_contract_stamp_18s.jpg", 18.0),
        ("magnates_real_04_damage_ledger_24s.jpg", 24.0),
        ("magnates_real_05_brand_verdict_33s.jpg", 33.0),
    ]

    for fname, ts in milestones:
        fp = OUTPUT_DIR / fname
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(ts), "-i", str(out_master_mp4),
            "-vframes", "1", "-q:v", "2", str(fp)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        art_p = artifacts_dir / fname
        art_p.write_bytes(fp.read_bytes())
        print(f"📸 Milestone frame copied to artifacts: {fname} (t={ts:.1f}s)")

    # Copy video to artifacts
    art_vid = artifacts_dir / "authentic_magnates_38s_sample.mp4"
    art_vid.write_bytes(out_master_mp4.read_bytes())
    print(f"🎥 Video copied to artifacts: {art_vid.name}")

    print("\n✅ AUTHENTIC MAGNATESMEDIA VIDEO PRODUCTION COMPLETE!")


if __name__ == "__main__":
    main()
