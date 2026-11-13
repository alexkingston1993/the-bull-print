import json
import os
import shutil

TOPIC_MAPPINGS = [
    {
        'match': lambda p: any(x in p['slug'].lower() or x in p['title'].lower() for x in ['silver', 'gold']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/gold_silver_macro_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_silver_gold_crash.png',
        'alt': 'Silver Crashes ₹56,000 & Gold Price Drop Analysis: Paper Futures Margin Liquidation vs Physical Bullion Reserve Fortress Infographic',
        'caption': 'Institutional macro breakdown: Why international commercial banks liquidate paper commodity derivatives during margin calls while sovereign entities accumulate physical bullion reserves.'
    },
    {
        'match': lambda p: any(x in p['slug'].lower() or x in p['title'].lower() for x in ['93%', '93-percent', '93-of-everyday', 'sebi_fo', 'quick market bets']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/sebi_options_trading_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_sebi_93_percent_options_loss.png',
        'alt': 'SEBI Study Infographic: Why 93% of Everyday Retail Traders Lose Money in Equity F&O Derivatives Due to Theta Time Decay',
        'caption': 'Official SEBI data telemetry: Retail option buyers lose an average of ₹1,25,000 as unrelenting Theta decay erodes contract value in the final 48 hours before weekly expiry.'
    },
    {
        'match': lambda p: any(x in p['slug'].lower() or x in p['title'].lower() for x in ['guide for beginners', 'what big bank selli', 'family savings']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/dalal_street_fii_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_indian_stock_market_beginners.png',
        'alt': 'Indian Stock Market Beginner Roadmap Infographic: The 3-Pillar Family Savings Fortress and Nifty 50 Secular Compounding',
        'caption': 'Dalal Street beginner guide: How everyday families build multi-generational compounding using low-cost index funds, sovereign gold, and zero debt leverage.'
    },
    {
        'match': lambda p: any(x in p['slug'].lower() or x in p['title'].lower() for x in ['big foreign banks sell', 'big-foreign-banks-sell', 'foreign banks sell ₹3,200']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/dalal_street_fii_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_fii_selling_block_deals.png',
        'alt': 'Foreign Institutional Investor (FII) Selling vs Domestic SIP Absorption Infographic on Dalal Street',
        'caption': 'Market mechanics: How ₹25,300 Cr monthly domestic mutual fund SIP inflows structurally absorb foreign institutional block sales without triggering systemic crashes.'
    },
    {
        'match': lambda p: any(x in p['slug'].lower() or x in p['title'].lower() for x in ['closing-bell', 'closing bell', 'price trap', '22,936']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/dalal_street_fii_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_closing_bell_price_trap.png',
        'alt': 'Closing Bell Price Trap Infographic: 3:15 PM Institutional Volume Dump and 30-Minute VWAP Settlement Auction Rules',
        'caption': 'Execution forensics: Why late afternoon retail momentum breakouts get crushed by the mandatory 3:00 PM to 3:30 PM Volume Weighted Average Price (VWAP) settlement.'
    },
    {
        'match': lambda p: any(x in p['slug'].lower() or x in p['title'].lower() for x in ['option chain', 'tbp-nifty-50-2025-01', 'nifty-opt']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/sebi_options_trading_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_nifty_option_chain_ladder.png',
        'alt': 'Nifty 50 Option Chain Ladder & Open Interest Concentration Infographic: Max Pain and Put-Call Ratio Telemetry',
        'caption': 'Quantitative derivatives breakdown: Tracking institutional Call and Put Open Interest clusters to identify structural support floors and resistance ceilings.'
    },
    {
        'match': lambda p: any(x in p['slug'].lower() or x in p['title'].lower() for x in ['order flow', 'order-flow-absorption', 'footprint']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/dalal_street_fii_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_nifty_order_flow_footprint.png',
        'alt': 'Nifty 50 Order Flow Absorption Infographic: Volume Delta Divergence and Institutional Footprint Chart Analysis',
        'caption': 'Tick-by-tick order book forensics: Detecting aggressive retail seller exhaustion into passive institutional limit bids before structural market reversals.'
    },
    {
        'match': lambda p: any(x in p['slug'].lower() or x in p['title'].lower() for x in ['camp_ird', 'settlement & surrender', 'settlement and surrender']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/irdai_insurance_claim_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_irdai_claim_settlement_rules.png',
        'alt': 'IRDAI New Regulations Infographic: Mandatory 30-Day Claim Settlement Window and Enhanced Surrender Value Standards',
        'caption': 'Policyholder regulatory safeguards: Insurers face mandatory interest penalties (Bank Rate + 2%) for claim delays beyond 30 days under the IRDAI Master Circular.'
    },
    {
        'match': lambda p: any(x in p['slug'].lower() or x in p['title'].lower() for x in ['csr', 'icr', 'claim settlement ratio', 'incurred claim']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/irdai_insurance_claim_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_csr_vs_icr_matrix.png',
        'alt': 'Insurance Marketing vs Reality Infographic: Why Claim Settlement Ratio (CSR) Hides Incurred Claim Ratio (ICR)',
        'caption': 'Forensic health insurance analysis: A 98% CSR measures claims by count, masking how low-ICR insurers routinely reject or haircut high-value critical care claims.'
    },
    {
        'match': lambda p: any(x in p['slug'].lower() or x in p['title'].lower() for x in ['section 45', 'ins-s45', 'incontestability']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/irdai_insurance_claim_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_section_45_insurance_act.png',
        'alt': 'Section 45 Insurance Act 1938 Infographic: The 3-Year Incontestability Shield and Absolute Death Claim Immunity',
        'caption': 'Statutory life insurance legal framework: Once 36 months elapse from policy issuance, Indian law strictly forbids insurers from questioning or repudiating claims.'
    },
    {
        'match': lambda p: any(x in p['slug'].lower() or x in p['title'].lower() for x in ['proportionate deduction', 'room cap', 'ins-ird-03']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/irdai_insurance_claim_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_irdai_proportionate_deduction.png',
        'alt': 'Health Insurance Proportionate Deduction Infographic: How Daily Room Rent Caps Slash Hospital Doctor & Surgery Bills',
        'caption': 'Mathematical breakdown of proportionate deduction: Choosing a room that exceeds the 1% cap triggers a proportional haircut across the entire surgical invoice.'
    },
    {
        'match': lambda p: any(x in p['slug'].lower() or x in p['title'].lower() for x in ['115bbh', '194s', 'ais / tis', 'crypto tax']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/crypto_forensics_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_crypto_tax_section_115bbh.png',
        'alt': 'India Crypto Tax Compliance Infographic: Section 115BBH 30% Flat Tax and Section 194S 1% TDS Reconciliation',
        'caption': 'Income tax forensic protocols: Reconciling on-chain transactions, exchange reports, and AIS/TIS filings under Section 115BBH without loss offsetting.'
    },
    {
        'match': lambda p: any(x in p['slug'].lower() or x in p['title'].lower() for x in ['funding rate', 'crypto_funding', 'perp structure']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/crypto_forensics_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_crypto_funding_rates.png',
        'alt': 'Crypto Perpetual Futures Funding Rates Infographic: Basis Arbitrage Mechanics and Delta-Neutral Cash & Carry Yields',
        'caption': 'Perpetual derivative mechanics: How periodic 8-hour funding rate transfers anchor crypto futures prices to spot markets and offer institutional arbitrage.'
    },
    {
        'match': lambda p: any(x in p['slug'].lower() or x in p['title'].lower() for x in ['solana', 'mev', 'sandwich bot', 'liquify']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/crypto_forensics_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_solana_mev_sandwich_bots.png',
        'alt': 'Solana Memecoin Siphon Infographic: Anatomy of an MEV Sandwich Attack on Decentralized Exchanges',
        'caption': 'On-chain telemetry: How automated MEV bots exploit high retail slippage settings via Jito bundles to extract immediate riskless profit on DEX swaps.'
    },
    {
        'match': lambda p: any(x in p['slug'].lower() or x in p['title'].lower() for x in ['tether', 'shadow engine', 'cantor fitzgerald']),
        'coverImage': 'https://bullprintmedia.com/assets/editorial/crypto_forensics_hero.jpg',
        'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_tether_reserve_forensics.png',
        'alt': 'Tether $110 Billion Shadow Engine Infographic: US Treasury Bills Backing and Cantor Fitzgerald Custody Audit',
        'caption': 'Forensic audit of USDT reserves: Deconstructing the $85B+ sovereign debt portfolio and interest income engine powering global stablecoin liquidity.'
    }
]

DEFAULT_MAPPING = {
    'coverImage': 'https://bullprintmedia.com/assets/editorial/dalal_street_fii_hero.jpg',
    'infographic': 'https://bullprintmedia.com/assets/infographics/infographic_indian_stock_market_beginners.png',
    'alt': 'Dalal Street Institutional Equity Research & Fundamental Moat Analysis Infographic | The Bull Print',
    'caption': 'Comprehensive quantitative breakdown, forensic accounting screens, and long-term economic moat evaluation for Indian equities.'
}

def get_mapping_for_post(p):
    for m in TOPIC_MAPPINGS:
        if m['match'](p):
            return m
    return DEFAULT_MAPPING

with open('content/posts.json') as f:
    posts = json.load(f)

print(f"Enriching {len(posts)} posts with tailor-made infographics and SEO metadata...")

for p in posts:
    mapping = get_mapping_for_post(p)
    p['coverImage'] = mapping['coverImage']
    p['infographic'] = mapping['infographic']
    p['imageAlt'] = mapping['alt']
    p['imageCaption'] = mapping['caption']
    p['imageMeta'] = {
        'url': mapping['infographic'],
        'coverUrl': mapping['coverImage'],
        'alt': mapping['alt'],
        'caption': mapping['caption'],
        'width': 1200,
        'height': 675,
        'type': 'image/png'
    }

    # Ensure schema has ImageObject in Article graph
    if 'schema' in p and '@graph' in p['schema']:
        article_node = None
        for node in p['schema']['@graph']:
            if node.get('@type') == 'Article':
                article_node = node
                break
        if article_node:
            article_node['image'] = {
                '@type': 'ImageObject',
                'url': mapping['coverImage'],
                'width': 1200,
                'height': 675,
                'caption': mapping['caption'],
                'description': mapping['alt'],
                'representativeOfPage': True
            }

with open('content/posts.json', 'w') as f:
    json.dump(posts, f, indent=2)

# Also mirror to public/content/posts.json
os.makedirs('public/content', exist_ok=True)
shutil.copy('content/posts.json', 'public/content/posts.json')

print("Successfully enriched all 50 posts and synchronized to public/content/posts.json!")
