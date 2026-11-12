# The Bull Print: Master Video Production Blueprint

## 1. Pacing & Cut Frequency Standards (MANDATORY)

- **YouTube Shorts (9:16 Vertical)**:
  - **Cut Frequency**: Exactly **1 frame every 3.0 seconds**.
  - *Example*: A 30-second Short requires 10 distinct frames; a 36-second Short requires 12 distinct frames.
  - *Pacing Rule*: Fast, punchy micro-beats maintaining relentless visual momentum.

- **Standard YouTube Videos (16:9 Landscape - Any Length)**:
  - **Cut Frequency**: Exactly **1 frame every 4.0 seconds**, regardless of video length.
  - *Example*: A 12-minute master documentary (720 seconds) requires exactly **180 distinct frames** (36 segments × 5 micro-beats).
  - *Example*: An 8-minute documentary (480 seconds) requires exactly **120 distinct frames** (24 segments × 5 micro-beats).
  - *Pacing Rule*: Pure hard cuts or smooth documentary cross-fades without artificial digital distortion.

---

## 2. Visual & Typography Architecture (MagnatesMedia Engine)

1. **Clean Background Plates (Zero Baked-in Text — 100% Kaggle GPU Rendered)**:
   - All AI-generated image plates for **both YouTube Shorts (9:16) and Documentaries (16:9)** must be rendered exclusively on **Kaggle Dual-T4 GPUs** (`app/services/kaggle_image_worker.py`) running ByteDance SDXL-Lightning (8-step) on CUDA.
   - **STRICT PROHIBITION**: Zero baked-in text, zero letters, zero numbers, zero typography, zero watermarks in prompts. All generations must enforce the strict negative prompt:
     `text, letters, words, numbers, digits, typography, watermark, logo, signage, banners, ticker symbols, displays with writing, labels, subtitles, signature, font, writing, cartoon, anime, 3d render, blurry, distorted, low quality`
   - Absolutely zero reliance on third-party web image APIs (Pollinations, Pexels, Unsplash) for video production. Every frame is a dedicated GPU-rendered 35mm clean plate.

2. **Dynamic Kinetic 3D Typography Layer**:
   - Giant stacked 3D extruded perspective typography rendered dynamically via the visual engine.
   - Forward italic shear angle (`0.22`), 16px extrusion shadow block, and saturated color grading (Crimson `#F51937` or Saffron Gold `#FFD700`).
   - Volumetric neon bloom / atmospheric aura radiating behind headline text (`GaussianBlur radius=28`).
   - Elastic kinetic slam pop-in (`1.35x -> 1.0x` over 0.45s) synchronized to narrator emphasis.

3. **High-Contrast Tactical Highlighter Badges**:
   - Stabilo-style glowing alert badges placed above headlines (e.g., `'DALAL STREET BOMBSHELL'`, `'OCTOBER SURPRISE'`, `'FED TRAPPED'`).
   - Saturated pill background with dark contrasting text or reverse-contrast alert glow.

4. **Lower-Third Word-Level Animated Captions (Mandatory for ALL Formats)**:
   - **Universal Requirement**: Applied to **both YouTube Shorts (9:16) and Standard Master Documentaries (16:9)** without exception. Zero flat un-pillboxed text.
   - **Chunk Structure**: Displayed in dynamic 3-to-5 word clusters inside a semi-transparent glassmorphic pill backdrop (`rgba(8, 12, 22, 0.88)` with emerald/cyan accent border).
   - **Active Spoken Highlight**: The currently pronounced word illuminates in vibrant electric gold (`#FACC15`), while inactive words in the cluster remain crisp off-white (`#F1F5F9`).
   - **Safe-Zone Positioning**:
     - **Vertical Shorts (9:16)**: $Y = 1480$ (centered in 1080×1920 mobile viewport).
     - **Standard Landscape Documentaries (16:9)**: $Y = 920$ (centered in 1920×1080 widescreen viewport).
   - **Camera Motion**: Every beat must feature smooth camera slow dolly/zoom drift (`1.00 -> 1.05`) synchronized across background plates.

---

## 3. Audio & Voiceover Standards

- **Narrator**: `en-US-ChristopherNeural` with `-2Hz` pitch calibration.
- **Soundtrack**: Ambient tension drone / modular 5-act score normalized to `-18 LUFS` relative to voiceover.
- **Workflow Sequence**: Lock narrative script -> synthesize voiceovers -> extract exact millisecond beat timestamps -> generate clean background plates -> composite & render.
