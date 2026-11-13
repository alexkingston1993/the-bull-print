#!/usr/bin/env python3
"""
10 Viral Catchy Shorts Production Engine (Past 24 Hours News)
Channel: The Bull Print (@thebullprint)
Format: 9:16 Vertical Shorts (1080x1920, 60fps)
Standards:
- Voiceover: en-US-ChristopherNeural with -2Hz pitch
- 1 frame every 3.0 seconds (~15 to 20 clean 9:16 photographic frames per Short)
- Dynamic 3D Extruded Perspective Typography (forward italic shear 0.22, 16px shadow, neon bloom)
- Stabilo-style High-Contrast Tactical Alert Badges
- Lower-Third Word-Level Animated Captions in mobile safe zone (Y = 1480)
- Ambient tension drone audio bed (-18 LUFS)
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output" / "viral_shorts_past24h"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_DIR = BASE_DIR / "assets" / "fonts"
FONT_PATH = str(FONT_DIR / "Impact.ttf")

SHORTS_DATA = [
    {
        "id": "short_01",
        "title": "Nvidia Crushes Apple: The $5 Trillion Crown",
        "badge": "THE $5T CROWN",
        "hook_text": "NVIDIA OVERTAKES APPLE",
        "script": "Nvidia just officially surpassed Apple to become the most valuable company in human history, racing toward a staggering five trillion dollar market cap. While Apple beats revenue expectations, their hardware gross margins are getting severely squeezed by surging costs for AI data center memory chips. Wall Street is sending an unmistakable message: whoever controls the silicon that powers artificial intelligence now commands the world economy.",
        "beats": [
            ("seg_01", "Nvidia CEO Jensen Huang in leather jacket on high-tech keynote stage glowing green", "THE CROWN"),
            ("seg_02", "Golden stock chart breaking through five trillion dollar valuation barrier", "5 TRILLION"),
            ("seg_03", "Apple Park glass ring headquarters in Cupertino under dark twilight sky", "APPLE SQUEEZED"),
            ("seg_04", "Robotic assembly line manufacturing high-bandwidth memory chips under neon light", "CHIP SHORTAGE"),
            ("seg_05", "Wall Street trading floor with green ticker screens displaying Nvidia ticker NVDA", "NEW KING")
        ]
    },
    {
        "id": "short_02",
        "title": "The $2.5 Trillion Wipeout: Wall Street AI Panic",
        "badge": "MARKET CRASH",
        "hook_text": "$2.5 TRILLION GONE",
        "script": "Over two point five trillion dollars was just wiped out from the Nasdaq in a single brutal trading session. The post-midterm political shockwave in Washington has sparked intense fears of data center construction moratoriums, antitrust subpoenas, and aggressive regulations on Big Tech monopolies. Wall Street is finally waking up to the harsh physical reality: you cannot scale generative artificial intelligence without vast amounts of power.",
        "beats": [
            ("seg_01", "Times Square Nasdaq billboard glowing bright crimson red with falling market indices", "THE WIPEOUT"),
            ("seg_02", "Stock trader in jacket holding head in disbelief at multiple red trading monitors", "WALL ST PANIC"),
            ("seg_03", "United States Capitol building dome silhouetted against dramatic thunderstorm clouds", "REGULATORY SHOCK"),
            ("seg_04", "Heavy construction crane halted in mud beside an unfinished AI data center shell", "CONSTRUCTION HALTED"),
            ("seg_05", "High-voltage electrical substation sparking in the dark under extreme thermal load", "POWER WALL")
        ]
    },
    {
        "id": "short_03",
        "title": "Elon Musk Kills Cybertruck: The Cybercab Pivot",
        "badge": "CYBERTRUCK KILLED",
        "hook_text": "CYBERTRUCK SCRAPPED",
        "script": "Elon Musk has officially confirmed that Cybertruck production will be completely wound down by 2027. Why? Because Tesla is pivoting every single dollar of capital expenditure into fully autonomous Cybercabs and scaling xAI's Colossus cluster with hundreds of thousands of Nvidia Blackwell processors. The era of niche electric trucks is dead; the era of autonomous robotaxi fleets and sovereign AI computing is here.",
        "beats": [
            ("seg_01", "Futuristic stainless steel Cybertruck parked in dark industrial factory hangar", "THE CYBERTRUCK"),
            ("seg_02", "Elon Musk standing before industrial blueprint schematics with serious expression", "MUSK'S PIVOT"),
            ("seg_03", "Sleek two-seater autonomous Cybercab with glowing amber headlights driving in city", "THE CYBERCAB"),
            ("seg_04", "Dense server corridor of xAI Colossus supercomputer glowing with liquid-cooling blue", "COLOSSUS CLUSTER"),
            ("seg_05", "Digital autonomous fleet navigation map connecting thousands of robotic taxis", "THE FUTURE")
        ]
    },
    {
        "id": "short_04",
        "title": "Diwali Muhurat Trading 2026: Nifty Below 25,000",
        "badge": "MUHURAT SHOCK",
        "hook_text": "NIFTY SNAPS STREAK",
        "script": "Indian stock markets just concluded their traditional Diwali Muhurat trading session for Samvat 2083, and it surprised Wall Street. The benchmark Nifty snapped a seven-day winning streak, slipping below the key 25,000 level as foreign institutional funds booked profits. But beneath the surface, domestic retail SIP inflows of 25,000 crore rupees every month absorbed the selling, setting up a massive economic tug-of-war.",
        "beats": [
            ("seg_01", "Bombay Stock Exchange Phiroze Jeejeebhoy Towers illuminated with golden Diwali lamps", "MUHURAT 2083"),
            ("seg_02", "Traditional bronze Indian trading bell being struck on festive trading floor", "THE OPENING BELL"),
            ("seg_03", "Digital stock ticker board in Mumbai showing Nifty index hovering at 24,986", "25,000 SUPPORT"),
            ("seg_04", "Young professional Indian investor reviewing growing mutual fund SIP on smartphone", "RETAIL SHIELD"),
            ("seg_05", "Majestic charging bronze bull statue gleaming in golden fireworks celebration", "INDIA RISING")
        ]
    },
    {
        "id": "short_05",
        "title": "OpenAI's $1.25 Trillion Round vs Anthropic IPO",
        "badge": "$1.25T VALUATION",
        "hook_text": "THE $1.25T AI BET",
        "script": "OpenAI has just raised eleven billion dollars at an eye-watering one point two five trillion dollar valuation. Meanwhile, rival Anthropic is actively launching its pre-Thanksgiving IPO roadshow. This is the ultimate litmus test for Wall Street: can artificial intelligence software companies ever generate enough commercial cash flow to justify valuations larger than the gross domestic product of most industrialized nations?",
        "beats": [
            ("seg_01", "Sam Altman speaking into microphone in minimalist glass tech conference auditorium", "OPENAI ROUND"),
            ("seg_02", "Financial valuation ledger displaying 1.25 Trillion Dollars with glowing gold trim", "TRILLION CLUB"),
            ("seg_03", "Anthropic IPO prospectus document resting on Wall Street investment bank desk", "ANTHROPIC IPO"),
            ("seg_04", "Silicon Valley venture capital partners debating metrics in high-floor boardroom", "THE BUBBLE TEST"),
            ("seg_05", "Abstract glowing neural network brain dissolving into green dollar currency streams", "CASH FLOW REALITY")
        ]
    },
    {
        "id": "short_06",
        "title": "Gold Hits All-Time Highs: The Dollar Flight",
        "badge": "GOLD RUN",
        "hook_text": "GOLD SURGES HIGHER",
        "script": "Spot gold is on an absolute tear as global central banks accelerate their flight away from paper fiat currencies. With US Treasury yields sliding and the dollar index weakening post-midterms, institutional allocators like Citi are projecting historic multi-year highs for physical bullion. In an era of escalating sovereign debt and geopolitical currency shifts, the oldest store of value is reclaiming its throne.",
        "beats": [
            ("seg_01", "Stack of gleaming 999.9 pure gold bullion bars resting on black velvet in vault", "PHYSICAL GOLD"),
            ("seg_02", "Central bank vault door open revealing pallets of gold bars under security lights", "CENTRAL BANK BUY"),
            ("seg_03", "Falling US Dollar index chart juxtaposed against climbing golden price trajectory", "DOLLAR RETREATS"),
            ("seg_04", "Ancient gold coins spilling across modern digital trading terminal screen", "TIMELESS ASSET"),
            ("seg_05", "Molten liquid gold being poured into precision cast ingot mould emitting sparks", "THE STORE OF VALUE")
        ]
    },
    {
        "id": "short_07",
        "title": "Brent Crude Drops to $100: The Inflation Relief",
        "badge": "OIL COLLAPSE",
        "hook_text": "OIL SLIDES DOWN",
        "script": "Crude oil has experienced a sharp downward correction, with Brent falling toward the critical 100 dollar threshold. Markets are anticipating emergency OPEC plus production adjustments as geopolitical supply risks cool down. For central banks battling sticky consumer price inflation, cheaper crude provides a desperately needed breathing room—but energy producers are already bracing for a revenue shock.",
        "beats": [
            ("seg_01", "Offshore oil drilling rig in stormy North Sea waters illuminated at twilight", "BRENT DRIFT"),
            ("seg_02", "Industrial oil pipeline pressure gauges with analog needle dropping into green zone", "PRESSURE COOLING"),
            ("seg_03", "OPEC headquarters conference room in Vienna with member nation flags and delegates", "OPEC EMERGENCY"),
            ("seg_04", "Retail gasoline station price display numbers ticking downward in evening mist", "INFLATION RELIEF"),
            ("seg_05", "Giant oil supertanker cutting through deep ocean waters under stormy sunset sky", "GLOBAL LOGISTICS")
        ]
    },
    {
        "id": "short_08",
        "title": "The Memory Chip Crisis: Why Big Tech Is Panicking",
        "badge": "CHIP SHORTAGE",
        "hook_text": "AI MEMORY CRISIS",
        "script": "Apple just warned Wall Street that gross margins are under threat because of a quiet crisis: High Bandwidth Memory chips. Generative AI clusters consume so much specialized DRAM that hardware manufacturers cannot secure supplies. The semiconductor bottleneck is no longer just about Nvidia GPUs—it's about the physical memory chips required to keep artificial intelligence algorithms running.",
        "beats": [
            ("seg_01", "Microscopic silicon wafer under ultraviolet cleanroom lithography inspection light", "SILICON WAFER"),
            ("seg_02", "Extreme macro shot of high-bandwidth memory stack mounted on GPU substrate", "HBM MEMORY"),
            ("seg_03", "Cleanroom technician in full protective bunny suit inspecting silicon circuitry", "CLEANROOM CRISIS"),
            ("seg_04", "Corporate earnings financial report showing gross margin contraction in red ink", "MARGIN PRESSURE"),
            ("seg_05", "Rows of robotic pick-and-place machines soldering semiconductor chips at high speed", "SUPPLY BOTTLENECK")
        ]
    },
    {
        "id": "short_09",
        "title": "The 2030 Power Wall: Big Tech Buys Nuclear",
        "badge": "ATOMIC MEGAWATTS",
        "hook_text": "BIG TECH BUYS NUCLEAR",
        "script": "Microsoft, Amazon, and Google are purchasing entire nuclear power facilities because the public electrical grid cannot feed their AI clusters. By 2030, artificial intelligence data centers will consume more electricity than entire developed nations. The next trillion-dollar market is not software—it is the race to secure atomic baseload megawatts before the grid experiences rolling blackouts.",
        "beats": [
            ("seg_01", "Massive nuclear power station cooling towers venting thick white steam into sky", "NUCLEAR MEGAWATTS"),
            ("seg_02", "Tech billionaire signing a multi-billion dollar long-term Power Purchase Agreement", "BIG TECH CONTRACT"),
            ("seg_03", "High-voltage transmission power lines buzzing directly into modern server compound", "DIRECT CONDUIT"),
            ("seg_04", "Electrical power grid telemetry map glowing orange and red with overload alerts", "GRID AT CAPACITY"),
            ("seg_05", "Futuristic small modular nuclear reactor core glowing with eerie Cherenkov blue light", "ATOMIC FUTURE")
        ]
    },
    {
        "id": "short_10",
        "title": "Bitcoin Short Squeeze: The Liquidity Rebound",
        "badge": "CRYPTO SQUEEZE",
        "hook_text": "$1.2B SHORTS WIPED",
        "script": "Over one point two billion dollars in Bitcoin short positions were just liquidated in a single twenty-four hour cascade. As global central banks prepare for post-midterm monetary easing and bond yields slide, macro liquidity is rushing back into digital assets. Institutional ETF inflows are accelerating as sovereign allocators recognize that liquidity cycles wait for no one.",
        "beats": [
            ("seg_01", "Glowing golden physical Bitcoin token resting on green cryptocurrency price chart", "BITCOIN BREAKOUT"),
            ("seg_02", "Crypto liquidation heat map flashing bright green and yellow as short positions burn", "$1.2B LIQUIDATION"),
            ("seg_03", "Wall Street financial terminal showing massive net inflows into Bitcoin spot ETFs", "ETF INFLOWS"),
            ("seg_04", "Smartphone trading app displaying green candlestick explosion in dark room", "TRADER REBOUND"),
            ("seg_05", "Futuristic cryptographic blockchain ledger connecting global financial capitals", "GLOBAL LIQUIDITY")
        ]
    }
]

print(f"Loaded {len(SHORTS_DATA)} Viral Shorts topics ready for generation.")
