#!/usr/bin/env python3
"""
SEO, AEO, Schema & Analytics Injector for BullPrint Media Core Pages.
Ensures uniform Google Analytics 4, Search Engine Verification (GSC & Bing),
high-intent CTR titles, meta descriptions, and structured JSON-LD schemas.
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

GA_SNIPPET = """    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BULLPRINT"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-BULLPRINT', { 'anonymize_ip': true });
    </script>
    <!-- Search Engine Verification -->
    <meta name="google-site-verification" content="google-site-verification-token">
    <meta name="msvalidate.01" content="4f29a7d83e204c329b45667e8125ac89">
"""

PAGES_CONFIG = {
    "calculators.html": {
        "title": "Free Financial Calculators — SIP, Step-Up, Compound Interest, CAGR & Loan EMI | The Bull Print",
        "description": "Institutional financial calculators for Mutual Funds SIP compound interest, Step-Up wealth planning, Car vs Wealth comparison, Loan EMIs, and Lumpsum investment projections.",
        "canonical": "https://bullprintmedia.com/calculators",
        "schema": """    <!-- Structured JSON-LD Schema: Financial Calculators Suite -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "The Bull Print Financial Calculators Suite",
      "url": "https://bullprintmedia.com/calculators",
      "description": "Suite of free financial compounding calculators for Indian investors including SIP Step-Up, Compound Interest, CAGR, and Loan EMI.",
      "applicationCategory": "FinanceApplication",
      "operatingSystem": "All",
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "INR"
      },
      "publisher": {
        "@type": "Organization",
        "name": "The Bull Print",
        "url": "https://bullprintmedia.com/"
      }
    }
    </script>"""
    },
    "screener.html": {
        "title": "NSE Stock Screener — Fundamental Value, High ROCE & Debt-Free Indian Equities | The Bull Print",
        "description": "Institutional-grade Indian equity screener: Coffee Can portfolio, Piotroski F-Score scan, Magic Formula, Debt-Free titans, and 30+ sector screeners.",
        "canonical": "https://bullprintmedia.com/screener",
        "schema": """    <!-- Structured JSON-LD Schema: Stock Screener Application -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "The Bull Print Fundamental Stock Screener",
      "url": "https://bullprintmedia.com/screener",
      "description": "Quantitative fundamental stock screener for Indian listed equities on NSE and BSE.",
      "applicationCategory": "FinanceApplication",
      "operatingSystem": "All",
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "INR"
      }
    }
    </script>"""
    },
    "articles.html": {
        "title": "Dalal Street Market News, Fundamental Equity Analysis & Macro Intelligence | The Bull Print",
        "description": "In-depth institutional equity research, quarterly corporate earnings teardowns, FII/DII flow breakdowns, and everyday wealth compounding guides.",
        "canonical": "https://bullprintmedia.com/articles",
        "schema": """    <!-- Structured JSON-LD Schema: News Media Collection -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "The Bull Print Market Research & Editorial Archives",
      "url": "https://bullprintmedia.com/articles",
      "description": "Curated collection of in-depth Indian equity research and global macro intelligence reports.",
      "publisher": {
        "@type": "NewsMediaOrganization",
        "name": "The Bull Print",
        "url": "https://bullprintmedia.com/"
      }
    }
    </script>"""
    },
    "crypto.html": {
        "title": "Cryptocurrency Market Cap, Live Prices, Charts & Indian VDA 30% Tax Audit | The Bull Print",
        "description": "Live cryptocurrency market cap rankings, real-time prices, 24h volume, circulating supply, sparkline charts, and Section 115BBH Indian crypto tax intelligence.",
        "canonical": "https://bullprintmedia.com/crypto",
        "schema": """    <!-- Structured JSON-LD Schema: Crypto Market Intelligence -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "The Bull Print Cryptocurrency Terminal",
      "url": "https://bullprintmedia.com/crypto",
      "description": "Real-time cryptocurrency market intelligence, tokenomics audit, and Indian VDA tax calculator.",
      "applicationCategory": "FinanceApplication",
      "operatingSystem": "All",
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "INR"
      }
    }
    </script>"""
    },
    "portfolio.html": {
        "title": "Portfolio Health Check & Risk Audit — Institutional Asset Allocation Modeler | The Bull Print",
        "description": "Audit your investment portfolio against institutional risk parameters, sector diversification benchmarks, and asset allocation compounding models.",
        "canonical": "https://bullprintmedia.com/portfolio",
        "schema": """    <!-- Structured JSON-LD Schema: Portfolio Health Check -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "The Bull Print Portfolio Health Check & Risk Modeler",
      "url": "https://bullprintmedia.com/portfolio",
      "description": "Institutional portfolio audit tool for sector diversification, downside protection, and wealth compounding.",
      "applicationCategory": "FinanceApplication",
      "operatingSystem": "All",
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "INR"
      }
    }
    </script>"""
    }
}

def update_page(filename, conf):
    path = ROOT / filename
    if not path.exists():
        print(f"Skipping {filename}: Not found")
        return
        
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update Title
    title_pattern = r"<title>(.*?)</title>"
    if re.search(title_pattern, content):
        content = re.sub(title_pattern, f"<title>{conf['title']}</title>", content, count=1)

    # 2. Update Meta Description
    desc_pattern = r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']>'
    desc = conf['description']
    canon = conf['canonical']
    if re.search(desc_pattern, content):
        content = re.sub(desc_pattern, f'<meta name="description" content="{desc}">', content, count=1)

    # 3. Update Canonical Link
    canon_pattern = r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']>'
    if re.search(canon_pattern, content):
        content = re.sub(canon_pattern, f'<link rel="canonical" href="{canon}">', content, count=1)

    # 4. Inject GA4 and verification if not already present
    if "G-BULLPRINT" not in content and "<head>" in content:
        content = content.replace("<head>", f"<head>\n{GA_SNIPPET}\n{conf['schema']}\n", 1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ Updated SEO, Schema, and Analytics for {filename}")

def main():
    print("=" * 80)
    print("🚀 INJECTING SEO, AEO, GA4 & STRUCTURED SCHEMAS ACROSS CORE PAGES")
    print("=" * 80)
    for fname, conf in PAGES_CONFIG.items():
        update_page(fname, conf)
    print("\nAll core pages optimized!")

if __name__ == "__main__":
    main()
