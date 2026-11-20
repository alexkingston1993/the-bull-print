#!/usr/bin/env python3
"""
The Bull Print — Kaggle GPU Frame Generation Worker (app/services/kaggle_image_worker.py)

Dispatches image generation batches to Kaggle's Dual Nvidia Tesla T4 GPUs.
Executes native SDXL-Lightning diffusers pipelines on CUDA across cuda:0 and cuda:1,
generates 100% bespoke photographic plates at native 1MP SDXL resolutions:
- 768x1344 for Vertical 9:16 Shorts
- 1344x768 for Landscape 16:9 Documentaries
Includes API queue lock, BATCH_UUID verification, and isolated download paths.
"""

from __future__ import annotations

import json
import os
import random
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


class KaggleImageWorker:
    """Automated Kaggle Dual-T4 GPU runner for batch image generation."""

    def __init__(self, username: Optional[str] = None):
        self.username = username or self._detect_username()
        self.kernel_slug = "tbp-gpu-frame-generator"
        self.stage_dir = BASE_DIR / "kaggle_stage_image"
        self.stage_dir.mkdir(parents=True, exist_ok=True)

    def _detect_username(self) -> str:
        if os.getenv("KAGGLE_API_TOKEN"):
            return os.getenv("KAGGLE_USERNAME", "alexkingston")
        cfg = Path.home() / ".kaggle" / "kaggle.json"
        if cfg.exists():
            try:
                with open(cfg) as f:
                    data = json.load(f)
                    return data.get("username", "alexkingston")
            except Exception:
                pass
        return os.getenv("KAGGLE_USERNAME", "alexkingston")

    def _get_kaggle_cmd(self) -> str:
        return shutil.which("kaggle") or str(BASE_DIR / ".venv" / "bin" / "kaggle")

    def wait_for_queue_lock(self, timeout_sec: int = 600) -> bool:
        """
        API-Level Queue Lock:
        Polls Kaggle kernel status before pushing to prevent concurrency collisions.
        If a batch is already running/queued, waits with jittered sleep until it completes.
        Strict check: an empty status or buffering response is treated as BUSY.
        """
        kaggle_bin = self._get_kaggle_cmd()
        ref = f"{self.username}/{self.kernel_slug}"
        start_time = time.time()
        logger.info(f"Checking Kaggle GPU queue lock for '{ref}'...")

        while time.time() - start_time < timeout_sec:
            res = subprocess.run([str(kaggle_bin), "kernels", "status", ref], capture_output=True, text=True)
            status_line = (res.stdout or "").strip().lower()

            is_done = any(k in status_line for k in ["complete", "error", "failed", "cancel"]) and len(status_line) > 0
            is_busy = any(k in status_line for k in ["running", "queued", "saving", "starting"]) or not status_line

            if is_busy or not is_done:
                wait_t = random.uniform(20, 40)
                raw_status = res.stdout.strip() or res.stderr.strip() or "Empty/API buffering"
                logger.info(f"⏳ Kaggle GPU busy (Status: {raw_status}). Waiting {wait_t:.1f}s for queue slot...")
                time.sleep(wait_t)
            else:
                logger.success(f"✓ Kaggle GPU slot available (Status: {res.stdout.strip()})")
                return True

        logger.error(f"Timed out after {timeout_sec}s waiting for Kaggle GPU queue lock.")
        return False

    def create_kernel_script(self, segments: List[Dict[str, Any]], batch_uuid: str) -> str:
        """Generates the Python worker script to execute inside Kaggle with Dual-T4 multiprocessing."""
        payload = []
        for s in segments:
            is_vertical = str(s.get("aspect_ratio", "")).strip() in ("9:16", "vertical") or s.get("height", 0) > s.get("width", 0)
            # Native 1MP SDXL resolutions
            w = s.get("width", 768 if is_vertical else 1344)
            h = s.get("height", 1344 if is_vertical else 768)
            payload.append({
                "id": s["id"],
                "prompt": s["prompt"],
                "title": s.get("title", f"Segment {s['id']}"),
                "width": w,
                "height": h,
                "aspect_ratio": "9:16" if is_vertical else "16:9"
            })
        payload_json = json.dumps(payload, indent=2)

        script = f'''# Auto-generated Kaggle GPU Frame Generator (Dual-T4 Optimized)
import os
import sys
import time
import json
import torch
import torch.multiprocessing as mp

BATCH_UUID = "{batch_uuid}"
print(f"[KaggleWorker] Booting Python on GPU | BATCH_UUID: {{BATCH_UUID}}", flush=True)

num_gpus = torch.cuda.device_count()
print(f"[KaggleWorker] CUDA Available: {{torch.cuda.is_available()}} | Device Count: {{num_gpus}}", flush=True)
for i in range(num_gpus):
    print(f"  --> GPU {{i}}: {{torch.cuda.get_device_name(i)}} ({{torch.cuda.get_device_properties(i).total_memory / 1e9:.1f}} GB VRAM)", flush=True)

# Install diffusers, accelerate & dependencies
os.system("pip install -q diffusers transformers accelerate safetensors")

from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

base_model = "stabilityai/stable-diffusion-xl-base-1.0"
repo_id = "ByteDance/SDXL-Lightning"
ckpt_file = "sdxl_lightning_8step_unet.safetensors"
NEGATIVE_PROMPT = "text, letters, words, numbers, digits, typography, watermark, logo, signage, banners, ticker symbols, displays with writing, labels, subtitles, signature, font, writing, cartoon, anime, 3d render, blurry, distorted, low quality"

out_dir = "/kaggle/working/frames"
os.makedirs(out_dir, exist_ok=True)

PAYLOAD = {payload_json}

def run_render_worker(device_id: int, items: list, output_folder: str):
    device_str = f"cuda:{{device_id}}"
    print(f"[Worker-{{device_id}}] Initializing SDXL-Lightning on {{device_str}} for {{len(items)}} plates...", flush=True)
    
    local_weights_dir = "/kaggle/input/sdxl-lightning-weights"
    local_ckpt = os.path.join(local_weights_dir, ckpt_file)
    if os.path.exists(local_ckpt):
        print(f"[Worker-{{device_id}}] Found local mounted weights at {{local_ckpt}}! Loading instantly from SSD...", flush=True)
        weights_path = local_ckpt
    else:
        print(f"[Worker-{{device_id}}] Local dataset weights not found at {{local_ckpt}}, downloading from HuggingFace {{repo_id}}/{{ckpt_file}}...", flush=True)
        weights_path = hf_hub_download(repo_id, ckpt_file)
    
    config = UNet2DConditionModel.load_config(base_model, subfolder="unet")
    unet = UNet2DConditionModel.from_config(config).to(device_str, torch.float16)
    unet.load_state_dict(load_file(weights_path, device=device_str))
    
    pipe = StableDiffusionXLPipeline.from_pretrained(
        base_model,
        unet=unet,
        torch_dtype=torch.float16,
        variant="fp16"
    ).to(device_str)
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")
    
    for item in items:
        seg_id = item["id"]
        prompt = item["prompt"]
        out_path = os.path.join(output_folder, f"segment_{{seg_id:02d}}.jpg")
        print(f"[Worker-{{device_id}}] Rendering Segment {{seg_id:02d}} ({{item['width']}}x{{item['height']}})...", flush=True)
        t0 = time.time()
        
        img = pipe(
            prompt=prompt,
            negative_prompt=NEGATIVE_PROMPT,
            num_inference_steps=8,
            guidance_scale=1.5,
            width=item["width"],
            height=item["height"]
        ).images[0]
        
        img.save(out_path, quality=95)
        print(f"[Worker-{{device_id}}] ✓ Saved segment_{{seg_id:02d}}.jpg in {{time.time() - t0:.2f}}s", flush=True)

if __name__ == "__main__":
    t_start = time.time()
    
    # Dual-T4 Parallel Execution
    if num_gpus >= 2 and len(PAYLOAD) > 1:
        print("[KaggleWorker] Distributing batch across 2x T4 GPUs via multiprocessing...", flush=True)
        ctx = mp.get_context("spawn")
        
        # Partition 50/50
        items_gpu0 = PAYLOAD[0::2]
        items_gpu1 = PAYLOAD[1::2]
        
        p0 = ctx.Process(target=run_render_worker, args=(0, items_gpu0, out_dir))
        p1 = ctx.Process(target=run_render_worker, args=(1, items_gpu1, out_dir))
        
        p0.start()
        p1.start()
        
        p0.join()
        p1.join()
    else:
        # Single GPU execution
        run_render_worker(0, PAYLOAD, out_dir)
        
    # Write BATCH_UUID verification file
    with open("/kaggle/working/batch_uuid.txt", "w") as f:
        f.write(BATCH_UUID.strip())
        
    print(f"[KaggleWorker] All {{len(PAYLOAD)}} bespoke plates completed in {{time.time() - t_start:.2f}}s! Batch UUID: {{BATCH_UUID}}", flush=True)
'''
        return script

    def dispatch(self, segments: List[Dict[str, Any]], batch_uuid: str) -> bool:
        """Acquires queue lock, prepares metadata, and pushes the kernel to Kaggle."""
        # 1. Wait for queue lock to prevent concurrent kernel abortions
        if not self.wait_for_queue_lock(timeout_sec=2700):
            return False

        logger.info(f"Preparing Kaggle GPU Kernel for {len(segments)} frames (Batch UUID: {batch_uuid})...")
        script_content = self.create_kernel_script(segments, batch_uuid=batch_uuid)
        
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
            "machine_shape": "NvidiaTeslaT4",
            "enable_tpu": "false",
            "enable_internet": "true",
            "dataset_sources": ["alexytcreative/sdxl-lightning-weights"],
            "competition_sources": [],
            "kernel_sources": []
        }
        
        with open(self.stage_dir / "kernel-metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        kaggle_bin = self._get_kaggle_cmd()
        logger.info(f"Pushing kernel '{self.username}/{self.kernel_slug}' to Kaggle Dual-T4 GPU...")
        
        for push_try in range(1, 4):
            res = subprocess.run([str(kaggle_bin), "kernels", "push", "-p", str(self.stage_dir)], capture_output=True, text=True)
            if res.returncode == 0:
                logger.info(f"✓ Kernel pushed successfully! Batch UUID: {batch_uuid}. Sleeping 25s for Kaggle status transition...")
                time.sleep(25)
                return True
            
            logger.warning(f"Kaggle push attempt {push_try}/3 notice: {res.stderr.strip() or res.stdout.strip()}. Backing off 30s...")
            time.sleep(30)
            self.wait_for_queue_lock(timeout_sec=300)

        logger.error(f"Kaggle push failed after 3 attempts: {res.stderr}")
        return False

    def generate_batch(self, prompts: List[Dict[str, Any]], aspect_ratio: str = "9:16", max_retries: int = 3) -> bool:
        """Dispatches a batch with unique BATCH_UUID, polls, and verifies before mapping output with auto-retries."""
        is_vert = aspect_ratio in ("9:16", "vertical")
        
        for attempt in range(1, max_retries + 1):
            batch_uuid = uuid.uuid4().hex[:8]
            segments = []
            for idx, p in enumerate(prompts, 1):
                segments.append({
                    "id": idx,
                    "prompt": p.get("prompt", ""),
                    "title": f"Frame {idx}",
                    "aspect_ratio": "9:16" if is_vert else "16:9",
                    "width": 768 if is_vert else 1344,
                    "height": 1344 if is_vert else 768,
                })

            logger.info(f"🚀 [Kaggle Batch Attempt {attempt}/{max_retries}] Dispatching {len(segments)} frames with UUID: {batch_uuid}")
            if not self.dispatch(segments, batch_uuid=batch_uuid):
                logger.warning(f"Dispatch attempt {attempt} failed to acquire lock or push. Retrying in 15s...")
                time.sleep(15)
                continue

            # Isolated directory per batch UUID
            out_dest = Path(f"/tmp/kaggle_downloaded_frames_{batch_uuid}")
            if out_dest.exists():
                shutil.rmtree(out_dest, ignore_errors=True)
            out_dest.mkdir(parents=True, exist_ok=True)

            if self.poll_and_download(out_dest, batch_uuid=batch_uuid, timeout_sec=600):
                mapped_count = 0
                for idx, p in enumerate(prompts, 1):
                    candidates = [
                        out_dest / "frames" / f"segment_{idx:02d}.jpg",
                        out_dest / "frames" / f"segment_{idx}.jpg",
                        out_dest / f"segment_{idx:02d}.jpg",
                        out_dest / f"segment_{idx}.jpg",
                    ]
                    downloaded = next((c for c in candidates if c.exists()), None)
                    if downloaded and "output_path" in p:
                        target_p = Path(p["output_path"])
                        target_p.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(downloaded, target_p)
                        mapped_count += 1
                if mapped_count == len(prompts):
                    logger.success(f"✓ Successfully mapped {mapped_count}/{len(prompts)} frames from Batch {batch_uuid}")
                    return True
                else:
                    logger.warning(f"Only {mapped_count}/{len(prompts)} mapped. Retrying batch in 15s...")
            else:
                logger.warning(f"Batch {batch_uuid} failed download/UUID check. Retrying in 15s...")
            
            time.sleep(15)

        return False

    def poll_and_download(self, dest_dir: Path, batch_uuid: str, timeout_sec: int = 900) -> bool:
        """Polls Kaggle status until complete, downloads frames, and verifies BATCH_UUID."""
        kaggle_bin = self._get_kaggle_cmd()
        ref = f"{self.username}/{self.kernel_slug}"
        start_time = time.time()
        has_seen_active = False

        while time.time() - start_time < timeout_sec:
            time.sleep(15)
            res = subprocess.run([str(kaggle_bin), "kernels", "status", ref], capture_output=True, text=True)
            status_line = res.stdout.strip()
            logger.info(f"[Kaggle Status] {status_line}")

            if any(k in status_line.lower() for k in ["running", "queued", "starting", "saving"]):
                has_seen_active = True

            if "complete" in status_line.lower():
                logger.info(f"Kaggle run completed! Downloading artifacts to {dest_dir}...")
                out_res = subprocess.run([str(kaggle_bin), "kernels", "output", ref, "-p", str(dest_dir)], capture_output=True, text=True)
                if out_res.returncode == 0:
                    uuid_candidates = [
                        dest_dir / "batch_uuid.txt",
                        dest_dir / "frames" / "batch_uuid.txt",
                    ]
                    uuid_file = next((u for u in uuid_candidates if u.exists()), None)
                    if uuid_file:
                        downloaded_uuid = uuid_file.read_text().strip()
                        if downloaded_uuid == batch_uuid:
                            logger.success(f"🎯 [UUID Match Verified] Downloaded frames match target Batch UUID: {batch_uuid}")
                            return True
                        else:
                            if not has_seen_active:
                                logger.warning(f"⚠️ Stale output from previous batch (got {downloaded_uuid}, expected {batch_uuid}). Kaggle has not transitioned to queued/running yet. Waiting...")
                            else:
                                logger.warning(f"⚠️ Batch UUID mismatch: Expected {batch_uuid}, got {downloaded_uuid}. Waiting for CDN artifact refresh...")
                            time.sleep(15)
                            continue
                    else:
                        logger.warning(f"⚠️ batch_uuid.txt not found in download. Retrying output pull in 15s...")
                        time.sleep(15)
                        continue
                else:
                    logger.error(f"Failed to download outputs: {out_res.stderr}")
                    return False
            elif any(k in status_line.lower() for k in ["error", "failed", "cancel"]):
                logger.error(f"Kaggle kernel reported error: {status_line}")
                return False

        logger.error(f"Timed out waiting for Kaggle GPU kernel batch {batch_uuid}.")
        return False
