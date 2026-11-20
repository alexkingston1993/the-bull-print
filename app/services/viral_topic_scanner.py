#!/usr/bin/env python3
"""
Autonomous 24-Hour Viral Topic Scanner & Compliance Auditor
app/services/viral_topic_scanner.py

Responsibilities:
1. Scans real-time financial market signals, FII/DII institutional data, and breaking 24h developments.
2. Injects the last 180 days of published content as a strict negative blacklist to guarantee zero duplication.
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


def fetch_live_financial_rss_headlines() -> List[str]:
    """Fetches breaking real-world financial catalysts from live RSS feeds to ground topics in reality."""
    import urllib.request
    import xml.etree.ElementTree as ET

    FEEDS = [
        ("MarketWatch", "https://feeds.content.dowjones.io/public/rss/mw_topstories"),
        ("CNBC", "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664"),
        ("EconomicTimes", "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"),
        ("Investing", "https://www.investing.com/rss/news.rss"),
    ]
    headlines = []
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

    for source, url in FEEDS:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=6) as response:
                root = ET.fromstring(response.read())
                for it in root.findall(".//item"):
                    t_el = it.find("title")
                    if t_el is not None and t_el.text:
                        cleaned = t_el.text.strip()
                        if len(cleaned) > 15 and cleaned not in headlines:
                            headlines.append(f"[{source}] {cleaned}")
                            if len(headlines) >= 40:
                                break
        except Exception as e:
            logger.warning(f"RSS feed fetch error for {source}: {e}")

    logger.info(f"✓ Fetched {len(headlines)} live RSS breaking financial headlines for grounding.")
    return headlines[:35]


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

    def _get_recent_published_titles(self, days: int = 180) -> List[str]:
        """Gathers all published titles from YouTube, posts.json, ledger, and recent audits to prevent semantic clones over a 180-day window."""
        titles = set()

        # 1. Check live YouTube uploads via OAuth service
        try:
            from app.services.youtube_uploader import get_uploader
            uploader = get_uploader()
            service = uploader._get_service("en")
            if service:
                channel_res = service.channels().list(mine=True, part="contentDetails").execute()
                if channel_res and channel_res.get("items"):
                    uploads_pl = channel_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
                    next_page = None
                    cutoff_dt = datetime.now(timezone.utc) - timedelta(days=days)
                    while True:
                        pl_res = service.playlistItems().list(
                            playlistId=uploads_pl,
                            part="snippet",
                            maxResults=50,
                            pageToken=next_page
                        ).execute()
                        for itm in pl_res.get("items", []):
                            snip = itm.get("snippet", {})
                            pub_at = snip.get("publishedAt", "")
                            t = snip.get("title", "")
                            if pub_at:
                                try:
                                    dt = datetime.fromisoformat(pub_at.replace("Z", "+00:00"))
                                    if dt < cutoff_dt:
                                        next_page = None
                                        break
                                except Exception:
                                    pass
                            if t and t != "Deleted video":
                                titles.add(t.strip())
                        next_page = pl_res.get("nextPageToken")
                        if not next_page or len(titles) >= 150:
                            break
                    logger.info(f"✓ [Scanner Deduplication] Retrieved {len(titles)} published titles from YouTube (last {days} days)")
        except Exception as yt_err:
            logger.debug(f"[Scanner Deduplication] Live YouTube query notice: {yt_err}")

        # 2. Check posts.json
        posts_file = BASE_DIR / "content" / "posts.json"
        if posts_file.exists():
            try:
                posts = json.loads(posts_file.read_text(encoding="utf-8"))
                for p in posts:
                    if p.get("title"):
                        titles.add(p["title"].strip())
            except Exception:
                pass

        # 3. Check video SEO ledger
        ledger_file = BASE_DIR / "state" / "video_seo_ledger.json"
        if ledger_file.exists():
            try:
                ledger = json.loads(ledger_file.read_text(encoding="utf-8"))
                for entry in ledger:
                    if entry.get("title"):
                        titles.add(entry["title"].strip())
            except Exception:
                pass

        # 4. Check quarantine audits
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

        # 1. Fetch Live RSS Breaking Headlines for Factual Grounding
        live_headlines = fetch_live_financial_rss_headlines()
        live_rss_sample = "\n".join(f"- {h}" for h in live_headlines)

        recent_titles = self._get_recent_published_titles(days=180)
        blacklist_sample = "\n".join(f"- {t}" for t in recent_titles[:100])

        prompt = f"""
        You are the Chief Investigative Journalist & Media Director for 'The Bull Print' (in the style of Coffeezilla, James Jani, and MagnatesMedia).
        Current Timestamp: {date_str}.
        
        TASK:
        Identify 10 high-velocity, completely DISTINCT financial investigations and institutional scandals from the PAST 24 HOURS.
        Target Audiences: Everyday retail investors, salaried professionals, and families who fear losing their savings to institutional traps.
        
        [LIVE VERIFIED BREAKING FINANCIAL CATALYSTS - PAST 24 HOURS]
        You MUST ground your investigative topics in actual breaking news, market movements, regulatory filings, or real corporate scandals from these live verified headlines:
{live_rss_sample}
        
        MANDATORY FACTUAL GROUNDING RULE:
        Every topic MUST cite, center on, or tie back to real market institutions, regulatory bodies (e.g. SEBI, RBI, US Fed, SEC, DOJ), real companies (e.g. Nvidia, Yes Bank, Adani, BlackRock, Boeing, TSMC, JPMorgan, Apple), or real breaking financial mechanisms.
        STRICTLY PROHIBITED: Do NOT invent fictional unnamed banks or repeat generic placeholder scenarios. Anchor to reality.

        STRICTLY FORBIDDEN VISUAL CLICHÉS (PROMPT-LEVEL MANDATE):
        Visual prompts must depict physical real-world artifacts: trading floors, bank vault doors swinging on multi-bolts, chip cleanrooms with silicon wafers, cargo container cranes, courtroom transcripts, server racks with fiber-optic LEDs, stacked 1kg gold bullion on marble.
        NEVER specify: obsidian monolith, golden crate on cables, red brick corridor, cybernetic bull, or generic floating pedestals.
        
        CRITICAL ZERO-DUPLICATION & ANTI-SAMENESS BLACKLIST:
        The following {len(recent_titles)} titles/topics were ALREADY PRODUCED in the past 180 days. You are STRICTLY FORBIDDEN from generating these topics, repeating their titles, or creating semantic clones, synonyms, or paraphrases of them:
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
              "title": "Documentary Headline 1 (Max 75 chars)",
              "badge": "INVESTIGATION BADGE",
              "hook_text": "MASTER TITLE HOOK",
              "investigative_thesis": "Deep investigative summary exposing the systemic institutional trap.",
              "sector": "Sector Name",
              "vertical": "stock_market"
            }},
            {{
              "id": "doc_02",
              "title": "Documentary Headline 2 (Max 75 chars)",
              "badge": "INVESTIGATION BADGE",
              "hook_text": "MASTER TITLE HOOK",
              "investigative_thesis": "Deep investigative summary exposing the systemic institutional trap.",
              "sector": "Sector Name",
              "vertical": "stock_market"
            }}
          ]
        }}
        """

        data = None
        if self.gemini_key:
            import time
            import requests
            from google import genai

            accumulated_shorts = []
            accumulated_docs = []

            # 1. Direct High-Speed REST Caller (Bypasses httpx SSL handshake hangs)
            rest_models = ["gemini-3-flash-preview", "gemini-flash-lite-latest", "gemini-3.5-flash-lite", "gemini-3.8-flash"]
            for rm in rest_models:
                if len(accumulated_shorts) >= 10 and len(accumulated_docs) >= 2:
                    break
                try:
                    logger.info(f"Querying Gemini REST ({rm}) for {10 - len(accumulated_shorts)} Shorts & {2 - len(accumulated_docs)} Docs...")
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{rm}:generateContent?key={self.gemini_key}"
                    payload = {
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "maxOutputTokens": 4096,
                            "responseMimeType": "application/json"
                        }
                    }
                    r = requests.post(url, json=payload, timeout=25)
                    if r.status_code == 200:
                        raw = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                        import re
                        cleaned_raw = re.sub(r",\s*([\]}])", r"\1", raw)
                        parsed = json.loads(cleaned_raw)

                        for st in parsed.get("shorts_topics", []):
                            if st.get("title") and self._is_compliant_and_unique(st["title"], accumulated_shorts, recent_titles):
                                accumulated_shorts.append(st)

                        for dt in parsed.get("documentary_topics", []):
                            if dt.get("title") and self._is_compliant_and_unique(dt["title"], accumulated_docs, recent_titles):
                                accumulated_docs.append(dt)

                        logger.info(f"REST Progress: {len(accumulated_shorts)}/10 Shorts, {len(accumulated_docs)}/2 Documentaries")
                        if len(accumulated_shorts) >= 10 and len(accumulated_docs) >= 2:
                            break
                except Exception as rest_err:
                    logger.debug(f"REST {rm} notice: {rest_err}")

            candidate_models = [
                "gemini-3-flash-preview",
                "gemini-flash-lite-latest",
                "gemini-3.8-flash",
            ]

            for api_ver in ["v1beta", "v1alpha"]:
                if len(accumulated_shorts) >= 10 and len(accumulated_docs) >= 2:
                    break
                try:
                    client = genai.Client(api_key=self.gemini_key, http_options={"api_version": api_ver})

                    for model_name in candidate_models:
                        if len(accumulated_shorts) >= 10 and len(accumulated_docs) >= 2:
                            break
                        for attempt in range(3):
                            needed_s = max(0, 10 - len(accumulated_shorts))
                            needed_d = max(0, 2 - len(accumulated_docs))
                            if needed_s == 0 and needed_d == 0:
                                break
                            
                            # Dynamically tailor prompt if only Documentaries or only Shorts are needed
                            active_prompt = prompt
                            if needed_d > 0 and needed_s == 0:
                                active_prompt = f"""Based on these breaking financial headlines:\n{live_rss_sample}\n\nGenerate 4 deep-dive investigative financial documentary topics (16:9 Landscape, 12-minute investigative thrillers). Focus on fraud, capital flight, institutional traps, and hidden balance sheets.\nRespond ONLY with JSON:\n{{\"documentary_topics\": [{{\"title\": \"...\", \"hook\": \"...\", \"synopsis\": \"...\", \"vertical\": \"stock_market\"}}]}}"""
                            elif needed_s > 0 and needed_d == 0:
                                active_prompt = f"""Based on these breaking financial headlines:\n{live_rss_sample}\n\nGenerate {needed_s + 4} viral 60-second financial short topics (9:16 vertical). Focus on visceral hooks, retail traps, and corporate deception.\nRespond ONLY with JSON:\n{{\"shorts_topics\": [{{\"title\": \"...\", \"hook\": \"...\", \"synopsis\": \"...\", \"vertical\": \"stock_market\"}}]}}"""

                            try:
                                logger.info(f"Querying {model_name} (attempt {attempt + 1}) for {needed_s} Shorts & {needed_d} Docs...")
                                resp = client.models.generate_content(model=model_name, contents=active_prompt)
                                raw = resp.text.strip()
                                if "```json" in raw:
                                    raw = raw.split("```json")[1].split("```")[0].strip()
                                elif "```" in raw:
                                    raw = raw.split("```")[1].split("```")[0].strip()

                                import re
                                cleaned_raw = re.sub(r",\s*([\]}])", r"\1", raw)
                                try:
                                    parsed = json.loads(cleaned_raw)
                                except Exception:
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
                                if "404" in err_str or "not found" in err_str.lower() or "no longer available" in err_str.lower():
                                    break
                                time.sleep(2 * (attempt + 1))
                                continue
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
        FINANCE_SECTOR_WORDS = {
            "central", "bank", "banks", "banking", "market", "markets", "credit", "debt",
            "power", "energy", "data", "center", "centers", "ai", "fund", "funds",
            "traders", "retail", "institutional", "dealers", "dealer", "bond", "bonds",
            "gold", "silver", "dollar", "dollars", "rupee", "rupees", "pool", "pools",
            "liquidity", "trade", "trading", "scam", "trap", "crisis", "fall", "rise",
            "india", "global", "wall", "street", "dalal", "money", "hidden", "secret"
        }
        for item in current_batch:
            other_title = item.get("title", "")
            other_tokens = _core_title_tokens(other_title)
            shared_batch = cand_tokens & other_tokens
            specific_shared = shared_batch - FINANCE_SECTOR_WORDS
            if len(shared_batch) >= 3 or len(specific_shared) >= 2:
                logger.warning(f"🛡️ [Compliance Gate] Candidate '{title}' too similar to another topic in current batch: '{other_title}' (shared: {shared_batch})")
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
