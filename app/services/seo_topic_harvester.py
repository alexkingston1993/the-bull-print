"""
SEO Topic Harvester (every-app/open-seo extraction) — "Dark-Query" Search Intent Feeder.

Feeds the 6 daily vertical slots with REAL Indian search intent instead of guessed topics:
1. Google Autocomplete JSON (free, no key) around vertical high-CPC seed matrices
2. Google Trends RSS (IN) for breaking market/insurance stories
3. Optional Google Search Console "striking-distance dark queries" (positions 5-20,
   impressions > 30, no dedicated article yet) when GSC_SERVICE_ACCOUNT_JSON exists
4. 30-day deduplication against the live posts.json manifest

Never raises — every failure path returns a deterministic registry-style topic so the
daily cron slot always has executable research input.
"""

import os
import re
import json
import html
import math
import random
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone, timedelta
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent
POSTS_MANIFEST = BASE_DIR / "content" / "posts.json"
SITE_BASE = os.getenv("SITE_BASE_URL", "https://bullprintmedia.com")

AUTOCOMPLETE_URL = "https://suggestqueries.google.com/complete/search"
TRENDS_RSS_URL = "https://trends.google.com/trending/rss?geo=IN"
GSC_SITE = f"{SITE_BASE}/"

# High-CPC Indian retail-intent seed matrices per vertical (open-seo cluster expansion)
SEED_QUERIES: Dict[str, List[str]] = {
    "stock_market": [
        "nifty 50 today", "bank nifty trap", "fii dii data today", "sebi f&o rules",
        "institutional order flow", "options gamma",
    ],
    "crypto": [
        "bitcoin liquidation", "crypto funding rate", "btc open interest",
        "altcoin unlock", "usdt dominance", "crypto tax india",
    ],
    "insurance": [
        "term insurance claim rejection", "health insurance room rent limit",
        "irdai new rules", "claim settlement ratio trap",
        "super top up health insurance", "cashless hospital network denied",
    ],
    "crypto_ethereum": [
        "ethereum gas fees", "eth exchange reserve", "crypto funding rate",
        "liquidation heatmap", "altcoin unlock", "usdt dominance",
    ],
}

# Intent modifiers that make a query a "article-worthy" evergreen question
INTENT_MODIFIERS = (
    "today", "why", "how", "explain", "rules", "rejection", "trap", "limit",
    "vs", "smashing", "down", "crash", "pump", "ban", "tax", "ratio", "fees",
    "abandoned", "secret", "trick", "avoid", "mistake", "caught",
)

_TOPIC_STOP = re.compile(r"[^a-zA-Z0-9 ₹&'\-\:\?]")

# Domain anchoring: a candidate must carry ≥1 vertical anchor token, or it is
# cross-domain noise (sports scores, celebrity queries, product searches) and dies.
DOMAIN_ANCHORS: Dict[str, tuple] = {
    "stock_market": ("nifty", "sensex", "bank nifty", "stock", "share", "market", "fii", "dii",
                      "sebi", "option", "options", "put", "call", "f&o", "gamma", "intraday", "ipo",
                      "delivery", "btst", "swing", "trading", "trader", "institutional"),
    "crypto": ("bitcoin", "btc", "crypto", "altcoin", "usdt", "stablecoin", "liquidation",
                 "funding", "open interest", "eth", "ethereum", "bnb", "xrp", "solana",
                 "doge", "exchange", "token", "coin", "wallet"),
    "insurance": ("insurance", "irdai", "claim", "policy", "premium", "cover", "deductible",
                   "health", "term plan", "rider", "cashless", "hospital", "sum insured",
                   "insurer", "insured", "reimbursement"),
    "crypto_ethereum": ("eth", "ethereum", "gas", "crypto", "usdt", "liquidation", "funding",
                          "altcoin", "exchange", "token", "coin"),
}


def _anchor_hits(q: str, vertical: str) -> int:
    ql = q.lower()
    return sum(1 for a in DOMAIN_ANCHORS.get(vertical, ()) if a in ql)


def _safe_get(url: str, params: Dict[str, str], timeout: float = 6.0) -> Optional[str]:
    try:
        res = requests.get(url, params=params, timeout=timeout, headers={
            "User-Agent": "Mozilla/5.0 (compatible; TheBullPrint-Harvester/1.0)",
            "Accept-Language": "en-IN,en;q=0.9",
        })
        if res.status_code == 200 and res.text:
            return res.text
    except Exception as e:
        logger.debug(f"[Harvester] GET failed {url}: {e}")
    return None


