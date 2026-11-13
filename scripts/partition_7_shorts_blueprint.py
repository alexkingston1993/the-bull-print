#!/usr/bin/env python3
"""
Master 3-Second Partitioning Spec for 7 Pending YouTube Shorts (Shorts 03 through 09)
Enforces:
- Exactly 1 frame every 3.0 seconds (Shorts Blueprint standard)
- 35mm clean photographic background plate (Zero baked-in text)
- Dynamic 3D typography lines & tactical badge pills
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output" / "shorts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SHORTS_SPEC = {
    "short_03": {
        "id": 3,
        "title": "The October Jobs Shocker: Why 165,000 Jobs Broke Wall Street #Shorts",
        "description": "U.S. employers added 165,000 jobs in October, crushing the 65,000 forecast. Why great economic news triggered a massive bond market sell-off.\n\n#TheBullPrint #USEconomy #JobsReport #FederalReserve #InterestRates #BondMarket #Shorts",
        "tags": ["TheBullPrint", "USEconomy", "JobsReport", "FederalReserve", "InterestRates", "BondMarket", "Shorts"],
        "audio_file": "short_03_audio.wav",
        "duration": 36.74,
        "cuts": [
            {
                "cut_idx": 1, "start": 0.0, "end": 3.0,
                "badge": "WALL STREET SHOCK", "badge_color": "yellow",
                "lines": ["65,000 JOBS", "EXPECTED"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, dramatic dark Wall Street trading floor, exhausted traders watching red digital ticker screens, moody volumetric shadows, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 2, "start": 3.0, "end": 6.0,
                "badge": "OCTOBER SURPRISE", "badge_color": "crimson",
                "lines": ["165,000 JOBS", "EXPLODED"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, towering Department of Labor neoclassical building in Washington at dusk with glowing amber windows, cold dramatic fog, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 3, "start": 6.0, "end": 9.0,
                "badge": "LABOR MARKET", "badge_color": "yellow",
                "lines": ["UNEMPLOYMENT", "FALLS TO 4.1%"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, high-tech corporate HR analytics center, glowing blue holographic charts of employment trends, shallow depth of field, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 4, "start": 9.0, "end": 12.0,
                "badge": "INFLATION RISK", "badge_color": "crimson",
                "lines": ["WAGE GROWTH", "ACCELERATES"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, modern manufacturing plant floor with high-precision robotic arms welding steel, bright glowing sparks, cinematic lighting, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 5, "start": 12.0, "end": 15.0,
                "badge": "BULL TRAP", "badge_color": "yellow",
                "lines": ["SHOULD BE", "CELEBRATION?"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, bustling New York stock exchange bell podium empty under dramatic spotlight, moody mist, dark financial architecture, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 6, "start": 15.0, "end": 18.0,
                "badge": "SELL-OFF TRIGGERED", "badge_color": "crimson",
                "lines": ["BOND MARKET", "IN HORROR"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, Wall Street bond trading terminal room, panic among institutional portfolio managers, red alarm ambient lighting, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 7, "start": 18.0, "end": 21.0,
                "badge": "YIELD SPIKE", "badge_color": "yellow",
                "lines": ["TREASURY YIELDS", "RUSH TO 4.9%"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, imposing marble columns of the Federal Reserve Eccles building in Washington DC under stormy midnight sky, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 8, "start": 21.0, "end": 24.0,
                "badge": "FED TRAPPED", "badge_color": "crimson",
                "lines": ["POWELL'S", "DILEMMA"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, dark leather boardroom chair at the head of a massive mahogany Federal Reserve table, dramatic single spotlight, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 9, "start": 24.0, "end": 27.0,
                "badge": "RATE FREEZE", "badge_color": "yellow",
                "lines": ["NO RATE CUTS", "IN SIGHT"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, massive industrial steel vault door locking tight with heavy mechanical gears, dark moody lighting, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 10, "start": 27.0, "end": 30.0,
                "badge": "DEBT SPIRAL", "badge_color": "crimson",
                "lines": ["DEBT-FUELED", "STOCKS CRACK"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, gleaming glass skyscraper of a Wall Street mega-bank reflecting dark stormy clouds, dramatic lightning flash, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 11, "start": 30.0, "end": 33.0,
                "badge": "PARADOX", "badge_color": "yellow",
                "lines": ["GOOD NEWS", "IS BAD NEWS"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, classic brass scales of justice tipping dangerously on an ancient mahogany desk, shadows, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 12, "start": 33.0, "end": 36.74,
                "badge": "THE REALITY", "badge_color": "crimson",
                "lines": ["WELCOME TO", "MODERN FINANCE"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, lone financial analyst standing before a panoramic glass window overlooking dark Manhattan skyline at midnight, 35mm photograph, zero text, no text, clean background."
            }
        ]
    },
    "short_04": {
        "id": 4,
        "title": "The ₹14,900 Crore U-Turn: FIIs Rush Back to Dalal Street #Shorts",
        "description": "Foreign institutional investors execute their biggest single-day buying spree in 7 months, pumping ₹14,900 crore into Indian bluechips.\n\n#TheBullPrint #DalalStreet #FII #Sensex #Nifty50 #IndianStockMarket #Shorts",
        "tags": ["TheBullPrint", "DalalStreet", "FII", "Sensex", "Nifty50", "IndianStockMarket", "Shorts"],
        "audio_file": "short_04_audio.wav",
        "duration": 34.20,
        "cuts": [
            {
                "cut_idx": 1, "start": 0.0, "end": 3.0,
                "badge": "RETAIL SURRENDER", "badge_color": "yellow",
                "lines": ["RETAIL GAVE UP", "ON DALAL ST"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, Bombay Stock Exchange Phiroze Jeejeebhoy Towers at dawn, moody monsoon atmosphere, wet pavement reflections, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 2, "start": 3.0, "end": 6.0,
                "badge": "INSTITUTIONAL SHOCK", "badge_color": "crimson",
                "lines": ["FOREIGN FUNDS", "VIOLENT U-TURN"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, sleek modern high-frequency institutional trading desk in Mumbai BKC financial district, multi-screen glow, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 3, "start": 6.0, "end": 9.0,
                "badge": "RECORD INFLOW", "badge_color": "yellow",
                "lines": ["₹14,900 CRORE", "PUMPED IN"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, high-security Indian bank currency treasury vault with stacks of clean bundled rupee currency notes, golden lighting, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 4, "start": 9.0, "end": 12.0,
                "badge": "7-MONTH RECORD", "badge_color": "crimson",
                "lines": ["BIGGEST BUYING", "IN 7 MONTHS"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, bronze charging bull statue in Mumbai illuminated dramatically by nighttime floodlights, powerful low-angle heroic view, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 5, "start": 12.0, "end": 15.0,
                "badge": "MARKET EXPLOSION", "badge_color": "yellow",
                "lines": ["NIFTY & SENSEX", "BREAKOUT RALLY"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, bustling Dalal Street trading floor cheering, green laser light reflections in the air, energetic atmosphere, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 6, "start": 15.0, "end": 18.0,
                "badge": "RETAIL PANIC", "badge_color": "crimson",
                "lines": ["RETAIL DUMPED", "AT THE BOTTOM"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, a retail investor staring in shock at his smartphone in a dark apartment room, screen glowing on face, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 7, "start": 18.0, "end": 21.0,
                "badge": "SMART MONEY MOVE", "badge_color": "yellow",
                "lines": ["SMART MONEY", "ACCUMULATING"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, luxury private wealth boardroom overlooking the Bandra-Worli Sea Link at sunset, silhouetted hedge fund managers, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 8, "start": 21.0, "end": 24.0,
                "badge": "TARGET SECTORS", "badge_color": "crimson",
                "lines": ["BANKING & TECH", "BLUECHIPS"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, gleaming glass corporate headquarters of major Indian private banking institutions in Mumbai, modern architecture, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 9, "start": 24.0, "end": 27.0,
                "badge": "DISCOUNT HUNTING", "badge_color": "yellow",
                "lines": ["CHEAP VALUATION", "FIRE SALE"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, close-up of institutional investor hands signing confidential acquisition term sheet with luxury fountain pen, warm rim light, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 10, "start": 27.0, "end": 30.0,
                "badge": "GOLDEN LESSON", "badge_color": "crimson",
                "lines": ["OUTFLOW IS NOT", "AN EXIT"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, high-tech server racks in Mumbai financial data center with flashing green and amber optic fiber status LEDs, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 11, "start": 30.0, "end": 34.20,
                "badge": "THE VERDICT", "badge_color": "yellow",
                "lines": ["FOLLOW THE", "SMART MONEY"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, panoramic view of Mumbai skyline from Marine Drive at twilight, illuminated skyscrapers reflecting in the Arabian Sea, 35mm photograph, zero text, no text, clean background."
            }
        ]
    },
    "short_05": {
        "id": 5,
        "title": "The Midterm Gridlock: Why AI Data Centers Face Investigation #Shorts",
        "description": "Democrats sweep Congress in the U.S. midterm elections, bringing an end to unified party rule. What it means for tech monopolies and energy subsidies.\n\n#TheBullPrint #USPolitics #Congress #Midterms #BigTech #AI #Shorts",
        "tags": ["TheBullPrint", "USPolitics", "Congress", "Midterms", "BigTech", "AI", "Shorts"],
        "audio_file": "short_05_audio.wav",
        "duration": 31.78,
        "cuts": [
            {
                "cut_idx": 1, "start": 0.0, "end": 3.0,
                "badge": "POLITICAL EARTHQUAKE", "badge_color": "crimson",
                "lines": ["WASHINGTON", "POWER SHIFT"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, United States Capitol dome at dusk with stormy clouds swirling above, dramatic illumination, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 2, "start": 3.0, "end": 6.0,
                "badge": "CONGRESSIONAL SWEEP", "badge_color": "yellow",
                "lines": ["DEMOCRATS SWEEP", "HOUSE & SENATE"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, empty congressional committee hearing room with rows of wooden desks, microphones, and flags in dark moody lighting, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 3, "start": 6.0, "end": 9.0,
                "badge": "END OF UNIFIED RULE", "badge_color": "crimson",
                "lines": ["ONE-PARTY RULE", "OFFICIALLY OVER"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, imposing bronze gavel resting on dark polished walnut bench beside legal briefs, dramatic beam of light, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 4, "start": 9.0, "end": 12.0,
                "badge": "WALL STREET PARADOX", "badge_color": "yellow",
                "lines": ["GRIDLOCK NORMALLY", "LOVED BY STOCKS"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, Wall Street financial district canyon between skyscrapers, rain slicked asphalt reflecting yellow taxi lights, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 5, "start": 12.0, "end": 15.0,
                "badge": "BIG TECH TARGET", "badge_color": "crimson",
                "lines": ["THIS TIME TECH", "IN CROSSHAIRS"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, glowing futuristic semiconductor silicon wafer under magnifying lens in dark microchip cleanroom, blue neon glow, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 6, "start": 15.0, "end": 18.0,
                "badge": "BILLIONS IN SUBSIDIES", "badge_color": "yellow",
                "lines": ["AI DATA CENTERS", "UNDER PROBE"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, sprawling hyperscale AI data center warehouse in Virginia countryside at night, thousands of cooling towers emitting steam, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 7, "start": 18.0, "end": 21.0,
                "badge": "FEDERAL SCRUTINY", "badge_color": "crimson",
                "lines": ["ENERGY DRAIN", "QUESTIONED"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, massive high-voltage electrical substation with towering power lines buzzing against a dark thunderous sky, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 8, "start": 21.0, "end": 24.0,
                "badge": "REGULATORY HOLIDAY OVER", "badge_color": "yellow",
                "lines": ["TECH GIANTS", "FREE PASS ENDS"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, sleek glass Silicon Valley tech campus boardroom with executive silhouettes facing dark stormy exterior, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 9, "start": 24.0, "end": 27.0,
                "badge": "SUBPOENAS COMING", "badge_color": "crimson",
                "lines": ["CONGRESSIONAL", "SUBPOENAS"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, official government subpoena document envelope stamped with red wax seal on a marble table, dramatic spotlight, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 10, "start": 27.0, "end": 30.0,
                "badge": "VALUATION SQUEEZE", "badge_color": "yellow",
                "lines": ["TECH MULTIPLES", "AT RISK"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, Nasdaq trading screen showing falling stock bars with red reflection on a glass barrier, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 11, "start": 30.0, "end": 31.78,
                "badge": "NEW ERA", "badge_color": "crimson",
                "lines": ["WASHINGTON'S", "WAR ON TECH"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, the Washington Monument piercing dark dusk clouds, majestic and solemn architectural silhouette, 35mm photograph, zero text, no text, clean background."
            }
        ]
    },
    "short_06": {
        "id": 6,
        "title": "SEBI's Nuclear Option: Why Weekly Expiries Are Being Banned #Shorts",
        "description": "SEBI is dismantling weekly derivative contracts after retail traders lost ₹1.8 Lakh Crore. Inside the clampdown on Dalal Street's casino.\n\n#TheBullPrint #SEBI #OptionTrading #Nifty #BankNifty #StockMarketIndia #Shorts",
        "tags": ["TheBullPrint", "SEBI", "OptionTrading", "Nifty", "BankNifty", "StockMarketIndia", "Shorts"],
        "audio_file": "short_06_audio.wav",
        "duration": 34.92,
        "cuts": [
            {
                "cut_idx": 1, "start": 0.0, "end": 3.0,
                "badge": "RETAIL MASSACRE", "badge_color": "crimson",
                "lines": ["93% OF TRADERS", "LOSE MONEY"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, an anxious Indian retail trader with head in hands at his computer desk, room lit by red candlestick chart glow, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 2, "start": 3.0, "end": 6.0,
                "badge": "THE CARNAGE", "badge_color": "yellow",
                "lines": ["₹1.8 LAKH CRORE", "EVAPORATED"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, burned and charred Indian paper currency floating through dark moody air, dramatic embers and sparks, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 3, "start": 6.0, "end": 9.0,
                "badge": "SEBI INTERVENTION", "badge_color": "crimson",
                "lines": ["SEBI DROPS", "THE HAMMER"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, SEBI Bhavan headquarters building in Bandra Kurla Complex Mumbai, imposing modern architectural facade, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 4, "start": 9.0, "end": 12.0,
                "badge": "WEEKLY BAN", "badge_color": "yellow",
                "lines": ["WEEKLY EXPIRIES", "SYSTEMATICALLY BANNED"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, an industrial metal calendar with pages being dramatically torn off and shredded into pieces, dramatic dark rim lighting, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 5, "start": 12.0, "end": 15.0,
                "badge": "ONE PER EXCHANGE", "badge_color": "crimson",
                "lines": ["SINGLE CONTRACT", "PER VENUE"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, the National Stock Exchange of India glass dome atrium in Mumbai, stark and orderly financial institution, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 6, "start": 15.0, "end": 18.0,
                "badge": "LOT SIZE HIKE", "badge_color": "yellow",
                "lines": ["LOT SIZES", "DOUBLED"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, heavy iron industrial weight slamming down onto a metal testing table, sparks, dark dramatic lighting, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 7, "start": 18.0, "end": 21.0,
                "badge": "MARGIN CRUSH", "badge_color": "crimson",
                "lines": ["MARGIN RULES", "HIKED UP"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, bank vault security barrier bars sliding shut with hydraulic precision, metallic gleam, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 8, "start": 21.0, "end": 24.0,
                "badge": "LEVERAGE CUT", "badge_color": "yellow",
                "lines": ["INTRADAY LEVERAGE", "KILLED"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, thick copper electrical power cable being cleanly severed with bright blue electrical arc, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 9, "start": 24.0, "end": 27.0,
                "badge": "CASINO CLOSING", "badge_color": "crimson",
                "lines": ["DALAL STREET CASINO", "SHUT DOWN"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, roulette wheel in a luxury casino abandoned in shadows, chips scattered, dim velvet lighting, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 10, "start": 27.0, "end": 30.0,
                "badge": "REVENUE HIT", "badge_color": "yellow",
                "lines": ["DISCOUNT BROKERS", "IN TROUBLE"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, modern fintech trading app office after hours, empty open-plan desks with illuminated screens, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 11, "start": 30.0, "end": 33.0,
                "badge": "CAPITAL SHIFT", "badge_color": "crimson",
                "lines": ["FLOWS RETURN", "TO MUTUAL FUNDS"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, a secure gold bullion vault with rows of polished pure gold bars under warm security lighting, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 12, "start": 33.0, "end": 34.92,
                "badge": "FINAL CURTAIN", "badge_color": "crimson",
                "lines": ["THE END OF", "ZERO-DAY GAMBLING"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, heavy iron gates of Dalal Street closing firmly against a backdrop of glowing Mumbai skyscrapers, 35mm photograph, zero text, no text, clean background."
            }
        ]
    },
    "short_07": {
        "id": 7,
        "title": "Big Tech's Nuclear Secret: Why AI Giants Are Buying Reactors #Shorts",
        "description": "Microsoft, Amazon, and Google are purchasing decommissioned nuclear reactors to power massive AI server clusters. The energy bottleneck exposed.\n\n#TheBullPrint #NuclearEnergy #ArtificialIntelligence #Microsoft #Amazon #BigTech #Shorts",
        "tags": ["TheBullPrint", "NuclearEnergy", "ArtificialIntelligence", "Microsoft", "Amazon", "BigTech", "Shorts"],
        "audio_file": "short_07_audio.wav",
        "duration": 36.50,
        "cuts": [
            {
                "cut_idx": 1, "start": 0.0, "end": 3.0,
                "badge": "AI DIRTY SECRET", "badge_color": "yellow",
                "lines": ["AI IS RUNNING", "OUT OF POWER"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, giant AI server hall undergoing sudden blackout, emergency amber beacon lights spinning, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 2, "start": 3.0, "end": 6.0,
                "badge": "ENERGY HUNGER", "badge_color": "crimson",
                "lines": ["10X MORE POWER", "PER QUERY"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, glowing glowing high-voltage electrical transformer humming with blue plasma corona discharge, dramatic shadows, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 3, "start": 6.0, "end": 9.0,
                "badge": "2030 FORECAST", "badge_color": "yellow",
                "lines": ["MORE POWER THAN", "ALL OF JAPAN"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, aerial nighttime view of Tokyo illuminated by millions of city lights sprawling to the horizon, dark sky, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 4, "start": 9.0, "end": 12.0,
                "badge": "GRID CHOKEHOLD", "badge_color": "crimson",
                "lines": ["AMERICAN GRID", "AT BREAKING POINT"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, massive electrical transmission towers marching across mountainous landscape under a dark stormy sky, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 5, "start": 12.0, "end": 15.0,
                "badge": "MICROSOFT SHOCK", "badge_color": "yellow",
                "lines": ["THREE MILE ISLAND", "REOPENING"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, iconic concrete cooling towers of Three Mile Island nuclear generating station reflected in river at sunrise, misty morning, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 6, "start": 15.0, "end": 18.0,
                "badge": "ATOMIC BILLIONS", "badge_color": "crimson",
                "lines": ["BILLIONS FOR", "NUCLEAR REACTORS"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, interior of nuclear reactor containment building with blue Cherenkov radiation glowing underwater in fuel pool, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 7, "start": 18.0, "end": 21.0,
                "badge": "AMAZON & GOOGLE", "badge_color": "yellow",
                "lines": ["BUYING DIRECTLY", "OFF THE GRID"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, modern modular nuclear reactor facility adjacent to massive glass tech datacenter, sleek clean energy future, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 8, "start": 21.0, "end": 24.0,
                "badge": "CLEAN BASELOAD", "badge_color": "crimson",
                "lines": ["24/7 ZERO-CARBON", "ATOMIC POWER"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, high-tech nuclear control room with glowing dials, monitors, and safety switches manned by engineers, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 9, "start": 24.0, "end": 27.0,
                "badge": "ALGORITHM VS ENERGY", "badge_color": "yellow",
                "lines": ["CODE IS NOT", "ENOUGH"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, futuristic AI microchip connected by heavy industrial copper electrical cables, glowing with heat, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 10, "start": 27.0, "end": 30.0,
                "badge": "THE NEW MOAT", "badge_color": "crimson",
                "lines": ["WHO CONTROLS", "THE GIGAWATTS?"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, massive hydroelectric dam turbine hall with giant spinning generators, immense industrial scale, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 11, "start": 30.0, "end": 33.0,
                "badge": "BIG TECH MONOPOLY", "badge_color": "yellow",
                "lines": ["ENERGY MONOPOLY", "IS THE PRIZE"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, silhouettes of Silicon Valley tech titans looking out over high-voltage electrical switchyard at dusk, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 12, "start": 33.0, "end": 36.50,
                "badge": "THE ATOMIC RACE", "badge_color": "crimson",
                "lines": ["THE WINNER", "HOLDS THE ATOM"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, dramatic glowing atomic symbol motif hovering above illuminated futuristic server racks, high contrast, 35mm photograph, zero text, no text, clean background."
            }
        ]
    },
    "short_08": {
        "id": 8,
        "title": "The Rupee at ₹85: How the RBI Is Fighting a Global Currency War #Shorts",
        "description": "The US Dollar Index surges, pushing USD/INR to test ₹85. Inside the Reserve Bank of India's multi-billion dollar foreign reserve defense.\n\n#TheBullPrint #IndianRupee #RBI #Forex #USDINR #DollarIndex #Economy #Shorts",
        "tags": ["TheBullPrint", "IndianRupee", "RBI", "Forex", "USDINR", "DollarIndex", "Economy", "Shorts"],
        "audio_file": "short_08_audio.wav",
        "duration": 35.26,
        "cuts": [
            {
                "cut_idx": 1, "start": 0.0, "end": 3.0,
                "badge": "DOLLAR SURGE", "badge_color": "yellow",
                "lines": ["DOLLAR INDEX", "TEARING HIGHER"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, close-up of a crisp United States one hundred dollar bill under dramatic spotlight with sharp currency engraving details, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 2, "start": 3.0, "end": 6.0,
                "badge": "RUPEE PRESSURE", "badge_color": "crimson",
                "lines": ["RUPEE TESTS", "₹85 PER DOLLAR"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, Indian rupee notes fan out on a dark teak desk beside an antique brass balance scale, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 3, "start": 6.0, "end": 9.0,
                "badge": "IMPORT INFLATION", "badge_color": "yellow",
                "lines": ["CRUDE OIL BILL", "SKYROCKETS"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, massive oil supertanker unloading crude at Mumbai offshore terminal at sunset, industrial silhouettes, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 4, "start": 9.0, "end": 12.0,
                "badge": "DOMESTIC THREAT", "badge_color": "crimson",
                "lines": ["INFLATION FEARS", "RETURN"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, bustling crowded Indian wholesale market street in early morning, spice sacks, atmospheric dust and shafts of sunlight, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 5, "start": 12.0, "end": 15.0,
                "badge": "RBI WAR CHEST", "badge_color": "yellow",
                "lines": ["RBI DEPLOYS", "$700 BILLION"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, Reserve Bank of India historic headquarters facade in Fort Mumbai under dramatic sky, lion statues, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 6, "start": 15.0, "end": 18.0,
                "badge": "FOREX INTERVENTION", "badge_color": "crimson",
                "lines": ["SELLING DOLLARS", "IN DEFENSE"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, central bank foreign exchange trading room with institutional dealing desks and green trading screens, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 7, "start": 18.0, "end": 21.0,
                "badge": "LIQUIDITY SOAK", "badge_color": "yellow",
                "lines": ["ABSORBING RUPEE", "LIQUIDITY"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, deep underground central bank gold and foreign currency vault with heavy steel bars, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 8, "start": 21.0, "end": 24.0,
                "badge": "CRASH PREVENTED", "badge_color": "crimson",
                "lines": ["PREVENTING A", "CURRENCY TAILSPIN"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, storm-tossed cargo ship navigated safely through turbulent waters past a towering lighthouse, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 9, "start": 24.0, "end": 27.0,
                "badge": "GLOBAL CONFLICT", "badge_color": "yellow",
                "lines": ["ECONOMIC WAR", "ON DOLLAR"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, glowing geopolitical world financial map displayed on dark glass wall in military-style economic war room, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 10, "start": 27.0, "end": 30.0,
                "badge": "SOVEREIGN SHIELD", "badge_color": "crimson",
                "lines": ["SOVEREIGN", "FINANCIAL SHIELD"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, solid engraved titanium shield reflecting beams of amber light, dark museum gallery setting, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 11, "start": 30.0, "end": 33.0,
                "badge": "RUPEE RESILIENCE", "badge_color": "yellow",
                "lines": ["INDIA HOLDS", "THE LINE"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, Mumbai financial district skyline illuminated at night with Gateway of India silhouetted in foreground, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 12, "start": 33.0, "end": 35.26,
                "badge": "THE CURRENCY BATTLE", "badge_color": "crimson",
                "lines": ["THE BATTLE FOR", "MONETARY FREEDOM"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, antique brass compass resting on top of leather-bound global shipping charts, golden cinematic lighting, 35mm photograph, zero text, no text, clean background."
            }
        ]
    },
    "short_09": {
        "id": 9,
        "title": "The $36 Trillion Trap: Why Central Banks Are Hoarding Gold #Shorts",
        "description": "Global central banks are hoarding physical gold at the fastest rate in human history. Why the $36 Trillion US debt is triggering a de-dollarization rush.\n\n#TheBullPrint #Gold #CentralBanks #DeDollarization #USDebt #GoldPrice #Shorts",
        "tags": ["TheBullPrint", "Gold", "CentralBanks", "DeDollarization", "USDebt", "GoldPrice", "Shorts"],
        "audio_file": "short_09_audio.wav",
        "duration": 38.69,
        "cuts": [
            {
                "cut_idx": 1, "start": 0.0, "end": 3.0,
                "badge": "EARNINGS DISTRACTION", "badge_color": "yellow",
                "lines": ["RETAIL OBSESSES", "OVER EARNINGS"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, a retail investor office with multiple glowing stock charts in the dark, frantic green and red lines, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 2, "start": 3.0, "end": 6.0,
                "badge": "HISTORIC GOLD RUSH", "badge_color": "crimson",
                "lines": ["CENTRAL BANKS", "HOARDING GOLD"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, endless rows of massive pure gold bullion bars stacked high in Bank of England subterranean vault, golden glow, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 3, "start": 6.0, "end": 9.0,
                "badge": "RECORD ACCUMULATION", "badge_color": "yellow",
                "lines": ["FASTEST RATE", "IN HUMAN HISTORY"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, heavy forklift transporting pallets of solid gold bricks inside an ultra-secure underground fortress, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 4, "start": 9.0, "end": 12.0,
                "badge": "GLOBAL COALITION", "badge_color": "crimson",
                "lines": ["CHINA, INDIA", "& SAUDI ARABIA"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, summit table of world leaders at international economic forum, flags of major nations, dignified atmosphere, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 5, "start": 12.0, "end": 15.0,
                "badge": "THE CATALYST", "badge_color": "yellow",
                "lines": ["WHY ARE THEY", "BUYING PHYSICAL?"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, close-up of a jeweler or banker holding a gleaming heavy pure gold coin with intricate mint stamp under magnifying glass, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 6, "start": 15.0, "end": 18.0,
                "badge": "US DEBT DISASTER", "badge_color": "crimson",
                "lines": ["$36 TRILLION", "NATIONAL DEBT"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, United States Treasury building in Washington DC with looming storm clouds overhead, dramatic lightning strike, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 7, "start": 18.0, "end": 21.0,
                "badge": "INTEREST BURDEN", "badge_color": "yellow",
                "lines": ["$1 TRILLION/YR", "JUST IN INTEREST"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, giant printing press spitting out endless ribbons of unprinted paper currency in dark industrial factory, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 8, "start": 21.0, "end": 24.0,
                "badge": "WEAPONIZED DOLLAR", "badge_color": "crimson",
                "lines": ["DOLLAR SANCTIONS", "TRIGGER REVOLT"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, steel chain and heavy padlock wrapped tightly around international financial wire transfer cable, dark moody lighting, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 9, "start": 24.0, "end": 27.0,
                "badge": "DE-DOLLARIZATION", "badge_color": "yellow",
                "lines": ["PRINTING MONEY", "CANNOT LAST"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, crumbling classical Greco-Roman marble column in financial district, autumn leaves blowing in wind, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 10, "start": 27.0, "end": 30.0,
                "badge": "NOT AN INVESTMENT", "badge_color": "crimson",
                "lines": ["GOLD IS NOT", "JUST AN ASSET"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, gleaming solid gold bar sitting on dark velvet pedestal, warm spotlight casting soft reflections, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 11, "start": 30.0, "end": 33.0,
                "badge": "MONETARY ARMOR", "badge_color": "yellow",
                "lines": ["GOLD IS", "MONETARY ARMOR"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, antique knight armor chestplate crafted from gleaming gold steel, standing in a regal hall of mirrors, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 12, "start": 33.0, "end": 36.0,
                "badge": "DEFAULT DEFENSE", "badge_color": "crimson",
                "lines": ["SHIELD AGAINST", "SOVEREIGN DEFAULT"], "text_color": "crimson",
                "prompt": "Cinematic vertical 9:16 photographic shot, bank vault door shaped like an impenetrable vault fortress, dramatic volumetric golden light rays pouring through, 35mm photograph, zero text, no text, clean background."
            },
            {
                "cut_idx": 13, "start": 36.0, "end": 38.69,
                "badge": "THE HARD TRUTH", "badge_color": "yellow",
                "lines": ["TRUST IN GOLD", "NOT IN DEBT"], "text_color": "gold",
                "prompt": "Cinematic vertical 9:16 photographic shot, silhouette of a central bank governor standing before a mountain of gold ingots as dawn breaks through high arched windows, 35mm photograph, zero text, no text, clean background."
            }
        ]
    }
}

spec_file = OUTPUT_DIR / "shorts_3s_master_spec.json"
with open(spec_file, "w") as f:
    json.dump(SHORTS_SPEC, f, indent=2)

print(f"Successfully generated 3-second partition spec for all 7 pending shorts!")
for k, v in SHORTS_SPEC.items():
    print(f" - {k}: {len(v['cuts'])} cuts ({v['duration']}s)")
