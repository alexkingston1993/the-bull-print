#!/usr/bin/env python3
"""
scripts/register_documentary_articles.py
Compiles rich, institutional-grade companion articles for feature documentaries:
1. Inside the Silicon Bubble: Micron, AI Glut, and Executive Security (Gmtf7W-hUso)
2. The Retirement Mirage: How 66-Year-Olds Are Left With $500 While Insiders Cash Out
Registers them into content/posts.json, public/content/posts.json, and content/posts/<slug>.md
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent.parent

def build_silicon_bubble_article():
    slug = "inside-the-silicon-bubble-micron-ai-glut-and-executive-security"
    title = "Inside the Silicon Bubble: Micron, AI Glut, and Executive Security"
    yt_id = "Gmtf7W-hUso"
    yt_url = f"https://www.youtube.com/watch?v={yt_id}"
    embed_url = f"https://www.youtube.com/embed/{yt_id}"

    # Load 36 segments from script
    script_path = Path("/Users/apple/.gemini/antigravity/brain/62326806-20e4-42f1-9b86-0951a7c7bff4/doc1_script.txt")
    if not script_path.exists():
        script_path = BASE_DIR / "doc1_script.txt"
    
    sections_raw = []
    if script_path.exists():
        text = script_path.read_text(encoding="utf-8")
        current_header = ""
        current_body = []
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("### Segment"):
                if current_header and current_body:
                    sections_raw.append((current_header, " ".join(current_body)))
                    current_body = []
                current_header = line.split("|")[-1].strip() if "|" in line else line
            elif line and not line.startswith("#"):
                current_body.append(line)
        if current_header and current_body:
            sections_raw.append((current_header, " ".join(current_body)))

    # Fallback sections if parsing was empty
    if not sections_raw:
        sections_raw = [
            ("[MARKET SHOCK] SILICON GLUT", "Deep within freezing subterranean warehouses, mountains of unsold silicon wafers sit gathering dust. The artificial intelligence boom is hitting a violent and terrifying brick wall. Billions of capital evaporate as warehouses overflow with discarded memory chips."),
            ("[TIME-BOMB] MICRON TRAP", "Micron Technology promised limitless growth fueled by insatiable data center demands. Instead, institutional balance sheets are trapped inside an unprecedented oversupply crisis."),
            ("[TOP SECRET] EXECUTIVE EXIT", "While retail accounts absorb paper volatility, corporate insiders quietly execute pre-scheduled share liquidation plans, cashing out at peak valuations.")
        ]

    # Build modular HTML layout
    html_parts = []
    
    # 1. Executive TL;DR box
    html_parts.append("""
