#!/usr/bin/env python3
"""
IndexNow Ping Engine for Bing Webmaster & Search Crawlers.
Instantly notifies search engines of new or updated URLs on bullprintmedia.com.
"""
import requests
import json
import sys

HOST = "bullprintmedia.com"
KEY = "4f29a7d83e204c329b45667e8125ac89"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"

def submit_urls(urls: list):
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls
    }
    
    endpoints = [
        "https://api.indexnow.org/indexnow",
        "https://www.bing.com/indexnow"
    ]
    
    for ep in endpoints:
        try:
            res = requests.post(
                ep,
                headers={"Content-Type": "application/json; charset=utf-8"},
                data=json.dumps(payload),
                timeout=10
            )
            print(f"IndexNow [{ep}]: HTTP {res.status_code}")
        except Exception as e:
            print(f"IndexNow [{ep}] failed: {e}")

if __name__ == "__main__":
    test_urls = [
        f"https://{HOST}/",
        f"https://{HOST}/calculators.html",
        f"https://{HOST}/screener.html",
        f"https://{HOST}/articles.html",
        f"https://{HOST}/stocks/ITC",
        f"https://{HOST}/stocks/RELIANCE",
        f"https://{HOST}/stocks/TCS"
    ]
    if len(sys.argv) > 1:
        test_urls = sys.argv[1:]
    submit_urls(test_urls)
