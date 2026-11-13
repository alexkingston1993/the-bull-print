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

## 2. Visual & Typography Architecture (MagnatesMedia Engine - Gold Standard)

1. **Clean Background Plates (Zero Baked-in Text — 100% Kaggle GPU Rendered)**:
   - All AI-generated image plates for **both YouTube Shorts (9:16) and Documentaries (16:9)** must be rendered exclusively on **Kaggle Dual-T4 GPUs** (`app/services/kaggle_image_worker.py`) running ByteDance SDXL-Lightning (8-step) on CUDA.
   - **Concrete Physical Metaphors Only (Zero Boardrooms Mandate)**:
     - Prompts must NEVER generate corporate offices, desks, suits around conference tables, or generic laptops.
     - Every visual plate must depict tangible physical metaphors: split cargo ships with chains, open bank vaults sucking currency vortices, 1kg gold bars on dark marble with laser charts, aerospace fighter jets, passports in chains, robotic arms assembling microchips with sparks, or distressed traders in rain with glowing phones.
   - **STRICT PROHIBITION**: Zero baked-in text, zero letters, zero numbers, zero typography, zero watermarks in prompts. All generations must enforce the strict negative prompt:
     `text, letters, words, numbers, digits, typography, watermark, logo, signage, banners, ticker symbols, displays with writing, labels, subtitles, signature, font, writing, cartoon, anime, 3d render, blurry, distorted, low quality`
   - Absolutely zero reliance on third-party web image APIs (Pollinations, Pexels, Unsplash) for video production. Every frame is a dedicated GPU-rendered 35mm clean plate.

2. **Blockbuster 3D Kinetic Typography Layer (Verified Winner)**:
   - **Massive Font Scale**: Baseline 120–144px font scale, occupying 85–88% of canvas width (`max_sheared_w = 950`), dominating the upper 35% of the frame.
   - **Strict Word Cadence**: Strictly 1 to 2 words per line (e.g., `$7 TRILLION` / `DEBT TRAP`, `1.3 MILLION` / `TROOPS`, `2 CRORE` / `TRAPPED`, `₹85` / `ALL-TIME LOW`). Long phrases MUST be auto-split to prevent font shrinkage.
   - **Two-Tone Contrast**:
     - Line 1 in vibrant electric accent: Saffron Gold (`#FFE600`), Molten Fire (`#FF3232`), Cyber Cyan (`#06DCFF`), Mint Emerald (`#10EB8C`), or Hazard Orange (`#FF8C14`).
     - Line 2 in Titanium White (`#FFFFFF`).
   - **Unified Anchor Geometry (Zero Ghosting / Duplication Guarantee)**:
     - All extrusion passes, black armor strokes, and face colors MUST render on a single unified coordinate anchor (`anchor="mt"` at `cx, line_y`). Never use separate sub-box coordinates or offset specular duplicates.
   - **Clean 1.22x Line Spacing**: Spacing set to `int(f_size * 1.22)` ($175\text{ px}$ at $144\text{ px}$ font), ensuring a crisp $16\text{ px}$ dark separation gap between Line 1's extrusion block and Line 2. Zero inter-line collision.
   - **Deep 22px 3D Block Extrusion & 7px Outer Armor Stroke**:
     - 22px downward-right directional block extrusion (`cx + d * 0.45, line_y + d`) in solid black `(5, 5, 10, 255)`.
     - 7px thick black outer perimeter stroke for 100% background separation against any brightness.
   - **Volumetric Neon Bloom & Dynamic Shear**:
     - Gaussian bloom ($r=28$) radiating behind headline text.
     - Forward italic shear angle `0.22` giving aggressive forward momentum.
     - Elastic kinetic slam pop-in (`1.35x -> 1.0x` over 0.45s) synchronized to narrator emphasis.

3. **Angled High-Friction Tactical Distress Badges**:
   - Tilted at **$-8^\circ$** to break visual symmetry.
   - Placed with **$40\text{ px}$ vertical clearance** above Line 1 so the tilted corner never collides with the headline.
   - Deep red/accent pill body with a glowing $4\text{ px}$ golden/neon border and dropped shadow.
   - High-friction urgency stamps: `MARKET SHOCK`, `TIME-BOMB`, `CRACKDOWN`, `OVERPRICED`, `TOP SECRET`, `WARNING`.

4. **Atmospheric Dark Vignette Grading**:
   - Cinematic grade applied to all plates ($+15\%$ contrast, $+18\%$ color saturation).
   - Top 38% procedural dark vignette separating the blockbuster title and badge.
   - Bottom 28% procedural dark vignette anchoring the lower-third captions.

5. **Lower-Third Word-Level Animated Captions (Mandatory for ALL Formats)**:
   - **Universal Requirement**: Applied to **both YouTube Shorts (9:16) and Standard Master Documentaries (16:9)** without exception. Zero flat un-pillboxed text.
   - **Chunk Structure**: Displayed in dynamic 3-to-5 word clusters inside a semi-transparent glassmorphic pill backdrop (`rgba(8, 12, 22, 0.88)` with emerald/cyan accent border).
   - **Active Spoken Highlight**: The currently pronounced word illuminates in vibrant electric gold (`#FACC15`), while inactive words in the cluster remain crisp off-white (`#F1F5F9`).
   - **Zero Border Overflow & 2-Line Auto-Wrap Guarantee**: If cluster text width exceeds allowable safe pill width (max 840px in 9:16 Shorts, max 1480px in 16:9 Documentaries), the engine MUST automatically wrap the text into two balanced, centered lines. The pill height dynamically expands to encase both lines. Under no circumstance may any word touch, clip, or bleed outside the pill outline or viewport boundaries.
   - **Safe-Zone Positioning**:
     - **Vertical Shorts (9:16)**: $Y = 1480$ (centered in 1080×1920 mobile viewport).
     - **Standard Landscape Documentaries (16:9)**: $Y = 920$ (centered in 1920×1080 widescreen viewport).
   - **Camera Motion**: Every beat must feature smooth camera slow dolly/zoom drift (`1.00 -> 1.05`) synchronized across background plates.

---

## 3. Audio & Voiceover Standards

- **Narrator**: `en-US-ChristopherNeural` with `-2Hz` pitch calibration.
- **Soundtrack**: Ambient tension drone / modular 5-act score normalized to `-18 LUFS` relative to voiceover.
- **Workflow Sequence**: Lock narrative script -> synthesize voiceovers -> extract exact millisecond beat timestamps -> generate clean background plates -> composite & render.
