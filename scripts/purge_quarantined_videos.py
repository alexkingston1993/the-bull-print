#!/usr/bin/env python3
"""
The Bull Print — Purge Quarantined Private Videos (scripts/purge_quarantined_videos.py)

Safely purges defective private quarantine videos from the YouTube channel that have:
- privacyStatus == 'private'
- publishAt is None (not scheduled for future release)
Preserves any scheduled or public videos.
"""

import os
import sys
import pickle
import time
from pathlib import Path
from loguru import logger
from googleapiclient.discovery import build

BASE_DIR = Path(__file__).resolve().parent.parent

def purge_quarantined_videos(dry_run: bool = False):
    token_file = BASE_DIR / "data" / "youtube_tokens" / "youtube_token_en.pickle"
    if not token_file.exists():
        logger.error(f"Token file {token_file} does not exist.")
        return

    with open(token_file, "rb") as f:
        creds = pickle.load(f)

    youtube = build("youtube", "v3", credentials=creds)
    
    # Get uploads playlist
    channels = youtube.channels().list(part="contentDetails", mine=True).execute()
    uploads_id = channels["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    logger.info(f"Fetching uploaded videos for channel playlist: {uploads_id}")
    
    # Paginate to get all recent private uploads
    video_ids = []
    page_token = None
    
    while True:
        res = youtube.playlistItems().list(
            part="snippet,status",
            playlistId=uploads_id,
            maxResults=50,
            pageToken=page_token
        ).execute()
        
        for item in res.get("items", []):
            vid = item["snippet"]["resourceId"]["videoId"]
            if item.get("status", {}).get("privacyStatus") == "private":
                video_ids.append(vid)
                
        page_token = res.get("nextPageToken")
        if not page_token or len(video_ids) >= 100:
            break

    logger.info(f"Identified {len(video_ids)} total private videos. Checking detailed status...")
    if not video_ids:
        logger.info("No private videos found to purge.")
        return

    # Check details in chunks of 50
    to_delete = []
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i+50]
        details = youtube.videos().list(
            part="status,snippet",
            id=",".join(chunk)
        ).execute()
        
        for item in details.get("items", []):
            vid = item["id"]
            title = item.get("snippet", {}).get("title", "")
            st = item.get("status", {})
            privacy = st.get("privacyStatus")
            publish_at = st.get("publishAt")
            
            # Target ONLY private videos with NO publishAt schedule
            if privacy == "private" and not publish_at:
                to_delete.append((vid, title))

    logger.warning(f"Found {len(to_delete)} private defective quarantine videos eligible for deletion.")
    
    deleted_count = 0
    for vid, title in to_delete:
        if dry_run:
            logger.info(f"[DRY RUN] Would delete: {vid} | {title}")
        else:
            try:
                youtube.videos().delete(id=vid).execute()
                deleted_count += 1
                logger.success(f"✓ [{deleted_count}/{len(to_delete)}] DELETED video {vid}: {title}")
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"Failed to delete {vid} ({title}): {e}")

    logger.info(f"Purge complete. Total deleted: {deleted_count} videos.")

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    purge_quarantined_videos(dry_run=dry_run)
