#!/usr/bin/env python3
"""
Complete Script Builder for 12-Minute Master Documentary #2:
THE GREAT FII EXODUS: Dalal Street's ₹3 Lakh Crore War and the Retail Counter-Attack
Generates all 36 Segments x 5 Micro-Beats = 180 Micro-Beats
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "output" / "fii_exodus_documentary" / "chapters_script.py"

SEGMENTS_DATA = [
    # --- ACT 1: THE ₹3 LAKH CRORE FOREIGN FLIGHT (1 - 7) ---
    {
        "id": 1, "act": 1, "title": "The October Red Tide on Dalal Street",
        "timestamp": "0:00 - 0:20",
        "voiceover": "On the trading floor of the Bombay Stock Exchange in Mumbai, terminal screens flashed an unbroken sea of crimson. Foreign institutional investors—the financial titans who had dictated Indian market fortunes for three decades—were smashing the sell button on an industrial scale.",
        "beats": [
            ("DALAL ST CRIMSON", "OCTOBER SHOCK", "Iconic Phiroze Jeejeebhoy Towers of Bombay Stock Exchange at dusk, red market ticker reflection on wet glass facade."),
            ("INSTITUTIONAL DUMP", "ALGO SELL FLOOD", "Close-up of institutional foreign broker executing multi-thousand crore block sell orders on trading terminal."),
            ("TRADERS IN PANIC", "MUMBAI DESKS", "Senior Indian stockbroker in white shirt and tie staring intently at falling Sensex numbers on multi-screen desk."),
            ("RUPEE PRESSURE", "CURRENCY STRAIN", "Reserve Bank of India building in Mumbai bathed in cool shadows as evening traffic passes."),
            ("THE FIRST CRACK", "GLOBAL EXODUS", "High-angle view of Dalal Street pedestrian plaza with financial professionals gathered under street lamps in serious conversation.")
        ]
    },
    {
        "id": 2, "act": 1, "title": "The ₹3 Lakh Crore Sell Button",
        "timestamp": "0:20 - 0:40",
        "voiceover": "Over sixty relentless trading days, foreign funds pulled over three lakh crore rupees out of Indian equities. It was the largest, most concentrated capital flight in Indian history—dwarfing the 2008 global financial crisis and the 2020 pandemic panic combined.",
        "beats": [
            ("RS.3 LAKH CRORE DUMP", "RECORD OUTFLOW", "Massive conceptual vault door in Mumbai cracking open with streams of glowing rupee notes being sucked into dark void."),
            ("DWARFS 2008 PANIC", "UNPRECEDENTED SCALE", "Wall Street and Dalal Street dual clock towers under dramatic storm clouds, lightning arcing between them."),
            ("FOREIGN FUNDS EXIT", "GLOBAL CAPITAL", "A sleek boardroom of a global hedge fund in New York with Manhattan skyline, portfolio managers pointing at India allocation charts."),
            ("SELLING INTENSIFIES", "BLUECHIPS TARGETED", "Extreme close-up of computer keyboard with a finger pressing execute on heavy block equity sales."),
            ("THE RECORD OUTFLOW", "HISTORIC DRAINING", "Bar chart visualization carved into stone monument showing a colossal red column plunging deep below baseline.")
        ]
    },
    {
        "id": 3, "act": 1, "title": "The US 10-Year Treasury Magnet (4.88%)",
        "timestamp": "0:40 - 1:00",
        "voiceover": "Why did foreign capital flee? Because of a magnetic pull thousands of miles away. As strong economic data pushed the United States ten-year Treasury yield toward four point nine percent, risk-free American dollar debt offered yields global asset managers simply could not ignore.",
        "beats": [
            ("US TREASURY 4.88%", "THE GLOBAL MAGNET", "Monumental classical pillars of the US Treasury Department in Washington DC glowing warmly under twilight sky."),
            ("RISK-FREE DOLLARS", "THE SAFE YIELD", "Engraved US Treasury bond certificate resting on dark polished mahogany table next to a brass desk lamp."),
            ("GLOBAL YIELD SPREAD", "CAPITAL REVERSAL", "Digital world map showing glowing golden capital flow streams redirecting from Asia back toward North America."),
            ("FUND MANAGERS CHOOSE", "RISK-FREE RETURN", "American fund manager in sharp suit reviewing bond yield spreadsheets through spectacles in a corner office."),
            ("DOLLAR SUPER-CYCLE", "CURRENCY GRAVITY", "Stylized 3D rendering of the US Dollar symbol in brushed gold towering over global currency icons.")
        ]
    },
    {
        "id": 4, "act": 1, "title": "The Master Title Plate: The Great FII Exodus",
        "timestamp": "1:00 - 1:20",
        "voiceover": "This is the inside story of Dalal Street’s greatest financial war. How foreign funds tried to crash the Indian market, how ten crore retail investors refused to fold, and how the battle sparked an emergency regulatory revolution to scrap capital gains taxes.",
        "beats": [
            ("THE GREAT FII EXODUS", "DALAL STREET WAR", "Monolithic black granite monument on Dalal Street engraved with glowing gold emblem of a Charging Indian Bull."),
            ("RETAIL STANDS FIRM", "10 CRORE TRADERS", "Vast crowd of everyday Indian investors holding up glowing smartphones displaying market charts like a constellation of stars."),
            ("FOREIGN RETREAT", "HEGELIST CRACK", "Foreign hedge fund trading floor in London with traders looking stunned at resilient Indian index charts."),
            ("TAX REVOLUTION", "SEBI DROPS BOMBSHELL", "SEBI Bhavan headquarters in Bandra Kurla Complex Mumbai illuminated against dark midnight sky."),
            ("THE NEW ERA", "INDIAN CAPITAL RISES", "Majestic sunrise over the Mumbai coastal skyline, shimmering golden water reflecting modern financial towers.")
        ]
    },
    {
        "id": 5, "act": 1, "title": "FIIs vs Indian Equities: A Decadal Shift",
        "timestamp": "1:20 - 1:40",
        "voiceover": "Historically, when foreign institutional investors sold, Indian markets collapsed. In 2008, a foreign outflow of forty thousand crore rupees halved the Sensex. Global funds believed they held absolute pricing power over India. They were about to discover that 2026 was not 2008.",
        "beats": [
            ("THE OLD RULES", "FOREIGN PRICING POWER", "Archival-style 35mm view of old open-outcry trading ring on Bombay Stock Exchange with paper tickets strewn across floor."),
            ("2008 CRASH MEMORY", "-50% WIPEOUT", "Dark dramatic representation of the 2008 stock market crash with falling ticker numbers reflected in rain puddles."),
            ("FOREIGN ARROGANCE", "THE ASSUMPTION", "High-end private dining club in Manhattan where Wall Street bankers toast with wine glasses."),
            ("THE PARADIGM BREAK", "NOT 2008 ANYMORE", "Modern digital operations room of the National Stock Exchange of India with automated algorithmic server racks."),
            ("A NEW POWER AWAKENS", "DOMESTIC MUSCLE", "Silhouette of a modern Indian professional woman working on financial portfolio analysis on a laptop in Bangalore.")
        ]
    },
    {
        "id": 6, "act": 1, "title": "The China 'Buy Everything' Diversion",
        "timestamp": "1:40 - 2:00",
        "voiceover": "Compounding the exodus, Beijing launched an unprecedented monetary bazooka. Foreign funds dumped expensive Indian equities trading at twenty-four times earnings to chase dirt-cheap Chinese tech stocks in Hong Kong. It was the great emerging market rotation.",
        "beats": [
            ("BEIJING BAZOOKA", "CHINA STIMULUS", "Imposing Great Hall of the People in Beijing with red flags flapping under dramatic sky."),
            ("HONG KONG SURGE", "ROTATION FEVER", "Hong Kong Victoria Harbour skyline at night with neon financial skyscrapers reflecting across vibrant water."),
            ("INDIA AT 24x P/E", "EXPENSIVE TAG", "Valuation chart carved in white marble comparing high Indian multiples against depressed Asian markets."),
            ("FUND ARBITRAGE", "SELL INDIA BUY CHINA", "Split conceptual frame showing Dalal Street on left and Shanghai Bund on right connected by financial laser lines."),
            ("TEMPORARY CHASE", "HOT MONEY MIGRATION", "Fleet of container ships leaving a bustling Asian shipping terminal at twilight.")
        ]
    },
    {
        "id": 7, "act": 1, "title": "The Currency Pressure: Rupee at ₹85",
        "timestamp": "2:00 - 2:20",
        "voiceover": "As foreign funds converted hundreds of billions of rupees into US dollars to remit overseas, the foreign exchange market buckled. The Indian Rupee slid toward eighty-five per dollar, threatening to trigger imported inflation and spike India’s crude oil import bill.",
        "beats": [
            ("RUPEE AT RS.85", "FOREX TEST", "Close macro shot of crisp new ₹500 currency notes alongside US $100 bills on dark slate surface."),
            ("OIL IMPORT BILL", "INFLATION SQUEEZE", "Oil tanker docking at a Mumbai port terminal under heavy overcast skies, massive crude pipelines."),
            ("RBI INTERVENTION", "WAR CHEST ACTIVATED", "Reserve Bank of India Governor's conference table with silver microphones under formal portrait lighting."),
            ("DOLLAR SQUEEZE", "LIQUIDITY ABSORPTION", "Banking terminal screen showing high-value interbank currency swap transactions in real time."),
            ("THE CURRENCY DEFENSE", "HOLDING THE LINE", "Severe industrial steel vault containing certified physical gold bullion inside RBI central depository.")
        ]
    },

    # --- ACT 2: DALAL STREET'S DOMESTIC FORTRESS (8 - 14) ---
    {
        "id": 8, "act": 2, "title": "The 10 Crore Demat Revolution",
        "timestamp": "2:20 - 2:40",
        "voiceover": "In the past, Indian households hoarded physical gold and bought overpriced urban real estate. But between 2020 and 2026, a structural revolution transformed Indian society. Over ten crore Indians opened digital demat accounts, bringing retail capital directly onto Dalal Street.",
        "beats": [
            ("10 CRORE DEMAT", "CITIZEN INVESTORS", "A young Indian couple in an apartment living room reviewing mutual fund portfolio on a tablet with tea on the table."),
            ("FROM GOLD TO STOCKS", "EQUITY CULTURE", "Traditional Indian gold jewellery resting beside a modern smartphone displaying a stock portfolio graph."),
            ("SMARTPHONE TRADING", "TIER-2 AND TIER-3", "A shopkeeper in Jaipur checking live Nifty stock quotes on his mobile phone between customers."),
            ("FINANCIAL INCLUSION", "THE NEW MIDDLE CLASS", "Modern metro train speeding through Mumbai or Delhi with young commuters glancing at financial news."),
            ("MASSIVE SCALE", "UNPRECEDENTED INFLOW", "Graphic visualization of millions of small digital streams converging into a massive roaring golden river.")
        ]
    },
    {
        "id": 9, "act": 2, "title": "The ₹25,000 Crore Monthly SIP Tsunami",
        "timestamp": "2:40 - 3:00",
        "voiceover": "Every single month, on the first and fifth, automated Systematic Investment Plans execute like clockwork. Over twenty-five thousand crore rupees—three billion dollars—flows relentlessly into domestic mutual funds, unaffected by headlines, geopolitical wars, or foreign panics.",
        "beats": [
            ("RS.25,000 CR SIP", "THE MONTHLY TSUNAMI", "A massive modern bank automated clearing house server room with blue and green server rack status lights."),
            ("AUTOMATED INFLOW", "THE DISCIPLINED ARMY", "Calendar page showing the 1st of the month circled in gold ink with an automated bank mandate notification."),
            ("THREE BILLION DOLLARS", "EVERY 30 DAYS", "Stacks of currency notes moving through a high-speed counting machine in a major Indian banking vault."),
            ("UNSTOPPABLE MOMENTUM", "IMMUNE TO PANIC", "Close-up of an Indian salaried professional receiving monthly salary credit and automated mutual fund deduction SMS."),
            ("THE FINANCIAL SHIELD", "DOMESTIC BEDROCK", "A heavy polished bronze shield standing upright on Dalal Street, deflecting arrows of red ticker tape.")
        ]
    },
    {
        "id": 10, "act": 2, "title": "DIIs Become the Buyer of Last Resort",
        "timestamp": "3:00 - 3:20",
        "voiceover": "Armed with this relentless domestic cash tsunami, Indian mutual funds and institutional managers did something unprecedented: every time foreign institutional investors dumped ten thousand crores, domestic institutions stepped forward and bought twelve thousand crores.",
        "beats": [
            ("DII COUNTER-ATTACK", "BUYERS OF LAST RESORT", "Sprawling trading floor of a top Indian mutual fund asset management company in BKC Mumbai."),
            ("EVERY DUMP ABSORBED", "10,000 CR BUY ORDERS", "Senior Indian fund manager pointing at large screen showing foreign sell orders being instantly filled by domestic bids."),
            ("INSTITUTIONAL DUEL", "EAST MEETS WEST", "Dramatic artistic conceptual painting of two charging bulls clashing horns on a marble floor in high contrast."),
            ("CONFIDENCE IN INDIA", "LONG-TERM HORIZON", "Conference room in Mumbai where domestic fund CIO addresses team with confident hand gesture."),
            ("THE NET POSITION", "DOMESTIC DOMINANCE", "Digital scoreboard showing foreign net selling alongside a larger domestic net buying total in green.")
        ]
    },
    {
        "id": 11, "act": 2, "title": "Absorbing the Shock Without a Crash",
        "timestamp": "3:20 - 3:40",
        "voiceover": "In 2008, a foreign exit caused a fifty percent crash. In 2026, after three lakh crore rupees in foreign selling, the benchmark Nifty corrected barely six percent. Wall Street risk models broke down: the Indian market had developed structural immunity.",
        "beats": [
            ("ONLY -6% DIP", "STRUCTURAL IMMUNITY", "Sensex index chart on Bloomberg terminal showing shallow controlled pullback despite massive volume spike."),
            ("WALL ST MODELS FAIL", "PREDICTED -30% CRASH", "Hedge fund quant analyst in London staring at a red mathematical model with an ERROR flag on screen."),
            ("MARKET ABSORPTION", "THE DEEP POCKETS", "A giant deep reservoir absorbing a massive wave of water without overflowing, calm surface."),
            ("RETAIL BUYING DIPS", "EVERY PULLBACK BOUGHT", "Coffee shop in Connaught Place New Delhi where young professionals discuss buying blue-chip shares during market dips."),
            ("THE NEW STABILITY", "WORLD-CLASS RESILIENCE", "A massive concrete suspension bridge in Mumbai (Bandra-Worli Sea Link) standing firm in heavy monsoon seas.")
        ]
    },
    {
        "id": 12, "act": 2, "title": "LIC and the Sovereign Balance Sheet",
        "timestamp": "3:40 - 4:00",
        "voiceover": "Behind the mutual funds stood India’s sovereign financial leviathan: the Life Insurance Corporation of India. With fifty lakh crore rupees in assets under management, LIC stepped in with strategic counter-cyclical buying, acquiring distressed bluechips at multi-year valuation discounts.",
        "beats": [
            ("LIC THE LEVIATHAN", "RS.50 LAKH CR ASSETS", "Iconic headquarters of Life Insurance Corporation of India in Mumbai under dramatic twilight lighting."),
            ("SOVEREIGN BUYING", "STRATEGIC STABILIZER", "Massive underground vault containing corporate bond and equity ledgers inside an institutional vault."),
            ("COUNTER-CYCLICAL", "BUYING THE PANIC", "Senior government investment committee seated in deep deliberation in New Delhi North Block."),
            ("DISCOUNTED BLUECHIPS", "VALUE AT SCALE", "Stack of blue-chip share certificates on dark oak table under single spotlight."),
            ("THE ANCHOR OF DALAL ST", "STATE-BACKED STRENGTH", "Heavy anchor resting on polished granite floor of the National Stock Exchange.")
        ]
    },
    {
        "id": 13, "act": 2, "title": "The Wealth Creation Mindset of Modern India",
        "timestamp": "4:00 - 4:20",
        "voiceover": "This resilience was not an accident; it reflected a cultural paradigm shift. An entire generation of young Indians realized that the fastest path to middle-class wealth was not fixed deposits or physical assets, but compounding equity ownership in India’s leading corporations.",
        "beats": [
            ("CULTURAL SHIFT", "THE COMPOUNDING MINDSET", "Father and grown son in an Indian living room looking at compounding investment charts together on a laptop."),
            ("FDs ARE DEAD", "BEATING INFLATION", "Old passbook and fixed deposit certificate next to a sleek digital investment portfolio app on phone."),
            ("ASPIRATIONAL INDIA", "OWNING THE BULL", "Crowded bustling street of Pune or Hyderabad filled with modern shops, cafes, and ambitious tech workers."),
            ("THE NEW PATRIOTS", "INVESTING IN HOME", "Young entrepreneur in Bangalore looking out of startup glass office over bustling city skyline at sunrise."),
            ("COMPOUNDING REALITY", "20-YEAR HORIZON", "Majestic banyan tree in an Indian courtyard with sprawling roots, sunlight filtering through canopy.")
        ]
    },
    {
        "id": 14, "act": 2, "title": "How India Decoupled from Emerging Market Panics",
        "timestamp": "4:20 - 4:40",
        "voiceover": "For decades, Wall Street lumped India into the emerging market basket alongside Argentina, Turkey, and South Africa. But as global capital fled emerging markets in late 2026, India stood alone—a domestic-demand-driven economic fortress with sovereign political stability.",
        "beats": [
            ("DECOUPLING PROVED", "NO LONGER TYPICAL EM", "World map highlighting India in vibrant glowing saffron gold while other emerging markets fade in grey shadows."),
            ("DOMESTIC DEMAND", "1.4 BILLION CONSUMERS", "Vibrant, crowded Indian retail shopping mall during Diwali festival with thousands of shoppers and bright lights."),
            ("POLITICAL STABILITY", "CONTINUITY ASSURED", "Rashtrapati Bhavan in New Delhi illuminated at night under majestic illuminated fountains."),
            ("WALL ST CONCESSION", "INDIA AS STANDALONE", "New York investment bank research report on desk titled 'INDIA: THE STANDALONE ALLOCATION'."),
            ("THE FORTRESS WALLS", "INDEPENDENT DESTINY", "Historic red sandstone ramparts of Red Fort in Delhi bathed in warm sunset glow.")
        ]
    },

    # --- ACT 3: THE VALUATION CHASM & TAX FRICTION (15 - 21) ---
    {
        "id": 15, "act": 3, "title": "Nifty at 23x P/E: The Premium Debate",
        "timestamp": "4:40 - 5:00",
        "voiceover": "Yet foreign institutional managers pointed to an undeniable friction point: valuation. Even after the pullback, the Nifty 50 traded at twenty-three times forward earnings, compared to twelve times for China and ten times for Brazil. Was India a premium market or a valuation bubble?",
        "beats": [
            ("23x P/E RATIO", "THE VALUATION DEBATE", "Analytical stock market valuation multiple bar chart comparison displayed on an iPad tablet."),
            ("PREMIUM MULTIPLE", "GROWTH HAS A PRICE", "Luxury jeweler inspecting a flawless diamond through an eyeglass in a Mumbai jewelry boutique."),
            ("GLOBAL SKEPTICS", "EXPENSIVE TICKER", "Boardroom in Singapore where sovereign wealth managers debate Asian country allocations."),
            ("EARNINGS QUALITY", "REAL ROE COUNTS", "Corporate auditor in Chennai reviewing verified clean balance sheets of top Indian conglomerates."),
            ("THE CROSSROADS", "JUSTIFYING THE PRICE", "A fork in an Indian national highway stretching towards mist-covered green hills at dawn.")
        ]
    },
    {
        "id": 16, "act": 3, "title": "The 12.5% LTCG Tax Backlash",
        "timestamp": "5:00 - 5:20",
        "voiceover": "Beyond valuations, foreign funds faced a bitter policy grievance: the 2024 budget decision to increase Long-Term Capital Gains tax to twelve point five percent and Short-Term Capital Gains to twenty percent. For international asset managers with fiduciary duties, the tax bite was punitive.",
        "beats": [
            ("12.5% LTCG TAX", "POLICY FRICTION", "Official government budget document in New Delhi stamped with Finance Ministry emblem and tax rates."),
            ("FII COMPLAINT", "DOUBLE TAXATION", "Foreign hedge fund lawyer in London marking red pen notes on Indian foreign portfolio investment regulations."),
            ("TAX BITE SHAVES YIELDS", "POST-TAX HURDLE", "A stack of golden coins with a metal blade cleanly slicing the top twenty percent off."),
            ("CAPITAL SEEKS LOW FRICTION", "GLOBAL COMPETITION", "Dubai International Financial Centre modern glass towers illuminated under clear night sky."),
            ("THE OUTFLOW ACCELERATOR", "TAX-DRIVEN EXITS", "Financial terminal showing tax deductions on portfolio redemptions in prominent red text.")
        ]
    },
    {
        "id": 17, "act": 3, "title": "FII Friction: Tax Clarity vs US Yields",
        "timestamp": "5:20 - 5:40",
        "voiceover": "When US Treasuries yielded nearly five percent in clean dollars with zero foreign tax withholding, paying twelve point five percent tax on Indian equities while bearing Rupee currency depreciation made India a difficult sell to conservative American pension trustees.",
        "beats": [
            ("CLEAN 5% DOLLARS", "THE SAFE ALTERNATIVE", "Calm boardroom of a major US public pension fund in California overlooking the Pacific coast."),
            ("PENSION TRUSTEES", "FIDUCIARY DUTY", "Grey-haired pension fund trustees seated around boardroom table reviewing risk allocation tables."),
            ("CURRENCY + TAX", "DOUBLE DRAG", "Two heavy iron weights pulling down a balance scale labeled 'CURRENCY DRAG' and 'TAX RATE'."),
            ("THE RISK EQUATION", "HARD MATH", "Chalkboard in an academic economics hall filled with complex Sharpe ratio and currency risk calculations."),
            ("CAPITAL RETREATS", "PATH OF LEAST RESISTANCE", "Silhouetted passenger jet taking off into a dramatic golden sunset sky.")
        ]
    },
    {
        "id": 18, "act": 3, "title": "SEBI's Internal Deliberations in Mumbai",
        "timestamp": "5:40 - 6:00",
        "voiceover": "Inside the fortified glass headquarters of the Securities and Exchange Board of India in Mumbai, senior leadership confronted the reality. While domestic retail inflows had saved the market from collapse, long-term capital formation required deep global sovereign pools.",
        "beats": [
            ("SEBI BHAVAN MUMBAI", "INTERNAL CRISIS ROOM", "Exterior of SEBI Bhavan in BKC Mumbai with its curved modern architectural glass facade at night."),
            ("REGULATORY HUDDLE", "LOOKING AT DATA", "Senior SEBI officials seated around circular conference table examining confidential flowcharts."),
            ("NEED GLOBAL POOLS", "BEYOND RETAIL", "Large digital display showing international sovereign wealth fund allocations by continent."),
            ("CAPITAL FORMATION", "INFRASTRUCTURE BILLIONS", "Construction site of a major Indian high-speed rail or highway corridor under bright worklights."),
            ("THE DECISION POINT", "TIME TO REFORM", "SEBI Chairman's wooden desk with a single uncap fountain pen resting beside an open memorandum.")
        ]
    },
    {
        "id": 19, "act": 3, "title": "The Secret High-Level Finance Ministry Memo",
        "timestamp": "6:00 - 6:20",
        "voiceover": "In early November, an internal confidential policy note traveled from Mumbai to North Block in New Delhi. The recommendation was radical: to restore India's global competitiveness and halt the currency drain, India needed to dismantle tax barriers for foreign institutional capital.",
        "beats": [
            ("CONFIDENTIAL NOTE", "MUMBAI TO DELHI", "A sealed official government dossier bound with red ceremonial ribbon resting on an executive desk."),
            ("NORTH BLOCK DELIBERATION", "MINISTRY OF FINANCE", "Imposing sandstone arches of North Block Central Secretariat in New Delhi under moody autumn skies."),
            ("RESTORE COMPETITIVENESS", "HALT DRAIN", "Civil servants in formal Indian attire walking through historic high-ceiling corridors carrying official files."),
            ("MINISTER REVIEWS", "THE STRATEGIC CHOICE", "High-level ministerial office in New Delhi with national emblem of India visible on mahogany wall."),
            ("POLICY TURNING POINT", "THE BOLD GAMBIT", "A single chess grandmaster move illuminated by warm dramatic directional spotlighting.")
        ]
    },
    {
        "id": 20, "act": 3, "title": "Proposal to Scrap 12.5% Tax for Foreign Capital",
        "timestamp": "6:20 - 6:40",
        "voiceover": "The bombshell proposal leaked: SEBI had formally recommended abolishing the twelve point five percent Long-Term Capital Gains tax on designated foreign portfolio investments, or slashing it back to zero for sovereign and pension funds willing to lock capital into Indian growth.",
        "beats": [
            ("SCRAP LTCG TAX", "SEBI'S BOMBSHELL", "Front page of a leading financial daily newspaper with bold headlines in black ink: 'LTCG SCRAP PROPOSED'."),
            ("ZERO TAX FOR PENSIONS", "SOVEREIGN INCENTIVE", "Gleaming conference hall of an international financial summit with national flags displayed."),
            ("EQUAL PLAYING FIELD", "MATCHING DUBAI & SINGAPORE", "Modern skyscrapers of GIFT City Gujarat reflecting in calm water at sunset."),
            ("THE TAX LEAK", "MARKET CHATTER", "Trading desk in Mumbai with multiple brokers frantically typing messages on secure messaging apps."),
            ("THE MULTI-BILLION BET", "GLOBAL ATTENTION", "High-angle view of a bustling Indian equity trading floor suddenly halting to read screens.")
        ]
    },
    {
        "id": 21, "act": 3, "title": "Dalal Street Rumors Igniting",
        "timestamp": "6:40 - 7:00",
        "voiceover": "Within minutes, the leak reverberated across trading desks from Churchgate to Bandra. If the Finance Ministry approved the reform ahead of the union budget, hundreds of billions of dollars in foreign institutional capital parked in Singapore and London would flood back into Indian bluechips.",
        "beats": [
            ("RUMORS EXPLODE", "DESKS ON FIRE", "Panicked excitement on Dalal Street trading desks, brokers picking up landline phones and pointing at news tickers."),
            ("SINGAPORE & LONDON", "CAPITAL ON STANDBY", "View from an office window in Mayfair London overlooking rainy dusk streets as traders huddle around monitors."),
            ("HUNDREDS OF BILLIONS", "WAITING ON SIDELINES", "Vast container of golden liquid ready to pour over a dry fertile plain, conceptual visualization."),
            ("THE BUZZ IN BKC", "PRIVATE BANKERS ALERT", "Bandra Kurla Complex commercial district in Mumbai with glowing corporate glass offices at night."),
            ("THE TINDERBOX", "READY TO IGNITE", "Close-up of a match being struck against a matchbox, bright flame flaring up in dark studio.")
        ]
    },

    # --- ACT 4: THE ₹14,900 CRORE U-TURN (22 - 28) ---
    {
        "id": 22, "act": 4, "title": "The November Buying Blitz",
        "timestamp": "7:00 - 7:20",
        "voiceover": "On November 6th, the reversal arrived with explosive force. Global macro hedge funds, fearing they would be caught short in the world’s fastest-growing major economy, reversed their positions simultaneously in one of the most violent U-turns in modern market history.",
        "beats": [
            ("THE U-TURN ARRIVES", "NOVEMBER 6 BLITZ", "Trading screens turning bright green in unison as buying volume spikes to off-the-chart levels."),
            ("HEDGE FUNDS REVERSE", "COVERING SHORTS", "Global macro portfolio manager in Hong Kong slamming phone receiver down and ordering immediate equity buys."),
            ("THE VIOLENT SPIKE", "PRICE BREAKOUT", "Candlestick chart of Nifty 50 shooting vertically upward through multiple resistance bands on large display."),
            ("EXPLOSIVE INFLOWS", "FOREIGN BUY ORDERS", "Fiber-optic cables pulsing with brilliant electric blue light representing high-speed trade execution."),
            ("MUMBAI TRADERS STUNNED", "NO SELLERS FOUND", "Brokers on Mumbai trading desk cheering and shouting as buy orders overwhelm market depth.")
        ]
    },
    {
        "id": 23, "act": 4, "title": "₹14,900 Crore Injected in One Session",
        "timestamp": "7:20 - 7:40",
        "voiceover": "By the closing bell, the official National Stock Exchange provisional figures revealed the staggering scale: foreign institutional investors had bought nearly fifteen thousand crore rupees worth of Indian equities in a single trading session—the largest single-day purchase in seven months.",
        "beats": [
            ("RS.14,900 CR INFLOW", "7-MONTH RECORD", "Official NSE provisional data sheet displayed on screen with massive green positive net figure."),
            ("THE SINGLE-DAY RECORD", "BUYING FRENZY", "BSE ticker tower in Mumbai displaying record positive net institutional figures in glowing emerald green."),
            ("THE CASH FLOOD", "MARKET ABSORPTION", "Graphic visualization of a golden tsunami wave rolling smoothly over a map of Indian financial exchanges."),
            ("CELEBRATION ON STREET", "BEARS CRUSHED", "Indian stock market traders embracing and high-fiving on a modern trading floor in Mumbai."),
            ("THE HISTORIC DAY", "NOVEMBER MILESTONE", "Front page of a financial newspaper being printed at high speed on industrial printing presses.")
        ]
    },
    {
        "id": 24, "act": 4, "title": "Short Squeeze on Index Futures",
        "timestamp": "7:40 - 8:00",
        "voiceover": "The violent influx triggered a textbook short squeeze. Proprietary trading desks and foreign quant funds that had accumulated massive bearish derivative positions were forced to buy back index futures at any price, sending the Nifty surging over four hundred points in hours.",
        "beats": [
            ("SHORT SQUEEZE", "BEAR TRAP SPRUNG", "Mechanical bear trap snapping violently shut on an iron trading desk in dramatic slow motion."),
            ("+400 POINT SURGE", "INDEX VERTICAL", "Electronic digital board at the National Stock Exchange displaying Nifty index climbing minute by minute."),
            ("FORCED BUYBACKS", "FUTURES LIQUIDATION", "Derivatives trader sweating profusely as stop-loss orders trigger automatically in rapid succession."),
            ("THE CASCADE", "BEARS IN FULL RETREAT", "A line of falling red dominoes suddenly stopped by a solid gold barrier, reversing direction."),
            ("DERIVATIVES EXPLODE", "EXPIRY CARNAGE", "View through a window of the Mumbai skyline at dusk as lightning illuminates storm clouds.")
        ]
    },
    {
        "id": 25, "act": 4, "title": "Large-Cap Banking & IT Surge",
        "timestamp": "8:00 - 8:20",
        "voiceover": "The capital did not flow into speculative penny stocks; it flooded into India’s heavyweight engine: HDFC Bank, ICICI Bank, State Bank of India, Infosys, and Reliance. The bluechips that foreign funds had spent sixty days dumping were repurchased at a premium.",
        "beats": [
            ("BANKING LEADERSHIP", "HDFC & ICICI LEAD", "Headquarters of HDFC Bank and ICICI Bank in Mumbai illuminated against twilight sky."),
            ("BLUECHIP ENGINES", "RELIANCE & INFOSYS", "Modern high-tech software campus of Infosys in Bangalore with manicured lawns and glass architecture."),
            ("BUYING AT A PREMIUM", "THE PRICE OF HESITATION", "Bank teller counting clean stacks of new Indian rupee notes with precision."),
            ("HEAVYWEIGHT RALLY", "INDEX MOVERS", "Architectural column of an Indian commercial bank building with neoclassical stonework and bronze plaques."),
            ("THE FOUNDATIONAL ASSETS", "INSTITUTIONAL CORE", "Heavy industrial gears turning smoothly inside an Indian steel or manufacturing plant.")
        ]
    },
    {
        "id": 26, "act": 4, "title": "Panic Among Short Sellers",
        "timestamp": "8:20 - 8:40",
        "voiceover": "Short sellers who had boasted on social media about the imminent collapse of the Indian economy deleted their posts. The liquidity trap had closed: those who tried to short the fastest-growing major economy in the world learned a brutal, expensive lesson in Dalal Street resilience.",
        "beats": [
            ("BEARS CRUSHED", "SOCIAL MEDIA SILENCE", "A smartphone screen displaying a financial influencer account with posts being rapidly deleted."),
            ("THE EXPENSIVE LESSON", "EXPENSIVE TO SHORT INDIA", "An empty wallet resting open on a desk beside an expensive red fountain pen."),
            ("NEVER SHORT INDIA", "THE GOLDEN RULE", "Famous wall plaque in an Indian investment bank quoting: 'NEVER SHORT THE INDIAN BULL'."),
            ("LIQUIDATION COMPLETE", "ACCOUNTS CLEANSED", "A brokerage account statement showing liquidation balances highlighted in red markers."),
            ("VICTORY FOR LONGS", "PATIENCE REWARDED", "Indian retail investor smiling calmly as he views his compounding investment balance on phone.")
        ]
    },
    {
        "id": 27, "act": 4, "title": "Global Funds Realize They Are Underweight",
        "timestamp": "8:40 - 9:00",
        "voiceover": "Global chief investment officers faced an urgent mathematical dilemma: India represented over twenty percent of emerging market gross domestic product, but foreign portfolios held less than fifteen percent exposure. They were dangerously underweight, and career risk was kicking in.",
        "beats": [
            ("UNDERWEIGHT DILEMMA", "CAREER RISK", "Senior global portfolio strategist in London leaning back in his leather chair with worried expression."),
            ("20% OF EM GDP", "CANNOT IGNORE", "Pie chart of emerging market economic output highlighting India's expanding slice in bright gold."),
            ("ALLOCATION MANDATE", "MUST BUY BACK", "Formal investment committee charter document on boardroom table with red checkmarks."),
            ("THE CHASE BEGINS", "FEAR OF MISSING OUT", "Traders in a global asset management firm gathered around an analyst presenting India GDP growth charts."),
            ("THE REALIGNMENT", "TRILLIONS REBALANCED", "Modern globe spinning slowly on a bronze stand inside a prestigious private library.")
        ]
    },
    {
        "id": 28, "act": 4, "title": "Dalal Street's Counter-Attack Complete",
        "timestamp": "9:00 - 9:20",
        "voiceover": "The war was won. In sixty days, foreign funds had thrown their worst at Dalal Street: dumping three lakh crore rupees, driving up bond yields, and exploiting currency pressure. And Dalal Street had absorbed it, held its ground, and rallied to new highs.",
        "beats": [
            ("THE WAR WON", "DALAL STREET PREVAILS", "Triumphant wide shot of Dalal Street in Mumbai bathed in bright golden morning sunlight, traders walking with pride."),
            ("WORST WAS THROWN", "HELD THE GROUND", "A solid stone fortress wall bearing minor battle scars but standing completely unbroken against sky."),
            ("NEW HIGHS IN SIGHT", "NIFTY REBOUND", "Digital stock chart showing Nifty climbing above previous all-time highs with bold green trend line."),
            ("THE TRIUMPH", "DOMESTIC MUSCLE PROVED", "Historic statue of the Bull outside BSE adorned with traditional marigold garlands in celebration."),
            ("A HISTORIC PIVOT", "AUTONOMOUS DESTINY", "The tricolor Indian national flag waving majestically against a clear blue sky over Mumbai skyline.")
        ]
    },

    # --- ACT 5: THE NEW WORLD ORDER FOR INDIAN CAPITAL (29 - 36) ---
    {
        "id": 29, "act": 5, "title": "No Longer Hostage to Foreign Flows",
        "timestamp": "9:20 - 9:40",
        "voiceover": "For the first time in modern Indian financial history, the stock market is no longer hostage to foreign institutional whims. India’s destiny is financed by Indian domestic capital, giving the nation monetary sovereignty that emerging markets could previously only dream of.",
        "beats": [
            ("MONETARY SOVEREIGNTY", "NO LONGER HOSTAGE", "A heavy broken iron chain lying on a polished marble floor, links shattered in two."),
            ("FINANCED AT HOME", "DOMESTIC SOVEREIGNTY", "View of modern Indian financial institutions in Mumbai standing proudly under open sunny skies."),
            ("INDIAN WEALTH DEPLOYED", "HOMELAND CAPITAL", "High-angle view of a modern Indian bank branch bustling with everyday citizens depositing and investing."),
            ("A GLOBAL PRECEDENT", "EMERGING MARKET BLUEPRINT", "International economic policy conference hall with Indian delegates speaking at main podium."),
            ("SOVEREIGN INDEPENDENCE", "THE NEW ERA", "A majestic stone archway overlooking the Arabian Sea at Gateway of India Mumbai at sunrise.")
        ]
    },
    {
        "id": 30, "act": 5, "title": "The Retail Investor's New Power",
        "timestamp": "9:40 - 10:00",
        "voiceover": "The unsung hero of this war was the ordinary Indian citizen. The school teacher in Lucknow, the doctor in Kochi, the coder in Hyderabad, and the shopkeeper in Ahmedabad whose monthly five-thousand-rupee SIP stood firm while Wall Street hedge funds panicked.",
        "beats": [
            ("THE UNSUNG HEROES", "ORDINARY CITIZENS", "A diverse montage portrait of everyday Indian citizens: teacher, doctor, engineer, and merchant smiling with quiet pride."),
            ("THE 5000 RUPEE SIP", "BRICK BY BRICK", "Close-up of a modest Indian bank passbook showing disciplined monthly mutual fund investments over five years."),
            ("PAN-INDIA SOLIDARITY", "FROM KASHMIR TO KANYAKUMARI", "Cinematic landscape transition across India: snow-capped mountains of north to lush green backwaters of south."),
            ("WEALTH CREATION FOR ALL", "DEMOCRATIZED CAPITAL", "Young Indian family moving into a bright new apartment, father hanging a framed picture on wall."),
            ("THE REAL STRENGTH", "THE PEOPLE'S BULL", "Close-up of the determined bronze eye of the Charging Bull statue in Mumbai reflecting bright sunlight.")
        ]
    },
    {
        "id": 31, "act": 5, "title": "India's $5 Trillion Market Cap Milestone",
        "timestamp": "10:00 - 10:20",
        "voiceover": "With the counter-attack complete, the combined market capitalization of Indian listed companies crossed five trillion dollars, cementing India’s position as the fourth-largest equity market on Earth, rapidly closing the gap with Japan and Hong Kong.",
        "beats": [
            ("$5 TRILLION MILESTONE", "4TH LARGEST ON EARTH", "A monumental golden trophy or commemorative plaque reading '$5 TRILLION MARKET CAP' inside BSE atrium."),
            ("CLOSING THE GAP", "CHASING JAPAN & HK", "Global financial ranking board showing India ascending past historic benchmarks into elite top tier."),
            ("NATIONAL PRIDE", "ECONOMIC SUPERPOWER", "Illuminated modern skyline of BKC Mumbai at night with high-speed expressways and gleaming glass towers."),
            ("GLOBAL CAPITAL WATCHES", "IMPOSSIBLE TO IGNORE", "International financial news studio in London broadcasting live market report on India's $5T economy."),
            ("THE ACCELERATION", "TRAJECTORY TO $10T", "A futuristic high-speed Vande Bharat express train cutting across a modern elevated viaduct across green plains.")
        ]
    },
    {
        "id": 32, "act": 5, "title": "Geopolitical Capital: Why Funds Must Return",
        "timestamp": "10:20 - 10:40",
        "voiceover": "Geopolitics dictates financial destiny. With Western powers actively derisking supply chains away from adversarial rivals, India stands as the only major democracy capable of delivering seven percent real annual GDP growth for the next two decades.",
        "beats": [
            ("GEOPOLITICAL ALLY", "THE CHINA+1 DESTINATION", "World leaders shaking hands at a major international summit with Indian Prime Minister at center."),
            ("7% GDP GROWTH", "WORLD'S BRIGHT SPOT", "Modern automated electronics manufacturing assembly line in Tamil Nadu assembling smartphones at speed."),
            ("DERISKING FROM RIVALS", "GLOBAL SUPPLY SHIFT", "Massive shipping container terminal in Nhava Sheva Mumbai operating 24-7 with automated cranes."),
            ("LONG-TERM DESTINY", "20-YEAR HORIZON", "Architectural model of a mega-city smart infrastructure project with green parks and modern transit."),
            ("THE INEVITABLE INFLOW", "CAPITAL CANNOT RESIST", "A powerful river breaking through a narrow canyon gorge, flowing into a vast fertile valley.")
        ]
    },
    {
        "id": 33, "act": 5, "title": "The Risks Ahead: Oil, Dollar, Global War",
        "timestamp": "10:40 - 11:00",
        "voiceover": "Victory does not mean complacency. Dalal Street still navigates significant global headwinds: crude oil price spikes in the Middle East, the structural strength of the US Dollar, and ongoing geopolitical tensions across trade corridors.",
        "beats": [
            ("GLOBAL HEADWINDS", "CRUDE OIL & WAR", "Oil platform offshore at night with flare stacks burning bright orange against dark choppy ocean waves."),
            ("THE STRONG DOLLAR", "FEDERAL RESERVE POWER", "Federal Reserve Eccles Building in Washington DC bathed in cool architectural spotlighting."),
            ("GEOPOLITICAL TENSION", "TRADE STRAINS", "Naval destroyers cruising in formation through strategic international straits at dusk."),
            ("INFLATION VIGILANCE", "RBI WATCHFUL EYE", "Reserve Bank of India Monetary Policy Committee seated in formal deliberation in Mumbai."),
            ("PRUDENCE REQUIRED", "RISK MANAGEMENT", "Captain of a large cargo vessel peering through bridge binoculars into foggy stormy seas.")
        ]
    },
    {
        "id": 34, "act": 5, "title": "Strategic Asset Allocation in the New Era",
        "timestamp": "11:00 - 11:20",
        "voiceover": "In this new financial reality, successful investing requires discipline. Seasoned wealth managers recommend a balanced strategy: overweight domestic consumption and manufacturing leaders, maintain tactical gold hedges, and view foreign selling as buying opportunities.",
        "beats": [
            ("BALANCED DISCIPLINE", "ASSET ALLOCATION", "Sleek wooden desk with a balanced portfolio layout: physical gold coins, equity documents, and bond certificates."),
            ("DOMESTIC CHAMPIONS", "INFRA & CONSUMPTION", "A massive modern Indian cement, steel, and renewable solar farm facility under brilliant blue skies."),
            ("GOLD AS MONETARY SHIELD", "TACTICAL HEDGE", "Pure 24-karat gold biscuits bearing official mint stamps resting on black velvet cloth."),
            ("BUYING FOREIGN DUMPS", "THE SMART STRATEGY", "Professional portfolio manager checking valuation metrics and placing limit buy orders calmly."),
            ("THE COMPOUNDING PATH", "PATIENCE IS KING", "Hourglass on a mahogany desk with fine white sand trickling steadily into bottom chamber.")
        ]
    },
    {
        "id": 35, "act": 5, "title": "Lessons from the Great Foreign Flight",
        "timestamp": "11:20 - 11:40",
        "voiceover": "The greatest lesson of the October 2026 foreign flight is simple: never underestimate the financial depth of a nation of one point four billion people determined to build their own prosperity. The foreign funds came, they sold, and India bought.",
        "beats": [
            ("NEVER UNDERESTIMATE", "1.4 BILLION CITIZENS", "Vast panoramic aerial shot of the bustling Marine Drive coastal boulevard in Mumbai at sunset."),
            ("THE FOREIGN LESSON", "INDIA BOUGHT", "Split screen showing foreign funds' sell tickets fading into dust while Indian retail receipts shine bright."),
            ("SELF-RELIANCE PROVED", "ATMANIRBHAR BHARAT", "Modern high-tech defense and aerospace engineering lab in Hyderabad with engineers inspecting satellite parts."),
            ("WEALTH CREATION LEGACY", "A GENERATION REWARDED", "Grandfather holding grandchild's hand, pointing proudly toward a modern city skyline at dusk."),
            ("THE MATURE MARKET", "DALAL ST STANDS TALL", "Front facade of Bombay Stock Exchange illuminated in vibrant saffron, white, and green lights.")
        ]
    },
    {
        "id": 36, "act": 5, "title": "Final Verdict: The Rise of the Indian Bull",
        "timestamp": "11:40 - 12:00",
        "voiceover": "The battle for Dalal Street has redefined the global financial order. Foreign institutional capital will return—not as masters, but as participants in the greatest wealth creation story of the twenty-first century. The Indian Bull has taken the field, and it will not be stopped.",
        "beats": [
            ("THE NEW ORDER", "MASTERS NO MORE", "Majestic bronze Charging Bull statue on Dalal Street gleaming under sunrise, surrounded by clear open skies."),
            ("PARTICIPANTS IN GROWTH", "GLOBAL CAPITAL RETURNS", "Diverse group of international and Indian institutional investors shaking hands on trading floor."),
            ("THE 21ST CENTURY", "INDIA'S DECADE", "Panoramic cityscape of modern Mumbai financial district stretching to horizon under golden sunlight."),
            ("THE BULL PRINT", "SUBSCRIBE & DOMINATE", "Signature high-CTR YouTube end-screen: sleek dark 3D gold embossed channel logo '@TheBullPrint'."),
            ("FINAL GLORY", "UNSTOPPABLE MOMENTUM", "Silhouetted Indian Bull statue standing proudly atop a mountain peak as the morning sun rises behind it.")
        ]
    }
]

def generate_script():
    print(f"Building complete chapters_script.py for Doc #2 with {len(SEGMENTS_DATA)} segments...")
    lines = [
        "#!/usr/bin/env python3",
        '"""',
        "THE GREAT FII EXODUS: Dalal Street's ₹3 Lakh Crore War and the Retail Counter-Attack",
        f"12-Minute Master Documentary ({len(SEGMENTS_DATA)} Segments x 5 Micro-Beats = {len(SEGMENTS_DATA)*5} Micro-Beats)",
        "Channel: The Bull Print (@thebullprint)",
        "Narrator: en-US-ChristopherNeural (-2Hz Pitch)",
        '"""',
        "",
        "SEGMENTS = ["
    ]
    for seg in SEGMENTS_DATA:
        lines.append("    {")
        lines.append(f'        "id": {seg["id"]},')
        lines.append(f'        "act": {seg["act"]},')
        lines.append(f'        "title": {json.dumps(seg["title"])},')
        lines.append(f'        "timestamp": {json.dumps(seg["timestamp"])},')
        lines.append(f'        "voiceover": {json.dumps(seg["voiceover"])},')
        lines.append('        "beats": [')
        for b_idx, (anchor, badge, vis_desc) in enumerate(seg["beats"], start=1):
            t_start = (b_idx - 1) * 4.0
            t_end = b_idx * 4.0
            prompt = (
                f"Cinematic 35mm film photograph, wide 16:9 ratio. {vis_desc} "
                "Moody chiaroscuro lighting, deep shadows, authentic film grain, documentary realism. "
                "Completely clean frame with zero text, zero words, zero letters, zero typography, zero numbers, zero watermarks."
            )
            lines.append("            {")
            lines.append(f'                "beat_num": {b_idx},')
            lines.append(f'                "timing": "{t_start:.1f}s - {t_end:.1f}s",')
            lines.append(f'                "visual_description": {json.dumps(vis_desc)},')
            lines.append(f'                "anchor_text": {json.dumps(anchor)},')
            lines.append(f'                "badge_text": {json.dumps(badge)},')
            lines.append(f'                "prompt": {json.dumps(prompt)}')
            lines.append("            }" + ("," if b_idx < 5 else ""))
        lines.append("        ]")
        lines.append("    }" + ("," if seg["id"] < 36 else ""))
    lines.append("]")
    lines.append("")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ Successfully wrote {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size} bytes)")

if __name__ == "__main__":
    generate_script()
