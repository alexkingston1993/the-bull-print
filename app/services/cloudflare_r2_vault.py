#!/usr/bin/env python3
"""
app/services/cloudflare_r2_vault.py

The Bull Print — Cloudflare D1 & R2 Frame Vault Engine
Features:
- D1 SQLite Serverless Ledger: Tracks video & frame metadata, seeds, visual prompts, and privacy states.
- Reversible Public <-> Private Lifecycle:
  * Public only in active R2: Only active public YouTube videos hold frames in R2.
  * Instant R2 Purge on Private/Unlisted/Deleted: Drops storage to 0 bytes when a video is privatized.
  * Auto-Recovery on Private -> Public: Restores frames when a video is re-published.
- Strict 180-Day (6-Month) Cooldown on Frame Reuse:
  * created_at_epoch <= now - 15,552,000 (180 days) AND last_used_epoch <= now - 15,552,000 AND privacy_status == 'public'.
  * YouTube perceptual hash-busting transforms (inverted pan direction + 1.04x crop offset + fresh grain seed).
"""

import os
import sys
import json
import time
import zipfile
import argparse
import requests
from pathlib import Path
from typing import Optional, Dict, Any, List

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Cloudflare Configuration
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "e91af5ac8ece067368d52e201025a370")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
D1_DATABASE_ID = os.getenv("CLOUDFLARE_D1_DATABASE_ID", "f54ea399-d524-45d9-8974-bf4edfb4741a")
R2_BUCKET_NAME = os.getenv("CLOUDFLARE_R2_BUCKET", "tbp-frame-vault")
VAULT_COOLDOWN_SECONDS = 180 * 86400  # 180 days (6 months) in seconds = 15,552,000s


