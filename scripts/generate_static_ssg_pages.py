#!/usr/bin/env python3
"""
High-Performance Static Site Generator (SSG) for The Bull Print
Generates 100% pre-rendered, lightning-fast, zero-JS-dependent static HTML pages for:
1. All 2,643 NSE Listed Stocks (public/stocks/:symbol/index.html & public/stocks/:symbol.html)
2. All 1,000 Top Cryptocurrencies (public/crypto/:symbol/index.html & public/crypto/:symbol.html)
"""

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

USD_INR_RATE = 86.80

GLOBAL_FOOTER_HTML = """
    <footer class="site-footer" style="background:#0f172a; color:#94a3b8; border-top:1px solid #1e293b; padding:48px 24px 32px 24px; margin-top:60px;">
        <div style="max-width:1440px; margin:0 auto; display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:32px; margin-bottom:36px;">
            <div>
                <h4 style="font-family:'Outfit',sans-serif; font-size:14px; text-transform:uppercase; letter-spacing:0.05em; color:#f8fafc; margin-bottom:14px;">🇮🇳 Dalal Street Giants</h4>
                <div style="display:flex; flex-direction:column; gap:8px; font-size:13px;">
                    <a href="/stocks/RELIANCE" style="color:#94a3b8; text-decoration:none;">Reliance Industries (RELIANCE)</a>
                    <a href="/stocks/TCS" style="color:#94a3b8; text-decoration:none;">Tata Consultancy Services (TCS)</a>
                    <a href="/stocks/HDFCBANK" style="color:#94a3b8; text-decoration:none;">HDFC Bank (HDFCBANK)</a>
                    <a href="/stocks/BHARTIARTL" style="color:#94a3b8; text-decoration:none;">Bharti Airtel (BHARTIARTL)</a>
                    <a href="/stocks/INFY" style="color:#94a3b8; text-decoration:none;">Infosys (INFY)</a>
                    <a href="/stocks/ICICIBANK" style="color:#94a3b8; text-decoration:none;">ICICI Bank (ICICIBANK)</a>
                    <a href="/stocks/SBIN" style="color:#94a3b8; text-decoration:none;">State Bank of India (SBIN)</a>
                    <a href="/stocks/ITC" style="color:#94a3b8; text-decoration:none;">ITC Ltd (ITC)</a>
                    <a href="/stocks/TATAMOTORS" style="color:#94a3b8; text-decoration:none;">Tata Motors (TATAMOTORS)</a>
                    <a href="/stocks/ZOMATO" style="color:#94a3b8; text-decoration:none;">Zomato Ltd (ZOMATO)</a>
                    <a href="/stocks" style="color:#00d09c; font-weight:700; text-decoration:none;">View All 2,640+ Stocks →</a>
                </div>
            </div>
            <div>
                <h4 style="font-family:'Outfit',sans-serif; font-size:14px; text-transform:uppercase; letter-spacing:0.05em; color:#f8fafc; margin-bottom:14px;">🌐 Institutional Digital Assets</h4>
                <div style="display:flex; flex-direction:column; gap:8px; font-size:13px;">
                    <a href="/crypto/BTC" style="color:#94a3b8; text-decoration:none;">Bitcoin (BTC) Price & Tax Audit</a>
                    <a href="/crypto/ETH" style="color:#94a3b8; text-decoration:none;">Ethereum (ETH) Tokenomics</a>
                    <a href="/crypto/SOL" style="color:#94a3b8; text-decoration:none;">Solana (SOL) Candlestick Chart</a>
                    <a href="/crypto/BNB" style="color:#94a3b8; text-decoration:none;">BNB Chain (BNB) Analysis</a>
                    <a href="/crypto/XRP" style="color:#94a3b8; text-decoration:none;">XRP (Ripple) Settlement</a>
                    <a href="/crypto/DOGE" style="color:#94a3b8; text-decoration:none;">Dogecoin (DOGE) Meme Audit</a>
                    <a href="/crypto/ADA" style="color:#94a3b8; text-decoration:none;">Cardano (ADA) Formal Proofs</a>
                    <a href="/crypto/SUI" style="color:#94a3b8; text-decoration:none;">Sui (SUI) Move Layer 1</a>
                    <a href="/crypto/TAO" style="color:#94a3b8; text-decoration:none;">Bittensor (TAO) Decentralized AI</a>
                    <a href="/crypto/RENDER" style="color:#94a3b8; text-decoration:none;">Render (RENDER) GPU Compute</a>
                    <a href="/crypto" style="color:#00d09c; font-weight:700; text-decoration:none;">View Top 1,000 Cryptos →</a>
                </div>
            </div>
            <div>
                <h4 style="font-family:'Outfit',sans-serif; font-size:14px; text-transform:uppercase; letter-spacing:0.05em; color:#f8fafc; margin-bottom:14px;">🛠️ Financial Tools & Radars</h4>
                <div style="display:flex; flex-direction:column; gap:8px; font-size:13px;">
                    <a href="/screener" style="color:#94a3b8; text-decoration:none;">NSE 10-Year Fundamental Screener</a>
                    <a href="/crypto-radar" style="color:#ff5252; font-weight:700; text-decoration:none;">🚀 New Crypto Projects Launchpad</a>
                    <a href="/calculators" style="color:#94a3b8; text-decoration:none;">Compounding & SIP Calculators</a>
                    <a href="/fno" style="color:#94a3b8; text-decoration:none;">Options & F&O Open Interest Radar</a>
                    <a href="/portfolio" style="color:#94a3b8; text-decoration:none;">Institutional Portfolio Tracker</a>
                    <a href="/ipo" style="color:#94a3b8; text-decoration:none;">Mainboard & SME IPO Calendar</a>
                    <a href="/unlisted" style="color:#94a3b8; text-decoration:none;">Pre-IPO & Unlisted Shares Desk</a>
                    <a href="/insurance" style="color:#94a3b8; text-decoration:none;">Health & Term Insurance Guide</a>
                </div>
            </div>
            <div>
                <h4 style="font-family:'Outfit',sans-serif; font-size:14px; text-transform:uppercase; letter-spacing:0.05em; color:#f8fafc; margin-bottom:14px;">⚖️ Statutory & Compliance</h4>
                <div style="display:flex; flex-direction:column; gap:8px; font-size:13px;">
                    <a href="/disclaimer" style="color:#94a3b8; text-decoration:none;">SEBI Research Analyst Disclaimer</a>
                    <a href="/risk-disclosure" style="color:#94a3b8; text-decoration:none;">Equity & Derivatives Risk Notice</a>
                    <a href="/privacy" style="color:#94a3b8; text-decoration:none;">Privacy Policy & Data Security</a>
                    <a href="/terms" style="color:#94a3b8; text-decoration:none;">Terms of Service & Usage</a>
                    <a href="/security.txt" style="color:#94a3b8; text-decoration:none;">Security Disclosure Policy</a>
                    <p style="font-size:11.5px; color:#64748b; margin-top:10px; line-height:1.5;">
                        The Bull Print provides educational market intelligence, on-chain telemetry, and observational analysis. Not registered under SEBI (Research Analyst) Regulations, 2014.
                    </p>
                </div>
            </div>
        </div>
        <div style="max-width:1440px; margin:0 auto; padding-top:24px; border-top:1px solid #1e293b; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; font-size:12px; color:#64748b;">
            <div>© 2026 The Bull Print Media Desk. All rights reserved.</div>
            <div>Canonical Sitemaps: <a href="/sitemap-stocks.xml" style="color:#64748b;">Stocks XML</a> · <a href="/sitemap-crypto.xml" style="color:#64748b;">Crypto XML</a> · <a href="/sitemap-articles.xml" style="color:#64748b;">Articles XML</a></div>
        </div>
    </footer>
"""