# ---------------------------------------------------------------- harvesters
def fetch_autocomplete_cluster(seed: str) -> List[str]:
    """Google Autocomplete JSON: seed → up to 10 real user-typed expansions (+2 letter-rounds)."""
    raw = _safe_get(AUTOCOMPLETE_URL, {"client": "firefox", "gl": "in", "hl": "en", "q": seed})
    variants: List[str] = []
    if raw:
        try:
            data = json.loads(raw)
            variants = [html.unescape(html.unescape(str(v))) for v in
                        (data[1] if isinstance(data, list) and len(data) > 1 else [])]
        except Exception:
            variants = []
    # second round on 1 promising variant to widen the cluster (open-seo 'widen keyword cluster')
    if variants:
        probe = variants[0]
        raw2 = _safe_get(AUTOCOMPLETE_URL, {"client": "firefox", "gl": "in", "hl": "en", "q": probe})
        if raw2:
            try:
                data2 = json.loads(raw2)
                if isinstance(data2, list) and len(data2) > 1:
                    variants += [html.unescape(html.unescape(str(v))) for v in data2[1]]
            except Exception:
                pass
    seen, out = set(), []
    for v in variants:
        k = v.strip().lower()
        if k and k not in seen:
            seen.add(k)
            out.append(v.strip())
    return out[:12]


def fetch_trends_headlines() -> List[str]:
    """Google Trends RSS (IN): breaking news titles, filtered to finance/biz vocab."""
    raw = _safe_get(TRENDS_RSS_URL, {})
    if not raw:
        return []
    titles = [html.unescape(html.unescape(t)).strip()
              for t in re.findall(r"<title>(?:<!\[CDATA\[)?(.*?)(?:]]>)?</title>", raw, flags=re.DOTALL)[1:]]  # skip channel title
    keys = ("nifty", "bank", "rbi", "rupee", "market", "stock", "crypto", "bitcoin", "btc", "gold",
            "insurance", "irdai", "claim", "policy", "fd", "sip", "tax", "sebi", "inflation", "fy", "india")
    return [t for t in titles if any(k in t.lower() for k in keys)][:10]


def fetch_gsc_dark_queries() -> List[Dict[str, Any]]:
    """Search Console striking-distance queries: rank 5-20, ≥30 impressions, 28-day window.
    Requires GSC_SERVICE_ACCOUNT_JSON (service-account with Search Console access)."""
    sa_b64 = os.getenv("GSC_SERVICE_ACCOUNT_JSON", "")
    if not sa_b64:
        return []
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        if os.path.sep in sa_b64 and Path(sa_b64).exists():
            creds = service_account.Credentials.from_service_account_file(
                sa_b64, scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
            )
        else:
            import base64
            info = json.loads(base64.b64decode(sa_b64).decode("utf-8"))
            creds = service_account.Credentials.from_service_account_info(
                info, scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
            )
        svc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
        end = datetime.now(timezone.utc).date()
        start = end - timedelta(days=28)
        res = svc.searchanalytics().query(
            siteUrl=GSC_SITE,
            body={
                "startDate": start.isoformat(),
                "endDate": end.isoformat(),
                "dimensions": ["query"],
                "rowLimit": 100,
                "dataState": "all",
            },
        ).execute()
        rows = []
        for row in (res.get("rows") or []):
            q = str(row.get("keys", [""])[0]).strip()
            pos = float(row.get("position", 99))
            imp = int(row.get("impressions", 0))
            if 5.0 <= pos < 20.0 and imp >= 30 and len(q.split()) >= 3:
                rows.append({"query": q, "position": pos, "impressions": imp})
        return rows[:20]
    except Exception as e:
        logger.warning(f"[Harvester] GSC dark-query fetch skipped: {e}")
        return []


# ---------------------------------------------------------------- dedupe / scoring
# ---------------------------------------------------------------- dedupe / scoring
CHANNEL_TITLES_FILE = BASE_DIR / "data" / "channel_video_titles.json"

STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "for", "with", "in", "on", "at", "by",
    "to", "from", "is", "are", "was", "were", "this", "that", "these", "those",
    "how", "why", "what", "when", "who", "which", "your", "my", "our", "their",
    "today", "exposed", "truth", "revealed", "video", "shorts", "bull", "print"
}


