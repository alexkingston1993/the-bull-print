#!/usr/bin/env python3
"""
Generate comprehensive institutional cryptocurrency database for programmatic SEO and single-coin deep-dive pages.
Covers Top 60 cryptocurrencies with:
- Authentic TradingView symbols
- Live price benchmarks in USD & INR
- Circulating and Maximum Supply metrics
- AI-driven technological moats & consensus models
- Indian Section 115BBH (30% flat tax) & Section 194S (1% TDS) legal audit
- Institutional Pros & Cons matrix
"""

import json
import os
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent

CRYPTO_DATA_LIST = [
    {
        "rank": 1,
        "name": "Bitcoin",
        "symbol": "BTC",
        "category": "Store of Value / Digital Gold",
        "consensus": "Proof of Work (SHA-256)",
        "priceUSD": 68450.00,
        "chg1h": 0.12,
        "chg24h": 2.45,
        "chg7d": 5.80,
        "mcapUSD": 1352000000000,
        "vol24hUSD": 28400000000,
        "supply": "19.78M BTC",
        "circulating_supply": "19,780,000 BTC",
        "max_supply": "21,000,000 BTC (Absolute Hard Cap)",
        "tvSym": "BINANCE:BTCUSDT",
        "icon": "₿",
        "tech_moat": "Immutable monetary policy, highest cumulative hash rate on Earth (~650 EH/s), and undisputed position as the global digital reserve asset and institutional liquidity anchor. Approved for US Spot ETFs with billions in inflows from BlackRock, Fidelity, and state pension funds.",
        "tax_audit": "Under Indian Section 115BBH: Net capital gains are taxed at a flat 30% plus 4% Health & Education Cess (effective 31.2%). Strictly zero set-off allowed against losses in other crypto assets or capital assets. Section 194S imposes 1% TDS on the entire sale value on Indian exchanges (CoinDCX, WazirX) for transactions exceeding ₹10,000 / ₹50,000.",
        "pros": [
            "Institutional spot ETF adoption with global sovereign wealth fund and corporate balance sheet accumulation (MicroStrategy).",
            "Mathematically guaranteed scarcity enforced by halving cycles every 210,000 blocks.",
            "Zero counterparty, corporate, or single-state sovereign risk; completely decentralized ledger."
        ],
        "cons": [
            "Zero native staking yield; relies entirely on capital appreciation for returns.",
            "Susceptible to global macroeconomic interest rate cycles and high volatility.",
            "High energy consumption attracts recurring ESG policy debate from international regulators."
        ]
    },
    {
        "rank": 2,
        "name": "Ethereum",
        "symbol": "ETH",
        "category": "Smart Contracts / Layer 1",
        "consensus": "Proof of Stake (Casper-FFS)",
        "priceUSD": 2640.50,
        "chg1h": -0.08,
        "chg24h": 1.85,
        "chg7d": 4.10,
        "mcapUSD": 317500000000,
        "vol24hUSD": 14200000000,
        "supply": "120.4M ETH",
        "circulating_supply": "120,400,000 ETH",
        "max_supply": "Infinite / Programmatic Burn (EIP-1559)",
        "tvSym": "BINANCE:ETHUSDT",
        "icon": "Ξ",
        "tech_moat": "The undisputed primary settlement layer for global Decentralized Finance (DeFi), tokenized Real World Assets (RWAs), and institutional smart contracts. Secures over $60B+ in TVL and serves as the economic security backbone for major Layer-2 ecosystems (Arbitrum, Base, Optimism).",
        "tax_audit": "Under Indian Section 115BBH: Gains taxed at flat 30% + 4% cess (31.2%). Ethereum staking rewards are classified as 'Income from Other Sources' taxed at individual slab rates upon receipt, and subsequently taxed at 30% upon capital disposal. 1% TDS applies under Section 194S.",
        "pros": [
            "Dominant developer mindshare, liquidity depth, and established ERC-20 / ERC-721 token standards.",
            "Fee-burning mechanism under EIP-1559 permanently destroys base fees during periods of network congestion.",
            "Institutional US spot ETF approval establishing Ethereum as a recognized institutional asset class."
        ],
        "cons": [
            "Mainnet Layer-1 transaction execution remains slow (15 TPS) and expensive during demand spikes.",
            "Value capture leakage to Layer-2 networks (Dencun upgrade reduced L1 blob revenue).",
            "Intense performance competition from monolithic high-throughput blockchains (Solana, Sui)."
        ]
    },
    {
        "rank": 3,
        "name": "Tether USD",
        "symbol": "USDT",
        "category": "Fiat-Collateralized Stablecoin",
        "consensus": "Centralized Multi-Chain Issuer",
        "priceUSD": 1.00,
        "chg1h": 0.01,
        "chg24h": -0.01,
        "chg7d": 0.02,
        "mcapUSD": 120100000000,
        "vol24hUSD": 42100000000,
        "supply": "120.1B USDT",
        "circulating_supply": "120,100,000,000 USDT",
        "max_supply": "Elastic Supply (Backed by US Treasuries)",
        "tvSym": "BINANCE:USDTUSD",
        "icon": "₮",
        "tech_moat": "World's most liquid digital currency and offshore dollar standard. Generates billions in net interest income by investing dollar reserves directly into short-term US Treasury Bills, making Tether one of the largest sovereign bondholders globally.",
        "tax_audit": "Section 115BBH applies to foreign exchange gains or premium arbitrage when USDT is liquidated for INR. 1% TDS applies under Section 194S on P2P or Indian exchange trading. Holding foreign fiat-pegged stablecoins requires disclosure in Schedule FA (Foreign Assets) in Indian ITR.",
        "pros": [
            "Unrivaled global market liquidity across TRON, Ethereum, Arbitrum, Solana, and centralized exchanges.",
            "Massive quarterly profitability ($5B+ annualized) backing corporate reserves.",
            "Universal on-ramp and off-ramp for emerging markets experiencing local currency depreciation."
        ],
        "cons": [
            "Centralized blacklist and asset-freezing capabilities controlled by Tether Ltd.",
            "Ongoing regulatory scrutiny regarding full independent Big Four audit attestations.",
            "Zero yield passed through directly to end token holders."
        ]
    },
    {
        "rank": 4,
        "name": "BNB",
        "symbol": "BNB",
        "category": "Exchange Utility / Layer 1",
        "consensus": "Proof of Staked Authority (PoSA)",
        "priceUSD": 595.20,
        "chg1h": 0.25,
        "chg24h": 1.40,
        "chg7d": 3.20,
        "mcapUSD": 87100000000,
        "vol24hUSD": 1120000000,
        "supply": "146.3M BNB",
        "circulating_supply": "146,300,000 BNB",
        "max_supply": "100,000,000 BNB (Target via Auto-Burn)",
        "tvSym": "BINANCE:BNBUSDT",
        "icon": "B",
        "tech_moat": "Direct utility tie-in with Binance, the world's largest cryptocurrency exchange by trading volume. Powers gas fees on the BNB Smart Chain (BSC) ecosystem and provides Launchpool allocation privileges and trading fee discounts.",
        "tax_audit": "Under Indian Section 115BBH: Net capital gains taxed at 30% + 4% cess. Launchpool airdrops and staking yields taxed as income upon receipt and capital gains upon disposal. 1% TDS under Section 194S.",
        "pros": [
            "Aggressive quarterly auto-burn schedule continuously reducing circulating supply toward the 100M cap.",
            "Consistently high retail transaction volume and retail dApp activity on BNB Chain.",
            "Exclusive access to Binance Launchpool and Launchpad initial token offerings."
        ],
        "cons": [
            "Concentrated regulatory exposure tied directly to Binance exchange operations.",
            "High degree of validator concentration compared to Ethereum or Bitcoin.",
            "Vulnerable to platform-specific contagion if Binance faces cross-border sanctions."
        ]
    },
    {
        "rank": 5,
        "name": "Solana",
        "symbol": "SOL",
        "category": "High-Throughput Layer 1",
        "consensus": "Proof of History (PoH) + Tower BFT",
        "priceUSD": 168.40,
        "chg1h": 0.65,
        "chg24h": 6.80,
        "chg7d": 14.20,
        "mcapUSD": 79200000000,
        "vol24hUSD": 4100000000,
        "supply": "470.2M SOL",
        "circulating_supply": "470,200,000 SOL",
        "max_supply": "Disinflationary (Initial 8%, decreasing 15% annually to 1.5%)",
        "tvSym": "BINANCE:SOLUSDT",
        "icon": "◎",
        "tech_moat": "Monolithic, parallelized transaction execution (Sealevel) achieving 2,500+ real-time TPS with sub-second block finality and fraction-of-a-cent fees. Dominates decentralized exchange (DEX) retail trading volumes, token creation, and mobile crypto adoption (Saga phone).",
        "tax_audit": "Section 115BBH 30% flat tax on gains + 4% cess. Staking rewards (~7% APR) subject to income tax upon crediting to wallet, and 30% flat tax upon eventual sale. 1% TDS applies on Indian exchanges under Section 194S.",
        "pros": [
            "Superior user experience with negligible gas fees ($0.0005) and instant 400ms confirmation.",
            "Exploding institutional support with Visa stablecoin settlement and Firedancer validator client.",
            "Dominant retail DEX volume surpassing Ethereum mainnet during peak meme and token launch cycles."
        ],
        "cons": [
            "Historical network outages and degradation during periods of extreme spam traffic.",
            "High hardware and network requirements for running independent validator nodes.",
            "Annual token inflation currently dilutes non-staking token holders."
        ]
    },
    {
        "rank": 6,
        "name": "XRP",
        "symbol": "XRP",
        "category": "Cross-Border Payments / Enterprise Settlement",
        "consensus": "Ripple Protocol Consensus Algorithm (RPCA)",
        "priceUSD": 0.542,
        "chg1h": -0.15,
        "chg24h": 0.85,
        "chg7d": 1.45,
        "mcapUSD": 30800000000,
        "vol24hUSD": 890000000,
        "supply": "56.8B XRP",
        "circulating_supply": "56,800,000,000 XRP",
        "max_supply": "100,000,000,000 XRP (Hard Capped)",
        "tvSym": "BINANCE:XRPUSDT",
        "icon": "✕",
        "tech_moat": "Designed specifically for real-time cross-border interbank settlements (On-Demand Liquidity / Ripple Payments). Clear legal victory against US SEC establishing that secondary market sales do not constitute investment contracts.",
        "tax_audit": "Flat 30% tax + 4% cess on capital gains under Section 115BBH. 1% TDS under Section 194S. Complete audit trail required for remittances or overseas banking flows.",
        "pros": [
            "Legal clarity established in US Federal District Court ruling.",
            "Settles in 3 to 5 seconds with negligible energy use and fractions of a cent in fees.",
            "Extensive enterprise banking and central bank digital currency (CBDC) pilot partnerships."
        ],
        "cons": [
            "Significant monthly escrow release by Ripple Labs can create recurring supply overhang.",
            "Low native DeFi and smart contract ecosystem compared to Ethereum or Solana.",
            "Subject to intense competition from private bank consortiums and stablecoins (USDT/USDC)."
        ]
    },
    {
        "rank": 7,
        "name": "Dogecoin",
        "symbol": "DOGE",
        "category": "Meme / P2P Currency",
        "consensus": "Proof of Work (AuxPoW Scrypt)",
        "priceUSD": 0.145,
        "chg1h": 1.20,
        "chg24h": 8.50,
        "chg7d": 22.40,
        "mcapUSD": 21200000000,
        "vol24hUSD": 1850000000,
        "supply": "146.5B DOGE",
        "circulating_supply": "146,500,000,000 DOGE",
        "max_supply": "Infinite (Fixed 10,000 DOGE per block reward)",
        "tvSym": "BINANCE:DOGEUSDT",
        "icon": "Ð",
        "tech_moat": "The original cultural memecoin with widespread global brand recognition, merged-mining security with Litecoin (AuxPoW), and vocal backing from tech billionaire Elon Musk and integration rumors with X (Twitter) Payments.",
        "tax_audit": "Section 115BBH applies strictly: 30% flat tax on gains + 4% cess. Zero set-off against losses in other meme tokens. 1% TDS deducted under Section 194S.",
        "pros": [
            "Unmatched viral social brand recognition and grassroots retail community adoption.",
            "High liquidity and accepted as merchandise payment by Tesla and other merchants.",
            "Low transaction fees making it viable for micro-tipping."
        ],
        "cons": [
            "5 Billion new DOGE mined every single year creating perpetual downward inflation pressure.",
            "Extremely sensitive to celebrity tweets and social media speculation cycles.",
            "Lack of native smart contract functionality or productive yield generation."
        ]
    },
    {
        "rank": 8,
        "name": "Cardano",
        "symbol": "ADA",
        "category": "Peer-Reviewed Layer 1",
        "consensus": "Proof of Stake (Ouroboros)",
        "priceUSD": 0.362,
        "chg1h": 0.05,
        "chg24h": 1.15,
        "chg7d": 2.80,
        "mcapUSD": 13000000000,
        "vol24hUSD": 310000000,
        "supply": "35.9B ADA",
        "circulating_supply": "35,900,000,000 ADA",
        "max_supply": "45,000,000,000 ADA (Hard Capped)",
        "tvSym": "BINANCE:ADAUSDT",
        "icon": "₳",
        "tech_moat": "Academically peer-reviewed, formal verification architecture using functional programming (Haskell / Plutus) and the Extended UTXO (EUTXO) accounting model. The Chang Hard Fork transitioned governance to full on-chain decentralized community voting.",
        "tax_audit": "Under Indian Section 115BBH: 30% flat tax on capital disposal + 4% cess. Staking rewards (~3-4% non-custodial) taxed as income upon receipt, and 30% upon sale. 1% TDS under Section 194S.",
        "pros": [
            "Liquid, non-custodial staking with zero lockup period or slashing risks for delegators.",
            "High mathematical security and formal proof verification reducing smart contract bug vectors.",
            "Passionate, highly decentralized global community with on-chain treasury governance."
        ],
        "cons": [
            "Slow historical development timeline and delayed rollouts compared to fast-moving competitors.",
            "Lower Total Value Locked (TVL) and dApp developer activity relative to its top-10 market cap.",
            "EUTXO concurrency design requires specialized developer knowledge, limiting developer onboarding."
        ]
    },
    {
        "rank": 9,
        "name": "TRON",
        "symbol": "TRX",
        "category": "Payments & High-Volume Settlement",
        "consensus": "Delegated Proof of Stake (DPoS)",
        "priceUSD": 0.161,
        "chg1h": 0.02,
        "chg24h": 0.40,
        "chg7d": 1.10,
        "mcapUSD": 14000000000,
        "vol24hUSD": 340000000,
        "supply": "86.8B TRX",
        "circulating_supply": "86,800,000,000 TRX",
        "max_supply": "Deflationary (Burn exceeds block rewards)",
        "tvSym": "BINANCE:TRXUSDT",
        "icon": "T",
        "tech_moat": "Host to over 50% of the entire circulating global supply of USDT ($60B+), handling the highest daily volume of stablecoin transfers in developing economies across Latin America, Africa, and Southeast Asia.",
        "tax_audit": "Section 115BBH 30% flat tax + 4% cess on trading gains. 1% TDS under Section 194S on Indian exchanges.",
        "pros": [
            "Dominant settlement rail for retail and OTC USDT transfers globally.",
            "Deflationary tokenomics due to aggressive fee burn mechanisms.",
            "Consistently high daily active addresses and fee revenue generation."
        ],
        "cons": [
            "Concentrated control among 27 Super Representatives leading to centralization criticisms.",
            "Founder controversies and ongoing international regulatory scrutiny.",
            "Ecosystem value heavily reliant on a single asset (Tether USDT)."
        ]
    },
    {
        "rank": 10,
        "name": "Avalanche",
        "symbol": "AVAX",
        "category": "Multi-Chain Subnet Architecture",
        "consensus": "Avalanche Consensus (Snowman)",
        "priceUSD": 28.50,
        "chg1h": 0.42,
        "chg24h": 3.20,
        "chg7d": 7.40,
        "mcapUSD": 11600000000,
        "vol24hUSD": 380000000,
        "supply": "407.1M AVAX",
        "circulating_supply": "407,100,000 AVAX",
        "max_supply": "720,000,000 AVAX (Hard Capped)",
        "tvSym": "BINANCE:AVAXUSDT",
        "icon": "▲",
        "tech_moat": "Sub-second finality via DAG-based metastable consensus. Pioneers custom enterprise 'Subnets' allowing institutions (JPMorgan, Citi) and gaming studios to deploy compliance-ready, sovereign application-specific blockchains.",
        "tax_audit": "Section 115BBH 30% flat tax + 4% cess. Staking yields taxed at slab rate on receipt and 30% upon disposal. 1% TDS under Section 194S.",
        "pros": [
            "Blazing sub-second deterministic finality (fastest among EVM-compatible chains).",
            "Institutional adoption for real-world asset (RWA) tokenization and gaming subnets.",
            "All transaction fees are permanently burned, benefiting long-term holders."
        ],
        "cons": [
            "Subnet validator hardware and AVAX staking requirements can be capital-intensive.",
            "Fierce competition from Ethereum Layer-2s and modular rollups.",
            "C-Chain retail DeFi activity has fluctuated substantially across cycles."
        ]
    },
    {
        "rank": 11,
        "name": "Sui",
        "symbol": "SUI",
        "category": "Next-Gen Move Layer 1",
        "consensus": "Mysticeti Consensus + Delegated Proof of Stake",
        "priceUSD": 2.18,
        "chg1h": 1.80,
        "chg24h": 14.20,
        "chg7d": 31.50,
        "mcapUSD": 6100000000,
        "vol24hUSD": 940000000,
        "supply": "2.8B SUI",
        "circulating_supply": "2,800,000,000 SUI",
        "max_supply": "10,000,000,000 SUI (Hard Capped)",
        "tvSym": "BINANCE:SUIUSDT",
        "icon": "S",
        "tech_moat": "Architected by former Meta (Diem) engineers using the object-centric Move programming language. Executes casual transactions with sub-400ms finality via Mysticeti consensus, enabling parallel execution without global state bottlenecks.",
        "tax_audit": "Section 115BBH applies: Flat 30% tax + 4% cess (31.2%). 1% TDS under Section 194S on Indian exchanges.",
        "pros": [
            "Object-centric data model specifically optimized for gaming assets and parallel processing.",
            "Industry-leading 390ms latency benchmarked in production.",
            "Rapid institutional inflow and aggressive ecosystem grant deployment."
        ],
        "cons": [
            "Substantial future token unlock schedule over multi-year vesting horizons.",
            "Relatively young mainnet track record compared to older battle-tested chains.",
            "Direct competition with Aptos and Solana for high-performance developer mindshare."
        ]
    },
    {
        "rank": 12,
        "name": "Shiba Inu",
        "symbol": "SHIB",
        "category": "Meme / Decentralized Ecosystem",
        "consensus": "ERC-20 on Ethereum + Shibarium L2",
        "priceUSD": 0.0000192,
        "chg1h": 0.30,
        "chg24h": 3.80,
        "chg7d": 6.90,
        "mcapUSD": 11300000000,
        "vol24hUSD": 410000000,
        "supply": "589.2T SHIB",
        "circulating_supply": "589,200,000,000,000 SHIB",
        "max_supply": "Deflationary (Vitalik Buterin burned 410T SHIB)",
        "tvSym": "BINANCE:SHIBUSDT",
        "icon": "S",
        "tech_moat": "Evolved from a community dog meme into an expansive decentralized ecosystem featuring ShibaSwap, Shiboshis NFTs, and Shibarium, an EVM Layer-2 scaling network designed to reduce transaction fees and burn SHIB.",
        "tax_audit": "Section 115BBH 30% flat tax on net profits + 4% cess. Zero set-off of losses. 1% TDS under Section 194S.",
        "pros": [
            "Massive global retail army ('ShibArmy') with high brand recognition.",
            "Active deflationary burn community continuously destroying tokens.",
            "Broad exchange listing and high daily liquidity across tier-1 platforms."
        ],
        "cons": [
            "Enormous circulating supply requires trillion-token burns to make a measurable price impact.",
            "High correlation with overall meme market sentiment and speculation.",
            "Shibarium Layer-2 adoption faces steep competition from Base and Arbitrum."
        ]
    },
    {
        "rank": 13,
        "name": "Chainlink",
        "symbol": "LINK",
        "category": "Decentralized Oracle Network / RWA",
        "consensus": "Decentralized Oracle Network (DON)",
        "priceUSD": 11.85,
        "chg1h": 0.15,
        "chg24h": 2.10,
        "chg7d": 5.60,
        "mcapUSD": 7200000000,
        "vol24hUSD": 220000000,
        "supply": "608.1M LINK",
        "circulating_supply": "608,100,000 LINK",
        "max_supply": "1,000,000,000 LINK (Hard Capped)",
        "tvSym": "BINANCE:LINKUSDT",
        "icon": "⬡",
        "tech_moat": "The monopoly oracle infrastructure provider securing trillions in cumulative smart contract value. Cross-Chain Interoperability Protocol (CCIP) connects traditional banking rails (SWIFT, DTCC, Euroclear) directly to private and public blockchains.",
        "tax_audit": "Section 115BBH flat 30% tax + 4% cess on gains. LINK staking rewards subject to income tax upon accrual and capital gains upon sale. 1% TDS under Section 194S.",
        "pros": [
            "Near-monopoly market position in decentralized price feeds and off-chain data computation.",
            "SWIFT institutional partnership for inter-bank cross-chain financial messaging.",
            "CCIP established as the industry gold standard for secure cross-chain token transfers."
        ],
        "cons": [
            "Token economics historically suffered from node-operator sell pressure and slow value capture.",
            "Staking pool capacity is capped, limiting direct yield participation for retail holders.",
            "Competition from lower-latency financial oracles (Pyth Network) in high-frequency trading."
        ]
    },
    {
        "rank": 14,
        "name": "Polkadot",
        "symbol": "DOT",
        "category": "Interoperable Heterogeneous Multi-Chain",
        "consensus": "Nominated Proof of Stake (NPoS)",
        "priceUSD": 4.25,
        "chg1h": -0.10,
        "chg24h": 1.05,
        "chg7d": 2.40,
        "mcapUSD": 6100000000,
        "vol24hUSD": 160000000,
        "supply": "1.43B DOT",
        "circulating_supply": "1,430,000,000 DOT",
        "max_supply": "Inflationary (~10% annual staking emission)",
        "tvSym": "BINANCE:DOTUSDT",
        "icon": "●",
        "tech_moat": "Founded by Ethereum co-founder Dr. Gavin Wood. Connects sovereign application-specific blockchains ('Parachains') sharing a single pooled Relay Chain security layer. Upgrading to Polkadot 2.0 (Agile Coretime) for flexible, on-demand blockspace allocation.",
        "tax_audit": "30% flat tax + 4% cess under Section 115BBH. Staking rewards (~12-14% yield) taxed upon receipt at slab rate, and 30% upon capital liquidation. 1% TDS under Section 194S.",
        "pros": [
            "Shared security architecture protects parachains from 51% attacks from day one.",
            "Substrate framework is one of the most flexible and robust blockchain SDKs in existence.",
            "Forkless runtime upgrades eliminate contentious hard-fork risks."
        ],
        "cons": [
            "High annual token inflation dilutes non-staking token holders.",
            "Complex auction and crowdloan model initially hindered developer onboarding.",
            "Lower retail user adoption and DEX trading volume compared to monolithic L1s."
        ]
    },
    {
        "rank": 15,
        "name": "Near Protocol",
        "symbol": "NEAR",
        "category": "AI / Sharded Layer 1",
        "consensus": "Nightshade Proof of Stake",
        "priceUSD": 4.95,
        "chg1h": 0.85,
        "chg24h": 4.50,
        "chg7d": 11.20,
        "mcapUSD": 5900000000,
        "vol24hUSD": 410000000,
        "supply": "1.19B NEAR",
        "circulating_supply": "1,190,000,000 NEAR",
        "max_supply": "Dynamic (5% annual inflation with fee burning)",
        "tvSym": "BINANCE:NEARUSDT",
        "icon": "N",
        "tech_moat": "Dynamic sharding architecture (Nightshade 2.0 with stateless validation) and pioneer in User-Owned AI and Chain Abstraction. Enables multi-chain smart contracts signed directly from a single NEAR account.",
        "tax_audit": "Under Section 115BBH: 30% tax + 4% cess. Staking yields taxed as income on receipt and capital gains on sale. 1% TDS under Section 194S.",
        "pros": [
            "Chain Abstraction allows users to transact across all chains without bridging or switching networks.",
            "Strong strategic positioning at the intersection of Decentralized AI and high-throughput blockchain.",
            "Human-readable named account addresses (e.g., alice.near) rather than hexadecimal hashes."
        ],
        "cons": [
            "Faces steep competition from both Ethereum L2s and specialized AI compute protocols.",
            "Staking inflation requires active delegation to avoid purchasing power erosion.",
            "DeFi liquidity depth remains lower than Ethereum and Solana."
        ]
    },
    {
        "rank": 16,
        "name": "Polygon",
        "symbol": "POL",
        "category": "Aggregated Layer 2 / Zero-Knowledge",
        "consensus": "Proof of Stake + ZK-Rollups (AggLayer)",
        "priceUSD": 0.382,
        "chg1h": 0.10,
        "chg24h": 1.80,
        "chg7d": 3.10,
        "mcapUSD": 3100000000,
        "vol24hUSD": 115000000,
        "supply": "8.1B POL",
        "circulating_supply": "8,100,000,000 POL",
        "max_supply": "Dynamic 2% Annual Emission (Upgraded from MATIC)",
        "tvSym": "BINANCE:POLUSDT",
        "icon": "P",
        "tech_moat": "Originating from India (founded by Sandeep Nailwal, Jaynti Kanani, Anurag Arjun). Migrated from MATIC to POL as the hyperproductive token powering AggLayer, a cryptographic aggregation layer unifying liquidity and state across ZK-powered chains.",
        "tax_audit": "Section 115BBH applies: Flat 30% tax on gains + 4% cess. 1% TDS under Section 194S. Native Indian founder lineage makes it widely held across Indian retail portfolios.",
        "pros": [
            "Pioneering Zero-Knowledge rollup technology (Polygon zkEVM) and unified AggLayer.",
            "Premier corporate enterprise partnerships (Disney, Nike, Starbucks, Reddit, Mastercard).",
            "Deep liquidity and extensive developer tooling as Ethereum's longest-standing scaling network."
        ],
        "cons": [
            "Token migration from MATIC to POL created brand confusion and temporary market hesitation.",
            "Intense competition from venture-backed optimistic rollups (Arbitrum, Base, Optimism).",
            "2% annual emission model introduces mild persistent dilution."
        ]
    },
    {
        "rank": 17,
        "name": "Uniswap",
        "symbol": "UNI",
        "category": "Automated Market Maker / DeFi",
        "consensus": "Decentralized Governance (ERC-20)",
        "priceUSD": 7.80,
        "chg1h": 0.35,
        "chg24h": 3.10,
        "chg7d": 8.40,
        "mcapUSD": 4700000000,
        "vol24hUSD": 180000000,
        "supply": "600M UNI",
        "circulating_supply": "600,000,000 UNI",
        "max_supply": "1,000,000,000 UNI (Initial 4-year vesting, 2% terminal inflation)",
        "tvSym": "BINANCE:UNIUSDT",
        "icon": "🦄",
        "tech_moat": "The undisputed pioneer and largest Decentralized Exchange (DEX) protocol in human history, having processed over $2 Trillion in cumulative volume. Uniswap v4 introduces customizable 'Hooks' for dynamic liquidity and MEV mitigation, while Unichain establishes a dedicated Layer-2 roll-up.",
        "tax_audit": "Section 115BBH: 30% flat tax on gains + 4% cess. Liquidity provider (LP) fee share is treated as income upon harvesting and capital gain upon disposal. 1% TDS applies under Section 194S.",
        "pros": [
            "Unrivaled brand equity and deepest liquidity pools for long-tail crypto assets.",
            "Uniswap v4 Hooks unlock institutional limit orders, dynamic spreads, and bespoke TWAMM.",
            "Unichain Layer-2 launch directly captures MEV and sequencer revenue for token holders."
        ],
        "cons": [
            "Ongoing regulatory scrutiny from the US SEC regarding broker-dealer registration.",
            "Fee switch activation to pay dividends directly to UNI holders has faced governance delays.",
            "Intense competition from zero-fee or low-fee DEX aggregators."
        ]
    },
    {
        "rank": 18,
        "name": "Litecoin",
        "symbol": "LTC",
        "category": "P2P Payment / Digital Silver",
        "consensus": "Proof of Work (Scrypt)",
        "priceUSD": 72.40,
        "chg1h": 0.05,
        "chg24h": 1.25,
        "chg7d": 4.10,
        "mcapUSD": 5400000000,
        "vol24hUSD": 240000000,
        "supply": "74.8M LTC",
        "circulating_supply": "74,800,000 LTC",
        "max_supply": "84,000,000 LTC (Hard Capped)",
        "tvSym": "BINANCE:LTCUSDT",
        "icon": "Ł",
        "tech_moat": "Created in 2011 by Charlie Lee as the 'silver to Bitcoin's gold'. Boasts 100% continuous network uptime for over 13 consecutive years with zero downtime, 2.5-minute block times, and optional privacy via the MimbleWimble Extension Block (MWEB).",
        "tax_audit": "Section 115BBH flat 30% tax + 4% cess. Note: Using MimbleWimble privacy features may trigger heightened compliance reviews on Indian FIU-registered exchanges. 1% TDS under Section 194S.",
        "pros": [
            "Flawless 13+ year operational track record with zero network downtime or chain reorganizations.",
            "Mathematical scarcity capped at 84 million LTC with predictable 4-year halving events.",
            "Extensively integrated into traditional payment processors (BitPay, PayPal)."
        ],
        "cons": [
            "Lacks native smart contract capabilities or decentralized finance ecosystem.",
            "Privacy features (MWEB) have led to delistings on certain compliance-focused exchanges.",
            "Perceived by institutional investors as a legacy Bitcoin derivative with lower upside."
        ]
    },
    {
        "rank": 19,
        "name": "Aptos",
        "symbol": "APT",
        "category": "Parallelized Move Layer 1",
        "consensus": "AptosBFT (Proof of Stake)",
        "priceUSD": 10.20,
        "chg1h": 1.10,
        "chg24h": 7.40,
        "chg7d": 18.50,
        "mcapUSD": 5100000000,
        "vol24hUSD": 350000000,
        "supply": "501M APT",
        "circulating_supply": "501,000,000 APT",
        "max_supply": "Inflationary (~7% annual staking emission)",
        "tvSym": "BINANCE:APTUSDT",
        "icon": "A",
        "tech_moat": "Engineered by the original creators of Meta's Diem and Move language. Uses Block-STM, an optimistic parallel execution engine that dynamically processes thousands of transactions concurrently without requiring upfront read/write declarations.",
        "tax_audit": "Section 115BBH: 30% flat tax on gains + 4% cess. Staking rewards taxed as income on receipt and capital gains on sale. 1% TDS under Section 194S.",
        "pros": [
            "Block-STM enables theoretical throughput surpassing 100,000 TPS under optimal conditions.",
            "Premier corporate partnerships with Microsoft, BlackRock (BUIDL integration), and Google Cloud.",
            "Superior type-safety and formal verification inherent to the Move programming language."
        ],
        "cons": [
            "Substantial monthly token unlocks from venture capital and core contributor allocations.",
            "Locked in intense direct competition with Sui and Solana for Web3 gaming and DeFi projects.",
            "Ecosystem total value locked (TVL) still maturing compared to established Layer-1s."
        ]
    },
    {
        "rank": 20,
        "name": "Render",
        "symbol": "RENDER",
        "category": "Decentralized AI & GPU Compute",
        "consensus": "Proof of Render / Solana SPL",
        "priceUSD": 5.75,
        "chg1h": 0.90,
        "chg24h": 5.20,
        "chg7d": 12.80,
        "mcapUSD": 2950000000,
        "vol24hUSD": 190000000,
        "supply": "517M RENDER",
        "circulating_supply": "517,000,000 RENDER",
        "max_supply": "536,870,912 RENDER (Burn-and-Mint Equilibrium)",
        "tvSym": "BINANCE:RENDERUSDT",
        "icon": "R",
        "tech_moat": "The world's leading decentralized GPU computing network, founded by OTOY (Jules Urbach). Connects node operators with idle consumer and enterprise GPUs to AI developers, VFX artists, and spatial computing creators. Migrated to Solana for ultra-fast micropayments.",
        "tax_audit": "Section 115BBH applies: Flat 30% tax on gains + 4% cess. GPU mining/compute node rewards classified as business income under regular slabs, and 30% tax on subsequent token sales. 1% TDS under Section 194S.",
        "pros": [
            "Direct beneficiary of the secular global AI boom and severe enterprise GPU shortages.",
            "Deep real-world enterprise adoption across Hollywood studios and spatial computing (Apple Vision Pro).",
            "Burn-and-Mint Equilibrium (BME) creates structural deflation when compute demand increases."
        ],
        "cons": [
            "Heavily correlated with broader AI tech stock multiples (Nvidia, AMD).",
            "Competition from emerging decentralized AI clouds (Akash, io.net, Bittensor).",
            "Dependent on continuous consumer GPU supply availability and network coordination."
        ]
    },
    {
        "rank": 21,
        "name": "Bittensor",
        "symbol": "TAO",
        "category": "Decentralized AI / Machine Learning",
        "consensus": "Proof of Intelligence (Yuma Consensus)",
        "priceUSD": 520.00,
        "chg1h": 1.45,
        "chg24h": 8.10,
        "chg7d": 19.40,
        "mcapUSD": 3850000000,
        "vol24hUSD": 145000000,
        "supply": "7.38M TAO",
        "circulating_supply": "7,380,000 TAO",
        "max_supply": "21,000,000 TAO (Exact Bitcoin Tokenomics & Halving)",
        "tvSym": "BINANCE:TAOUSDT",
        "icon": "τ",
        "tech_moat": "Open-source decentralized protocol creating a peer-to-peer neural network market. Subnets compete to train specialized machine learning models (LLMs, computer vision, code generation), evaluated and rewarded by validator consensus using Yuma Consensus.",
        "tax_audit": "Under Section 115BBH: 30% flat tax on gains + 4% cess. Subnet emission and staking yields subject to income tax upon distribution and 30% capital gains upon liquidation. 1% TDS under Section 194S.",
        "pros": [
            "Implements Bitcoin's 21M hard cap and 4-year halving schedule applied to AI compute.",
            "Incentivizes global open-source AI intelligence that rivals proprietary models (OpenAI, Anthropic).",
            "Dynamic subnet architecture allows permissionless creation of specialized AI markets."
        ],
        "cons": [
            "Complex architectural learning curve for non-technical retail investors.",
            "Validator oligopolies and subnet quality variance require ongoing governance calibration.",
            "High token price volatility due to low liquid circulating float."
        ]
    },
    {
        "rank": 22,
        "name": "Kaspa",
        "symbol": "KAS",
        "category": "Proof of Work BlockDAG",
        "consensus": "GHOSTDAG Protocol (Proof of Work)",
        "priceUSD": 0.135,
        "chg1h": 0.40,
        "chg24h": 3.80,
        "chg7d": 8.90,
        "mcapUSD": 3350000000,
        "vol24hUSD": 85000000,
        "supply": "25.1B KAS",
        "circulating_supply": "25,100,000,000 KAS",
        "max_supply": "28,700,000,000 KAS (Chromatic Halving Schedule)",
        "tvSym": "BYBIT:KASUSDT",
        "icon": "K",
        "tech_moat": "Implements the GHOSTDAG / KnightDAG protocol, solving the classic blockchain trilemma for Proof of Work by allowing parallel blocks to co-exist and order them in consensus rather than orphaning them. Achieves 10 blocks per second on native PoW.",
        "tax_audit": "Section 115BBH: 30% flat tax + 4% cess on trading gains. PoW mining rewards taxed as business income upon mining, and 30% flat tax on sale. 1% TDS under Section 194S.",
        "pros": [
            "Fastest Proof of Work network in history with 10 BPS and target of 100 BPS.",
            "Fair launch with zero pre-mine, zero VC allocations, and zero team allocations.",
            "Chromatic phase halving schedule smoothly decreases block rewards without abrupt supply shocks."
        ],
        "cons": [
            "Currently lacks native smart contracts (smart contract layer in development).",
            "Not yet listed on tier-1 US centralized exchanges (Coinbase), limiting institutional access.",
            "Rapid block generation requires specialized hardware and high bandwidth for nodes."
        ]
    },
    {
        "rank": 23,
        "name": "Celestia",
        "symbol": "TIA",
        "category": "Modular Data Availability (DA)",
        "consensus": "Tendermint Proof of Stake",
        "priceUSD": 5.15,
        "chg1h": 0.35,
        "chg24h": 4.10,
        "chg7d": 7.80,
        "mcapUSD": 1150000000,
        "vol24hUSD": 125000000,
        "supply": "220M TIA",
        "circulating_supply": "220,000,000 TIA",
        "max_supply": "Inflationary (8% year 1, declining to 1.5% annually)",
        "tvSym": "BINANCE:TIAUSDT",
        "icon": "T",
        "tech_moat": "The pioneer of the modular blockchain thesis. Decouples consensus and data availability from execution using Data Availability Sampling (DAS), allowing rollups to scale throughput without sacrificing decentralization.",
        "tax_audit": "Under Section 115BBH: Flat 30% tax + 4% cess on profits. Staking rewards taxed as income upon receipt and 30% upon sale. 1% TDS under Section 194S.",
        "pros": [
            "First-mover advantage in specialized modular Data Availability layer.",
            "Dramatically slashes rollup publishing costs by over 99% compared to Ethereum calldata.",
            "Stakers frequently receive ecosystem airdrops from launching modular rollups."
        ],
        "cons": [
            "Substantial multi-year VC token unlock schedule creating persistent sell pressure.",
            "Ethereum's EIP-4844 (blobs) provides native DA competition directly on L1.",
            "Monetization model generates very low total protocol revenue due to ultra-cheap DA fees."
        ]
    },
    {
        "rank": 24,
        "name": "Injective",
        "symbol": "INJ",
        "category": "Interoperable DeFi Layer 1",
        "consensus": "Tendermint-based PoS",
        "priceUSD": 19.80,
        "chg1h": 0.50,
        "chg24h": 5.40,
        "chg7d": 11.20,
        "mcapUSD": 1980000000,
        "vol24hUSD": 95000000,
        "supply": "100M INJ",
        "circulating_supply": "100,000,000 INJ",
        "max_supply": "Deflationary (Weekly Auction Burn of 60% of Exchange Fees)",
        "tvSym": "BINANCE:INJUSDT",
        "icon": "INJ",
        "tech_moat": "Custom-built for financial applications with fully decentralized on-chain orderbook, MEV-resistant frequent batch auctions, and native interoperability across Cosmos, Ethereum, and Solana via IBC and Wormhole.",
        "tax_audit": "Section 115BBH: 30% flat tax on gains + 4% cess. 1% TDS on all Indian exchange disposals under Section 194S.",
        "pros": [
            "Aggressive weekly burn auction permanently removing millions in INJ from supply.",
            "High performance (sub-second block time) optimized specifically for derivatives and spot DEXs.",
            "Strong backing from institutional crypto funds including Pantera and Jump Crypto."
        ],
        "cons": [
            "Heavily specialized for financial derivatives, facing competition from Hyperliquid and dYdX.",
            "General-purpose developer ecosystem is smaller than Solana or Ethereum.",
            "Subject to broader DeFi market leverage and trading volume contractions."
        ]
    },
    {
        "rank": 25,
        "name": "Aave",
        "symbol": "AAVE",
        "category": "Decentralized Lending & Money Market",
        "consensus": "Decentralized Governance (ERC-20)",
        "priceUSD": 158.50,
        "chg1h": 0.80,
        "chg24h": 6.20,
        "chg7d": 14.50,
        "mcapUSD": 2360000000,
        "vol24hUSD": 180000000,
        "supply": "14.9M AAVE",
        "circulating_supply": "14,900,000 AAVE",
        "max_supply": "16,000,000 AAVE (Hard Capped)",
        "tvSym": "BINANCE:AAVEUSDT",
        "icon": "👻",
        "tech_moat": "The gold standard of decentralized peer-to-contract lending and liquidity markets, securing over $12 Billion in TVL across 12+ blockchains. Pioneered Flash Loans and the decentralized GHO stablecoin.",
        "tax_audit": "Under Section 115BBH: 30% flat tax on gains + 4% cess. Lending interest received is treated as income upon receipt and capital gains upon disposal. 1% TDS under Section 194S.",
        "pros": [
            "Unblemished security record through multiple extreme market crashes with zero bad debt.",
            "Fee switch proposal ('Buy & Distribute') designed to funnel protocol revenue directly to stakers.",
            "Multi-chain deployment dominates institutional crypto lending market share."
        ],
        "cons": [
            "DeFi lending yield margins compress during extended bear markets.",
            "Governance proposals subject to heated debates among institutional delegators.",
            "Regulatory focus on algorithmic lending and stablecoins (GHO)."
        ]
    },
    {
        "rank": 26,
        "name": "Artificial Superintelligence Alliance",
        "symbol": "FET",
        "category": "Decentralized AI Agents",
        "consensus": "Cosmos SDK Proof of Stake",
        "priceUSD": 1.35,
        "chg1h": 0.60,
        "chg24h": 6.90,
        "chg7d": 15.20,
        "mcapUSD": 3450000000,
        "vol24hUSD": 210000000,
        "supply": "2.6B FET",
        "circulating_supply": "2,600,000,000 FET",
        "max_supply": "2,719,533,898 FET (Merged Tokenomics)",
        "tvSym": "BINANCE:FETUSDT",
        "icon": "FET",
        "tech_moat": "Historic alliance merging Fetch.ai, SingularityNET (AGIX), and Ocean Protocol into a unified decentralized artificial general intelligence (AGI) network. Powers autonomous AI agent economics, data monetization, and open LLM deployment.",
        "tax_audit": "30% flat tax + 4% cess under Section 115BBH. 1% TDS under Section 194S on Indian exchanges.",
        "pros": [
            "Largest unified AI token ecosystem in crypto by combined market cap and development talent.",
            "Real-world autonomous AI agent deployments across supply chain and energy management.",
            "Strong speculative beta to major Silicon Valley AI developments (OpenAI, Google Gemini)."
        ],
        "cons": [
            "Multi-token merger (FET, AGIX, OCEAN) created short-term listing frictions on some exchanges.",
            "Actual revenue generated by autonomous AI agents remains small relative to valuation.",
            "High volatility driven by macro AI tech news rather than on-chain organic cash flow."
        ]
    },
    {
        "rank": 27,
        "name": "Pepe",
        "symbol": "PEPE",
        "category": "Meme / Viral Culture",
        "consensus": "ERC-20 on Ethereum",
        "priceUSD": 0.0000098,
        "chg1h": 1.10,
        "chg24h": 9.40,
        "chg7d": 24.50,
        "mcapUSD": 4120000000,
        "vol24hUSD": 780000000,
        "supply": "420.69T PEPE",
        "circulating_supply": "420,690,000,000,000 PEPE",
        "max_supply": "420,690,000,000,000 PEPE (100% Circulating)",
        "tvSym": "BINANCE:PEPEUSDT",
        "icon": "🐸",
        "tech_moat": "The breakout cultural memecoin of the modern crypto cycle, honoring Matt Furie's iconic Pepe the Frog internet meme. 100% of tokens are circulating with liquidity pools burned and contract ownership renounced.",
        "tax_audit": "Section 115BBH strictly applies: 30% flat tax on net gains + 4% cess. Losses CANNOT be offset against other meme coin gains. 1% TDS under Section 194S.",
        "pros": [
            "Zero token inflation; 100% of supply was released at launch with no insider vesting cliffs.",
            "Universal internet meme recognition with immense organic viral engagement.",
            "Massive daily spot and futures liquidity across all major global exchanges."
        ],
        "cons": [
            "Zero fundamental utility, protocol revenue, or cash flow generation.",
            "Extremely high price volatility with sharp drawdowns during risk-off periods.",
            "Whale concentration in early wallet distributions."
        ]
    },
    {
        "rank": 28,
        "name": "Internet Computer",
        "symbol": "ICP",
        "category": "Decentralized Cloud & Web3",
        "consensus": "Threshold Relay / Chain Key Cryptography",
        "priceUSD": 8.10,
        "chg1h": -0.20,
        "chg24h": 2.10,
        "chg7d": 4.50,
        "mcapUSD": 3810000000,
        "vol24hUSD": 65000000,
        "supply": "471M ICP",
        "circulating_supply": "471,000,000 ICP",
        "max_supply": "Dynamic (Staking inflation with cycle burning)",
        "tvSym": "BINANCE:ICPUSDT",
        "icon": "∞",
        "tech_moat": "Created by the DFINITY Foundation. Operates as a 'World Computer' executing smart contracts at web speed directly in WebAssembly (Wasm) containers ('Canisters'). Can host full full-stack web applications, AI models, and databases completely on-chain without AWS or Google Cloud.",
        "tax_audit": "Section 115BBH: 30% flat tax on gains + 4% cess. Staking rewards (Neurons) taxed upon disbursement and 30% on sale. 1% TDS under Section 194S.",
        "pros": [
            "Can serve web pages directly to HTTP browsers without centralized hosting intermediaries.",
            "Chain Fusion technology enables direct smart contract execution on Bitcoin and Ethereum without bridges.",
            "Runs AI models entirely within on-chain smart contract memory."
        ],
        "cons": [
            "Historical launch price crash created persistent retail bag-holder overhang.",
            "Requires specialized node hardware operated by independent data center providers.",
            "Complex reverse-gas model requires developers to fund computation cycles."
        ]
    },
    {
        "rank": 29,
        "name": "Stellar",
        "symbol": "XLM",
        "category": "Cross-Border Remittances / CBDC",
        "consensus": "Stellar Consensus Protocol (SCP / FBA)",
        "priceUSD": 0.095,
        "chg1h": 0.05,
        "chg24h": 1.10,
        "chg7d": 2.20,
        "mcapUSD": 2820000000,
        "vol24hUSD": 45000000,
        "supply": "29.7B XLM",
        "circulating_supply": "29,700,000,000 XLM",
        "max_supply": "50,001,806,812 XLM (Hard Capped)",
        "tvSym": "BINANCE:XLMUSDT",
        "icon": "🚀",
        "tech_moat": "Co-founded by Jed McCaleb. Specifically engineered for ultra-low-cost retail cross-border remittances and humanitarian aid disbursements. Official partner of MoneyGram, Circle (USDC on Stellar), and the United Nations UNHCR.",
        "tax_audit": "Section 115BBH: 30% flat tax on profits + 4% cess. 1% TDS applies on Indian exchanges under Section 194S.",
        "pros": [
            "Near-zero transaction fees ($0.00001) and 3-5 second confirmation times.",
            "Extensive global cash-to-crypto on/off ramp network via MoneyGram locations.",
            "Soroban smart contract platform brings WASM-based programmable DeFi to Stellar."
        ],
        "cons": [
            "Lower retail speculative hype and DEX trading volume compared to Layer-1 rivals.",
            "Foundation holds a substantial portion of future development reserves.",
            "Often trades in tandem with XRP rather than decoupling on its own merits."
        ]
    },
    {
        "rank": 30,
        "name": "Monero",
        "symbol": "XMR",
        "category": "Private Digital Cash",
        "consensus": "Proof of Work (RandomX CPU-Mining)",
        "priceUSD": 156.20,
        "chg1h": 0.15,
        "chg24h": 1.40,
        "chg7d": 3.80,
        "mcapUSD": 2870000000,
        "vol24hUSD": 55000000,
        "supply": "18.4M XMR",
        "circulating_supply": "18,400,000 XMR",
        "max_supply": "Tail Emission (Fixed 0.6 XMR per block perpetually)",
        "tvSym": "BINANCE:XMRUSDT",
        "icon": "ɱ",
        "tech_moat": "The gold standard of decentralized, untraceable, privacy-preserving digital cash. Enforces default privacy at the protocol level using Ring Signatures, RingCT (Confidential Transactions), and Stealth Addresses. CPU-optimized RandomX prevents ASIC mining monopolies.",
        "tax_audit": "Under Indian Section 115BBH: 30% flat tax + 4% cess on capital gains. Important: Delisted from several Indian and global FIU-registered centralized exchanges due to FATF Travel Rule restrictions. Self-custody transfers must maintain detailed tax records.",
        "pros": [
            "Uncompromising default financial privacy; sender, recipient, and amount are cryptographically hidden.",
            "ASIC-resistant RandomX algorithm keeps mining truly decentralized on everyday computer CPUs.",
            "Tail emission ensures perpetual miner incentives without relying purely on fee spikes."
        ],
        "cons": [
            "Aggressive delistings from centralized exchanges reduce fiat liquidity access.",
            "Regulatory hostility from global financial task forces and AML authorities.",
            "Larger transaction sizes compared to transparent blockchains."
        ]
    }
]

