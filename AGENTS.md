# The Bull Print: Standing Rules & Execution Boundaries

## Mandatory Rules (Non-Negotiable)

### 1. 100% Cloud Execution Only (Zero Local Rendering)
- Never run heavy FFmpeg compositing, video encoding, or bulk image rendering on the local machine.
- **Two-Tier Autonomous Cloud Architecture**:
  1. **Kaggle GPU Cloud Engine (`alexytcreative/tbp-gpu-frame-generator`)**: Generates 100% of all visual plates for **both YouTube Shorts (9:16) and Documentaries (16:9)** using native CUDA `diffusers` with ByteDance SDXL-Lightning (8-step) and strict negative prompt enforcement. Zero reliance on third-party web image APIs (Pollinations, Pexels, Unsplash).
  2. **GitHub Actions Cloud Runners (`parallel_video_matrix.yml`)**: Dispatches up to 20 parallel Ubuntu workers to composite master video files, render dynamic 3D kinetic typography, duck audio, align word-level safe-zone captions, and publish directly to YouTube.

### 2. Strict Zero Frame Reuse Mandate
- Generated frames must NEVER be reused, recycled, or modulo-looped (`b_num % len(...)`).
- Every single beat must have a fresh, uniquely generated clean photographic plate from Kaggle GPU.
- Cut pacing must strictly adhere to `.agents/rules/MASTER_BLUEPRINT.md`:
  - **YouTube Shorts (9:16 Vertical)**: Exactly 1 unique frame every 3.0 seconds (60s = 20 unique frames, 30s = 10 unique frames, 36s = 12 unique frames).
  - **Documentaries (16:9 Landscape)**: Exactly 1 unique frame every 4.0 seconds (12 min = 180 unique frames, 8 min = 120 unique frames).

### 3. Mandatory Design Blueprint Validation
- Before dispatching any cloud production or publishing, validate the manifest, assets, and typography against:
  1. `.agents/rules/MASTER_BLUEPRINT.md`
  2. `DESIGN.md`
  3. `.agents/rules/HIGH_CTR_FRAMES.md`
  4. `.agents/rules/viral_thumbnail_gold_standard.md`
- **Blockbuster 3D Kinetic Typography (Verified Winner Standard)**:
  - Massive scale: 120-144px font scale, occupying 85-88% of canvas width (`max_sheared_w = 950`).
  - Strict 1 to 2 words per line power hooks (e.g. `$7 TRILLION` / `DEBT TRAP`, `1.3 MILLION` / `TROOPS`, `2 CRORE` / `TRAPPED`, `₹85` / `ALL-TIME LOW`).
  - Two-tone contrast: Line 1 in electric accent (Saffron Gold `#FFE600`, Molten Fire `#FF3232`, Cyber Cyan `#06DCFF`, Mint Emerald `#10EB8C`, Hazard Orange `#FF8C14`), Line 2 in Titanium White (`#FFFFFF`).
  - Unified anchor geometry (`anchor="mt"` at `cx, line_y`) strictly preventing ghosting or duplicate text passes.
  - Clean 1.22x line spacing ($175\text{ px}$ at $144\text{ px}$ font) providing a crisp $16\text{ px}$ dark separation gap between Line 1's extrusion block and Line 2. Zero inter-line collision.
  - Deep 22px 3D block extrusion shadow, 7px solid black outer armor rim stroke for 100% background separation, and Gaussian bloom $r=28$ with forward italic shear 0.22.
  - Angled tactical distress badge tilted at -8° with 40px vertical clearance above Line 1, 4px glowing golden border, and drop shadow.
  - Atmospheric dark vignette grading (top 38% for title separation, bottom 28% for captions).
- **Concrete Physical Metaphors Only (Zero Boardrooms Mandate)**:
  - Visual prompts must NEVER generate corporate offices, suits around conference tables, or generic laptops.
  - Every visual plate must depict tangible physical metaphors: split cargo ships with chains, open bank vaults sucking currency vortices, 1kg gold bars on dark marble with laser charts, aerospace fighter jets, passports in chains, robotic arms assembling microchips with sparks, or distressed traders in rain with glowing phones.
- **Lower-Third Word-Level Captions**:
  - Safe zone $Y = 1480$ for 9:16 Shorts, $Y = 920$ for 16:9 Documentaries in glassmorphic pills with vibrant electric gold (`#FACC15`) active-word highlight.
  - Strict Zero Caption Overflow: When cluster text width exceeds maximum pill width, the engine MUST wrap into two balanced lines with dynamic pill height expansion. No text may ever touch or bleed outside the pill outline.
