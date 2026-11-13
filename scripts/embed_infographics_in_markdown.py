import os
import re
import json

with open('content/posts.json') as f:
    posts = json.load(f)

posts_by_slug = {p['slug']: p for p in posts}

posts_dir = 'content/posts'
files = [f for f in os.listdir(posts_dir) if f.endswith('.md')]

updated_count = 0

for fname in files:
    fpath = os.path.join(posts_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find slug
    slug = None
    slug_match = re.search(r'^slug:\s*["\']?([^"\'\n]+)["\']?', content, re.MULTILINE)
    if slug_match:
        slug = slug_match.group(1).strip()
    else:
        slug = os.path.splitext(fname)[0]

    post_meta = posts_by_slug.get(slug)
    if not post_meta:
        continue

    infographic_url = post_meta.get('infographic')
    cover_url = post_meta.get('coverImage')
    alt_text = post_meta.get('imageAlt', post_meta.get('title'))
    caption_text = post_meta.get('imageCaption', 'Quantitative breakdown and regulatory telemetry by The Bull Print Research Desk.')

    # Update Frontmatter with coverImage and infographic if missing
    if 'coverImage:' not in content:
        content = re.sub(
            r'(---\s*\n)',
            f'\\1coverImage: "{cover_url}"\ninfographic: "{infographic_url}"\nimageAlt: "{alt_text}"\n',
            content,
            count=1
        )

    # Insert infographic figure into the markdown body if not already present
    if 'article-infographic-embed' not in content and infographic_url:
        figure_html = f'''
 <!-- Tailor-Made Research Infographic for SEO & AI Overviews -->
 <figure class="article-infographic-embed" style="margin:28px 0; background:rgba(11,19,36,0.6); border:1px solid rgba(255,255,255,0.08); border-radius:12px; overflow:hidden;">
 <img src="{infographic_url}" alt="{alt_text}" title="{alt_text}" style="width:100%; height:auto; display:block; border-bottom:1px solid rgba(255,255,255,0.08);" loading="lazy" decoding="async">
 <figcaption style="padding:12px 18px; font-size:13px; color:#94a3b8; font-family:var(--font-body); display:flex; align-items:center; gap:8px;">
 <span>📊</span> <span><strong>Infographic:</strong> {caption_text}</span>
 </figcaption>
 </figure>
'''
        # Place right after TL;DR box if present, or after frontmatter
        if '</div>\n\n <!-- 2.' in content:
            content = content.replace('</div>\n\n <!-- 2.', f'</div>\n{figure_html}\n <!-- 2.', 1)
        elif '</div>\n\n' in content:
            content = content.replace('</div>\n\n', f'</div>\n{figure_html}\n', 1)
        else:
            content = content + f"\n\n{figure_html}"

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    updated_count += 1

print(f"Successfully embedded tailor-made infographics in {updated_count} markdown articles!")
