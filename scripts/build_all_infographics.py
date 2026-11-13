import os
from PIL import Image
from render_infographics import render_infographic

os.makedirs('assets/infographics', exist_ok=True)
os.makedirs('public/assets/infographics', exist_ok=True)

SPECS = [
    {
        'key': 'infographic_silver_gold_crash',
        'category': 'PRECIOUS METALS · MACRO FORENSICS',
        'title': 'Silver Crashes ₹56,000 & Gold Drops: Why Big Banks Shake Out Retail',
        'subtitle': 'Paper futures margin liquidation vs physical bullion counterparty-free fortress',
        'accent': '#F59E0B', # Gold
        'cards': [
            {
                'value': '-18.4%',
                'label': 'Paper Margin Squeeze',
                'desc': 'Forced institutional liquidation\nin COMEX/MCX futures contracts.',
                'color': '#EF4444'
            },
            {
                'value': '100%',
                'label': 'Physical Vault Backing',
                'desc': 'Zero counterparty liability.\nSovereign store of family wealth.',
                'color': '#F59E0B'
            },
            {
                'value': '+34.2%',
                'label': 'Post-Shakeout Median',
                'desc': '18-Month historical recovery\nfollowing paper price shakeouts.',
                'color': '#00D09C'
            }
        ],
        'framework_title': 'THE WEALTH ACCUMULATION PROTOCOL',
        'bullets': [
            '1. Distinguish between Paper Derivatives (speculative margin) and Physical Bullion (zero default risk).',
            '2. Foreign banks dump paper contracts during liquidity crunches to fund collateral calls in Treasuries.',
            '3. Everyday investors must avoid panic selling and use volatility to build disciplined sovereign reserves.'
        ],
        'source': 'Source: LBMA Bullion Registry, COMEX Commitment of Traders & The Bull Print Macro Desk'
    },
    {
        'key': 'infographic_sebi_93_percent_options_loss',
        'category': 'REGULATORY STUDY · SEBI F&O FORENSICS',
        'title': 'Why 93% of Everyday People Lose Money in F&O Derivatives',
        'subtitle': 'SEBI study reveals how rapid theta time decay systematically wipes out retail option buyers',
        'accent': '#EF4444', # Red
        'cards': [
            {
                'value': '93.0%',
                'label': 'Retail Net Capital Loss',
                'desc': '9 out of 10 retail traders suffer\npermanent loss within 90 days.',
                'color': '#EF4444'
            },
            {
                'value': '₹1,25,000',
                'label': 'Average Loss Per Trader',
                'desc': 'Net wealth erosion excluding\nbrokerage and exchange STT costs.',
                'color': '#F59E0B'
            },
            {
                'value': '70% Loss',
                'label': 'Theta Decay in 48 Hours',
                'desc': 'Out-of-the-money premium melts\nrapidly toward zero on expiry.',
                'color': '#EF4444'
            }
        ],
        'framework_title': 'WHY THE MATH FAVORS INSTITUTIONAL SELLERS',
        'bullets': [
            '1. Option buyers fight against both market direction and unrelenting daily Theta time decay.',
            '2. Institutional algorithmic desks harvest option premiums by acting as passive liquidity providers.',
            '3. Direct long-term equity SIPs in high-ROCE compounders consistently outperform 99% of F&O traders.'
        ],
        'source': 'Source: SEBI Official Study on Individual Traders in Equity F&O Segment (FY22-FY24)'
    },
    {
        'key': 'infographic_indian_stock_market_beginners',
        'category': 'FAMILY WEALTH · BEGINNER ROADMAP',
        'title': 'Indian Stock Market Beginner Guide: Building Generational Compounding',
        'subtitle': 'How everyday families can harness Indian demographic growth without speculating',
        'accent': '#00D09C', # Mint
        'cards': [
            {
                'value': '13.8%',
                'label': 'Nifty 50 20-Year CAGR',
                'desc': 'Historical compounding returns of\nIndia’s top 50 industrial leaders.',
                'color': '#00D09C'
            },
            {
                'value': '₹25,300 Cr',
                'label': 'Monthly Domestic SIP',
                'desc': 'Systematic domestic inflows\ncushioning against foreign volatility.',
                'color': '#38BDF8'
            },
            {
                'value': '0% Leverage',
                'label': 'Zero Debt Rule',
                'desc': 'Never borrow to invest. Preserve\nstaying power during downturns.',
                'color': '#F59E0B'
            }
        ],
        'framework_title': 'THE 3-PILLAR FAMILY SAVINGS ARCHITECTURE',
        'bullets': [
            '1. Pillar 1 (50% Equities): Low-cost Nifty 50 & Junior 50 index funds for secular GDP compounding.',
            '2. Pillar 2 (20% Sovereign Bullion): Physical Gold / SGBs as a non-correlated inflation insurance hedge.',
            '3. Pillar 3 (30% Cash Buffer): Overnight Liquid Funds and Fixed Deposits to cover 12 months of expenses.'
        ],
        'source': 'Source: NSE Historical Indices Data & AMFI Monthly Mutual Fund Inflow Telemetry'
    },
    {
        'key': 'infographic_fii_selling_block_deals',
        'category': 'INSTITUTIONAL FLOW · MARKET MECHANICS',
        'title': 'Big Foreign Banks Sell ₹3,200 Cr: The Ultimate Beginner Guide',
        'subtitle': 'Pre-market institutional block sales vs domestic mutual fund structural absorption',
        'accent': '#38BDF8', # Sky Blue
        'cards': [
            {
                'value': '₹3,200 Cr',
                'label': 'FII Tactical Sale',
                'desc': 'Pre-market negotiated block deals\nexecuted by offshore global banks.',
                'color': '#F59E0B'
            },
            {
                'value': '₹4,150 Cr',
                'label': 'DII Cash Absorption',
                'desc': 'Domestic funds and retail SIPs\nabsorb supply without flash-crashing.',
                'color': '#00D09C'
            },
            {
                'value': '+0.42%',
                'label': 'Net Market Resilience',
                'desc': 'Benchmark Nifty closes higher\nas domestic liquidity dictates trend.',
                'color': '#38BDF8'
            }
        ],
        'framework_title': 'WHY FOREIGN OUTFLOWS NO LONGER PARALYZE DALAL STREET',
        'bullets': [
            '1. FII selling is often global portfolio rebalancing (covering US margin calls), not a verdict on Indian earnings.',
            '2. India’s domestic mutual fund SIP run-rate (>₹25,000 Cr/mo) has created a structural liquidity floor.',
            '3. Retail panic selling during FII block sales delivers high-quality compounders to institutions at a discount.'
        ],
        'source': 'Source: BSE/NSE Bulk & Block Deal Disclosures and NSDL Foreign Portfolio Investment Reports'
    },
    {
        'key': 'infographic_closing_bell_price_trap',
        'category': 'ORDER FLOW FORENSICS · EXECUTION TRAPS',
        'title': 'Closing Bell Price Trap: What Happens When Big Funds Sell at 3:15 PM',
        'subtitle': 'How the 30-minute volume-weighted average price (VWAP) calculation creates retail traps',
        'accent': '#EF4444',
        'cards': [
            {
                'value': '3:00 - 3:15 PM',
                'label': 'The Retail Momentum Trap',
                'desc': 'Late retail buyers chase intraday\nbreakouts with market orders.',
                'color': '#F59E0B'
            },
            {
                'value': '45% Volume',
                'label': 'The 3:15 PM Institutional Dump',
                'desc': 'Algos execute massive closing\norders into retail bid liquidity.',
                'color': '#EF4444'
            },
            {
                'value': 'VWAP Reset',
                'label': 'Final Settlement Price',
                'desc': 'Closing price settles at the 30-min\nVWAP average, wiping late gains.',
                'color': '#38BDF8'
            }
        ],
        'framework_title': 'TACTICAL CLOSING BELL RULES FOR INVESTORS',
        'bullets': [
            '1. The closing price of Indian equities is the weighted average between 3:00 PM and 3:30 PM, not the last traded tick.',
            '2. Institutional passive matching desks take the opposite side of urgent retail market orders.',
            '3. Avoid initiating new intraday equity or derivative trades after 3:00 PM to protect against auction slippage.'
        ],
        'source': 'Source: NSE Trading Regulations & Market Order Matching Engine Forensics'
    },
    {
        'key': 'infographic_nifty_option_chain_ladder',
        'category': 'QUANTITATIVE TELEMETRY · DERIVATIVES',
        'title': 'Nifty 50 Option Chain Analysis: Institutional Order Flow & Traps',
        'subtitle': 'Deciphering Open Interest concentration, Put-Call Ratio (PCR), and the Max Pain gravitational center',
        'accent': '#38BDF8',
        'cards': [
            {
                'value': '24,500',
                'label': 'Max Pain Strike',
                'desc': 'The exact index level where option\nwriters experience minimal payout.',
                'color': '#00D09C'
            },
            {
                'value': '1.42 Cr OI',
                'label': '24,800 Call Resistance',
                'desc': 'Institutional call writers capping\nupside before weekly expiry.',
                'color': '#EF4444'
            },
            {
                'value': '0.94 PCR',
                'label': 'Put-Call Ratio Median',
                'desc': 'Neutral sentiment balance.\nAbsence of extreme retail greed.',
                'color': '#38BDF8'
            }
        ],
        'framework_title': 'READING THE INSTITUTIONAL CHESSBOARD',
        'bullets': [
            '1. High Call Open Interest acts as a ceiling; High Put Open Interest acts as a structural institutional floor.',
            '2. Sudden unwinding of Put Open Interest signals smart money preparing for an impending volatility expansion.',
            '3. When PCR exceeds 1.40, markets are overbought; when PCR drops below 0.65, markets are prime for short covering.'
        ],
        'source': 'Source: NSE Live Option Chain Analytics & The Bull Print Quantitative Engine'
    },
    {
        'key': 'infographic_nifty_order_flow_footprint',
        'category': 'ORDER BOOK FORENSICS · LIQUIDITY PROFILE',
        'title': 'Nifty 50 Order Flow Absorption & Institutional Footprint Forensics',
        'subtitle': 'Aggressive market orders vs passive limit orders: spotting smart money absorption before reversals',
        'accent': '#00D09C',
        'cards': [
            {
                'value': 'Bullish Delta',
                'label': 'Volume Delta Divergence',
                'desc': 'Price prints equal lows while\nbuying delta surges positive.',
                'color': '#00D09C'
            },
            {
                'value': '18,500 Lots',
                'label': 'Passive Bid Absorption',
                'desc': 'Institutional limit orders soak up\naggressive retail panic sales.',
                'color': '#38BDF8'
            },
            {
                'value': 'POC Node',
                'label': 'Point of Control Shift',
                'desc': 'Heavy volume cluster forms at\nthe low, signaling accumulation.',
                'color': '#F59E0B'
            }
        ],
        'framework_title': 'FOOTPRINT FORENSIC CHECKLIST',
        'bullets': [
            '1. Normal candlestick charts hide inside volume; footprint charts reveal the executed buy/sell imbalance at each tick.',
            '2. Absorption occurs when high sell volume fails to push price down, confirming passive institutional accumulation.',
            '3. Never chase sudden momentum without verifying that aggressive delta is accompanied by expanding volume.'
        ],
        'source': 'Source: NSE Direct Tick-by-Tick Feed & Order Flow Footprint Algorithms'
    },
    {
        'key': 'infographic_irdai_claim_settlement_rules',
        'category': 'INSURANCE REGULATION · POLICYHOLDER RIGHTS',
        'title': 'IRDAI New Rules For Claim Settlement & Surrender: Complete Guide',
        'subtitle': 'Mandatory 30-day settlement windows, delayed interest penalties, and transparent surrender values',
        'accent': '#00D09C',
        'cards': [
            {
                'value': '30 Days',
                'label': 'Mandatory Claim Window',
                'desc': 'Insurer must pay or reject claim\nwithin 30 days of last document.',
                'color': '#00D09C'
            },
            {
                'value': 'Bank + 2%',
                'label': 'Penalty for Delay',
                'desc': 'Interest penalty payable directly\nto policyholder on delayed claims.',
                'color': '#F59E0B'
            },
            {
                'value': 'Up to 75%',
                'label': 'Early Surrender Payout',
                'desc': 'Mandatory higher surrender value\neven if terminated after Year 1.',
                'color': '#38BDF8'
            }
        ],
        'framework_title': 'YOUR STATUTORY RIGHTS UNDER IRDAI 2024 MASTER CIRCULAR',
        'bullets': [
            '1. Once all required claim documents are submitted, the insurer cannot raise piecemeal objections after 30 days.',
            '2. Cashless pre-authorization decisions at network hospitals must be communicated within 1 hour of hospital request.',
            '3. Grievances not resolved by the insurer within 14 days can be escalated directly to the Insurance Ombudsman.'
        ],
        'source': 'Source: IRDAI Master Circular on Protection of Policyholders’ Interests & Insurance Ombudsman Mandates'
    },
    {
        'key': 'infographic_csr_vs_icr_matrix',
        'category': 'INSURANCE FORENSICS · RISK METRICS',
        'title': 'Why Claim Settlement Ratio (CSR) Marketing Hides Incurred Claim Ratio (ICR)',
        'subtitle': 'How insurance companies advertise 98% settlement counts while slashing high-value rupee payouts',
        'accent': '#EF4444',
        'cards': [
            {
                'value': '98.5%',
                'label': 'Advertised CSR (Count)',
                'desc': 'Based purely on number of claims.\nSmall ₹10,000 claims mask the stat.',
                'color': '#00D09C'
            },
            {
                'value': '64.2%',
                'label': 'Forensic ICR (Rupees)',
                'desc': 'Net rupees paid out relative to\ntotal net premiums collected.',
                'color': '#EF4444'
            },
            {
                'value': '34.3%',
                'label': 'The Protection Gap',
                'desc': 'Severe deductions applied on\nhigh-value critical illness claims.',
                'color': '#F59E0B'
            }
        ],
        'framework_title': 'HOW TO AUDIT AN INSURER BEFORE PURCHASING',
        'bullets': [
            '1. Claim Settlement Ratio (CSR) tells you how many claims were approved, not how much money was paid out.',
            '2. Incurred Claim Ratio (ICR) between 70% and 85% represents the sweet spot of financial solvency and claim fairness.',
            '3. Insurers with ICR < 55% reject or drastically haircut large hospital bills to maximize underwriting margins.'
        ],
        'source': 'Source: IRDAI Annual Reports & Forensic Policyholder Claim Payout Audits'
    },
    {
        'key': 'infographic_section_45_insurance_act',
        'category': 'LEGAL FORENSICS · STATUTORY RIGHTS',
        'title': 'Section 45 Insurance Act 1938: The 3-Year Incontestability Shield',
        'subtitle': 'Why no life insurance policy in India can be repudiated on any grounds once 3 years have elapsed',
        'accent': '#00D09C',
        'cards': [
            {
                'value': '0 - 36 Mo',
                'label': 'Contestable Window',
                'desc': 'Insurer can investigate claim and\ncontest on proof of material fraud.',
                'color': '#F59E0B'
            },
            {
                'value': '36+ Mo',
                'label': 'Absolute Legal Immunity',
                'desc': 'No policy can be questioned on\nany grounds whatsoever.',
                'color': '#00D09C'
            },
            {
                'value': '100%',
                'label': 'Nominee Protection',
                'desc': 'Statutory guarantee established\nunder amended Section 45.',
                'color': '#38BDF8'
            }
        ],
        'framework_title': 'THE 3 CRITICAL DISCLOSURE RULES FOR FULL PROTECTION',
        'bullets': [
            '1. Truthful disclosure of medical history (diabetes, hypertension, tobacco) in the proposal form is paramount.',
            '2. Once 3 continuous policy years pass from issuance, the insurer loses all legal power to reject a death claim.',
            '3. Supreme Court of India precedents have strictly upheld Section 45, ordering insurers to pay 100% sum assured.'
        ],
        'source': 'Source: Insurance Act 1938 (Amended 2015) & Supreme Court of India Insurance Precedents'
    },
    {
        'key': 'infographic_irdai_proportionate_deduction',
        'category': 'HEALTH INSURANCE · HIDDEN CLAUSES',
        'title': 'IRDAI Proportionate Deduction Math: Room Caps & Claim Cuts',
        'subtitle': 'How choosing a deluxe hospital room triggers a catastrophic 50% slash across your entire surgery bill',
        'accent': '#EF4444',
        'cards': [
            {
                'value': '1% Cap',
                'label': 'Policy Room Sub-Limit',
                'desc': '₹5,000/day limit on a ₹5,00,000\nsum insured basic health policy.',
                'color': '#F59E0B'
            },
            {
                'value': '2x Surge',
                'label': 'Deluxe Room Admitted',
                'desc': 'Patient admitted to ₹10,000/day\nroom (200% of policy limit).',
                'color': '#EF4444'
            },
            {
                'value': '-50% Cut',
                'label': 'Proportionate Slash',
                'desc': 'Insurer cuts doctor fees, surgery,\nand OT charges by 50% across bill.',
                'color': '#EF4444'
            }
        ],
        'framework_title': 'THE PROPORTIONATE DEDUCTION FORMULA EXPLAINED',
        'bullets': [
            '1. Proportionate Formula: Allowed Claim = (Eligible Room Rent / Actual Room Rent) × Total Associated Medical Expenses.',
            '2. A patient with ₹5,00,000 total bill receives only ₹2,50,000 simply for choosing a room that exceeded the daily cap.',
            '3. Solution: Never buy a health insurance policy that contains a room rent sub-limit. Always mandate "No Room Rent Cap".'
        ],
        'source': 'Source: IRDAI Health Insurance Guidelines & Third-Party Administrator (TPA) Billing Protocols'
    },
    {
        'key': 'infographic_crypto_tax_section_115bbh',
        'category': 'CRYPTO TAXATION · COMPLIANCE AUDIT',
        'title': 'Section 115BBH & 194S Forensic Audit: Reconciling AIS / TIS Data',
        'subtitle': 'India’s 30% flat crypto tax, 1% Section 194S TDS matching, and zero loss set-off reality',
        'accent': '#F59E0B',
        'cards': [
            {
                'value': '30% Flat',
                'label': 'Section 115BBH Tax Rate',
                'desc': 'Mandatory flat tax on all crypto\ncapital gains with zero slab relief.',
                'color': '#EF4444'
            },
            {
                'value': '1.0% TDS',
                'label': 'Section 194S On-Chain TDS',
                'desc': 'Deducted on every crypto transfer\nand reported to Income Tax AIS.',
                'color': '#F59E0B'
            },
            {
                'value': '0% Offset',
                'label': 'No Loss Set-Off',
                'desc': 'Losses in one coin CANNOT offset\ngains in another coin under law.',
                'color': '#EF4444'
            }
        ],
        'framework_title': 'INCOME TAX RECONCILIATION PROTOCOL',
        'bullets': [
            '1. On-chain swaps, DEX transactions, and offshore CEX trades are tracked via PAN-linked banking and FIU telemetry.',
            '2. Failing to declare Virtual Digital Asset (VDA) transactions in Schedule VDA triggers automatic Section 148A scrutiny.',
            '3. Maintain complete transaction hash (TxID) archives for all self-custody cold wallets to establish cost of acquisition.'
        ],
        'source': 'Source: Income Tax Act 1961 (Section 115BBH & 194S) & Central Board of Direct Taxes (CBDT) Guidelines'
    },
    {
        'key': 'infographic_crypto_funding_rates',
        'category': 'CRYPTO PERPETUALS · DERIVATIVE ARBITRAGE',
        'title': 'Crypto Funding Rates Explained: Master Perp Structure & Arbitrage',
        'subtitle': 'How 8-hour funding rates maintain perpetual futures parity with spot prices and enable delta-neutral yields',
        'accent': '#38BDF8',
        'cards': [
            {
                'value': '+0.04%',
                'label': 'Positive Funding Rate',
                'desc': 'Longs pay Shorts every 8 hours.\nSignals overleveraged bullish retail.',
                'color': '#00D09C'
            },
            {
                'value': '-0.02%',
                'label': 'Negative Funding Rate',
                'desc': 'Shorts pay Longs every 8 hours.\nSignals aggressive short speculation.',
                'color': '#EF4444'
            },
            {
                'value': '14 - 22%',
                'label': 'Cash & Carry APY',
                'desc': 'Delta-neutral yield achieved by\nholding spot and shorting perp.',
                'color': '#38BDF8'
            }
        ],
        'framework_title': 'THE PERPETUAL FUNDING ARBITRAGE BLUEPRINT',
        'bullets': [
            '1. Funding rates act as an automatic anchor pulling perpetual contract prices back to the underlying spot index.',
            '2. When funding rates reach extreme positive spikes (>0.10% / 8h), markets are vulnerable to devastating long flushes.',
            '3. Institutional quant desks harvest positive funding fees risk-free using spot-perpetual delta-neutral hedging.'
        ],
        'source': 'Source: Binance & Bybit Perpetual Futures Telemetry & Quantitative Deribit Imbalance Models'
    },
    {
        'key': 'infographic_solana_mev_sandwich_bots',
        'category': 'DEFI FORENSICS · ON-CHAIN EXPLOITS',
        'title': 'Solana Memecoin Siphon: How MEV Bots Liquify 99% of Retail Traders',
        'subtitle': 'Anatomy of a DEX sandwich attack: Jito bundles, validator priority fees, and retail slippage extraction',
        'accent': '#EF4444',
        'cards': [
            {
                'value': 'Step 1: Front-Run',
                'label': 'Bot Detects Retail Buy',
                'desc': 'Bot pays high priority fee to buy\ntokens right before retail order.',
                'color': '#F59E0B'
            },
            {
                'value': 'Step 2: Slippage',
                'label': 'Retail Fills at Peak',
                'desc': 'Retail order executes at inflated\nprice due to slippage tolerance.',
                'color': '#EF4444'
            },
            {
                'value': 'Step 3: Back-Run',
                'label': 'Bot Dumps for Profit',
                'desc': 'Bot sells entire bag immediately,\nextracting riskless retail capital.',
                'color': '#00D09C'
            }
        ],
        'framework_title': 'DEFENSIVE ON-CHAIN TRADING PROTOCOLS',
        'bullets': [
            '1. Never use high slippage (>1%) on decentralized exchanges; set maximum slippage tolerance to 0.2% - 0.5%.',
            '2. Utilize private RPC endpoints or MEV-protected routing to prevent mempool transactions from being front-run.',
            '3. 99% of micro-cap liquidity pools on DEXs are dominated by automated arbitrageurs that treat retail as exit liquidity.'
        ],
        'source': 'Source: Solana On-Chain Mempool Telemetry, Jito Bundle Audits & DEX Forensic Research'
    },
    {
        'key': 'infographic_tether_reserve_forensics',
        'category': 'STABLECOIN FORENSICS · SYSTEMIC LIQUIDITY',
        'title': 'The $110B Shadow Engine: Forensic Audit of Tether Reserves & Cantor Fitzgerald',
        'subtitle': 'Deconstructing USDT backing, US Treasury bills portfolio, and global crypto liquidity mechanics',
        'accent': '#00D09C',
        'cards': [
            {
                'value': '$85.0B',
                'label': 'US Treasury Bills',
                'desc': 'Direct and repo exposure to\nshort-term US government debt.',
                'color': '#00D09C'
            },
            {
                'value': '$5.2B',
                'label': 'Physical Gold Bullion',
                'desc': 'LBMA-accredited gold bars stored\nin high-security Swiss vaults.',
                'color': '#F59E0B'
            },
            {
                'value': 'Tier-1 Desk',
                'label': 'Cantor Fitzgerald Custody',
                'desc': 'Wall Street primary broker manages\nand audits sovereign collateral.',
                'color': '#38BDF8'
            }
        ],
        'framework_title': 'STABLECOIN SYSTEMIC LIQUIDITY AUDIT',
        'bullets': [
            '1. Over 77% of Tether’s $110+ billion reserve is held in ultra-liquid, short-duration US Treasury securities yielding >4.5%.',
            '2. Cantor Fitzgerald’s role as primary custodian establishes institutional-grade oversight over sovereign bill reserves.',
            '3. Net operational profit exceeds $1 billion per quarter, creating a capital buffer against extreme market redemption shocks.'
        ],
        'source': 'Source: BDO Independent Assurance Attestation Reports & Cantor Fitzgerald Custody Disclosures'
    }
]

for spec in SPECS:
    img = render_infographic(spec)
    p1 = os.path.join('assets/infographics', f"{spec['key']}.png")
    p2 = os.path.join('public/assets/infographics', f"{spec['key']}.png")
    img.save(p1, 'PNG', optimize=True)
    img.save(p2, 'PNG', optimize=True)
    print(f"Generated {spec['key']}.png ({os.path.getsize(p1):,} bytes)")

print(f"All {len(SPECS)} bespoke infographics rendered successfully!")
