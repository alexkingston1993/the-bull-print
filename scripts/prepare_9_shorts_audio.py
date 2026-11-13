#!/usr/bin/env python3
"""
Step 1: Audio Synthesis & Script Definition for 9 Viral YouTube Shorts
Channel: The Bull Print
"""

import asyncio
import json
import os
import subprocess
from pathlib import Path
import edge_tts

BASE_DIR = Path(__file__).resolve().parent.parent
SHORTS_DIR = BASE_DIR / "output" / "shorts"
SHORTS_DIR.mkdir(parents=True, exist_ok=True)

DRONE_WAV = BASE_DIR / "remotion-engine" / "public" / "audio" / "sfx_ambient_drone.wav"

SHORTS_DATA = [
    {
        "id": 1,
        "title": "The $2.5 Trillion AI Crash: What Happened to Big Tech #Shorts",
        "description": "In a single 24-hour trading session, $2.5 Trillion in market value evaporated from the Nasdaq. Here is what triggered the tech panic post-midterms.\n\n#TheBullPrint #TechStocks #Nasdaq #AI #StockMarket #Shorts",
        "tags": ["TheBullPrint", "TechStocks", "Nasdaq", "AI", "StockMarket", "Shorts"],
        "script": """In a single twenty-four hour window, two point five trillion dollars evaporated from the Nasdaq.
Tech shares suffered their worst plunge since April, tipping the index straight into official correction territory.
Why? The midterm election sweep sparked sudden panic that Washington is about to slap heavy regulations on AI data centers.
When Wall Street realized the AI capital expenditure party might face legislative gridlock, hedge funds rushed for the exit.
The AI boom isn't dead. But the era of free passes in Washington is officially over."""
    },
    {
        "id": 2,
        "title": "SEBI's Shock Move: 12.5% Tax Scrapped for Foreign Funds? #Shorts",
        "description": "After a record ₹3 Lakh Crore foreign capital flight, SEBI proposes removing the 12.5% LTCG tax for FIIs. Dalal Street's biggest tax bombshell.\n\n#TheBullPrint #SEBI #DalalStreet #LTCG #StockMarketIndia #FII #Shorts",
        "tags": ["TheBullPrint", "SEBI", "DalalStreet", "LTCG", "StockMarketIndia", "FII", "Shorts"],
        "script": """SEBI just dropped a multi-billion dollar bombshell on Dalal Street.
The regulator has officially recommended abolishing the twelve point five percent Long-Term Capital Gains tax for foreign institutional investors.
Over the past two months, global funds dumped three lakh crore rupees out of Indian equities, chasing high US bond yields.
To stop the bleeding and make India globally competitive, SEBI wants foreign tax hurdles erased.
If the Finance Ministry signs off, Dalal Street could see the largest flood of foreign institutional capital in Indian history."""
    },
    {
        "id": 3,
        "title": "The October Jobs Shocker: Why 165,000 Jobs Broke Wall Street #Shorts",
        "description": "U.S. employers added 165,000 jobs in October, crushing the 65,000 forecast. Why great economic news triggered a massive bond market sell-off.\n\n#TheBullPrint #USEconomy #JobsReport #FederalReserve #InterestRates #BondMarket #Shorts",
        "tags": ["TheBullPrint", "USEconomy", "JobsReport", "FederalReserve", "InterestRates", "BondMarket", "Shorts"],
        "script": """Wall Street was expecting sixty-five thousand new jobs. Instead, the economy exploded with one hundred sixty-five thousand.
Unemployment dropped to four point one percent, and wages surged faster than anticipated.
Normally, that would be celebration time. But the bond market instantly reacted in horror.
The ten-year Treasury yield spiked towards four point nine percent as investors realized the Federal Reserve cannot cut interest rates anytime soon.
In modern finance, good news for workers is terrifying news for debt-fueled stock valuations."""
    },
    {
        "id": 4,
        "title": "The ₹14,900 Crore U-Turn: FIIs Rush Back to Dalal Street #Shorts",
        "description": "Foreign institutional investors execute their biggest single-day buying spree in 7 months, pumping ₹14,900 crore into Indian bluechips.\n\n#TheBullPrint #DalalStreet #FII #Sensex #Nifty50 #IndianStockMarket #Shorts",
        "tags": ["TheBullPrint", "DalalStreet", "FII", "Sensex", "Nifty50", "IndianStockMarket", "Shorts"],
        "script": """Just when every retail trader gave up on Dalal Street, foreign institutions pulled a violent U-turn.
In a single trading session, foreign funds injected nearly fifteen thousand crore rupees back into Indian bluechips.
It marks the single largest one-day buying frenzy seen in seven months, driving benchmark indices into massive breakout rallies.
While retail panicked over global sell-offs, smart money scooped up oversold banking and tech leaders at discounted valuations.
Never mistake a temporary foreign outflow for a permanent exit."""
    },
    {
        "id": 5,
        "title": "The Midterm Gridlock: Why AI Data Centers Face Investigation #Shorts",
        "description": "Democrats sweep Congress in the U.S. midterm elections, bringing an end to unified party rule. What it means for tech monopolies and energy subsidies.\n\n#TheBullPrint #USPolitics #Congress #Midterms #BigTech #AI #Shorts",
        "tags": ["TheBullPrint", "USPolitics", "Congress", "Midterms", "BigTech", "AI", "Shorts"],
        "script": """The United States midterm elections just delivered an earthquake in Washington.
A total Democratic sweep of both the House and Senate has officially ended single-party rule.
Historically, Wall Street loves legislative gridlock. But this time, big tech is in the crosshairs.
Congressional committees are already preparing inquiries into the billions in federal subsidies funneled into artificial intelligence data centers.
The free-wheeling regulatory holiday for tech giants is meeting a divided government with subpoenas."""
    },
    {
        "id": 6,
        "title": "SEBI's Nuclear Option: Why Weekly Expiries Are Being Banned #Shorts",
        "description": "SEBI is dismantling weekly derivative contracts after retail traders lost ₹1.8 Lakh Crore. Inside the clampdown on Dalal Street's casino.\n\n#TheBullPrint #SEBI #OptionTrading #Nifty #BankNifty #StockMarketIndia #Shorts",
        "tags": ["TheBullPrint", "SEBI", "OptionTrading", "Nifty", "BankNifty", "StockMarketIndia", "Shorts"],
        "script": """Ninety-three percent of retail options traders in India lose money.
The total damage? Over one point eight lakh crore rupees wiped out in just three fiscal years.
Now, SEBI is dropping the hammer.
The regulator is systematically banning weekly index expiries, restricting exchanges to a single weekly contract per venue.
They are hiking lot sizes, increasing margin requirements, and cutting off intraday leverage.
The zero-day options casino that turned Dalal Street into a roulette wheel is officially closing its doors."""
    },
    {
        "id": 7,
        "title": "Big Tech's Nuclear Secret: Why AI Giants Are Buying Reactors #Shorts",
        "description": "Microsoft, Amazon, and Google are purchasing decommissioned nuclear reactors to power massive AI server clusters. The energy bottleneck exposed.\n\n#TheBullPrint #NuclearEnergy #ArtificialIntelligence #Microsoft #Amazon #BigTech #Shorts",
        "tags": ["TheBullPrint", "NuclearEnergy", "ArtificialIntelligence", "Microsoft", "Amazon", "BigTech", "Shorts"],
        "script": """Artificial intelligence has a dirty little secret: it is running out of electricity.
A single query on advanced AI models consumes ten times more power than a standard Google search.
By twenty-thirty, AI data centers in America will consume more power than the entire country of Japan.
That is why Microsoft signed a deal to restart the shuttered Three Mile Island nuclear plant.
Amazon and Google are buying nuclear reactors directly off the grid.
The winner of the AI race won't just be who has the best algorithms. It will be who controls the atomic power."""
    },
    {
        "id": 8,
        "title": "The Rupee at ₹85: How the RBI Is Fighting a Global Currency War #Shorts",
        "description": "The US Dollar Index surges, pushing USD/INR to test ₹85. Inside the Reserve Bank of India's multi-billion dollar foreign reserve defense.\n\n#TheBullPrint #IndianRupee #RBI #Forex #USDINR #DollarIndex #Economy #Shorts",
        "tags": ["TheBullPrint", "IndianRupee", "RBI", "Forex", "USDINR", "DollarIndex", "Economy", "Shorts"],
        "script": """The US dollar index is soaring, and the Indian Rupee is testing eighty-five per dollar.
Every single point the Rupee depreciates adds thousands of crores to India's crude oil import bill and feeds domestic inflation.
Behind the scenes, the Reserve Bank of India has stepped into the forex market with its seven-hundred-billion-dollar war chest.
By selling dollars and absorbing rupee liquidity, the central bank has prevented a currency tailspin.
India isn't just managing exchange rates. It is fighting an economic defensive war against global dollar dominance."""
    },
    {
        "id": 9,
        "title": "The $36 Trillion Trap: Why Central Banks Are Hoarding Gold #Shorts",
        "description": "Global central banks are hoarding physical gold at the fastest rate in human history. Why the $36 Trillion US debt is triggering a de-dollarization rush.\n\n#TheBullPrint #Gold #CentralBanks #DeDollarization #USDebt #GoldPrice #Shorts",
        "tags": ["TheBullPrint", "Gold", "CentralBanks", "DeDollarization", "USDebt", "GoldPrice", "Shorts"],
        "script": """While retail investors obsess over quarterly earnings, the world's central banks are quietly executing the largest gold rush in human history.
Countries from China and India to Saudi Arabia are accumulating physical gold bullion at record speed.
Why? Because the United States national debt just crossed thirty-six trillion dollars, with one trillion dollars paid annually just on interest.
Global financial authorities know that weaponized dollars and uncontrolled debt printing cannot last forever.
Gold isn't just an investment. To global superpowers, gold is monetary armor against sovereign default."""
    }
]