GLOBAL_NAVBAR_HTML = """
    <header style="position:sticky; top:0; z-index:100; background:rgba(11,14,20,0.92); backdrop-filter:blur(12px); border-bottom:1px solid #222733; padding:0 24px;">
        <div style="max-width:1440px; margin:0 auto; height:64px; display:flex; align-items:center; justify-content:space-between; gap:20px;">
            <a href="/" style="display:flex; align-items:center; gap:10px; text-decoration:none;">
                <img src="/brand_assets/website_favicon_192x192.png" alt="Logo" style="width:34px; height:34px; border-radius:8px;">
                <span style="font-family:'Outfit',sans-serif; font-size:18px; font-weight:800; letter-spacing:-0.02em; color:#f8fafc;">THE BULL <span style="color:#00d09c;">PRINT</span></span>
            </a>
            <nav style="display:flex; align-items:center; gap:6px; overflow-x:auto;">
                <a href="/" style="text-decoration:none; color:#94a3b8; font-size:13.5px; font-weight:500; padding:6px 12px; border-radius:8px;">Dashboard</a>
                <a href="/screener" style="text-decoration:none; color:#94a3b8; font-size:13.5px; font-weight:500; padding:6px 12px; border-radius:8px;">Screener</a>
                <a href="/stocks" style="text-decoration:none; color:#00d09c; font-size:13.5px; font-weight:500; padding:6px 12px; border-radius:8px; background:rgba(0,208,156,0.12);">Stocks (2,640+)</a>
                <a href="/articles" style="text-decoration:none; color:#94a3b8; font-size:13.5px; font-weight:500; padding:6px 12px; border-radius:8px;">Articles</a>
                <a href="/crypto" style="text-decoration:none; color:#94a3b8; font-size:13.5px; font-weight:500; padding:6px 12px; border-radius:8px;">Crypto (1,000)</a>
                <a href="/crypto-radar" style="text-decoration:none; color:#ff5252; font-size:13.5px; font-weight:700; padding:6px 12px; border-radius:8px; background:rgba(234,57,67,0.15); border:1px solid rgba(234,57,67,0.3);">🚀 New Radar</a>
                <a href="/calculators" style="text-decoration:none; color:#94a3b8; font-size:13.5px; font-weight:500; padding:6px 12px; border-radius:8px;">Calculators</a>
            </nav>
        </div>
    </header>
"""

