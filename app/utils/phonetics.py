"""
Local Christopher Phonetic Preprocessor (app/utils/phonetics.py)

Maps crypto/financial terminology and slang to exact phonetic spellings
for the local zero-shot TTS model (Christopher / F5-TTS / XTTS / Kokoro),
ensuring flawless native pronunciation without mis-tokenization (e.g. 'me-me-coin').

CRITICAL ARCHITECTURE RULE:
Pass normalize_tts_phonetics(script) ONLY to the voice synthesis engine.
Keep original un-modified text for on-screen visual captions and subtitle display!
"""

import re
from typing import Dict

CRYPTO_FINANCE_PHONETICS: Dict[str, str] = {
    # Crypto Slang & Tokens
    r"\bmemecoin\b": "meem coin",
    r"\bmemecoins\b": "meem coins",
    r"\bMemecoin\b": "Meem coin",
    r"\bMemecoins\b": "Meem coins",
    r"\bmempool\b": "mem pool",
    r"\bmempools\b": "mem pools",
    r"\bSOL\b": "Solana",
    r"\bUSDT\b": "U S D T",
    r"\bUSDC\b": "U S D C",
    r"\bDeFi\b": "dee-fie",
    r"\bdefi\b": "dee-fie",
    r"\bTradFi\b": "trad-fie",
    r"\bgwei\b": "gway",
    r"\bzk-SNARK\b": "zee-kay snark",
    r"\baltcoin\b": "ahlt coin",
    r"\baltcoins\b": "ahlt coins",
    r"\bstablecoin\b": "stable coin",
    r"\bstablecoins\b": "stable coins",
    r"\bdApp\b": "dee-app",
    r"\bdApps\b": "dee-apps",
    r"\bRaydium\b": "Ray-dee-um",
    r"\bMeteora\b": "Meh-teh-or-ah",
    r"\bOrca\b": "Or-kuh",

    # Solana & MEV Specifics
    r"\bMEV\b": "M E V",
    r"\bJito\b": "Jee-toh",
    r"\bjito\b": "jee-toh",
    r"\bRPC\b": "R P C",
    r"\bRPCs\b": "R P Cees",
    r"\bfrontrun\b": "front-run",
    r"\bfront-runs\b": "front-runs",
    r"\bbackrun\b": "back-run",
    r"\bbackruns\b": "back-runs",
    r"\bback-runs\b": "back-runs",
    r"\bon-chain\b": "on chain",
    r"\bOn-Chain\b": "On Chain",
    r"\bTWAP\b": "tee-wapp",

    # Institutional & Legal Acronyms
    r"\bNYAG\b": "N Y A G",
    r"\bSDNY\b": "S D N Y",
    r"\bDOJ\b": "D O J",
    r"\bSEC\b": "S E C",
    r"\bCFTC\b": "C F T C",
    r"\bFOMC\b": "F O M C",
    r"\bFDIC\b": "F D I C",
    r"\bT-Bills\b": "Treasury bills",
    r"\bT-bills\b": "treasury bills",
    r"\bbps\b": "basis points",
    r"\bPnL\b": "P and L",
    r"\bAUM\b": "A U M",
    r"\bFII\b": "F I I",
    r"\bDII\b": "D I I",

    # Brand & Domain Pronunciations
    r"thebullprint\.in\b": "the bull print dot I N",
    r"TheBullPrint\.in\b": "The Bull Print dot I N",
    r"@TheBullPrint\b": "at the bull print",
}


def normalize_tts_phonetics(text: str) -> str:
    """
    Replaces crypto/finance terms with phonetic spellings ONLY for the TTS audio input.
    Preserves numbers, punctuation, and converts financial shorthand ($42M -> 42 million dollars).
    """
    if not text:
        return ""

    out = text
    for pattern, phonetic in CRYPTO_FINANCE_PHONETICS.items():
        out = re.sub(pattern, phonetic, out)

    # Convert shorthand currency amounts ($42M, $8.8B, $100K) to spoken words
    out = re.sub(r"\$(\d+(?:\.\d+)?)B\b", r"\1 billion dollars", out)
    out = re.sub(r"\$(\d+(?:\.\d+)?)M\b", r"\1 million dollars", out)
    out = re.sub(r"\$(\d+(?:\.\d+)?)K\b", r"\1 thousand dollars", out)

    # Clean double spaces
    out = re.sub(r"\s{2,}", " ", out).strip()
    return out
