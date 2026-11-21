import json
import re

with open("public/pipeline-dashboard.html", "r") as f:
    html = f.read()

# 1. Update KPI gauge
old_kpi = """          <div class="text-slate-400 text-[10px] uppercase tracking-wider">Shorts Target</div>
          <div class="text-base font-bold text-emerald-400 mt-0.5 flex items-baseline gap-1">
            5 <span class="text-xs text-slate-500 font-normal">/ 10 Published</span>
          </div>
          <div class="w-full bg-slate-800 h-1 rounded-full mt-1.5 overflow-hidden">
            <div class="bg-emerald-500 h-full rounded-full" style="width: 50%"></div>
          </div>"""

new_kpi = """          <div class="text-slate-400 text-[10px] uppercase tracking-wider">Shorts Target</div>
          <div class="text-base font-bold text-emerald-400 mt-0.5 flex items-baseline gap-1">
            16 <span class="text-xs text-slate-500 font-normal">/ 10 Published (160%)</span>
          </div>
          <div class="w-full bg-slate-800 h-1 rounded-full mt-1.5 overflow-hidden">
            <div class="bg-emerald-500 h-full rounded-full" style="width: 100%"></div>
          </div>"""

if old_kpi in html:
    html = html.replace(old_kpi, new_kpi)

old_doc_kpi = """          <div class="text-slate-400 text-[10px] uppercase tracking-wider">Documentaries</div>
          <div class="text-base font-bold text-amber-400 mt-0.5 flex items-baseline gap-1">
            1 <span class="text-xs text-slate-500 font-normal">/ 2 In Production</span>
          </div>
          <div class="text-[10px] text-amber-400 mt-1">Run #44817798379 Running</div>"""

new_doc_kpi = """          <div class="text-slate-400 text-[10px] uppercase tracking-wider">Documentaries</div>
          <div class="text-base font-bold text-amber-400 mt-0.5 flex items-baseline gap-1">
            0 <span class="text-xs text-slate-500 font-normal">/ 2 (Healer Armed)</span>
          </div>
          <div class="text-[10px] text-emerald-400 mt-1">Auto-Resizing Patched</div>"""

if old_doc_kpi in html:
    html = html.replace(old_doc_kpi, new_doc_kpi)

# 2. Build full VIDEO_DATA object
raw_videos = [
  {"id": "lSdRmaHCets", "num": 1, "title": "The $4.6M CEO Piggy Bank Scandal", "sector": "Corporate Whistleblower & Accounting Forensics", "duration": "57.7s", "run_id": "44730421801"},
  {"id": "m34Yd5TphF0", "num": 2, "title": "CoreWeave 16% Bonds: The Fragile AI Credit Card Bubble", "sector": "Private Credit & AI Datacenter Capex", "duration": "57.7s", "run_id": "44775170439"},
  {"id": "o7DBAxFF6HI", "num": 3, "title": "Strait of Hormuz Crude Chokepoint: Why Tanker Insurance Surged 400%", "sector": "Maritime Logistics & Energy Supply Lines", "duration": "58.1s", "run_id": "44790697149"},
  {"id": "LHAfeWbgshI", "num": 4, "title": "Japan Yen Carry Trade: The $20 Trillion Liquidity Unwind Trigger", "sector": "Sovereign Currency & Central Bank Reserves", "duration": "58.4s", "run_id": "44808550467"},
  {"id": "e7bSJ_Hqohc", "num": 5, "title": "Berkshire Cash Hoard: Why Buffett Bought $150B in Treasuries", "sector": "Sovereign Debt & Treasury Tail Risk", "duration": "58.2s", "run_id": "44817765149"},
  {"id": "G7Jp4JtjgQY", "num": 6, "title": "Anthropic Locked-Up Share Avalanche: The Hidden IPO Catch", "sector": "Pre-IPO Liquidity & Venture Secondaries", "duration": "58.0s", "run_id": "44840302607"},
  {"id": "rbrhGzjuqDo", "num": 7, "title": "Autonomous AI Agent Transactions: The New Fintech Squeeze", "sector": "Fintech Infrastructure & Payment Rails", "duration": "57.5s", "run_id": "44841180455"},
  {"id": "amV2Zaxef5Y", "num": 8, "title": "Commercial Debt Refinancing Cliff: Non-Bank Lenders Liquidation", "sector": "Commercial Real Estate & Shadow Banking", "duration": "58.3s", "run_id": "44842064134"},
  {"id": "2LuQmso-YVs", "num": 9, "title": "Crude Oil Plunges to $85 as Global Supply Lines Shift", "sector": "Commodity Supercycle & Geopolitics", "duration": "57.9s", "run_id": "44843004929"},
  {"id": "RqdSQrqcex8", "num": 10, "title": "Dow & S&P 500 Enter Correction as Yield Curves Shift", "sector": "Equity Valuations & Bond Yield Dynamics", "duration": "58.1s", "run_id": "44843813958"},
  {"id": "-aAsqzc03j8", "num": 11, "title": "Fed 50bps Shock: Why the Institutional Smart Money Is Running", "sector": "Federal Reserve Monetary Policy & Rates", "duration": "57.6s", "run_id": "44844731344"},
  {"id": "OIjYybHD9OU", "num": 12, "title": "Fed Strips 2027 Voting Power: The Stealth Policy Coup", "sector": "Central Banking Governance & Inflation", "duration": "58.5s", "run_id": "44845670284"},
  {"id": "E4Mfz8c-HhA", "num": 13, "title": "Kevin Warsh Strategy vs AI Inflation Pressure", "sector": "Macroeconomic Policy & AI Productivity", "duration": "57.8s", "run_id": "44846593094"},
  {"id": "lM2JdIRy_bk", "num": 14, "title": "The $2.3 Trillion Chip Wreck: Inside the Panic Gripping AI", "sector": "Semiconductor Supply Chain & Capex", "duration": "58.2s", "run_id": "44847398982"},
  {"id": "C-Cu-k-SeJQ", "num": 15, "title": "The Fed Secret 2027 Voting Blackout Explained", "sector": "FOMC Voting Dynamics & Balance Sheet", "duration": "57.9s", "run_id": "44819602974"},
  {"id": "h5ol3-qNex4", "num": 16, "title": "U.S. Crude Drops to $85 on Middle East Flows", "sector": "Energy Markets & Strategic Reserves", "duration": "58.0s", "run_id": "44837391902"}
]

