# The Bull Print — UI/UX Design System & Architecture Specification
*Built according to Awwwards Site of the Day Standards & Groww + Screener.in Benchmarks*

---

## 1. Concept Card

- **Product Identity**: The Bull Print (`https://bullprintmedia.com`)
- **Idea**: An institutional-grade Indian market intelligence and exploration desk combining Groww's uncluttered consumer layout with Screener.in's deep fundamental financial metrics.
- **Metaphor**: A Bloomberg Terminal stripped of noise — high signal-to-noise ratio, pure readability, dark mode precision with live ticks.
- **Signature Interactions**:
  1. **Top Live Index Constituent Drawer**: Real-time tick bar across benchmark Indian indices (`NIFTY 50`, `SENSEX`, `BANK NIFTY`, `MIDCAP SELECT`, `FINNIFTY`) with an instant `Split ↗` constituent drawer displaying stock weights, live prices, 1D % changes, and 52W high/lows.
  2. **Groww-Style Tabbed Explorer**: Seamless toggle between Market Movers (Gainers / Losers / Volume Shockers with mini sparklines), Sectors Trending (with visual gainers-to-losers ratio bars), Stock Screener, and Research Articles.
  3. **Dedicated Standalone Article Pages**: Zero popup/modal traps. Each article is a dedicated, fully scrollable URL (`/article?slug=...` / `/article/:slug`) featuring reading progress telemetry, 16:9 YouTube video embeds, and valuation breakdown tables.
  4. **Screener.in Fundamental Financial Suite**: Comprehensive 9-ratio matrix (M.Cap, CMP, 52W High/Low, P/E, Book Value, Div Yield, ROCE, ROE, Debt/Equity), Pros & Cons cards, Sector Peer Comparison, 10-Year Compounding Scorecard, and Shareholding distribution.
  5. **Direct Technical Analysis Terminal**: Embedded 1080p TradingView real-time candlestick chart engine for institutional order-flow analysis.

---

## 2. Art Direction & Visual Hierarchy

### Typography
- **Headings & Display**: `Outfit` (Weights: 600, 700, 800) — Bold, geometric, modern readability.
- **Body & Navigation**: `Plus Jakarta Sans` (Weights: 400, 500, 600, 700) — Ultra-clean corporate clarity.
- **Financial Tickers & Ratios**: `JetBrains Mono` (Weights: 500, 600, 700) — Tabular numeric alignment with zero jitter on ticker ticks.

### Color Palette & Visual Tokens
- **Canvas Base**: `#070b14` (Deep obsidian dark mode)
- **Surface Elevation**: `#0c1220` (Header / navigation / top strip)
- **Card Background**: `#111a2e` / Card Hover: `#16223b`
- **Groww Mint (Positive/Gainers)**: `#00d09c` (`rgba(0, 208, 156, 0.12)` background)
- **Market Rose (Negative/Losers)**: `#f43f5e` (`rgba(244, 63, 94, 0.12)` background)
- **Bloomberg Cyan / Blue**: `#3b82f6` / `#38bdf8` (Primary badges, telemetry indicators)
- **Gold Accent (F&O / Regulatory)**: `#f59e0b`

---

## 3. Page Routes & Structural Information Architecture

| Route | Purpose | UX Highlights |
|---|---|---|
| `/` (`index.html`) | Primary Market Dashboard | Live Indices Strip, Index Split Drawer, Groww-style Movers/Sectors/Screener/Reports, Market Breadth sidebar, TradingView widget. |
| `/article?slug=:slug` (`article.html`) | Standalone Research Article | Standalone URL, full native vertical scroll, reading progress indicator, 16:9 video player, balance sheet tables, SEBI disclaimer. |
| `/stock.html?symbol=:symbol` (`stock.html`) | Stock Intelligence Hub | Complete Screener.in 9-ratio suite, Pros/Cons AI analysis, Peer comparison, 10y CAGR scorecard, live TradingView chart. |
| `/disclaimer` (`disclaimer.html`) | SEBI & Compliance Policy | Statutory SEBI RA/RIA disclosures, educational platform charter. |

---

## 4. Key Performance & UX Safeguards