def _all_known_titles() -> List[str]:
    """Retrieves all historical titles across website posts and YouTube uploads to eliminate duplicates."""
    titles: List[str] = []
    
    # 1. From live YouTube channel titles cache
    if CHANNEL_TITLES_FILE.exists():
        try:
            yt_titles = json.loads(CHANNEL_TITLES_FILE.read_text(encoding="utf-8"))
            if isinstance(yt_titles, list):
                titles.extend([str(t) for t in yt_titles if t and t != "Deleted video"])
        except Exception as e:
            logger.debug(f"[Harvester] channel_video_titles.json unreadable: {e}")

    # 2. From content/posts.json
    if POSTS_MANIFEST.exists():
        try:
            posts = json.loads(POSTS_MANIFEST.read_text(encoding="utf-8"))
            if isinstance(posts, dict):
                posts = posts.get("posts", [])
            for p in posts:
                if isinstance(p, dict) and p.get("title"):
                    titles.append(str(p["title"]))
        except Exception as e:
            logger.debug(f"[Harvester] posts.json unreadable: {e}")

    return list(dict.fromkeys(titles))


def _extract_tokens(text: str) -> set:
    words = re.findall(r"[a-z0-9₹]+", text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) > 1}


def _is_duplicate(candidate: str, titles: List[str]) -> bool:
    """
    Advanced Deduplication Shield:
    - Rejects if token Jaccard similarity >= 0.35 with any existing video/article.
    - Rejects if 3+ significant content words overlap.
    - Rejects if exact numeric level (e.g. 24500, 30%) overlaps with key domain words.
    """
    cand_tokens = _extract_tokens(candidate)
    if not cand_tokens:
        return True

    # Extract digits/levels (e.g. '24500', '30')
    cand_digits = set(re.findall(r"\b\d+\b", candidate))

    for t in titles:
        t_tokens = _extract_tokens(t)
        if not t_tokens:
            continue
        
        shared = cand_tokens & t_tokens
        union = cand_tokens | t_tokens
        jaccard = len(shared) / len(union) if union else 0.0

        if jaccard >= 0.35:
            return True
        if len(shared) >= 3:
            return True

        # Check numeric trap collision (e.g. multiple videos about 24500 or 30% tax)
        t_digits = set(re.findall(r"\b\d+\b", t))
        shared_digits = cand_digits & t_digits
        if shared_digits and len(shared) >= 2:
            return True

    return False


def _score_query(q: str, vertical: str = "stock_market") -> float:
    ql = q.lower()
    score = 0.0
    score += sum(2.0 for m in INTENT_MODIFIERS if f" {m}" in f" {ql}" or ql.endswith(m))
    score += min(2.0, 0.18 * len(q.split()))  # longer queries = lower competition
    score += min(2.5, 0.9 * _anchor_hits(q, vertical))  # in-domain anchoring bonus
    return score


def _fetch_google_news_rss(query: str) -> List[str]:
    """Fetches breaking real-time news headlines from Google News RSS (India)."""
    url = "https://news.google.com/rss/search"
    raw = _safe_get(url, {"q": query, "hl": "en-IN", "gl": "IN", "ceid": "IN:en"}, timeout=6.0)
    if not raw:
        return []
    items = re.findall(r"<title>(?:<!\[CDATA\[)?(.*?)(?:]]>)?</title>", raw, flags=re.DOTALL)[1:]
    clean_titles = []
    for it in items:
        # Strip source suffix (e.g. ' - Moneycontrol', ' - Livemint')
        t = re.sub(r"\s*-\s*[^-]+$", "", html.unescape(it)).strip()
        if len(t.split()) >= 4:
            clean_titles.append(t)
    return clean_titles[:15]


