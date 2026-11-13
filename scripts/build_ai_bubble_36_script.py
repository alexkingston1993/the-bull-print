#!/usr/bin/env python3
"""
Complete Script Builder for 12-Minute Master Documentary #1:
THE $2.5 TRILLION AI BUBBLE PANIC: Inside the Tech Wipeout and the Midterm Regulatory Reckoning
Generates all 36 Segments x 5 Micro-Beats = 180 Micro-Beats
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "output" / "ai_bubble_documentary" / "chapters_script.py"

# Data for all 36 segments across 5 acts
SEGMENTS_DATA = [
    # --- ACT 1: THE 24-HOUR EVAPORATION (1 - 7) ---
    {
        "id": 1, "act": 1, "title": "The 9:30 AM Opening Bell Wipeout",
        "timestamp": "0:00 - 0:20",
        "voiceover": "At precisely 9:30 AM on a cold November morning in New York, the opening bell of the New York Stock Exchange rang out. But what followed was not an orderly trading session. In less than sixty seconds, automated algorithmic sell orders flooded the fiber-optic cables connecting Wall Street to New Jersey data centers.",
        "beats": [
            ("9:30 AM BELL", "WALL ST ALARM", "NYSE opening bell podium on Wall Street floor, brass bell vibrating under intense theatrical lighting, sea of traders in navy jackets staring up in disbelief."),
            ("FIBER OPTIC RUN", "MICROSECOND CRASH", "Extreme close-up of a high-frequency trading server rack with blinking crimson LEDs and tangled fiber-optic cables."),
            ("RED PLUNGE", "ALGO SELL WAVE", "Wall Street hedge fund trading floor, multi-monitor desks glowing with deep red candlestick plunge charts."),
            ("TRADERS FROZEN", "SYSTEMIC PANIC", "Senior portfolio manager taking off reading glasses, rubbing eyes in front of three glowing screens."),
            ("MANHATTAN CHILL", "OCTOBER SURPRISE", "Exterior of Wall Street subway station and Trinity Church, grey overcast November drizzle, somber city skyline.")
        ]
    },
    {
        "id": 2, "act": 1, "title": "The $2.5 Trillion Evaporation",
        "timestamp": "0:20 - 0:40",
        "voiceover": "By the closing cross, the scale of the destruction became undeniable. Two point five trillion dollars in equity valuation—an amount greater than the entire economy of Canada or Italy—had simply evaporated from the technology sector in a single 24-hour trading window.",
        "beats": [
            ("$2.5 TRILLION GONE", "RECORD WIPE", "Massive monolithic black digital billboard displaying a collapsing mountain of gold coins dissolving into smoke."),
            ("SILICON VALLEY", "LIGHTS DIM", "Panoramic view of Silicon Valley campus at dusk, glass office headquarters dark and quiet under heavy clouds."),
            ("LIQUIDITY DRAIN", "FED TIGHTENING", "Federal Reserve cash vault doors swinging closed, heavy steel gears locking in cold shadows."),
            ("TECH WORKERS", "EQUITY HIT", "Young tech employee standing on balcony looking over San Francisco skyline at sunset, holding phone tightly."),
            ("EMERGENCY MEET", "POST-BELL CRISIS", "Hedge fund conference boardroom, whiteboards with erased diagrams, half-empty coffee cups on mahogany table.")
        ]
    },
    {
        "id": 3, "act": 1, "title": "The Mag Seven Domino Effect",
        "timestamp": "0:40 - 1:00",
        "voiceover": "This was not an isolated mid-cap selloff. The carnage struck the crown jewels of American capitalism: Microsoft, Nvidia, Apple, Alphabet, Amazon, Meta, and Tesla. Together, the Magnificent Seven had carried eighty percent of the S&P 500's gains for two years. Now, the pillars were buckling.",
        "beats": [
            ("MAG SEVEN BUCKLE", "PILLARS SHATTER", "Seven massive stone classical columns crumbling simultaneously under dark stormy sky."),
            ("CHIP FEVER", "SUPPLY CHAIN", "Semiconductor cleanroom technician inspecting silicon wafer glowing green under laser inspection."),
            ("NASDAQ CORRECTION", "-5.5% CRASH", "Nasdaq Times Square tower in Manhattan, digital wrap screens reflecting on wet street below."),
            ("PANIC HEDGE", "PUT BUYING", "Institutional portfolio manager on telephone headset staring intently at Bloomberg terminal screen."),
            ("THE CRACK", "LEADERSHIP LOST", "A financial index chart line dropping sharply off a cliff into dark fog.")
        ]
    },
    {
        "id": 4, "act": 1, "title": "The Master Title Plate: The $2.5 Trillion AI Reckoning",
        "timestamp": "1:00 - 1:20",
        "voiceover": "This is the forensic autopsy of the AI bubble panic. How astronomical capital expenditures, an energy grid on the verge of blackout, and a sudden political earthquake in Washington collided to expose the fragile mathematics behind Wall Street's favorite narrative.",
        "beats": [
            ("THE AI RECKONING", "FORENSIC AUTOPSY", "Monolithic obsidian slab engraved with glowing circuitry, sitting in vast black water reflective pool."),
            ("$200B CAPEX", "MONUMENTAL BET", "Vast endless rows of AI data center server corridors illuminated by eerie electric blue and emerald light."),
            ("WASHINGTON SHOCK", "CONGRESSIONAL PROBE", "United States Capitol dome glowing under dark stormy purple thunderclouds in Washington DC."),
            ("POWER CRUNCH", "GRID AT LIMIT", "Electric power transmission towers stretching across desert landscape carrying massive high-voltage cables."),
            ("BUBBLE TEST", "MATHEMATICAL TRUTH", "Wall Street financial contract papers scattering across black marble floor in slow motion.")
        ]
    },
    {
        "id": 5, "act": 1, "title": "The Post-Midterm Political Shockwave",
        "timestamp": "1:20 - 1:40",
        "voiceover": "To understand why the panic erupted on this exact day, you have to look 250 miles south of Wall Street, to Washington DC. The midterm elections had just concluded with an unexpected Democratic sweep of both the House and Senate, abruptly dismantling unified party governance.",
        "beats": [
            ("MIDTERM SWEEP", "CAPITOL REVERSAL", "Ballot counting center at night, election workers sorting paper ballots under fluorescent warehouse lights."),
            ("CONGRESS SHIFT", "DIVIDED POWER", "Long empty marble hallway in the Cannon House Office Building in Washington DC, dramatic shadows."),
            ("GAVEL DROPS", "HEARINGS AHEAD", "Congressional hearing gavel resting on dark wood witness table next to microphone."),
            ("K STREET STUNNED", "LOBBYING PANIC", "Lobbyist in tailored overcoat walking rapidly down steps of Capitol towards waiting black town car."),
            ("WALL ST VS DC", "POWER COLLISION", "Low-angle architectural view of the iconic bronze Charging Bull statue in lower Manhattan during late twilight.")
        ]
    },
    {
        "id": 6, "act": 1, "title": "The AI Capital Expenditure Trap",
        "timestamp": "1:40 - 2:00",
        "voiceover": "For the past eighteen months, tech giants told Wall Street an alluring story: spend every spare dollar building AI compute, and the revenues will inevitably follow. Between Microsoft, Alphabet, Amazon, and Meta, annual capital expenditures soared past two hundred billion dollars.",
        "beats": [
            ("$200B SPEND", "DATA CENTER SPREE", "Massive construction cranes erecting a giant hyperscale data center facility in rural Virginia."),
            ("GPU HOARDING", "HUNDREDS OF THOUSANDS", "Forklift unloading pallets of Nvidia GPU server chassis inside high-tech staging warehouse."),
            ("CAPEX MOUNTING", "CASH BLEED", "Tech CFO staring at glowing bar charts of mounting capital expenditures on computer screen."),
            ("BURN RATE", "WHERE IS THE CASH?", "Stack of fresh $100 bills dissolving into digital green pixels and smoke in midair."),
            ("ANALYSTS QUESTION", "PATIENCE RUNS OUT", "Wall Street analyst taking notes during a tech quarterly earnings conference call.")
        ]
    },
    {
        "id": 7, "act": 1, "title": "The Wall Street Margin Call",
        "timestamp": "2:00 - 2:20",
        "voiceover": "When the post-election reality sank in—that tax breaks could be challenged and federal subsidies scrutinized—hedge funds realized the party was over. What started as subtle portfolio trimming exploded into cascading margin calls across automated momentum funds.",
        "beats": [
            ("MARGIN CALL", "FORCED LIQUIDATION", "Hedge fund trading terminal flashing urgent red liquidation notifications."),
            ("FLASH EXITS", "NO BID FOUND", "Crowded Wall Street sidewalk during evening rush hour, people staring down at illuminated phone screens in shock."),
            ("QUANT SELLOFF", "AUTOMATED DUMP", "Glass office skyscraper at night in Chicago, lights on in high-frequency quant trading floors."),
            ("CASCADE EFFECT", "DOMINO COLLAPSE", "Red digital ticker tape winding around classical stone building columns."),
            ("DAY ONE CLOSE", "TOTAL SHOCK", "Empty trading desk with discarded headphones and jacket hanging on back of chair.")
        ]
    },

    # --- ACT 2: THE $600 BILLION REVENUE HOLE (8 - 14) ---
    {
        "id": 8, "act": 2, "title": "The Circular AI Economy",
        "timestamp": "2:20 - 2:40",
        "voiceover": "Behind the gleaming corporate press releases lay an uncomfortable economic truth: much of the AI boom was an elaborate game of circular accounting. Big Tech invested billions into foundational model startups, who immediately funneled that exact cash back to Big Tech to rent cloud servers.",
        "beats": [
            ("CIRCULAR MONEY", "THE REVENUE ILLUSION", "Glowing digital ouroboros snake eating its tail made of golden dollar symbols in dark space."),
            ("VENTURE PUMP", "BILLIONS RECYCLED", "Venture capital partner signing an investment term sheet with a sleek silver fountain pen in a penthouse."),
            ("CLOUD INVOICE", "BACK TO TECH GIANTS", "Macro shot of a glowing high-tech digital invoice terminal showing cloud server compute billing."),
            ("ACCOUNTING MAZE", "NO REAL CUSTOMERS", "Maze of glass corridors in an ultra-modern corporate office with mysterious glowing blue pathways."),
            ("WALL ST DISCOVERY", "SMOKE & MIRRORS", "Senior forensic accountant examining financial flowcharts under a warm green desk lamp.")
        ]
    },
    {
        "id": 9, "act": 2, "title": "Silicon Valley's Desperate Land Grab",
        "timestamp": "2:40 - 3:00",
        "voiceover": "Every chief executive feared being labeled a dinosaur. So boardrooms authorized unvetted purchases of computing hardware at any price. It was a classic speculative land grab: whoever controls the clusters controls the future, regardless of whether anyone was paying to use them.",
        "beats": [
            ("CEO LAND GRAB", "FEAR OF EXTINCTION", "High-level board meeting in a glass skyscraper, CEO pointing emphatically at a glowing strategic map."),
            ("GPU AUCTION", "PAY ANY PRICE", "Industrial auction house floor where high-end AI server racks are bid upon under harsh spotlighting."),
            ("SPECULATIVE MANIA", "FOMO AT THE TOP", "Crowded Silicon Valley tech conference auditorium, thousands of attendees bathed in dramatic blue laser light."),
            ("WAREHOUSE GLUT", "IDLE CHIPS", "Endless shelves of crated server parts sitting dormant in a cavernous dimly-lit warehouse."),
            ("THE SPREADSHEET", "UNCHECKED EXPENSES", "Extreme close-up of a laptop screen reflecting in glasses as row after row of capital expenditure multiplies.")
        ]
    },
    {
        "id": 10, "act": 2, "title": "Where Are the Real Profits?",
        "timestamp": "3:00 - 3:20",
        "voiceover": "To justify two hundred billion dollars in annual hardware spending, the tech sector needed to generate over six hundred billion dollars in high-margin AI software revenues. But consumer subscription fees for chatbots were barely generating a fraction of that astronomical target.",
        "beats": [
            ("$600B GAP", "REVENUE DEFICIT", "Massive deep canyon with a tiny wooden bridge suspended over it, dark fog below and gold sunset above."),
            ("$20 CHATBOTS", "PENNIES ON THE DOLLAR", "A glowing smartphone on a coffee table showing a $20 monthly subscription prompt in a dark apartment."),
            ("MATH EXPOSED", "THE MISSING CASH", "Dark slate chalkboard covered in complex mathematical and economic equations faintly glowing white."),
            ("DISAPPOINTED FUNDS", "PROFIT DEFICIT", "Wall Street boardroom with three venture capitalists looking somberly down at a red leather binder."),
            ("THE REAL BILL", "COSTS OUTRUN SALES", "Old-fashioned mechanical balance scale tilting heavily towards a mountain of black hardware weights.")
        ]
    },
    {
        "id": 11, "act": 2, "title": "The GPU Depreciation Time Bomb",
        "timestamp": "3:20 - 3:40",
        "voiceover": "Unlike real estate or software code, AI hardware is not an enduring asset. State-of-the-art GPUs degrade under continuous maximum thermal load and become technologically obsolete in less than thirty-six months. Tech giants had loaded their balance sheets with rapidly decaying silicon.",
        "beats": [
            ("3-YEAR EXPIRY", "DEPRECIATION CLOCK", "A futuristic digital hourglass where glowing silicon microchips slowly dissolve into sand at the bottom."),
            ("THERMAL STRESS", "100 DEGREES CELSIUS", "Infrared thermal imaging view of a GPU motherboard glowing bright orange and white-hot under heavy computation."),
            ("OBSOLETE SILICON", "SCRAP VALUE", "Discarded previous-generation computer motherboards stacked neatly in an industrial recycling facility."),
            ("BALANCE SHEET HIT", "WRITE-DOWNS AHEAD", "A CFO's desk with an ink stamp slamming down an urgent document under harsh desk lamp light."),
            ("THE SILICON CLOCK", "TICKING ASSETS", "Close macro shot of a complex microchip die under blue light with a digital countdown reflection.")
        ]
    },
    {
        "id": 12, "act": 2, "title": "Enterprise Software's Brutal Reality",
        "timestamp": "3:40 - 4:00",
        "voiceover": "Chief Information Officers across the Fortune 500 started running the actual numbers. Deploying generative AI across corporate databases was producing hallucination risks, legal liabilities, and ballooning token bills. Corporate IT departments began quietly putting AI pilot projects on freeze.",
        "beats": [
            ("CIO FREEZE", "PILOTS ON HOLD", "Corporate IT command center with glass screens showing multiple cancelled software rollouts."),
            ("LEGAL EXPOSURE", "HALLUCINATION RISK", "Corporate legal library with rows of leather law books, an open laptop displaying copyright disclaimers."),
            ("TOKEN BILL SHOCK", "BUDGET OVERRUNS", "A stack of paper enterprise cloud invoices highlighted with harsh yellow markers on a corporate desk."),
            ("SECURITY AUDIT", "DATA LEAK FEARS", "Cybersecurity engineer with encrypted smart card entering a biometric server vault."),
            ("ENTERPRISE PAUSE", "SHOW ME ROI", "Fortune 500 board room table where an executive firmly closes a sleek presentation folder.")
        ]
    },
    {
        "id": 13, "act": 2, "title": "Venture Capital's Burn Rate Crisis",
        "timestamp": "4:00 - 4:20",
        "voiceover": "In Silicon Valley, seed-stage AI startups were burning through fifty million dollars in compute credits every quarter with zero customer retention. When venture capitalists realized the runway was ending without a viable business model, the funding spigots abruptly turned off.",
        "beats": [
            ("$50M BURN", "NO RUNWAY LEFT", "Sleek loft startup office in San Francisco, empty beanbags and deserted workstations under industrial pendant lights."),
            ("VC DOOR SLAMS", "FUNDING DRY-UP", "Polished oak double doors of a top Sand Hill Road venture firm slowly closing shut in sharp lighting."),
            ("UNPAID COMPUTE", "DEFAULT WARNING", "A dark laptop screen in a coffee shop flashing a red server disconnection warning notice."),
            ("FOUNDER DESPAIR", "THE COLD REALITY", "Young startup founder in a grey hoodie sitting on steps outside an office building holding a paper coffee cup."),
            ("VALUATION COLLAPSE", "DOWN-ROUNDS BEGIN", "Graph of plunging private market startup valuations displayed on an iPad tablet.")
        ]
    },
    {
        "id": 14, "act": 2, "title": "The Return on Investment Mirage",
        "timestamp": "4:20 - 4:40",
        "voiceover": "Wall Street investment banks published blistering research reports: the entire generative artificial intelligence sector was facing a three-hundred-billion-dollar annual revenue shortfall. The narrative had broken: AI was brilliant science, but an unprofitable financial black hole.",
        "beats": [
            ("THE ROI MIRAGE", "THE $300B VOID", "Desert mirage landscape where a glowing glass city shimmers on the horizon and dissolves into hot desert air."),
            ("GOLDMAN BOMBSHELL", "WALL ST REVOLT", "Research floor of a major Wall Street bank, analysts printing off confidential black-and-white reports."),
            ("THE BLACK HOLE", "CAPITAL CONSUMPTION", "Conceptual visualization of a glowing vortex pulling in gold coins and green currency into a dark cosmic center."),
            ("INVESTOR SKEPTICISM", "TRUST SHATTERED", "A panel of stern institutional asset managers listening to a presentation in a luxury auditorium."),
            ("THE REALITY TEST", "NUMBERS DON'T LIE", "A heavy mechanical iron safe door resting half-open, revealing empty silver shelves inside.")
        ]
    },

    # --- ACT 3: THE PHYSICAL WALL — ENERGY & WATER (15 - 21) ---
    {
        "id": 15, "act": 3, "title": "Running Out of Watts",
        "timestamp": "4:40 - 5:00",
        "voiceover": "Even if the financing had remained infinite, the AI boom was hurtling into an unyielding physical brick wall: the laws of thermodynamics. Advanced artificial intelligence models do not run on software magic; they run on raw, unadulterated electric wattage.",
        "beats": [
            ("PHYSICAL WALL", "LAWS OF THERMO", "Massive concrete brutalist wall standing in a barren desert under harsh overhead midday sunlight."),
            ("RAW WATTAGE", "THE HUNGRY CHIP", "Macro view of copper heat pipes and cooling fins inside an industrial computer heatsink with heat shimmering."),
            ("SUBSTATION GLOW", "HEAVY TRANSFORMERS", "Massive electrical utility substation humming at twilight, thick ceramic insulators and humming transformers."),
            ("ENERGY METERS", "DIALS SPINNING", "Industrial power consumption meter with spinning metal dial vibrating under heavy load."),
            ("THE GRID CHOKE", "CAPACITY DEPLETED", "Silhouetted electrical worker in hard hat inspecting high-voltage power lines against stormy sunset.")
        ]
    },
    {
        "id": 16, "act": 3, "title": "The Gigawatt Data Center Crisis",
        "timestamp": "5:00 - 5:20",
        "voiceover": "Training the next generation of frontier models requires not megawatt facilities, but gigawatt campuses. A single gigawatt data center consumes as much electricity as seven hundred and fifty thousand American households. In Northern Virginia, the power grid literally had no more electricity to give.",
        "beats": [
            ("1 GIGAWATT NEED", "CITY-SIZED POWER", "Aerial view of a sprawling metropolitan city at night, thousands of illuminated buildings stretching to horizon."),
            ("VIRGINIA HUB", "DATA CENTER ALLEY", "Drone landscape view over Northern Virginia Data Center Alley, massive flat-roofed grey server facilities surrounded by trees."),
            ("TRANSMISSION STRAIN", "OVERLOAD RISK", "Heavy industrial power cables suspended high above ground, sizzling in mist and rain."),
            ("UTILITY REJECTION", "NO MORE POWER", "Power utility executive reviewing a red-stamped grid interconnect denial letter in an office."),
            ("THE BOTTLENECK", "VIRTUAL MEETS PHYSICAL", "A single fiber optic cable running into a heavy rusted iron electrical conduit in a concrete tunnel.")
        ]
    },
    {
        "id": 17, "act": 3, "title": "Local Grids Pushed to the Brink",
        "timestamp": "5:20 - 5:40",
        "voiceover": "In communities from Georgia to Arizona, local residents saw their residential utility bills spike twenty-five percent to subsidize high-voltage power lines built exclusively for tech data centers. Public backlash exploded at town hall meetings across the country.",
        "beats": [
            ("BILLS SPIKE +25%", "CITIZENS PAY", "Close-up of a residential electricity utility bill held in elderly hands at a kitchen table under soft light."),
            ("TOWN HALL RAGE", "PUBLIC BACKLASH", "Packed suburban municipal town hall meeting, citizens standing up and speaking passionately at a podium microphone."),
            ("SUBSTATION ENCROACHMENT", "NEIGHBORHOOD LINES", "High-voltage transmission towers looming directly behind quiet suburban residential homes and lawns."),
            ("PROTEST OUTSIDE", "NOT OUR TAXES", "Peaceful demonstration outside a corporate data center perimeter fence with banners in afternoon sunlight."),
            ("POLITICAL FLASHPOINT", "ENERGY JUSTICE", "Local city council members seated at dais listening with grave expressions to angry constituents.")
        ]
    },
    {
        "id": 18, "act": 3, "title": "Big Tech's Secret Nuclear Deals",
        "timestamp": "5:40 - 6:00",
        "voiceover": "Desperate to bypass public utility queues, tech conglomerates began making unprecedented deals. Microsoft signed a twenty-year power purchase agreement to restart the decommissioned Three Mile Island nuclear plant in Pennsylvania. Amazon and Google followed with atomic energy agreements.",
        "beats": [
            ("ATOMIC AI", "THE NUCLEAR SHIFT", "Massive concrete nuclear cooling towers venting clean white steam plumes into a dark blue twilight sky."),
            ("THREE MILE ISLAND", "RESTARTING A LEGEND", "Aerial wide shot of the iconic Three Mile Island nuclear generating station surrounded by the Susquehanna River."),
            ("TECH SIGNS CONTRACTS", "20-YEAR PPA", "Corporate fountain pen signing a leather-bound energy purchase agreement under warm studio lighting."),
            ("REACTOR VAULT", "ATOMIC POWER", "Gleaming blue Cherenkov radiation glowing at the bottom of a deep nuclear reactor water pool."),
            ("ENERGY MONOPOLY", "TECH BUYS THE GRID", "Silhouette of a modern tech executive standing before a massive nuclear facility at dawn.")
        ]
    },
    {
        "id": 19, "act": 3, "title": "The Three Mile Island Gamble",
        "timestamp": "6:00 - 6:20",
        "voiceover": "Restarting a shuttered nuclear reactor is not like flipping a light switch. It requires billions in capital, years of safety retrofits, and rigorous federal Nuclear Regulatory Commission approvals. Wall Street had priced in immediate AI deployment; reality offered a five-year waiting line.",
        "beats": [
            ("5-YEAR DELAY", "CANNOT FLIP SWITCH", "Old mechanical control room inside a decommissioned nuclear plant with dusty analog gauges and dials."),
            ("SAFETY RETROFITS", "BILLIONS REQUIRED", "Nuclear engineers in white safety coveralls and dosimeters inspecting heavy steel steam pipes with flashlights."),
            ("NRC REGULATORS", "FEDERAL SCRUTINY", "Official seal of the Nuclear Regulatory Commission in Washington DC under formal institutional lighting."),
            ("WALL ST IMPATIENCE", "CLOCK IS TICKING", "Trading desk timer counting down seconds against a dark red backdrop."),
            ("REALITY SINKS IN", "THE ATOMIC WAIT", "Heavy rusted padlock hanging on the security gate of an industrial nuclear perimeter.")
        ]
    },
    {
        "id": 20, "act": 3, "title": "Water Scarcity in Desert Towns",
        "timestamp": "6:20 - 6:40",
        "voiceover": "Electricity was only half the physical nightmare. Millions of AI chips generate intense heat that must be continuously cooled by evaporating billions of gallons of drinking water. In drought-stricken Arizona and Utah, server farms were draining subterranean municipal aquifers.",
        "beats": [
            ("WATER DRAIN", "BILLIONS OF GALLONS", "Massive evaporative industrial cooling towers spraying cascades of water over heat exchange coils."),
            ("DESERT AQUIFER", "DRYING UP", "Cracked parched desert earth in the American Southwest stretching towards distant barren mountains under baking sun."),
            ("MUNICIPAL CRISIS", "DRINKING WATER THREAT", "Water reservoir showing a prominent white bathtub ring indicating severely depleted water levels."),
            ("PIPELINE TO DATA CENTER", "RIVALS WITH FARMS", "Heavy industrial water pipeline cutting through agricultural fields in Arizona towards a grey server complex."),
            ("ENVIRONMENTAL CLASH", "TECH VS WATER", "Close macro shot of a single water droplet falling from a metal spigot onto dry dust.")
        ]
    },
    {
        "id": 21, "act": 3, "title": "The Physical Limits of Moore's Law",
        "timestamp": "6:40 - 7:00",
        "voiceover": "For half a century, computing progressed on the guarantee that chips would become twice as efficient every eighteen months. But at the atomic two-nanometer threshold, quantum tunneling and thermal throttling arrived. You could no longer double speed without doubling power.",
        "beats": [
            ("MOORE'S LAW WALL", "ATOMIC LIMITS", "Stylized visualization of silicon atoms and electron quantum tunneling effects glowing neon blue."),
            ("2-NANOMETER CHIPS", "QUANTUM DRIFT", "Ultra-high-resolution electron microscope image of nanoscale semiconductor transistors."),
            ("THERMAL CHOKE", "MELTING THRESHOLD", "Liquid nitrogen cooling apparatus venting dense cold fog over an ultra-dense GPU test bench."),
            ("ENGINEERING STALEMATE", "NO EASY FIX", "Chief semiconductor architect sketching circuit diagrams on a glass board with white marker."),
            ("THE REAL COST", "BRUTE FORCE FAILS", "A heavy iron anvil resting under an industrial hydraulic press, dramatic atmospheric studio lighting.")
        ]
    },

    # --- ACT 4: WASHINGTON DROPS THE HAMMER (22 - 28) ---
    {
        "id": 22, "act": 4, "title": "The Midterm Democratic Congressional Sweep",
        "timestamp": "7:00 - 7:20",
        "voiceover": "When the dust settled from the 2026 midterm elections, the political landscape in Washington had completely transformed. A decisive sweep gave Democrats control of key House and Senate oversight committees, placing antitrust reformers into the most powerful committee chairmanships.",
        "beats": [
            ("MIDTERM EARTHQUAKE", "CONGRESS FLIPS", "Wide panoramic view of the US House of Representatives chamber filled with lawmakers in session under chandeliers."),
            ("NEW CHAIRS", "ANTITRUST HAWKS", "Portrait of a determined congressional committee chairman reviewing a leather dossier on Capitol Hill."),
            ("OVERSIGHT POWERS", "SUBPOENA CANNON", "Official congressional committee letterhead stamped with formal blue wax seal on executive desk."),
            ("CORPORATE LOBBYISTS", "ACCESS CUT", "K Street lobbying firm boardroom in downtown Washington DC with dark mahogany blinds drawn closed."),
            ("DIVIDED CAPITAL", "THE NEW ERA", "Exterior shot of the White House and Capitol building illuminated against deep twilight sky.")
        ]
    },
    {
        "id": 23, "act": 4, "title": "Subpoenas and Antitrust Hearings",
        "timestamp": "7:20 - 7:40",
        "voiceover": "Within seventy-two hours of the election results, formal inquiry letters and document requests were dispatched to Silicon Valley headquarters. Congressional investigators demanded internal communications regarding algorithmic collusion, anticompetitive exclusive cloud deals, and chip allocation agreements.",
        "beats": [
            ("SUBPOENAS FLY", "72-HOUR NOTICE", "Courier delivering a thick white official envelope marked URGENT CONGRESSIONAL INQUIRY to a corporate reception desk."),
            ("SWORN TESTIMONY", "WITNESS TABLE", "Witness table in a formal Senate hearing room with green felt cloth, microphones, and water pitchers."),
            ("EXCLUSIVE DEALS", "ANTITRUST SCRUTINY", "Two corporate executives shaking hands in silhouette behind translucent frosted glass office walls."),
            ("INTERNAL EMAILS", "SMOKING GUNS", "Close-up of a printed court exhibit document with bold black redaction bars across confidential text."),
            ("LEGAL TEAMS MOBILIZE", "WAR ROOMS OPEN", "A high-powered corporate legal defense team working late into the night surrounded by white archive boxes.")
        ]
    },
    {
        "id": 24, "act": 4, "title": "Investigating AI Data Center Subsidies",
        "timestamp": "7:40 - 8:00",
        "voiceover": "The most explosive investigation focused on government subsidies. Lawmakers revealed that tech giants had captured tens of billions in federal green energy tax credits and state municipal tax exemptions to build computing hubs that employed virtually zero local permanent workers.",
        "beats": [
            ("BILLIONS IN CREDITS", "THE TAX GRAB", "IRS federal building exterior in Washington DC with stone carved signage and autumn trees."),
            ("ZERO JOBS CREATED", "EMPTY HUBS", "Vast interior of an automated data center where automated robotic carts glide past server racks with no humans present."),
            ("LOCAL TAX LOSS", "SCHOOLS DEFUNDED", "A small-town county courthouse in rural America with a modest clock tower against dusk sky."),
            ("CONGRESSIONAL EXPOSURE", "CHAIR SPEAKS", "Congressional hearing dais with news television camera lenses focused on speaking lawmakers."),
            ("SUBSIDY CLAWBACK", "LEGISLATION FILED", "A printed bill titled 'AI Infrastructure Accountability Act' resting on a desk with pen ready.")
        ]
    },
    {
        "id": 25, "act": 4, "title": "The Energy Monopoly Investigation",
        "timestamp": "8:00 - 8:20",
        "voiceover": "The Federal Energy Regulatory Commission opened an emergency review into tech firms co-locating data centers directly behind nuclear power stations. If tech companies consumed base-load nuclear power directly, ordinary citizens would be forced to bear the cost of dirtier, more expensive backup grid power.",
        "beats": [
            ("FERC INVESTIGATION", "GRID FAVORITISM", "Headquarters of the Federal Energy Regulatory Commission in Washington DC with stone pillars."),
            ("BEHIND-THE-METER DEALS", "CUTTING THE QUEUE", "Schematic diagram of an electrical substation showing power diverted directly from a nuclear plant to a server farm."),
            ("CITIZENS ON COAL", "DIRTY BACKUP", "Coal-fired power plant smokestacks billowing dark plumes into a stormy sunset sky."),
            ("REGULATORY BLOCK", "FERC SAYS NO", "Gavel hitting sound block at an administrative regulatory energy hearing room."),
            ("ENERGY BATTLE", "PUBLIC VS TECH", "High-voltage transmission line dividing a green public park from a high-security barbed-wire tech facility.")
        ]
    },
    {
        "id": 26, "act": 4, "title": "National Security Export Controls",
        "timestamp": "8:20 - 8:40",
        "voiceover": "Simultaneously, the Department of Commerce unveiled a draconian expansion of export restrictions. To prevent advanced semiconductors from reaching rival superpowers, international chip shipments were halted, cutting off twenty percent of projected global hardware demand overnight.",
        "beats": [
            ("EXPORT CLAMPDOWN", "GLOBAL EMBARGO", "Cargo container port at night with towering cranes loading shipping containers under amber stadium lights."),
            ("CHIP BAN", "COMMERCE RULES", "Department of Commerce Herbert C. Hoover Building in Washington DC at twilight."),
            ("CUSTOMS INSPECTION", "SILICON SEIZED", "Customs officer with flashlight inspecting high-tech wooden crates filled with sealed GPU hardware at an airport."),
            ("DEMAND CUT -20%", "GLOBAL CANCEL", "Plunging world trade route map with glowing flight paths fading to black across oceans."),
            ("GEOPOLITICAL WAR", "CHIP SHIELD", "High-tech world map with red holographic border lines intersecting across trade corridors.")
        ]
    },
    {
        "id": 27, "act": 4, "title": "The Big Tech Lobbying Firewall Collapses",
        "timestamp": "8:40 - 9:00",
        "voiceover": "For two decades, Silicon Valley had enjoyed bipartisan deference in Washington. Tech titans walked the halls of Congress as celebrated innovators. But in late 2026, the lobbying firewall completely collapsed under public anger over energy prices, job displacement, and market monopolization.",
        "beats": [
            ("FIREWALL BREAKS", "THE ERA ENDS", "Cracking glass shield reflecting the glowing US Capitol dome, fissures expanding across the surface."),
            ("THE TECH TITANS", "CALLED TO TESTIFY", "Rows of television cameras and journalists waiting outside a closed congressional hearing room door."),
            ("PUBLIC SKEPTICISM", "HEROES NO MORE", "A newspaper stand in a busy city with headlines questioning big tech monopolies."),
            ("K STREET RETREAT", "DOORS CLOSED", "Silhouettes of lobbyists sitting in quiet lounge with heads in hands under dim table lamps."),
            ("POLITICAL ISOLATION", "NO MORE ALLIES", "A lone microphone standing in the center of an imposing marble hearing hall under a single spotlight.")
        ]
    },
    {
        "id": 28, "act": 4, "title": "Wall Street Prices In Regulatory Winter",
        "timestamp": "9:00 - 9:20",
        "voiceover": "Wall Street equity analysts rapidly tore up their earnings models. The assumption of perpetual tax breaks, cheap subsidized electricity, and unchecked monopoly acquisitions was gone. In forty-eight hours, risk premiums on tech multiples soared to ten-year highs.",
        "beats": [
            ("REGULATORY WINTER", "MODELS SHREDDED", "Wall Street financial model on laptop screen with bright red negative forecast revisions highlighted."),
            ("MULTIPLE CONTRACTION", "P/E RATIOS CRUSHED", "Antique brass scales with heavy lead weight dropping down on financial equities pan."),
            ("RISK PREMIUM SPIKE", "TEN-YEAR HIGH", "Bond yield graph climbing steeply upward against dark backdrop on a financial terminal."),
            ("EARNINGS CUTS", "DOWNWARD REVISIONS", "Stack of freshly stamped investment bank research reports labeled 'DOWNGRADE TO UNDERWEIGHT'."),
            ("INSTITUTIONAL SHIFT", "CAPITAL ROTATION", "Hand of an institutional fund manager transferring heavy chess pieces across a polished dark board.")
        ]
    },

    # --- ACT 5: THE AFTERMATH & THE REAL NEW PARADIGM (29 - 36) ---
    {
        "id": 29, "act": 5, "title": "The Dot-Com Echo: 2000 vs 2026",
        "timestamp": "9:20 - 9:40",
        "voiceover": "Veteran market historians immediately pointed to the eerie parallels with the year 2000. Back then, telecom giants spent hundreds of billions laying millions of miles of dark fiber optic cables that sat unused for a decade before the real internet economy was born.",
        "beats": [
            ("DOT-COM PARALLEL", "THE 2000 LESSON", "Vintage 2000 newspaper front page reading 'TECH BUBBLE BURSTS' beside a modern digital tablet."),
            ("DARK FIBER", "EMPTY PIPES", "Underground industrial trench with thousands of colorful fiber optic conduits buried under pavement."),
            ("OVERBUILD CYCLE", "YEARS AHEAD OF DEMAND", "Massive empty telecommunications switching warehouse with silent rows of equipment racks."),
            ("SPECULATIVE RESET", "CLEARING THE ROT", "Storm clearing over Wall Street with golden sunlight breaking through dark dissipating clouds."),
            ("HISTORICAL RHYTHM", "CYCLE REPEATS", "An antique grandfather clock with brass pendulum swinging steadily inside a quiet study.")
        ]
    },
    {
        "id": 30, "act": 5, "title": "Who Survives the Crash?",
        "timestamp": "9:40 - 10:00",
        "voiceover": "Just as Amazon and Google emerged stronger from the wreckage of the dot-com crash, the bursting of the AI bubble does not mean the technology disappears. It separates the companies with fortress balance sheets and real cash flows from the leveraged paper pretenders.",
        "beats": [
            ("SURVIVAL OF FITTEST", "THE CASH KINGS", "A massive solid titanium vault door standing resolute against a roaring storm of wind and sparks."),
            ("FORTRESS BALANCE", "HUNDREDS OF BILLIONS", "Stacks of gold bullion bars reflecting warm light inside a high-security central depository."),
            ("THE FALLEN", "BANKRUPTCIES MOUNT", "Empty glass office building with a yellow lease sign posted in the window."),
            ("PRUDENT CAPITAL", "DISCIPLINE WINS", "Conservative portfolio manager reviewing financial statements with a calm focused expression."),
            ("PHOENIX FROM ASHES", "THE REAL LEADERS", "A sleek modern semiconductor chip resting on a bed of dark volcanic rock, gleaming in spotlight.")
        ]
    },
    {
        "id": 31, "act": 5, "title": "The Sovereign AI Arms Race",
        "timestamp": "10:00 - 10:20",
        "voiceover": "As private venture capital retreated, a new buyer stepped in to backstop compute: national governments. From France and Japan to Saudi Arabia and the UAE, sovereign wealth funds began nationalizing AI infrastructure as critical strategic state assets.",
        "beats": [
            ("SOVEREIGN AI", "NATIONS STEP IN", "Panoramic view of a futuristic government data center built in the desert under starry night sky."),
            ("PETRODOLLAR COMPUTE", "MIDDLE EAST FUNDS", "Ultra-luxurious sovereign investment conference hall in Riyadh with gold trim and digital displays."),
            ("NATIONAL SECURITY", "STATE INFRASTRUCTURE", "Military-grade communications dish and radome atop a mountain ridge at sunrise."),
            ("GOVERNMENT CONTRACTS", "NEW BUYER OF LAST RESORT", "Government procurement officer stamping official approval on a high-security compute acquisition."),
            ("GLOBAL REBALANCING", "COMPUTE GOES NATIONAL", "World globe illuminated by glowing flight paths connecting national capitals with data links.")
        ]
    },
    {
        "id": 32, "act": 5, "title": "From Hype to Infrastructure Utility",
        "timestamp": "10:20 - 10:40",
        "voiceover": "Artificial intelligence is undergoing the same transition as electricity, railroads, and the cloud: transitioning from an over-hyped speculative novelty into a boring, low-margin, heavily regulated public utility.",
        "beats": [
            ("UTILITY PARADIGM", "BORING IS BETTER", "Industrial 19th-century railway tracks stretching toward vanishing point under cloudy sky."),
            ("REGULATED MARGINS", "NO MORE 80% GROSS", "Water utility treatment plant with massive pipes and valves operating quietly and steadily."),
            ("COMMODITY COMPUTE", "STANDARDIZED POWER", "Modern electrical power switchboard with uniform grey circuit breakers humming calmly."),
            ("THE REAL BENEFIT", "EVERYDAY INTEGRATION", "Doctor in a clinic looking at an AI diagnostic scanner overlay on a tablet beside patient."),
            ("THE QUIET WORKHORSE", "NO MORE DRAMA", "A clean automated logistics warehouse where robotic arms sort packages with silent precision.")
        ]
    },
    {
        "id": 33, "act": 5, "title": "The Retail Traps & False Rebounds",
        "timestamp": "10:40 - 11:00",
        "voiceover": "During every major market cycle reset, retail traders fall victim to the dead-cat bounce. Believing every dip is an automatic buying opportunity, thousands rush in on minor green days, only to be crushed by institutional block distribution.",
        "beats": [
            ("DEAD CAT BOUNCE", "THE RETAIL TRAP", "Plunging stock chart that gives a brief upward hop before continuing its steep downward trajectory."),
            ("BUY THE DIP LIE", "FALLING KNIVES", "A smartphone screen displaying a popular trading app with green notifications in front of a gloomy window."),
            ("INSTITUTIONAL UNLOAD", "SMART MONEY SELLS", "Hand of an institutional trader quietly clicking 'EXECUTE BLOCK SALE' on an understated terminal."),
            ("THE SQUEEZE", "TRAPPED LONGS", "Close-up of an anxious young retail trader holding head in hands as screen turns bright red."),
            ("DISCIPLINE OVER FOMO", "THE HARD LESSON", "An open classic investing book on a dark oak desk under reading light with highlighted passages.")
        ]
    },
    {
        "id": 34, "act": 5, "title": "The Smart Money Rotation",
        "timestamp": "11:00 - 11:20",
        "voiceover": "Where did the trillions of dollars fleeing technology actually go? Smart money rotated into tangible real assets: energy infrastructure, defense contractors, gold bullion, and high-yielding sovereign bonds. The era of pure paper wealth surrendered to the real economy.",
        "beats": [
            ("CAPITAL ROTATION", "TANGIBLE ASSETS", "Heavy gold bars, crude oil barrels, and industrial machinery arranged dramatically on dark slate."),
            ("ENERGY SURGE", "POWER PRODUCERS WIN", "Massive hydroelectric dam with roaring white water pouring through spillways under sunlight."),
            ("DEFENSE CONTRACTS", "HARD POWER", "Sleek modern defense aerospace assembly hangar with military aircraft frames under construction."),
            ("TREASURY HAVEN", "5% YIELD APPEAL", "Official US Treasury bond certificate printed on textured paper with ornate green border."),
            ("REAL OVER PAPER", "THE NEW WINNERS", "Silhouette of a container cargo ship heavily laden with containers steaming across open ocean at sunset.")
        ]
    },
    {
        "id": 35, "act": 5, "title": "The True Valuation of Artificial Intelligence",
        "timestamp": "11:20 - 11:40",
        "voiceover": "Artificial intelligence will change the world. It will cure diseases, optimize logistics, and automate routine human labor. But its value will be measured in actual corporate productivity gains, not astronomical price-to-sales ratios detached from reality.",
        "beats": [
            ("TRUE VALUE", "PRODUCTIVITY GAINS", "A high-tech medical laboratory with scientist peering into laser holographic DNA visualization."),
            ("LOGISTICS OPTIMIZED", "GLOBAL EFFICIENCY", "Automated container port operating seamlessly under night sky with robotic vehicles moving shipping boxes."),
            ("REAL METRICS", "CASH FLOW MATTERS", "Clean ledger book with black fountain pen ink numbers balancing perfectly under warm lamp light."),
            ("THE BALANCED VIEW", "SCIENCE MEETS REALITY", "A sleek glass hourglass resting on a marble mantlepiece with sand flowing steadily down."),
            ("HUMAN & MACHINE", "THE SUSTAINABLE PATH", "A human hand reaching across to gently adjust a precision robotic manipulator in a high-tech lab.")
        ]
    },
    {
        "id": 36, "act": 5, "title": "Final Verdict: The End of Free Passes",
        "timestamp": "11:40 - 12:00",
        "voiceover": "The $2.5 Trillion wipeout was not a death blow to artificial intelligence; it was the arrival of adulthood. The era of free passes in Washington, infinite capital from Wall Street, and unchecked consumption of public resources is over. The game has changed, and only the mathematically disciplined will survive.",
        "beats": [
            ("THE ARRIVAL", "ADULTHOOD FOR TECH", "Dramatic silhouette of a solitary figure standing at the precipice of a high mountain overlooking sunrise."),
            ("FREE PASSES OVER", "ACCOUNTABILITY", "The massive brass doors of the Supreme Court and Capitol standing imposing and immovable."),
            ("MATHEMATICAL DISCIPLINE", "ONLY THE STRONG", "A master chess board set on a polished table, the king piece illuminated by a single warm spotlight."),
            ("THE BULL PRINT", "SUBSCRIBE & STAY AHEAD", "Signature high-CTR YouTube end-screen: sleek dark 3D gold embossed channel logo '@TheBullPrint'."),
            ("FINAL BLACKOUT", "THE LESSON REMAINS", "Cinematic dark room where a single glowing server light gently pulses and fades into deep black.")
        ]
    }
]

def generate_script():
    print(f"Building complete chapters_script.py with {len(SEGMENTS_DATA)} segments...")
    lines = [
        "#!/usr/bin/env python3",
        '"""',
        "THE $2.5 TRILLION AI BUBBLE PANIC: Inside the Tech Wipeout and the Midterm Regulatory Reckoning",
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
