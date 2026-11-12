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
- Ensure zero baked-in text in background plates, dynamic 3D kinetic typography (0.22 shear, 16px extrusion shadow, Gaussian bloom $r=28$), and lower-third word-level animated captions inside glassmorphic pills with vibrant electric gold (`#FACC15`) active-word highlight across ALL formats (safe zone $Y = 1480$ for 9:16 Shorts, $Y = 920$ for 16:9 Documentaries).
