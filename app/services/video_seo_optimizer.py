"""
app/services/video_seo_optimizer.py
Automated vidIQ 50/50 SEO, Canonical Article Backlinking, and Video Interlinking Engine.

Responsibilities:
1. Automatically optimizes video Title, Description, and Tags to achieve 48-50/50 vidIQ Actionable SEO Score.
2. Injects exact canonical website article backlink (https://bullprintmedia.com/article/:slug).
3. Injects contextual companion video recommendation ("Watch Next" Binge Loop).
4. Provides mathematical, calculatable vidIQ score verification (0.0 to 50.0).
5. Provides a pre-upload validation gate and post-upload audit ledger.
"""

import os
import json
import re
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from loguru import logger

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
POSTS_JSON_PATH = PROJECT_ROOT / "content" / "posts.json"
LEDGER_PATH = PROJECT_ROOT / "state" / "video_seo_ledger.json"

HIGH_VOLUME_CORE_TAGS = [
    "The Bull Print", "Nifty 50", "Stock Market India", "Dalal Street",
    "Indian Stock Market", "Share Market", "FII DII Flows", "Option Trading",
    "SEBI Rules", "Personal Finance India", "Mutual Funds", "Investing For Beginners"
]

HIGH_VOLUME_KEYWORDS = [
    "nifty", "stock", "share", "market", "sebi", "trading", "option", "fii", 
    "money", "crypto", "bitcoin", "gold", "silver", "investment", "finance", 
    "ipo", "bank", "rupee", "dalal", "sensex", "mutual", "fund", "wealth"
]

STOP_WORDS = {
    "what", "with", "this", "that", "your", "from", "have", "more", "shorts",
    "short", "about", "when", "will", "make", "into", "after", "here", "just",
    "very", "some", "them", "then", "their", "only", "also", "been", "were"
}


def clean_words(text: str) -> List[str]:
    """Tokenizes text into significant keywords."""
    clean = re.sub(r"[^\w\s]", " ", str(text or "").lower())
    return [w for w in clean.split() if len(w) > 3 and w not in STOP_WORDS]


