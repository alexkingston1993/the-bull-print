#!/usr/bin/env python3
"""
The Bull Print: Batch Renderer for All 6 Free Tool Viral Shorts
Architecture: 1080x1920 9:16 Vertical, 36.0s (12 cuts @ 3.0s),
35mm clean plates, camera dolly, 3D kinetic typography, Stabilo badges,
mobile word captions at Y=1480, ChristopherNeural (-2Hz), ducked ambient BGM (-18 LUFS).
"""

import math
import os
import shutil
import subprocess
import asyncio
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = Path(__file__).resolve().parent.parent
BRAIN_DIR = Path("/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364")
BGM_POOL = BASE_DIR / "assets" / "audio" / "bgm_pool" / "dark_investigative" / "bed_01_subterranean_pulse.wav"
OUTPUT_DIR = BASE_DIR / "output" / "tool_videos"
FONT_IMPACT = "/System/Library/Fonts/Supplemental/Impact.ttf"

TOOLS_SPECS = [
    # Tool 02: Rent vs Buy 5% Rule Matrix
    {
        "id": "Tool_02_Rent_vs_Buy_5_Percent_Rule",
        "tool_key": "rent-vs-buy",
        "script": [
            "Buying a house on a twenty-year loan is sold as the ultimate adult milestone.",
            "Without math, it is the single largest wealth destroyer of the middle class.",
            "People compare monthly rent to the EMI, ignoring massive unrecoverable costs.",
            "Three percent cost of debt capital, one percent maintenance, and one percent taxes.",
            "That is the Wall Street five percent rule.",
            "If your annual rent is less than five percent of property value, buying is a financial penalty.",
            "Our decision matrix calculates your exact city numbers.",
            "Renting and investing the difference into index funds compounds exponentially.",
            "Over fifteen years, that difference creates over one crore in extra net worth.",
            "Do not sign a twenty-year home loan blindly.",
            "Run your numbers one hundred percent free at bullprintmedia.com.",
            "Claim your institutional comparison report today."
        ],
        "cuts": [
            {"id": 1, "lines": ["THE ₹1 CRORE", "HOME TRAP"], "badge": "EMOTIONAL MILESTONE", "badge_col": (239, 68, 68), "t_col": (245, 25, 55), "b_col": (255, 30, 60), "plate": "12min_doc_plate_05.jpg"},
            {"id": 2, "lines": ["20-YEAR EMI", "PRISON"], "badge": "WEALTH DESTROYER", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "12min_doc_plate_06.jpg"},
            {"id": 3, "lines": ["UNRECOVERABLE", "COSTS EXPOSED"], "badge": "THE 5% RULE", "badge_col": (245, 158, 11), "t_col": (245, 158, 11), "b_col": (255, 160, 20), "plate": "12min_doc_plate_07.jpg"},
            {"id": 4, "lines": ["3% COST OF", "DEBT CAPITAL"], "badge": "MORTGAGE DRAIN", "badge_col": (239, 68, 68), "t_col": (245, 25, 55), "b_col": (255, 30, 60), "plate": "12min_doc_plate_08.jpg"},
            {"id": 5, "lines": ["1% REPAIR +", "1% PROPERTY TAX"], "badge": "HIDDEN FEES", "badge_col": (245, 158, 11), "t_col": (245, 158, 11), "b_col": (255, 160, 20), "plate": "12min_doc_plate_09.jpg"},
            {"id": 6, "lines": ["ANNUAL RENT", "UNDER 5%?"], "badge": "RENTING WINS", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_10.jpg"},
            {"id": 7, "lines": ["INVEST THE", "DIFFERENCE"], "badge": "INDEX COMPOUNDING", "badge_col": (0, 229, 255), "t_col": (0, 229, 255), "b_col": (0, 200, 240), "plate": "12min_doc_plate_11.jpg"},
            {"id": 8, "lines": ["+₹1.03 CRORES", "WEALTH GAP"], "badge": "15-YEAR WEALTH ALPHA", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "12min_doc_plate_12.jpg"},
            {"id": 9, "lines": ["DO NOT BUY", "BLINDLY"], "badge": "RATIONAL INVESTING", "badge_col": (239, 68, 68), "t_col": (245, 25, 55), "b_col": (255, 30, 60), "plate": "clean_bg_cut01_1794022641757.jpg"},
            {"id": 10, "lines": ["RENT VS BUY", "MATRIX OS"], "badge": "QUANT ALGORITHM", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "clean_bg_cut02_1794027147675.jpg"},
            {"id": 11, "lines": ["100% FREE", "BULLPRINTMEDIA.COM"], "badge": "NO PAYWALLS", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "clean_bg_cut03_1794027172678.jpg"},
            {"id": 12, "lines": ["CLAIM YOUR", "EXCEL REPORT"], "badge": "LINK IN BIO", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "bull_print_banner_plate_1794211800384.jpg"}
        ],
        "captions": [
            (0, 3, ["Buying", "a", "home", "on", "loan,"]),
            (3, 6, ["Is", "the", "biggest", "wealth", "destroyer."]),
            (6, 9, ["Ignoring", "massive", "unrecoverable", "costs."]),
            (9, 12, ["3%", "interest,", "1%", "tax,", "1%", "repairs."]),
            (12, 15, ["That", "is", "the", "5%", "Rule."]),
            (15, 18, ["If", "rent", "is", "under", "5%,", "renting", "wins."]),
            (18, 21, ["Our", "matrix", "calculates", "your", "city."]),
            (21, 24, ["Renting", "and", "investing", "the", "gap,"]),
            (24, 27, ["Creates", "+₹1.03", "Crores", "extra", "net", "worth."]),
            (27, 30, ["Never", "buy", "a", "home", "blindly."]),
            (30, 33, ["Use", "this", "free", "at", "bullprintmedia.com."]),
            (33, 36, ["Download", "your", "free", "report", "now."])
        ]
    },
    # Tool 03: Car Loan Depreciation Trap
    {
        "id": "Tool_03_Car_Loan_Depreciation_Trap",
        "tool_key": "car-trap",
        "script": [
            "Your car loan is secretly stealing sixty lakhs from your retirement.",
            "Banks train everyone to ask only one question: Can I afford the EMI?",
            "When you buy an eighteen lakh car, you pay over twenty-one lakhs with interest.",
            "Cars lose sixty percent of their value within five years.",
            "You are financing a depreciating asset at nine point five percent compound interest.",
            "If that exact down payment and monthly EMI were invested into Nifty index funds,",
            "That capital compounds into over fifty-eight lakhs of pure net worth.",
            "Every luxury car purchase delays your financial freedom by over three years.",
            "Before signing dealership loan documents, audit the true opportunity cost.",
            "The Car Wealth Destroyer reveals the exact retirement delay in seconds.",
            "Audit your car one hundred percent free at bullprintmedia.com.",
            "Get your free wealth audit report today."
        ],
        "cuts": [
            {"id": 1, "lines": ["YOUR CAR LOAN", "STOLE ₹60 LAKHS"], "badge": "RETIREMENT THEFT", "badge_col": (239, 68, 68), "t_col": (245, 25, 55), "b_col": (255, 30, 60), "plate": "12min_doc_plate_01.jpg"},
            {"id": 2, "lines": ["CAN I AFFORD", "THE MONTHLY EMI?"], "badge": "THE FATAL QUESTION", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "12min_doc_plate_02.jpg"},
            {"id": 3, "lines": ["₹18 LAKH CAR", "₹21 LAKH CASH"], "badge": "INTEREST DRAIN", "badge_col": (245, 158, 11), "t_col": (245, 158, 11), "b_col": (255, 160, 20), "plate": "12min_doc_plate_03.jpg"},
            {"id": 4, "lines": ["-60% VALUE", "IN 5 YEARS"], "badge": "DEPRECIATING ASSET", "badge_col": (239, 68, 68), "t_col": (245, 25, 55), "b_col": (255, 30, 60), "plate": "12min_doc_plate_04.jpg"},
            {"id": 5, "lines": ["PAYING 9.5%", "ON A SINKING SHIP"], "badge": "COMPOUND PENALTY", "badge_col": (239, 68, 68), "t_col": (245, 25, 55), "b_col": (255, 30, 60), "plate": "12min_doc_plate_05.jpg"},
            {"id": 6, "lines": ["INDEX COMPOUNDING", "ALTERNATIVE"], "badge": "THE REAL CHOICE", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_06.jpg"},
            {"id": 7, "lines": ["COMPOUNDS TO", "₹58 LAKHS"], "badge": "10-YEAR WEALTH ALPHA", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "12min_doc_plate_07.jpg"},
            {"id": 8, "lines": ["DELAYS RETIREMENT", "BY 3.2 YEARS"], "badge": "TIME HORIZON PENALTY", "badge_col": (239, 68, 68), "t_col": (245, 25, 55), "b_col": (255, 30, 60), "plate": "12min_doc_plate_08.jpg"},
            {"id": 9, "lines": ["AUDIT BEFORE", "YOU SIGN"], "badge": "PROTECT YOUR WEALTH", "badge_col": (245, 158, 11), "t_col": (245, 158, 11), "b_col": (255, 160, 20), "plate": "12min_doc_plate_09.jpg"},
            {"id": 10, "lines": ["CAR TRAP OS", "DIAGNOSTIC"], "badge": "QUANT CALCULATOR", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_10.jpg"},
            {"id": 11, "lines": ["100% FREE", "BULLPRINTMEDIA.COM"], "badge": "ZERO PAYWALLS", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_11.jpg"},
            {"id": 12, "lines": ["CLAIM YOUR", "AUDIT REPORT"], "badge": "LINK IN DESCRIPTION", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "bull_print_banner_plate_1794211800384.jpg"}
        ],
        "captions": [
            (0, 3, ["Your", "car", "loan", "steals", "sixty", "lakhs."]),
            (3, 6, ["Asking", "only:", "can", "I", "afford", "EMI?"]),
            (6, 9, ["18", "lakh", "car", "costs", "21", "lakhs."]),
            (9, 12, ["Cars", "lose", "60%", "value", "in", "5", "years."]),
            (12, 15, ["Paying", "9.5%", "on", "a", "falling", "asset."]),
            (15, 18, ["Invested", "into", "index", "funds", "instead,"]),
            (18, 21, ["That", "compounds", "into", "58", "lakhs."]),
            (21, 24, ["It", "delays", "retirement", "by", "3.2", "years."]),
            (24, 27, ["Audit", "before", "you", "sign", "loans."]),
            (27, 30, ["Our", "engine", "reveals", "true", "cost."]),
            (30, 33, ["Use", "this", "free", "at", "bullprintmedia.com."]),
            (33, 36, ["Download", "your", "free", "report", "now."])
        ]
    },
    # Tool 04: Step-Up SIP Compounder
    {
        "id": "Tool_04_Step_Up_SIP_Compounder",
        "tool_key": "sip",
        "script": [
            "Why do ninety percent of mutual fund investors fail to build true wealth?",
            "Because keeping your SIP flat for fifteen years guarantees losing to seven percent inflation.",
            "If your salary increases by ten percent annually, keeping your SIP identical destroys your savings rate.",
            "By simply stepping up your SIP by ten percent each year to match your increment,",
            "Your maturity wealth explodes from sixty-seven lakhs to nearly one point eight crores.",
            "That is nearly three times more wealth without cutting your current lifestyle.",
            "Our Step-Up Compounder lets you test custom annual step-up rates from zero to twenty-five percent.",
            "See the exponential divergence between invested capital and pure compounding gains in real time.",
            "Stop investing with flat yesterday numbers.",
            "Calculate your exact step-up trajectory one hundred percent free at bullprintmedia.com.",
            "Claim your twenty-year personalized wealth roadmap today."
        ],
        "cuts": [
            {"id": 1, "lines": ["WHY FLAT SIPS", "FAIL OVER TIME"], "badge": "THE INFLATION TRAP", "badge_col": (239, 68, 68), "t_col": (245, 25, 55), "b_col": (255, 30, 60), "plate": "12min_doc_plate_01.jpg"},
            {"id": 2, "lines": ["7% LIFESTYLE", "INFLATION ATTACK"], "badge": "PURCHASING POWER", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "12min_doc_plate_02.jpg"},
            {"id": 3, "lines": ["SALARY RISES 10%", "SIP STAYS FLAT?"], "badge": "THE BIG MISTAKE", "badge_col": (245, 158, 11), "t_col": (245, 158, 11), "b_col": (255, 160, 20), "plate": "12min_doc_plate_03.jpg"},
            {"id": 4, "lines": ["THE 10% STEP-UP", "QUANT SECRET"], "badge": "MATCH SALARY HIKE", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_04.jpg"},
            {"id": 5, "lines": ["FROM ₹67 LAKHS", "TO ₹1.8 CRORES"], "badge": "2.4X MORE WEALTH", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "12min_doc_plate_05.jpg"},
            {"id": 6, "lines": ["TRIPLE YOUR CORPUS", "ZERO PAIN"], "badge": "LIFESTYLE PRESERVED", "badge_col": (0, 229, 255), "t_col": (0, 229, 255), "b_col": (0, 200, 240), "plate": "12min_doc_plate_06.jpg"},
            {"id": 7, "lines": ["SLIDE STEP-UP", "0% TO 25%"], "badge": "INTERACTIVE MODEL", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_07.jpg"},
            {"id": 8, "lines": ["EXPONENTIAL", "COMPOUNDING"], "badge": "PURE ALPHA CURVE", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "12min_doc_plate_08.jpg"},
            {"id": 9, "lines": ["UPGRADE YOUR", "STRATEGY"], "badge": "QUANT CLARITY", "badge_col": (245, 158, 11), "t_col": (245, 158, 11), "b_col": (255, 160, 20), "plate": "12min_doc_plate_09.jpg"},
            {"id": 10, "lines": ["STEP-UP SIP", "ENGINE OS"], "badge": "INSTITUTIONAL TOOL", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_10.jpg"},
            {"id": 11, "lines": ["100% FREE", "BULLPRINTMEDIA.COM"], "badge": "NO SUBSCRIPTION", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_11.jpg"},
            {"id": 12, "lines": ["DOWNLOAD YOUR", "20-YR ROADMAP"], "badge": "LINK IN DESCRIPTION", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "bull_print_banner_plate_1794211800384.jpg"}
        ],
        "captions": [
            (0, 3, ["Flat", "SIPs", "fail", "over", "time."]),
            (3, 6, ["7%", "inflation", "cuts", "wealth", "in", "half."]),
            (6, 9, ["Salary", "rises,", "so", "step", "up", "SIP."]),
            (9, 12, ["10%", "annual", "step-up", "changes", "everything."]),
            (12, 15, ["Grow", "from", "67", "lakhs", "to", "1.8", "crores."]),
            (15, 18, ["Nearly", "triple", "the", "final", "wealth."]),
            (18, 21, ["Test", "your", "own", "step-up", "rate."]),
            (21, 24, ["Watch", "compounding", "returns", "explode."]),
            (24, 27, ["Upgrade", "your", "investing", "system."]),
            (27, 30, ["Our", "engine", "reveals", "the", "numbers."]),
            (30, 33, ["Use", "this", "free", "at", "bullprintmedia.com."]),
            (33, 36, ["Download", "your", "wealth", "roadmap", "now."])
        ]
    },
    # Tool 05: Debt Snowball vs Avalanche Optimizer
    {
        "id": "Tool_05_Debt_Snowball_Avalanche_Optimizer",
        "tool_key": "debt-destroyer",
        "script": [
            "Paying the minimum due on your credit card takes up to twenty-seven years to clear.",
            "You end up paying four hundred percent more than what you actually borrowed in pure interest.",
            "High interest compound debt acts like aggressive financial cancer.",
            "The Bull Print Debt Destroyer mathematically optimizes the quantitative Avalanche method.",
            "It prioritizes your forty-two percent APR credit card debt first while maintaining minimums on others.",
            "Saving you over four point eight lakhs in pure interest payments.",
            "And slashing your payoff timeline by over eighty percent faster.",
            "Model both Snowball and Avalanche strategies side by side in seconds.",
            "Get your exact month by month debt freedom milestone calendar.",
            "Break free from the banking interest trap forever.",
            "Use this tool one hundred percent free at bullprintmedia.com.",
            "Download your custom debt free milestone tracker today."
        ],
        "cuts": [
            {"id": 1, "lines": ["42% CREDIT CARD", "INTEREST PRISON"], "badge": "FINANCIAL CANCER", "badge_col": (239, 68, 68), "t_col": (245, 25, 55), "b_col": (255, 30, 60), "plate": "12min_doc_plate_01.jpg"},
            {"id": 2, "lines": ["THE 27-YEAR", "MINIMUM DUE TRAP"], "badge": "BANK PROFITS", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "12min_doc_plate_02.jpg"},
            {"id": 3, "lines": ["400% MORE", "INTEREST PAID"], "badge": "THE HIDDEN COST", "badge_col": (239, 68, 68), "t_col": (245, 25, 55), "b_col": (255, 30, 60), "plate": "12min_doc_plate_03.jpg"},
            {"id": 4, "lines": ["DEBT AVALANCHE", "QUANT METHOD"], "badge": "MATHEMATICAL FIX", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_04.jpg"},
            {"id": 5, "lines": ["KILL 42% APR", "CARD FIRST"], "badge": "PRIORITY TARGET", "badge_col": (239, 68, 68), "t_col": (245, 25, 55), "b_col": (255, 30, 60), "plate": "12min_doc_plate_05.jpg"},
            {"id": 6, "lines": ["SAVES ₹4.8 LAKHS", "PURE INTEREST"], "badge": "INSTANT SAVINGS", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "12min_doc_plate_06.jpg"},
            {"id": 7, "lines": ["83% TIME", "SLASHED OFF"], "badge": "VELOCITY WIN", "badge_col": (0, 229, 255), "t_col": (0, 229, 255), "b_col": (0, 200, 240), "plate": "12min_doc_plate_07.jpg"},
            {"id": 8, "lines": ["SNOWBALL VS", "AVALANCHE MODEL"], "badge": "SIDE BY SIDE", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_08.jpg"},
            {"id": 9, "lines": ["EXACT DATE", "TO ZERO DEBT"], "badge": "CLEAR CALENDAR", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "12min_doc_plate_09.jpg"},
            {"id": 10, "lines": ["DEBT DESTROYER", "ENGINE OS"], "badge": "FREE INSTITUTIONAL TOOL", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_10.jpg"},
            {"id": 11, "lines": ["100% FREE", "BULLPRINTMEDIA.COM"], "badge": "NO CHARGES", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_11.jpg"},
            {"id": 12, "lines": ["DOWNLOAD YOUR", "DEBT-FREE OS"], "badge": "LINK IN DESCRIPTION", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "bull_print_banner_plate_1794211800384.jpg"}
        ],
        "captions": [
            (0, 3, ["Paying", "minimum", "due", "takes", "27", "years."]),
            (3, 6, ["Paying", "400%", "more", "than", "borrowed."]),
            (6, 9, ["High", "interest", "debt", "is", "financial", "cancer."]),
            (9, 12, ["The", "Avalanche", "method", "solves", "it."]),
            (12, 15, ["Kill", "the", "42%", "card", "debt", "first."]),
            (15, 18, ["Saves", "over", "4.8", "lakhs", "interest."]),
            (18, 21, ["Slashes", "payoff", "time", "by", "83%."]),
            (21, 24, ["Compare", "Snowball", "vs", "Avalanche."]),
            (24, 27, ["Get", "your", "exact", "freedom", "date."]),
            (27, 30, ["Break", "free", "from", "banking", "traps."]),
            (30, 33, ["Use", "this", "free", "at", "bullprintmedia.com."]),
            (33, 36, ["Download", "your", "tracker", "today."])
        ]
    },
    # Tool 06: Stock DCF Intrinsic Value Screener
    {
        "id": "Tool_06_Stock_DCF_Intrinsic_Value",
        "tool_key": "dcf",
        "script": [
            "Stop buying stocks based on P E ratios, social media hype, or tips.",
            "That guarantees you buy at the absolute peak right before an eighty percent collapse.",
            "A stock is fractional ownership of a real business.",
            "Its true value is the discounted present value of all future cash flows.",
            "Our two-stage Discounted Cash Flow model brings hedge fund math to your pocket.",
            "Enter free cash flow per share, projected growth, discount rate, and terminal multiple.",
            "The model instantly calculates the intrinsic fair value with institutional margin of safety.",
            "Telling you whether a stock is heavily undervalued, fair value, or a dangerous bubble.",
            "Never overpay for an equity again.",
            "Value any stock in sixty seconds one hundred percent free at bullprintmedia.com.",
            "Download your complete institutional DCF spreadsheet model today."
        ],
        "cuts": [
            {"id": 1, "lines": ["STOP BUYING ON", "HYPE & P/E"], "badge": "THE RETAIL TRAP", "badge_col": (239, 68, 68), "t_col": (245, 25, 55), "b_col": (255, 30, 60), "plate": "12min_doc_plate_01.jpg"},
            {"id": 2, "lines": ["P/E RATIOS LIE", "TOP BUY TRAP"], "badge": "CRASH RISK", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "12min_doc_plate_02.jpg"},
            {"id": 3, "lines": ["WHAT IS A STOCK?", "FRACTION OF BIZ"], "badge": "CASH FLOW REALITY", "badge_col": (0, 229, 255), "t_col": (0, 229, 255), "b_col": (0, 200, 240), "plate": "12min_doc_plate_03.jpg"},
            {"id": 4, "lines": ["DISCOUNTED", "CASH FLOW MODEL"], "badge": "WALL STREET STANDARD", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_04.jpg"},
            {"id": 5, "lines": ["2-STAGE DCF", "IN 60 SECONDS"], "badge": "HEDGE FUND ALPHA", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "12min_doc_plate_05.jpg"},
            {"id": 6, "lines": ["FREE CASH FLOW", "& GROWTH RATE"], "badge": "KEY INPUTS", "badge_col": (245, 158, 11), "t_col": (245, 158, 11), "b_col": (255, 160, 20), "plate": "12min_doc_plate_06.jpg"},
            {"id": 7, "lines": ["INTRINSIC VALUE", "TRUE WORTH"], "badge": "MARGIN OF SAFETY", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_07.jpg"},
            {"id": 8, "lines": ["UNDERVALUED OR", "BUBBLE ASSET?"], "badge": "ACTIONABLE SIGNAL", "badge_col": (239, 68, 68), "t_col": (245, 25, 55), "b_col": (255, 30, 60), "plate": "12min_doc_plate_08.jpg"},
            {"id": 9, "lines": ["NEVER OVERPAY", "AGAIN"], "badge": "DISCIPLINED INVESTING", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "12min_doc_plate_09.jpg"},
            {"id": 10, "lines": ["DCF SCREENER", "ENGINE OS"], "badge": "INSTITUTIONAL TOOL", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_10.jpg"},
            {"id": 11, "lines": ["100% FREE", "BULLPRINTMEDIA.COM"], "badge": "ZERO SUBSCRIPTION", "badge_col": (0, 135, 90), "t_col": (0, 220, 130), "b_col": (0, 180, 90), "plate": "12min_doc_plate_11.jpg"},
            {"id": 12, "lines": ["DOWNLOAD YOUR", "DCF EXCEL MODEL"], "badge": "LINK IN DESCRIPTION", "badge_col": (255, 215, 0), "t_col": (255, 215, 0), "b_col": (255, 190, 30), "plate": "bull_print_banner_plate_1794211800384.jpg"}
        ],
        "captions": [
            (0, 3, ["Stop", "buying", "stocks", "on", "hype."]),
            (3, 6, ["P/E", "ratios", "lead", "to", "crashes."]),
            (6, 9, ["A", "stock", "is", "a", "real", "business."]),
            (9, 12, ["Value", "is", "future", "cash", "flows."]),
            (12, 15, ["Our", "DCF", "brings", "hedge", "fund", "math."]),
            (15, 18, ["Input", "free", "cash", "flow", "and", "growth."]),
            (18, 21, ["Get", "instant", "intrinsic", "fair", "value."]),
            (21, 24, ["Revealing", "margin", "of", "safety."]),
            (24, 27, ["Never", "overpay", "for", "equities", "again."]),
            (27, 30, ["Value", "any", "stock", "in", "60", "seconds."]),
            (30, 33, ["Use", "this", "free", "at", "bullprintmedia.com."]),
            (33, 36, ["Download", "your", "DCF", "model", "today."])
        ]
    }
]

def load_and_prep_plate(path, w=1080, h=1920):
    if not path.exists():
        path = list(BRAIN_DIR.glob("*.jpg"))[0]
    im = Image.open(path).convert("RGB")
    scale = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    left = (im.width - w) // 2
    top = (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))

async def generate_voice(text, out_path):
    import edge_tts
    comm = edge_tts.Communicate(text, "en-US-ChristopherNeural", rate="-2%")
    await comm.save(str(out_path))

def build_tool_short(spec):
    tool_folder = OUTPUT_DIR / spec["id"]
    tool_folder.mkdir(parents=True, exist_ok=True)
    voice_file = tool_folder / "christopher_voice.mp3"
    raw_video = tool_folder / "raw_frames.mp4"
    final_short = tool_folder / "master_video_magnates.mp4"

    full_narration = " ".join(spec["script"])
    print(f"\n==========================================")
    print(f"🎬 RENDERING: {spec['id']}")
    print(f"==========================================")

    # 1. Voice
    print(f"🎙️ Synthesizing ChristopherNeural (-2Hz)...")
    asyncio.run(generate_voice(full_narration, voice_file))

    # 2. Plates
    W, H = 1080, 1920
    fps = 30
    total_duration = 36.0
    total_frames = int(total_duration * fps)

    plates = {}
    for c in spec["cuts"]:
        plate_p = BRAIN_DIR / c["plate"]
        plates[c["id"]] = load_and_prep_plate(plate_p, W, H)

    # 3. Stream frames
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p", str(raw_video)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    cut_duration = total_duration / len(spec["cuts"])

    for f_idx in range(total_frames):
        t = f_idx / fps
        cut_idx = min(len(spec["cuts"]) - 1, int(t / cut_duration))
        curr_cut = spec["cuts"][cut_idx]

        cut_t = t - (cut_idx * cut_duration)
        cut_progress = cut_t / cut_duration

        # Dolly Zoom
        zoom = 1.0 + 0.05 * cut_progress
        base_im = plates[curr_cut["id"]]
        zw, zh = int(W * zoom), int(H * zoom)
        zoomed = base_im.resize((zw, zh), Image.Resampling.BILINEAR)
        zx = (zw - W) // 2
        zy = (zh - H) // 2
        frame_canvas = zoomed.crop((zx, zy, zx + W, zy + H)).convert("RGBA")

        # Slam Physics
        slam_duration = 0.28
        if cut_t < slam_duration:
            p = cut_t / slam_duration
            scale_anim = 1.0 + 0.40 * ((1.0 - p) ** 2) * math.cos(p * math.pi * 2.5)
            alpha_anim = min(255, int(255 * (p * 2.0)))
            shake_y = int(6.0 * (1.0 - p) * math.sin(p * math.pi * 4))
        else:
            p_hold = cut_t - slam_duration
            scale_anim = 1.0 + 0.015 * cut_progress
            alpha_anim = 255
            shake_y = int(2.5 * math.sin(p_hold * 2.2))

        # 3D Typography
        text_w, text_h = 1000, 650
        text_layer = Image.new("RGBA", (text_w, text_h), (0, 0, 0, 0))
        draw_t = ImageDraw.Draw(text_layer)

        f_size = int(125 * scale_anim)
        f_hero = ImageFont.truetype(FONT_IMPACT, f_size)
        f_badge = ImageFont.truetype(FONT_IMPACT, int(46 * scale_anim))

        y_offset = 20 + shake_y
        line_spacing = int(f_size * 0.96)
        col_face = curr_cut["t_col"]
        col_bloom = curr_cut["b_col"]

        for line in curr_cut["lines"]:
            for d in range(16, 0, -2):
                shade = int(70 * (1.0 - d / 16.0))
                draw_t.text((25 + d, y_offset + d), line, font=f_hero, fill=(shade, 0, 0, alpha_anim), stroke_width=7, stroke_fill=(0, 0, 0, alpha_anim))
            draw_t.text((25, y_offset), line, font=f_hero, fill=(col_face[0], col_face[1], col_face[2], alpha_anim), stroke_width=5, stroke_fill=(15, 0, 5, alpha_anim))
            y_offset += line_spacing

        # Stabilo Badge
        badge_text = curr_cut["badge"]
        b_len = int(draw_t.textlength(badge_text, font=f_badge))
        b_pad_x = 22
        b_h = int(60 * scale_anim)
        b_w = b_len + (b_pad_x * 2)
        b_y = y_offset + 14

        wipe_p = 1.0 if cut_t >= 0.40 else ((cut_t - 0.15) / 0.25 if cut_t >= 0.15 else 0.0)
        if wipe_p > 0.05:
            active_bw = int(b_w * wipe_p)
            bg_col = curr_cut["badge_col"]
            draw_t.rectangle([25, b_y, 25 + active_bw, b_y + b_h], fill=(bg_col[0], bg_col[1], bg_col[2], int(alpha_anim * 0.94)))
            if wipe_p > 0.4:
                b_text_col = (10, 10, 10) if bg_col != (239, 68, 68) else (255, 255, 255)
                draw_t.text((25 + b_pad_x, b_y + 8), badge_text, font=f_badge, fill=(b_text_col[0], b_text_col[1], b_text_col[2], alpha_anim))

        # Forward Shear 0.22
        m = [1, -0.22, 0, 0, 1, 0]
        slanted_text = text_layer.transform((text_w + 140, text_h), Image.Transform.AFFINE, m, resample=Image.Resampling.BILINEAR)

        # Volumetric Bloom
        alpha_channel = slanted_text.split()[3]
        bloom_mask = alpha_channel.filter(ImageFilter.GaussianBlur(32))
        bloom_layer = Image.new("RGBA", slanted_text.size, (col_bloom[0], col_bloom[1], col_bloom[2], 0))
        bloom_layer.putalpha(bloom_mask)

        tx, ty = (70, 250)
        frame_canvas.alpha_composite(bloom_layer, (tx, ty))
        frame_canvas.alpha_composite(slanted_text, (tx, ty))

        # Captions at Y = 1480
        draw_f = ImageDraw.Draw(frame_canvas)
        active_chunk = None
        for c_start, c_end, words in spec["captions"]:
            if c_start <= t <= c_end:
                active_chunk = (c_start, c_end, words)
                break

        if active_chunk:
            c_start, c_end, words = active_chunk
            n_words = len(words)
            c_dur = c_end - c_start
            w_idx = int(((t - c_start) / max(0.01, c_dur)) * n_words)
            w_idx = max(0, min(n_words - 1, w_idx))

            font_cap = ImageFont.truetype(FONT_IMPACT, 52)
            word_widths = [draw_f.textlength(w, font=font_cap) for w in words]
            space_w = draw_f.textlength(" ", font=font_cap)
            total_cap_w = sum(word_widths) + space_w * (n_words - 1)

            cap_x = (W - total_cap_w) // 2
            cap_y = 1480

            pill_pad_x = 24
            pill_pad_y = 10
            draw_f.rounded_rectangle(
                [cap_x - pill_pad_x, cap_y - pill_pad_y, cap_x + total_cap_w + pill_pad_x, cap_y + 60 + pill_pad_y],
                radius=18,
                fill=(10, 10, 15, 215),
                outline=(255, 215, 0, 180) if (w_idx % 2 == 0) else (239, 68, 68, 180),
                width=3
            )

            curr_x = cap_x
            for idx, w in enumerate(words):
                if idx == w_idx:
                    draw_f.text((curr_x + 1, cap_y + 1), w, font=font_cap, fill=(0, 0, 0, 255))
                    draw_f.text((curr_x, cap_y), w, font=font_cap, fill=(255, 220, 20, 255), stroke_width=3, stroke_fill=(180, 20, 30, 255))
                elif idx < w_idx:
                    draw_f.text((curr_x, cap_y), w, font=font_cap, fill=(245, 245, 245, 230))
                else:
                    draw_f.text((curr_x, cap_y), w, font=font_cap, fill=(150, 150, 155, 160))
                curr_x += word_widths[idx] + space_w

        proc.stdin.write(frame_canvas.convert("RGB").tobytes())

        if f_idx % 180 == 0 or f_idx == total_frames - 1:
            print(f"  Frame {f_idx + 1}/{total_frames} rendered...")

    proc.stdin.close()
    proc.wait()

    # Audio Mux
    print("🎵 Muxing Christopher audio + ducked tension soundtrack (-18 LUFS)...")
    mux_cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
        "-i", str(voice_file),
        "-i", str(BGM_POOL),
        "-filter_complex",
        "[2:a]volume=0.16[bgm];[1:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(final_short)
    ]
    subprocess.run(mux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    if raw_video.exists():
        raw_video.unlink()

    shutil.copy(final_short, tool_folder / "master_video.mp4")
    print(f"🎉 MASTER SHORT COMPLETE: {final_short} ({total_duration}s)")

if __name__ == "__main__":
    for spec in TOOLS_SPECS:
        build_tool_short(spec)
    print("\n🚀 ALL 5 REMAINING TOOL SHORTS SUCCESSFULLY RENDERED TO MASTER ENGINE BAR!")
