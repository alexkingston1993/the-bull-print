# The Ubersuggest 100-Point Technical & On-Page SEO Checklist

This checklist mirrors the exact scoring criteria and diagnostic checks used by **Ubersuggest** and **NP Digital** enterprise auditing tools to score website health from 0 to 100.

---

## 1. Crawlability & Indexation (Weight: 25%)

| Check | Target Standard | Failure Condition | Diagnostic & Fix |
| :--- | :--- | :--- | :--- |
| **Robots.txt Presence** | Valid `robots.txt` at root (`/robots.txt`) | Missing (404) or empty | Ensure `User-agent: *` with clean disallows and XML Sitemap location. |
| **Robots.txt Directives** | Disallows only admin, private, and internal dynamic API endpoints | Disallows root `/` or CSS/JS assets | Remove `Disallow: /` or disallows on `brand_assets/`, `styles.css`, or images. |
| **XML Sitemap** | Valid XML sitemap (`/sitemap.xml`) submitted to GSC & Bing | Missing sitemap, malformed XML, or URLs returning non-200 HTTP codes | Ensure sitemap contains clean canonical 200 URLs with `<lastmod>` tags. |
| **Meta Robots Tag** | `<meta name="robots" content="index, follow">` on public pages | `noindex` or `nofollow` on money pages | Verify no accidental `noindex` tags injected by staging or CMS configurations. |
| **Canonical Tags** | Self-referential canonical `<link rel="canonical" href="...">` | Missing, relative URLs, or pointing to 404/redirecting URLs | Enforce absolute canonical URLs matching the primary protocol and trailing slash rule. |
| **HTTP Status Codes** | 100% of internal links return HTTP 200 OK | Presence of internal 404s, 500s, or 302 temporary redirects | Replace internal links pointing to redirects with direct destination URLs; 301 redirect dead 404s. |
| **Redirect Chains & Loops** | Direct 1-hop 301 redirects only (`A ➔ B`) | 2+ hops (`A ➔ B ➔ C`) or infinite redirect loops | Flatten redirect chains to point directly to final destination. |
| **Hreflang Implementation** | Valid hreflang tags for multi-region/language content | Broken language codes or missing self-referential return tags | Validate ISO 639-1 language and ISO 3166-1 alpha-2 country codes. |

---

## 2. On-Page SEO & Content Quality (Weight: 30%)

| Check | Target Standard | Failure Condition | Diagnostic & Fix |
| :--- | :--- | :--- | :--- |
| **Title Tag Existence** | 100% of indexable pages have unique `<title>` tags | Missing `<title>` or empty tag | Generate unique titles for every page. |
| **Title Tag Length** | **50 to 60 characters** (500-580px width) | < 30 chars (wasteful) or > 65 chars (truncated in SERP) | Rewrite using Neil Patel CTR formula: Hook + Primary Keyword + Year. |
| **Meta Description Presence** | 100% of pages have `<meta name="description">` | Missing or duplicate descriptions | Draft unique, persuasive descriptions with primary keyword and CTA. |
| **Meta Description Length**| **140 to 155 characters** | < 80 chars or > 165 chars | Optimize character count so description displays fully without truncation. |
| **H1 Tag Structure** | Exactly **one `<h1>`** per page containing primary keyword | 0 H1s, multiple H1s, or generic text (e.g. *"Home"*) | Set primary title as `<h1>`, convert subtitles and section headers to `<h2>`/`<h3>`. |
| **Subheading Hierarchy** | Clean nested structure (`H1 ➔ H2 ➔ H3`) | Skipping heading levels (e.g. `H1 ➔ H3` or `H4 ➔ H2`) | Ensure logical document outline for accessibility screen readers and crawlers. |
| **Content Depth (Thin Content)**| Minimum 800 words for articles; 2,000+ for pillar guides | Word count < 300 words on non-utility pages | Expand thin pages with case studies, FAQs, data tables, and actionable steps. |
| **Keyword In First 100 Words**| Primary search keyword appears in first 100 words | Keyword first appears late in the article | Hook the reader and search engine within the opening paragraph. |
| **LSI / Semantic Keyword Density**| Natural inclusion of synonyms and secondary intent keywords | Keyword stuffing (> 3% density) or zero semantic variance | Use natural LSI keywords discovered via Ubersuggest keyword suggestions. |
| **Image Alt Attributes** | 100% of `<img>` tags have descriptive `alt` text | Missing `alt` or empty `alt=""` on editorial images | Add descriptive, keyword-rich alt tags explaining the image context. |
| **Outbound External Links** | 2 to 4 citations to high-authority, non-competing domains | Zero external links or linking to low-quality spam sites | Link to official research (.gov, .edu, SEBI, SEC, Bloomberg, Reuters). |
| **Internal Linking Depth** | 3 to 6 contextual internal links per article | Orphan pages with 0 incoming links, or click depth > 3 | Build Hub & Spoke links pointing from clusters back to pillar pages. |

---

## 3. Site Speed & Core Web Vitals (Weight: 25%)

| Metric / Check | Ubersuggest Good Threshold | Needs Improvement | Poor / Failing |
| :--- | :--- | :--- | :--- |
| **Largest Contentful Paint (LCP)** | **< 2.5 seconds** | 2.5s – 4.0s | > 4.0 seconds |
| **Interaction to Next Paint (INP)** | **< 200 ms** | 200ms – 500ms | > 500 ms |
| **Cumulative Layout Shift (CLS)** | **< 0.10** | 0.10 – 0.25 | > 0.25 |
| **Total Blocking Time (TBT)** | **< 200 ms** | 200ms – 600ms | > 600 ms |
| **Time to First Byte (TTFB)** | **< 800 ms** | 800ms – 1,800ms | > 1,800 ms |
| **Image Compression** | 100% modern WebP / AVIF format | Large uncompressed PNGs/JPEGs | Files > 150 KB |
| **Image Dimensions** | Explicit `width` & `height` attributes on all images | Missing dimensions (causes CLS reflow) | Zero dimensions |
| **Render-Blocking Resources** | Critical CSS inlined; scripts deferred (`defer`/`async`) | Synchronous JS files in `<head>` blocking FCP | > 500ms wasted |

---

## 4. Mobile Usability & Technical Architecture (Weight: 20%)

* **Viewport Tag**: Must include `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.
* **Touch Target Sizing**: All buttons, links, and navigation items must be at least **48x48px** with at least **8px separation** to prevent accidental clicks.
* **Readable Font Sizing**: Body text must be at least **16px** with a line-height of **1.5 to 1.6** to prevent pinch-zooming on mobile devices.
* **Structured Data (Schema.org)**:
  * `NewsArticle` or `Article` on all editorial content.
  * `FAQPage` schema on articles containing Q&A sections (to capture rich SERP snippets).
  * `BreadcrumbList` to display clean navigation paths in Google search results.
  * `Organization` or `NewsMediaOrganization` on homepage with verified social links.
* **OpenGraph & Twitter Cards**:
  * `og:title`, `og:description`, `og:image` (1200x630px WebP), `og:url`, `og:type`.
  * `twitter:card` set to `summary_large_image`.
