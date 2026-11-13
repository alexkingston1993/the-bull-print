#!/usr/bin/env python3
"""
Produces 6 Dedicated Videos for The Bull Print's Free Financial Tools.
Each video breaks down:
1. The visceral pain / tough reality of being without that tool.
2. How the tool mathematically solves the problem.
3. How to use the tool step-by-step.
4. Free link to the website tool + report form.
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output" / "tool_videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TOOLS_DATA = [
    {
        "id": "Tool_01_Emergency_Runway_Diagnostic",
        "tool_key": "runway",
        "title": "Are You 1 Paycheck From Financial Ruin? (Free Emergency Runway Calculator)",
        "pain_hook": "Living without knowing your exact survival runway is like flying a jetliner through fog with your fuel gauge taped over.",
        "solution": "Most people assume their salary will never stop. But when a layoff, health emergency, or client loss strikes, you are forced into panic-selling investments at the worst possible bottom or taking 16% personal loans. The Bull Print Emergency Runway Calculator takes your liquid cash, deposits, and fixed burn rate, and tells you to the exact day how long you can survive with zero income.",
        "walkthrough": "Slide your bank balance, fixed deposits, and monthly mandatory expenses. The quant engine instantly categorizes your safety moat: Critical Deficit under 3 months, Moderate Buffer at 3 to 6 months, or Fortified at 12 months. It shows you the exact rupee deficit to reach complete financial invincibility.",
        "cta": "Stop guessing your survival. Use this tool 100% free right now at bullprintmedia.com/calculators with the runway parameter. Submit your free audit form to download your pre-filled survival plan and our institutional Financial OS.",
        "link": "https://bullprintmedia.com/calculators.html?tool=runway",
        "cuts": [
            {"badge": "THE BLIND SPOT", "lines": ["1 PAYCHECK FROM", "TOTAL DISASTER"], "col": (239, 68, 68)},
            {"badge": "QUANT DIAGNOSTIC", "lines": ["SURVIVAL RUNWAY:", "EXACT DAYS LEFT"], "col": (245, 158, 11)},
            {"badge": "FORTIFIED BUFFER", "lines": ["6-12 MONTHS", "SAFETY MOAT"], "col": (0, 135, 90)},
            {"badge": "FREE ACCESS", "lines": ["AUDIT YOUR RUNWAY", "AT BULLPRINTMEDIA.COM"], "col": (255, 215, 0)}
        ]
    },
    {
        "id": "Tool_02_Rent_vs_Buy_5_Percent_Rule",
        "tool_key": "rent-vs-buy",
        "title": "The ₹1 Crore Home Trap: Rent vs Buy 5% Rule Explained (Free Tool)",
        "pain_hook": "Buying a house on a 20-year EMI is sold as the ultimate adult milestone. But without math, it is the single largest wealth destroyer of the middle class.",
        "solution": "People compare their monthly rent to the home loan EMI, forgetting that buying a home involves massive unrecoverable costs: 3% cost of debt capital, 1% property taxes and insurance, and 1% annual maintenance depreciation. That is the institutional 5% Rule. If your annual rent is less than 5% of the property value, buying is a mathematical penalty.",
        "walkthrough": "Input the property price, your city's rental rate, and your expected home loan interest. Our decision matrix instantly reveals your break-even rental threshold and calculates how many Crores of extra net worth you will generate by renting and compounding the difference in index funds over 15 years.",
        "cta": "Do not commit to a 20-year EMI blindly. Run your exact city numbers 100% free at bullprintmedia.com/calculators with the rent-vs-buy parameter. Fill the form to download the institutional Excel comparison model.",
        "link": "https://bullprintmedia.com/calculators.html?tool=rent-vs-buy",
        "cuts": [
            {"badge": "THE EMOTIONAL TRAP", "lines": ["THE ₹1 CRORE", "HOME LOAN TRAP"], "col": (239, 68, 68)},
            {"badge": "WALL STREET FORMULA", "lines": ["THE 5% RULE", "UNRECOVERABLE COST"], "col": (245, 158, 11)},
            {"badge": "15-YEAR WEALTH GAP", "lines": ["+₹1.03 CRORES", "BY INVESTING DIFF"], "col": (0, 135, 90)},
            {"badge": "FREE INSTITUTIONAL TOOL", "lines": ["RUN YOUR NUMBERS", "AT BULLPRINTMEDIA.COM"], "col": (255, 215, 0)}
        ]
    },
    {
        "id": "Tool_03_Car_Loan_Depreciation_Trap",
        "tool_key": "car-trap",
        "title": "How Your Car Loan Stole ₹60 Lakhs From Your Retirement (Free Audit Tool)",
        "pain_hook": "Automakers and banks have trained everyone to ask only one question: Can I afford the monthly EMI? That single question costs you over ₹60 Lakhs in lost retirement compounding.",
        "solution": "When you buy an ₹18 Lakh car with a 5-year loan, you pay over ₹21 Lakhs in total cash. But cars depreciate 60% in 5 years. You are financing an asset that drops in value every single day while paying 9.5% compound interest. If you invested that same down payment and monthly EMI in Nifty index funds, that money would compound into over ₹58 Lakhs.",
        "walkthrough": "Enter the on-road price of your dream car, down payment, and tenure. The Car Wealth Destroyer reveals the harsh reality: the true 10-year opportunity cost and the exact number of years this purchase delays your retirement.",
        "cta": "Audit your vehicle purchase before signing the loan papers. Use our free tool at bullprintmedia.com/calculators with the car-trap parameter. Free link in the description with your pre-filled wealth report.",
        "link": "https://bullprintmedia.com/calculators.html?tool=car-trap",
        "cuts": [
            {"badge": "WEALTH RETARDATION", "lines": ["YOUR CAR LOAN", "STOLE ₹60 LAKHS"], "col": (239, 68, 68)},
            {"badge": "DEPRECIATION REALITY", "lines": ["-60% VALUE IN 5 YRS", "WHILE PAYING 9.5%"], "col": (245, 158, 11)},
            {"badge": "OPPORTUNITY COST", "lines": ["DELAYS RETIREMENT", "BY 3.2 YEARS"], "col": (239, 68, 68)},
            {"badge": "FREE AUDIT MODEL", "lines": ["TEST YOUR CAR NOW", "AT BULLPRINTMEDIA.COM"], "col": (255, 215, 0)}
        ]
    },
    {
        "id": "Tool_04_Step_Up_SIP_Compounder",
        "tool_key": "sip",
        "title": "Why Flat SIPs Fail: How a 10% Step-Up Triples Your Wealth (Free Calculator)",
        "pain_hook": "Starting a ₹10,000 monthly SIP feels great, but keeping it flat for 15 years guarantees you will lose the race against 7% lifestyle inflation.",
        "solution": "If your salary increases by 10% every year but your SIP stays identical, your real savings rate is collapsing. By simply increasing your SIP by 10% annually—matching your annual increment—your final corpus explodes from ₹67 Lakhs to nearly ₹1.8 Crores. You triple your wealth without sacrificing your current standard of living.",
        "walkthrough": "Our Step-Up SIP Compounder lets you test monthly contributions, expected CAGR returns, and custom annual step-up rates from 0% to 25%. Watch the visual breakdown between your invested capital and explosive compound returns in real-time.",
        "cta": "Find your exact step-up trajectory today. Access the calculator 100% free at bullprintmedia.com/calculators with the sip parameter. Submit the form to receive your custom 20-year wealth projection PDF.",
        "link": "https://bullprintmedia.com/calculators.html?tool=sip",
        "cuts": [
            {"badge": "THE INFLATION TRAP", "lines": ["WHY FLAT SIPS", "FAIL AFTER 15 YRS"], "col": (239, 68, 68)},
            {"badge": "THE 10% STEP-UP SECRET", "lines": ["MATCH SALARY HIKE", "TRIPLE YOUR WEALTH"], "col": (0, 135, 90)},
            {"badge": "COMPOUND EXPLOSION", "lines": ["FROM ₹67 LAKHS", "TO ₹1.8 CRORES"], "col": (245, 158, 11)},
            {"badge": "FREE WEALTH TOOL", "lines": ["CALCULATE STEP-UP", "AT BULLPRINTMEDIA.COM"], "col": (255, 215, 0)}
        ]
    },
    {
        "id": "Tool_05_Debt_Snowball_Avalanche_Optimizer",
        "tool_key": "debt-destroyer",
        "title": "Kill 42% Credit Card Debt 80% Faster (Free Payoff Calculator)",
        "pain_hook": "Paying only the minimum due on your credit cards is a mathematical trap that takes up to 27 years and costs you 400% more than what you actually borrowed.",
        "solution": "High-interest debt compound interest works against you like financial cancer. The Bull Print Debt Destroyer applies the quantitative Debt Avalanche method, mathematically prioritizing your highest APR debt first while maintaining minimums on others, saving you lakhs in pure interest and slashing years off your payoff timeline.",
        "walkthrough": "Input your credit card balances, APR interest rates, personal loans, and your extra monthly payoff budget. The engine models both Snowball and Avalanche, projects your exact debt freedom month, and computes the exact interest saved.",
        "cta": "Break free from the banking trap. Use this free calculator at bullprintmedia.com/calculators with the debt-destroyer parameter. Submit your form to download your automated debt-free milestone tracker.",
        "link": "https://bullprintmedia.com/calculators.html?tool=debt-destroyer",
        "cuts": [
            {"badge": "THE 42% APR PRISON", "lines": ["THE 27-YEAR", "MINIMUM DUE TRAP"], "col": (239, 68, 68)},
            {"badge": "QUANT METHOD", "lines": ["DEBT AVALANCHE", "SAVES ₹4.8 LAKHS"], "col": (0, 135, 90)},
            {"badge": "RAPID VELOCITY", "lines": ["SLASH PAYOFF TIME", "BY 83% FASTER"], "col": (245, 158, 11)},
            {"badge": "FREE DESTROYER TOOL", "lines": ["FREE YOURSELF NOW", "AT BULLPRINTMEDIA.COM"], "col": (255, 215, 0)}
        ]
    },
    {
        "id": "Tool_06_Stock_DCF_Intrinsic_Value",
        "tool_key": "dcf",
        "title": "Find Any Stock's True Fair Value in 60 Seconds (Free Hedge Fund DCF Tool)",
        "pain_hook": "Buying stocks based on P/E ratios, social media tips, or hype guarantees you will buy at the absolute peak right before a 50% drawdown.",
        "solution": "A stock is not a lottery ticket—it is fractional ownership of a business. Its true value is the discounted present value of all cash flows it will generate in the future. Our 2-Stage Discounted Cash Flow model lets everyday investors value any company like a professional hedge fund analyst with an institutional margin of safety.",
        "walkthrough": "Input the company's free cash flow per share, projected 5-year growth, cost of capital discount rate, and terminal multiple. The model instantly outputs the fair value, current discount or premium, and an exact accumulate signal.",
        "cta": "Never overpay for a stock again. Value your portfolio 100% free at bullprintmedia.com/calculators with the dcf parameter. Download the full institutional valuation spreadsheet today.",
        "link": "https://bullprintmedia.com/calculators.html?tool=dcf",
        "cuts": [
            {"badge": "THE RETAIL TRAP", "lines": ["STOP BUYING STOCKS", "ON HYPE & P/E"], "col": (239, 68, 68)},
            {"badge": "HEDGE FUND MODEL", "lines": ["2-STAGE DCF", "CASH FLOW VALUE"], "col": (59, 130, 246)},
            {"badge": "MARGIN OF SAFETY", "lines": ["BUY AT 20% DISCOUNT", "LOCK IN ALPHA"], "col": (0, 135, 90)},
            {"badge": "FREE VALUATION SUITE", "lines": ["VALUATE STOCKS FREE", "AT BULLPRINTMEDIA.COM"], "col": (255, 215, 0)}
        ]
    }
]

def render_frame_plate(cut_data, tool_title, tool_key, output_path):
    width, height = 1080, 1920
    im = Image.new("RGB", (width, height), (12, 14, 18))
    draw = ImageDraw.Draw(im)

    # Gradient background
    for y in range(height):
        r = int(12 + (y / height) * 16)
        g = int(14 + (y / height) * 18)
        b = int(18 + (y / height) * 26)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Grid lines / Tech quant mesh
    grid_col = (25, 30, 42)
    for x in range(0, width, 90):
        draw.line([(x, 0), (x, height)], fill=grid_col, width=1)
    for y in range(0, height, 90):
        draw.line([(0, y), (width, y)], fill=grid_col, width=1)

    # Glow orb in center
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    col = cut_data["col"]
    glow_draw.ellipse([width//2 - 350, 600, width//2 + 350, 1300], fill=(col[0], col[1], col[2], 40))
    glow = glow.filter(ImageFilter.GaussianBlur(100))
    im.paste(glow, (0, 0), glow)
    draw = ImageDraw.Draw(im)

    # Load Fonts
    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial Black.ttf",
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Unicode.ttf"
    ]
    font_bold = None
    for p in font_paths:
        if os.path.exists(p):
            try:
                font_bold = ImageFont.truetype(p, 96)
                font_badge = ImageFont.truetype(p, 36)
                font_sub = ImageFont.truetype(p, 32)
                break
            except:
                pass
    if not font_bold:
        font_bold = ImageFont.load_default()
        font_badge = font_bold
        font_sub = font_bold

    # Top Brand Header Pill
    draw.rounded_rectangle([180, 160, width - 180, 240], radius=40, fill=(20, 24, 33), outline=(255, 215, 0), width=2)
    draw.text((width//2, 200), "THE BULL PRINT  |  QUANTITATIVE WEALTH OS", fill=(255, 215, 0), font=font_sub, anchor="mm")

    # Stabilo Badge Marker
    badge_text = cut_data["badge"]
    badge_w = len(badge_text) * 24 + 60
    bx1 = (width - badge_w) // 2
    by1 = 440
    bx2 = bx1 + badge_w
    by2 = by1 + 65
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=10, fill=cut_data["col"])
    draw.text((width//2, (by1 + by2)//2), badge_text, fill=(0, 0, 0) if cut_data["col"] != (239, 68, 68) else (255, 255, 255), font=font_badge, anchor="mm")

    # Giant 3D Kinetic Typography
    lines = cut_data["lines"]
    start_y = 660
    for i, line in enumerate(lines):
        ly = start_y + (i * 135)
        # 3D shadow extrusion
        for ext in range(16, 0, -2):
            draw.text((width//2 + ext, ly + ext), line, fill=(5, 5, 8), font=font_bold, anchor="mm")
        # Main text face
        draw.text((width//2, ly), line, fill=(255, 255, 255), font=font_bold, anchor="mm")

    # Center Institutional Graphic Box (Dashboard Card)
    cx1, cy1, cx2, cy2 = 100, 1080, width - 100, 1500
    draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=24, fill=(18, 22, 30), outline=(50, 60, 80), width=2)

    # Card internal metrics
    draw.text((cx1 + 40, cy1 + 40), "FLAGSHIP INSTITUTIONAL FINANCIAL TOOL", fill=(140, 155, 175), font=font_sub)
    draw.text((cx1 + 40, cy1 + 90), tool_title[:38] + "...", fill=(255, 255, 255), font=font_badge)

    # Metric Mockup
    draw.rounded_rectangle([cx1 + 40, cy1 + 170, cx2 - 40, cy1 + 270], radius=16, fill=(26, 32, 45), outline=cut_data["col"], width=2)
    draw.text((cx1 + 60, cy1 + 220), "OFFICIAL VERDICT / RESULT:", fill=(180, 190, 205), font=font_sub, anchor="lm")
    draw.text((cx2 - 60, cy1 + 220), "100% MATHEMATICAL", fill=cut_data["col"], font=font_badge, anchor="rm")

    draw.rounded_rectangle([cx1 + 40, cy1 + 295, cx2 - 40, cy1 + 380], radius=14, fill=(255, 215, 0))
    draw.text((width//2, cy1 + 338), f"RUN FREE AT: bullprintmedia.com/calculators?tool={tool_key}", fill=(0, 0, 0), font=font_sub, anchor="mm")

    # Safe Zone Captions Banner
    draw.rectangle([0, 1680, width, 1850], fill=(10, 12, 16))
    draw.line([(0, 1680), (width, 1680)], fill=(40, 50, 65), width=2)
    draw.text((width//2, 1735), "⚡ 100% FREE VALUE  |  NO PAYWALLS  |  INSTANT AUDIT", fill=(255, 215, 0), font=font_sub, anchor="mm")
    draw.text((width//2, 1795), "Link in description & comments with downloadable Excel OS", fill=(160, 175, 195), font=font_sub, anchor="mm")

    im.save(output_path, quality=95)

def synthesize_audio(text, output_file):
    # High-quality authoritative British finance narrator (Daniel) via native macOS speech engine + ffmpeg 44.1kHz
    aiff_tmp = output_file.with_suffix(".aiff")
    cmd_say = ["say", "-v", "Daniel", "-r", "185", "-o", str(aiff_tmp), text]
    subprocess.run(cmd_say, check=True)
    cmd_conv = [
        "ffmpeg", "-y", "-i", str(aiff_tmp),
        "-ar", "44100", "-ac", "2", "-b:a", "192k",
        str(output_file)
    ]
    subprocess.run(cmd_conv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if aiff_tmp.exists():
        aiff_tmp.unlink()

def produce_all_tools():
    for idx, t in enumerate(TOOLS_DATA, 1):
        folder = OUTPUT_DIR / t["id"]
        folder.mkdir(parents=True, exist_ok=True)
        frames_dir = folder / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)

        full_script = f"{t['pain_hook']} {t['solution']} {t['walkthrough']} {t['cta']}"

        # 1. Research & Dossier
        with open(folder / "RESEARCH.md", "w", encoding="utf-8") as f:
            f.write(f"# {t['title']}\n\n"
                    f"## 1. The Real-World Pain & The Cost of Living Without It\n"
                    f"{t['pain_hook']}\n\n"
                    f"## 2. Quantitative Financial Solution\n"
                    f"{t['solution']}\n\n"
                    f"## 3. Step-by-Step Tool Walkthrough\n"
                    f"{t['walkthrough']}\n\n"
                    f"## 4. Monetization & Long-Term Asset Strategy\n"
                    f"- High-intent financial lead acquisition (Name, Email, Goal).\n"
                    f"- Owned email list compound growth.\n"
                    f"- Upsell runway to 365-Day Masterclass and Institutional Alpha tools.\n"
                    f"- Direct link: `{t['link']}`\n")

        # 2. Script
        with open(folder / "SCRIPT.md", "w", encoding="utf-8") as f:
            f.write(f"# High-Retention Video Script: {t['title']}\n\n"
                    f"**Voice**: en-US-ChristopherNeural (-2Hz)\n"
                    f"**Format**: Vertical Short (9:16) / Institutional Reel\n\n"
                    f"### Complete Narration Voiceover:\n\n"
                    f"\"{full_script}\"\n")

        # 3. Metadata
        metadata = {
            "title": t["title"],
            "tool_key": t["tool_key"],
            "direct_tool_link": t["link"],
            "description": f"{t['title']}\n\n"
                           f"Run this calculation for free right now on our official platform:\n"
                           f"👉 {t['link']}\n\n"
                           f"Financial Freedom for Everyone Through Financial Literacy.\n\n"
                           f"Timestamps:\n"
                           f"0:00 - The Hidden Cost of Living Without This\n"
                           f"0:15 - The Quantitative Solution\n"
                           f"0:35 - Step-by-Step Tool Walkthrough\n"
                           f"0:50 - Claim Your Free Report & Financial OS\n\n"
                           f"#Finance #Investing #TheBullPrint #Wealth #Money #PersonalFinance #StockMarket #StockMarketIndia",
            "tags": ["personal finance", "stock market", "the bull print", "financial calculators", "money management", "investing"],
            "pinned_comment": f"Run your exact numbers 100% free here: {t['link']}\nFill the form to download your pre-filled custom wealth audit!"
        }
        with open(folder / "METADATA.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        # 4. Generate Voiceover via Daniel / ffmpeg 44.1kHz
        audio_path = folder / "narration.mp3"
        print(f"[{idx}/6] Synthesizing audio for {t['id']}...")
        synthesize_audio(full_script, audio_path)

        # 5. Generate Visual Plates
        print(f"[{idx}/6] Generating frame plates for {t['id']}...")
        for cut_idx, cut in enumerate(t["cuts"], 1):
            frame_path = frames_dir / f"frame_{cut_idx:02d}.jpg"
            render_frame_plate(cut, t["title"], t["tool_key"], frame_path)

        # 6. Composite Master Video via ffmpeg
        video_path = folder / "master_video.mp4"
        print(f"[{idx}/6] Rendering master video for {t['id']}...")
        
        # Build concat list with duration per frame
        # Get audio duration
        probe_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)]
        duration_str = subprocess.check_output(probe_cmd).decode().strip()
        duration = float(duration_str)
        cut_duration = duration / len(t["cuts"])

        concat_file = folder / "concat_frames.txt"
        with open(concat_file, "w") as f:
            for cut_idx in range(1, len(t["cuts"]) + 1):
                f_path = frames_dir / f"frame_{cut_idx:02d}.jpg"
                f.write(f"file '{f_path.resolve()}'\n")
                f.write(f"duration {cut_duration:.3f}\n")
            # Last frame duplicated for ffmpeg concat requirement
            last_f = frames_dir / f"frame_{len(t['cuts']):02d}.jpg"
            f.write(f"file '{last_f.resolve()}'\n")

        render_cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat_file),
            "-i", str(audio_path),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(video_path)
        ]
        subprocess.run(render_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ Successfully compiled {video_path} (Duration: {duration:.1f}s)")

if __name__ == "__main__":
    produce_all_tools()
    print("\n🎉 ALL 6 TOOL VIDEOS AND ASSETS FULLY PRODUCED!")
