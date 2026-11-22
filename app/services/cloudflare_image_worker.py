#!/usr/bin/env python3
"""
The Bull Print — Cloudflare Serverless GPU Frame Generation Worker (app/services/cloudflare_image_worker.py)

Generates 100% bespoke photographic plates at lightning speed using Cloudflare Workers AI.
Runs FLUX.1-schnell / SDXL on Cloudflare serverless GPUs via:
https://tbp-cloudflare-orchestrator.cloudflare-orchestrator.workers.dev/generate-plate

Zero local GPU usage, 100% cloud execution, concurrent parallel batch rendering.
"""

from __future__ import annotations

import io
import json
import os
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional
from loguru import logger
from PIL import Image, ImageOps

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DEFAULT_WORKER_URL = os.getenv(
    "CLOUDFLARE_WORKER_URL",
    "https://tbp-cloudflare-orchestrator.cloudflare-orchestrator.workers.dev"
)


class CloudflareImageWorker:
    """Automated Cloudflare Workers AI runner for lightning-fast batch image generation."""

    def __init__(self, worker_url: Optional[str] = None):
        self.worker_url = (worker_url or DEFAULT_WORKER_URL).rstrip("/")
        self.endpoint = f"{self.worker_url}/generate-plate"

    def generate_single_plate(
        self,
        prompt: str,
        width: int = 1080,
        height: int = 1920,
        out_path: Optional[Path] = None,
        max_retries: int = 3
    ) -> Optional[Image.Image]:
        """
        Generates a single photographic plate via Cloudflare Workers AI,
        crops/fits to exact target dimensions with Lanczos resampling, and saves to out_path.
        """
        clean_prompt = prompt.replace("clean plate", "").replace("zero text", "").replace("zero watermark", "").strip()

        payload = json.dumps({
            "prompt": clean_prompt,
            "model": "@cf/black-forest-labs/flux-1-schnell"
        }).encode("utf-8")

        for attempt in range(1, max_retries + 1):
            try:
                req = urllib.request.Request(
                    self.endpoint,
                    data=payload,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "TheBullPrint-CloudImageWorker/1.0"
                    }
                )
                start_t = time.time()
                with urllib.request.urlopen(req, timeout=60) as resp:
                    if resp.status == 200:
                        img_bytes = resp.read()
                        raw_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                        fitted_img = ImageOps.fit(
                            raw_img,
                            (width, height),
                            method=Image.Resampling.LANCZOS,
                            centering=(0.5, 0.5)
                        )
                        if out_path:
                            out_p = Path(out_path)
                            out_p.parent.mkdir(parents=True, exist_ok=True)
                            fitted_img.save(out_p, quality=95)
                            logger.success(f"⚡ [Cloudflare Plate] Saved {out_p.name} ({width}x{height}, {time.time()-start_t:.2f}s)")
                        return fitted_img
                    else:
                        logger.warning(f"⚠️ [Cloudflare Plate] Status {resp.status} on attempt {attempt}")
            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="ignore")
                logger.warning(f"⚠️ [Cloudflare Plate] HTTP {e.code} on attempt {attempt}: {err_body[:200]}")
                if e.code in (404, 401, 403):
                    return None
            except Exception as e:
                logger.warning(f"⚠️ [Cloudflare Plate] Error on attempt {attempt}: {e}")

            if attempt < max_retries:
                time.sleep(2 * attempt)

        return None

    def generate_batch(
        self,
        prompts: List[Dict[str, str]],
        aspect_ratio: str = "9:16",
        max_workers: int = 5
    ) -> bool:
        """
        Generates a batch of photographic plates concurrently on Cloudflare Workers AI.
        prompts: list of dicts with keys: 'prompt' and 'output_path'
        aspect_ratio: '9:16' (1080x1920) or '16:9' (1920x1080)
        """
        if not prompts:
            logger.info("ℹ️ [Cloudflare Batch] No prompts provided.")
            return True

        if aspect_ratio == "9:16":
            w, h = 1080, 1920
        else:
            w, h = 1920, 1080

        total = len(prompts)
        logger.info(f"🚀 [Cloudflare Batch] Generating {total} plates ({aspect_ratio}, {w}x{h}) across Cloudflare serverless GPUs...")

        start_all = time.time()
        success_count = 0
        failed_prompts = []

        def _worker(item: Dict[str, str]) -> bool:
            p_text = item.get("prompt", "")
            out_p = Path(item.get("output_path", ""))
            img = self.generate_single_plate(prompt=p_text, width=w, height=h, out_path=out_p)
            return img is not None and out_p.exists()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_item = {executor.submit(_worker, item): item for item in prompts}
            for future in as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    ok = future.result()
                    if ok:
                        success_count += 1
                    else:
                        failed_prompts.append(item)
                except Exception as exc:
                    logger.error(f"❌ [Cloudflare Batch] Worker exception: {exc}")
                    failed_prompts.append(item)

        elapsed = time.time() - start_all
        logger.info(f"🏁 [Cloudflare Batch] Completed {success_count}/{total} plates in {elapsed:.1f}s ({elapsed/max(1,total):.2f}s/frame)")

        if failed_prompts:
            logger.warning(f"⚠️ [Cloudflare Batch] {len(failed_prompts)} plates failed.")
            return False

        return True
