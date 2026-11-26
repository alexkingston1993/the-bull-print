import os
import re
import json
import yaml
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "content" / "posts"
POSTS_JSON = ROOT / "content" / "posts.json"
PUB_POSTS_JSON = ROOT / "public" / "content" / "posts.json"
SITEMAP_PATH = ROOT / "public" / "sitemap-articles.xml"

def md_to_html(md_text):
    """Simple clean markdown to HTML converter for article body."""
    # If text is already mostly HTML, return as is
    if "<div" in md_text or "<p" in md_text:
        return md_text

    html_lines = []
    in_list = False

    for line in md_text.splitlines():
        line_str = line.strip()
        if not line_str:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        if line_str.startswith("# "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<h1>{line_str[2:]}</h1>")
        elif line_str.startswith("## "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<h2>{line_str[3:]}</h2>")
        elif line_str.startswith("### "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<h3>{line_str[4:]}</h3>")
        elif line_str.startswith("> "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f"<blockquote><p>{line_str[2:]}</p></blockquote>")
        elif line_str.startswith("* ") or line_str.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            item_text = line_str[2:]
            # inline bold
            item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item_text)
            html_lines.append(f"<li>{item_text}</li>")
        else:
            if in_list: html_lines.append("</ul>"); in_list = False
            p_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line_str)
            html_lines.append(f"<p>{p_text}</p>")

    if in_list:
        html_lines.append("</ul>")

    return "\n".join(html_lines)

def compile_all_posts():
    print("🚀 Starting compilation of all articles into posts.json...")
    
    # 1. Load existing posts
    existing_posts = []
    seen_slugs = set()
    if POSTS_JSON.exists():
        with open(POSTS_JSON, "r", encoding="utf-8") as f:
            existing_posts = json.load(f)
            for p in existing_posts:
                if p.get("slug"):
                    seen_slugs.add(p["slug"])
                for alias in p.get("aliases", []):
                    seen_slugs.add(alias)

    print(f"Loaded {len(existing_posts)} existing registered posts in posts.json.")

    new_posts = []
    md_files = sorted(POSTS_DIR.glob("*.md"))
    print(f"Found {len(md_files)} markdown files in {POSTS_DIR}...")

    for f in md_files:
        stem = f.stem
        # Clean slug
        clean_slug = re.sub(r'[^a-z0-9\-]', '-', stem.lower())
        clean_slug = re.sub(r'-+', '-', clean_slug).strip('-')

        if clean_slug in seen_slugs or stem in seen_slugs:
            continue

        raw = f.read_text(encoding="utf-8", errors="ignore")
        fm = {}
        body = raw

        if raw.startswith("---"):
            parts = raw.split("---", 2)
            if len(parts) >= 3:
                try:
                    fm = yaml.safe_load(parts[1]) or {}
                except Exception:
                    # Fallback simple parser
                    for line in parts[1].splitlines():
                        if ":" in line:
                            k, v = line.split(":", 1)
                            fm[k.strip()] = v.strip().strip('"').strip("'")
                body = parts[2].strip()

        title = fm.get("title") or stem.replace("-", " ").title()
        slug = fm.get("slug") or clean_slug
        slug = re.sub(r'[^a-z0-9\-]', '-', slug.lower())
        slug = re.sub(r'-+', '-', slug).strip('-')

        if slug in seen_slugs:
            continue

        yt_id = fm.get("youtube_video_id")
        if not yt_id:
            # Check body for yt id
            yt_match = re.search(r'(?:youtube\.com/embed/|youtu\.be/|youtube\.com/watch\?v=)([a-zA-Z0-9_-]{11})', body)
            if yt_match:
                yt_id = yt_match.group(1)

        yt_url = fm.get("youtubeUrl") or (f"https://www.youtube.com/watch?v={yt_id}" if yt_id else None)
        excerpt = fm.get("excerpt") or fm.get("description") or ""
        if not excerpt:
            # First paragraph
            first_p = [p.strip() for p in body.split("\n\n") if p.strip() and not p.startswith("#") and not p.startswith("<")]
            excerpt = first_p[0][:180] if first_p else title

        word_count = len(body.split())
        reading_time = max(1, word_count // 200)

        # Build clean HTML
        html_content = body if ("<div" in body or "<p" in body) else md_to_html(body)
        if yt_id and "video-embed-container" not in html_content:
            embed_header = f"""<div class="video-embed-container" style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin:28px 0; border:1px solid rgba(255,255,255,0.1); box-shadow:0 8px 30px rgba(0,0,0,0.5);">
 <iframe src="https://www.youtube.com/embed/{yt_id}" title="{title}" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allowfullscreen></iframe>
</div>\n\n"""
            html_content = embed_header + html_content

        date_val = str(fm.get("date") or "2026-11-20")
        if len(date_val) == 10:
            date_val = f"{date_val} 12:00:00"

        categories = fm.get("categories") or ([fm["category"]] if "category" in fm else ["Market Analysis", "The Bull Print"])
        if isinstance(categories, str):
            categories = [categories]

        tags = fm.get("tags") or ["StockMarket", "Finance", "TheBullPrint"]
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        post_obj = {
            "slug": slug,
            "aliases": [stem] if stem != slug else [],
            "title": title,
            "date": date_val,
            "excerpt": excerpt,
            "focusKeyword": fm.get("focusKeyword") or title.lower(),
            "categories": categories,
            "tags": tags,
            "youtubeUrl": yt_url,
            "coverImage": fm.get("coverImage") or "/brand_assets/cover_master_1920x1080.png",
            "html": html_content,
            "schema": {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "Article",
                        "headline": title,
                        "description": excerpt,
                        "datePublished": date_val.replace(" ", "T") + "+00:00",
                        "mainEntityOfPage": {
                            "@type": "WebPage",
                            "@id": f"https://bullprintmedia.com/posts/{slug}"
                        },
                        "author": {
                            "@type": "Organization",
                            "name": "The Bull Print Research Desk"
                        }
                    }
                ]
            },
            "wordCount": word_count,
            "readingTime": reading_time,
            "author": fm.get("author") or "The Bull Print Research Desk"
        }

        if yt_id and yt_url:
            post_obj["schema"]["@graph"].append({
                "@type": "VideoObject",
                "name": title,
                "description": excerpt,
                "thumbnailUrl": [f"https://i.ytimg.com/vi/{yt_id}/maxresdefault.jpg"],
                "uploadDate": date_val.replace(" ", "T") + "+00:00",
                "embedUrl": f"https://www.youtube.com/embed/{yt_id}"
            })

        new_posts.append(post_obj)
        seen_slugs.add(slug)
        seen_slugs.add(stem)

    print(f"Compiled {len(new_posts)} new articles from markdown files!")
    total_posts = existing_posts + new_posts
    print(f"Total articles now indexed: {len(total_posts)}")

    # Save to content/posts.json and public/content/posts.json
    with open(POSTS_JSON, "w", encoding="utf-8") as f:
        json.dump(total_posts, f, indent=2, ensure_ascii=False)
    with open(PUB_POSTS_JSON, "w", encoding="utf-8") as f:
        json.dump(total_posts, f, indent=2, ensure_ascii=False)
    print("✓ Successfully synchronized content/posts.json and public/content/posts.json")

    # 4. Regenerate public/sitemap-articles.xml
    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in total_posts:
        slug = p.get("slug")
        if not slug: continue
        d = p.get("date", "2026-11-26")[:10]
        sitemap_lines.append("  <url>")
        sitemap_lines.append(f"    <loc>https://bullprintmedia.com/posts/{slug}</loc>")
        sitemap_lines.append(f"    <lastmod>{d}</lastmod>")
        sitemap_lines.append("    <changefreq>weekly</changefreq>")
        sitemap_lines.append("    <priority>0.8</priority>")
        sitemap_lines.append("  </url>")
    sitemap_lines.append("</urlset>")

    SITEMAP_PATH.write_text("\n".join(sitemap_lines), encoding="utf-8")
    print(f"✓ Successfully generated {SITEMAP_PATH} with {len(total_posts)} article URLs!")

if __name__ == "__main__":
    compile_all_posts()
