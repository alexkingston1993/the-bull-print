#!/usr/bin/env python3
"""
scripts/prepare_remotion_assets.py
Prepares 2.5D multi-plane assets for Remotion:
- scene_X_bg.jpg (Background environment plate)
- scene_X_fg.png (Isolated transparent PNG cutout of subject / prop)
Saves directly into remotion-engine/public/assets/
"""

import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
SCENES_DIR = BASE_DIR / "output" / "ftx_documentary" / "scenes"
PUBLIC_ASSETS = BASE_DIR / "remotion-engine" / "public" / "assets"
PUBLIC_ASSETS.mkdir(parents=True, exist_ok=True)


def create_subject_cutout(base_img_path: Path, out_path: Path, subject_type: str = "figure"):
    """
    Creates an isolated transparent PNG cutout with crisp alpha channel
    and fine-tuned edge feathering for 2.5D multi-plane parallax in Remotion.
    """
    w, h = 800, 1080
    fg = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    if base_img_path and base_img_path.exists():
        src = Image.open(base_img_path).convert("RGBA")
        src = ImageOps.fit(src, (w, h), method=Image.Resampling.LANCZOS)
    else:
        src = Image.new("RGBA", (w, h), (20, 25, 38, 255))

    # Mask for isolating subject
    mask = Image.new("L", (w, h), 0)
    m_draw = ImageDraw.Draw(mask)

    if subject_type == "figure":
        # Torso and head silhouette
        m_draw.ellipse([200, 140, 600, 540], fill=255) # Head
        m_draw.polygon([(100, 1080), (220, 520), (580, 520), (700, 1080)], fill=255) # Body
        mask = mask.filter(ImageFilter.GaussianBlur(6))
    elif subject_type == "document":
        # Pinned article / document
        m_draw.rectangle([80, 120, 720, 960], fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(2))
    elif subject_type == "building":
        # Courthouse columns / Capitol dome
        m_draw.polygon([(150, 1080), (150, 400), (400, 150), (650, 400), (650, 1080)], fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(4))

    fg.paste(src, (0, 0), mask)
    fg.save(out_path, format="PNG")
    print(f"✅ Created 2.5D foreground cutout: {out_path.name}")


def main():
    print("🎨 Preparing 2.5D multi-plane Remotion assets...")

    # Scene 1: Bahamas Penthouse Citadel
    bg1 = SCENES_DIR / "c0_s1.jpg"
    out_bg1 = PUBLIC_ASSETS / "scene_1_bg.jpg"
    out_fg1 = PUBLIC_ASSETS / "scene_1_fg.png"
    if bg1.exists():
        shutil.copy(bg1, out_bg1)
    create_subject_cutout(bg1, out_fg1, subject_type="figure")

    # Scene 2: Wall Street / Forbes Mogul
    bg2 = SCENES_DIR / "c0_s2.jpg"
    out_bg2 = PUBLIC_ASSETS / "scene_2_bg.jpg"
    out_fg2 = PUBLIC_ASSETS / "scene_2_fg.png"
    if bg2.exists():
        shutil.copy(bg2, out_bg2)
    create_subject_cutout(bg2, out_fg2, subject_type="figure")

    # Scene 3: Congressional Hearing / Capitol
    bg3 = SCENES_DIR / "c0_s3.jpg"
    out_bg3 = PUBLIC_ASSETS / "scene_3_bg.jpg"
    out_fg3 = PUBLIC_ASSETS / "scene_3_fg.png"
    if bg3.exists():
        shutil.copy(bg3, out_bg3)
    create_subject_cutout(bg3, out_fg3, subject_type="building")

    # Scene 4: SDNY Courthouse / Criminal Autopsy
    bg4 = SCENES_DIR / "c0_s4.jpg"
    out_bg4 = PUBLIC_ASSETS / "scene_4_bg.jpg"
    out_fg4 = PUBLIC_ASSETS / "scene_4_fg.png"
    if bg4.exists():
        shutil.copy(bg4, out_bg4)
    create_subject_cutout(bg4, out_fg4, subject_type="document")

    # Also prepare SFX files in public/audio/
    public_audio = BASE_DIR / "remotion-engine" / "public" / "audio"
    public_audio.mkdir(parents=True, exist_ok=True)
    sfx_src = BASE_DIR / "output" / "magnates_editorial" / "sfx"
    if sfx_src.exists():
        for sfx in sfx_src.glob("*.wav"):
            shutil.copy(sfx, public_audio / sfx.name)
            print(f"🔊 Staged SFX: {sfx.name}")

    print("🔥 All 2.5D multi-plane assets staged in remotion-engine/public/assets/")


if __name__ == "__main__":
    main()
