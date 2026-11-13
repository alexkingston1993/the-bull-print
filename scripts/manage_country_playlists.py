#!/usr/bin/env python3
"""
Global Multi-Country Playlist Architect & Video Tagging Engine
Channel: The Bull Print (@thebullprint)

Targets 11 key wealth & capital market jurisdictions:
1. India (Dalal Street, SEBI, Equities, Corporate Heists)
2. United States (Wall Street, SEC, Fed, Tech, Trump Trade)
3. Australia & New Zealand (ASX, Mining, Commodities, Superannuation)
4. United Kingdom & Ireland (City of London, BoE, European Macro)
5. Canada (Bay Street, Natural Resources, Banking, Real Estate)
6. Singapore & Hong Kong (Asian Wealth Hubs, MAS, HKEX, FinTech)
7. United Arab Emirates & Gulf (Dubai/Abu Dhabi, OPEC Energy, Global Capital)
8. South Africa & Emerging Markets (JSE, Gold Mining, Reserve Currencies)
9. Global Investigative Documentaries (The Masterclass 12-Minute Series)

Creates the playlist ecosystem and categorizes current documentaries and shorts.
"""

import sys
import time
from pathlib import Path
from typing import Dict, List, Set, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from googleapiclient.errors import HttpError
from app.services.youtube_uploader import YouTubeUploader

COUNTRY_PLAYLISTS = {
    "global_masters": {
        "title": "Investigative Documentaries | The 100-Year Masterclass Series",
        "description": "Exhaustive, forensic 12-minute financial master documentaries uncovering corporate fraud, algorithmic manipulation, and institutional market structure by The Bull Print.",
        "countries": ["US", "IN", "GB", "AU", "CA", "SG", "AE", "HK", "NZ", "IE", "ZA"],
    },
    "united_states": {
        "title": "United States | Wall Street, Fed Policy & Global Macro",
        "description": "Deep-dive investigations into US capital markets, Federal Reserve rate cycles, Wall Street institutional flow, US tech monopolies, and cross-border geopolitical shifts.",
        "countries": ["US"],
    },
    "india": {
        "title": "India | Dalal Street, SEBI & Corporate Forensics",
        "description": "Forensic breakdowns of Dalal Street, SEBI regulations, institutional operator syndicates, Indian corporate heists, Nifty/Bank Nifty order flow, and retail wealth preservation.",
        "countries": ["IN"],
    },
    "united_kingdom_ireland": {
        "title": "United Kingdom & Ireland | London City & Sovereign Capital",
        "description": "Investigative analysis of the City of London, Bank of England monetary shifts, European financial flows, cross-border corporate forensics, and multinational capital corridors.",
        "countries": ["GB", "IE"],
    },
    "australia_new_zealand": {
        "title": "Australia & New Zealand | ASX, Mining & Wealth Corridors",
        "description": "Institutional investigations into the Australian Securities Exchange (ASX), mining and energy titans, superannuation capital deployment, and Asia-Pacific trade dynamics.",
        "countries": ["AU", "NZ"],
    },
    "canada": {
        "title": "Canada | Bay Street, Resources & Banking Forensics",
        "description": "Forensic coverage of Canadian financial institutions, commodity balance sheets, Toronto Stock Exchange (TSX) dynamics, and US-Canada cross-border capital integration.",
        "countries": ["CA"],
    },
    "singapore_hong_kong": {
        "title": "Singapore & Hong Kong | Asian Financial Hubs & Tech Capital",
        "description": "Unpacking Singapore (MAS) and Hong Kong (HKEX) sovereign wealth management, offshore family offices, fintech infrastructure, and Asian capital corridors.",
        "countries": ["SG", "HK"],
    },
    "uae_gulf": {
        "title": "United Arab Emirates & Gulf | Sovereign Energy & Global Wealth",
        "description": "Forensic audits of Dubai & Abu Dhabi sovereign funds, OPEC crude economics, luxury capital flight corridors, and Middle East wealth diversification.",
        "countries": ["AE"],
    },
    "south_africa": {
        "title": "South Africa & Emerging Markets | Mining, Gold & Macro",
        "description": "Forensic investigations into African precious metals, JSE equity dynamics, central bank reserve hoarding, and emerging market currency volatility.",
        "countries": ["ZA"],
    },
}

# Country specific tags mapping to augment video SEO
COUNTRY_TAG_MAPPING = {
    "US": ["#WallStreet", "#FederalReserve", "#USStocks", "#SEC", "#TrumpTrade", "#USMarkets", "#NYSE", "#Nasdaq"],
    "IN": ["#DalalStreet", "#Nifty50", "#SEBI", "#StockMarketIndia", "#Sensex", "#IndianEconomy"],
    "GB": ["#LondonCity", "#FTSE", "#BankOfEngland", "#UKFinance", "#FCA"],
    "IE": ["#IrelandBusiness", "#DublinFinance", "#EuropeanEconomy"],
    "AU": ["#ASX", "#ASIC", "#AustraliaEconomy", "#MiningStocks", "#Superannuation"],
    "NZ": ["#RBNZ", "#NewZealandEconomy", "#NZX"],
    "CA": ["#TSX", "#BayStreet", "#BankOfCanada", "#CanadianEconomy"],
    "SG": ["#MAS", "#SGX", "#SingaporeFinance", "#Temasek"],
    "HK": ["#HKEX", "#HongKongFinance", "#HangSeng"],
    "AE": ["#DubaiFinance", "#ADGM", "#DIFC", "#OPEC", "#GulfEnergy", "#UAE"],
    "ZA": ["#JSE", "#SouthAfricaEconomy", "#GoldMining", "#FSCA"],
}