SHARED_CSS = """
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background-color: #0b0e14; color: #f8fafc; font-family: 'Inter', -apple-system, sans-serif; line-height: 1.5; -webkit-font-smoothing: antialiased; }
    .container { max-width: 1440px; margin: 0 auto; padding: 24px 20px; }
    .card { background: #151921; border: 1px solid #222733; border-radius: 12px; padding: 24px; margin-bottom: 24px; }
    .pill { display: inline-block; font-size: 11.5px; font-family: 'JetBrains Mono', monospace; font-weight: 600; padding: 3px 10px; border-radius: 20px; background: #1e232d; border: 1px solid #313848; color: #94a3b8; }
    .pill-green { background: rgba(0,208,156,0.15); color: #00d09c; border-color: #00d09c; }
    .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }
    .metric-card { background: #151921; border: 1px solid #222733; border-radius: 10px; padding: 16px 20px; }
    .metric-label { font-size: 11px; text-transform: uppercase; font-family: 'JetBrains Mono', monospace; color: #64748b; margin-bottom: 4px; }
    .metric-val { font-size: 18px; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: #f8fafc; }
    .metric-sub { font-size: 11.5px; color: #94a3b8; margin-top: 2px; }
    .badge-up { color: #16c784; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
    .badge-down { color: #ea3943; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
    .table-wrap { overflow-x: auto; margin-top: 16px; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; }
    th { padding: 10px 14px; background: #1e232d; border-bottom: 1px solid #222733; color: #64748b; font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase; white-space: nowrap; }
    td { padding: 12px 14px; border-bottom: 1px solid #222733; white-space: nowrap; }
    tr:hover td { background: #1a202c; }
    .breadcrumb-nav { margin-bottom: 16px; font-size: 13px; color: #64748b; }
    .breadcrumb-nav a { color: #94a3b8; text-decoration: none; }
    .breadcrumb-nav a:hover { color: #00d09c; }
"""

def build_table_from_dict(title, data_obj):
    if not isinstance(data_obj, dict) or 'columns' not in data_obj or 'rows' not in data_obj:
        return ""
    cols = data_obj.get('columns', [])
    rows = data_obj.get('rows', [])
    if not cols or not rows:
        return ""
    html = f"<div class='card'><h2 style=\"font-family:'Outfit',sans-serif; font-size:20px; font-weight:700; margin-bottom:12px;\">{title}</h2><div class='table-wrap'><table><thead><tr><th>Metric</th>"
    for c in cols:
        html += f"<th>{c}</th>"
    html += "</tr></thead><tbody>"
    for r in rows:
        html += f"<tr><td><strong>{r.get('name', '')}</strong></td>"
        for v in r.get('values', []):
            html += f"<td>{v}</td>"
        html += "</tr>"
    html += "</tbody></table></div></div>"
    return html

