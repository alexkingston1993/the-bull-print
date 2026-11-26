#!/usr/bin/env python3
"""
Deep Internal Linking & Semantic Authority Mesh Generator:
Cross-links all 338 research articles with:
1. Contextual equity links -> /stocks/:symbol (2,643 stocks)
2. Contextual crypto links -> /crypto/:symbol (1,000 cryptos)
3. Financial calculators & tooling links -> /calculators, /screener, /crypto-radar
4. Hierarchical breadcrumbs & thematic SEO clusters
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Key High-Search Equities Map
STOCK_KEYWORDS = {
    r'\bReliance Industries\b': ('Reliance Industries', '/stocks/RELIANCE'),
    r'\bReliance\b': ('Reliance', '/stocks/RELIANCE'),
    r'\bTata Consultancy Services\b': ('Tata Consultancy Services', '/stocks/TCS'),
    r'\bTCS\b': ('TCS', '/stocks/TCS'),
    r'\bHDFC Bank\b': ('HDFC Bank', '/stocks/HDFCBANK'),
    r'\bInfosys\b': ('Infosys', '/stocks/INFY'),
    r'\bICICI Bank\b': ('ICICI Bank', '/stocks/ICICIBANK'),
    r'\bState Bank of India\b': ('State Bank of India', '/stocks/SBIN'),
    r'\bSBI\b': ('SBI', '/stocks/SBIN'),
    r'\bBharti Airtel\b': ('Bharti Airtel', '/stocks/BHARTIARTL'),
    r'\bAirtel\b': ('Airtel', '/stocks/BHARTIARTL'),
    r'\bITC Ltd\b': ('ITC Ltd', '/stocks/ITC'),
    r'\bITC\b': ('ITC', '/stocks/ITC'),
    r'\bLarsen & Toubro\b': ('Larsen & Toubro', '/stocks/LT'),
    r'\bL&T\b': ('L&T', '/stocks/LT'),
    r'\bTata Motors\b': ('Tata Motors', '/stocks/TATAMOTORS'),
    r'\bMaruti Suzuki\b': ('Maruti Suzuki', '/stocks/MARUTI'),
    r'\bBajaj Finance\b': ('Bajaj Finance', '/stocks/BAJFINANCE'),
    r'\bSun Pharma\b': ('Sun Pharma', '/stocks/SUNPHARMA'),
    r'\bTrent\b': ('Trent', '/stocks/TRENT'),
    r'\bTitan Company\b': ('Titan Company', '/stocks/TITAN'),
    r'\bTitan\b': ('Titan', '/stocks/TITAN'),
    r'\bZomato\b': ('Zomato', '/stocks/ZOMATO'),
    r'\bJio Financial\b': ('Jio Financial', '/stocks/JIOFIN')
}

# Key High-Search Cryptocurrencies Map
CRYPTO_KEYWORDS = {
    r'\bBitcoin\b': ('Bitcoin', '/crypto/BTC'),
    r'\bBTC\b': ('BTC', '/crypto/BTC'),
    r'\bEthereum\b': ('Ethereum', '/crypto/ETH'),
    r'\bETH\b': ('ETH', '/crypto/ETH'),
    r'\bSolana\b': ('Solana', '/crypto/SOL'),
    r'\bSOL\b': ('SOL', '/crypto/SOL'),
    r'\bTether\b': ('Tether', '/crypto/USDT'),
    r'\bUSDT\b': ('USDT', '/crypto/USDT'),
    r'\bBinance Coin\b': ('Binance Coin', '/crypto/BNB'),
    r'\bBNB\b': ('BNB', '/crypto/BNB'),
    r'\bRipple\b': ('Ripple', '/crypto/XRP'),
    r'\bXRP\b': ('XRP', '/crypto/XRP'),
    r'\bDogecoin\b': ('Dogecoin', '/crypto/DOGE'),
    r'\bCardano\b': ('Cardano', '/crypto/ADA'),
    r'\bChainlink\b': ('Chainlink', '/crypto/LINK'),
    r'\bPolygon\b': ('Polygon', '/crypto/POL'),
    r'\bAvalanche\b': ('Avalanche', '/crypto/AVAX'),
    r'\bSui\b': ('Sui', '/crypto/SUI'),
    r'\bBittensor\b': ('Bittensor', '/crypto/TAO'),
    r'\bRender Network\b': ('Render Network', '/crypto/RENDER'),
    r'\bRender\b': ('Render', '/crypto/RENDER')
}

def inject_interlinks(text):
    if not text or not isinstance(text, str):
        return text

    # Avoid modifying existing markdown links [Text](URL) or HTML tags <...>
    # Match words only when not inside a link bracket
    for pattern, (anchor, url) in list(STOCK_KEYWORDS.items()) + list(CRYPTO_KEYWORDS.items()):
        # Replace only the first occurrence in the entire article to avoid link spam
        def replacer(match):
            m_start = match.start()
            # Simple check if already inside a markdown link [ ... ]
            before = text[max(0, m_start-50):m_start]
            after = text[match.end():min(len(text), match.end()+50)]
            if '[' in before and ']' in after:
                return match.group(0)
            if '(' in before and ')' in after and 'http' in before:
                return match.group(0)
            return f"[{match.group(0)}]({url})"

        # Replace first occurrence only
        text = re.sub(pattern, replacer, text, count=1)

    return text

def main():
    print("⚡ GENERATING GLOBAL INTERNAL LINKING MESH ACROSS 338 ARTICLES")
    
    post_files = [
        ROOT / 'content/posts.json',
        ROOT / 'public/content/posts.json'
    ]
    
    with open(post_files[0], 'r', encoding='utf-8') as f:
        posts = json.load(f)
        
    enriched_count = 0
    total_links_added = 0
    
    for post in posts:
        original_body = post.get('html', '')
        if not original_body:
            continue
            
        enriched_body = inject_interlinks(original_body)
        
        # Add related institutional terminal links if not already present
        if "### Institutional Tools & Market Terminal" not in enriched_body:
            related_box = (
                "\n\n---\n\n"
                "### Institutional Tools & Market Terminal\n"
                "- Track real-time equity fundamentals across 2,640+ listed companies on the [NSE Equity Screener](/screener) and [Stock Profiles](/stocks).\n"
                "- Monitor top 1,000 digital assets with Indian Section 115BBH 30% tax audits on the [Cryptocurrency Terminal](/crypto).\n"
                "- Track early-stage token drops and bonding curve graduates on the [New Crypto Radar](/crypto-radar).\n"
                "- Run compounding and retirement scenario audits on [The Bull Print Financial Calculators](/calculators).\n"
            )
            enriched_body += related_box
            
        if enriched_body != original_body:
            post['html'] = enriched_body
            enriched_count += 1
            
    print(f"✅ Enriched {enriched_count} articles with contextual stock, crypto, and tool backlinks.")
    
    for p in post_files:
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2)
        print(f"✅ Saved enriched articles to {p}")

if __name__ == "__main__":
    main()