class VideoSEOOptimizer:
    """Centralized SEO & Interlinking Engine for The Bull Print channel uploads."""

    def __init__(self):
        self.posts: List[Dict[str, Any]] = self._load_posts()
        self.recent_channel_videos: List[Dict[str, str]] = self._load_recent_videos()

    def _load_posts(self) -> List[Dict[str, Any]]:
        """Loads available articles from content/posts.json."""
        if POSTS_JSON_PATH.exists():
            try:
                with open(POSTS_JSON_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to read posts.json: {e}")
        return []

    def _load_recent_videos(self) -> List[Dict[str, str]]:
        """Loads recent channel videos from state cache or default seed."""
        cache_path = PROJECT_ROOT / "state" / "recent_videos_cache.json"
        if cache_path.exists():
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return [
            {"id": "TNqajzmdPh8", "title": "Rupee Stands Firm at 93.93: FII Inflows Anchor Currency"},
            {"id": "V-E02LLAwac", "title": "Bitcoin Liquidity Rebound: Crypto Shakes Off Tech Selloff"},
            {"id": "haWQ3J8xyio", "title": "FII Cash Bazooka: Foreign Funds Pump RS. 48,000 Crore"},
            {"id": "JeNhYFa9UWE", "title": "Silver Crashes Rs 56,000: Gold Drops As Dollar Surges"},
            {"id": "Ja_CgE2wiSw", "title": "SEBI Clears Mega IPO Rush: MakeMyTrip & Veritas Approved"},
            {"id": "oKGnsqVXNys", "title": "Crypto Tax Section 115BBH & 194S Forensic Audit"}
        ]

    def match_best_article(self, title: str, description: str = "") -> Dict[str, Any]:
        """Finds the most relevant article in content/posts.json based on semantic and keyword overlap."""
        if not self.posts:
            return {
                "title": "Comprehensive Guide to Indian Stock Market Investing",
                "slug": "indian-stock-market-guide-for-beginners"
            }

        v_words = clean_words(f"{title} {description}")
        best_post = None
        best_score = -1.0

        for p in self.posts:
            p_title = p.get("title", "")
            p_words = clean_words(p_title)
            overlap = len(set(v_words).intersection(set(p_words)))
            seq = SequenceMatcher(None, title.lower(), p_title.lower()).ratio()
            score = (overlap * 2.5) + seq
            if score > best_score:
                best_score = score
                best_post = p

        return best_post or self.posts[0]

    def match_best_interlink_video(self, title: str, exclude_id: Optional[str] = None) -> Dict[str, str]:
        """Finds a topically aligned companion video for session duration binge looping."""
        candidates = [v for v in self.recent_channel_videos if v.get("id") != exclude_id]
        if not candidates:
            return {"id": "TNqajzmdPh8", "title": "Rupee Stands Firm at 93.93: FII Inflows Anchor Currency"}

        v_words = clean_words(title)
        best_video = None
        best_score = -1.0

        for c in candidates:
            c_words = clean_words(c.get("title", ""))
            overlap = len(set(v_words).intersection(set(c_words)))
            if overlap > best_score:
                best_score = overlap
                best_video = c

        return best_video or candidates[0]

    def optimize_metadata(
        self,
        title: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        is_short: bool = True,
        companion_video_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transforms raw metadata into a 50/50 vidIQ compliant payload:
        - Front-loaded title keywords.
        - Tripled keywords in first 200 characters of description.
        - Canonical article backlink: https://bullprintmedia.com/article/:slug
        - Companion video interlink with 'Why watch this next' value bridge.
        - 18-20 high-volume tags within character limit (< 460 chars).
        """
        clean_title = re.sub(r"#\w+", "", title).strip()
        v_words = clean_words(clean_title)

        primary_kws = v_words[:3]
        if len(primary_kws) < 3:
            primary_kws += ["stock", "market", "nifty"]
        kw1, kw2, kw3 = primary_kws[0].capitalize(), primary_kws[1].capitalize(), primary_kws[2].capitalize()

        # 1. Match Canonical Article
        article = self.match_best_article(clean_title, description)
        article_url = f"https://bullprintmedia.com/article/{article.get('slug', 'indian-stock-market-guide-for-beginners')}"

        # 2. Match Companion Video
        interlink = self.match_best_interlink_video(clean_title, exclude_id=companion_video_id)
        interlink_url = f"https://youtu.be/{interlink['id']}"

        # 3. Construct 18-20 High-Volume Tags (< 460 chars)
        video_specific_tags = [w.capitalize() for w in v_words if len(w) > 3][:6]
        candidate_tags = [
            clean_title.split(":")[0].strip(),
            f"{kw1} {kw2}",
            f"{kw2} {kw3}",
            kw1, kw2, kw3
        ] + video_specific_tags + HIGH_VOLUME_CORE_TAGS

        unique_tags: List[str] = []
        total_len = 0
        for t in candidate_tags:
            ct = t.replace("#", "").strip()
            if ct and ct.lower() not in [u.lower() for u in unique_tags]:
                if total_len + len(ct) + 1 <= 460 and len(unique_tags) < 20:
                    unique_tags.append(ct)
                    total_len += len(ct) + 1

        # 4. Construct Description with Tripled Keywords & Backlinks
        # First 200 chars MUST contain kw1, kw2, kw3
        opening_hook = (
            f"{clean_title} — Forensic analysis on {kw1}, {kw2}, and {kw3} for Indian and global investors.\n"
            f"In this data-backed breakdown, The Bull Print uncovers institutional liquidity shifts, market microstructure, and actionable risk management principles."
        )

        full_description = f"""{opening_hook}

📖 Read our full forensic investigation & charts on our website:
{article_url}

🎬 Recommended Next Watch (Interlinked Deep-Dive):
{interlink['title']}
👉 Watch here: {interlink_url}
💡 Why watch this next: This breakdown connects directly to how smart money and institutional liquidity dictate market momentum.

📊 Key Market Takeaways:
• Quantitative data and institutional order flow breakdown.
• Risk-adjusted positioning metrics for volatile market regimes.
• Moat and balance sheet forensic screening principles.

🌐 Free Institutional Tools on The Bull Print:
• Real-Time F&O Screener & PCR: https://bullprintmedia.com/fno
• Comprehensive Stock Screener: https://bullprintmedia.com/screener
• SIP Step-Up Wealth Calculator: https://bullprintmedia.com/calculators

⚖️ Mandatory Statutory Disclaimer:
This content is published strictly for educational and informational purposes under SEBI RA guidelines and does not constitute financial, investment, or legal advice. Securities market investments are subject to market risks. Read all scheme disclosures carefully before investing.

#TheBullPrint #StockMarketIndia #Nifty50 #DalalStreet #FinanceIndia #InvestSmart{' #Shorts' if is_short else ''}"""

        final_title = clean_title[:100]
        final_desc = full_description[:5000].strip()

        # Score & Validate
        score_data = self.calculate_vidiq_score(final_title, final_desc, unique_tags)

        return {
            "title": final_title,
            "description": final_desc,
            "tags": unique_tags,
            "article_url": article_url,
            "article_slug": article.get("slug"),
            "interlink_url": interlink_url,
            "interlink_id": interlink["id"],
            "vidiq_score": score_data["score"],
            "vidiq_breakdown": score_data["breakdown"]
        }

    def calculate_vidiq_score(
        self,
        title: str,
        description: str,
        tags: List[str]
    ) -> Dict[str, Any]:
        """
        Computes the standard vidIQ Actionable SEO Score (0.0 to 50.0):
        1. Tag Count (max 5 pts): >= 15 tags = 5.0
        2. Tag Volume (max 5 pts): >= 8 high-volume keywords = 5.0
        3. Keywords in Title (max 5 pts): >= 3 strong keywords = 5.0
        4. Keywords in First 200c Desc (max 5 pts): >= 3 title keywords in first 200c = 5.0
        5. Tripled Keywords (max 5 pts): >= 3 keywords in Title AND Desc AND Tags = 5.0
        Total Score = Sum of 5 metrics * 2.0 (Scale: 0 - 50.0).
        """
        # 1. Tag Count
        tc = len(tags or [])
        s_tc = 5.0 if tc >= 15 else (4.0 if tc >= 10 else (3.0 if tc >= 5 else (2.0 if tc >= 1 else 0.0)))

        # 2. Keywords in Title
        tw = clean_words(title)
        s_kw_t = 5.0 if len(tw) >= 3 else 3.0

        # 3. Keywords in First 200 Chars of Description
        desc_200 = (description or "")[:200].lower()
        m_desc = sum(1 for w in tw if w in desc_200)
        s_kw_d = 5.0 if m_desc >= 3 else (3.5 if m_desc >= 1 else 1.0)

        # 4. Tripled Keywords (Title + Desc + Tags)
        desc_lower = (description or "").lower()
        tags_lower = [t.lower() for t in (tags or [])]
        tripled = sum(1 for w in tw if any(w in t for t in tags_lower) and w in desc_lower)
        s_trip = 5.0 if tripled >= 3 else (3.5 if tripled >= 1 else 0.0)

        # 5. Tag Volume
        h_c = sum(1 for t in (tags or []) if any(h in t.lower() for h in HIGH_VOLUME_KEYWORDS))
        s_vol = 5.0 if h_c >= 8 else (3.5 if h_c >= 4 else (2.0 if h_c >= 1 else 0.0))

        total_score = (s_tc + s_kw_t + s_kw_d + s_trip + s_vol) * 2.0

        return {
            "score": round(total_score, 2),
            "percentage": round((total_score / 50.0) * 100, 1),
            "breakdown": {
                "tag_count": s_tc,
                "tag_volume": s_vol,
                "kw_in_title": s_kw_t,
                "kw_in_desc_first_200": s_kw_d,
                "tripled_keywords": s_trip
            }
        }

    def validate_metadata(
        self,
        title: str,
        description: str,
        tags: List[str],
        min_score: float = 48.0
    ) -> Dict[str, Any]:
        """
        Calculable Validation Gate for CI/CD and pre-upload checks.
        Returns passed: True/False with detailed audit diagnostic.
        """
        errors = []
        warnings = []

        # Check lengths
        if not title or len(title) > 100:
            errors.append(f"Title length invalid: {len(title or '')} (max 100)")
        if not description or len(description) > 5000:
            errors.append(f"Description length invalid: {len(description or '')} (max 5000)")

        total_tag_chars = sum(len(t) for t in (tags or []))
        if total_tag_chars > 490:
            errors.append(f"Tags total character length exceeds YouTube limit: {total_tag_chars}/500")

        # Check backlinks
        has_article_backlink = "https://bullprintmedia.com/article/" in (description or "")
        if not has_article_backlink:
            errors.append("Missing exact canonical article backlink (https://bullprintmedia.com/article/:slug)")

        # Check interlinks
        has_video_interlink = ("https://youtu.be/" in (description or "")) or ("youtube.com/watch" in (description or ""))
        if not has_video_interlink:
            errors.append("Missing contextual companion video interlink (https://youtu.be/:id)")

        # Check vidIQ Score
        scoring = self.calculate_vidiq_score(title, description, tags)
        score = scoring["score"]
        if score < min_score:
            errors.append(f"vidIQ score {score}/50.0 below required threshold of {min_score}/50.0")

        passed = len(errors) == 0

        return {
            "passed": passed,
            "score": score,
            "min_score": min_score,
            "errors": errors,
            "warnings": warnings,
            "has_article_backlink": has_article_backlink,
            "has_video_interlink": has_video_interlink,
            "breakdown": scoring["breakdown"]
        }

    def record_upload_audit(self, video_id: str, title: str, validation_result: Dict[str, Any]):
        """Persists validation audit to state/video_seo_ledger.json for continuous monitoring."""
        try:
            os.makedirs(LEDGER_PATH.parent, exist_ok=True)
            ledger = []
            if LEDGER_PATH.exists():
                try:
                    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
                        ledger = json.load(f)
                except Exception:
                    ledger = []

            entry = {
                "video_id": video_id,
                "title": title,
                "timestamp": str(Path(__file__).stat().st_mtime),
                "vidiq_score": validation_result.get("score"),
                "passed": validation_result.get("passed"),
                "has_backlink": validation_result.get("has_article_backlink"),
                "has_interlink": validation_result.get("has_video_interlink"),
                "errors": validation_result.get("errors", [])
            }
            ledger.append(entry)
            with open(LEDGER_PATH, "w", encoding="utf-8") as f:
                json.dump(ledger[-200:], f, indent=2)
            logger.info(f"✓ Recorded SEO & Interlink audit ledger for video {video_id} (Score: {validation_result.get('score')}/50)")
            return entry
        except Exception as e:
            logger.warning(f"Failed to record upload audit: {e}")
            return None


# Global Singleton
_seo_optimizer: Optional[VideoSEOOptimizer] = None

def get_video_seo_optimizer() -> VideoSEOOptimizer:
    global _seo_optimizer
    if _seo_optimizer is None:
        _seo_optimizer = VideoSEOOptimizer()
    return _seo_optimizer
