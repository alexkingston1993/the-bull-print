import sys
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from output.options_casino_documentary.chapters_script import SEGMENTS

FRAMES_DIR = BASE_DIR / "output" / "options_casino_documentary" / "frames"
all_frames = sorted([f for f in FRAMES_DIR.glob("*.jpg") if not f.name.startswith("segment_")])

print(f"Total bespoke frames available: {len(all_frames)}")

# Comprehensive semantic keyword profiles for all 36 segments
KEYWORD_PROFILES = {
    1: ["expiry", "zero", "afternoon", "mumbai", "software", "engineer", "frozen", "screen", "vaporized", "call", "option", "worthless", "p&l", "smartphone", "bedroom", "crashing", "90-second", "drops"],
    2: ["1.8", "lakh", "crore", "black", "hole", "sebi", "bombshell", "study", "regulator", "93", "ninety", "three", "percent", "derivatives", "vortex", "notes", "currency", "national", "stock", "exchange", "headquarters", "building", "losing", "nse"],
    3: ["hero", "delusion", "roulette", "wheel", "strike", "prices", "lottery", "scratch", "5000", "cheap", "black", "ash", "dissolving", "pie", "burnt", "tickets", "casino", "table"],
    4: ["title", "monument", "obsidian", "candlestick", "lasers", "casino", "investigation", "zero-day", "monolithic", "red", "laser", "plate", "master"],
    5: ["calendar", "flipping", "expiry", "finnifty", "banknifty", "sensex", "thursday", "friday", "tuesday", "wednesday", "week", "weekly", "labels", "five"],
    6: ["400", "trillion", "volume", "explosion", "globe", "india", "pillar", "skyrocketing", "world", "gdp", "turnover", "planet", "map", "high", "counter", "dwarf", "surpasses", "neon"],
    7: ["leverage", "mrf", "vault", "small", "capital", "lottery", "drawer", "2000", "seduced", "reaching", "buying", "stock_vault", "comparison"],
    8: ["quants", "supercomputers", "server", "racks", "fiber", "chicago", "amsterdam", "mumbai", "wins", "proprietary", "extracting", "desks", "arbitrage", "processing"],
    9: ["theta", "decay", "hourglass", "sand", "bleeding", "time", "clockwork", "certainty", "vault", "rupee", "symbols", "formula", "falling", "chart"],
    10: ["gamma", "parabolic", "electrocardiogram", "heart", "flatline", "monitor", "spike", "10-point", "risk", "curve", "wiped", "crush"],
    11: ["stop-loss", "hunting", "order", "book", "crosshair", "laser", "algo", "flush", "twenty", "rupees", "targeted", "algorithmic", "wave", "skyrocketing", "reveals"],
    12: ["co-location", "millisecond", "latency", "nanoseconds", "dark", "fiber", "4g", "mobile", "buffer", "spinning", "delay", "execution", "speed", "versus", "cables", "blinking", "connection"],
    13: ["asymmetry", "balance", "scale", "feather", "titanium", "cube", "50000", "500", "crore", "margin", "squeeze", "crushing", "deploying", "call", "liquidated"],
    14: ["gambler", "ruin", "mathematical", "probability", "skull", "chalk", "equations", "bankrupt", "100%", "distribution", "forming", "dissolving"],
    15: ["finfluencer", "rented", "ferrari", "supercar", "sunglasses", "influencer", "instagram", "fake", "green", "posing", "street", "parked", "displaying"],
    16: ["inspect", "element", "devtools", "laptop", "code", "editing", "simulator", "paper", "screenshot", "developer", "tag", "span"],
    17: ["course", "sales", "masterclass", "funnel", "dashboard", "ipad", "notifications", "mentorship", "20000", "webinars", "payment", "button", "student", "breakdown"],
    18: ["telegram", "sure", "shot", "jackpot", "subscribers", "pump", "dump", "alert", "arrows", "siphoning", "trap", "receiving"],
    19: ["sebi", "clampdown", "gurus", "raids", "frozen", "bank", "accounts", "itr", "disqualified", "50", "crores", "officers", "serving", "lifestyle", "luxury", "seizes"],
    20: ["dopamine", "addiction", "slot", "machine", "cherries", "brain", "scan", "neurological", "reward", "loop", "spiking", "activity", "cherries"],
    21: ["human", "cost", "office", "desk", "night", "debt", "recovery", "notice", "wedding", "photos", "passbook", "tear", "loans", "alone", "shadows", "kitchen"],
    22: ["pyramid", "house", "wins", "apex", "middle", "foundation", "discount", "brokerages", "exchanges", "golden", "architectural", "representing", "flowing"],
    23: ["brokerage", "churn", "fintech", "boardroom", "profits", "surging", "20", "rupees", "5000", "crores", "windfall", "revenue", "exponential", "pie"],
    24: ["friction", "contract", "note", "scalpel", "peeling", "stt", "gst", "stamp", "duty", "28%", "charges", "invoice", "deductions", "breakdown"],
    25: ["treasury", "government", "stt", "goldmine", "counter", "national", "exchequer", "tenfold", "revenue", "flowing", "upward"],
    26: ["gamified", "confetti", "notifications", "phone", "buttons", "mimic", "gaming", "app", "ui", "taking", "photo", "ledger"],
    27: ["epiphany", "savings", "fixed", "deposits", "productive", "infographic", "map", "households", "threat", "officials", "reviewing", "demographics"],
    28: ["hammer", "7-point", "clampdown", "lot", "size", "15", "lakhs", "bkc", "seal", "bronze", "mandate", "stamping", "regulatory"],
    29: ["recovery", "math", "chalkboard", "90%", "900%", "50%", "100%", "formulas", "grim", "realization", "losses", "accepting", "defeated"],
    30: ["disable", "toggle", "f&o", "settings", "broker", "profile", "gray", "24-hour", "cooling", "off", "disabling", "finger", "deactivating"],
    31: ["umbrella", "hedging", "insurance", "storm", "rain", "lightning", "protecting", "basket", "fire", "policy", "deflecting", "chicago"],
    32: ["compounding", "staircase", "sunrise", "golden", "dawn", "mumbai", "skyline", "index", "funds", "boring", "ascending", "nifty_50", "growth", "sleeping"],
    33: ["sundial", "golden", "marble", "dalal", "street", "bse", "patience", "shadow", "impatient", "time"],
    34: ["mirror", "opposite", "supercomputer", "quantum", "reflections", "trader", "blue", "eyes", "simulation", "running"],
    35: ["sovereignty", "skyscraper", "sunset", "certificates", "prosperous", "booming", "cityscape", "real", "assets", "investor", "holding", "physical"],
    36: ["outro", "bull", "emblem", "titanium", "crimson", "fog", "subscribe", "bell", "truth", "emerging"]
}