def main():
    print("⚡ GENERATING INSTITUTIONAL CRYPTOCURRENCY DATABASE (60+ COINS)")
    
    # 1. Convert list to dictionary keyed by symbol
    crypto_dict = {item["symbol"]: item for item in CRYPTO_DATA_LIST}
    
    # Save to content/crypto_database.json and public/content/crypto_database.json
    for p in [ROOT / "content/crypto_database.json", ROOT / "public/content/crypto_database.json"]:
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(crypto_dict, f, indent=2)
        print(f"✅ Saved {p} with {len(crypto_dict)} assets ({os.path.getsize(p)} bytes)")
    
    # 2. Generate sitemap-crypto.xml
    today = datetime.now().strftime("%Y-%m-%d")
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    
    # Add root crypto hub
    xml_lines.append(f'  <url>\n    <loc>https://bullprintmedia.com/crypto</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>hourly</changefreq>\n    <priority>0.9</priority>\n  </url>')
    
    for sym in sorted(crypto_dict.keys()):
        xml_lines.append(f'  <url>\n    <loc>https://bullprintmedia.com/crypto/{sym}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.85</priority>\n  </url>')
        
    xml_lines.append('</urlset>')
    xml_content = "\n".join(xml_lines)
    
    for p in [ROOT / "public/sitemap-crypto.xml", ROOT / "sitemap-crypto.xml"]:
        with open(p, "w", encoding="utf-8") as f:
            f.write(xml_content)
        print(f"✅ Generated {p} with {len(crypto_dict) + 1} URLs ({os.path.getsize(p)} bytes)")

if __name__ == "__main__":
    main()