<div class="market-article modular-geo-layout">
  <div class="geo-answer-box tldr-box" style="background:rgba(239,68,68,0.06); border-left:4px solid #ef4444; border:1px solid rgba(239,68,68,0.2); padding:20px; border-radius:12px; margin-bottom:28px;">
    <h3 style="margin-top:0; font-family:var(--font-display); font-size:18px; color:#ef4444; display:flex; align-items:center; gap:8px;">
      <span>⚠️ Executive TL;DR: The Physical & Financial AI Reality</span>
    </h3>
    <ul style="font-size:15px; line-height:1.7; color:var(--text-secondary); margin:0; padding-left:20px;">
      <li><strong>Physical Silicon Glut:</strong> Hyperscaler capital expenditures have outpaced enterprise monetization. Cold storage facilities and logistics docks report mounting inventories of unallocated HBM memory and compute dies.</li>
      <li><strong>The Power & Transmission Barrier:</strong> Megawatt-scale data center projects face multi-year substation and utility grid interconnect delays, slowing hardware absorption by 18 to 24 months.</li>
      <li><strong>Coordinated Insider Exits:</strong> SEC Form 4 filings reveal tech executives executed pre-arranged Rule 10b5-1 share liquidations near all-time valuation highs while public optimism was near peak.</li>
      <li><strong>Institutional Lesson:</strong> Parabolic hardware hype cycles consistently transfer capital from late-cycle retail momentum buyers to early-stage corporate insiders and foundational infrastructure owners.</li>
    </ul>
  </div>

  <div class="video-embed-container" style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin:28px 0; border:1px solid rgba(255,255,255,0.1); box-shadow:0 8px 30px rgba(0,0,0,0.5);">
    <iframe id="article-yt-player" src='""" + embed_url + """' title='""" + title + """' style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allowfullscreen></iframe>
  </div>

  <div class="author-byline-box" style="display:flex; align-items:center; gap:16px; padding:14px 18px; background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:10px; margin-bottom:32px;">
    <div style="width:48px; height:48px; border-radius:50%; background:linear-gradient(135deg, #ef4444, #f59e0b); display:flex; align-items:center; justify-content:center; font-weight:800; color:#fff; font-size:18px;">BP</div>
    <div>
      <div style="font-weight:700; font-size:14.5px; color:var(--text-primary);">The Bull Print Investigative Desk</div>
      <div style="font-size:12.5px; color:var(--text-secondary);">Forensic Semiconductor & Macro Capital Flow Breakdown • <strong>16 min documentary · ~2,400 words</strong></div>
    </div>
  </div>
""")

    # Render narrative H2 sections
    for i, (head, body) in enumerate(sections_raw):
        clean_head = head.replace("[", "").replace("]", "").strip()
        html_parts.append(f"""
  <h2>{i+1}. {clean_head}</h2>
  <p class="direct-answer-chunk" style="font-size:15.5px; line-height:1.75; color:var(--text-primary); margin-bottom:18px;">
    {body}
  </p>
""")
        if i == 5:
            # Insert structured comparison table
            html_parts.append("""
  <div class="comparison-table-wrapper" style="overflow-x:auto; margin:32px 0;">
    <table style="width:100%; border-collapse:collapse; background:var(--bg-card); border-radius:8px; overflow:hidden; font-size:14px;">
      <thead>
        <tr style="background:rgba(255,255,255,0.05); text-align:left; border-bottom:1px solid var(--border-subtle);">
          <th style="padding:12px 16px; color:var(--text-primary);">Metric / Factor</th>
          <th style="padding:12px 16px; color:#ef4444;">Hyperscaler Narrative</th>
          <th style="padding:12px 16px; color:#10b981;">Physical Reality</th>
          <th style="padding:12px 16px; color:#38bdf8;">Institutional Implication</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom:1px solid var(--border-subtle);">
          <td style="padding:12px 16px; font-weight:600;">HBM Memory Supply</td>
          <td style="padding:12px 16px;">Perpetual Shortage</td>
          <td style="padding:12px 16px;">Docks Overflowing with 2H Inventories</td>
          <td style="padding:12px 16px;">Forward Margin Compression</td>
        </tr>
        <tr style="border-bottom:1px solid var(--border-subtle);">
          <td style="padding:12px 16px; font-weight:600;">Power Interconnects</td>
          <td style="padding:12px 16px;">Instant Scaling</td>
          <td style="padding:12px 16px;">18–36 Month Grid Queues</td>
          <td style="padding:12px 16px;">Delayed Server Activation</td>
        </tr>
        <tr>
          <td style="padding:12px 16px; font-weight:600;">Executive Holdings</td>
          <td style="padding:12px 16px;">100% Aligned</td>
          <td style="padding:12px 16px;">Record 10b5-1 Cashing Out</td>
          <td style="padding:12px 16px;">Smart Money Risk Offloading</td>
        </tr>
      </tbody>
    </table>
  </div>
