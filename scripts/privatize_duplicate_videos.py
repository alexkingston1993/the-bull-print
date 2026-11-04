"""
Channel Duplicate Video Cleaner (scripts/privatize_duplicate_videos.py)

Finds all duplicated videos on The Bull Print channel, identifies the top-performing
representative video in each cluster (highest views, earliest publish date), and safely moves
all duplicate uploads to 'private' status.

This ensures view counts and watch hours are preserved while cleaning up channel clutter.
"""

import os
import re
import sys
import pickle
from collections import defaultdict
from pathlib import Path
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


def get_authenticated_service():
    """Tries slot 2 token, then slot 1, then token_en."""
    candidates = [
        BASE_DIR / "data" / "youtube_tokens" / "youtube_token_slot_2.pickle",
        BASE_DIR / "data" / "youtube_tokens" / "youtube_token_en.pickle",
    ]
    for p in candidates:
        if p.exists():
            try:
                creds = pickle.loads(p.read_bytes())
                if hasattr(creds, "refresh"):
                    creds.refresh(Request())
                    if creds.valid:
                        logger.success(f"✓ Authenticated via {p.name}")
                        return build("youtube", "v3", credentials=creds)
            except Exception as e:
                logger.warning(f"Failed {p.name}: {e}")
    raise RuntimeError("No working YouTube OAuth token found!")


def normalize_title(title: str) -> str:
    cleaned = re.sub(r'#\w+', '', title)
    cleaned = re.sub(r'[^a-zA-Z0-9]+', ' ', cleaned.lower()).strip()
    return cleaned


def clean_duplicates():
    yt = get_authenticated_service()
    ch = yt.channels().list(mine=True, part="contentDetails").execute()
    uploads_pl = ch["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    logger.info("Fetching all channel uploads...")
    videos = []
    page_token = None
    while True:
        res = yt.playlistItems().list(
            playlistId=uploads_pl,
            part="snippet,status",
            maxResults=50,
            pageToken=page_token
        ).execute()
        for item in res.get("items", []):
            videos.append({
                "video_id": item["snippet"]["resourceId"]["videoId"],
                "title": item["snippet"]["title"],
                "privacy": item["status"].get("privacyStatus", "public"),
                "published_at": item["snippet"]["publishedAt"],
            })
        page_token = res.get("nextPageToken")
        if not page_token:
            break

    logger.info(f"Retrieved {len(videos)} total videos.")

    # Fetch view counts
    vids_map = {v["video_id"]: v for v in videos}
    vid_ids = list(vids_map.keys())
    for i in range(0, len(vid_ids), 50):
        batch = vid_ids[i:i+50]
        stats_res = yt.videos().list(id=",".join(batch), part="statistics").execute()
        for it in stats_res.get("items", []):
            vids_map[it["id"]]["views"] = int(it.get("statistics", {}).get("viewCount", 0))

    title_map = defaultdict(list)
    for v in videos:
        if v["title"] == "Deleted video":
            continue
        norm = normalize_title(v["title"])
        title_map[norm].append(v)

    duplicate_clusters = {k: v for k, v in title_map.items() if len(v) > 1}
    logger.info(f"Found {len(duplicate_clusters)} duplicate clusters.")

    privatized_count = 0
    kept_count = 0

    for norm, group in duplicate_clusters.items():
        # Prefer public videos with highest views
        public_group = [v for v in group if v["privacy"] == "public"]
        if public_group:
            public_group.sort(key=lambda x: (x.get("views", 0), x["published_at"]), reverse=True)
            winner = public_group[0]
        else:
            group.sort(key=lambda x: (x.get("views", 0), x["published_at"]), reverse=True)
            winner = group[0]

        logger.info(f"\nCluster: '{winner['title']}' ({len(group)} uploads)")
        logger.info(f"  --> KEEPING PUBLIC: {winner['video_id']} (Views: {winner.get('views', 0)}, Status: {winner['privacy']})")
        kept_count += 1

        for dupe in group:
            if dupe["video_id"] == winner["video_id"]:
                continue
            if dupe["privacy"] != "private":
                logger.warning(f"  --> PRIVATIZING duplicate {dupe['video_id']} (Views: {dupe.get('views', 0)}, Status: {dupe['privacy']})...")
                try:
                    yt.videos().update(
                        part="status",
                        body={
                            "id": dupe["video_id"],
                            "status": {
                                "privacyStatus": "private"
                            }
                        }
                    ).execute()
                    privatized_count += 1
                    logger.success(f"    ✓ Successfully set {dupe['video_id']} to private.")
                except Exception as err:
                    logger.error(f"    ❌ Failed to privatize {dupe['video_id']}: {err}")
            else:
                logger.info(f"  --> Already private: {dupe['video_id']}")

    logger.success(f"\nClean-up Complete: {privatized_count} duplicate videos moved to private, {kept_count} primary videos kept public.")


if __name__ == "__main__":
    clean_duplicates()
