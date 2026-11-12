# High-CTR Visual & Kinetic Typography Rules

## 1. Frame Timing Standards
- **Shorts (9:16 Vertical)**: Exactly **1 frame every 3.0 seconds**.
- **Standard YouTube Videos (16:9 Landscape - Regardless of Length)**: Exactly **1 frame every 4.0 seconds**.
  - 12-minute documentary = exactly 180 distinct clean frames.

## 2. Separation of Clean Plates & Dynamic 3D Typography
- **Clean Plates**: All generated frames MUST be clean 35mm photographic stills with **ZERO baked-in text**.
- **Dynamic 3D Typography Layer**: Headlines and badges are rendered dynamically on top of the clean plates using the Python MagnatesMedia kinetic typography engine (forward shear, 16px extrusion, neon volumetric bloom, elastic slam).
- **Badges**: High-contrast tactical alert pills (e.g. `'OCTOBER SURPRISE'`, `'RS. 14,900 CR INFLOW'`, `'FED TRAPPED'`).

## 3. Universal Word-Level Glassmorphic Captions (Mandatory for ALL Formats)
- **Universal Requirement**: Both Shorts (9:16) and Documentaries (16:9) MUST render word-level animated caption pills.
- **Glassmorphic Pill**: `rgba(8, 12, 22, 0.88)` dark rounded backdrop with emerald/cyan accent border.
- **Active Spoken Highlight**: Word actively pronounced by Christopher voice is illuminated in vibrant electric gold (`#FACC15`), while surrounding cluster words remain crisp off-white (`#F1F5F9`).
- **Safe Zone Positioning**:
  - Vertical Shorts (9:16): $Y = 1480$ (centered in 1080×1920 mobile viewport).
  - Landscape Documentaries (16:9): $Y = 920$ (centered in 1920×1080 landscape viewport).
- **Zero Border Overflow & 2-Line Auto-Wrap**: When cluster length exceeds maximum allowable pill width (max 840px in Shorts, 1480px in Docs), automatically wrap into two balanced lines, expanding the pill height dynamically. No word may ever touch or bleed outside the pill outline.

