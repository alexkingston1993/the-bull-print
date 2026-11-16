#!/usr/bin/env python3
"""
The Bull Print — Publish Deferred Artifacts (scripts/publish_deferred_artifacts.py)

Designed for 1:35 PM IST execution (following Pacific Time YouTube API quota reset).
1. Finds today's completed runs of parallel_video_matrix.yml.
2. Downloads master-broadcast-* artifacts into /tmp/deferred_publish/<run_id>/.
3. Reads upload_manifest.json, generates fresh 2-hour staggered publishAt timestamps.
4. Uploads all 12 master videos + thumbnails across Slot 1 & Slot 2 with full metadata.
"""

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

def get_gh_cmd() -> str:
    for candidate in ["/usr/local/bin/gh", "/opt/homebrew/bin/gh", "/usr/bin/gh"]:
        if os.path.exists(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return shutil.which("gh") or "gh"

def publish_deferred_artifacts(dry_run: bool = False):
    gh_bin = get_gh_cmd()
    ist_tz = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(timezone.utc).astimezone(ist_tz)
    today_ist = now_ist.strftime("%Y-%m-%d")

    logger.info(f"🚀 [Deferred Publish] Checking completed matrix workflows for {today_ist} (IST)...")

    # 1. Fetch runs from GitHub Actions
    res = subprocess.run(
        [gh_bin, "run", "list", "--workflow=parallel_video_matrix.yml", "--limit", "40", "--json", "databaseId,conclusion,createdAt,status"],
        capture_output=True, text=True
    )
    if res.returncode != 0:
        logger.error(f"Failed to query gh runs: {res.stderr}")
        return

    try:
        runs = json.loads(res.stdout.strip())
    except Exception as e:
        logger.error(f"Failed to parse gh output as JSON: {e} | Raw: {res.stdout[:100]}")
        return
    today_runs = []
    for r in runs:
        c_at = r.get("createdAt")
        if c_at:
            run_date = datetime.fromisoformat(c_at.replace("Z", "+00:00")).astimezone(ist_tz).strftime("%Y-%m-%d")
            if run_date == today_ist and r.get("conclusion") == "success":
                today_runs.append(r)

    logger.info(f"Found {len(today_runs)} successful matrix workflow runs from today.")
    if not today_runs:
        logger.warning("No runs found from today. Checking previous 24 hours...")
        for r in runs[:15]:
            if r.get("conclusion") == "success":
                today_runs.append(r)

    today_runs = today_runs[:12]
    # Reverse so earliest run is slot 0
    today_runs = list(reversed(today_runs))
    logger.info(f"Targeting {len(today_runs)} video artifacts for publishing.")

    download_base = Path("/tmp/deferred_publish")
    download_base.mkdir(parents=True, exist_ok=True)

    from app.services.youtube_uploader import get_uploader
    uploader = get_uploader()

    base_publish_time = datetime.now(timezone.utc) + timedelta(hours=1)
    published_count = 0
    seen_topics = []

    for idx, run_item in enumerate(today_runs):
        run_id = str(run_item["databaseId"])
        run_dir = download_base / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"\n[{idx+1}/{len(today_runs)}] 📥 Processing Run #{run_id}...")

        # Download artifact
        dl_res = subprocess.run(
            [gh_bin, "run", "download", run_id, "--dir", str(run_dir)],
            capture_output=True, text=True
        )
        if dl_res.returncode != 0:
            logger.warning(f"Could not download artifacts for run #{run_id}: {dl_res.stderr}")

        # Locate upload_manifest.json
        manifest_files = list(run_dir.glob("**/upload_manifest.json"))
        if not manifest_files:
            logger.error(f"No upload_manifest.json found in run #{run_id} artifacts.")
            continue

        manifest_path = manifest_files[0]
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        artifact_dir = manifest_path.parent
        mp4_files = list(artifact_dir.glob("*.mp4"))
        if not mp4_files:
            logger.error(f"No master MP4 found in {artifact_dir}")
            continue
        master_mp4 = mp4_files[0]

        thumb_files = list(artifact_dir.glob("*.jpg")) + list(artifact_dir.glob("*.png"))
        thumb_path = thumb_files[0] if thumb_files else None

        title = manifest.get("title", "The Bull Print Episode")
        desc = manifest.get("description", "")
        tags = manifest.get("tags", ["the bull print", "finance", "investing"])
        is_short = manifest.get("is_short", True)

        # 1. Title typo sanitization
        if "October 2027" in title:
            title = title.replace("October 2027", "2026/2027")

        # 2. Intra-batch topic deduplication (e.g. Polymarket $1.8B Short vs Doc)
        import re
        words = set(re.findall(r"\b[a-zA-Z0-9]{3,}\b", title.lower())) - {"the", "and", "why", "how", "what", "for", "with", "into", "new"}
        is_duplicate = False
        for seen in seen_topics:
            overlap = len(words & seen["words"])
            if len(words) > 0 and (overlap / len(words)) >= 0.5:
                # If current is Short and an earlier was Doc (or vice versa), keep the high-production Doc
                if is_short and not seen["is_short"]:
                    logger.warning(f"⚠️ [Batch Deduplicator] Suppressing duplicate Short '{title}' in favor of 16:9 Documentary '{seen['title']}'.")
                    is_duplicate = True
                    break
                elif not is_short and seen["is_short"]:
                    logger.warning(f"⚠️ [Batch Deduplicator] Found 16:9 Documentary '{title}' which supersedes Short '{seen['title']}'.")

        if is_duplicate:
            continue

        seen_topics.append({"title": title, "words": words, "is_short": is_short})

        # Fresh 2-hour staggered timestamp using published_count to avoid gaps
        staggered_time = (base_publish_time + timedelta(hours=published_count * 2)).strftime("%Y-%m-%dT%H:%M:%SZ")

        logger.info(f"🎬 Video: '{title}'")
        logger.info(f"   Format: {'Short 9:16' if is_short else 'Doc 16:9'} | Scheduled: {staggered_time} UTC")
        logger.info(f"   MP4: {master_mp4.name} ({master_mp4.stat().st_size / 1e6:.1f} MB)")

        if dry_run:
            logger.info(f"   [DRY RUN] Would upload to YouTube across OAuth pool.")
            published_count += 1
            continue

        try:
            res = uploader.upload_video(
                language="en",
                video_path=str(master_mp4),
                title=title,
                description=desc,
                tags=tags,
                thumbnail_path=str(thumb_path) if thumb_path else None,
                category_id="27",
                privacy_status="private",
                publish_at=staggered_time,
                is_short=is_short,
                force_upload=True,
            )
            vid_id = (res.get("video_id") or res.get("id")) if isinstance(res, dict) else None
            if vid_id:
                published_count += 1
                logger.success(f"✓ [{published_count}/{len(today_runs)}] Uploaded successfully: https://youtu.be/{vid_id}")
            else:
                logger.error(f"Upload failed for run #{run_id}: {res}")
        except Exception as e:
            logger.error(f"Exception during upload for run #{run_id}: {e}")

        time.sleep(5)

    logger.success(f"\n🎉 [Publish Complete] Successfully published {published_count}/{len(today_runs)} deferred videos!")

if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    publish_deferred_artifacts(dry_run=dry)