# Video to Playlist Mapping Rules
VIDEO_TARGET_MAP = {
    # Master Documentaries
    "OwNPa-sz-2Q": ["global_masters", "united_states", "singapore_hong_kong", "united_kingdom_ireland"], # FTX & Alameda
    "UWH9EJhDU9Q": ["global_masters", "india", "united_states"], # ₹20 Lakh Barrier (SEBI/Algo HFT)
    "J2yXwOno1lA": ["global_masters", "india", "singapore_hong_kong"], # WazirX & Zettai Pte Ltd Singapore
    "MRaIL_-X3wA": ["global_masters", "india", "uae_gulf"], # Operator Syndicate & Dubai Hawala
    "t30Zwep0L9s": ["global_masters", "india", "united_states", "united_kingdom_ireland"], # Health Insurance Rejection Machine

    # Trump 10 Shorts Series
    "sXW3aekYFx8": ["united_states", "india"], # Short 01: Rupee to 85 & USD Index
    "W0eARjv3IVE": ["united_states", "india", "australia_new_zealand"], # Short 02: 60% China Tariff
    "uCTA_6AuxfI": ["united_states", "india", "canada", "united_kingdom_ireland"], # Short 03: H-1B vs 15% Tax Cut
    "5kTihclG_bw": ["united_states", "india", "australia_new_zealand"], # Short 04: ₹50,000 Cr Weapons Axis (Quad)
    "t1h7gZMGMUs": ["united_states", "india", "singapore_hong_kong", "uae_gulf"], # Short 05: Bitcoin $100K & 30% Tax
    "fwNkXmnWaHo": ["united_states", "india", "united_kingdom_ireland"], # Short 06: FIIs Dump ₹1.2 Lakh Cr
    "4rkbyVAi-pA": ["united_states", "india", "uae_gulf"], # Short 07: Drill Baby Drill & Cheap Oil
    "qhtpW1OL3EE": ["united_states", "india", "united_kingdom_ireland", "canada"], # Short 08: Drug Price War & Generics
    "UHq60qmTAA0": ["united_states", "india", "uae_gulf", "south_africa", "australia_new_zealand"], # Short 09: Sona & Gold Boom
    "XYyXJ-Zi1a4": ["united_states", "india", "australia_new_zealand", "uae_gulf"], # Short 10: Adani-Trump Energy Axis
}

def get_or_create_playlists(srv) -> Dict[str, str]:
    print("Auditing existing playlists on YouTube...")
    res = srv.playlists().list(part="snippet,status", mine=True, maxResults=50).execute()
    existing = res.get("items", [])
    title_to_id = {it["snippet"]["title"].strip().lower(): it["id"] for it in existing}

    pl_map = {}
    for key, info in COUNTRY_PLAYLISTS.items():
        t_lower = info["title"].strip().lower()
        if t_lower in title_to_id:
            pl_id = title_to_id[t_lower]
            print(f"✓ Found existing: '{info['title']}' ({pl_id})")
            pl_map[key] = pl_id
        else:
            print(f"Creating playlist: '{info['title']}'...")
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
            print(f"🎉 Created new playlist: '{info['title']}' ({pl_id})")
            pl_map[key] = pl_id
            time.sleep(0.5)

    return pl_map

def get_playlist_video_ids(srv, playlist_id: str) -> Set[str]:
    vids = set()
    page_token = None
    while True:
        try:
            res = srv.playlistItems().list(
                playlistId=playlist_id,
                part="snippet",
                maxResults=50,
                pageToken=page_token
            ).execute()
            for it in res.get("items", []):
                vid = it.get("snippet", {}).get("resourceId", {}).get("videoId")
                if vid:
                    vids.add(vid)
            page_token = res.get("nextPageToken")
            if not page_token:
                break
        except Exception as e:
            print(f"Warning fetching playlist {playlist_id}: {e}")
            break
    return vids

def main():
    print("=" * 75)
    print("🌍 THE BULL PRINT: MULTI-COUNTRY PLAYLIST ARCHITECT & ASSIGNMENT")
    print("=" * 75)

    uploader = YouTubeUploader()
    srv = uploader._get_service("en")
    if not srv:
        print("❌ Could not obtain YouTube service.")
        return

    # 1. Ensure all 9 country/regional playlists exist
    pl_map = get_or_create_playlists(srv)

    # 2. Get existing videos per playlist
    existing_in_pl = {}
    for key, pl_id in pl_map.items():
        existing_in_pl[key] = get_playlist_video_ids(srv, pl_id)

    # 3. Add videos according to VIDEO_TARGET_MAP
    added_count = 0
    print("\nPopulating playlists with targeted documentaries and shorts...")
    for vid, target_keys in VIDEO_TARGET_MAP.items():
        for key in target_keys:
            pl_id = pl_map[key]
            if vid in existing_in_pl[key]:
                continue

            try:
                srv.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": pl_id,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": vid,
                            }
                        }
                    }
                ).execute()
                added_count += 1
                existing_in_pl[key].add(vid)
                print(f"✓ Added {vid} to [{COUNTRY_PLAYLISTS[key]['title'][:35]}...]")
                time.sleep(0.3)
            except Exception as e:
                print(f"❌ Failed to add {vid} to {key}: {e}")

    print("\n" + "=" * 75)
    print(f"✨ MULTI-COUNTRY PLAYLIST SETUP COMPLETE! Added {added_count} video entries.")
    print("Playlists created & live on channel:")
    for key, pl_id in pl_map.items():
        url = f"https://www.youtube.com/playlist?list={pl_id}"
        count = len(existing_in_pl[key])
        print(f"📁 {COUNTRY_PLAYLISTS[key]['title']} ({count} videos): {url}")
    print("=" * 75)

if __name__ == "__main__":
    main()
