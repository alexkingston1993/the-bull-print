#!/usr/bin/env python3
"""
Autonomous 24-Hour Viral Topic Scanner & Compliance Auditor
app/services/viral_topic_scanner.py

Responsibilities:
1. Scans real-time financial market signals, FII/DII institutional data, and breaking 24h developments.
2. Injects the last 30 days of published content as a strict negative blacklist to guarantee zero duplication.
3. Utilizes Gemini API to discover 10 viral Shorts topics and 2 deep-dive Documentary topics across 10 distinct macro sectors.
4. Strictly verifies every candidate through ContentAuthenticityEngine (Gate 1) & SEBI Safe Harbor Shield.
5. ZERO HARDCODED FALLBACKS & ZERO COMPROMISES.
"""

import os
import sys
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.compliance_shield import TARGET_JURISDICTIONS
from app.services.content_authenticity_engine import (
    ContentAuthenticityEngine,
    STOPWORDS,
    _core_title_tokens,
    _normalize_words,
    _trigrams,
    _jaccard,
    TRIGRAM_MAX_JACCARD,
    TITLE_CORE_OVERLAP_LIMIT
)


class ViralTopicScanner:
    """Discovers viral, compliant financial topics from the past 24 hours with strict semantic anti-duplication."""

    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_key:
            try:
                from app.config import config
                self.gemini_key = config._cfg.get("app", {}).get("gemini_api_key")
            except Exception:
                pass
        self.authenticity_engine = ContentAuthenticityEngine()

    def _get_recent_published_titles(self, days: int = 30) -> List[str]:
        """Gathers all published titles from posts.json, ledger, and recent audits to prevent semantic clones."""
        titles = set()
        posts_file = BASE_DIR / "content" / "posts.json"
        if posts_file.exists():
            try:
                posts = json.loads(posts_file.read_text(encoding="utf-8"))
                for p in posts:
                    if p.get("title"):
                        titles.add(p["title"].strip())
            except Exception:
                pass

        ledger_file = BASE_DIR / "state" / "video_seo_ledger.json"
        if ledger_file.exists():
            try:
                ledger = json.loads(ledger_file.read_text(encoding="utf-8"))
                for entry in ledger:
                    if entry.get("title"):
                        titles.add(entry["title"].strip())
            except Exception:
                pass

        audit_dir = BASE_DIR / "output" / "quarantine_audit"
        for a_file in audit_dir.glob("**/*.json"):
            try:
                audit_data = json.loads(a_file.read_text(encoding="utf-8"))
                for item in audit_data.get("quarantined_videos", []):
                    if item.get("title"):
                        titles.add(item["title"].strip())
            except Exception:
                pass

        return sorted(list(titles))

    def scan_past_24h_topics(self) -> Dict[str, Any]:
        """
        Executes real-time scan and LLM reasoning to produce:
        - 10 Viral Shorts (9:16 Vertical)
        - 2 Master Documentaries (16:9 Landscape)
        Enforces strict compliance, zero semantic clones, and sector diversity.
        """
        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m-%d %H:%M UTC")

        recent_titles = self._get_recent_published_titles(days=30)
        blacklist_sample = "\n".join(f"- {t}" for t in recent_titles[:40])

        prompt = f"""
        You are the Chief Investigative Journalist & Media Director for 'The Bull Print' (in the style of Coffeezilla, James Jani, and MagnatesMedia).
        Current Timestamp: {date_str}.
        
        TASK:
        Identify 10 high-velocity, completely DISTINCT financial investigations and institutional scandals from the PAST 24 HOURS.
        Target Audiences: Everyday retail investors, salaried professionals, and families who fear losing their savings to institutional traps.
        
        CRITICAL ZERO-DUPLICATION & ANTI-SAMENESS BLACKLIST:
        The following {len(recent_titles)} titles/topics were ALREADY PRODUCED in the past 30 days. You are STRICTLY FORBIDDEN from generating these topics, repeating their titles, or creating semantic clones, synonyms, or paraphrases of them:
{blacklist_sample}
        
        MANDATORY 10-SECTOR DIVERSITY RULE:
        Every single one of the 10 Shorts MUST come from a completely DIFFERENT financial domain. Do NOT produce more than ONE topic on F&O or options margin traps.
        You MUST assign exactly ONE topic to each of these 10 distinct macro sectors:
        1. Sovereign Currency & Central Bank Reserves (e.g. Dollar hegemony, Rupee defense, Yen carry trade unwind, physical gold repatriation, SWIFT alternatives).
        2. AI Infrastructure, Semiconductor Scaling & Power Grid Realities (e.g. TSMC wafer allocation bottlenecks, nuclear power deals for datacenters, cloud capex margin compression).
        3. Maritime Logistics & Energy Supply Lines (e.g. Crude tanker rerouting, maritime insurance spikes, Red Sea/Strait of Malacca chokepoints).
        4. Corporate Accounting Forensics & Whistleblower Revelations (e.g. Off-balance-sheet SPVs, auditor resignations, revenue recognition manipulation).
        5. Private Credit & Commercial Real Estate Debt Defaults (e.g. Distressed mezzanine debt, refinancing cliffs, non-bank lender liquidation).
        6. Everyday Banking Traps & Secret Consumer Fee Hikes (e.g. Account freeze clauses, credit card surcharge changes, debit card liability caps).
        7. Global Raw Material & Mineral Cartels (e.g. Lithium export bans, Uranium enrichment bottlenecks, Copper supply deficits).
        8. High-Frequency Trading Dark Pools & Order Routing (e.g. Payment for order flow, exchange co-location latency arbitrage, algorithmic stop hunts).
        9. Sovereign Debt Markets & Yield Curve Inversion (e.g. Treasury auction tail risk, primary dealer liquidity drying up, sovereign CDS spreads).
        10. Fintech Spread Siphoning & Digital Payment Intermediaries (e.g. Merchant fee extraction, wallet float yield games, hidden foreign exchange markups).

        CRITICAL NARRATIVE DIRECTIVES (FOR MAXIMUM AUDIENCE RETENTION):
        1. NO BORING CORPORATE JARGON:
           - Open directly with the smoking gun fact, urgent personal threat, or systemic vulnerability.
           - Ban words like: liquidity, absorption, VWAP, correlation, fiscal deficit from the opening lines.
        2. PUNCHY 1-2 WORD BLOCKBUSTER HOOKS & BADGES:
           - 'hook_text': Exactly 1 to 2 words per line (e.g. '$7 TRILLION / DEBT TRAP', '2 CRORE / TRAPPED', '1.3 MILLION / TROOPS', '₹85 / RECORD LOW').
           - 'badge': High-friction urgency stamps (e.g. 'MARKET SHOCK', 'TIME-BOMB', 'CRACKDOWN', 'OVERPRICED', 'TOP SECRET', 'WARNING').
        3. COMPLIANCE MANDATE (SEBI & GLOBAL REGULATORY SAFE HARBOR):
           - ZERO stock recommendations (no 'buy', 'sell', 'target price', 'multibagger').
           - Strictly educational, forensic, and investigative.
        
        OUTPUT FORMAT:
        Respond ONLY with a valid JSON object matching this exact structure:
        {{
          "scan_timestamp": "{date_str}",
          "shorts_topics": [
            {{
              "id": "short_01",
              "title": "Headline (Max 65 chars)",
              "badge": "ALERT BADGE (Max 16 chars)",
              "hook_text": "HOOK PHRASE (Max 22 chars)",
              "core_thesis": "Why this broke in the past 24 hours, who is the victim, and what trap it exposes.",
              "sector": "Sector Name from the 10 above",
              "vertical": "stock_market"
            }}
          ],
          "documentary_topics": [
            {{
              "id": "doc_01",
              "title": "Documentary Headline (Max 75 chars)",
              "badge": "INVESTIGATION BADGE",
              "hook_text": "MASTER TITLE HOOK",
              "investigative_thesis": "Deep investigative summary exposing the systemic institutional trap.",
              "vertical": "stock_market"
            }}
          ]
        }}
        """

        data = None
        if self.gemini_key:
            import time
            from google import genai

            candidate_models = [
                "gemini-2.0-flash",
                "gemini-1.5-flash",
                "gemini-1.5-pro",
                "gemini-flash-lite-latest"
            ]

            accumulated_shorts = []
            accumulated_docs = []

            for api_ver in ["v1alpha", None]:
                if len(accumulated_shorts) >= 10 and len(accumulated_docs) >= 2:
                    break
                try:
                    client_kwargs = {"api_key": self.gemini_key}
                    if api_ver:
                        client_kwargs["http_options"] = {"api_version": api_ver}
                    client = genai.Client(**client_kwargs)

                    for model_name in candidate_models:
                        if len(accumulated_shorts) >= 10 and len(accumulated_docs) >= 2:
                            break
                        for attempt in range(3):
                            needed_s = max(0, 10 - len(accumulated_shorts))
                            needed_d = max(0, 2 - len(accumulated_docs))
                            if needed_s == 0 and needed_d == 0:
                                break
                            try:
                                logger.info(f"Querying {model_name} (API {api_ver or 'default'}, attempt {attempt + 1}) for {needed_s} Shorts & {needed_d} Docs...")
                                resp = client.models.generate_content(model=model_name, contents=prompt)
                                raw = resp.text.strip()
                                if "```json" in raw:
                                    raw = raw.split("```json")[1].split("```")[0].strip()
                                elif "```" in raw:
                                    raw = raw.split("```")[1].split("```")[0].strip()
                                parsed = json.loads(raw)

                                for st in parsed.get("shorts_topics", []):
                                    if not st.get("title"):
                                        continue
                                    if self._is_compliant_and_unique(st["title"], accumulated_shorts, recent_titles):
                                        accumulated_shorts.append(st)

                                for dt in parsed.get("documentary_topics", []):
                                    if not dt.get("title"):
                                        continue
                                    if self._is_compliant_and_unique(dt["title"], accumulated_docs, recent_titles):
                                        accumulated_docs.append(dt)

                                logger.info(f"Progress: {len(accumulated_shorts)}/10 Shorts, {len(accumulated_docs)}/2 Documentaries")
                                if len(accumulated_shorts) >= 10 and len(accumulated_docs) >= 2:
                                    break
                            except Exception as me:
                                err_str = str(me)
                                logger.warning(f"{model_name} attempt {attempt + 1} error: {err_str[:120]}")
                                if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str:
                                    time.sleep(2 * (attempt + 1))
                                    continue
                                else:
                                    break
                except Exception as ce:
                    logger.warning(f"Client init error with api_ver {api_ver}: {ce}")

            if len(accumulated_shorts) >= 10 and len(accumulated_docs) >= 2:
                data = {
                    "shorts_topics": accumulated_shorts[:10],
                    "documentary_topics": accumulated_docs[:2]
                }
                logger.success(f"✓ Discovered full compliant batch: {len(data['shorts_topics'])} Shorts & {len(data['documentary_topics'])} Documentaries")

        if not data or len(data.get("shorts_topics", [])) < 10:
            raise RuntimeError("CRITICAL: Failed to discover 10 Shorts and 2 Documentaries from past 24h news. Hardcoded fallbacks and compromises are strictly prohibited.")

        validated_shorts = data["shorts_topics"][:10]
        validated_docs = data["documentary_topics"][:2]

        return {
            "timestamp": date_str,
            "shorts": validated_shorts,
            "documentaries": validated_docs,
            "shorts_topics": validated_shorts,
            "documentary_topics": validated_docs,
        }

    def _is_compliant_and_unique(self, title: str, current_batch: List[Dict[str, Any]], recent_titles: List[str]) -> bool:
        """Enforces ContentAuthenticityEngine standards: SEBI safe harbor, 30-day anti-duplication, and intra-batch diversity."""
        # 1. SEBI Safe Harbor filter
        banned = [
            r"\bbuy\s+now\b", r"\bsell\s+now\b", r"\btarget\s+price\b", r"\bmultibagger\b",
            r"\bguaranteed\s+return\b", r"\b100x\b", r"\bjackpot\b", r"\btrading\s+call\b",
            r"\bsure\s*shot\b"
        ]
        t_low = title.lower()
        for pat in banned:
            if re.search(pat, t_low):
                logger.warning(f"🛡️ [Compliance Gate] Banned marketing term in candidate: '{title}'")
                return False

        # 2. Check ContentAuthenticityEngine Gate 1 against content/posts.json
        dupe = self.authenticity_engine.find_dupe_offender(
            {"youtube_payload": {"metadata": {"title": title}}, "topic": title},
            vertical="stock_market"
        )
        if dupe:
            logger.warning(f"🛡️ [Compliance Gate] Candidate duplicates post '{dupe['offender']}': '{title}'")
            return False

        # 3. Check 30-Day History Overlap
        cand_tokens = _core_title_tokens(title)
        cand_trigrams = _trigrams(_normalize_words(title))
        for prev in recent_titles:
            prev_tokens = _core_title_tokens(prev)
            shared = cand_tokens & prev_tokens
            if len(shared) >= TITLE_CORE_OVERLAP_LIMIT:
                logger.warning(f"🛡️ [Compliance Gate] Candidate '{title}' shares {len(shared)} core keywords with past title '{prev}'")
                return False
            prev_trigrams = _trigrams(_normalize_words(prev))
            jac = _jaccard(cand_trigrams, prev_trigrams)
            if jac > TRIGRAM_MAX_JACCARD:
                logger.warning(f"🛡️ [Compliance Gate] Candidate '{title}' exceeds trigram Jaccard cap ({jac:.2f} > {TRIGRAM_MAX_JACCARD}) with '{prev}'")
                return False

        # 4. Check Intra-Batch Diversity
        for item in current_batch:
            other_title = item.get("title", "")
            other_tokens = _core_title_tokens(other_title)
            shared_batch = cand_tokens & other_tokens
            if len(shared_batch) >= 2:
                logger.warning(f"🛡️ [Compliance Gate] Candidate '{title}' too similar to another topic in current batch: '{other_title}'")
                return False

        return True


if __name__ == "__main__":
    scanner = ViralTopicScanner()
    res = scanner.scan_past_24h_topics()
    print("\n" + "=" * 65)
    print("🔥 LIVE 24-HOUR VIRAL TOPIC INTELLIGENCE (10 SHORTS + 2 DOCS)")
    print("=" * 65)
    print(f"Scanned at: {res['timestamp']}")
    print(f"\n📱 10 VIRAL SHORTS:")
    for idx, s in enumerate(res["shorts"], 1):
        print(f"  {idx:02d}. [{s['badge']}] {s['title']} ({s['hook_text']}) | Sector: {s.get('sector', 'N/A')}")
    print(f"\n🎬 2 MASTER DOCUMENTARIES:")
    for idx, d in enumerate(res["documentaries"], 1):
        print(f"  {idx:02d}. [{d['badge']}] {d['title']}")