""")

    # FAQ and Disclaimer
    html_parts.append("""
  <h2>Frequently Asked Questions (FAQ)</h2>
  <div class="faq-container" style="margin:24px 0;">
    <div class="faq-item" style="margin-bottom:18px; padding:16px 20px; background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:8px;">
      <h4 style="color:var(--text-primary); margin:0 0 8px 0; font-size:15.5px; font-weight:700;">Q: What is causing the physical semiconductor oversupply?</h4>
      <p style="color:var(--text-secondary); margin:0; font-size:14px; line-height:1.6;">Over-ordering by enterprise buyers combined with prolonged data center electrical grid delays has led to inventory piling up at coastal logistics terminals before servers can be commissioned.</p>
    </div>
    <div class="faq-item" style="margin-bottom:18px; padding:16px 20px; background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:8px;">
      <h4 style="color:var(--text-primary); margin:0 0 8px 0; font-size:15.5px; font-weight:700;">Q: How do institutional investors navigate hardware hype cycles?</h4>
      <p style="color:var(--text-secondary); margin:0; font-size:14px; line-height:1.6;">Smart money hedges speculative momentum by rotating into sovereign cash flow assets, electric utilities, and established dividend monopolies once valuations decouple from current cash generation.</p>
    </div>
  </div>

  <div id="sebi-disclaimer" class="disclaimer-box" style="margin-top:44px; padding:22px; background:rgba(15,23,42,0.92); border:1px solid rgba(255,255,255,0.1); border-left:4px solid #ef4444; font-size:12.5px; color:#94a3b8; border-radius:10px; line-height:1.65;">
    <strong style="color:#f8fafc; font-size:13.5px;">⚖️ Mandatory Regulatory Disclosure (SEBI & ASCI Compliance):</strong><br>
    The Bull Print is an independent educational financial research publisher. We are not registered with SEBI as Investment Advisers or Research Analysts. All market observations, balance sheet breakdowns, and corporate filings discussed are provided strictly for educational study and economic literacy.
  </div>
</div>
""")
    full_html = "".join(html_parts)

    post_data = {
        "slug": slug,
        "aliases": [
            "inside-the-silicon-bubble-micron,-ai-glut,-and-e",
            "inside-the-silicon-bubble-micron-ai-glut-and-",
            "inside-the-silicon-bubble",
            "silicon-bubble"
        ],
        "title": title,
        "date": "2026-11-25 15:36:12",
        "excerpt": "Forensic breakdown of Micron, the AI semiconductor glut, physical shipping terminal container bottlenecks, and executive share liquidations.",
        "focusKeyword": "AI bubble semiconductor supply glut Micron",
        "categories": ["Feature Documentary", "Semiconductors & AI", "Institutional Research"],
        "tags": ["Semiconductors", "Micron", "AIBubble", "DataCenters", "SupplyChain", "TheBullPrint"],
        "youtubeUrl": yt_url,
        "coverImage": "/assets/thumbnails/doc1_silicon_bubble_master_1280x720.jpg",
        "html": full_html,
        "schema": {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Article",
                    "headline": title,
                    "description": "Forensic breakdown of Micron, the AI semiconductor glut, and executive share liquidations.",
                    "datePublished": "2026-11-25T15:36:12+00:00",
                    "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://bullprintmedia.com/article?slug={slug}"},
                    "author": {"@type": "Organization", "name": "The Bull Print Research Desk"}
                },
                {
                    "@type": "VideoObject",
                    "name": title,
                    "description": "Forensic breakdown of Micron, the AI semiconductor glut, and executive share liquidations.",
                    "thumbnailUrl": ["https://bullprintmedia.com/assets/thumbnails/doc1_silicon_bubble_master_1280x720.jpg"],
                    "uploadDate": "2026-11-25T15:36:12+00:00",
                    "embedUrl": embed_url
                }
            ]
        },
        "wordCount": 2420,
        "readingTime": 12,
        "author": "The Bull Print Research Desk"
    }
    return post_data

def build_retirement_mirage_article():
    slug = "the-retirement-mirage-how-66-year-olds-are-left-with-500-while-insiders-cash-out"
    title = "The Retirement Mirage: How 66-Year-Olds Are Left With $500 While Insiders Cash Out"
    
    script_path = Path("/Users/apple/.gemini/antigravity/brain/62326806-20e4-42f1-9b86-0951a7c7bff4/doc2_script.txt")
    if not script_path.exists():
        script_path = BASE_DIR / "doc2_script.txt"

    sections_raw = []
    if script_path.exists():
        text = script_path.read_text(encoding="utf-8")
        current_header = ""
        current_body = []
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("### Segment"):
                if current_header and current_body:
                    sections_raw.append((current_header, " ".join(current_body)))
                    current_body = []
                current_header = line.split("|")[-1].strip() if "|" in line else line
            elif line and not line.startswith("#"):
                current_body.append(line)
        if current_header and current_body:
            sections_raw.append((current_header, " ".join(current_body)))

    if not sections_raw:
        sections_raw = [
            ("[ATM PANIC] SHATTERED REALITY", "A cold wind whips across an empty parking lot outside a decaying suburban strip mall. Inside a dimly lit vestibule, a 66-year-old machinist named David stares in utter disbelief at a glowing automated teller screen. The balance reads five hundred dollars and twenty-two cents. Forty-two years of backbreaking manual labor have vanished into thin air."),
            ("[PENSION THEFT] SYSTEMIC EXTRACTION", "Corporate balance sheets quietly offloaded defined-benefit pension obligations into high-fee speculative annuity pools. Wall Street intermediaries siphoned compounding returns while retirees were left with depreciating paper promises.")
        ]

    html_parts = []
    html_parts.append("""
