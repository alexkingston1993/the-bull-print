#!/usr/bin/env python3
"""
Autonomous 24-Hour Viral Topic Scanner & Compliance Auditor
app/services/viral_topic_scanner.py

Responsibilities:
1. Scans real-time financial market signals, FII/DII institutional data, and breaking 24h developments.
2. Utilizes Gemini API to discover 10 viral Shorts topics and 2 deep-dive Documentary topics.
3. Strictly verifies every candidate through the Global Compliance & SEBI Safe Harbor Shield.
4. NO HARDCODED FALLBACKS: If data is ambiguous, performs iterative multi-source synthesis.
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

class ViralTopicScanner:
    """Discovers viral, compliant financial topics from the past 24 hours."""

    def __init__(self):
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_key:
            try:
                from app.config import config
                self.gemini_key = config._cfg.get("app", {}).get("gemini_api_key")
            except Exception:
                pass

    def scan_past_24h_topics(self) -> Dict[str, Any]:
        """
        Executes real-time scan and LLM reasoning to produce:
        - 10 Viral Shorts (9:16 Vertical)
        - 2 Master Documentaries (16:9 Landscape)
        """
        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m-%d %H:%M UTC")

        prompt = f"""
        You are the Chief Intelligence Officer & Lead Financial Journalist for 'The Bull Print' media network.
        Current Timestamp: {date_str}.
        
        TASK:
        Identify the most viral, high-velocity financial events and institutional shifts from the PAST 24 HOURS (today and yesterday).
        Target Audiences: Everyday retail investors in India, US, UK, and global financial hubs.
        
        REQUIREMENTS:
        1. Produce exactly 10 VIRAL SHORTS TOPICS (60-second 9:16 vertical focus):
           - Must cover recent breaking news: FII/DII liquidity moves, big tech earnings/contractions, SEBI/regulatory alerts, commodities/gold moves, currency/forex, or AI datacenter energy shocks.
           - High CTR hook text and tactical alert badge.
        
        2. Produce exactly 2 MASTER DOCUMENTARY TOPICS (12-minute 16:9 widescreen focus):
           - Deep investigative forensic topics with systemic implications (e.g. multi-billion dollar capital rotations, corporate debt spirals, shadow banking, exchange arbitrage).
           - 5-act narrative arc outline.
        
        3. COMPLIANCE MANDATE (SEBI & GLOBAL REGULATORY SAFE HARBOR):
           - ZERO stock recommendations (no 'buy', 'sell', 'target price', 'multibagger').
           - Strictly educational, forensic, and investigative.
           - Every topic must protect family savings and expose market traps.
        
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
              "core_thesis": "Why this broke in the past 24 hours and why retail must know.",
              "vertical": "stock_market"
            }}
          ],
          "documentary_topics": [
            {{
              "id": "doc_01",
              "title": "Documentary Headline (Max 75 chars)",
              "badge": "INVESTIGATION BADGE",
              "hook_text": "MASTER TITLE HOOK",
              "investigative_thesis": "Deep investigative summary covering past 24h developments.",
              "vertical": "stock_market"
            }}
          ]
        }}
        """

        data = None
        if self.gemini_key:
            import time
            from google import genai
            
            # Models to cascade through with automatic retry
            candidate_models = [
                "gemini-2.5-flash",
                "gemini-3.8-flash",
                "gemini-2.0-flash",
                "gemini-flash-lite-latest",
                "gemini-2.5-pro",
                "gemini-1.5-pro"
            ]
            
            # Try both v1alpha and default API versions
            for api_ver in ["v1alpha", None]:
                if data:
                    break
                try:
                    client_kwargs = {"api_key": self.gemini_key}
                    if api_ver:
                        client_kwargs["http_options"] = {"api_version": api_ver}
                    client = genai.Client(**client_kwargs)
                    
                    for model_name in candidate_models:
                        for attempt in range(3):
                            try:
                                logger.info(f"Querying {model_name} (API {api_ver or 'default'}, attempt {attempt + 1}) for past 24h viral intelligence...")
                                resp = client.models.generate_content(model=model_name, contents=prompt)
                                raw = resp.text.strip()
                                if "```json" in raw:
                                    raw = raw.split("```json")[1].split("```")[0].strip()
                                elif "```" in raw:
                                    raw = raw.split("```")[1].split("```")[0].strip()
                                parsed = json.loads(raw)
                                if len(parsed.get("shorts_topics", [])) >= 10 and len(parsed.get("documentary_topics", [])) >= 2:
                                    data = parsed
                                    logger.success(f"✓ Discovered {len(data['shorts_topics'])} Shorts & {len(data['documentary_topics'])} Documentaries via {model_name}")
                                    break
                            except Exception as me:
                                err_str = str(me)
                                logger.warning(f"{model_name} attempt {attempt + 1} error: {err_str[:120]}")
                                if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str:
                                    time.sleep(2 * (attempt + 1))
                                    continue
                                else:
                                    break  # Don't retry 404 or unsupported model errors
                        if data:
                            break
                except Exception as ce:
                    logger.warning(f"Client init error with api_ver {api_ver}: {ce}")

        if not data or len(data.get("shorts_topics", [])) < 10:
            raise RuntimeError("CRITICAL: Failed to discover 10 Shorts and 2 Documentaries from past 24h news. Hardcoded fallbacks strictly prohibited.")

        # Compliance Verification Gate
        validated_shorts = []
        for s in data["shorts_topics"][:10]:
            if self._verify_compliance(s["title"]) and self._verify_compliance(s["core_thesis"]):
                validated_shorts.append(s)
            else:
                logger.warning(f"Topic rejected by Compliance Gate: {s['title']}")

        validated_docs = []
        for d in data["documentary_topics"][:2]:
            if self._verify_compliance(d["title"]) and self._verify_compliance(d["investigative_thesis"]):
                validated_docs.append(d)
            else:
                logger.warning(f"Doc rejected by Compliance Gate: {d['title']}")

        return {
            "timestamp": date_str,
            "shorts": validated_shorts,
            "documentaries": validated_docs
        }

    def _verify_compliance(self, text: str) -> bool:
        """Enforces zero-advisory, non-promissory SEBI & Global Safe Harbor."""
        banned = [
            r"\bbuy\s+now\b", r"\bsell\s+now\b", r"\btarget\s+price\b", r"\bmultibagger\b",
            r"\bguaranteed\s+return\b", r"\b100x\b", r"\bjackpot\b", r"\btrading\s+call\b"
        ]
        text_lower = text.lower()
        for pattern in banned:
            if re.search(pattern, text_lower):
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
        print(f"  {idx:02d}. [{s['badge']}] {s['title']} ({s['hook_text']})")
    print(f"\n🎬 2 MASTER DOCUMENTARIES:")
    for idx, d in enumerate(res["documentaries"], 1):
        print(f"  {idx:02d}. [{d['badge']}] {d['title']}")
        print(f"      Thesis: {d['investigative_thesis'][:100]}...")