1. **Zero Local Compute Burden (Two-Tier Cloud Matrix)**: All visual plate generation for Shorts (9:16) and Documentaries (16:9) runs on Kaggle Dual-T4 GPU runners (`ByteDance SDXL-Lightning`), while parallel compositing, typography, and publishing execute on GitHub Actions cloud runners. Zero local rendering.
2. **Accessible Native Scrolling**: No `document.body.style.overflow = "hidden"` traps on article content.
3. **Responsive Viewport Support**: Fluid breakpoint scaling across mobile (375px+), tablet (768px+), and ultra-wide desktop monitors (1440px+).
4. **Vercel Edge Clean Routing**: Clean rewrites for `/article/:slug` and `/stocks/:symbol` configured in `vercel.json`.

---

## 5. YouTube Shorts High-CTR Frame Standard (Google Flow AI 2K Benchmark)

To guarantee that any random frame auto-selected by YouTube's algorithm serves as a viral, high-CTR thumbnail, all Shorts are constructed from unique background frames switching exactly every **3.0 seconds** (60s Short = 20 unique frames; 30s Short = 10 unique frames), with zero frame reuse:

- **Master Reference Bank**: `assets/flow_ai_masters/`
  - `crypto_mev/`: 10 pristine 2K master frames (`frame_00.jpg` – `frame_09.jpg`).
- **Required Visual Anatomy**:
  1. **Physical 3D Graphic Anchor**: Concrete, mechanical, or tangible objects (e.g. industrial hazard bear traps crushing tokens with sparks, liquid cyber-vortex funnels, glowing terminator skulls with network wiring, shattering laser trendline arrows). Flat vector clip-art or simple 2D shapes are strictly prohibited.
  2. **Multi-Stop Incandescent 3D Typography**: Chiseled brushed-chrome / silver primary hook + molten gold / fiery red sub-hook with incandescent inner glow and drop shadow.
  3. **Dual-Tone Floating Neon Badges**: Glass/plasma rounded capsules with neon edge borders (e.g., `MEV TRAP [!]`, `BOT EXPOSED`, `92,000 WALLETS`).
  4. **Volumetric Atmosphere**: Glowing candlestick lightning, depth-of-field blur, dark obsidian vignette, falling embers, and laser grid floor.
- **Section Pacing**:
  - 60s Short: 20 unique frames × 3.0s = 60s total duration.
  - 30s Short: 10 unique frames × 3.0s = 30s total duration.

### 5.1 Google Flow AI Systematic Prompt Blueprint

Every frame prompt generated for Shorts must strictly follow the 5-part blueprint:

```
[Format & Aspect Ratio] + [Core Subject & Metaphor] + [Lighting & Color Strategy] + [Typography & Text Overlay] + [Composition & Finish]
```

- **Format**: `A high CTR viral vertical 9:16 YouTube Short thumbnail...`
- **Subject**: One primary, clear visual subject (single focal point, tangible 3D physical metaphor).
- **Lighting**: Dark obsidian background with vivid, high-saturation accents (neon cyan/mint `#14F195`, electric purple `#9945FF`, molten gold `#FACC15`, volumetric glow, rim lights).
- **Typography**: Specific 3D text styling instructions (e.g. bold 3D chiseled typography reading 2–4 high-impact words).
- **Finish**: `hyper-detailed, clean compositing, high contrast, cinematic depth of field, 8k render.`

### 5.2 High-CTR Rules for AI Models

1. **Single Focal Point**: Mobile feeds require immediate readability (< 1 second). Every frame must center on exactly ONE dramatic concept.
2. **Extreme Contrast**: Pair deep obsidian/black moody backdrops with bright neon glows or rim lighting to make elements pop off the mobile OLED screen.
3. **Concise Text Hooks (2–4 Words)**: Never render long sentences. Use short, high-impact punchy hooks (`MEV BOT TRAP`, `LIQUIDITY DRAIN`, `SLIPPAGE EXPOSED`).
4. **Image-to-Image Refinement (`:base`)**: When iterating or redesigning visual assets, supply the base reference frame so the model preserves spatial structure while elevating visual fidelity.
5. **Strict Non-Reuse Mandate**: **NEVER re-use the same images for any future Shorts or standard videos**. Each new video must generate bespoke, fresh frames customized specifically to that production's unique script.

