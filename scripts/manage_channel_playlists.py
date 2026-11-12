"""
Channel Playlist Organizer & Video Categorizer (scripts/manage_channel_playlists.py)

Creates the 3 core playlists on The Bull Print YouTube channel:
1. Crypto
2. Stock Market
3. Insurance

Audits all channel uploads, classifies each video by topic/vertical,
and adds every video into its respective playlist.
"""

import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Set, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from googleapiclient.errors import HttpError
from app.services.youtube_uploader import YouTubeUploader, detect_vertical_from_content
from loguru import logger


TARGET_PLAYLISTS = {
    "crypto": {
        "title": "Crypto",
        "description": "On-Chain Forensics, Liquidity Heatmaps, Perpetual Derivatives, and Web3 Market Structure by The Bull Print.",
    },
    "stock_market": {
        "title": "Stock Market",
        "description": "Nifty 50, Bank Nifty, Options Chain Open Interest, FII/DII Institutional Order Flow & Quantitative Equities.",
    },
    "insurance": {
        "title": "Insurance",
        "description": "IRDAI Regulatory Forensics, Health & Term Insurance Audits, Incurred Claim Ratios, and Consumer Protection.",
    },
    "beginners_finance": {
        "title": "Beginners in Finance: The 365-Day Masterclass",
        "description": "Zero to Wall Street: The complete 365-day masterclass on Corporate Finance, Investment Banking, Quantitative Trading, Equity Analysis, and Wealth Building by The Bull Print.",
    },
}


def get_or_create_playlists(srv) -> Dict[str, str]:
    """Retrieves or creates the 3 targeted playlists. Returns {vertical_key: playlist_id}."""
    logger.info("Auditing channel playlists...")
    res = srv.playlists().list(part="snippet,status", mine=True, maxResults=50).execute()
    existing = res.get("items", [])
    
    pl_map: Dict[str, str] = {}
    title_to_id = {it["snippet"]["title"].strip().lower(): it["id"] for it in existing}

    for key, info in TARGET_PLAYLISTS.items():
        t_lower = info["title"].lower()
        if t_lower in title_to_id:
            pl_id = title_to_id[t_lower]
            logger.info(f"✓ Found existing playlist '{info['title']}': {pl_id}")
            pl_map[key] = pl_id
        else:
            logger.info(f"Creating playlist '{info['title']}'...")
            body = {
                "snippet": {
                    "title": info["title"],
                    "description": info["description"],
                },
                "status": {
                    "privacyStatus": "public"
                }
            }
            new_pl = srv.playlists().insert(part="snippet,status", body=body).execute()
            pl_id = new_pl["id"]
            logger.success(f"✓ Created new playlist '{info['title']}': {pl_id}")
            pl_map[key] = pl_id

    return pl_map


def get_existing_playlist_video_ids(srv, playlist_id: str) -> Set[str]:
    """Returns set of videoIds already in a playlist to prevent duplicates."""
    video_ids = set()
    page_token = None
    while True:
        try:
            res = srv.playlistItems().list(
                playlistId=playlist_id,
                part="snippet,contentDetails",
                maxResults=50,
                pageToken=page_token
            ).execute()
            for item in res.get("items", []):
                vid = item.get("snippet", {}).get("resourceId", {}).get("videoId")
                if vid:
                    video_ids.add(vid)
            page_token = res.get("nextPageToken")
            if not page_token:
                break
        except Exception as e:
            logger.warning(f"Error fetching items for playlist {playlist_id}: {e}")
            break
    return video_ids


def categorize_and_populate():
    uploader = YouTubeUploader()
    srv = uploader._get_service("en")
    if not srv:
        logger.error("Could not obtain authenticated YouTube service!")
        return

    # 1. Ensure the 3 playlists exist
    pl_map = get_or_create_playlists(srv)

    # 2. Get existing items per playlist
    existing_items: Dict[str, Set[str]] = {}
    for key, pl_id in pl_map.items():
        existing_items[key] = get_existing_playlist_video_ids(srv, pl_id)
        logger.info(f"Playlist '{TARGET_PLAYLISTS[key]['title']}' currently has {len(existing_items[key])} videos.")

    # 3. Retrieve all uploads from channel
    ch = srv.channels().list(mine=True, part="contentDetails").execute()
    uploads_pl = ch["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    
    logger.info("Retrieving all uploaded channel videos...")
    all_uploads = []
    page_token = None
    while True:
        res = srv.playlistItems().list(
            playlistId=uploads_pl,
            part="snippet",
            maxResults=50,
            pageToken=page_token
        ).execute()
        all_uploads.extend(res.get("items", []))
        page_token = res.get("nextPageToken")
        if not page_token:
            break

    logger.info(f"Found {len(all_uploads)} total uploads on channel.")

    stats = {"crypto": 0, "stock_market": 0, "insurance": 0, "skipped": 0, "already_in": 0}

    # 4. Classify and add each video
    for it in all_uploads:
        snippet = it.get("snippet", {})
        vid_id = snippet.get("resourceId", {}).get("videoId")
        title = snippet.get("title", "")
        desc = snippet.get("description", "")

        if not vid_id or title == "Deleted video" or title == "Private video":
            stats["skipped"] += 1
            continue

        # Detect vertical
        vertical = detect_vertical_from_content(title, desc)
        target_pl_id = pl_map[vertical]

        if vid_id in existing_items[vertical]:
            stats["already_in"] += 1
            continue

        try:
            srv.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": target_pl_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": vid_id,
                        }
                    }
                }
            ).execute()
            stats[vertical] += 1
            existing_items[vertical].add(vid_id)
            logger.info(f"[{TARGET_PLAYLISTS[vertical]['title']}] Added: {title[:50]} ({vid_id})")
            time.sleep(0.3) # Rate limit courtesy
        except HttpError as e:
            if "quotaExceeded" in str(e):
                logger.error("YouTube API quota reached during playlist insertions!")
                break
            logger.warning(f"Could not add {vid_id} to playlist {vertical}: {e}")

    print("\n═══════════════════════════════════════════════════════════════")
    print("✨ PLAYLIST POPULATION COMPLETE!")
    print("═══════════════════════════════════════════════════════════════")
    for key, pl_id in pl_map.items():
        name = TARGET_PLAYLISTS[key]["title"]
        count = len(existing_items[key])
        url = f"https://www.youtube.com/playlist?list={pl_id}"
        print(f"📁 {name} Playlist ({count} videos): {url}")
    print(f"\nStats: {stats['crypto']} added to Crypto, {stats['stock_market']} added to Stock Market, {stats['insurance']} added to Insurance. ({stats['already_in']} already existed, {stats['skipped']} skipped).")
    print("═══════════════════════════════════════════════════════════════\n")


if __name__ == "__main__":
    categorize_and_populate()