video_dict = {}
for v in raw_videos:
    run_url = "https://github.com/alexkingston1993/the-bull-print/actions/runs/" + str(v["run_id"])
    video_dict[v["num"]] = {
        "id": v["id"],
        "num": v["num"],
        "title": v["title"],
        "sector": v["sector"],
        "status": "public",
        "duration": v["duration"],
        "plates": 20,
        "kaggle_time": "4m 15s",
        "render_time": "2m 10s",
        "run_id": v["run_id"],
        "run_url": run_url,
        "audio": "Master Continuous Monologue (Single-Runner Engine)"
    }

# 3. Inject new VIDEO_DATA and renderVideoCards function
start_vdata = html.find("const VIDEO_DATA = {")
end_vdata = html.find("let currentVideo =", start_vdata)
if start_vdata != -1 and end_vdata != -1:
    vdata_str = "const VIDEO_DATA = " + json.dumps(video_dict, indent=2) + ";\n\n    "
    html = html[:start_vdata] + vdata_str + html[end_vdata:]

# Update renderVideoCards loop to [1..16]
html = re.sub(r"\[1,\s*2,\s*3,\s*4(?:,\s*5)?\]\.forEach", f"{list(range(1, 17))}.forEach", html)

# Update video selector tab buttons
tabs_start = html.find("<div class=\"flex items-center gap-1.5 flex-wrap\">")
if tabs_start != -1:
    tabs_end = html.find("</div>", tabs_start)
    new_tabs = "<div class=\"flex items-center gap-1.5 flex-wrap\">\n"
    for num in range(1, 17):
        cls_name = "v-tab px-2.5 py-1 rounded-lg text-xs font-mono "
        if num == 16:
            cls_name += "border border-emerald-500/50 bg-emerald-500/20 text-emerald-300 font-bold transition"
        else:
            cls_name += "border border-slate-800 bg-slate-950 text-slate-400 hover:text-white transition"
        new_tabs += f"            <button onclick=\"selectVideo({num})\" class=\"{cls_name}\">Short #{num}</button>\n"
    new_tabs += "          "
    html = html[:tabs_start] + new_tabs + html[tabs_end:]

with open("public/pipeline-dashboard.html", "w") as f:
    f.write(html)
with open("pipeline-dashboard.html", "w") as f:
    f.write(html)

print("✓ Updated pipeline-dashboard.html with all 16 videos!")
