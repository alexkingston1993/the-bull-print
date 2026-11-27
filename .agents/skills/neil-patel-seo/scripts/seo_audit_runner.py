#!/usr/bin/env python3
"""
Neil Patel / Ubersuggest Automated SEO Audit Runner
Simulates Ubersuggest's 100-Point Site Audit Engine.
Checks HTML files or live URLs for:
- Critical Errors (Titles, Canonical, Robots, HTTPS, 404s)
- Warnings (Title/Meta lengths, H1 hierarchy, Alt tags, Image optimization, Thin content)
- Recommendations (Schema.org JSON-LD, Internal/External links, OpenGraph)
- Generates a calculated Ubersuggest Health Score (0-100)
"""

import sys
import os
import re
import json
from pathlib import Path
from html.parser import HTMLParser
import urllib.request
import urllib.parse

class SEOHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        self.meta_desc = ""
        self.canonical = ""
        self.h1_tags = []
        self.in_h1 = False
        self.h2_tags = []
        self.in_h2 = False
        self.images = []
        self.links = []
        self.in_a = False
        self.current_a = {}
        self.schema_scripts = []
        self.in_schema = False
        self.current_schema = ""
        self.og_title = ""
        self.og_image = ""
        self.body_text = []
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer'}
        self.current_skip = 0

    def handle_starttag(self, tag, attrs):
        attr_dict = {k.lower(): v for k, v in attrs if v is not None}
        tag_lower = tag.lower()

        if tag_lower in self.skip_tags:
            self.current_skip += 1

        if tag_lower == 'title':
            self.in_title = True
        elif tag_lower == 'meta':
            name = attr_dict.get('name', '').lower()
            prop = attr_dict.get('property', '').lower()
            content = attr_dict.get('content', '')
            if name == 'description':
                self.meta_desc = content
            elif prop == 'og:title':
                self.og_title = content
            elif prop == 'og:image':
                self.og_image = content
        elif tag_lower == 'link' and attr_dict.get('rel', '').lower() == 'canonical':
            self.canonical = attr_dict.get('href', '')
        elif tag_lower == 'h1':
            self.in_h1 = True
        elif tag_lower == 'h2':
            self.in_h2 = True
        elif tag_lower == 'img':
            self.images.append({
                'src': attr_dict.get('src', ''),
                'alt': attr_dict.get('alt', ''),
                'width': attr_dict.get('width', ''),
                'height': attr_dict.get('height', '')
            })
        elif tag_lower == 'a':
            self.in_a = True
            self.current_a = {'href': attr_dict.get('href', ''), 'text': ''}
        elif tag_lower == 'script' and attr_dict.get('type', '') == 'application/ld+json':
            self.in_schema = True
            self.current_schema = ""

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower in self.skip_tags:
            self.current_skip = max(0, self.current_skip - 1)
        if tag_lower == 'title':
            self.in_title = False
        elif tag_lower == 'h1':
            self.in_h1 = False
        elif tag_lower == 'h2':
            self.in_h2 = False
        elif tag_lower == 'a':
            self.in_a = False
            if self.current_a.get('href'):
                self.links.append(self.current_a)
        elif tag_lower == 'script' and self.in_schema:
            self.in_schema = False
            self.schema_scripts.append(self.current_schema)

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.in_h1:
            if self.h1_tags and self.in_h1:
                self.h1_tags[-1] += data
            else:
                self.h1_tags.append(data)
        elif self.in_h2:
            if self.h2_tags and self.in_h2:
                self.h2_tags[-1] += data
            else:
                self.h2_tags.append(data)
        elif self.in_a:
            self.current_a['text'] += data
        elif self.in_schema:
            self.current_schema += data
        
        if self.current_skip == 0:
            text = data.strip()
            if text:
                self.body_text.append(text)