# Score each frame against all segments
frame_scores = {}
for f in all_frames:
    fname = f.name.lower()
    fwords = re.findall(r"[a-z0-9]{3,}", fname)
    scores = {}
    for sid in range(1, 37):
        kws = set(KEYWORD_PROFILES[sid])
        s = sum(4 for w in fwords if w in kws)
        for w in fwords:
            for kw in kws:
                if len(w) >= 4 and len(kw) >= 4 and (w in kw or kw in w):
                    s += 1
        scores[sid] = s
    frame_scores[f] = scores

# We want 4 to 5 frames per segment
# Initial assignment: assign each frame to its highest scoring segment
segment_buckets = {sid: [] for sid in range(1, 37)}
unassigned = []

for f in all_frames:
    best_sid = max(frame_scores[f], key=frame_scores[f].get)
    if frame_scores[f][best_sid] > 0:
        segment_buckets[best_sid].append((f, frame_scores[f][best_sid]))
    else:
        unassigned.append(f)

# Balance buckets: every segment must have at least 3, ideal 4-5
for sid in range(1, 37):
    if len(segment_buckets[sid]) < 3:
        # Find closest frames from overpopulated buckets or unassigned
        candidates = []
        for other_sid, flist in segment_buckets.items():
            if len(flist) > 4:
                for f, sc in flist:
                    candidates.append((other_sid, f, frame_scores[f][sid]))
        candidates.sort(key=lambda x: x[2], reverse=True)
        while len(segment_buckets[sid]) < 3 and candidates:
            from_sid, cand_f, cand_sc = candidates.pop(0)
            if len(segment_buckets[from_sid]) > 4:
                # Move
                segment_buckets[from_sid] = [x for x in segment_buckets[from_sid] if x[0] != cand_f]
                segment_buckets[sid].append((cand_f, cand_sc))

final_mapping = {}
for sid in range(1, 37):
    # Sort by score or filename
    files = [x[0].name for x in sorted(segment_buckets[sid], key=lambda x: x[1], reverse=True)]
    final_mapping[sid] = files
    print(f"Segment {sid:02d} ({SEGMENTS[sid-1]['title'][:32]}): {len(files)} frames -> {files[:2]}")

out_json = BASE_DIR / "output" / "options_casino_documentary" / "segment_frame_mapping.json"
out_json.write_text(json.dumps(final_mapping, indent=2))
print(f"\nSaved mapping to {out_json}")