---

## 6. Unified Viral Video Engine (`app/services/viral_video_engine.py`)

A modular, CPU-compatible rendering component for GitHub Actions, Kaggle workers, and local execution.

### 6.1 Strict Segmentation & High-CTR Frame Blueprint Standards

| Video Type | Target Aspect Ratio | Resolution | Segmentation Rule | Pacing Frequency | Dynamic Typography Engine |
|---|---|---|---|---|---|
| **Shorts (Vertical)** | 9:16 Vertical | 1080 $\times$ 1920 | **1 frame every 3.0 seconds** | 10–20 frames (30s–60s) | Clean 35mm plate + Dynamic 3D Extruded Type & Badges |
| **Standard YouTube Videos** | 16:9 Widescreen | 2560 $\times$ 1440 (2K Master) | **1 frame every 4.0 seconds** *(regardless of length)* | 180 frames (12-min doc) | Clean 35mm plate + Dynamic 3D Extruded Type & Badges |

#### Mandatory Visual & Typography Architecture (Verified Winner Standard):
1. **Clean Photographic Background Plates (100% Kaggle GPU Only)**: 100% of all visual plates across all video formats (9:16 Shorts and 16:9 Documentaries) are generated exclusively on Kaggle Dual-T4 GPUs (`alexytcreative/tbp-gpu-frame-generator`) with ByteDance SDXL-Lightning 8-step and strict negative prompt filtering. Third-party web APIs (Pollinations, Pexels, Unsplash) are permanently deprecated and removed from the codebase. Zero baked-in text, zero watermarks.
   - **Concrete Physical Metaphors Only (Zero Boardrooms Mandate)**: Prompts must NEVER generate corporate offices, suits around conference tables, or generic laptops. Every plate must depict tangible physical metaphors: split cargo ships with chains, open bank vaults sucking currency vortices, 1kg gold bars on dark marble with laser charts, aerospace fighter jets, passports in chains, robotic arms assembling microchips with sparks, or distressed traders in rain with glowing phones.
2. **Blockbuster 3D Kinetic Typography Layer**:
   - **Massive Font Scale**: 120–144px font scale, occupying 85–88% of canvas width (`max_sheared_w = 950`), dominating the upper third of the frame.
   - **Strict Word Cadence**: Strictly 1 to 2 words per line (e.g. `$7 TRILLION` / `DEBT TRAP`, `1.3 MILLION` / `TROOPS`, `2 CRORE` / `TRAPPED`, `₹85` / `ALL-TIME LOW`).
   - **Two-Tone Contrast**: Line 1 in vibrant electric accent (Saffron Gold `#FFE600`, Molten Fire `#FF3232`, Cyber Cyan `#06DCFF`, Mint Emerald `#10EB8C`, Hazard Orange `#FF8C14`), Line 2 in Titanium White (`#FFFFFF`).
   - **Unified Anchor Geometry (Zero Ghosting Guarantee)**: All extrusion passes, black armor strokes, and face colors render on a single unified coordinate anchor (`anchor="mt"` at `cx, line_y`). No separate sub-box coordinates or offset specular duplicate passes.
   - **1.22x Line Spacing**: Set to `int(f_size * 1.22)` ($175\text{ px}$ at $144\text{ px}$ font), providing a clean $16\text{ px}$ dark separation gap between Line 1's extrusion block and Line 2. Zero inter-line collision.
   - **Deep 22px 3D Block Extrusion & 7px Outer Armor Stroke**: 22px downward-right directional block extrusion (`cx + d * 0.45, line_y + d`) in solid black `(5, 5, 10, 255)` with a 7px solid black perimeter stroke for 100% background separation.
   - **Volumetric Neon Bloom & Dynamic Shear**: Gaussian bloom ($r=28$) radiating behind headline text with forward italic shear angle `0.22`.
