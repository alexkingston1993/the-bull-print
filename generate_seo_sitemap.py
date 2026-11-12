"""
Programmatic Modular Sitemap Cluster & Robots.txt Generator for BullPrint Media.
Produces Google & Bing Compliant Sitemap Index with dedicated sub-sitemaps:
1. sitemap-core.xml (Calculators, Screener, Tools, Legal)
2. sitemap-stocks.xml (All Programmatic Equities)
3. sitemap-crypto.xml (Top Cryptocurrencies)
4. sitemap-articles.xml (Market Intelligence & News Archives)
5. sitemap.xml (Master Sitemap Index)
6. robots.txt (AI-friendly crawler permissions)
"""

import datetime
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_URL = "https://bullprintmedia.com"

def build_url_block(urls):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{u['loc']}</loc>")
        lines.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        lines.append(f"    <priority>{u['priority']}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines)

def generate_sitemaps():
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    
    # -------------------------------------------------------------
    # 1. Core Pages (Calculators, Tools, Screener, Legal)
    # -------------------------------------------------------------
    core_urls = [
        {"loc": f"{BASE_URL}/", "lastmod": now_iso, "changefreq": "daily", "priority": "1.0"},
        {"loc": f"{BASE_URL}/calculators", "lastmod": now_iso, "changefreq": "daily", "priority": "0.95"},
        {"loc": f"{BASE_URL}/screener", "lastmod": now_iso, "changefreq": "daily", "priority": "0.95"},
        {"loc": f"{BASE_URL}/portfolio", "lastmod": now_iso, "changefreq": "daily", "priority": "0.90"},
        {"loc": f"{BASE_URL}/crypto", "lastmod": now_iso, "changefreq": "daily", "priority": "0.90"},
        {"loc": f"{BASE_URL}/articles", "lastmod": now_iso, "changefreq": "hourly", "priority": "0.90"},
        {"loc": f"{BASE_URL}/ipo", "lastmod": now_iso, "changefreq": "daily", "priority": "0.85"},
        {"loc": f"{BASE_URL}/fno", "lastmod": now_iso, "changefreq": "daily", "priority": "0.85"},
        {"loc": f"{BASE_URL}/insurance", "lastmod": now_iso, "changefreq": "weekly", "priority": "0.80"},
        {"loc": f"{BASE_URL}/schemes", "lastmod": now_iso, "changefreq": "weekly", "priority": "0.80"},
        {"loc": f"{BASE_URL}/tools", "lastmod": now_iso, "changefreq": "weekly", "priority": "0.80"},
        {"loc": f"{BASE_URL}/unlisted", "lastmod": now_iso, "changefreq": "weekly", "priority": "0.80"},
        {"loc": f"{BASE_URL}/disclaimer", "lastmod": now_iso, "changefreq": "monthly", "priority": "0.5"},
        {"loc": f"{BASE_URL}/risk-disclosure", "lastmod": now_iso, "changefreq": "monthly", "priority": "0.5"},
        {"loc": f"{BASE_URL}/affiliate-disclosure", "lastmod": now_iso, "changefreq": "monthly", "priority": "0.5"},
        {"loc": f"{BASE_URL}/terms", "lastmod": now_iso, "changefreq": "monthly", "priority": "0.5"},
        {"loc": f"{BASE_URL}/privacy", "lastmod": now_iso, "changefreq": "monthly", "priority": "0.5"},
    ]
    with open(ROOT / "sitemap-core.xml", "w", encoding="utf-8") as f:
        f.write(build_url_block(core_urls))
    print(f"✅ Generated sitemap-core.xml ({len(core_urls)} URLs)")

    # -------------------------------------------------------------
    # 2. Programmatic Stocks (All Equities)
    # -------------------------------------------------------------
    stocks_file = ROOT / "content/stocks_database.json"
    stock_urls = []
    if stocks_file.exists():
        with open(stocks_file, "r", encoding="utf-8") as f:
            stocks_db = json.load(f)
        for sym in sorted(stocks_db.keys()):
            clean = sym.strip().upper()
            if clean:
                stock_urls.append({
                    "loc": f"{BASE_URL}/stocks/{clean}",
                    "lastmod": now_iso,
                    "changefreq": "daily",
                    "priority": "0.85"
                })
    with open(ROOT / "sitemap-stocks.xml", "w", encoding="utf-8") as f:
        f.write(build_url_block(stock_urls))
    print(f"✅ Generated sitemap-stocks.xml ({len(stock_urls)} programmatic stock URLs)")

    # -------------------------------------------------------------
    # 3. Cryptocurrency Assets
    # -------------------------------------------------------------
    crypto_file = ROOT / "content/crypto_database.json"
    crypto_urls = []
    if crypto_file.exists():
        with open(crypto_file, "r", encoding="utf-8") as f:
            crypto_db = json.load(f)
        for sym in sorted(crypto_db.keys()):
            clean = sym.strip().upper()
            if clean:
                crypto_urls.append({
                    "loc": f"{BASE_URL}/crypto/{clean}",
                    "lastmod": now_iso,
                    "changefreq": "daily",
                    "priority": "0.85"
                })
    with open(ROOT / "sitemap-crypto.xml", "w", encoding="utf-8") as f:
        f.write(build_url_block(crypto_urls))
    print(f"✅ Generated sitemap-crypto.xml ({len(crypto_urls)} crypto asset URLs)")

    # -------------------------------------------------------------
    # 4. Editorial & Market News Articles
    # -------------------------------------------------------------
    posts_file = ROOT / "content/posts.json"
    article_urls = []
    if posts_file.exists():
        with open(posts_file, "r", encoding="utf-8") as f:
            posts = json.load(f)
        for p in posts:
            slug = p.get("slug")
            if slug:
                article_urls.append({
                    "loc": f"{BASE_URL}/article/{slug}",
                    "lastmod": p.get("date", now_iso)[:10],
                    "changefreq": "weekly",
                    "priority": "0.80"
                })
    with open(ROOT / "sitemap-articles.xml", "w", encoding="utf-8") as f:
        f.write(build_url_block(article_urls))
    print(f"✅ Generated sitemap-articles.xml ({len(article_urls)} editorial articles)")

    # -------------------------------------------------------------
    # 5. Master Sitemap Index (sitemap.xml)
    # -------------------------------------------------------------
    index_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <sitemap>',
        f'    <loc>{BASE_URL}/sitemap-core.xml</loc>',
        f'    <lastmod>{now_iso}</lastmod>',
        '  </sitemap>',
        '  <sitemap>',
        f'    <loc>{BASE_URL}/sitemap-stocks.xml</loc>',
        f'    <lastmod>{now_iso}</lastmod>',
        '  </sitemap>',
        '  <sitemap>',
        f'    <loc>{BASE_URL}/sitemap-crypto.xml</loc>',
        f'    <lastmod>{now_iso}</lastmod>',
        '  </sitemap>',
        '  <sitemap>',
        f'    <loc>{BASE_URL}/sitemap-articles.xml</loc>',
        f'    <lastmod>{now_iso}</lastmod>',
        '  </sitemap>',
        '</sitemapindex>'
    ]

    robots_txt = f"""# The Bull Print - Dalal Street Market Intelligence & Financial Research
User-agent: *
Allow: /
Disallow: /admin
Disallow: /mission-control
Disallow: /api/mission-control/

# AI Crawlers & LLM Indexers Explicitly Welcomed for GEO / Perplexity / Gemini
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Bingbot
Allow: /

# Canonical Sitemaps
Sitemap: {BASE_URL}/sitemap.xml
Sitemap: {BASE_URL}/sitemap-core.xml
Sitemap: {BASE_URL}/sitemap-stocks.xml
Sitemap: {BASE_URL}/sitemap-crypto.xml
Sitemap: {BASE_URL}/sitemap-articles.xml
"""

    for fname, data in [
        ("sitemap-core.xml", build_url_block(core_urls)),
        ("sitemap-stocks.xml", build_url_block(stock_urls)),
        ("sitemap-crypto.xml", build_url_block(crypto_urls)),
        ("sitemap-articles.xml", build_url_block(article_urls)),
        ("sitemap.xml", "\n".join(index_lines)),
        ("robots.txt", robots_txt)
    ]:
        with open(ROOT / fname, "w", encoding="utf-8") as f:
            f.write(data)
        pub = ROOT / "public"
        if pub.exists():
            with open(pub / fname, "w", encoding="utf-8") as f:
                f.write(data)
    print("✅ Generated AI-optimized robots.txt")

if __name__ == "__main__":
    generate_sitemaps()