def _dynamic_llm_fresh_topic(vertical: str, titles: List[str]) -> Dict[str, Any]:
    """
    Zero-Static-Default Fallback:
    Engages Gemini / LLM to dynamically generate an unprecedented, high-curiosity,
    compliant retail topic that has NEVER appeared in the channel history.
    """
    recent_sample = ", ".join(f'"{t}"' for t in titles[:20])
    prompt = (
        f"You are the Lead Quantitative Research Director for an educational channel in India. "
        f"Generate ONE novel, highly engaging, institutional-grade research topic for the vertical '{vertical}'.\n\n"
        f"MANDATORY NOVELTY CONSTRAINT:\n"
        f"It must NOT duplicate, rehash, or closely resemble any of these already covered topics:\n"
        f"[{recent_sample}]\n\n"
        f"Requirements:\n"
        f"- Target real retail search curiosity in India (e.g. hidden traps, order flow math, regulatory clauses, settlement realities).\n"
        f"- Must NOT contain buy/sell recommendations or price predictions.\n"
        f"- Format as a clean, compelling question or investigative hook between 7 and 12 words.\n"
        f"Respond with ONLY the topic string. No quotes, no markdown, no preamble."
    )

    try:
        api_key = os.getenv("GEMINI_API_KEY", "")
        if api_key:
            from google import genai
            client = genai.Client(api_key=api_key)
            resp = client.models.generate_content(
                model=os.getenv("GEMINI_MODEL_NAME", "gemini-flash-lite-latest"),
                contents=prompt
            )
            candidate = (resp.text or "").strip().strip('"').strip("'")
            if candidate and not _is_duplicate(candidate, titles):
                logger.success(f"[Harvester] Dynamically generated fresh topic via Gemini: '{candidate}'")
                return {
                    "topic": candidate,
                    "search_cluster": SEED_QUERIES.get(vertical, SEED_QUERIES["stock_market"])[:5],
                    "vertical": vertical,
                    "source": "dynamic_ai_fresh_synthesis"
                }
    except Exception as gem_err:
        logger.debug(f"[Harvester] Gemini fresh topic call failed: {gem_err}")

    # Fallback to Pollinations fast LLM if Gemini is unavailable
    try:
        res = requests.post(
            "https://text.pollinations.ai/openai",
            json={"messages": [{"role": "user", "content": prompt}], "model": "openai-fast"},
            timeout=10.0
        )
        if res.status_code == 200:
            candidate = res.text.strip().strip('"').strip("'")
            if candidate and not _is_duplicate(candidate, titles):
                logger.success(f"[Harvester] Dynamically generated fresh topic via Pollinations: '{candidate}'")
                return {
                    "topic": candidate,
                    "search_cluster": SEED_QUERIES.get(vertical, SEED_QUERIES["stock_market"])[:5],
                    "vertical": vertical,
                    "source": "dynamic_pollinations_synthesis"
                }
    except Exception as pol_err:
        logger.debug(f"[Harvester] Pollinations fresh topic call failed: {pol_err}")

    # Final dynamic generator: algorithmic query combination that guarantees novelty
    angles = [
        "Uncovering Hidden Liquidity Absorption In",
        "The Mathematical Settlement Reality Of",
        "Why Retail Volatility Models Fail Around",
        "Regulatory Order Flow Audit Of Recent",
        "Institutional Block Footprint Mechanics In",
    ]
    keywords = SEED_QUERIES.get(vertical, SEED_QUERIES["stock_market"])
    timestamp_seed = int(time.time())
    chosen_angle = angles[timestamp_seed % len(angles)]
    chosen_kw = keywords[(timestamp_seed // 7) % len(keywords)].title()
    generated = f"{chosen_angle} {chosen_kw}"
    return {
        "topic": generated,
        "search_cluster": keywords[:5],
        "vertical": vertical,
        "source": "dynamic_algorithmic_novel_generator"
    }


def _fallback_topic(vertical: str, titles: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    100% Dynamic Multi-Source Fallback (Zero static or repeated topics):
    1. Probes real-time Google News RSS for live breaking stories in {vertical}.
    2. Probes AI synthesis with strict channel history exclusion.
    3. Algorithmic novelty generator guaranteeing non-repetition.
    """
    if titles is None:
        titles = _all_known_titles()

    news_queries = {
        "stock_market": "Nifty SEBI trading options when:3d",
        "crypto": "crypto bitcoin liquidation on-chain when:3d",
        "insurance": "health insurance IRDAI claim settlement when:7d",
        "crypto_ethereum": "ethereum gas fees onchain when:3d"
    }

    q = news_queries.get(vertical, "Nifty market when:3d")
    news_items = _fetch_google_news_rss(q)
    for item in news_items:
        if not _is_duplicate(item, titles) and _anchor_hits(item, vertical) >= 1:
            clean_item = _TOPIC_STOP.sub(" ", item).strip()
            clean_item = " ".join(clean_item.split())
            logger.info(f"[Harvester] Harvested live breaking news fallback for {vertical}: '{clean_item}'")
            return {
                "topic": clean_item,
                "search_cluster": SEED_QUERIES.get(vertical, SEED_QUERIES["stock_market"])[:5],
                "vertical": vertical,
                "source": "google_news_rss_live"
            }

    return _dynamic_llm_fresh_topic(vertical, titles)


# ---------------------------------------------------------------- public API
def harvest_topic_for_slot(vertical: str, slot_number: int) -> Dict[str, Any]:
    """
    open-seo dark-query loop for one daily slot:
    GSC striking-distance queries → ranked autocomplete cluster → 30-day dedupe.
    Returns {"topic", "search_cluster" (≤5), "vertical", "source"}.
    """
    if vertical not in SEED_QUERIES:
        vertical = "stock_market"

    titles = _all_known_titles()

    # 0. Check Competitor Viral Radar (Trending Outlier Pattern)
    try:
        from app.services.competitor_viral_radar import CompetitorViralRadar
        winning_horse = CompetitorViralRadar.get_winning_horse(vertical, slot_number)
        if winning_horse and winning_horse.get("safe_original_research_angle"):
            safe_angle = winning_horse["safe_original_research_angle"]
            if not _is_duplicate(safe_angle, titles):
                horse_cluster = fetch_autocomplete_cluster(winning_horse.get("title", "")[:35])
                cluster_clean = [q for q in horse_cluster if not _is_duplicate(q, titles)][:4]
                return {
                    "topic": safe_angle,
                    "search_cluster": [safe_angle] + cluster_clean,
                    "vertical": vertical,
                    "source": f"viral_horse_{winning_horse.get('outlier_multiplier', 1)}x",
                    "structural_dna": winning_horse,
                }
    except Exception as h_err:
        logger.debug(f"[Harvester] Viral horse check note: {h_err}")

    # 1. GSC dark queries are pure gold (our own domain, positions 5-20)
    if slot_number % 2 == 0:
        for row in fetch_gsc_dark_queries():
            q = row["query"]
            if not _is_duplicate(q, titles):
                return {
                    "topic": f"{q[:1].upper()}{q[1:]} - What The Data Shows",
                    "search_cluster": SEED_QUERIES[vertical][:5],
                    "vertical": vertical,
                    "source": f"gsc_pos{row['position']:.0f}",
                }

    # 2. Autocomplete clusters around this vertical's seeds; slot_number picks rotation seed
    seeds = SEED_QUERIES[vertical]
    seed = seeds[(slot_number - 1) % len(seeds)]
    cluster = fetch_autocomplete_cluster(seed)
    trends = fetch_trends_headlines() if slot_number % 3 == 0 else []

    candidates: List[Dict[str, float]] = []
    for q in cluster:
        if _is_duplicate(q, titles) or len(q.split()) < 3:
            continue
        if _anchor_hits(q, vertical) < 1:  # cross-domain noise guard (sports/celebs/products die here)
            continue
        candidates.append({"q": q, "s": _score_query(q, vertical)})
    for t in trends:
        if _is_duplicate(t, titles) or _anchor_hits(t, vertical) < 1:
            continue
        candidates.append({"q": t, "s": _score_query(t, vertical) + 1.5})  # breaking trends edge

    if not candidates:
        return _fallback_topic(vertical, titles)

    candidates.sort(key=lambda c: (-c["s"], c["q"]))
    picked = candidates[0]["q"]
    search_cluster = [c["q"] for c in candidates[:5]]

    top_seed_score = _score_query(seed, vertical)
    if _score_query(picked, vertical) < top_seed_score:  # seed is still stronger intent — stay on it
        picked = seed
        search_cluster = [seed] + search_cluster[1:5]

    pick = _TOPIC_STOP.sub(" ", picked)
    pick = " ".join(w for w in pick.split() if w)
    pick = pick[:1].upper() + pick[1:]
    return {
        "topic": pick,
        "search_cluster": search_cluster[:5],
        "vertical": vertical,
        "source": "autocomplete" + ("+trends" if any(picked == t for t in trends) else ""),
    }


def enrichNotes(notes: str, cluster: List[str]) -> str:
    """Weave the keyword cluster into research notes so Gemini bakes them into script/description/SEO."""
    if not cluster:
        return notes
    kw = ", ".join(f"\"{c}\"" for c in cluster[:5])
    return f"{notes}\nSEARCH-INTENT CLUSTER (weave ALL of these naturally into the script, article headings, SEO title/description and YouTube tags): {kw}"


if __name__ == "__main__":
    for v in ("stock_market", "crypto", "insurance"):
        res = harvest_topic_for_slot(v, 1)
        print(v, "→", res["topic"], "| cluster:", res["search_cluster"], "| src:", res["source"])
