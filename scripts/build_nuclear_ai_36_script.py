#!/usr/bin/env python3
"""
Complete Script Builder for 12-Minute Master Documentary #3:
THE ENERGY GRID CHOKEHOLD: Why Big Tech Is Buying Nuclear Reactors for AI
Generates all 36 Segments x 5 Micro-Beats = 180 Micro-Beats
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "output" / "nuclear_ai_documentary" / "chapters_script.py"

SEGMENTS_DATA = [
    # --- ACT 1: THE INVISIBLE BLACKOUT (1 - 7) ---
    {
        "id": 1, "act": 1, "title": "When The Query Hits The Grid",
        "timestamp": "0:00 - 0:20",
        "voiceover": "Every time you type a prompt into ChatGPT, generate a photorealistic image, or synthesize high-definition video, a shockwave travels through an invisible physical supply chain. Deep inside an industrial server warehouse, high-voltage transformers groan under a sudden surge of electric current.",
        "beats": [
            ("THE PROMPT PULSE", "GRID SHOCKWAVE", "A glowing smartphone resting on a minimalist concrete table in a dark room, glowing blue interface reflecting in screen."),
            ("THE TRANSFORMER SURGE", "PHYSICAL REALITY", "Massive outdoor electrical utility transformer humming in high-voltage substation at dusk, ceramic insulators glowing."),
            ("DATA CENTER CORRIDOR", "ROW OF COMPUTE", "Perspective view down an endless aisle of black server racks with pulsating cyan status LEDs on polished floor."),
            ("HEAT EMISSION", "THERMAL PLUME", "Infrared thermal camera view of an AI computing cluster glowing intense white-hot and orange under thermal strain."),
            ("THE INVISIBLE CHAIN", "VIRTUAL TO PHYSICAL", "High-voltage transmission line slicing through morning mist against deep forest background.")
        ]
    },
    {
        "id": 2, "act": 1, "title": "10x More Power Than a Google Search",
        "timestamp": "0:20 - 0:40",
        "voiceover": "A conventional Google search requires zero point three watt-hours of electricity—barely enough to light an LED bulb for a second. An artificial intelligence query consumes nearly three watt-hours—ten times more energy. To generate a single AI video, the compute consumes enough power to charge multiple smartphones.",
        "beats": [
            ("10x POWER SURGE", "THE ENERGY TAX", "Comparison shot: small delicate incandescent light bulb filament next to a roaring industrial plasma torch."),
            ("3 WATT-HOURS", "PER QUERY COST", "Digital watt-hour meter spinning rapidly with glowing green digital numerals advancing in blur."),
            ("VIDEO GENERATION", "MASSIVE COMPUTE", "A rack of specialized AI processing units with thick copper liquid-cooling manifolds venting heat."),
            ("MILLIONS OF QUERIES", "CUMULATIVE LOAD", "Graphic visualization of millions of electric sparks converging from across the globe into a single dense electrical node."),
            ("THE INVISIBLE DRAW", "ENERGY CONVERSION", "Silhouetted silhouette of an electrical grid dispatcher looking at citywide load curves in control center.")
        ]
    },
    {
        "id": 3, "act": 1, "title": "The 2030 Power Deficit Shock",
        "timestamp": "0:40 - 1:00",
        "voiceover": "According to the International Energy Agency, global data center electricity consumption will double by 2026, reaching one thousand terawatt-hours—equivalent to the entire electricity demand of Japan. By 2030, artificial intelligence could consume nearly ten percent of all electricity generated in the United States.",
        "beats": [
            ("1,000 TWh BY 2026", "EQUAL TO JAPAN", "Panoramic night aerial view of Tokyo glowing with millions of neon lights stretching to horizon."),
            ("10% OF US POWER", "AI CONSUMPTION", "A massive map of the United States electrical grid with major interconnections pulsing with glowing energy rivers."),
            ("DEFICIT WARNING", "GRID ALARM", "Official international energy report document stamped with confidential red seal on mahogany desk."),
            ("UTILITY LEADERS GATHER", "URGENT SUMMIT", "Electric utility chief executives gathered around an executive table reviewing steep exponential load curves."),
            ("THE POWER CHOKE", "NOT ENOUGH WATTS", "An industrial electrical circuit breaker tripping open with a bright electric arc spark in slow motion.")
        ]
    },
    {
        "id": 4, "act": 1, "title": "Master Title Plate: The Energy Grid Chokehold",
        "timestamp": "1:00 - 1:20",
        "voiceover": "This is the investigative documentary into Silicon Valley’s greatest crisis: the energy bottleneck. Why the trillion-dollar artificial intelligence race has run out of electricity, and why Big Tech is buying up atomic reactors to survive.",
        "beats": [
            ("ENERGY CHOKEHOLD", "THE ATOMIC RACE", "Monumental monolithic cooling tower of a nuclear plant rising behind a futuristic data center campus under stormy twilight sky."),
            ("SILICON VALLEY CRISIS", "POWER RUNS OUT", "Silicon Valley executive suite at night with glass windows overlooking dark quiet highway."),
            ("THE NUCLEAR REVIVAL", "ATOMIC AI", "Gleaming blue Cherenkov radiation glowing at the bottom of an open nuclear reactor pool in high contrast."),
            ("BILLIONS ON THE LINE", "BIG TECH GAMBLE", "High-angle view of a corporate tech headquarters illuminated with glowing corporate logos."),
            ("PHYSICS OVER HYPE", "THE HARD REALITY", "A massive steel turbine rotor being machined in an industrial factory with sparks flying.")
        ]
    },
    {
        "id": 5, "act": 1, "title": "Northern Virginia: Data Center Alley Maxes Out",
        "timestamp": "1:20 - 1:40",
        "voiceover": "In Loudoun County, Virginia—known as Data Center Alley—seventy percent of the world’s internet traffic passes through a thirty-mile corridor. But in late 2024, local utility Dominion Energy delivered a historic shock: the transmission grid had reached total capacity. New data centers would have to wait up to seven years for power.",
        "beats": [
            ("LOUDOUN COUNTY VA", "DATA CENTER ALLEY", "Aerial drone shot over sprawling hyperscale data center buildings nestled among Virginia woodland at dawn."),
            ("70% OF WEB TRAFFIC", "THE INTERNET'S HEART", "Fiber optic junction vault under street pavement glowing with bundled glass cables in neon colors."),
            ("GRID REACHES MAX", "ZERO SPARE WATTS", "Heavy transmission substation in Northern Virginia with humming transformers surrounded by security fencing."),
            ("7-YEAR QUEUE", "THE INTERCONNECT DELAY", "A formal utility queue schedule document with dates stretching past 2032 stamped with PENDING."),
            ("THE REALITY CRASH", "CANNOT EXPAND", "A bulldozer parked motionless in an unfinished muddy construction lot behind an empty data center shell.")
        ]
    },
    {
        "id": 6, "act": 1, "title": "Utilities Issue The Red Alert",
        "timestamp": "1:40 - 2:00",
        "voiceover": "From PJM Interconnection in the Mid-Atlantic to ERCOT in Texas, regional grid operators raised emergency flags. Tech giants were demanding thousands of megawatts of baseload power faster than utilities could build transmission lines, threatening brownouts during peak summer heatwaves.",
        "beats": [
            ("RED ALERT ISSUED", "PJM & ERCOT WARN", "Command room of a regional power transmission authority with operators monitoring massive wall-sized grid telemetry map."),
            ("THOUSANDS OF MEGAWATTS", "INSATIABLE APPETITE", "High-voltage power transmission tower silhouetted against a dramatic fiery sunset in Texas."),
            ("BROWNOUT FEARS", "SUMMER PEAK RISK", "Suburban neighborhood street lights flickering in twilight as an air conditioning compressor hums loudly."),
            ("INFRASTRUCTURE LAG", "DECADE TO BUILD", "Construction crew erecting heavy steel lattice transmission pylons in rugged rural terrain."),
            ("THE GRID STANDOFF", "TECH VS UTILITIES", "Two heavy iron electrical connectors separated by a narrow gap, a bright electric arc bridging them.")
        ]
    },
    {
        "id": 7, "act": 1, "title": "The Physics of Artificial Intelligence",
        "timestamp": "2:00 - 2:20",
        "voiceover": "Silicon Valley software engineers spent decades in a world of zero marginal cost bits. But artificial intelligence operates in the realm of atoms. Every floating-point computation requires physical electrons, physical copper, and physical water for heat dissipation.",
        "beats": [
            ("BITS TO ATOMS", "THE PHYSICAL REALITY", "A microchip die resting on a rough chunk of raw iron and copper ore in dramatic studio lighting."),
            ("ELECTRONS IN COPPER", "PHYSICAL FRICTION", "Macro view of high-density copper busbars delivering thousands of amperes of DC current into server motherboard."),
            ("WATER FOR COOLING", "EVAPORATIVE DEMAND", "Industrial cooling tower discharging dense plumes of clean water vapor into cold night air."),
            ("ZERO MARGINAL COST ENDS", "EVERY TOKEN HAS A PRICE", "An open engineering notebook with thermodynamic equations handwritten beside a silicon microchip."),
            ("THE RECKONING", "PHYSICS WINS", "A heavy brass pendulum swinging slowly and inevitably across a dark stone floor.")
        ]
    },

    # --- ACT 2: BIG TECH'S ATOMIC DESPERATION (8 - 14) ---
    {
        "id": 8, "act": 2, "title": "Renewables Cannot Bridge The Baseload Gap",
        "timestamp": "2:20 - 2:40",
        "voiceover": "Tech companies initially promised to power their AI empires entirely with solar and wind. But AI data centers require 99.999% uptime—twenty-four hours a day, three hundred and sixty-five days a year. When the sun sets and the wind calms, renewables cannot keep a cluster running.",
        "beats": [
            ("THE BASELOAD TRAP", "24/7/365 DEMAND", "A sprawling solar farm at twilight as shadows lengthen and solar panels tilt horizontally toward dark sky."),
            ("WIND TURBINES CALM", "THE INTERMITTENCY FLAW", "Massive wind turbines standing completely still on a foggy hill with no wind stirring the blades."),
            ("99.999% UPTIME", "ZERO DOWNTIME TOLERANCE", "Close-up of a critical data center power distribution unit displaying stable 60Hz frequency reading."),
            ("BATTERY LIMITS", "HOURS NOT DAYS", "Industrial lithium-ion battery storage container installation enclosed in gravel yard under security lights."),
            ("THE HARD TRUTH", "GREEN DREAMS MEET REALITY", "Solar inverter station humming quietly as output meter drops toward zero at dusk.")
        ]
    },
    {
        "id": 9, "act": 2, "title": "Solar & Wind: The Intermittency Trap",
        "timestamp": "2:40 - 3:00",
        "voiceover": "To power a one-gigawatt data center continuously with solar energy, a tech company would need over forty square miles of solar panels and billions of dollars in battery backup that lasts only four hours. The land requirements and mineral costs made clean intermittency an economic impossibility.",
        "beats": [
            ("40 SQUARE MILES", "MASSIVE FOOTPRINT", "Aerial view showing endless blue solar panels blanketing an entire desert valley toward horizon."),
            ("4-HOUR BATTERIES", "CANNOT COVER STORMS", "Rows of heavy grey battery cabinets with cooling fans running in desert heat."),
            ("MINERAL SHORTAGE", "COPPER & LITHIUM", "Open-pit lithium or copper mine terraced into red earth with massive mining dump trucks operating."),
            ("ECONOMIC DEAD END", "COSTS SPIRAL", "Financial spreadsheet comparing nuclear baseload capital cost against massive solar-plus-storage setup."),
            ("THE PIVOT", "SEARCH FOR CLEAN BASELOAD", "Silhouette of a tech executive looking out of window toward distant industrial steam plumes.")
        ]
    },
    {
        "id": 10, "act": 2, "title": "Microsoft’s Three Mile Island Coup (Constellation Deal)",
        "timestamp": "3:00 - 3:20",
        "voiceover": "In September 2024, Microsoft made history. The tech titan signed an unprecedented twenty-year deal with Constellation Energy to restart Unit 1 of the Three Mile Island nuclear plant in Pennsylvania—rebranding it the Crane Clean Energy Center to secure eight hundred megawatts of dedicated carbon-free atomic power.",
        "beats": [
            ("THREE MILE ISLAND", "UNIT 1 RESTART", "Panoramic wide shot of Three Mile Island nuclear station along the Susquehanna River with iconic cooling towers."),
            ("800 MEGAWATTS", "DEDICATED TO AI", "Modern high-voltage switchyard outside Three Mile Island with heavy transmission lines stretching into distance."),
            ("20-YEAR CONTRACT", "CONSTELLATION DEAL", "Close-up of legal power purchase agreement document with corporate signatures and official corporate seals."),
            ("CRANE CLEAN ENERGY", "HISTORIC REBRANDING", "Architectural rendering of modernized entrance to Crane Clean Energy Center with clean glass facade."),
            ("ATOMIC MILESTONE", "THE FIRST TECH REACTOR", "Control room engineer seated at retrofitted digital instrumentation panel inside nuclear facility.")
        ]
    },
    {
        "id": 11, "act": 2, "title": "Amazon’s $650M Talen Energy Nuclear Campus",
        "timestamp": "3:20 - 3:40",
        "voiceover": "Not to be outdone, Amazon Web Services acquired a massive data center campus directly adjacent to the Susquehanna Nuclear Power Station in Pennsylvania for six hundred and fifty million dollars, signing an agreement to siphon up to nine hundred and sixty megawatts directly from the twin reactors.",
        "beats": [
            ("AMAZON BUYS ATOMIC", "$650M CAMPUS", "Aerial view of Amazon Web Services data center buildings situated directly next to a massive dual-unit nuclear plant."),
            ("SUSQUEHANNA TWINS", "960 MEGAWATTS", "The twin reactor containment domes and cooling towers of Susquehanna nuclear station illuminated by morning light."),
            ("DIRECT FEED", "BEHIND-THE-METER", "Heavy concrete electrical trench housing shielded high-voltage cables running straight from reactor to server building."),
            ("AWS INFRASTRUCTURE", "MASSIVE EXPANSION", "Security gatehouse of AWS Cumulus data center campus with high-tech badge scanners and perimeter fencing."),
            ("THE ATOMIC MONOPOLY", "BUYING POWER PLANTS", "A scale model of the nuclear-powered data center complex displayed in a corporate boardroom.")
        ]
    },
    {
        "id": 12, "act": 2, "title": "Google’s Bet on Kairos Power SMRs",
        "timestamp": "3:40 - 4:00",
        "voiceover": "Google took a different technological bet. Rather than reviving legacy twentieth-century reactors, Google partnered with Kairos Power to commission seven next-generation Small Modular Reactors utilizing molten fluoride salt cooling, committing to five hundred megawatts of atomic power by 2030.",
        "beats": [
            ("GOOGLE'S BET", "KAIROS POWER SMRs", "Futuristic architectural rendering of a sleek, compact Small Modular Reactor building with modern glass accents."),
            ("MOLTEN SALT COOLING", "ADVANCED PHYSICS", "Glowing amber-gold molten salt liquid flowing smoothly through polished stainless steel demonstration pipe."),
            ("SEVEN MODULAR PLANTS", "500 MEGAWATTS", "Cluster of seven compact modular reactor containment vessels arranged neatly on an industrial campus."),
            ("CLEAN CARBON-FREE", "THE 2030 TIMELINE", "Google headquarters campus in Mountain View California with modern glass architecture under sunny skies."),
            ("THE ADVANCED DAWN", "NEXT-GEN NUCLEAR", "Engineering team inspecting a precision-machined reactor core component in a high-tech lab.")
        ]
    },
    {
        "id": 13, "act": 2, "title": "Behind-the-Meter: Bypassing Public Utilities",
        "timestamp": "4:00 - 4:20",
        "voiceover": "What made these deals radical was their behind-the-meter architecture. By connecting server buildings directly to the nuclear generator before the power reaches the public transmission grid, tech giants effectively cut the line, bypassing public utility waiting queues entirely.",
        "beats": [
            ("BEHIND-THE-METER", "CUTTING THE QUEUE", "Diagrammatic visualization of an electrical circuit showing power flowing directly from generator to data center, bypassing public grid lines."),
            ("PUBLIC GRID BYPASSED", "NO WAITING IN LINE", "A highway bypass lane where high-speed traffic zips past a massive stagnant traffic jam on the main highway."),
            ("EXCLUSIVE ACCESS", "DEDICATED POWER", "Heavy padlocked electrical switchbox with exclusive industrial access badges displayed."),
            ("THE LEGAL GAMBIT", "PRIVATE POWER ISLAND", "An island of illuminated modern server buildings surrounded by darkness in a rural landscape."),
            ("THE PRIVILEGE", "BIG TECH INDEPENDENCE", "Corporate tech executive holding private electrical substation keys inside sleek company office.")
        ]
    },
    {
        "id": 14, "act": 2, "title": "The 20-Year Power Purchase Land Grab",
        "timestamp": "4:20 - 4:40",
        "voiceover": "A ruthless corporate land grab erupted across the energy sector. Tech giants deployed hundreds of billions in balance-sheet cash to lock up every available nuclear kilowatt-hour in North America for the next two decades, leaving traditional heavy industries and manufacturing stranded.",
        "beats": [
            ("20-YEAR LAND GRAB", "LOCKING UP THE ATOM", "Executive boardroom table covered in signed 20-year Power Purchase Agreements stamped with corporate seals."),
            ("MANUFACTURING STRANDED", "NO WATTS LEFT", "An older American steel or chemical factory in the Midwest sitting quiet with cool smokestacks in late afternoon."),
            ("HUNDREDS OF BILLIONS", "BALANCE SHEET ADVANTAGE", "Stack of corporate treasury bonds and contracts illuminated by focused desk lamp in dark room."),
            ("NUCLEAR MONOPOLY", "THE EXCLUSIVE CLUB", "A secure nuclear facility entrance gate with corporate access badges required for entry."),
            ("THE ENERGY DIVIDE", "TECH VS TRADITIONAL", "Split frame showing an ultra-modern glowing data center on left and an older darkened industrial plant on right.")
        ]
    },

    # --- ACT 3: THE REGULATORY & CITIZEN REVOLT (15 - 21) ---
    {
        "id": 15, "act": 3, "title": "FERC’s Historic Rejection of the Amazon Deal",
        "timestamp": "4:40 - 5:00",
        "voiceover": "In November 2024, the federal regulatory hammer fell. The Federal Energy Regulatory Commission voted two-to-one to reject the interconnection agreement between Amazon and the Susquehanna nuclear plant, declaring that diverting base-load nuclear power to Big Tech threatened public grid reliability.",
        "beats": [
            ("FERC VOTES NO", "HISTORIC REJECTION", "Hearing room of the Federal Energy Regulatory Commission with commissioners seated at wooden dais voting."),
            ("INTERCONNECT BLOCKED", "THE RULING", "Official FERC order document with bold black text reading 'ORDER REJECTING INTERCONNECTION AGREEMENT'."),
            ("AMAZON SHOCKED", "LEGAL ROADBLOCK", "Amazon corporate legal counsel in Washington DC reviewing regulatory ruling with grim expression."),
            ("COMMISSIONER'S REASON", "PUBLIC RELIABILITY", "Close-up of a commissioner speaking into a microphone with television news cameras filming in background."),
            ("THE PRECEDENT", "A CHILL OVER DEALS", "A heavy gavel resting on official sound block inside federal regulatory chamber under sharp lighting.")
        ]
    },
    {
        "id": 16, "act": 3, "title": "Co-location Controversy: Who Pays for the Grid?",
        "timestamp": "5:00 - 5:20",
        "voiceover": "Regulatory commissioners and state consumer advocates exposed the core economic injustice: if tech companies take nuclear power off the public grid, ordinary households and small businesses are forced to pay higher network transmission charges to maintain the remaining grid infrastructure.",
        "beats": [
            ("WHO PAYS THE BILL?", "THE ECONOMIC TRAP", "Balance scale with heavy stack of residential consumer electricity bills on one side, tiny corporate check on other."),
            ("CONSUMER ADVOCATES", "SPEAKING OUT", "State public utility consumer advocate standing before microphones holding up comparative utility cost charts."),
            ("NETWORK CHARGES SHIFT", "CITIZENS SUBSIDIZE", "Diagram showing transmission line maintenance costs being reallocated to residential neighborhood lines."),
            ("THE HIDDEN SUBSIDY", "CORPORATE PRIVILEGE", "Close-up of a residential utility bill line item marked 'SYSTEM RELIABILITY ADJUSTMENT' highlighted in yellow."),
            ("PUBLIC OUTCRY", "RISING RESENTMENT", "Suburban living room where a family examines an unexpectedly high electricity bill with concern.")
        ]
    },
    {
        "id": 17, "act": 3, "title": "Residential Bills Surge +20% to +35%",
        "timestamp": "5:20 - 5:40",
        "voiceover": "In states bordering data center clusters—from Virginia and Maryland to Texas and Ohio—residential utility rates surged between twenty and thirty-five percent. Working-class families discovered they were quietly subsidizing the electric bills of trillion-dollar artificial intelligence conglomerates.",
        "beats": [
            ("BILLS SURGE +35%", "THE SHOCK NUMBER", "Macro shot of a residential electric bill with final balance printed in bold red ink on kitchen table."),
            ("WORKING CLASS STRAIN", "KITCHEN TABLE CRISIS", "Senior citizen carefully counting currency notes beside unpaid utility envelope under soft lamp light."),
            ("REGIONAL CLUSTERS", "WHERE COSTS SPIKE", "Map of US states highlighting Mid-Atlantic and Texas in alarming bright amber and red shades."),
            ("PUBLIC COMMISSION MEETS", "TESTIMONY HEARD", "State Public Utility Commission hearing room with crowded gallery of concerned citizens listening intently."),
            ("INFLATION COMPOUNDED", "ENERGY POVERTY", "Suburban house at twilight with single kitchen light on as evening temperatures drop outside.")
        ]
    },
    {
        "id": 18, "act": 3, "title": "Public Anger at Town Hall Meetings",
        "timestamp": "5:40 - 6:00",
        "voiceover": "Town hall meetings across rural Pennsylvania, Virginia, and Georgia erupted into fiery shouting matches. Local citizens confronted county supervisors, demanding moratoria on data center construction and asking why their quiet pastoral communities were being converted into buzzing computer server hubs.",
        "beats": [
            ("TOWN HALL FURY", "CITIZENS REVOLT", "Crowded county auditorium with an angry resident speaking impassioned words at microphone on floor."),
            ("LOCAL OFFICIALS STUNNED", "FACING THE PUBLIC", "County commissioners seated at wooden dais listening defensively to heated public testimony."),
            ("MORATORIUM DEMANDED", "HALT CONSTRUCTION", "Citizens holding printed signs reading 'NO MORE DATA CENTERS' and 'PROTECT OUR POWER' in town hall."),
            ("PASTORAL TO INDUSTRIAL", "COMMUNITY LOST", "Peaceful green Virginia rural pasture adjacent to a massive grey concrete data center facility with security cameras."),
            ("THE RESISTANCE", "GRASSROOTS BATTLE", "Close-up of a community petition clipboard filled with hundreds of handwritten citizen signatures.")
        ]
    },
    {
        "id": 19, "act": 3, "title": "Environmentalists vs AI Data Centers",
        "timestamp": "6:00 - 6:20",
        "voiceover": "Environmental coalitions found themselves in an ideological dilemma. While tech leaders campaigned as green visionaries, their computing clusters were delaying coal plant retirements, demanding gas peaker plants, and consuming billions of gallons of drinking water for cooling.",
        "beats": [
            ("GREEN DILEMMA", "THE CLIMATE CRACK", "Pristine mountain stream flowing in foreground with towering coal-fired power plant smokestacks in background."),
            ("COAL RETIREMENTS DELAYED", "DIRTY POWER STAYS", "Industrial coal storage yard where bulldozers move dark mounds of coal under heavy grey skies."),
            ("GAS PEAKER PLANTS", "RUNNING FULL TILT", "Natural gas power generation plant running at full capacity with heat shimmering from exhaust stacks."),
            ("ENVIRONMENTAL PROTEST", "OUTSIDE TECH HQ", "Young environmental activists marching with banners outside a gleaming corporate tech headquarters entrance."),
            ("THE CONTRADICTION", "NET-ZERO PROMISES BROKEN", "A printed corporate sustainability brochure with green leaves resting in a wastepaper bin.")
        ]
    },
    {
        "id": 20, "act": 3, "title": "Water Scarcity: Draining Aquifers for Cooling",
        "timestamp": "6:20 - 6:40",
        "voiceover": "Beyond power, cooling an AI server cluster consumes millions of gallons of potable water every day through evaporative cooling towers. In drought-stressed Western basins like Arizona and Utah, server farms were accused of depleting subterranean aquifers that communities relied upon for agriculture.",
        "beats": [
            ("MILLIONS OF GALLONS", "WATER CONSUMPTION", "Massive water treatment manifold inside a data center utility building with huge blue pipes and pressure valves."),
            ("DROUGHT IN THE WEST", "DRY AQUIFERS", "Cracked mud lakebed in American West under intense sunlight with bleached driftwood."),
            ("FARMERS VS SERVERS", "THE WATER WAR", "An elderly farmer in denim shirt standing in a dry dusty irrigation canal looking toward distant server warehouse."),
            ("EVAPORATIVE TOWERS", "STEAM INTO DESERT AIR", "Massive rooftop cooling towers venting white clouds of evaporated water over a desert tech facility."),
            ("PRECIOUS RESOURCE", "EVERY DROP COUNTS", "Close macro shot of a clear glass of tap water reflecting a bright kitchen window.")
        ]
    },
    {
        "id": 21, "act": 3, "title": "The Transmission Line Bottleneck (10-Year Wait)",
        "timestamp": "6:40 - 7:00",
        "voiceover": "Even when power generation is available, moving electricity from nuclear plants to server farms requires high-voltage transmission corridors. In America, obtaining permits, negotiating rights-of-way, and constructing transmission lines takes an average of ten to twelve years.",
        "beats": [
            ("10-YEAR BOTTLENECK", "PERMITTING PURGATORY", "A thick stack of government environmental impact assessment binders on a desk with colored tabs."),
            ("RIGHT-OF-WAY BATTLES", "FARMERS RESIST", "A rural country fence line with a bright yellow 'NO TRESPASSING - TRANSMISSION CORRIDOR' sign posted."),
            ("CONSTRUCTION CREW", "HEAVY STEEL TOWERS", "Linemen in safety harnesses working hundreds of feet in the air on high-voltage transmission crossarms."),
            ("THE GRID ARTERIES", "TOO NARROW FOR POWER", "Aerial view of high-voltage transmission lines cutting a straight swath through dense green mountain forest."),
            ("THE REAL CHOKEPOINT", "CANNOT MOVE POWER", "A heavy steel transformer being transported on a massive 32-wheel specialized flatbed trailer along a highway.")
        ]
    },

    # --- ACT 4: THE SMR PROMISE VS INDUSTRIAL REALITY (22 - 28) ---
    {
        "id": 22, "act": 4, "title": "Small Modular Reactors: The Promised Savior",
        "timestamp": "7:00 - 7:20",
        "voiceover": "Confronted by public opposition and utility bottlenecks, Big Tech pinned its hopes on a revolutionary concept: Small Modular Reactors. Rather than building bespoke multi-billion-dollar gigawatt plants, SMRs promised factory-fabricated, modular reactors assembled directly on data center campuses.",
        "beats": [
            ("SMR REVOLUTION", "FACTORY-BUILT ATOMS", "Sleek high-tech factory assembly line where stainless steel nuclear containment modules are precision-manufactured."),
            ("MODULAR DESIGN", "COMPACT & SAFE", "3D architectural cutaway model of an underground Small Modular Reactor showing passive safety cooling pools."),
            ("ON-CAMPUS POWER", "SELF-CONTAINED AI", "Rendering of a modern AI data center with three compact cylindrical reactor buildings integrated into landscaping."),
            ("THE TECH VISION", "UNLIMITED ABUNDANCE", "Tech visionary presenting on stage at an innovation summit with glowing holographic reactor diagram."),
            ("THE PROMISE", "PLUG-AND-PLAY POWER", "Close-up of a precision nuclear fuel assembly model gleaming under studio gallery lighting.")
        ]
    },
    {
        "id": 23, "act": 4, "title": "NuScale, X-Energy, & Oklo: The SMR Landscape",
        "timestamp": "7:20 - 7:40",
        "voiceover": "A wave of advanced nuclear startups captured Silicon Valley’s capital. NuScale secured the first design approval from the Nuclear Regulatory Commission; X-Energy advanced high-temperature gas-cooled pebble-bed reactors; and Oklo, backed by Sam Altman, promoted fast fission micro-reactors.",
        "beats": [
            ("THE SMR LEADERS", "SILICON MEETS ATOM", "Executive logos and blueprints of NuScale, X-Energy, and Oklo displayed on clean digital drafting tablets."),
            ("PEBBLE-BED FUEL", "TRISO PARTICLES", "Macro view of spherical graphite-coated uranium TRISO fuel pebbles resting in a laboratory petri dish."),
            ("FAST FISSION DESIGN", "OKLO'S MICRO-REACTOR", "Futuristic rendering of an A-frame micro-reactor building integrated seamlessly into mountain scenery."),
            ("VENTURE BILLIONS", "INVESTORS BET BIG", "Silicon Valley venture capital partners gathered around an interactive touchscreen reviewing reactor deployment timelines."),
            ("THE NUCLEAR FRONTIER", "THE NEW PIONEERS", "Young nuclear engineers in clean blue lab coats smiling as they inspect advanced testing apparatus.")
        ]
    },
    {
        "id": 24, "act": 4, "title": "First-of-a-Kind Cost Overruns & NRC Timelines",
        "timestamp": "7:40 - 8:00",
        "voiceover": "But nuclear physics is unforgiving to software timelines. In early 2024, NuScale’s flagship commercial project in Utah was abruptly cancelled after projected electricity costs surged fifty percent to eighty-nine dollars per megawatt-hour. First-of-a-kind engineering always costs more and takes longer.",
        "beats": [
            ("UTAH PROJECT CANCELLED", "THE SMR REALITY", "Desert construction site in Idaho/Utah with marked surveyor stakes standing abandoned in cold wind."),
            ("COSTS SURGE +50%", "$89 PER MWh", "Financial cost-overrun document showing escalating capital expenditure projections on an analyst's desk."),
            ("NRC SCRUTINY", "YEARS OF LICENSING", "Nuclear Regulatory Commission hearing room in Rockville Maryland with thick regulatory binders lining shelves."),
            ("THE TIME DISCONNECT", "MONTHS VS DECADES", "Dual clocks on a wall: a digital stopwatch ticking rapidly beside an antique stone sundial."),
            ("THE FIRST-OF-A-KIND CURSE", "PROTOTYPES ARE HARD", "Industrial testing facility with complex stainless steel piping under pressure testing with gauges.")
        ]
    },
    {
        "id": 25, "act": 4, "title": "Uranium Fuel Enrichment: The Russian Bottleneck (HALEU)",
        "timestamp": "8:00 - 8:20",
        "voiceover": "Even if the reactors were built tomorrow, an invisible geopolitical trap awaited. Advanced SMRs require High-Assay Low-Enriched Uranium—enriched up to twenty percent. Currently, only one country in the world produces commercial quantities of this specialized fuel: the Russian Federation.",
        "beats": [
            ("HALEU FUEL", "THE CRITICAL BOTTLENECK", "Close macro shot of a sealed titanium canister labeled with radiation trefoil and 'HALEU 19.75%'."),
            ("RUSSIAN MONOPOLY", "TENEX ENRICHMENT", "Vast centrifuge hall of a Russian uranium enrichment facility with thousands of tall spinning silver cylinders."),
            ("WESTERN SHORTAGE", "ZERO DOMESTIC SUPPLY", "Empty storage rack in an American nuclear logistics facility with warning tape across bay."),
            ("GEOPOLITICAL LEVERAGE", "MOSCOW'S CARDS", "The Kremlin towers in Moscow illuminated at twilight under snow flurries."),
            ("THE FUEL CHOKEPOINT", "NO CHIPS WITHOUT FUEL", "Stylized representation of a chessboard where a nuclear fuel assembly stands between two flags.")
        ]
    },
    {
        "id": 26, "act": 4, "title": "Geopolitical Nuclear Fuel Supply Chains",
        "timestamp": "8:20 - 8:40",
        "voiceover": "Congress passed emergency legislation banning Russian enriched uranium imports, forcing the United States and allied nations into a multi-billion-dollar race to stand up domestic enrichment centrifuges in Ohio and New Mexico—a rebuilding process that will take until at least 2029.",
        "beats": [
            ("CONGRESSIONAL EMBARGO", "BANNING RUSSIAN FUEL", "The floor of the US Senate with lawmakers voting on the Prohibiting Russian Uranium Imports Act."),
            ("OHIO CENTRIFUGE RACE", "AMERICAN CENTUS", "American centrifuge demonstration plant in Piketon Ohio with technicians inspecting uranium hexafluoride pipes."),
            ("2029 TIMELINE", "CANNOT HURRY CENTRIFUGES", "Architectural timeline banner at a nuclear construction site with milestones marked into the late 2020s."),
            ("ALLIED COLLABORATION", "URANCO & ORANO", "European uranium enrichment plant in Almelo Netherlands with clean industrial buildings and security patrols."),
            ("THE SUPPLY SHIELD", "INDEPENDENCE RACE", "A heavy steel transport cask for nuclear material loaded onto a secure transport rail car.")
        ]
    },
    {
        "id": 27, "act": 4, "title": "Wall Street Realizes SMRs Won’t Arrive Before 2030",
        "timestamp": "8:40 - 9:00",
        "voiceover": "On Wall Street, investment analysts completed a sobering reassessment. Small Modular Reactors would not deliver commercial power to artificial intelligence clusters until 2032 or beyond. The gap between today's exponential AI demand and nuclear power delivery was an eight-year void.",
        "beats": [
            ("THE 2030 GAP", "AN 8-YEAR VOID", "Deep chasms in an arid canyon under twilight with a broken suspension bridge stretching halfway across."),
            ("ANALYSTS SOBER UP", "REALITY PRICED IN", "Wall Street energy research analyst taking off glasses and rubbing temples over spreadsheet revisions."),
            ("EXPONENTIAL MEETS LINEAR", "THE DIVERGENCE", "A dual chart showing AI compute demand climbing vertically while nuclear capacity crawls horizontally."),
            ("INVESTOR REALLOCATION", "HYPE RESET", "Stock terminal displaying sharp pullbacks in speculative nuclear and SMR startup equity tickers."),
            ("THE WAITING ROOM", "NO SHORTCUTS", "An empty modern industrial waiting room with large windows looking out on an empty field.")
        ]
    },
    {
        "id": 28, "act": 4, "title": "The Interim Bridge: Natural Gas & Coal Revival",
        "timestamp": "9:00 - 9:20",
        "voiceover": "To bridge this brutal eight-year void, tech giants quietly did what they swore they never would: they signed long-term contracts with natural gas combined-cycle power plants, and utilities delayed the retirement of fossil-fuel infrastructure across the American heartland.",
        "beats": [
            ("THE FOSSIL BRIDGE", "UNCOMFORTABLE TRUTH", "A modern natural gas power plant at dusk with three large exhaust stacks emitting clear heat waves."),
            ("NATURAL GAS PIPELINES", "PUMPING ENERGY", "Heavy steel natural gas compressor station in Pennsylvania humming along an interstate pipeline corridor."),
            ("COAL PLANT EXTENSIONS", "HEARTLAND REALITY", "An imposing coal plant in Indiana with rail cars of coal arriving under dramatic storm clouds."),
            ("SILENT CONTRACTS", "REALPOLITIK ENERGY", "A corporate legal document titled 'POWER SUPPLY SERVICE AGREEMENT' with gas utility signature lines."),
            ("PRAGMATISM WINS", "KEEP THE LIGHTS ON", "A glowing computer monitor in a dark room showing active GPU computation funded by gas turbine power.")
        ]
    },

    # --- ACT 5: THE GEOPOLITICS OF POWER & COMPUTE (29 - 36) ---
    {
        "id": 29, "act": 5, "title": "The Sovereign Compute Hierarchy",
        "timestamp": "9:20 - 9:40",
        "voiceover": "In the emerging world order, national power is no longer measured solely in aircraft carriers or gold reserves; it is measured in terawatt-hours of sovereign compute. Nations that can generate cheap, continuous, carbon-free energy will dominate the global artificial intelligence economy.",
        "beats": [
            ("SOVEREIGN COMPUTE", "THE NEW CURRENCY", "Conceptual visualization of a futuristic sovereign digital vault combining electrical towers and supercomputers."),
            ("CARRIERS TO COMPUTE", "SHIFT IN POWER", "A naval aircraft carrier at sea at dusk side-by-side with an illuminated nuclear data center facility."),
            ("CHEAP CLEAN ENERGY", "NATIONAL ADVANTAGE", "Massive hydroelectric dam with roaring white water under sunny skies producing clean baseload."),
            ("GLOBAL RANKINGS", "WHO CONTROLS INTELLIGENCE", "Digital global leaderboard ranking nations by gigawatts of operational compute infrastructure."),
            ("THE STRATEGIC CHESSBOARD", "ENERGY SOVEREIGNTY", "A polished marble globe surrounded by carved chess pieces representing world superpowers.")
        ]
    },
    {
        "id": 30, "act": 5, "title": "Whomever Controls Power Controls Intelligence",
        "timestamp": "9:40 - 10:00",
        "voiceover": "The ultimate lesson of the AI energy crisis is definitive: software algorithms are commoditized and easily replicated, but access to baseload electricity is finite and strictly governed by geography. Whomever controls the power grid controls the intelligence of the planet.",
        "beats": [
            ("ALGORITHMS ARE CHEAP", "CODE IS COMMODITIZED", "Open-source software code scrolling in green text across a dark terminal screen."),
            ("WATTS ARE FINITE", "PHYSICAL LIMITS", "A heavy brass master electrical knife switch on an industrial slate switchboard under single spotlight."),
            ("GEOGRAPHY OF POWER", "BLESSED BASINS", "Satellite view of Earth at night showing intense concentrations of electric light in energy-rich regions."),
            ("THE ULTIMATE LEVERAGE", "WHO HAS THE SWITCH", "Silhouette of a grid operator's hand hovering over a master power control button."),
            ("THE REAL EMPIRE", "ATOMS OVER BITS", "A giant bronze statue of Prometheus holding fire, standing outside an imposing modern power station.")
        ]
    },
    {
        "id": 31, "act": 5, "title": "China’s Nuclear Buildout vs Western Slowness",
        "timestamp": "10:00 - 10:20",
        "voiceover": "While Western tech companies fight ten-year regulatory battles for transmission permits, China is currently constructing thirty modern commercial nuclear reactors simultaneously, deploying state-backed capital to build an uninterrupted atomic infrastructure grid.",
        "beats": [
            ("CHINA'S ATOMIC SPREE", "30 REACTORS AT ONCE", "Massive construction site of a modern coastal nuclear power plant in Guangdong China with multiple cranes."),
            ("STATE DIRECTIVE", "COMPLETION IN 5 YEARS", "Chinese nuclear engineers reviewing blueprints on an active reactor containment pad at sunset."),
            ("WESTERN REGULATORY LAG", "PERMIT PARALYSIS", "A lonely gavel sitting beside years of unapproved environmental impact assessments in a US office."),
            ("THE SPEED DIVIDE", "INFRASTRUCTURE VELOCITY", "High-speed rail line speeding smoothly past an operational Chinese nuclear cooling tower."),
            ("THE GEOPOLITICAL SQUEEZE", "WHO WINS THE DECADE", "Global map comparing nuclear construction timelines between Western democracies and Asia.")
        ]
    },
    {
        "id": 32, "act": 5, "title": "The New Power Magnates: Utilities Become Tech Titans",
        "timestamp": "10:20 - 10:40",
        "voiceover": "The balance of power on Wall Street has shifted. Electric utilities and independent power producers—once considered sleepy dividend investments—have become the most sought-after growth stocks on the market. Constellation, Vistra, and Talen Energy trade like hyper-growth tech titans.",
        "beats": [
            ("THE NEW MAGNATES", "UTILITIES BECOME GIANTS", "Stock market ticker board showing utility stocks surging in bright green while tech stocks stall."),
            ("CONSTELLATION & VISTRA", "ATOMIC WINNERS", "The corporate headquarters building of a major independent nuclear power producer glowing at night."),
            ("SLEEPY DIVIDENDS NO MORE", "THE GROWTH DARLINGS", "Investment banker on Wall Street presenting an aggressive growth pitch deck for utility equities."),
            ("THE POWER PRICING POWER", "SETTING THE TARIFFS", "An executive signing a long-term electricity contract with lucrative indexed capacity rates."),
            ("THE REVERSAL", "POWER OVER SOFTWARE", "Antique electrical porcelain insulator sitting proudly on a CEO's mahogany desk beside a laptop.")
        ]
    },
    {
        "id": 33, "act": 5, "title": "Efficiency Innovations: Optical Computing & Liquid Cooling",
        "timestamp": "10:40 - 11:00",
        "voiceover": "Pushed to the brink by physical energy constraints, the technology sector is pioneering radical engineering breakthroughs: optical computing using light instead of electricity, direct-to-chip liquid cooling with synthetic fluorochemicals, and neuromorphic computing architectures.",
        "beats": [
            ("RADICAL EFFICIENCY", "BEYOND SILICON", "Ultra-modern optical computing chip with microscopic lasers transmitting pulses of multicolored light."),
            ("DIRECT-TO-CHIP LIQUID", "IMMERSION TANKS", "Clear synthetic dielectric fluid bubbling gently over glowing server motherboards in an immersion tank."),
            ("LIGHT OVER ELECTRONS", "ZERO HEAT LOSS", "Macro laser refraction through a precision silicon prism creating vibrant optical spectrum."),
            ("NEUROMORPHIC CHIPS", "MIMICKING THE BRAIN", "Microscopic view of a brain-inspired neuromorphic computing processor with organic-style circuit layout."),
            ("ENGINEERING TRIUMPH", "DOING MORE WITH LESS", "Chief research scientist examining a glowing prototype wafer through protective safety goggles.")
        ]
    },
    {
        "id": 34, "act": 5, "title": "The Investment Playbook: Uranium, Infrastructure & SMRs",
        "timestamp": "11:00 - 11:20",
        "voiceover": "For astute investors, the AI energy chokehold defines the most asymmetric investment playbook of the decade: physical uranium miners, specialized nuclear enrichment providers, heavy electrical transformer manufacturers, and utility infrastructure operators.",
        "beats": [
            ("THE ASYMMETRIC PLAYBOOK", "HARD ASSET WINNERS", "A physical yellowcake uranium sample in an acrylic museum block beside shiny copper wire spools."),
            ("URANIUM MINERS", "THE ATOMIC FUEL", "Underground uranium mine tunnel in Saskatchewan Canada with heavy automated extraction equipment."),
            ("TRANSFORMER BUILDERS", "THE HARDWARE HEROES", "Heavy electrical engineering factory where giant copper windings for 500kV transformers are assembled."),
            ("INVESTMENT HORIZON", "THE DECADAL TREND", "An institutional portfolio allocation chart showing heavy overweights in energy infrastructure and nuclear."),
            ("SMART MONEY POSITIONED", "AHEAD OF THE HERD", "Hand placing a solid gold and copper token on the winning sector of a financial investment board.")
        ]
    },
    {
        "id": 35, "act": 5, "title": "The Long Road to Nuclear Abundance",
        "timestamp": "11:20 - 11:40",
        "voiceover": "The journey to clean energy abundance will not be cheap or painless. It will require over one trillion dollars in grid transmission modernizations, a complete overhaul of Western regulatory permitting, and a cultural embrace of the atom as humanity’s safest, densest source of clean power.",
        "beats": [
            ("THE $1T GRID OVERHAUL", "MODERNIZING AMERICA", "Massive civil infrastructure project with engineers installing high-capacity superconducting underground cables."),
            ("REGULATORY OVERHAUL", "CLEARING THE RED TAPE", "Official legislative reform document signed into law on Capitol Hill with pens resting on parchment."),
            ("EMBRACING THE ATOM", "THE SAFEST POWER", "Dramatic low-angle view of a clean white nuclear cooling tower releasing pure condensation into sunset sky."),
            ("HUMANITY'S DENSEST FUEL", "ENERGY DENSITY", "A single uranium ceramic fuel pellet resting in an open hand, illustrating its energy equivalence to a ton of coal."),
            ("THE PATH FORWARD", "ENGINEERING AUSTERE BEAUTY", "A clean futuristic electrical transmission corridor vanishing peacefully into distant green mountains.")
        ]
    },
    {
        "id": 36, "act": 5, "title": "Final Verdict: The Atomic Age of AI",
        "timestamp": "11:40 - 12:00",
        "voiceover": "Artificial intelligence and nuclear power were both born in the middle of the twentieth century. Now, in the twenty-first century, their destinies have converged. The digital mind has met the atomic fire, and together, they will reshape human civilization.",
        "beats": [
            ("TWO GIANTS CONVERGE", "MIND & ATOM", "Stunning conceptual cinematic shot: a glowing human neural network visualization intertwining with the atomic structure of uranium."),
            ("BORN IN 20TH CENTURY", "MEETING IN 21ST", "Historic black-and-white archive photos of early computing and atomic research blending into modern 4K digital realism."),
            ("THE NEW CIVILIZATION", "ENERGY & INTELLIGENCE", "Futuristic cityscape at dawn powered by clean atomic reactors and automated intelligence systems."),
            ("THE BULL PRINT", "SUBSCRIBE & STAY AHEAD", "Signature high-CTR YouTube end-screen: sleek dark 3D gold embossed channel logo '@TheBullPrint'."),
            ("FINAL BLACKOUT", "THE ATOMIC PULSE", "Cinematic blackout where a single golden particle pulses gently and fades into deep timeless dark.")
        ]
    }
]

def generate_script():
    print(f"Building complete chapters_script.py for Doc #3 with {len(SEGMENTS_DATA)} segments...")
    lines = [
        "#!/usr/bin/env python3",
        '"""',
        "THE ENERGY GRID CHOKEHOLD: Why Big Tech Is Buying Nuclear Reactors for AI",
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
