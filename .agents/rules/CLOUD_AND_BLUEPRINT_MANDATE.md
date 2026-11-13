# Mandatory Standing Rule: 100% Cloud Execution, Zero Frame Reuse & Blueprint Validation

## 1. 100% Cloud Execution Rule (ZERO Local Compute)
- **STRICT PROHIBITION**: NEVER render video pipelines, heavy FFmpeg composites, or bulk frame synthesis on the user's local Mac machine.
- **CLOUD MATRIX DISPATCH**: All video generation, multi-segment rendering, audio ducking, and final aggregation MUST run in the cloud on GitHub Actions runners via `.github/workflows/parallel_video_matrix.yml` (using `/usr/local/bin/gh workflow run parallel_video_matrix.yml ...`).
- **Local Machine Boundary**: The local workspace is strictly for code editing, lightweight orchestration, inspection, and metadata management.

---

## 2. Strict Zero-Reuse Mandate (Zero Duplicate Frames)
- **NO FRAME RECYCLING**: NEVER reuse frames, never modulo loop (`b_num % len(frames)`), and never re-use assets across beats or past videos.
- **BESPOKE PER BEAT**: Every single micro-beat requires a fresh, uniquely generated clean plate customized specifically to that beat's narration.
- **PACING QUANTITY ENFORCEMENT**:
  - **Shorts (9:16)**: Exactly **1 unique frame every 3.0 seconds** (e.g., 30s Short = 10 unique frames; 60s Short = 20 unique frames).
  - **Documentaries (16:9)**: Exactly **1 unique frame every 4.0 seconds** (e.g., 12-minute documentary = 180 unique frames; 8-minute documentary = 120 unique frames).
- If any frame hash is duplicated or count < required, the production fails validation immediately.

---

## 3. Mandatory Blueprint Pre-Flight Validation (Verified Winner Standard)
Before dispatching any cloud job or publishing:
1. **Validate against `.agents/rules/MASTER_BLUEPRINT.md`**:
   - Clean background plates (zero baked-in text/letters/numbers in AI image prompts).
   - Concrete physical visual metaphors only (bank vaults, cargo ships, 1kg gold bars, fighter jets, passports in chains, robotic assembly lines, panic traders in rain with phones; ZERO corporate boardrooms, suits, or desks).
   - Blockbuster 3D kinetic typography: massive 120–144px scale (`max_sheared_w = 950`), strictly 1–2 words per line, two-tone color contrast (Hero accent + Titanium White), unified anchor geometry (`anchor="mt"` preventing duplicate ghosting), 1.22x line spacing (16px dark gap between lines), 22px deep 3D block extrusion, 7px outer armor stroke, and volumetric neon bloom ($r=28$) with forward italic shear 0.22.
   - Angled tactical distress badge: tilted at -8° with 40px vertical clearance above Line 1.
   - Atmospheric dark vignette grading (top 38%, bottom 28%).
   - Universal lower-third animated word-level captions in glassmorphic pills with vibrant electric gold (`#FACC15`) active highlight and 2-line auto-wrapping.
   - Voiceover calibrated to `en-US-ChristopherNeural` (-2Hz pitch) with ambient score sidechain-ducked to -18 LUFS.
2. **Validate against `DESIGN.md`**:
   - Flow AI 2K benchmark standards.
   - High-contrast OLED dark background with vibrant rim lighting.
   - Extreme focal point clarity (< 1s mobile comprehension).
