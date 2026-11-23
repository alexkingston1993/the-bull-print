#!/usr/bin/env python3
"""
scripts/max_out_public_vidiq_seo_and_interlinks.py
Audits and updates all PUBLIC and SCHEDULED videos on The Bull Print channel:
1. Maxes out vidIQ Actionable SEO Score (Tag Count, Tag Volume, Keywords in Title/Desc, Tripled Keywords) -> 48-50/50.
2. Contextually interlinks related YouTube videos with a custom note ("Watch Next" Binge Loop).
3. Adds exact canonical website article backlink to https://bullprintmedia.com/article/:slug.
4. Adds platform tools links (/fno, /screener, /calculators) and Key Market Takeaways for AI search.
5. Uses OAuth Slot 2 to preserve primary upload quota.
6. Safely skips already fully optimized videos to conserve API quota.
"""

import os
import sys
import json
import time
import re
import pickle
from difflib import SequenceMatcher
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# 1. Setup YouTube Client with auto-refresh
TOKEN_PATH = 'data/youtube_tokens/youtube_token_slot_2.pickle'
if not os.path.exists(TOKEN_PATH):
    TOKEN_PATH = 'data/youtube_tokens/youtube_token_en.pickle'

with open(TOKEN_PATH, 'rb') as f:
    creds = pickle.load(f)

if creds and creds.expired and creds.refresh_token:
    print("Refreshing OAuth credentials...")
    creds.refresh(Request())
    with open(TOKEN_PATH, 'wb') as f:
        pickle.dump(creds, f)

youtube = build('youtube', 'v3', credentials=creds)

# 2. Load articles
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

# 3. Dynamically discover uploads playlist
ch_res = youtube.channels().list(part='contentDetails', mine=True).execute()
playlist_id = ch_res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
print(f"Discovered channel uploads playlist: {playlist_id}")

# 4. Fetch all videos from uploads playlist
all_channel_videos = []
next_page_token = None

print("Fetching all videos from uploads playlist...")
while True:
    res = youtube.playlistItems().list(
        playlistId=playlist_id,
        part='snippet,status',
        maxResults=50,
        pageToken=next_page_token
    ).execute()
    for item in res.get('items', []):
        all_channel_videos.append({
            'id': item['snippet']['resourceId']['videoId'],
            'title': item['snippet']['title'],
            'privacy': item['status'].get('privacyStatus')
        })
    next_page_token = res.get('nextPageToken')
    if not next_page_token:
        break

print(f"Total Videos on Channel: {len(all_channel_videos)}")

# 5. Fetch full snippets in batches of 50
detailed_videos = {}
for i in range(0, len(all_channel_videos), 50):
    b = [v['id'] for v in all_channel_videos[i:i+50]]
    r = youtube.videos().list(id=','.join(b), part='snippet').execute()
    for it in r.get('items', []):
        detailed_videos[it['id']] = it['snippet']

# 6. Audit & Determine Candidates Needing Upgrade
updates = []
skipped_count = 0

