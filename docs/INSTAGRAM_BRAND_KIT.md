# The Bull Print — Instagram & Meta Brand Kit

**Instagram Account**: [@thebullprint](https://www.instagram.com/thebullprint/)  
**Account ID**: `17841460023302021`  
**Facebook Page**: `1478131388718462` ("The Bull Print")  
**Primary Hub Link**: `https://tbp-cloudflare-orchestrator.cloudflare-orchestrator.workers.dev/links`

---

## 1. Official Instagram Profile Specifications

Copy and paste these exact fields into your Instagram profile settings:

### **Name Field** (Search & Meta AI Indexed — 30 Chars max)
```text
The Bull Print | Macro & Finance
```

### **Category**
`Media/news company` or `Financial service`

### **Bio** (Under 150 Characters — Authority + Mission + CTA)
```text
Macro Forensics & Sovereign Liquidity 📊
Financial freedom for everyone through financial literacy.
🎥 Full 12-Min Briefings 👇
```

### **Website / External Link**
```text
https://tbp-cloudflare-orchestrator.cloudflare-orchestrator.workers.dev/links
```
*(Alternative direct link: `https://www.youtube.com/@TheBullPrint?sub_confirmation=1`)*

---

## 2. Brand Visual Identity

* **Primary Colors**:
  * **Obsidian Black**: `#0B0F17` (Canvas background)
  * **Institutional Charcoal**: `#141A24` (Elevated card surfaces)
  * **Sovereign Gold**: `#FFE600` / `#FACC15` (Primary accents & active highlights)
  * **Titanium White**: `#FFFFFF` (Primary typography)
  * **Slate Muted**: `#94A3B8` (Secondary metadata & labels)
* **Typography**: Clean geometric grotesque (Inter, Helvetica Neue, SF Pro Display)
* **Profile Avatar**: Minimalist 1080x1080 matte-gold geometric bull silhouette inside an obsidian circular trading ring. Asset stored at `assets/brand/thebullprint_avatar_1080.png`.

---

## 3. Automated Reels Caption Structure (AI & SEO Engine)

Every automated 9:16 Short published as an Instagram Reel utilizes this structure:

1. **Line 1 (Hook Headline)**: Uppercase 1–2 word shock hook + primary financial figure (e.g. `COREWEAVE'S $7.5B DEBT TRAP 🚨`).
2. **Paragraph 2 (AI/SEO Entity Summary)**: 2–3 sentences explicitly naming central banks, institutions, tickers, and macro catalysts for search indexers.
3. **Paragraph 3 (Brand Mission Anchor)**: `Financial freedom for everyone through financial literacy. 💡`
4. **Paragraph 4 (Cross-Platform CTA)**:
   ```text
   📌 Watch the full 12-minute institutional breakdown on YouTube — tap the link in our bio (@thebullprint) or search "{title}" on YouTube (youtu.be/{youtube_video_id}).
   🌐 Portal: thebullprint.com | 📘 Facebook: The Bull Print
   ```
5. **Footer**: `#TheBullPrint #MacroEconomics #FinancialLiteracy #InstitutionalTrading` + 3–4 dynamic entity hashtags.

---

## 4. Automation Architecture

* **Engine**: Cloudflare Worker (`tbp-cloudflare-orchestrator`) + D1 SQLite Ledger (`tbp-production-db`).
* **Cadence**: 30-minute cron sweeps (`*/30 * * * *`). Spaced $\ge 2\text{ hours}$ apart.
* **Quarantine Policy**: Blacklisted videos (e.g. `Z6LEnQyhuvw`) are hard-blocked by D1 (`ig_status = 'QUARANTINED'`) and never published.