def generate_stock_html(stock):
    sym = stock["symbol"]
    name = stock.get("name", sym)
    sector = stock.get("sector", "Diversified Equity")
    cat = stock.get("category", "Listed Equity")
    isin = stock.get("isin", "")
    raw_cmp = stock.get("cmp", 0.0)
    try:
        cmp = float(str(raw_cmp).replace(',', ''))
    except:
        cmp = 0.0
    raw_mcap = stock.get("mcap", 0.0)
    try:
        mcap = float(str(raw_mcap).replace(',', ''))
    except:
        mcap = 0.0
    pe = stock.get("pe", 22.0)
    ind_pe = stock.get("industryPe", 24.0)
    roce = stock.get("roce", 14.5)
    roe = stock.get("roe", 12.8)
    d2e = stock.get("debtToEquity", 0.25)
    high_low = stock.get("highLow", "0.00 / 0.00")
    about = stock.get("about", f"{name} ({sym}) is an active publicly traded Indian corporation listed on the National Stock Exchange of India.")
    exec_summary = stock.get("executiveSummary", f"{name} ({sym}) evaluated under The Bull Print institutional fundamental framework.")
    pros = stock.get("pros", ["Actively listed constituent on the National Stock Exchange.", f"Exposure to Indian {sector} growth.", "Regulatory compliance under SEBI LODR."])
    cons = stock.get("cons", [f"Cyclical demand risks in {sector}.", "Raw material price inflation."])
    
    q_table_html = build_table_from_dict("Quarterly Operating Performance", stock.get("quarterlyResults"))
    pnl_table_html = build_table_from_dict("10-Year Profit & Loss Trajectory", stock.get("profitAndLoss"))
    bs_table_html = build_table_from_dict("10-Year Balance Sheet Compounding", stock.get("balanceSheet"))
    cf_table_html = build_table_from_dict("10-Year Cash Flow Statement", stock.get("cashFlows"))

    schema_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Corporation",
                "name": name,
                "tickerSymbol": f"NSE:{sym}",
                "url": f"https://bullprintmedia.com/stocks/{sym}",
                "description": about
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://bullprintmedia.com/" },
                    { "@type": "ListItem", "position": 2, "name": "NSE Stocks", "item": "https://bullprintmedia.com/stocks" },
                    { "@type": "ListItem", "position": 3, "name": f"{name} ({sym})", "item": f"https://bullprintmedia.com/stocks/{sym}" }
                ]
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"What is the P/E ratio and ROCE of {name} ({sym})?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"{name} trades at a P/E multiple of {pe} (Industry P/E: {ind_pe}) with a Return on Capital Employed (ROCE) of {roce}% and Return on Equity (ROE) of {roe}%."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"What is the debt to equity ratio of {name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"{name} has a Debt to Equity ratio of {d2e}, evaluated under The Bull Print balance sheet stress-testing framework."
                        }
                    }
                ]
            }
        ]
    }, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} ({sym}) Share Price, 10-Yr Financial Statements, ROCE & Screener | The Bull Print</title>
    <meta name="description" content="Complete institutional fundamental research on {name} (NSE: {sym}). Real-time share price, 10-year balance sheet, P&L, quarterly results, promoter pledge audit, and ROCE trajectory.">
    <link rel="canonical" href="https://bullprintmedia.com/stocks/{sym}">
    <meta property="og:title" content="{name} ({sym}) Fundamentals & Balance Sheet | The Bull Print">
    <meta property="og:description" content="10-year Screener.in grade financial statements, ROCE, and promoter shareholding audit for {name}.">
    <meta property="og:image" content="/brand_assets/opengraph_social_card_1200x630.png">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" type="image/png" sizes="32x32" href="/brand_assets/website_favicon_32x32.png">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">

    <!-- Schema.org JSON-LD -->
    <script type="application/ld+json">
{schema_jsonld}
    </script>

    <style>
{SHARED_CSS}
    </style>
