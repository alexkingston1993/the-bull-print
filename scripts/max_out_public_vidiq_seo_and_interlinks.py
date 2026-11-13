#!/usr/bin/env python3
"""
scripts/max_out_public_vidiq_seo_and_interlinks.py
Audits and updates all 61 PUBLIC videos on The Bull Print channel:
1. Maxes out vidIQ Actionable SEO Score (Tag Count, Tag Volume, Keywords in Title/Desc, Tripled Keywords) -> 48-50/50.
2. Contextually interlinks related YouTube videos with a custom note ("Watch Next" Binge Loop).
3. Adds exact canonical website article backlink to https://bullprintmedia.com/article/:slug.
4. Uses OAuth Slot 2 to preserve primary upload quota.
"""

import os
import sys
import json
import time
import re
import pickle
from difflib import SequenceMatcher
from googleapiclient.discovery import build

TOKEN_PATH = 'data/youtube_tokens/youtube_token_slot_2.pickle'
if not os.path.exists(TOKEN_PATH):
    TOKEN_PATH = 'data/youtube_tokens/youtube_token_en.pickle'

with open(TOKEN_PATH, 'rb') as f:
    creds = pickle.load(f)

youtube = build('youtube', 'v3', credentials=creds)

with open('content/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

print(f"Loaded {len(posts)} articles from content/posts.json")

# Master high-volume baseline tags pool
HIGH_VOLUME_CORE_TAGS = [
    "The Bull Print", "Nifty 50", "Stock Market India", "Dalal Street", 
    "Indian Stock Market", "Share Market", "FII DII Flows", "Option Trading", 
    "SEBI Rules", "Personal Finance India", "Mutual Funds", "Investing For Beginners"
]

def clean_words(text):
    clean = re.sub(r'[^\w\s]', ' ', text.lower())
    stop = {'what', 'with', 'this', 'that', 'your', 'from', 'have', 'more', 'shorts', 'short', 'about', 'when', 'will', 'make', 'into', 'after'}
    return [w for w in clean.split() if len(w) > 3 and w not in stop]

# 1. Fetch all public videos from channel
playlist_id = 'UUwe4D4M4i9aaHdi2ZBlbUmA'
public_videos = []
next_page_token = None

print("Fetching all public videos from uploads playlist...")
while True:
    res = youtube.playlistItems().list(
        playlistId=playlist_id,
        part='snippet,status',
        maxResults=50,
        pageToken=next_page_token
    ).execute()
    for item in res.get('items', []):
        if item['status'].get('privacyStatus') == 'public':
            public_videos.append({
                'id': item['snippet']['resourceId']['videoId'],
                'title': item['snippet']['title']
            })
    next_page_token = res.get('nextPageToken')
    if not next_page_token:
        break

print(f"Total Public Videos to Optimize: {len(public_videos)}")

# 2. Fetch full snippet for all public videos
detailed_videos = {}
for i in range(0, len(public_videos), 50):
    b = [v['id'] for v in public_videos[i:i+50]]
    r = youtube.videos().list(id=','.join(b), part='snippet').execute()
    for it in r.get('items', []):
        detailed_videos[it['id']] = it['snippet']

# 3. Matching and Optimization Engine
updates = []
for idx, v in enumerate(public_videos):
    vid_id = v['id']
    old_snip = detailed_videos[vid_id]
    orig_title = old_snip['title']
    cat_id = old_snip.get('categoryId', '27')
    v_words = clean_words(orig_title)

    # A. Best Article Match
    best_post = None
    best_score = -1.0
    for p in posts:
        p_title = p.get('title', '')
        p_words = clean_words(p_title)
        overlap = len(set(v_words).intersection(set(p_words)))
        seq = SequenceMatcher(None, orig_title.lower(), p_title.lower()).ratio()
        score = (overlap * 2.5) + seq
        if score > best_score:
            best_score = score
            best_post = p

    # Fallback to high-authority beginner post if no match
    if not best_post:
        best_post = posts[0]

    # B. Best Related Video Interlink (different video, same theme)
    rel_video = None
    best_rel_score = -1
    for other_v in public_videos:
        if other_v['id'] == vid_id:
            continue
        o_words = clean_words(other_v['title'])
        overlap = len(set(v_words).intersection(set(o_words)))
        if overlap > best_rel_score:
            best_rel_score = overlap
            rel_video = other_v

    if not rel_video:
        rel_video = public_videos[(idx + 1) % len(public_videos)]

    # C. Extract primary entities for Tripled Keywords
    clean_t = re.sub(r'#\w+', '', orig_title).strip()
    primary_kws = v_words[:3]
    if len(primary_kws) < 3:
        primary_kws += ['stock', 'market', 'nifty']
    kw1, kw2, kw3 = primary_kws[0].capitalize(), primary_kws[1].capitalize(), primary_kws[2].capitalize()

    # D. Tags construction (Target: 18-20 tags, < 500 chars total)
    video_specific_tags = [w.capitalize() for w in v_words if len(w) > 3][:6]
    candidate_tags = [
        orig_title.split(':')[0].strip(),
        f"{kw1} {kw2}",
        f"{kw2} {kw3}",
        kw1, kw2, kw3
    ] + video_specific_tags + HIGH_VOLUME_CORE_TAGS
    
    unique_tags = []
    total_len = 0
    for t in candidate_tags:
        clean_tag = t.replace('#', '').strip()
        if clean_tag and clean_tag.lower() not in [u.lower() for u in unique_tags]:
            if total_len + len(clean_tag) + 1 <= 460 and len(unique_tags) < 20:
                unique_tags.append(clean_tag)
                total_len += len(clean_tag) + 1

    # E. Contextual Description with Exact Tripled Keywords, Article Backlink, and Interlink
    article_url = f"https://bullprintmedia.com/article/{best_post['slug']}"
    related_vid_url = f"https://youtu.be/{rel_video['id']}"

    new_description = f"""{clean_t} — Forensic analysis on {kw1}, {kw2}, and {kw3} for Indian and global investors.
In this data-backed breakdown, The Bull Print uncovers institutional liquidity shifts, market microstructure, and actionable risk management principles.

📖 Read our full forensic investigation & charts on our website:
{article_url}

🎬 Recommended Next Watch (Interlinked Deep-Dive):
{rel_video['title']}
👉 Watch here: {related_vid_url}
💡 Why watch this next: This breakdown connects directly to how smart money and institutional liquidity dictate market momentum.

📊 Key Market Takeaways:
• Quantitative data and institutional order flow breakdown.
• Risk-adjusted positioning metrics for volatile market regimes.
• Moat and balance sheet forensic screening principles.

🌐 Free Institutional Tools on The Bull Print:
• Real-Time F&O Screener & PCR: https://bullprintmedia.com/fno
• Comprehensive Stock Screener: https://bullprintmedia.com/screener
• SIP Step-Up Wealth Calculator: https://bullprintmedia.com/calculators

⚠️ Statutory Disclaimer:
This content is published strictly for educational and informational purposes under SEBI RA guidelines and does not constitute financial, investment, or legal advice. Securities market investments are subject to market risks. Read all scheme disclosures carefully before investing.

#TheBullPrint #StockMarketIndia #Nifty50 #DalalStreet #FinanceIndia #InvestSmart #Shorts"""

    updates.append({
        'id': vid_id,
        'title': orig_title,
        'description': new_description.strip(),
        'tags': unique_tags,
        'categoryId': cat_id,
        'article_title': best_post['title'],
        'article_slug': best_post['slug'],
        'related_title': rel_video['title'],
        'related_id': rel_video['id']
    })

print(f"\nPrepared {len(updates)} video optimizations.")
print("Executing YouTube Data API metadata updates across all 61 public videos...\n")

success_count = 0
failed_count = 0

for i, u in enumerate(updates):
    try:
        body = {
            'id': u['id'],
            'snippet': {
                'title': u['title'],
                'description': u['description'],
                'tags': u['tags'],
                'categoryId': u['categoryId']
            }
        }
        res = youtube.videos().update(part='snippet', body=body).execute()
        success_count += 1
        print(f"[{i+1}/{len(updates)}] [OK] {u['id']} | Tags: {len(u['tags'])} | Matched Article: {u['article_slug'][:35]} | Next: {u['related_id']}")
        time.sleep(0.4) # Safe API pacing
    except Exception as e:
        failed_count += 1
        print(f"[{i+1}/{len(updates)}] [ERR] {u['id']} Error: {e}")

print(f"\nUpdate Complete: {success_count} succeeded, {failed_count} failed.")
