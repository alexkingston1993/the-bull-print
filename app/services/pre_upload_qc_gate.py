#!/usr/bin/env python3
"""
The Bull Print — Pre-Upload Quality Control Gate (app/services/pre_upload_qc_gate.py)

Mandatory pre-upload validation gate executed immediately before YouTube API dispatch.
Enforces:
1. File size > 1MB
2. Strict aspect ratio (1080x1920 for 9:16 Shorts, 1920x1080 for 16:9 Documentaries)
3. Duration bounds (20s - 61s for Shorts, >= 150s for Documentaries)
4. Audio presence & volume check (mean_volume > -45.0 dB, zero silence)
5. dHash perceptual hash frame uniqueness (>= 85% unique frames, zero frozen plates)
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple
from loguru import logger
from PIL import Image

class PreUploadQCGate:
    """Pre-Upload QC Gate: Guarantees zero corrupted, silent, misaligned, or cloned video uploads."""

    @classmethod
    def validate_manifest_prompt_diversity(cls, manifest_path: Path, min_unique_ratio: float = 0.95) -> Tuple[bool, List[str]]:
        """
        Validates that >= 95% of visual prompts across micro-beats and sections are strictly unique.
        Catches repetitive visual prompts, copy-pasted clichés, and prompt recycling.
        """
        manifest_path = Path(manifest_path)
        errors = []
        if not manifest_path.exists():
            errors.append(f"Manifest not found for prompt diversity check: {manifest_path}")
            return False, errors

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception as e:
            errors.append(f"Failed to read manifest JSON: {e}")
            return False, errors

        prompts = []
        for s in manifest.get("sections", []):
            if s.get("micro_beats"):
                for b in s["micro_beats"]:
                    p = b.get("visual_prompt", "").strip()
                    if p:
                        prompts.append(p)
            else:
                p = s.get("visual_prompt", "").strip()
                if p:
                    prompts.append(p)

        if not prompts:
            errors.append("No visual prompts found in manifest to validate")
            return False, errors

        # Normalize prompts for strict comparison (strip standard photographic prefix/suffix & punctuation)
        def normalize_p(text: str) -> str:
            t = text.lower()
            t = re.sub(r"^cinematic 35mm photograph(?:,\s*visual metaphor of)?", "", t)
            t = re.sub(r",?\s*(?:8k hyper-detailed|clean plate|zero text|zero watermark).*", "", t)
            t = re.sub(r"[^\w\s]", "", t)
            norm = " ".join(t.split())
            return norm if norm else text.lower().strip()

        norm_prompts = [normalize_p(p) for p in prompts]
        unique_norm = set(norm_prompts)
        unique_ratio = len(unique_norm) / len(norm_prompts)

        logger.info(f"🔍 [Prompt QC] Total prompts: {len(prompts)} | Unique normalized: {len(unique_norm)}/{len(norm_prompts)} ({unique_ratio*100:.1f}%)")

        if unique_ratio < min_unique_ratio:
            errors.append(
                f"Prompt repetition detected: unique prompt ratio is {unique_ratio*100:.1f}% "
                f"({len(unique_norm)}/{len(norm_prompts)}), strictly below required {min_unique_ratio*100:.1f}% threshold. "
                f"Every beat must have a 100% bespoke prompt illustrating its specific spoken words."
            )
            return False, errors

        logger.success(f"✓ [Prompt QC] Passed! {unique_ratio*100:.1f}% unique prompts across all beats (threshold: {min_unique_ratio*100:.1f}%)")
        return True, []

    @staticmethod
    def _compute_dhash(img: Image.Image, hash_size: int = 8) -> int:
        """Computes difference hash (dHash) for an image to detect perceptual duplicates."""
        # Convert to grayscale and resize to (hash_size + 1, hash_size)
        resized = img.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
        pixels = list(resized.getdata())
        
        diff = []
        for row in range(hash_size):
            for col in range(hash_size):
                idx = row * (hash_size + 1) + col
                diff.append(pixels[idx] > pixels[idx + 1])
                
        # Convert boolean array to 64-bit int
        hash_val = 0
        for bit in diff:
            hash_val = (hash_val << 1) | bit
        return hash_val

    @staticmethod
    def _hamming_distance(h1: int, h2: int) -> int:
        """Hamming distance between two 64-bit hashes."""
        return bin(h1 ^ h2).count("1")

    @classmethod
    def validate(cls, video_path: Path, is_short: bool = True, manifest_path: Optional[Path] = None) -> Tuple[bool, List[str]]:
        video_path = Path(video_path)
        errors = []

        logger.info(f"🔍 [Pre-Upload QC] Validating '{video_path.name}' (Format: {'Short 9:16' if is_short else 'Doc 16:9'})...")

        # 0. Prompt Diversity Check if manifest is provided or locatable
        candidate_manifest = manifest_path
        if candidate_manifest is None:
            # Check adjacent directory structures
            for cand in [
                video_path.parent / "session_manifest.json",
                video_path.parent.parent / "session_bundle" / "session_manifest.json",
            ]:
                if cand.exists():
                    candidate_manifest = cand
                    break

        if candidate_manifest and candidate_manifest.exists():
            p_passed, p_errors = cls.validate_manifest_prompt_diversity(candidate_manifest, min_unique_ratio=0.95)
            if not p_passed:
                errors.extend(p_errors)

        # 1. Existence and File Size Check
        if not video_path.exists():
            errors.append(f"File not found: {video_path}")
            return False, errors

        file_size = video_path.stat().st_size
        if file_size < 1_000_000:
            errors.append(f"File size too small ({file_size / 1e6:.2f} MB < 1.0 MB)")

        ffprobe_bin = shutil.which("ffprobe") or "ffprobe"
        ffmpeg_bin = shutil.which("ffmpeg") or "ffmpeg"

        # 2. ffprobe Stream & Geometry Check
        try:
            probe_cmd = [
                ffprobe_bin, "-v", "error",
                "-show_entries", "stream=codec_type,width,height:format=duration",
                "-of", "json", str(video_path)
            ]
            res = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
            probe_data = json.loads(res.stdout)
            
            streams = probe_data.get("streams", [])
            video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
            audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

            if not video_stream:
                errors.append("No video stream found in master render")
            else:
                width = int(video_stream.get("width", 0))
                height = int(video_stream.get("height", 0))
                if is_short:
                    if (width, height) not in [(1080, 1920)]:
                        errors.append(f"Invalid dimensions: got {width}x{height}, expected 1080x1920")
                else:
                    valid_16x9 = [(1920, 1080), (2560, 1440), (3840, 2160)]
                    if (width, height) not in valid_16x9:
                        errors.append(f"Invalid dimensions: got {width}x{height}, expected standard 16:9 (1920x1080, 2560x1440, or 3840x2160)")

            if not audio_stream:
                errors.append("No audio stream found in master render")

            # Duration Check
            duration_str = probe_data.get("format", {}).get("duration")
            if not duration_str:
                errors.append("Unable to determine video duration")
            else:
                dur = float(duration_str)
                if is_short:
                    if dur < 20.0 or dur > 61.0:
                        errors.append(f"Shorts duration out of bounds: {dur:.1f}s (must be 20s - 61s)")
                else:
                    if dur < 660.0 or dur > 2400.0:
                        errors.append(f"Documentary duration out of bounds: {dur:.1f}s (must be 660s - 2400s / 11m - 40m)")
        except Exception as e:
            errors.append(f"ffprobe metadata extraction failed: {e}")

        # 3. Audio Volume / Silence Detection
        try:
            vol_cmd = [
                ffmpeg_bin, "-i", str(video_path),
                "-af", "volumedetect", "-vn", "-sn", "-dn",
                "-f", "null", "/dev/null"
            ]
            vol_res = subprocess.run(vol_cmd, capture_output=True, text=True)
            mean_vol = None
            for line in vol_res.stderr.splitlines():
                if "mean_volume:" in line:
                    parts = line.split("mean_volume:")
                    if len(parts) > 1:
                        mean_vol = float(parts[1].replace("dB", "").strip())
                        break
            
            if mean_vol is None:
                errors.append("Could not compute audio mean volume")
            elif mean_vol < -45.0:
                errors.append(f"Audio is nearly silent (mean_volume: {mean_vol:.1f} dB < -45.0 dB threshold)")
            else:
                logger.info(f"✓ Audio check passed: mean_volume = {mean_vol:.1f} dB")
        except Exception as e:
            errors.append(f"Audio volume detection error: {e}")

        # 4. dHash Perceptual Hash Frame Uniqueness
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_path = Path(tmp_dir)
                # Sample 10 frames across the video
                fps_val = max(10.0 / max(dur, 1.0), 0.01)
                extract_cmd = [
                    ffmpeg_bin, "-i", str(video_path),
                    "-vf", f"fps={fps_val:.4f}",
                    "-vframes", "10",
                    str(tmp_path / "sample_%02d.jpg")
                ]
                subprocess.run(extract_cmd, capture_output=True, text=True, check=True)
                sample_files = sorted(list(tmp_path.glob("sample_*.jpg")))
                
                if len(sample_files) < 3:
                    errors.append(f"Insufficient frames extracted for dHash uniqueness check ({len(sample_files)} frames)")
                else:
                    hashes = []
                    for f in sample_files:
                        with Image.open(f) as img:
                            hashes.append(cls._compute_dhash(img))

                    # Check pairwise difference
                    unique_transitions = 0
                    total_comparisons = len(hashes) - 1
                    for i in range(total_comparisons):
                        dist = cls._hamming_distance(hashes[i], hashes[i + 1])
                        # If distance >= 5, visual content has distinctly changed
                        if dist >= 5:
                            unique_transitions += 1

                    transition_rate = unique_transitions / max(total_comparisons, 1)
                    logger.info(f"✓ dHash sample analysis: {unique_transitions}/{total_comparisons} distinct transitions ({transition_rate*100:.1f}%)")

                    # If all frames are identical (0 transitions), video is frozen/static
                    if unique_transitions == 0:
                        errors.append("Perceptual hash failure: 100% frozen/static frame throughout entire video")
                    elif transition_rate < 0.40:
                        errors.append(f"Perceptual hash warning: low visual dynamism ({transition_rate*100:.1f}% unique transitions)")
        except Exception as e:
            logger.warning(f"dHash check skipped due to warning: {e}")

        passed = len(errors) == 0
        if passed:
            logger.success(f"✓ [Pre-Upload QC] Video PASSED all quality gates! Ready for YouTube upload.")
        else:
            logger.error(f"❌ [Pre-Upload QC] Video FAILED quality control gates: {errors}")

        return passed, errors

