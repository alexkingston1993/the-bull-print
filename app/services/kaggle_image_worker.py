#!/usr/bin/env python3
"""
The Bull Print — Kaggle GPU Frame Generation Worker (app/services/kaggle_image_worker.py)

Dispatches image generation batches to Kaggle's free Nvidia Tesla T4 GPU (30 hours/week quota).
Executes diffusers pipelines on CUDA, generates 16:9 high-CTR documentary plates,
and downloads the output frames directly into the project workspace.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


class KaggleImageWorker:
    """Automated Kaggle GPU runner for batch image generation."""

    def __init__(self, username: Optional[str] = None):
        self.username = username or self._detect_username()
        self.kernel_slug = "tbp-gpu-frame-generator"
        self.stage_dir = BASE_DIR / "kaggle_stage_image"
        self.stage_dir.mkdir(parents=True, exist_ok=True)

    def _detect_username(self) -> str:
        cfg = Path.home() / ".kaggle" / "kaggle.json"
        if cfg.exists():
            try:
                with open(cfg) as f:
                    data = json.load(f)
                    return data.get("username", "alexytcreative")
            except Exception:
                pass
        return os.getenv("KAGGLE_USERNAME", "alexytcreative")

    def create_kernel_script(self, segments: List[Dict[str, Any]]) -> str:
        """Generates the Python worker script to execute inside the Kaggle GPU kernel."""
        # Sanitize segments to only what's needed: id, prompt, title
        payload = [
            {
                "id": s["id"],
                "prompt": s["prompt"],
                "title": s.get("title", f"Segment {s['id']}")
            }
            for s in segments
        ]
        payload_json = json.dumps(payload, indent=2)

        script = f'''# Auto-generated Kaggle GPU Frame Generator
import os
import sys
import time
import json
import torch

print("[KaggleWorker] Booting Python on GPU...", flush=True)
print(f"[KaggleWorker] CUDA Available: {{torch.cuda.is_available()}}", flush=True)
if torch.cuda.is_available():
    print(f"[KaggleWorker] Device: {{torch.cuda.get_device_name(0)}} (VRAM: {{torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}} GB)", flush=True)

# Install diffusers & accelerate
print("[KaggleWorker] Installing diffusers, transformers, accelerate...", flush=True)
os.system("pip install -q diffusers transformers accelerate safetensors")

from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

base = "stabilityai/stable-diffusion-xl-base-1.0"
repo = "ByteDance/SDXL-Lightning"
ckpt = "sdxl_lightning_8step_unet.safetensors"

print(f"[KaggleWorker] Loading SDXL-Lightning 8-step model from {{repo}} with strict negative prompt enforcement...", flush=True)
config = UNet2DConditionModel.load_config(base, subfolder="unet")
unet = UNet2DConditionModel.from_config(config).to("cuda", torch.float16)
unet.load_state_dict(load_file(hf_hub_download(repo, ckpt), device="cuda"))
pipe = StableDiffusionXLPipeline.from_pretrained(base, unet=unet, torch_dtype=torch.float16, variant="fp16").to("cuda")
pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")

NEGATIVE_PROMPT = "text, letters, words, numbers, digits, typography, watermark, logo, signage, banners, ticker symbols, displays with writing, labels, subtitles, signature, font, writing, cartoon, anime, 3d render, blurry, distorted, low quality"

out_dir = "/kaggle/working/frames"
os.makedirs(out_dir, exist_ok=True)

PAYLOAD = {payload_json}

print(f"[KaggleWorker] Starting batch generation for {{len(PAYLOAD)}} frames with zero-baked-text enforcement...", flush=True)
for item in PAYLOAD:
    seg_id = item["id"]
    prompt = item["prompt"]
    out_path = os.path.join(out_dir, f"segment_{{seg_id:02d}}.jpg")
    print(f"--> Rendering Segment {{seg_id:02d}}: {{item['title']}}...", flush=True)
    t0 = time.time()
    
    # 16:9 ratio (1024 x 576) with CFG & Negative Prompt Enforcement
    image = pipe(
        prompt=prompt,
        negative_prompt=NEGATIVE_PROMPT,
        num_inference_steps=8,
        guidance_scale=1.5,
        width=1024,
        height=576
    ).images[0]
    
    image.save(out_path, quality=95)
    elapsed = time.time() - t0
    print(f"✓ Saved Clean Segment {{seg_id:02d}} in {{elapsed:.2f}}s", flush=True)

print("[KaggleWorker] All clean photographic frames generated successfully!", flush=True)
'''
        return script

    def dispatch(self, segments: List[Dict[str, Any]]) -> bool:
        """Pushes the kernel to Kaggle and monitors its execution."""
        logger.info(f"Preparing Kaggle GPU Kernel for {len(segments)} frames...")
        script_content = self.create_kernel_script(segments)
        
        script_file = self.stage_dir / "generate_frames.py"
        with open(script_file, "w") as f:
            f.write(script_content)

        metadata = {
            "id": f"{self.username}/{self.kernel_slug}",
            "title": "TBP GPU Frame Generator",
            "code_file": "generate_frames.py",
            "language": "python",
            "kernel_type": "script",
            "is_private": "true",
            "enable_gpu": "true",
            "enable_tpu": "false",
            "enable_internet": "true",
            "dataset_sources": [],
            "competition_sources": [],
            "kernel_sources": []
        }
        
        with open(self.stage_dir / "kernel-metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        kaggle_bin = shutil.which("kaggle") or str(BASE_DIR / ".venv" / "bin" / "kaggle")
        logger.info(f"Pushing kernel '{self.username}/{self.kernel_slug}' to Kaggle GPU...")
        res = subprocess.run([str(kaggle_bin), "kernels", "push", "-p", str(self.stage_dir)], capture_output=True, text=True)
        if res.returncode != 0:
            logger.error(f"Kaggle push failed: {res.stderr}")
            return False

        logger.info("Kernel pushed successfully! Waiting for Kaggle GPU execution...")
        return True

    def poll_and_download(self, dest_dir: Path, timeout_sec: int = 600) -> bool:
        """Polls Kaggle status until complete, then downloads the rendered frames."""
        kaggle_bin = shutil.which("kaggle") or str(BASE_DIR / ".venv" / "bin" / "kaggle")
        ref = f"{self.username}/{self.kernel_slug}"
        start_time = time.time()

        while time.time() - start_time < timeout_sec:
            time.sleep(15)
            res = subprocess.run([str(kaggle_bin), "kernels", "status", ref], capture_output=True, text=True)
            status_line = res.stdout.strip()
            logger.info(f"[Kaggle Status] {status_line}")

            if "complete" in status_line.lower():
                logger.info("Kaggle GPU generation complete! Downloading output frames...")
                out_res = subprocess.run([str(kaggle_bin), "kernels", "output", ref, "-p", str(dest_dir)], capture_output=True, text=True)
                if out_res.returncode == 0:
                    logger.info(f"✓ Frames downloaded to {dest_dir}")
                    return True
                else:
                    logger.error(f"Failed to download outputs: {out_res.stderr}")
                    return False
            elif "error" in status_line.lower():
                logger.error(f"Kaggle kernel failed: {status_line}")
                return False

        logger.error("Timed out waiting for Kaggle GPU kernel.")
        return False


if __name__ == "__main__":
    from output.sebi_hft_documentary.chapters_script import SEGMENTS
    remaining = [s for s in SEGMENTS if s["id"] >= 11]
    worker = KaggleImageWorker()
    if worker.dispatch(remaining):
        dest = BASE_DIR / "output" / "sebi_hft_documentary" / "frames"
        worker.poll_and_download(dest)