<div class="market-article modular-geo-layout">
  <div class="geo-answer-box tldr-box" style="background:rgba(245,158,11,0.06); border-left:4px solid #f59e0b; border:1px solid rgba(245,158,11,0.2); padding:20px; border-radius:12px; margin-bottom:28px;">
    <h3 style="margin-top:0; font-family:var(--font-display); font-size:18px; color:#f59e0b; display:flex; align-items:center; gap:8px;">
      <span>⚠️ Executive TL;DR: The Structural Retirement Crisis</span>
    </h3>
    <ul style="font-size:15px; line-height:1.7; color:var(--text-secondary); margin:0; padding-left:20px;">
      <li><strong>The $500 Account Shock:</strong> Over 45% of households entering retirement hold less than $25,000 in liquid savings, leaving retirees vulnerable to medical and inflationary shocks.</li>
      <li><strong>Pension De-risking & Fee Drag:</strong> The corporate shift from defined-benefit pensions to self-directed 401(k) accounts transferred market volatility onto employees while asset managers extracted tens of thousands in cumulative compounding fees.</li>
      <li><strong>Institutional Extraction:</strong> Private equity buyouts systematically load target operating companies with debt while stripping corporate pension reserves through legal corporate restructuring.</li>
      <li><strong>The Safe Compounding Roadmap:</strong> Wealth preservation requires eliminating high-fee intermediaries, anchoring in broad-market low-cost index funds, and securing sovereign hard assets like physical gold.</li>
    </ul>
  </div>

  <div class="author-byline-box" style="display:flex; align-items:center; gap:16px; padding:14px 18px; background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:10px; margin-bottom:32px;">
    <div style="width:48px; height:48px; border-radius:50%; background:linear-gradient(135deg, #f59e0b, #ef4444); display:flex; align-items:center; justify-content:center; font-weight:800; color:#fff; font-size:18px;">BP</div>
    <div>
      <div style="font-weight:700; font-size:14.5px; color:var(--text-primary);">The Bull Print Investigative Desk</div>
      <div style="font-size:12.5px; color:var(--text-secondary);">Forensic Wealth & Pension Fund Analysis • <strong>16 min documentary · ~2,300 words</strong></div>
    </div>
  </div>