</head>
<body>
{GLOBAL_NAVBAR_HTML}

    <main class="container">
        <!-- Breadcrumb -->
        <div class="breadcrumb-nav">
            <a href="/">Home</a> / <a href="/stocks">NSE Equities</a> / <a href="/stocks">{sector}</a> / <span style="color:#f8fafc;">{name} ({sym})</span>
        </div>

        <!-- Hero Header -->
        <div class="card" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;">
            <div>
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                    <h1 style="font-family:'Outfit',sans-serif; font-size:28px; font-weight:800; letter-spacing:-0.02em;">{name}</h1>
                    <span class="pill pill-green">NSE: {sym}</span>
                </div>
                <div style="display:flex; gap:8px; flex-wrap:wrap;">
                    <span class="pill">{sector}</span>
                    <span class="pill">{cat}</span>
                    {f'<span class="pill">ISIN: {isin}</span>' if isin else ''}
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:32px; font-weight:800;" id="hero-ltp">₹ {cmp if cmp > 0 else 'Fetching Live...'}</div>
                <div style="font-size:12px; color:#94a3b8; font-family:'JetBrains Mono',monospace;">52W Range: {high_low}</div>
            </div>
        </div>

        <!-- Metrics Grid -->
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Market Capitalization</div>
                <div class="metric-val">₹ {mcap:,.0f} Cr</div>
                <div class="metric-sub">{cat} constituent</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Stock P/E vs Industry P/E</div>
                <div class="metric-val">{pe} / {ind_pe}</div>
                <div class="metric-sub">Valuation Multiple</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">ROCE / ROE</div>
                <div class="metric-val">{roce}% / {roe}%</div>
                <div class="metric-sub">Capital Efficiency</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Debt to Equity</div>
                <div class="metric-val">{d2e}</div>
                <div class="metric-sub">Balance Sheet Leverage</div>
            </div>
        </div>

        <!-- TradingView Chart -->
        <div class="card" style="padding:0; overflow:hidden;">
            <div style="padding:16px 20px; border-bottom:1px solid #222733; display:flex; justify-content:space-between; align-items:center;">
                <strong style="font-family:'Outfit',sans-serif;">{name} Live Candlestick & Volume Stream</strong>
                <span style="font-size:12px; color:#64748b; font-family:'JetBrains Mono',monospace;">Direct Exchange Feed</span>
            </div>
            <div style="height:500px; width:100%;">
                <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_stock&symbol=NSE%3A{sym}&interval=1D&hidesidetoolbar=0&symboledit=1&saveimage=0&toolbarbg=f1f3f6&studies=[]&theme=dark&style=1&timezone=Asia%2FKolkata&studies_overrides={{}}&overrides={{}}&enabled_features=[]&disabled_features=[]&locale=en" 
                width="100%" height="100%" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
            </div>
        </div>

        <!-- AI Moat Breakdown -->
        <div class="card">
            <h2 style="font-family:'Outfit',sans-serif; font-size:20px; font-weight:700; margin-bottom:12px;">🧠 The Bull Print Institutional Analysis</h2>
            <p style="font-size:14.5px; line-height:1.7; color:#94a3b8; margin-bottom:16px;">{exec_summary}</p>
            <p style="font-size:14px; line-height:1.6; color:#64748b;">{about}</p>
        </div>

        <!-- Pros and Cons -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:20px; margin-bottom:24px;">
            <div class="card" style="margin-bottom:0;">
                <h3 style="font-family:'Outfit',sans-serif; font-size:16px; font-weight:700; color:#16c784; margin-bottom:12px;">✓ Core Fundamental Catalysts</h3>
                <ul style="list-style:none; display:flex; flex-direction:column; gap:8px;">
                    {''.join([f'<li style="font-size:13.5px; color:#94a3b8;">✓ {p}</li>' for p in pros])}
                </ul>
            </div>
            <div class="card" style="margin-bottom:0;">
                <h3 style="font-family:'Outfit',sans-serif; font-size:16px; font-weight:700; color:#ea3943; margin-bottom:12px;">⚠ Structural Headwinds & Risks</h3>
                <ul style="list-style:none; display:flex; flex-direction:column; gap:8px;">
                    {''.join([f'<li style="font-size:13.5px; color:#94a3b8;">⚠ {c}</li>' for c in cons])}
                </ul>
            </div>
        </div>

        {q_table_html}
        {pnl_table_html}
        {bs_table_html}
        {cf_table_html}

    </main>