3. **Angled High-Friction Tactical Distress Badges**: Tilted at **$-8^\circ$** with **$40\text{ px}$ vertical clearance** above Line 1. Rounded pill with a glowing $4\text{ px}$ golden/neon border and dropped shadow (`MARKET SHOCK`, `TIME-BOMB`, `CRACKDOWN`, `OVERPRICED`, `TOP SECRET`, `WARNING`).
4. **Atmospheric Dark Vignette Grading**: Cinematic grade applied to all plates ($+15\%$ contrast, $+18\%$ color saturation). Top 38% procedural dark vignette separating the blockbuster title and badge; bottom 28% procedural dark vignette anchoring the lower-third captions.
5. **Lower-Third Animated Word-Level Captions (Mandatory for ALL Formats)**: Dynamic glassmorphic caption pill (`rgba(8, 12, 22, 0.88)` with emerald/cyan accent border) displaying 3-5 word clusters with the currently spoken active word illuminated in electric gold (`#FACC15`) and inactive words in crisp off-white (`#F1F5F9`). Safe-zone positioning: $Y = 1480$ for 9:16 Shorts, $Y = 920$ for 16:9 Documentaries. Zero flat un-pillboxed text.
6. **2-Line Auto-Wrapping & Zero Overflow Guarantee**: If word cluster length exceeds safe pill width (max 840px in 9:16 Shorts, max 1480px in 16:9 Documentaries), the engine automatically splits text into two balanced, centered lines, expanding pill height dynamically. No word may ever touch or bleed outside the pill outline.

### 6.2 Word-Level Dynamic Captioning Engine

- **Audio Timestamp Extraction**: Millisecond-accurate word boundaries extracted via `faster-whisper` (`base.en`, `word_timestamps=True`).
- **Active Spoken Pop-On**: Only the word **actively pronounced by the voice** appears on screen. No trailing or pre-rendered words.
- **Strict Pause Blanking**: During natural pauses, breaths, or transitions between sentences, **zero words appear on screen** to keep the visual composition uncluttered.
- **Mute-Legible Aesthetics**:
  - High-contrast typography (80–92pt Impact / Bold) inside a floating obsidian glass pill (`rgba(5, 8, 15, 0.86)`).
  - Dual glowing neon borders (`#14F195` mint green for standard words, `#FACC15` molten gold for high-impact financial keywords).
  - Vertical positioning: Lower third ($y \approx 1530$ for 9:16 Shorts; $y \approx 1180$ for 16:9 Standard), positioned safely above platform UI controls and below central 3D visual anchors.
- **CPU Native Streaming**: Renders frame-by-frame via Pillow and pipes raw RGB24 frames directly into `ffmpeg -f rawvideo -pix_fmt yuv420p` for universal mobile/desktop hardware playback.

### 6.3 Production Deliverables Registry