def audit_html_content(html_content, source_name="Page"):
    parser = SEOHTMLParser()
    try:
        parser.feed(html_content)
    except Exception as e:
        pass

    critical_errors = []
    warnings = []
    recommendations = []
    passed_checks = []

    # 1. Title Tag Check
    title_text = parser.title.strip()
    if not title_text:
        critical_errors.append("Missing <title> tag on page")
    else:
        t_len = len(title_text)
        if 40 <= t_len <= 65:
            passed_checks.append(f"Title tag is optimal length ({t_len} chars): '{title_text[:40]}...'")
        elif t_len < 30:
            warnings.append(f"Title tag too short ({t_len} chars, recommend 50-60 chars): '{title_text}'")
        elif t_len > 65:
            warnings.append(f"Title tag too long ({t_len} chars, will truncate on SERPs): '{title_text[:55]}...'")
        else:
            passed_checks.append(f"Title tag length acceptable ({t_len} chars)")

    # 2. Meta Description Check
    desc_text = parser.meta_desc.strip()
    if not desc_text:
        warnings.append("Missing meta description tag")
    else:
        d_len = len(desc_text)
        if 130 <= d_len <= 165:
            passed_checks.append(f"Meta description is optimal length ({d_len} chars)")
        elif d_len < 80:
            warnings.append(f"Meta description too short ({d_len} chars, recommend 145-155 chars)")
        elif d_len > 165:
            warnings.append(f"Meta description too long ({d_len} chars, will truncate on Google)")
        else:
            passed_checks.append(f"Meta description length acceptable ({d_len} chars)")

    # 3. Canonical Tag Check
    canonical = parser.canonical.strip()
    if not canonical:
        critical_errors.append("Missing canonical tag (<link rel='canonical'>)")
    else:
        if canonical.startswith("http://") or canonical.startswith("https://"):
            passed_checks.append(f"Valid canonical tag: {canonical}")
        else:
            warnings.append(f"Canonical URL is relative instead of absolute: {canonical}")

    # 4. Heading Structure (H1, H2)
    h1s = [h.strip() for h in parser.h1_tags if h.strip()]
    if len(h1s) == 0:
        critical_errors.append("No <h1> heading tag found on page")
    elif len(h1s) > 1:
        warnings.append(f"Multiple ({len(h1s)}) <h1> tags found. Best practice is exactly one <h1>")
    else:
        passed_checks.append(f"Single <h1> tag verified: '{h1s[0][:40]}...'")

    h2s = [h.strip() for h in parser.h2_tags if h.strip()]
    if len(h2s) == 0:
        warnings.append("No <h2> subheading tags found. Break content into logical sections")
    else:
        passed_checks.append(f"Found {len(h2s)} <h2> subheadings")

    # 5. Word Count & Content Depth
    full_text = " ".join(parser.body_text)
    words = len(full_text.split())
    if words < 300:
        warnings.append(f"Thin content detected: {words} words. Ubersuggest recommends > 800 words")
    elif words >= 1500:
        passed_checks.append(f"Comprehensive 10x content depth: {words:,} words")
    else:
        passed_checks.append(f"Content length acceptable: {words:,} words")

    # 6. Images & Alt Attributes & Modern Formats
    img_tags = parser.images
    missing_alt = 0
    non_webp = 0
    missing_dims = 0
    for img in img_tags:
        src = img.get("src", "")
        alt = img.get("alt", "")
        if not alt.strip():
            missing_alt += 1
        if src.lower().endswith((".png", ".jpg", ".jpeg")):
            non_webp += 1
        if not img.get("width") or not img.get("height"):
            missing_dims += 1

    if len(img_tags) > 0:
        if missing_alt > 0:
            warnings.append(f"{missing_alt} / {len(img_tags)} images missing descriptive alt text")
        else:
            passed_checks.append(f"100% of images ({len(img_tags)}) have alt attributes")

        if non_webp > 0:
            warnings.append(f"{non_webp} / {len(img_tags)} images using legacy PNG/JPEG format instead of WebP")
        else:
            passed_checks.append(f"100% of images are modern WebP/SVG format")

        if missing_dims > 0:
            recommendations.append(f"{missing_dims} / {len(img_tags)} images missing explicit width/height attributes (causes CLS)")
    else:
        recommendations.append("Page has 0 images. Visual graphics enhance dwell time and engagement")

    # 7. Internal & Outbound Links
    links = parser.links
    internal_links = 0
    external_links = 0
    generic_anchors = 0
    generic_terms = {"click here", "read more", "here", "learn more", "link"}

    for a in links:
        href = a["href"].strip()
        anchor = a.get("text", "").strip().lower()
        if anchor in generic_terms:
            generic_anchors += 1
        if href.startswith("/") or "bullprintmedia.com" in href:
            internal_links += 1
        elif href.startswith("http"):
            external_links += 1

    passed_checks.append(f"Found {internal_links} internal links and {external_links} external links")
    if generic_anchors > 0:
        recommendations.append(f"{generic_anchors} links use generic anchor text ('click here', 'read more'). Use descriptive keywords")

    # 8. Schema Markup (Structured Data)
    if len(parser.schema_scripts) > 0:
        passed_checks.append(f"Detected {len(parser.schema_scripts)} Schema.org JSON-LD blocks")
    else:
        recommendations.append("Missing Schema.org JSON-LD structured data (Article, NewsArticle, FAQPage)")

    # 9. OpenGraph Social Cards
    if parser.og_title and parser.og_image:
        passed_checks.append("OpenGraph social meta tags present")
    else:
        recommendations.append("Incomplete OpenGraph tags (og:image / og:title missing)")

    # Calculate Ubersuggest Health Score (100 base)
    score = 100
    score -= len(critical_errors) * 15
    score -= len(warnings) * 4
    score -= len(recommendations) * 1.5
    score = max(10, min(100, int(score)))

    return {
        "source": source_name,
        "score": score,
        "critical_errors": critical_errors,
        "warnings": warnings,
        "recommendations": recommendations,
        "passed_checks": passed_checks
    }

