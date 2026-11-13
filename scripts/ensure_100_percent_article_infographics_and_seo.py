#!/usr/bin/env python3
"""
Ensure 100% Infographic Embeds, Image Alt Attributes, SEO Image Tags,
and Structured JSON-LD ImageObject Schemas across ALL Articles and Markdown Files.
"""

import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TOPIC_SPECS = [
    {
        'key': 'silver_gold',
        'match': lambda text: any(k in text for k in ['silver', 'gold', 'precious metal', 'bullion', 'mcx']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/gold_silver_macro_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_silver_gold_crash.png',
        'alt': 'Silver Crashes ₹56,000 & Gold Price Drop Analysis: Paper Futures Margin Liquidation vs Physical Bullion Reserve Fortress Infographic',
        'caption': 'Institutional macro breakdown: Why international commercial banks liquidate paper commodity derivatives during margin calls while sovereign entities accumulate physical bullion reserves.',
        'faq': [
            ("Why did paper silver and gold prices drop sharply?", "Paper futures dropped due to institutional margin liquidations and collateral rebalancing across global commodity exchanges, not due to lack of physical demand."),
            ("What is the difference between paper gold and physical gold?", "Physical gold carries zero counterparty default liability and protects family savings, while paper contracts are speculative derivatives subject to forced liquidations.")
        ]
    },
    {
        'key': 'sebi_fo_93',
        'match': lambda text: any(k in text for k in ['93%', '93 percent', '93-percent', '93-of-everyday', 'sebi', 'f&o', 'options loss', 'theta decay', 'quick market bet']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/sebi_options_trading_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_sebi_93_percent_options_loss.png',
        'alt': 'SEBI Study Infographic: Why 93% of Everyday Retail Traders Lose Money in Equity F&O Derivatives Due to Theta Time Decay',
        'caption': 'Official SEBI data telemetry: Retail option buyers lose an average of ₹1,25,000 as unrelenting Theta decay erodes contract value in the final 48 hours before weekly expiry.',
        'faq': [
            ("Why do 93% of retail option buyers lose capital?", "Rapid Theta time decay systematically drains contract value every hour into weekly expiry, creating an insurmountable mathematical disadvantage for retail buyers."),
            ("What is the safest alternative for retail equity investors?", "Maintaining a disciplined, low-cost monthly SIP in the Nifty 50 Index and accumulating debt-free secular compounders.")
        ]
    },
    {
        'key': 'fii_selling',
        'match': lambda text: any(k in text for k in ['foreign banks sell', 'big foreign bank', 'fii selling', 'fii-selling', 'block deals', 'foreign institutional']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/dalal_street_fii_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_fii_selling_block_deals.png',
        'alt': 'Foreign Institutional Investor (FII) Selling vs Domestic SIP Absorption Infographic on Dalal Street',
        'caption': 'Market mechanics: How ₹25,300 Cr monthly domestic mutual fund SIP inflows structurally absorb foreign institutional block sales without triggering systemic crashes.',
        'faq': [
            ("Why do foreign institutional investors sell Indian equities?", "Global asset managers periodically sell to rebalance emerging market weights, lock in dollar gains, or manage margin requirements in overseas markets."),
            ("How do domestic SIPs protect the Indian market?", "Domestic mutual fund SIPs provide a relentless monthly inflow of over ₹25,000 Cr, absorbing foreign supply and reducing market volatility.")
        ]
    },
    {
        'key': 'closing_bell',
        'match': lambda text: any(k in text for k in ['closing bell', 'closing-bell', 'price trap', '3:15 pm', 'vwap settlement', 'opening trap']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/dalal_street_fii_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_closing_bell_price_trap.png',
        'alt': 'Closing Bell Price Trap Infographic: 3:15 PM Institutional Volume Dump and 30-Minute VWAP Settlement Auction Rules',
        'caption': 'Execution forensics: Why late afternoon retail momentum breakouts get crushed by the mandatory 3:00 PM to 3:30 PM Volume Weighted Average Price (VWAP) settlement.',
        'faq': [
            ("What is the 3:15 PM closing bell trap?", "Institutional algorithms execute massive rebalancing orders during the final 30 minutes, triggering artificial false breakouts that trap late retail momentum traders."),
            ("How is the official closing price calculated in Indian markets?", "The official close is the Volume Weighted Average Price (VWAP) of all trades executed between 3:00 PM and 3:30 PM.")
        ]
    },
    {
        'key': 'option_chain',
        'match': lambda text: any(k in text for k in ['option chain', 'open interest', 'max pain', 'put-call ratio', 'pcr', 'gamma', 'derivatives']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/sebi_options_trading_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_nifty_option_chain_ladder.png',
        'alt': 'Nifty 50 Option Chain Ladder & Open Interest Concentration Infographic: Max Pain and Put-Call Ratio Telemetry',
        'caption': 'Quantitative derivatives breakdown: Tracking institutional Call and Put Open Interest clusters to identify structural support floors and resistance ceilings.',
        'faq': [
            ("What is Max Pain in the Nifty Option Chain?", "Max Pain is the strike price where the greatest number of outstanding option contracts expire worthless, maximizing writing revenue for institutional market makers."),
            ("How does Put-Call Ratio (PCR) indicate sentiment?", "A PCR below 0.7 suggests oversold extremes ready for short-covering, while a PCR above 1.4 signals complacency and potential topping behavior.")
        ]
    },
    {
        'key': 'order_flow',
        'match': lambda text: any(k in text for k in ['order flow', 'order-flow', 'footprint', 'volume delta', 'absorption', 'limit bid']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/dalal_street_fii_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_nifty_order_flow_footprint.png',
        'alt': 'Nifty 50 Order Flow Absorption Infographic: Volume Delta Divergence and Institutional Footprint Chart Analysis',
        'caption': 'Tick-by-tick order book forensics: Detecting aggressive retail seller exhaustion into passive institutional limit bids before structural market reversals.',
        'faq': [
            ("What is volume delta divergence?", "It occurs when price makes a new extreme but net aggressive market orders decline, revealing institutional limit order absorption and imminent reversal."),
            ("Why is order flow superior to traditional indicators?", "Order flow reflects actual executed transactions in the limit order book rather than lagging mathematical derivatives of price.")
        ]
    },
    {
        'key': 'irdai_rules',
        'match': lambda text: any(k in text for k in ['irdai', 'claim settlement rules', 'surrender value', '30-day window', 'master circular']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/irdai_insurance_claim_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_irdai_claim_settlement_rules.png',
        'alt': 'IRDAI New Regulations Infographic: Mandatory 30-Day Claim Settlement Window and Enhanced Surrender Value Standards',
        'caption': 'Policyholder regulatory safeguards: Insurers face mandatory interest penalties (Bank Rate + 2%) for claim delays beyond 30 days under the IRDAI Master Circular.',
        'faq': [
            ("What is the mandatory claim settlement timeline under IRDAI?", "Insurers must settle claims within 30 days of receiving all documentation or pay statutory penal interest of Bank Rate plus 2%."),
            ("How do the new surrender value guidelines protect consumers?", "Insurers are prohibited from zero-value forfeitures after the first premium year, ensuring policyholders recover a guaranteed minimum proportion of paid premiums.")
        ]
    },
    {
        'key': 'csr_vs_icr',
        'match': lambda text: any(k in text for k in ['csr', 'icr', 'claim settlement ratio', 'incurred claim ratio', 'health insurance claim']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/irdai_insurance_claim_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_csr_vs_icr_matrix.png',
        'alt': 'Insurance Marketing vs Reality Infographic: Why Claim Settlement Ratio (CSR) Hides Incurred Claim Ratio (ICR)',
        'caption': 'Forensic health insurance analysis: A 98% CSR measures claims by count, masking how low-ICR insurers routinely reject or haircut high-value critical care claims.',
        'faq': [
            ("Why is CSR misleading in health insurance?", "CSR only measures the number of claims settled versus filed, treating a ₹5,000 claim identically to a ₹15,00,000 critical cancer surgery claim."),
            ("What is Incurred Claim Ratio (ICR)?", "ICR measures the total monetary value of claims paid out as a percentage of total collected premiums, revealing the insurer's true financial payouts.")
        ]
    },
    {
        'key': 'section_45',
        'match': lambda text: any(k in text for k in ['section 45', 'insurance act', 'incontestability', '3-year', 'repudiation', 'claim rejection']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/irdai_insurance_claim_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_section_45_insurance_act.png',
        'alt': 'Section 45 Insurance Act 1938 Infographic: The 3-Year Incontestability Shield and Absolute Death Claim Immunity',
        'caption': 'Statutory life insurance legal framework: Once 36 months elapse from policy issuance, Indian law strictly forbids insurers from questioning or repudiating claims.',
        'faq': [
            ("What is the 3-year incontestability clause?", "Under Section 45 of the Insurance Act 1938, no life insurance policy can be called in question by an insurer after 3 years on any ground whatsoever."),
            ("Can an insurer reject a death claim after 3 years for non-disclosure?", "No. The statutory protection under Section 45 is absolute after 36 months, preventing insurers from denying life claim payouts to nominees.")
        ]
    },
    {
        'key': 'proportionate_deduction',
        'match': lambda text: any(k in text for k in ['proportionate deduction', 'room rent', 'room cap', 'icu cap', 'hospital bill haircut']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/irdai_insurance_claim_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_irdai_proportionate_deduction.png',
        'alt': 'Health Insurance Proportionate Deduction Infographic: How Daily Room Rent Caps Slash Hospital Doctor & Surgery Bills',
        'caption': 'Mathematical breakdown of proportionate deduction: Choosing a room that exceeds the 1% cap triggers a proportional haircut across the entire surgical invoice.',
        'faq': [
            ("How does a room rent sub-limit trigger proportionate deductions?", "If your room rent exceeds your policy cap by 50%, the insurer proportionately slashes your doctor fees, operation theater, and nursing charges by 50%."),
            ("How can policyholders avoid proportionate deductions?", "Always choose health insurance plans with zero room rent capping, single private room eligibility, or ICU sub-limit waivers.")
        ]
    },
    {
        'key': 'crypto_tax_115bbh',
        'match': lambda text: any(k in text for k in ['115bbh', '194s', 'vda', 'crypto tax', 'taxation', 'tds']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/crypto_forensics_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_crypto_tax_section_115bbh.png',
        'alt': 'India Crypto Tax Compliance Infographic: Section 115BBH 30% Flat Tax and Section 194S 1% TDS Reconciliation',
        'caption': 'Income tax forensic protocols: Reconciling on-chain transactions, exchange reports, and AIS/TIS filings under Section 115BBH without loss offsetting.',
        'faq': [
            ("Can crypto losses be set off against crypto gains in India?", "No. Section 115BBH of the Income Tax Act strictly prohibits offsetting losses from one virtual digital asset against gains in another."),
            ("What is the penalty for failing to pay 1% TDS under Section 194S?", "Failure to deduct or deposit 1% TDS attracts interest penalties, disallowance, and potential penal scrutiny from the Income Tax Department.")
        ]
    },
    {
        'key': 'crypto_funding',
        'match': lambda text: any(k in text for k in ['funding rate', 'perpetual', 'perp', 'basis trade', 'arbitrage', 'delta-neutral']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/crypto_forensics_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_crypto_funding_rates.png',
        'alt': 'Crypto Perpetual Futures Funding Rates Infographic: Basis Arbitrage Mechanics and Delta-Neutral Cash & Carry Yields',
        'caption': 'Perpetual derivative mechanics: How periodic 8-hour funding rate transfers anchor crypto futures prices to spot markets and offer institutional arbitrage.',
        'faq': [
            ("What are crypto perpetual funding rates?", "Funding rates are periodic payments exchanged between long and short traders every 8 hours to anchor the perpetual futures price to the underlying spot price."),
            ("How do institutional investors earn delta-neutral yield on funding rates?", "By buying spot crypto and simultaneously shorting an equal value of perpetual futures when the funding rate is heavily positive.")
        ]
    },
    {
        'key': 'solana_mev',
        'match': lambda text: any(k in text for k in ['solana', 'mev', 'sandwich', 'memecoin', 'slippage', 'jito', 'dex']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/crypto_forensics_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_solana_mev_sandwich_bots.png',
        'alt': 'Solana Memecoin Siphon Infographic: Anatomy of an MEV Sandwich Attack on Decentralized Exchanges',
        'caption': 'On-chain telemetry: How automated MEV bots exploit high retail slippage settings via Jito bundles to extract immediate riskless profit on DEX swaps.',
        'faq': [
            ("What is an MEV sandwich attack?", "An automated bot detects your pending swap in the mempool, front-runs by buying the token to pump the price, and immediately back-runs by selling for riskless profit."),
            ("How can retail traders protect against MEV sandwich bots?", "Set tight slippage tolerances (under 0.5%), use MEV-protected RPC endpoints, and avoid trading illiquid micro-caps during peak volatility.")
        ]
    },
    {
        'key': 'tether_reserves',
        'match': lambda text: any(k in text for k in ['tether', 'usdt', 'shadow engine', 'cantor fitzgerald', 'commercial paper', 'reserves']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/crypto_forensics_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_tether_reserve_forensics.png',
        'alt': 'Tether $110 Billion Shadow Engine Infographic: US Treasury Bills Backing and Cantor Fitzgerald Custody Audit',
        'caption': 'Forensic audit of USDT reserves: Deconstructing the $85B+ sovereign debt portfolio and interest income engine powering global stablecoin liquidity.',
        'faq': [
            ("What backs Tether USDT reserves?", "Tether reserves are primarily backed by short-term US Treasury Bills, overnight repo agreements, and gold bullion custodied by Cantor Fitzgerald."),
            ("How much profit does Tether generate annually?", "Tether generates over $6 billion in annualized net profit from high US Treasury yields on its $100B+ reserve portfolio.")
        ]
    }
]

DEFAULT_SPEC = {
    'key': 'dalal_street_beginners',
    'coverImage': 'https://bullprintmedia.com/assets/editorial/dalal_street_fii_hero.jpg',
    'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_indian_stock_market_beginners.png',
    'alt': 'Indian Stock Market Beginner Roadmap Infographic: The 3-Pillar Family Savings Fortress and Nifty 50 Secular Compounding',
    'caption': 'Dalal Street beginner guide: How everyday families build multi-generational compounding using low-cost index funds, sovereign gold, and zero debt leverage.',
    'faq': [
        ("What is the most reliable strategy for Indian equity beginners?", "Starting a regular monthly SIP in the top 50 index funds, maintaining a physical gold cushion, and avoiding high-risk derivatives."),
        ("Why is market volatility beneficial for long-term investors?", "Market drops allow monthly SIP investors to accumulate more units at lower valuations, accelerating compounding returns over 10 to 15 years.")
    ]
}

def match_spec(text):
    text_lower = text.lower()
    for s in TOPIC_SPECS:
        if s['match'](text_lower):
            return s
    return DEFAULT_SPEC

def build_schema(post, spec):
    slug = post['slug']
    title = post['title']
    desc = post.get('excerpt', post['title'])
    date_pub = post.get('date', '2026-10-27T14:23:46.525559+00:00')
    canonical_url = f"https://bullprintmedia.com/article?slug={slug}"
    
    faq_nodes = []
    for q, a in spec['faq']:
        faq_nodes.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })

    graph = [
        {
            "@type": "Article",
            "headline": title,
            "description": desc,
            "datePublished": date_pub,
            "dateModified": date_pub,
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": canonical_url
            },
            "author": {
                "@type": "Person",
                "name": "The Bull Print Research Desk",
                "jobTitle": "Institutional Market Analysts & Forensic Researchers",
                "url": "https://bullprintmedia.com/"
            },
            "publisher": {
                "@type": "Organization",
                "name": "The Bull Print",
                "url": "https://bullprintmedia.com",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://bullprintmedia.com/brand_assets/logo_master_1024x1024.png"
                }
            },
            "image": {
                "@type": "ImageObject",
                "url": spec['infographic'],
                "width": 1200,
                "height": 675,
                "caption": spec['caption'],
                "description": spec['alt'],
                "representativeOfPage": True
            }
        },
        {
            "@type": "FAQPage",
            "mainEntity": faq_nodes
        }
    ]

    yt_url = post.get('youtubeUrl')
    if yt_url:
        vid_id = ""
        if "watch?v=" in yt_url:
            vid_id = yt_url.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in yt_url:
            vid_id = yt_url.split("youtu.be/")[1].split("?")[0]
        if vid_id:
            graph.append({
                "@type": "VideoObject",
                "name": title,
                "description": desc,
                "thumbnailUrl": [
                    spec['coverImage'],
                    f"https://img.youtube.com/vi/{vid_id}/maxresdefault.jpg"
                ],
                "uploadDate": date_pub,
                "embedUrl": f"https://www.youtube.com/embed/{vid_id}"
            })

    return {
        "@context": "https://schema.org",
        "@graph": graph
    }

def process_posts_json():
    posts_path = ROOT / 'content/posts.json'
    with open(posts_path, 'r', encoding='utf-8') as f:
        posts = json.load(f)

    for p in posts:
        text = f"{p.get('title', '')} {p.get('slug', '')} {p.get('excerpt', '')} {' '.join(p.get('tags', []))}"
        spec = match_spec(text)

        p['coverImage'] = spec['coverImage']
        p['infographic'] = spec['infographic']
        p['imageAlt'] = spec['alt']
        p['imageCaption'] = spec['caption']
        p['imageMeta'] = {
            'url': spec['infographic'],
            'coverUrl': spec['coverImage'],
            'alt': spec['alt'],
            'caption': spec['caption'],
            'width': 1200,
            'height': 675,
            'type': 'image/png'
        }
        p['schema'] = build_schema(p, spec)

    with open(posts_path, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2)

    public_posts = ROOT / 'public/content/posts.json'
    public_posts.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(posts_path, public_posts)
    print(f"✅ Processed all {len(posts)} posts in posts.json with complete SEO/Schema/Infographics!")

def process_markdown_files():
    posts_dir = ROOT / 'content/posts'
    md_files = list(posts_dir.glob('*.md'))
    updated = 0

    for fpath in md_files:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        text = f"{fpath.name} {content[:500]}"
        spec = match_spec(text)

        alt = spec['alt']
        caption = spec['caption']
        info_url = spec['infographic']
        cover_url = spec['coverImage']

        # Ensure frontmatter has coverImage and infographic
        if 'coverImage:' not in content:
            content = re.sub(
                r'(---\s*\n)',
                f'\\1coverImage: "{cover_url}"\ninfographic: "{info_url}"\nimageAlt: "{alt}"\n',
                content,
                count=1
            )
        else:
            # Replace existing frontmatter values if needed
            content = re.sub(r'coverImage:\s*["\']?[^"\'\n]+["\']?', f'coverImage: "{cover_url}"', content)
            content = re.sub(r'infographic:\s*["\']?[^"\'\n]+["\']?', f'infographic: "{info_url}"', content)

        # Inject figure embed if missing
        if 'article-infographic-embed' not in content:
            figure_html = f'''
<!-- Tailor-Made Research Infographic for SEO & AI Overviews -->
<figure class="article-infographic-embed" style="margin:28px 0; background:rgba(11,19,36,0.6); border:1px solid rgba(255,255,255,0.08); border-radius:12px; overflow:hidden;">
  <img src="{info_url}" alt="{alt}" title="{alt}" style="width:100%; height:auto; display:block; border-bottom:1px solid rgba(255,255,255,0.08);" loading="lazy" decoding="async">
  <figcaption style="padding:12px 18px; font-size:13px; color:#94a3b8; font-family:var(--font-body); display:flex; align-items:center; gap:8px;">
    <span>📊</span> <span><strong>Infographic:</strong> {caption}</span>
  </figcaption>
</figure>
'''
            if '</div>\n\n <!-- 2.' in content:
                content = content.replace('</div>\n\n <!-- 2.', f'</div>\n{figure_html}\n <!-- 2.', 1)
            elif '</div>\n\n' in content:
                content = content.replace('</div>\n\n', f'</div>\n{figure_html}\n', 1)
            elif '---' in content:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    content = f"---{parts[1]}---\n\n{figure_html}\n{parts[2]}"
                else:
                    content = content + f"\n\n{figure_html}"
            else:
                content = content + f"\n\n{figure_html}"

            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1

    print(f"✅ Processed all {len(md_files)} markdown files! Newly embedded: {updated}")

if __name__ == '__main__':
    process_posts_json()
    process_markdown_files()