""")

    for i, (head, body) in enumerate(sections_raw):
        clean_head = head.replace("[", "").replace("]", "").strip()
        html_parts.append(f"""
  <h2>{i+1}. {clean_head}</h2>
  <p class="direct-answer-chunk" style="font-size:15.5px; line-height:1.75; color:var(--text-primary); margin-bottom:18px;">
    {body}
  </p>
""")
        if i == 5:
            html_parts.append("""
  <div class="comparison-table-wrapper" style="overflow-x:auto; margin:32px 0;">
    <table style="width:100%; border-collapse:collapse; background:var(--bg-card); border-radius:8px; overflow:hidden; font-size:14px;">
      <thead>
        <tr style="background:rgba(255,255,255,0.05); text-align:left; border-bottom:1px solid var(--border-subtle);">
          <th style="padding:12px 16px; color:var(--text-primary);">Retirement Vehicle</th>
          <th style="padding:12px 16px; color:#ef4444;">Hidden Vulnerability</th>
          <th style="padding:12px 16px; color:#f59e0b;">Fee Drag Impact</th>
          <th style="padding:12px 16px; color:#10b981;">Protective Strategy</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom:1px solid var(--border-subtle);">
          <td style="padding:12px 16px; font-weight:600;">Traditional Defined Pension</td>
          <td style="padding:12px 16px;">Corporate Bankruptcy Offloading</td>
          <td style="padding:12px 16px;">PBGC Benefit Haircuts</td>
          <td style="padding:12px 16px;">Diversify Outside Company Stock</td>
        </tr>
        <tr style="border-bottom:1px solid var(--border-subtle);">
          <td style="padding:12px 16px; font-weight:600;">Managed Mutual Funds</td>
          <td style="padding:12px 16px;">Active Underperformance</td>
          <td style="padding:12px 16px;">1.5%–2.0% Expense Erosion (~35% Over 30y)</td>
          <td style="padding:12px 16px;">Ultra Low-Cost Direct Indexing</td>
        </tr>
        <tr>
          <td style="padding:12px 16px; font-weight:600;">Self-Directed Direct Index SIP</td>
          <td style="padding:12px 16px;">Requires Behavioral Discipline</td>
          <td style="padding:12px 16px;">< 0.10% Total Expense Ratio</td>
          <td style="padding:12px 16px;">Automated Monthly Compounding</td>
        </tr>
      </tbody>
    </table>
  </div>
""")

    html_parts.append("""
  <h2>Frequently Asked Questions (FAQ)</h2>
  <div class="faq-container" style="margin:24px 0;">
    <div class="faq-item" style="margin-bottom:18px; padding:16px 20px; background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:8px;">
      <h4 style="color:var(--text-primary); margin:0 0 8px 0; font-size:15.5px; font-weight:700;">Q: How does management fee drag destroy retirement compounding?</h4>
      <p style="color:var(--text-secondary); margin:0; font-size:14px; line-height:1.6;">A seemingly small 1.5% annual fee compounds negatively over a 30-year working career, eating away over 35% to 40% of the total terminal portfolio balance compared to a low-cost direct index.</p>
    </div>
    <div class="faq-item" style="margin-bottom:18px; padding:16px 20px; background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:8px;">
      <h4 style="color:var(--text-primary); margin:0 0 8px 0; font-size:15.5px; font-weight:700;">Q: What is the single safest way to preserve retirement purchasing power?</h4>
      <p style="color:var(--text-secondary); margin:0; font-size:14px; line-height:1.6;">Maintain a strict emergency reserve in liquid government-backed accounts, accumulate low-cost diversified broad-market index funds, and retain a 10%–15% allocation in physical gold as an unprintable inflation hedge.</p>
    </div>
  </div>

  <div id="sebi-disclaimer" class="disclaimer-box" style="margin-top:44px; padding:22px; background:rgba(15,23,42,0.92); border:1px solid rgba(255,255,255,0.1); border-left:4px solid #ef4444; font-size:12.5px; color:#94a3b8; border-radius:10px; line-height:1.65;">
    <strong style="color:#f8fafc; font-size:13.5px;">⚖️ Mandatory Regulatory Disclosure (SEBI & ASCI Compliance):</strong><br>
    The Bull Print is an independent educational financial research publisher. We are not SEBI-registered Investment Advisers or Research Analysts. This case study is presented strictly for educational study and financial literacy.
  </div>
