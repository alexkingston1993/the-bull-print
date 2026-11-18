-- Cloudflare D1 Database Schema for The Bull Print Control Plane
-- Database: tbp-production-db (UUID: f54ea399-d524-45d9-8974-bf4edfb4741a)

CREATE TABLE IF NOT EXISTS videos (
  video_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  privacy_status TEXT NOT NULL DEFAULT 'unlisted', -- 'public', 'private', 'unlisted', 'deleted'
  r2_prefix TEXT,
  total_frames INTEGER DEFAULT 0,
  created_at_epoch INTEGER NOT NULL,
  last_checked_epoch INTEGER NOT NULL,
  cold_backup_url TEXT,
  cut_timestamps_json TEXT
);

CREATE TABLE IF NOT EXISTS frames (
  frame_id TEXT PRIMARY KEY,
  video_id TEXT NOT NULL,
  frame_index INTEGER NOT NULL,
  r2_key TEXT NOT NULL,
  privacy_status TEXT NOT NULL DEFAULT 'unlisted',
  visual_prompt TEXT NOT NULL,
  seed INTEGER DEFAULT 0,
  created_at_epoch INTEGER NOT NULL,
  last_used_epoch INTEGER NOT NULL,
  is_vault_eligible INTEGER DEFAULT 0, -- 1 only when >= 180 days old and public
  FOREIGN KEY (video_id) REFERENCES videos(video_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_videos_privacy ON videos(privacy_status);
CREATE INDEX IF NOT EXISTS idx_frames_vault_eligibility ON frames(is_vault_eligible, privacy_status, created_at_epoch);