{GLOBAL_FOOTER_HTML}

    <!-- Live Quote Hydration for Interactive Users -->
    <script>
        async function fetchLive() {{
            try {{
                const res = await fetch(`/api/quote?symbol={sym}`);
                if (res.ok) {{
                    const d = await res.json();
                    if (d.success && d.price) {{
                        document.getElementById('hero-ltp').textContent = '₹ ' + d.price.toLocaleString('en-IN', {{ minimumFractionDigits: 2 }});
                    }}
                }}
            }} catch(e) {{}}
        }}
        fetchLive();
        setInterval(fetchLive, 5000);
    </script>
</body>
</html>
"""

def generate_crypto_html(coin):
    sym = coin["symbol"]
    name = coin.get("name", sym)
    rank = coin.get("rank", "-")
    cat = coin.get("category", "Decentralized Asset")
    consensus = coin.get("consensus", "Smart Contract")
    price_usd = coin.get("priceUSD", 1.0)
    price_inr = price_usd * USD_INR_RATE
    chg = coin.get("chg24h", 0.0)
    vol = coin.get("vol24hUSD", 1000000)
    mcap = coin.get("mcapUSD", vol * 10)
    mcap_inr = (mcap * USD_INR_RATE) / 10000000
    supply = coin.get("supply", f"{sym}")
    max_supply = coin.get("max_supply", "Dynamic Supply")
    tv_sym = coin.get("tvSym", f"BINANCE:{sym}USDT")
    tech_moat = coin.get("tech_moat", f"{name} ({sym}) is an established protocol constituent.")
    tax_audit = coin.get("tax_audit", f"Under Section 115BBH: Net capital gains from {sym} are taxed at a flat 30% plus 4% cess (31.2%). 1% TDS under Section 194S.")
    pros = coin.get("pros", ["Actively traded on global tier-1 exchanges.", "Decentralized smart contract validation."])
    price_str_usd = f"{price_usd:,.2f}" if price_usd >= 1 else f"{price_usd:.4f}"
    price_str_inr = f"{price_inr:,.2f}" if price_inr >= 1 else f"{price_inr:.4f}"
    badge_cls = 'badge-up' if chg >= 0 else 'badge-down'
    arrow = '▲' if chg >= 0 else '▼'

    cons = coin.get("cons", ["Macroeconomic price volatility.", "Section 115BBH Indian tax compliance."])

    schema_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "FinancialProduct",
                "name": f"{name} ({sym})",
                "category": cat,
                "url": f"https://bullprintmedia.com/crypto/{sym}",
                "offers": {
                    "@type": "Offer",
                    "price": price_usd,
                    "priceCurrency": "USD"
                }
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://bullprintmedia.com/" },
                    { "@type": "ListItem", "position": 2, "name": "Cryptocurrencies", "item": "https://bullprintmedia.com/crypto" },
                    { "@type": "ListItem", "position": 3, "name": f"{name} ({sym})", "item": f"https://bullprintmedia.com/crypto/{sym}" }
                ]
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"How is {name} ({sym}) taxed in India under Section 115BBH?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Gains from {name} ({sym}) are subject to a flat 30% tax plus 4% cess (effective 31.2%) under Section 115BBH of the Indian Income Tax Act. Zero set-off against other crypto losses is permitted. 1% TDS applies under Section 194S."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"What is the maximum and circulating supply of {name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"{name} has a circulating supply of {supply} and maximum limit of {max_supply}."
                        }
                    }
                ]
            }
        ]
    }, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} ({sym}) Live Price, Candlestick Chart, Tokenomics & Indian Section 115BBH Tax Audit | The Bull Print</title>
    <meta name="description" content="Institutional digital asset analysis of {name} ({sym}). Real-time live prices in USD and INR, TradingView candlestick charts, tokenomics supply breakdown, AI moat breakdown, and Section 115BBH Indian crypto 30% tax audit.">
    <link rel="canonical" href="https://bullprintmedia.com/crypto/{sym}">
    <meta property="og:title" content="{name} ({sym}) Live Price, Chart & Tax Audit | The Bull Print">
    <meta property="og:description" content="Live price in USD and INR, tokenomics, and Indian Section 115BBH 30% flat tax audit for {name} ({sym}).">
    <meta property="og:image" content="/brand_assets/opengraph_social_card_1200x630.png">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" type="image/png" sizes="32x32" href="/brand_assets/website_favicon_32x32.png">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">

    <!-- Schema.org JSON-LD -->
    <script type="application/ld+json">
{schema_jsonld}
    </script>

    <style>
{SHARED_CSS}
    </style>
</head>
<body>
{GLOBAL_NAVBAR_HTML}

    <main class="container">
        <!-- Breadcrumbs -->
        <div class="breadcrumb-nav">
            <a href="/">Home</a> / <a href="/crypto">Cryptocurrencies</a> / <a href="/crypto">{cat}</a> / <span style="color:#f8fafc;">{name} ({sym})</span>
        </div>

        <!-- Hero Header -->
        <div class="card" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;">
            <div style="display:flex; align-items:center; gap:16px;">
                <div style="width:52px; height:52px; border-radius:50%; background:#1e232d; border:2px solid #00d09c; display:flex; align-items:center; justify-content:center; font-size:20px; font-weight:800; font-family:'JetBrains Mono',monospace; color:#00d09c;">
                    {sym[:3]}
                </div>
                <div>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <h1 style="font-family:'Outfit',sans-serif; font-size:28px; font-weight:800; letter-spacing:-0.02em;">{name}</h1>
                        <span class="pill pill-green">Rank #{rank}</span>
                    </div>
                    <div style="display:flex; gap:8px; margin-top:6px; flex-wrap:wrap;">
                        <span class="pill">{sym}</span>
                        <span class="pill">{cat}</span>
                        <span class="pill">{consensus}</span>
                    </div>
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:32px; font-weight:800;">$ {price_str_usd}</div>
                <div style="font-size:16px; color:#94a3b8; font-family:'JetBrains Mono',monospace;">₹ {price_str_inr}</div>
                <div style="margin-top:4px;"><span class="{badge_cls}">{arrow} {abs(chg):.2f}% (24h)</span></div>
            </div>
        </div>

        <!-- Metrics Grid -->
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Market Capitalization</div>
                <div class="metric-val">$ {mcap/1000000000:.2f}B</div>
                <div class="metric-sub">₹ {mcap_inr:,.0f} Cr</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">24h Trading Volume</div>
                <div class="metric-val">$ {vol/1000000:.2f}M</div>
                <div class="metric-sub">High Liquidity</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Circulating Supply</div>
                <div class="metric-val">{supply}</div>
                <div class="metric-sub">Verified Float</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Maximum Supply</div>
                <div class="metric-val">{max_supply}</div>
                <div class="metric-sub">Emission Protocol</div>
            </div>
        </div>

        <!-- TradingView Chart -->
        <div class="card" style="padding:0; overflow:hidden;">
            <div style="padding:16px 20px; border-bottom:1px solid #222733; display:flex; justify-content:space-between; align-items:center;">
                <strong style="font-family:'Outfit',sans-serif;">{name} Multi-Timeframe Candlestick & Volume Stream</strong>
                <span style="font-size:12px; color:#64748b; font-family:'JetBrains Mono',monospace;">Binance High-Liquidity Feed</span>
            </div>
            <div style="height:500px; width:100%;">
                <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_crypto&symbol={tv_sym}&interval=1D&hidesidetoolbar=0&symboledit=1&saveimage=0&toolbarbg=f1f3f6&studies=[]&theme=dark&style=1&timezone=Asia%2FKolkata&studies_overrides={{}}&overrides={{}}&enabled_features=[]&disabled_features=[]&locale=en" 
                width="100%" height="100%" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
            </div>
        </div>

        <!-- Indian Section 115BBH VDA Tax Card -->
        <div class="card" style="border:2px solid rgba(234,57,67,0.4);">
            <div style="display:inline-block; background:rgba(234,57,67,0.15); color:#ea3943; font-size:11px; font-weight:800; font-family:'JetBrains Mono',monospace; padding:4px 10px; border-radius:4px; text-transform:uppercase; margin-bottom:12px;">
                🇮🇳 Statutory Compliance Audit · Indian Income Tax Act
            </div>
            <h2 style="font-family:'Outfit',sans-serif; font-size:20px; margin-bottom:10px;">Section 115BBH 30% Flat Tax & Section 194S 1% TDS Audit</h2>
            <p style="font-size:14.5px; line-height:1.7; color:#94a3b8; margin-bottom:18px;">{tax_audit}</p>
            <div style="background:#1e232d; border:1px solid #222733; border-radius:8px; padding:16px 20px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
                <div>
                    <span style="font-size:12px; color:#64748b; display:block;">Simulate Net Profit of ₹ 1,00,000 in {sym}:</span>
                    <strong style="font-size:14px; color:#f8fafc;">Mandatory 31.2% Tax Payable:</strong>
                </div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:24px; font-weight:800; color:#ea3943;">₹ 31,200</div>
            </div>
        </div>

        <!-- AI Moat Breakdown -->
        <div class="card">
            <h2 style="font-family:'Outfit',sans-serif; font-size:20px; font-weight:700; margin-bottom:12px;">🧠 The Bull Print Institutional Protocol Analysis</h2>
            <p style="font-size:14.5px; line-height:1.7; color:#94a3b8;">{tech_moat}</p>
        </div>

        <!-- Pros and Cons -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:20px; margin-bottom:24px;">
            <div class="card" style="margin-bottom:0;">
                <h3 style="font-family:'Outfit',sans-serif; font-size:16px; font-weight:700; color:#16c784; margin-bottom:12px;">✓ Institutional Strengths & Catalysts</h3>
                <ul style="list-style:none; display:flex; flex-direction:column; gap:8px;">
                    {''.join([f'<li style="font-size:13.5px; color:#94a3b8;">✓ {p}</li>' for p in pros])}
                </ul>
            </div>
            <div class="card" style="margin-bottom:0;">
                <h3 style="font-family:'Outfit',sans-serif; font-size:16px; font-weight:700; color:#ea3943; margin-bottom:12px;">⚠ Structural Risks & Headwinds</h3>
                <ul style="list-style:none; display:flex; flex-direction:column; gap:8px;">
                    {''.join([f'<li style="font-size:13.5px; color:#94a3b8;">⚠ {c}</li>' for c in cons])}
                </ul>
            </div>
        </div>

    </main>

{GLOBAL_FOOTER_HTML}
</body>
</html>
"""