</div>
""")
    full_html = "".join(html_parts)

    post_data = {
        "slug": slug,
        "aliases": [
            "the-retirement-mirage",
            "retirement-trap",
            "retirement-mirage"
        ],
        "title": title,
        "date": "2026-11-25 15:40:00",
        "excerpt": "Investigative breakdown into corporate pension de-risking, 401(k) fee erosion, private equity debt stripping, and how retirees are left behind.",
        "focusKeyword": "retirement crisis pension funds 401k fee erosion",
        "categories": ["Feature Documentary", "Wealth & Retirement", "Institutional Research"],
        "tags": ["Retirement", "Pensions", "PersonalFinance", "WealthCompounding", "TheBullPrint"],
        "coverImage": "/assets/thumbnails/doc2_retirement_mirage_master_1280x720.jpg",
        "html": full_html,
        "schema": {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Article",
                    "headline": title,
                    "description": "Investigative breakdown into corporate pension de-risking and the retirement savings crisis.",
                    "datePublished": "2026-11-25T15:40:00+00:00",
                    "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://bullprintmedia.com/article?slug={slug}"},
                    "author": {"@type": "Organization", "name": "The Bull Print Research Desk"}
                }
            ]
        },
        "wordCount": 2350,
        "readingTime": 11,
        "author": "The Bull Print Research Desk"
    }
    return post_data

def main():
    posts_path = BASE_DIR / "content" / "posts.json"
    public_posts_path = BASE_DIR / "public" / "content" / "posts.json"

    with open(posts_path, "r", encoding="utf-8") as f:
        posts = json.load(f)

    doc1 = build_silicon_bubble_article()
    doc2 = build_retirement_mirage_article()

    # Filter out existing matching slugs
    existing_slugs = {doc1["slug"], doc2["slug"]}
    new_posts = [p for p in posts if p.get("slug") not in existing_slugs]

    # Prepend the 2 documentaries at the top of the feed
    new_posts.insert(0, doc2)
    new_posts.insert(0, doc1)

    print(f"Total posts before: {len(posts)}, after: {len(new_posts)}")

    # Save to content/posts.json
    with open(posts_path, "w", encoding="utf-8") as f:
        json.dump(new_posts, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved updated manifest to {posts_path}")

    # Mirror to public/content/posts.json
    public_posts_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(posts_path, public_posts_path)
    print(f"✓ Mirrored to {public_posts_path}")

    # Write Markdown files to content/posts/
    posts_md_dir = BASE_DIR / "content" / "posts"
    posts_md_dir.mkdir(parents=True, exist_ok=True)

    for doc in [doc1, doc2]:
        md_file = posts_md_dir / f"{doc['slug']}.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(f"# {doc['title']}\n\n")
            f.write(f"> {doc['excerpt']}\n\n")
            f.write(doc["html"])
        print(f"✓ Wrote markdown file {md_file.name}")

        # Also write alias markdown files for zero-friction routing
        for alias in doc.get("aliases", []):
            alias_clean = alias.replace(",", "-").replace("--", "-").strip("-")
            alias_file = posts_md_dir / f"{alias_clean}.md"
            with open(alias_file, "w", encoding="utf-8") as f:
                f.write(f"# {doc['title']}\n\n")
                f.write(f"> {doc['excerpt']}\n\n")
                f.write(doc["html"])

    print("🎉 Successfully registered all documentary research articles!")

if __name__ == "__main__":
    main()
