#!/usr/bin/env python3
"""
IndexNow Fast-Track Submission Engine
Pings search engines (Bing, Perplexity, Yandex, Seznam) via the IndexNow protocol
for all 3,980+ static URLs across Dalal Street stocks, cryptocurrencies, articles, and financial terminals.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOST = "bullprintmedia.com"
KEY = "4f29a7d83e204c329b45667e8125ac89"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
INDEXNOW_ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow"
]

def load_all_urls():
    urls = []
    
    # 1. Core pages & hubs
    core_paths = [
        "",
        "/stocks",
        "/crypto",
        "/crypto-radar",
        "/screener",
        "/calculators",
        "/portfolio",
        "/insurance",
        "/fno",
        "/ipo",
        "/unlisted",
        "/articles",
        "/pipeline-dashboard"
    ]
    for p in core_paths:
        urls.append(f"https://{HOST}{p}")
        
    # 2. All active NSE Stocks
    stocks_file = ROOT / "content" / "stocks_database.json"
    if stocks_file.exists():
        with open(stocks_file, "r", encoding="utf-8") as f:
            stocks = json.load(f)
            if isinstance(stocks, dict):
                for sym in stocks.keys():
                    urls.append(f"https://{HOST}/stocks/{sym}")
            elif isinstance(stocks, list):
                for s in stocks:
                    sym = s.get("symbol") if isinstance(s, dict) else str(s)
                    if sym:
                        urls.append(f"https://{HOST}/stocks/{sym}")
                    
    # 3. All Top 1,000 Cryptos
    crypto_file = ROOT / "content" / "crypto_database.json"
    if crypto_file.exists():
        with open(crypto_file, "r", encoding="utf-8") as f:
            cryptos = json.load(f)
            if isinstance(cryptos, dict):
                for sym in cryptos.keys():
                    urls.append(f"https://{HOST}/crypto/{sym}")
            elif isinstance(cryptos, list):
                for c in cryptos:
                    sym = c.get("symbol") if isinstance(c, dict) else str(c)
                    if sym:
                        urls.append(f"https://{HOST}/crypto/{sym}")
                    
    # 4. All Published Articles
    posts_file = ROOT / "content" / "posts.json"
    if posts_file.exists():
        with open(posts_file, "r", encoding="utf-8") as f:
            posts = json.load(f)
            for p in posts:
                slug = p.get("slug")
                if slug:
                    urls.append(f"https://{HOST}/posts/{slug}")
                    
    # Deduplicate while preserving order
    unique_urls = list(dict.fromkeys(urls))
    return unique_urls

def ping_indexnow(urls):
    print(f"[*] Total unique URLs gathered: {len(urls)}")
    BATCH_SIZE = 1000
    
    for i in range(0, len(urls), BATCH_SIZE):
        batch = urls[i:i + BATCH_SIZE]
        payload = {
            "host": HOST,
            "key": KEY,
            "keyLocation": KEY_LOCATION,
            "urlList": batch
        }
        data = json.dumps(payload).encode("utf-8")
        
        for endpoint in INDEXNOW_ENDPOINTS:
            print(f"[*] Submitting batch {i // BATCH_SIZE + 1} ({len(batch)} URLs) to {endpoint}...")
            req = urllib.request.Request(
                endpoint,
                data=data,
                headers={
                    "Content-Type": "application/json; charset=utf-8",
                    "User-Agent": "TheBullPrint-IndexNow/2.0"
                },
                method="POST"
            )
            try:
                with urllib.request.urlopen(req, timeout=15) as resp:
                    print(f"    [+] Response: {resp.status} {resp.reason}")
            except urllib.error.HTTPError as e:
                print(f"    [-] HTTP Error {e.code}: {e.read().decode('utf-8', errors='ignore')}")
            except Exception as e:
                print(f"    [-] Error pinging {endpoint}: {e}")

if __name__ == "__main__":
    all_urls = load_all_urls()
    ping_indexnow(all_urls)