class CloudflareD1Client:
    """Interacts with Cloudflare D1 SQLite database via Cloudflare REST API."""

    def __init__(self, account_id: str = CLOUDFLARE_ACCOUNT_ID, api_token: str = CLOUDFLARE_API_TOKEN, database_id: str = D1_DATABASE_ID):
        self.account_id = account_id
        self.api_token = api_token
        self.database_id = database_id
        self.endpoint = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/d1/database/{self.database_id}/query"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def execute_query(self, sql: str, params: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
        payload: Dict[str, Any] = {"sql": sql}
        if params:
            payload["params"] = params

        try:
            resp = requests.post(self.endpoint, headers=self.headers, json=payload, timeout=15)
            data = resp.json()
            if not data.get("success"):
                errors = data.get("errors", [])
                print(f"⚠️ [D1 Query Warning] Errors: {errors}")
                return []
            result = data.get("result", [])
            if result and isinstance(result, list) and len(result) > 0:
                return result[0].get("results", [])
            return []
        except Exception as e:
            print(f"⚠️ [D1 Connection Notice] {e}")
            return []

    def index_video(
        self,
        video_id: str,
        title: str,
        privacy_status: str,
        total_frames: int,
        cut_timestamps_json: str,
        frames_meta: List[Dict[str, Any]],
        cold_backup_url: Optional[str] = None
    ) -> bool:
        now = int(time.time())
        r2_prefix = f"public/{video_id}/" if privacy_status == "public" else f"staging/{video_id}/"

        # 1. Upsert video record
        v_sql = """
        INSERT INTO videos (video_id, title, privacy_status, r2_prefix, total_frames, created_at_epoch, last_checked_epoch, cold_backup_url, cut_timestamps_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(video_id) DO UPDATE SET
            privacy_status = excluded.privacy_status,
            r2_prefix = excluded.r2_prefix,
            last_checked_epoch = excluded.last_checked_epoch,
            cold_backup_url = COALESCE(excluded.cold_backup_url, videos.cold_backup_url);
        """
        self.execute_query(v_sql, [
            video_id, title, privacy_status, r2_prefix, total_frames, now, now, cold_backup_url, cut_timestamps_json
        ])

        # 2. Upsert frame records
        for f_meta in frames_meta:
            f_idx = f_meta.get("frame_index", 0)
            frame_id = f"{video_id}_frame_{f_idx:02d}"
            r2_key = f"{r2_prefix}frame_{f_idx:02d}.jpg"
            prompt = f_meta.get("visual_prompt", "")
            seed = f_meta.get("seed", 0)

            f_sql = """
            INSERT INTO frames (frame_id, video_id, frame_index, r2_key, privacy_status, visual_prompt, seed, created_at_epoch, last_used_epoch, is_vault_eligible)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            ON CONFLICT(frame_id) DO UPDATE SET
                privacy_status = excluded.privacy_status,
                r2_key = excluded.r2_key;
            """
            self.execute_query(f_sql, [
                frame_id, video_id, f_idx, r2_key, privacy_status, prompt, seed, now, now
            ])

        print(f"✅ [D1 Ledger] Indexed video {video_id} ('{title}', {privacy_status}) with {len(frames_meta)} frames.")
        return True

    def get_indexed_videos(self) -> List[Dict[str, Any]]:
        sql = "SELECT video_id, title, privacy_status, r2_prefix, total_frames, created_at_epoch, cold_backup_url FROM videos;"
        return self.execute_query(sql)

    def update_video_status(self, video_id: str, new_status: str) -> None:
        now = int(time.time())
        cutoff = now - VAULT_COOLDOWN_SECONDS

        v_sql = "UPDATE videos SET privacy_status = ?, last_checked_epoch = ? WHERE video_id = ?;"
        self.execute_query(v_sql, [new_status, now, video_id])

        if new_status == "public":
            # Check 180-day age gate for vault eligibility
            f_sql = """
            UPDATE frames 
            SET privacy_status = 'public',
                is_vault_eligible = CASE WHEN created_at_epoch <= ? THEN 1 ELSE 0 END
            WHERE video_id = ?;
            """
            self.execute_query(f_sql, [cutoff, video_id])
        else:
            # Drop from vault if private, unlisted, or deleted
            f_sql = "UPDATE frames SET privacy_status = ?, is_vault_eligible = 0 WHERE video_id = ?;"
            self.execute_query(f_sql, [new_status, video_id])

    def get_vault_eligible_frames(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        STRICT 180-DAY (6-MONTH) VAULT REUSE GATE:
        Only returns frames that are:
        1. Currently 'public' on YouTube
        2. Created at least 180 days ago (created_at <= now - 15,552,000s)
        3. Last used at least 180 days ago (last_used <= now - 15,552,000s)
        """
        now = int(time.time())
        cutoff = now - VAULT_COOLDOWN_SECONDS

        sql = """
        SELECT frame_id, video_id, frame_index, r2_key, visual_prompt, seed, created_at_epoch, last_used_epoch
        FROM frames
        WHERE privacy_status = 'public'
          AND created_at_epoch <= ?
          AND last_used_epoch <= ?
        ORDER BY last_used_epoch ASC
        LIMIT ?;
        """
        return self.execute_query(sql, [cutoff, cutoff, limit])

    def mark_frame_reused(self, frame_id: str) -> None:
        """Updates last_used_epoch to now when a frame is reused after its 180-day cooldown."""
        now = int(time.time())
        sql = "UPDATE frames SET last_used_epoch = ?, is_vault_eligible = 0 WHERE frame_id = ?;"
        self.execute_query(sql, [now, frame_id])


class CloudflareR2Client:
    """Interacts with Cloudflare R2 object storage with fallback to cold local/release storage."""

    def __init__(self, account_id: str = CLOUDFLARE_ACCOUNT_ID, api_token: str = CLOUDFLARE_API_TOKEN, bucket_name: str = R2_BUCKET_NAME):
        self.account_id = account_id
        self.api_token = api_token
        self.bucket_name = bucket_name
        self.s3_endpoint = f"https://{self.account_id}.r2.cloudflarestorage.com"
        self._s3_client = None

    def _get_s3(self):
        if self._s3_client is not None:
            return self._s3_client

        ak = os.getenv("R2_ACCESS_KEY_ID")
        sk = os.getenv("R2_SECRET_ACCESS_KEY")
        if ak and sk:
            try:
                import boto3
                self._s3_client = boto3.client(
                    "s3",
                    endpoint_url=self.s3_endpoint,
                    aws_access_key_id=ak,
                    aws_secret_access_key=sk,
                    region_name="auto"
                )
                return self._s3_client
            except Exception as e:
                print(f"⚠️ [R2 Boto3 Init Notice] {e}")

        return None

    def upload_public_frames(self, video_id: str, frame_paths: List[Path]) -> str:
        """
        Uploads or archives clean .jpg frames when a video goes public.
        Also creates a cold .zip backup to enable lossless Private -> Public recovery.
        """
        prefix = f"public/{video_id}/"
        s3 = self._get_s3()

        # Create cold backup .zip in local cold vault
        cold_dir = BASE_DIR / "state" / "cold_vault"
        cold_dir.mkdir(parents=True, exist_ok=True)
        zip_path = cold_dir / f"{video_id}_frames_backup.zip"

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in frame_paths:
                if p.exists():
                    zf.write(p, arcname=p.name)

        if s3:
            try:
                for p in frame_paths:
                    if p.exists():
                        key = f"{prefix}{p.name}"
                        s3.upload_file(str(p), self.bucket_name, key, ExtraArgs={"ContentType": "image/jpeg"})
                print(f"✅ [R2 Storage] Uploaded {len(frame_paths)} frames to r2://{self.bucket_name}/{prefix}")
            except Exception as e:
                print(f"⚠️ [R2 Upload Notice] {e}. Stored in cold archive: {zip_path.name}")
        else:
            print(f"ℹ️ [Cold Vault] Archived {len(frame_paths)} frames for {video_id} in {zip_path.name}")

        return str(zip_path)

    def purge_frames_for_video(self, video_id: str) -> int:
        """Immediately purges all .jpg objects for a private/unlisted/deleted video from R2."""
        prefix = f"public/{video_id}/"
        s3 = self._get_s3()
        purged_count = 0

        if s3:
            try:
                resp = s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
                objects = resp.get("Contents", [])
                if objects:
                    delete_keys = [{"Key": obj["Key"]} for obj in objects]
                    s3.delete_objects(Bucket=self.bucket_name, Delete={"Objects": delete_keys})
                    purged_count = len(delete_keys)
                    print(f"🗑️ [R2 Purge] Deleted {purged_count} frame objects under r2://{self.bucket_name}/{prefix}")
            except Exception as e:
                print(f"⚠️ [R2 Purge Notice] {e}")

        return purged_count

    def restore_frames_for_video(self, video_id: str, target_dir: Path) -> List[Path]:
        """
        Auto-restores clean .jpg frames when a previously private video flips back to public:
        Extracts from cold backup .zip and re-uploads to R2.
        """
        target_dir.mkdir(parents=True, exist_ok=True)
        cold_zip = BASE_DIR / "state" / "cold_vault" / f"{video_id}_frames_backup.zip"
        restored = []

        if cold_zip.exists():
            with zipfile.ZipFile(cold_zip, "r") as zf:
                zf.extractall(target_dir)
            restored = list(target_dir.glob("*.jpg"))
            print(f"🔄 [Auto-Recovery] Restored {len(restored)} frames from {cold_zip.name} -> {target_dir}")
            self.upload_public_frames(video_id, restored)
        else:
            print(f"ℹ️ [Auto-Recovery] Cold backup zip not found for {video_id}.")

        return restored


def sync_youtube_privacy_and_vault() -> Dict[str, Any]:
    """
    30-Minute YouTube Privacy & R2 Frame Vault Synchronizer:
    1. Checks all indexed videos in Cloudflare D1.
    2. Queries YouTube Data API videos.list(part="status").
    3. If video changed from public -> private/unlisted/deleted: instantly purges R2 frames!
    4. If video changed from private -> public: auto-recovers frames into R2!
    """
    d1 = CloudflareD1Client()
    r2 = CloudflareR2Client()

    videos = d1.get_indexed_videos()
    if not videos:
        print("ℹ️ No indexed videos found in Cloudflare D1 database.")
        return {"status": "empty", "checked": 0}

    print(f"🔍 [Privacy Sync Sweep] Auditing {len(videos)} indexed videos against live YouTube status...")

    # Load OAuth token
    from app.services.youtube_uploader import get_uploader
    try:
        uploader = get_uploader()
        service = uploader._get_service()
    except Exception as e:
        print(f"⚠️ Could not initialize YouTube service: {e}")
        return {"status": "error", "error": str(e)}

    video_ids = [v["video_id"] for v in videos]
    # YouTube API: 50 videos per request costs only 1 unit!
    try:
        yt_resp = service.videos().list(part="status", id=",".join(video_ids[:50])).execute()
    except Exception as e:
        print(f"⚠️ YouTube API query failed: {e}")
        return {"status": "error", "error": str(e)}

    live_map = {}
    for item in yt_resp.get("items", []):
        vid = item["id"]
        status = item.get("status", {}).get("privacyStatus", "private").lower()
        live_map[vid] = status

    purged = 0
    restored = 0
    unchanged = 0

    for v in videos:
        vid = v["video_id"]
        title = v.get("title", "")
        prev_status = (v.get("privacy_status") or "unlisted").lower()
        current_status = live_map.get(vid, "deleted")

        if prev_status == "public" and current_status != "public":
            print(f"🚨 Video {vid} ('{title}') changed: {prev_status} -> {current_status}. Purging R2 frames!")
            r2.purge_frames_for_video(vid)
            d1.update_video_status(vid, current_status)
            purged += 1
        elif prev_status != "public" and current_status == "public":
            print(f"🎉 Video {vid} ('{title}') changed: {prev_status} -> public! Restoring R2 frames...")
            rec_dir = Path("/tmp") / f"recovered_{vid}"
            r2.restore_frames_for_video(vid, rec_dir)
            d1.update_video_status(vid, "public")
            restored += 1
        else:
            d1.update_video_status(vid, current_status)
            unchanged += 1

    summary = {
        "status": "success",
        "total_checked": len(videos),
        "purged": purged,
        "restored": restored,
        "unchanged": unchanged
    }
    print(f"✅ [Privacy Sync Complete] Checked: {len(videos)} | Purged: {purged} | Restored: {restored} | Unchanged: {unchanged}")
    return summary


def get_vault_reusable_frame_with_hash_bust(d1_client: CloudflareD1Client, prompt: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a >=180-day-old vault frame and applies perceptual hash-busting transforms:
    - Inverted pan direction
    - 1.04x crop offset
    - Fresh temporal 35mm grain seed
    To YouTube's vHash algorithm, it registers as a brand-new camera angle.
    """
    eligible = d1_client.get_vault_eligible_frames(limit=1)
    if not eligible:
        return None

    frame = eligible[0]
    frame_id = frame["frame_id"]
    d1_client.mark_frame_reused(frame_id)

    # Hash-busting parameters for render_segment
    return {
        "frame_id": frame_id,
        "video_id": frame["video_id"],
        "r2_key": frame["r2_key"],
        "visual_prompt": frame["visual_prompt"],
        "hash_bust_transform": {
            "pan_invert": True,
            "crop_scale": 1.04,
            "grain_seed_offset": int(time.time()) % 1000
        }
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The Bull Print Cloudflare D1 & R2 Frame Vault CLI")
    parser.add_argument("--sync-youtube-privacy", action="store_true", help="Audit live YouTube privacy and sync R2 frames")
    parser.add_argument("--eligible-vault-frames", action="store_true", help="List >=180-day-old vault frames eligible for reuse")
    args = parser.parse_args()

    if args.sync_youtube_privacy:
        sync_youtube_privacy_and_vault()
    elif args.eligible_vault_frames:
        d1 = CloudflareD1Client()
        frames = d1.get_vault_eligible_frames(limit=20)
        print(f"🏛️ Found {len(frames)} vault frames eligible for reuse (>= 180 days old & public):")
        for f in frames:
            print(f" - [{f['frame_id']}] Video: {f['video_id']} | Prompt: {f['visual_prompt'][:60]}... | Created: {f['created_at_epoch']}")
    else:
        parser.print_help()