def main():
    start_time = time.time()
    print("🚀 STARTING STATIC SITE GENERATION (SSG) FOR ALL STOCKS & CRYPTOS")

    # 1. Load Databases
    with open(ROOT / "public/content/stocks_database.json", "r", encoding="utf-8") as f:
        stocks_db = json.load(f)
    print(f"Loaded {len(stocks_db)} stock records.")

    with open(ROOT / "public/content/crypto_database.json", "r", encoding="utf-8") as f:
        crypto_db = json.load(f)
    print(f"Loaded {len(crypto_db)} crypto records.")

    # 2. Generate Stock Static HTMLs
    stocks_dir = ROOT / "public/stocks"
    stocks_dir.mkdir(parents=True, exist_ok=True)
    
    stock_count = 0
    for sym, stock in stocks_db.items():
        clean_sym = sym.strip().upper()
        sym_dir = stocks_dir / clean_sym
        sym_dir.mkdir(parents=True, exist_ok=True)
        
        html_content = generate_stock_html(stock)
        
        # Write both public/stocks/:symbol/index.html AND public/stocks/:symbol.html for cleanUrls
        with open(sym_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        with open(stocks_dir / f"{clean_sym}.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        stock_count += 1
        if stock_count % 500 == 0:
            print(f"  ✓ Pre-rendered {stock_count}/{len(stocks_db)} stock pages...")

    print(f"✅ Generated {stock_count} static stock pages in {time.time() - start_time:.2f}s.")

    # 3. Generate Crypto Static HTMLs
    crypto_start = time.time()
    crypto_dir = ROOT / "public/crypto"
    crypto_dir.mkdir(parents=True, exist_ok=True)
    
    crypto_count = 0
    for sym, coin in crypto_db.items():
        clean_sym = sym.strip().upper()
        sym_dir = crypto_dir / clean_sym
        sym_dir.mkdir(parents=True, exist_ok=True)
        
        html_content = generate_crypto_html(coin)
        
        # Write both public/crypto/:symbol/index.html AND public/crypto/:symbol.html
        with open(sym_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        with open(crypto_dir / f"{clean_sym}.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        crypto_count += 1
        if crypto_count % 250 == 0:
            print(f"  ✓ Pre-rendered {crypto_count}/{len(crypto_db)} crypto pages...")

    print(f"✅ Generated {crypto_count} static crypto pages in {time.time() - crypto_start:.2f}s.")
    print(f"🎉 TOTAL SSG COMPLETE: {stock_count + crypto_count} static pages pre-baked in {time.time() - start_time:.2f}s!")

if __name__ == "__main__":
    main()