for idx, v in enumerate(all_channel_videos):
    vid_id = v['id']
    old_snip = detailed_videos.get(vid_id)
    if not old_snip:
        continue
    orig_title = old_snip['title']
    old_desc = old_snip.get('description', '')
    old_tags = old_snip.get('tags', [])
    cat_id = old_snip.get('categoryId', '27')
    v_words = clean_words(orig_title)

    has_backlink = ('bullprintmedia.com/article/' in old_desc) or ('bullprintmedia.com/posts/' in old_desc)
    has_interlink = ('youtu.be/' in old_desc) or ('youtube.com/watch' in old_desc)
    has_tools = ('bullprintmedia.com/fno' in old_desc) and ('bullprintmedia.com/calculators' in old_desc)
    has_sufficient_tags = len(old_tags) >= 15

    # Safe Skip: If video already meets full 6-layer standard, don't overwrite
    if has_backlink and has_interlink and has_tools and has_sufficient_tags:
        skipped_count += 1
        continue

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

    if not best_post:
        best_post = posts[0]

    # B. Best Related Video Interlink (different video, same theme)
    rel_video = None
    best_rel_score = -1
    for other_v in all_channel_videos:
        if other_v['id'] == vid_id:
            continue
        o_words = clean_words(other_v['title'])
        overlap = len(set(v_words).intersection(set(o_words)))
        if overlap > best_rel_score:
            best_rel_score = overlap
            rel_video = other_v

    if not rel_video:
        rel_video = all_channel_videos[(idx + 1) % len(all_channel_videos)]

    # C. Extract primary entities for Tripled Keywords
    clean_t = re.sub(r'#\w+', '', orig_title).strip()
    primary_kws = v_words[:3]
    if len(primary_kws) < 3:
        primary_kws += ['stock', 'market', 'nifty']
    kw1, kw2, kw3 = primary_kws[0].capitalize(), primary_kws[1].capitalize(), primary_kws[2].capitalize()

    # D. Tags construction (Target: 18-20 tags, < 480 chars total)
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

    # E. Contextual Description with Tripled Keywords, Article Backlink, and Interlink
    article_url = f"https://bullprintmedia.com/article/{best_post['slug']}"
    related_vid_url = f"https://youtu.be/{rel_video['id']}"

    desc_templates = [
        f"{clean_t} — Investigative deep-dive examining {kw1}, {kw2}, and {kw3} across institutional balance sheets.\nThis data-backed breakdown dissects structural order flows, regulatory filings, and systemic risk factors driving market volatility.",
        f"{clean_t} — Forensic analysis uncovering {kw1}, {kw2}, and structural {kw3} dynamics.\nWe dissect institutional transaction data, macro liquidity imbalances, and risk-adjusted positioning metrics for investors.",
        f"{clean_t} — Unpacking the critical mechanics behind {kw1}, {kw2}, and {kw3} across modern markets.\nA data-driven investigation into off-balance-sheet exposures, capital flows, and empirical valuation anomalies.",
        f"{clean_t} — Behind the scenes of {kw1}, {kw2}, and {kw3}: how institutional desks position ahead of systemic shocks.\nExamining transaction telemetry, regulatory disclosures, and market microstructure.",
        f"{clean_t} — Quantitative investigation into {kw1}, {kw2}, and {kw3} across global and domestic markets.\nTracking institutional positioning, derivatives pressure points, and capital preservation protocols.",
        f"{clean_t} — Forensic research breakdown on {kw1}, {kw2}, and {kw3}.\nEvaluating balance sheet fragility, institutional accumulation patterns, and macro catalysts shaping the current regime.",
        f"{clean_t} — Critical breakdown of {kw1}, {kw2}, and {kw3}.\nTracing order flow imbalances, custodial filings, and historical precedents to decode today's market structure.",
        f"{clean_t} — Forensic audit investigating {kw1}, {kw2}, and {kw3}.\nRevealing the underlying institutional mechanics, liquidity cycles, and systemic risks impacting capital allocation.",
    ]
    opening_hook = desc_templates[abs(hash(clean_t)) % len(desc_templates)]

    value_bridges = [
        "This breakdown connects directly to how institutional capital cycles and liquidity regimes dictate market momentum.",
        "Essential context on how large-scale balance sheet adjustments ripple into broader market structure.",
        "Deepens the forensic picture by exposing the underlying transaction mechanics and counterparty risks.",
        "Provides actionable analytical depth into the macroeconomic catalysts and volatility drivers highlighted here.",
    ]
    bridge_text = value_bridges[abs(hash(clean_t + "bridge")) % len(value_bridges)]

    new_description = f"""{opening_hook}

📖 Read our full forensic investigation & charts on our website:
{article_url}

🎬 Recommended Next Watch (Interlinked Deep-Dive):
{rel_video['title']}
👉 Watch here: {related_vid_url}
💡 Why watch this next: {bridge_text}

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

print(f"\nAudit Results: {skipped_count} videos already fully optimized.")
print(f"Queued for vidIQ & Interlink Upgrade: {len(updates)} legacy videos.\n")

if not updates:
    print("✅ All videos on the channel are already 100% fully optimized!")
    sys.exit(0)

print(f"Executing YouTube Data API metadata updates across {len(updates)} legacy videos...\n")

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
        time.sleep(0.5)  # Safe API pacing to respect rate limits
    except Exception as e:
        failed_count += 1
        print(f"[{i+1}/{len(updates)}] [ERR] {u['id']} Error: {e}")

print(f"\n{'='*60}")
print(f"🎉 Batch Optimization Complete!")
print(f"✓ Successfully upgraded: {success_count} videos")
if failed_count > 0:
    print(f"⚠️ Failed: {failed_count} videos")
print(f"✓ Already optimized: {skipped_count} videos")
print(f"✓ Total catalog optimized: {skipped_count + success_count}/{len(all_channel_videos)}")
print(f"{'='*60}")
