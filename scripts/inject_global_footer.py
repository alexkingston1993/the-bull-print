import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FOOTER_HTML = """
    <!-- Global Institutional Authority & Interlink Footer -->
    <footer class="site-footer" style="background:var(--bg-card); border-top:1px solid var(--border-subtle); padding:48px 24px 32px 24px; margin-top:60px;">
        <div style="max-width:1440px; margin:0 auto; display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:32px; margin-bottom:36px;">
            <div>
                <h4 style="font-family:var(--font-display); font-size:14px; text-transform:uppercase; letter-spacing:0.05em; color:var(--text-primary); margin-bottom:14px;">🇮🇳 Dalal Street Giants</h4>
                <div style="display:flex; flex-direction:column; gap:8px; font-size:13px;">
                    <a href="/stocks/RELIANCE" style="color:var(--text-secondary); text-decoration:none;">Reliance Industries (RELIANCE)</a>
                    <a href="/stocks/TCS" style="color:var(--text-secondary); text-decoration:none;">Tata Consultancy Services (TCS)</a>
                    <a href="/stocks/HDFCBANK" style="color:var(--text-secondary); text-decoration:none;">HDFC Bank (HDFCBANK)</a>
                    <a href="/stocks/BHARTIARTL" style="color:var(--text-secondary); text-decoration:none;">Bharti Airtel (BHARTIARTL)</a>
                    <a href="/stocks/INFY" style="color:var(--text-secondary); text-decoration:none;">Infosys (INFY)</a>
                    <a href="/stocks/ICICIBANK" style="color:var(--text-secondary); text-decoration:none;">ICICI Bank (ICICIBANK)</a>
                    <a href="/stocks/SBIN" style="color:var(--text-secondary); text-decoration:none;">State Bank of India (SBIN)</a>
                    <a href="/stocks/ITC" style="color:var(--text-secondary); text-decoration:none;">ITC Ltd (ITC)</a>
                    <a href="/stocks/TATAMOTORS" style="color:var(--text-secondary); text-decoration:none;">Tata Motors (TATAMOTORS)</a>
                    <a href="/stocks/ZOMATO" style="color:var(--text-secondary); text-decoration:none;">Zomato Ltd (ZOMATO)</a>
                    <a href="/stocks" style="color:var(--groww-mint); font-weight:700; text-decoration:none;">View All 2,640+ Stocks →</a>
                </div>
            </div>
            <div>
                <h4 style="font-family:var(--font-display); font-size:14px; text-transform:uppercase; letter-spacing:0.05em; color:var(--text-primary); margin-bottom:14px;">🌐 Institutional Digital Assets</h4>
                <div style="display:flex; flex-direction:column; gap:8px; font-size:13px;">
                    <a href="/crypto/BTC" style="color:var(--text-secondary); text-decoration:none;">Bitcoin (BTC) Price & Tax Audit</a>
                    <a href="/crypto/ETH" style="color:var(--text-secondary); text-decoration:none;">Ethereum (ETH) Tokenomics</a>
                    <a href="/crypto/SOL" style="color:var(--text-secondary); text-decoration:none;">Solana (SOL) Candlestick Chart</a>
                    <a href="/crypto/BNB" style="color:var(--text-secondary); text-decoration:none;">BNB Chain (BNB) Analysis</a>
                    <a href="/crypto/XRP" style="color:var(--text-secondary); text-decoration:none;">XRP (Ripple) Settlement</a>
                    <a href="/crypto/DOGE" style="color:var(--text-secondary); text-decoration:none;">Dogecoin (DOGE) Meme Audit</a>
                    <a href="/crypto/ADA" style="color:var(--text-secondary); text-decoration:none;">Cardano (ADA) Formal Proofs</a>
                    <a href="/crypto/SUI" style="color:var(--text-secondary); text-decoration:none;">Sui (SUI) Move Layer 1</a>
                    <a href="/crypto/TAO" style="color:var(--text-secondary); text-decoration:none;">Bittensor (TAO) Decentralized AI</a>
                    <a href="/crypto/RENDER" style="color:var(--text-secondary); text-decoration:none;">Render (RENDER) GPU Compute</a>
                    <a href="/crypto" style="color:var(--groww-mint); font-weight:700; text-decoration:none;">View Top 1,000 Cryptos →</a>
                </div>
            </div>
            <div>
                <h4 style="font-family:var(--font-display); font-size:14px; text-transform:uppercase; letter-spacing:0.05em; color:var(--text-primary); margin-bottom:14px;">🛠️ Financial Tools & Radars</h4>
                <div style="display:flex; flex-direction:column; gap:8px; font-size:13px;">
                    <a href="/screener" style="color:var(--text-secondary); text-decoration:none;">NSE 10-Year Fundamental Screener</a>
                    <a href="/crypto-radar" style="color:#ff5252; font-weight:700; text-decoration:none;">🚀 New Crypto Projects Launchpad</a>
                    <a href="/calculators" style="color:var(--text-secondary); text-decoration:none;">Compounding & SIP Calculators</a>
                    <a href="/fno" style="color:var(--text-secondary); text-decoration:none;">Options & F&O Open Interest Radar</a>
                    <a href="/portfolio" style="color:var(--text-secondary); text-decoration:none;">Institutional Portfolio Tracker</a>
                    <a href="/ipo" style="color:var(--text-secondary); text-decoration:none;">Mainboard & SME IPO Calendar</a>
                    <a href="/unlisted" style="color:var(--text-secondary); text-decoration:none;">Pre-IPO & Unlisted Shares Desk</a>
                    <a href="/insurance" style="color:var(--text-secondary); text-decoration:none;">Health & Term Insurance Guide</a>
                </div>
            </div>
            <div>
                <h4 style="font-family:var(--font-display); font-size:14px; text-transform:uppercase; letter-spacing:0.05em; color:var(--text-primary); margin-bottom:14px;">⚖️ Statutory & Compliance</h4>
                <div style="display:flex; flex-direction:column; gap:8px; font-size:13px;">
                    <a href="/disclaimer" style="color:var(--text-secondary); text-decoration:none;">SEBI Research Analyst Disclaimer</a>
                    <a href="/risk-disclosure" style="color:var(--text-secondary); text-decoration:none;">Equity & Derivatives Risk Notice</a>
                    <a href="/privacy" style="color:var(--text-secondary); text-decoration:none;">Privacy Policy & Data Security</a>
                    <a href="/terms" style="color:var(--text-secondary); text-decoration:none;">Terms of Service & Usage</a>
                    <a href="/security.txt" style="color:var(--text-secondary); text-decoration:none;">Security Disclosure Policy</a>
                    <p style="font-size:11.5px; color:var(--text-muted); margin-top:10px; line-height:1.5;">
                        The Bull Print provides educational market intelligence, on-chain telemetry, and observational analysis. Not registered under SEBI (Research Analyst) Regulations, 2014.
                    </p>
                </div>
            </div>
        </div>
        <div style="max-width:1440px; margin:0 auto; padding-top:24px; border-top:1px solid var(--border-subtle); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; font-size:12px; color:var(--text-muted);">
            <div>© 2026 The Bull Print Media Desk. All rights reserved.</div>
            <div>Canonical Sitemaps: <a href="/sitemap-stocks.xml" style="color:var(--text-muted);">Stocks XML</a> · <a href="/sitemap-crypto.xml" style="color:var(--text-muted);">Crypto XML</a> · <a href="/sitemap-articles.xml" style="color:var(--text-muted);">Articles XML</a></div>
        </div>
    </footer>
"""

targets = [
    ROOT / 'public/crypto.html',
    ROOT / 'crypto.html',
    ROOT / 'public/stock.html',
    ROOT / 'stock.html',
    ROOT / 'public/crypto-radar.html',
    ROOT / 'crypto-radar.html'
]

for t in targets:
    if not t.exists():
        continue
    with open(t, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove existing basic footer if present
    content = re.sub(r'<footer class="site-footer">[\s\S]*?<\/footer>', '', content)
    
    # Inject before </main> or </body>
    if '</main>' in content:
        content = content.replace('</main>', '</main>\n' + FOOTER_HTML)
    else:
        content = content.replace('</body>', FOOTER_HTML + '\n</body>')
        
    with open(t, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Injected authority footer into {t.name}")