async def synthesize_all():
    print("🎙️ Synthesizing Voiceovers for all 9 Viral Shorts via edge-tts...")
    meta_path = SHORTS_DIR / "all_9_shorts_meta.json"
    
    tasks = []
    for item in SHORTS_DATA:
        sid = item["id"]
        raw_vo = SHORTS_DIR / f"short_{sid:02d}_vo.mp3"
        master_audio = SHORTS_DIR / f"short_{sid:02d}_audio.wav"
        
        print(f"[{sid:02d}/09] Synthesizing: {item['title'][:45]}...")
        comm = edge_tts.Communicate(item["script"], "en-US-ChristopherNeural", rate="+2%", pitch="-1Hz")
        await comm.save(str(raw_vo))
        
        # Mix with ambient drone
        filter_complex = (
            "[0:a]volume=1.3[vo];"
            "[1:a]aloop=loop=-1:size=2e+09,volume=0.20[bg];"
            "[vo][bg]amix=inputs=2:duration=first:dropout_transition=2[out]"
        )
        mix_cmd = [
            "ffmpeg", "-y",
            "-i", str(raw_vo),
            "-i", str(DRONE_WAV),
            "-filter_complex", filter_complex,
            "-map", "[out]",
            "-ar", "44100", "-ac", "2",
            str(master_audio)
        ]
        subprocess.run(mix_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"   -> Master audio: {master_audio.name}")

    with open(meta_path, "w") as f:
        json.dump(SHORTS_DATA, f, indent=2)
    print("✅ All 9 audio masters generated and saved!")

if __name__ == "__main__":
    asyncio.run(synthesize_all())