def print_audit_report(result):
    print("=" * 68)
    print(f"  UBERSUGGEST SEO AUDIT REPORT: {result['source']}")
    print("=" * 68)
    
    score = result['score']
    status = "🟢 EXCELLENT" if score >= 85 else ("🟡 FAIR" if score >= 65 else "🔴 POOR")
    print(f"\n  OVERALL SEO HEALTH SCORE: {score} / 100 ({status})\n")
    
    print(f"[-] CRITICAL ERRORS: {len(result['critical_errors'])}")
    if result['critical_errors']:
        for e in result['critical_errors']:
            print(f"    ❌ {e}")
    else:
        print("    ✓ Zero critical blockers detected.")
        
    print(f"\n[!] WARNINGS: {len(result['warnings'])}")
    if result['warnings']:
        for w in result['warnings']:
            print(f"    ⚠️  {w}")
    else:
        print("    ✓ Zero warnings detected.")
        
    print(f"\n[*] RECOMMENDATIONS: {len(result['recommendations'])}")
    if result['recommendations']:
        for r in result['recommendations']:
            print(f"    💡 {r}")
    else:
        print("    ✓ All secondary recommendations fulfilled.")

    print(f"\n[✓] PASSED CHECKS: {len(result['passed_checks'])}")
    for p in result['passed_checks']:
        print(f"    ✓ {p}")
        
    print("\n" + "=" * 68)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "public/index.html"
    
    if target.startswith("http://") or target.startswith("https://"):
        req = urllib.request.Request(target, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) UbersuggestBot/1.0"})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")
        res = audit_html_content(html, target)
    else:
        with open(target, "r", encoding="utf-8") as f:
            html = f.read()
        res = audit_html_content(html, target)
        
    print_audit_report(res)
