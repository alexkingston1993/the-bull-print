# High-CTR Visual & Kinetic Typography Rules

## 1. Frame Timing Standards
- **Shorts (9:16 Vertical)**: Exactly **1 frame every 3.0 seconds**.
- **Standard YouTube Videos (16:9 Landscape - Regardless of Length)**: Exactly **1 frame every 4.0 seconds**.
  - 12-minute documentary = exactly 180 distinct clean frames.

## 2. Separation of Clean Plates & Dynamic 3D Typography (Verified Winner Standard)
- **Clean Plates (Zero Baked-in Text — Kaggle Dual-T4 GPU Only)**: All generated frames MUST be clean 35mm photographic stills with **ZERO baked-in text, zero watermarks, and zero digits**.
  - **Concrete Physical Metaphors Only (Zero Boardrooms Mandate)**: Prompts must NEVER generate corporate offices, desks, suits around conference tables, or generic laptops. Every plate must depict tangible physical metaphors: split cargo ships with chains, open bank vaults sucking currency vortices, 1kg gold bars on dark marble with laser charts, aerospace fighter jets, passports in chains, robotic arms assembling microchips with sparks, or distressed traders in rain with glowing phones.
- **Dynamic 3D Blockbuster Typography Layer**:
  - **Scale**: 120–144px font scale, occupying 85–88% of canvas width (`max_sheared_w = 950`), dominating the upper third of the frame.
  - **Strict Word Cadence**: Strictly 1 to 2 words per line (e.g. `$7 TRILLION` / `DEBT TRAP`, `1.3 MILLION` / `TROOPS`, `2 CRORE` / `TRAPPED`, `₹85` / `ALL-TIME LOW`).
  - **Two-Tone Contrast**: Line 1 in vibrant electric accent (Saffron Gold `#FFE600`, Molten Fire `#FF3232`, Cyber Cyan `#06DCFF`, Mint Emerald `#10EB8C`, Hazard Orange `#FF8C14`), Line 2 in Titanium White (`#FFFFFF`).
  - **Unified Anchor Geometry (Zero Ghosting Guarantee)**: All extrusion passes, black armor strokes, and face colors render on a single unified coordinate anchor (`anchor="mt"` at `cx, line_y`). No separate sub-box coordinates or offset specular duplicate passes.
  - **1.22x Line Spacing**: Set to `int(f_size * 1.22)` ($175\text{ px}$ at $144\text{ px}$ font), providing a clean $16\text{ px}$ dark separation gap between Line 1's extrusion block and Line 2. Zero inter-line collision.
  - **Deep 22px 3D Block Extrusion & 7px Outer Armor Stroke**: 22px downward-right directional block extrusion (`cx + d * 0.45, line_y + d`) in solid black `(5, 5, 10, 255)` with a 7px solid black perimeter stroke for 100% background separation.
  - **Volumetric Neon Bloom & Dynamic Shear**: Gaussian bloom ($r=28$) radiating behind headline text with forward italic shear angle `0.22`.
- **Angled Tactical Distress Badges**: Tilted at **$-8^\circ$** with **$40\text{ px}$ vertical clearance** above Line 1. Rounded pill with a glowing $4\text{ px}$ golden/neon border and dropped shadow (`MARKET SHOCK`, `TIME-BOMB`, `CRACKDOWN`, `OVERPRICED`, `TOP SECRET`, `WARNING`).
- **Atmospheric Dark Vignette Grading**: Cinematic grade applied to all plates ($+15\%$ contrast, $+18\%$ color saturation). Top 38% procedural dark vignette separating the blockbuster title and badge; bottom 28% procedural dark vignette anchoring the lower-third captions.

## 3. Universal Word-Level Glassmorphic Captions (Mandatory for ALL Formats)
- **Universal Requirement**: Both Shorts (9:16) and Documentaries (16:9) MUST render word-level animated caption pills.
- **Glassmorphic Pill**: `rgba(8, 12, 22, 0.88)` dark rounded backdrop with emerald/cyan accent border.
- **Active Spoken Highlight**: Word actively pronounced by Christopher voice is illuminated in vibrant electric gold (`#FACC15`), while surrounding cluster words remain crisp off-white (`#F1F5F9`).
- **Safe Zone Positioning**:
  - Vertical Shorts (9:16): $Y = 1480$ (centered in 1080×1920 mobile viewport).
  - Landscape Documentaries (16:9): $Y = 920$ (centered in 1920×1080 landscape viewport).
- **Zero Border Overflow & 2-Line Auto-Wrap**: When cluster length exceeds maximum allowable pill width (max 840px in Shorts, 1480px in Docs), automatically wrap into two balanced lines, expanding the pill height dynamically. No word may ever touch or bleed outside the pill outline.

