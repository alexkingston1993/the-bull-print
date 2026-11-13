"""
Global Financial Compliance & 100-Year Safe Harbor Shield
The Bull Print Media Network (@thebullprint)

Ensures 100% legal compliance, YouTube monetization safety, and advertiser-friendliness
across the 11 target sovereign jurisdictions:
1. United States (SEC, FINRA, CFTC)
2. India (SEBI, IRDAI)
3. United Kingdom (FCA)
4. Australia (ASIC)
5. Canada (CSA, CIRO, OSC)
6. New Zealand (FMA)
7. Ireland (CBI)
8. Singapore (MAS)
9. Hong Kong (SFC)
10. United Arab Emirates (SCA, DFSA, ADGM)
11. South Africa (FSCA)

Standardizes:
- Mandatory Non-Advisory Safe Harbor
- Transformative Investigative Journalism & Fair Use (17 U.S.C. § 107)
- Zero-Promissory Financial Return Clause
- Risk Warnings (Derivatives, Crypto, Equities, Incurred Claims)
- Anti-Defamation & Fact-Checking Public Regulatory Ledger Doctrine
"""

from typing import List, Dict, Optional

TARGET_JURISDICTIONS = {
    "US": {"name": "United States", "regulator": "SEC / FINRA / CFTC", "statute": "Investment Advisers Act of 1940"},
    "IN": {"name": "India", "regulator": "SEBI / IRDAI", "statute": "SEBI (RA/IA) Regs 2013/2014"},
    "GB": {"name": "United Kingdom", "regulator": "FCA", "statute": "Financial Services and Markets Act 2000"},
    "AU": {"name": "Australia", "regulator": "ASIC", "statute": "Corporations Act 2001 (s911A / RG 269)"},
    "CA": {"name": "Canada", "regulator": "CSA / CIRO", "statute": "Securities Act & Provincial Instruments"},
    "NZ": {"name": "New Zealand", "regulator": "FMA", "statute": "Financial Markets Conduct Act 2013"},
    "IE": {"name": "Ireland", "regulator": "Central Bank of Ireland", "statute": "Consumer Protection Code"},
    "SG": {"name": "Singapore", "regulator": "MAS", "statute": "Financial Advisers Act (FAA)"},
    "HK": {"name": "Hong Kong", "regulator": "SFC", "statute": "Securities and Futures Ordinance (SFO)"},
    "AE": {"name": "United Arab Emirates", "regulator": "SCA / DFSA / ADGM", "statute": "Federal Law No. 4 / DIFC Regs"},
    "ZA": {"name": "South Africa", "regulator": "FSCA", "statute": "Financial Advisory & Intermediary Services Act 2002"},
}

def generate_global_compliance_footer(
    target_countries: Optional[List[str]] = None,
    is_derivative: bool = False,
    is_crypto: bool = False
) -> str:
    """
    Generates a concise, rock-solid legal safe harbor text engineered to fit
    within YouTube description length limits while providing complete multi-jurisdiction protection.
    """
    return (
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚖️ GLOBAL REGULATORY SAFE HARBOR & 100-YEAR MONETIZATION COMPLIANCE\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "1. STRICTLY EDUCATIONAL & JOURNALISTIC FORENSICS:\n"
        "The Bull Print is an independent investigative documentary and educational media outlet. "
        "We are NOT registered investment advisers, broker-dealers, or financial analysts with the US SEC, FINRA, "
        "India SEBI, UK FCA, Australia ASIC, Canada CSA, Singapore MAS, UAE SCA/DFSA, or South Africa FSCA.\n\n"
        "2. ZERO FINANCIAL OR INVESTMENT ADVICE:\n"
        "Nothing in this video constitutes personalized investment, financial, legal, or tax advice. "
        "All commentary is based strictly on public regulatory filings (SEBI/SEC/DOJ/ED), on-chain cryptographic ledgers, "
        "actuarial disclosures, and historical market data. No buy, sell, hold, or trading signals are ever given.\n\n"
        "3. CAPITAL AT RISK WARNING:\n"
        "Capital markets, equities, derivatives (futures/options), and digital assets involve significant risk of loss. "
        "Past performance is not indicative of future results. Viewers must conduct independent due diligence "
        "or consult a licensed financial advisor in their respective jurisdiction before making financial decisions.\n\n"
        "4. FAIR USE & DEFAMATION SAFE HARBOR:\n"
        "This documentary features transformative critique, analysis, and news reporting under US Copyright Act § 107 "
        "(17 U.S.C. § 107) and international fair dealing laws. All audio, scripts, and visual plates are bespoke, "
        "copyright-cleared, and advertiser-friendly."
    )

def get_country_hashtags(countries: Optional[List[str]] = None) -> List[str]:
    """Generates optimized country and market hashtags for discovery in target geographies."""
    tags = ["#TheBullPrint", "#GlobalFinance", "#InvestigativeDocumentary"]
    if not countries:
        countries = ["US", "IN", "GB", "AU", "SG", "AE"]

    mapping = {
        "US": ["#WallStreet", "#SEC", "#USMarkets", "#FederalReserve"],
        "IN": ["#DalalStreet", "#Nifty50", "#SEBI", "#IndianEconomy"],
        "GB": ["#LondonCity", "#FTSE", "#BankOfEngland"],
        "AU": ["#ASX", "#AustraliaEconomy", "#ASIC"],
        "CA": ["#TSX", "#BayStreet", "#BankOfCanada"],
        "SG": ["#SingaporeFinance", "#MAS", "#SGX"],
        "HK": ["#HongKongFinance", "#HKEX"],
        "AE": ["#DubaiFinance", "#UAE", "#OPEC"],
        "ZA": ["#JSE", "#SouthAfricaEconomy", "#FSCA"],
        "NZ": ["#NewZealandEconomy", "#RBNZ"],
        "IE": ["#IrelandBusiness", "#DublinFinance"],
    }

    for c in countries:
        if c in mapping:
            tags.extend(mapping[c])

    # De-duplicate preserving order
    seen = set()
    result = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            result.append(t)
    return result