1. **YouTube Shorts Upload**:
   - **Video Title**: `Solana Memecoin MEV Trap: How Bots Siphon 90% of Retail! 🚨 #shorts`
   - **Live YouTube URL**: [https://youtu.be/9oB6Fg-XpJQ](https://youtu.be/9oB6Fg-XpJQ)
   - **Video ID**: `9oB6Fg-XpJQ`
   - **Custom Thumbnail**: Flow AI 2K Master (`output/solana_mev_short/frames/revamped frames/frame_00.jpg_fb35175f_2K.jpg`)
   - **Original Video Preserved**: `output/solana_mev_short/solana-mev-bot-siphon_60s.mp4` & `solana-mev-bot-siphon_60s_raw.mp4`

2. **Published Website Article**:
   - **Slug**: `solana-mev-bot-siphon`
   - **Word Count**: **2,696 words** (Markdown in `content/posts/solana-mev-bot-siphon.md` & HTML in `content/posts.json`).
   - **Embedded Video**: Linked to live YouTube ID `9oB6Fg-XpJQ`.

3. **Standard 3-Minute 16:9 Widescreen Masterclass**:
   - **Rendered Output**: `output/solana_mev_masterclass_3m/solana-mev-masterclass_3m.mp4`
   - **Duration**: **179.52 seconds** (3.0 minutes)
   - **Resolution**: **2560 $\times$ 1440 (2K Master)** @ 25.0 fps, H.264 `yuv420p`, AAC stereo.
   - **Visual Segments**: **45 bespoke 2560x1440 frames** switching every **4.0 seconds** (`output/solana_mev_masterclass_3m/frames/frame_00.jpg` – `frame_44.jpg`).
   - **Captions**: 383 millisecond-accurate dynamic spoken-word pop-on overlays.

---

## 7. Multi-Pacing A/B Test Suite & Audio Pool Architecture

> **Legacy A/B test suite (not used for final Shorts):** final Shorts pacing is strictly **1 unique frame every 3.0 seconds**. The slot-splitting experiments below remain archived for optional in-hold variation only and must never override the 3.0s cadence or the zero-reuse mandate.

To eliminate static hold fatigue within long documentary slots without amateurish center crop-zooms or doubling image API costs, each frame slot splits cleanly at the halfway mark (`t = frame_hold / 2.0`).

### 7.1 The 3 Pacing Test Videos

- **Method A (Forensic X-Ray Shift)**: `output/test_pacing/test_method_A_forensic_lut.mp4` (5.46 MB)
  - `0.0s–5.0s`: Clean full-color visual plate with continuous ease-out pan.
  - `5.0s–10.0s`: High-contrast Forensic LUT state shift (cyan/crimson tint + dark telemetry horizontal grid lines) synced with terminal click SFX.
- **Method B (Widescreen Split-Pan)**: `output/test_pacing/test_method_B_whip_pan.mp4` (7.50 MB)
  - `0.0s–5.0s`: Left 9:16 crop of 16:9 cinematic master (Retail Perspective).
  - at `t=5.0s`: Swift motion-blurred whip-pan to the right.
  - `5.0s–10.0s`: Right 9:16 crop of 16:9 cinematic master (Institutional Perspective).
- **Method C (Glass Data Callout)**: `output/test_pacing/test_method_C_glass_hud.mp4` (4.95 MB)
  - `0.0s–5.0s`: Clean visual plate.
  - `5.0s–10.0s`: Background dims/blurs slightly, and a sleek translucent glass metric HUD strip slides in from top displaying key script data.

### 7.2 Royalty-Free / Zero-Attribution Audio Pool

- **BGM Beds** (`assets/audio/bgm_pool/`, 60s seamless stereo loops):
  - `bed_01_subterranean_pulse.wav`: 65 BPM Moog sub-bass pulse + airy shimmer.
  - `bed_02_quant_clockwork.wav`: 120 BPM clockwork ticking + D-minor analog pad drone.
  - `bed_03_offshore_noir.wav`: Atmospheric dark low string drone with harmonic filter sweeps.
  - `bed_04_cyber_forensic.wav`: 16th-note analog arpeggio low-pass filtered below 900Hz.
  - `bed_05_wall_street_afterhours.wav`: Moody Rhodes electric piano chords + warm vinyl dust.
  - `bed_06_systemic_collapse.wav`: Rising Shepard-tone dread with industrial resonance.
- **Transition SFX** (`assets/audio/sfx_pool/`):
  - `sfx_01_low_air_whoosh.wav`: 180ms deep aerodynamic swipe for scene cuts.
  - `sfx_02_sub_thud_drop.wav`: 250ms tight 60Hz sub-bass impact for heavy reveals.
  - `sfx_03_leica_shutter_snap.wav`: 120ms mechanical camera shutter click.
  - `sfx_04_terminal_data_chirp.wav`: 90ms institutional matrix double-beep for halfway splits.
  - `sfx_05_magnetic_tape_stop.wav`: 150ms pitch-down micro-glitch.
  - `sfx_06_glass_resonator_hit.wav`: 300ms crystalline harmonic resonator ping.

### 7.3 Local Christopher Phonetics (`app/utils/phonetics.py`)

- Normalizes crypto compounds (`memecoin` $\to$ `meem coin`, `Jito` $\to$ `Jee-toh`, `MEV` $\to$ `M E V`, `bullprintmedia.com` $\to$ `the bull print dot I N`, `$42M` $\to$ `42 million dollars`).
- Pre-processed strictly before voice synthesis; on-screen captions retain clean orthographic spelling.




