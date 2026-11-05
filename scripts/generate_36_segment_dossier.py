"""
36 Segments Breakdown for 12-Minute Long-Format Standard YouTube Documentary:
'THE $32 BILLION ILLUSION: The Criminal Rise and Fall of FTX & Alameda Research'
Cadence: Exactly 1 Frame every 20 Seconds (36 Frames Total for 720 Seconds)
Resolution: 2560x1440 (2K 16:9 Landscape)
"""

SEGMENTS = [
    # --- PROLOGUE: THE CITADEL & THE MYTH (00:00 - 02:00) ---
    {
        "seg": 1,
        "time": "00:00 - 00:20",
        "chapter": "PROLOGUE: THE CITADEL",
        "script": (
            "In November 2022, inside a thirty-million-dollar penthouse overlooking the turquoise waters "
            "of the Bahamas, a thirty-year-old billionaire sat in cargo shorts, furiously typing on a mechanical keyboard. "
            "To the outside world, Sam Bankman-Fried was the undisputed crown prince of modern finance."
        ),
        "visual_prompt": (
            "Cinematic ultra-wide establishing shot of an opulent dark glass penthouse in the Bahamas at twilight, "
            "glowing curved Bloomberg terminals on a dark teak desk, turquoise Caribbean ocean visible through floor-to-ceiling glass, "
            "moody chiaroscuro lighting, HBO documentary style, 35mm film still, photorealistic 8k, no text"
        ),
        "eyebrow": "PROLOGUE // NASSAU, THE BAHAMAS",
        "headline": "THE $30,000,000 CITADEL",
        "emphasis": "THE $32B ILLUSION",
        "subtext": "Behind locked doors, a thirty-year-old billionaire ran a secret financial empire.",
        "accent": "Emerald"
    },
    {
        "seg": 2,
        "time": "00:20 - 00:40",
        "chapter": "PROLOGUE: THE CITADEL",
        "script": (
            "He was profiled on the front cover of Forbes. Billed as the next J.P. Morgan. "
            "A mathematical savant who built a thirty-two billion dollar crypto empire in less than three years, "
            "trusted by institutional titans and everyday investors with over sixteen billion dollars in customer deposits."
        ),
        "visual_prompt": (
            "Cinematic shot of high-speed industrial printing presses churning out glossy business magazines, "
            "spotlights cutting through paper dust, bold magazine cover featuring curly-haired tech founder, "
            "dramatic editorial lighting, Wall Street thriller aesthetic, 35mm film still, photorealistic 8k, no text"
        ),
        "eyebrow": "MEDIA APOTHEOSIS // SILICON VALLEY",
        "headline": "THE FORBES SAVIOR",
        "emphasis": "THE NEXT J.P. MORGAN",
        "subtext": "Financial media and elite venture firms crowned him the future of capitalism.",
        "accent": "Amber"
    },
    {
        "seg": 3,
        "time": "00:40 - 01:00",
        "chapter": "PROLOGUE: THE CITADEL",
        "script": (
            "Elite Silicon Valley venture firm Sequoia Capital declared him the world's first future trillionaire. "
            "They famously swooned over pitch meetings where he played video games while casually closing "
            "hundred-million-dollar funding rounds without surrendering a single corporate board seat."
        ),
        "visual_prompt": (
            "Cinematic high-contrast shot of a Sand Hill Road venture boardroom at dusk, luxury leather chairs around a marble table, "
            "an open glowing laptop displaying video game graphics juxtaposed against multi-million-dollar term sheets, "
            "golden hour haze, David Fincher cinematography, 35mm film still, no text"
        ),
        "eyebrow": "VENTURE CAPITAL // SILICON VALLEY",
        "headline": "THE FUTURE TRILLIONAIRE",
        "emphasis": "$1.9B IN UNCHECKED EQUITY",
        "subtext": "Sequoia Capital wired hundreds of millions without demanding a single board seat.",
        "accent": "Cyan"
    },
    {
        "seg": 4,
        "time": "01:00 - 01:20",
        "chapter": "PROLOGUE: THE CITADEL",
        "script": (
            "In Washington D.C., politicians lined up to shake his hand. He poured seventy million dollars "
            "into political campaigns, testified before congressional committees, and positioned himself as the trusted, "
            "sensible insider begging regulators to create transparent market rules."
        ),
        "visual_prompt": (
            "Cinematic shot of grand United States Capitol congressional hearing room, dark mahogany benches, microphones, "
            "flashing press cameras in background, atmospheric smoke and beam lighting, authentic political documentary cinematography, 35mm film still, no text"
        ),
        "eyebrow": "CAPITOL HILL // SENATE TESTIMONY",
        "headline": "WASHINGTON'S DARLING",
        "emphasis": "$70M IN POLITICAL ALPHA",
        "subtext": "Preaching regulatory transparency while concealing the deepest financial black hole.",
        "accent": "Amber"
    },
    {
        "seg": 5,
        "time": "01:20 - 01:40",
        "chapter": "PROLOGUE: THE CITADEL",
        "script": (
            "He preached Effective Altruism: the gospel of accumulating unfathomable wealth solely to donate "
            "every dollar to save humanity. He drove a battered Toyota Corolla and slept on an office beanbag. "
            "It was the ultimate, irresistible moral camouflage."
        ),
        "visual_prompt": (
            "Cinematic shot of a rumpled beanbag and a battered car key sitting on a high-gloss polished marble penthouse floor, "
            "contrasting poverty props against immense luxury, surreal chiaroscuro lighting, editorial documentary framing, 35mm film still, no text"
        ),
        "eyebrow": "PHILOSOPHICAL SMOKESCREEN",
        "headline": "THE EFFECTIVE ALTRUIST",
        "emphasis": "THE BEANBAG DECEPTION",
        "subtext": "Cultivating an unpretentious persona to deflect forensic financial scrutiny.",
        "accent": "Emerald"
    },
    {
        "seg": 6,
        "time": "01:40 - 02:00",
        "chapter": "PROLOGUE: THE CITADEL",
        "script": (
            "There was only one problem. The entire empire was built on a lie. "
            "Deep inside FTX's core codebase, buried beneath thousands of lines of JavaScript, lay a secret backdoor: "
            "an algorithmic rule that siphoned customer deposits directly into his private hedge fund."
        ),
        "visual_prompt": (
            "Cinematic macro shot of glowing server racks in darkness, reflection of cascading green and red code on glass partitions, "
            "ominous true crime documentary lighting, dramatic red warning pulses, 35mm film still, photorealistic 8k, no text"
        ),
        "eyebrow": "CRIMINAL FORENSIC AUDIT // EXHIBIT 01",
        "headline": "THE SECRET BACKDOOR",
        "emphasis": "$8,000,000,000 DRAINED",
        "subtext": "A single hardcoded exemption granted his private fund unlimited customer cash.",
        "accent": "Crimson"
    },

    # --- CHAPTER 1: THE INFINITE MONEY GLITCH (02:00 - 04:20) ---
    {
        "seg": 7,
        "time": "02:00 - 02:20",
        "chapter": "CHAPTER 1: THE INFINITE MONEY GLITCH",
        "script": (
            "To understand how thirty-two billion dollars evaporated, we have to travel back to 2017 in Berkeley, California. "
            "Sam Bankman-Fried was an MIT physics graduate and an ambitious junior trader from Jane Street Capital, "
            "one of Wall Street's most ruthless quantitative trading firms."
        ),
        "visual_prompt": (
            "Cinematic shot of a dark quantitative trading trading floor at night, multiple glowing monitors showing mathematical models "
            "and algorithmic order flow, coffee cups and chalkboards filled with probability formulas, 35mm film still, no text"
        ),
        "eyebrow": "WALL STREET ORIGINS // JANE STREET",
        "headline": "THE QUANT GENESIS",
        "emphasis": "HIGH-FREQUENCY ARBITRAGE",
        "subtext": "Trained in statistical arbitrage and ruthless high-stakes probability games.",
        "accent": "Cyan"
    },
    {
        "seg": 8,
        "time": "02:20 - 02:40",
        "chapter": "CHAPTER 1: THE INFINITE MONEY GLITCH",
        "script": (
            "In late 2017, Sam discovered a massive inefficiency: the Kimchi Premium. "
            "Bitcoin was trading up to thirty percent higher in Japan and South Korea than in the West. "
            "By setting up complex international banking corridors, his new fund, Alameda Research, printed twenty million dollars in pure profit."
        ),
        "visual_prompt": (
            "Cinematic split-screen visual metaphor: Tokyo electronic trading district at night juxtaposed against San Francisco financial skyscrapers, "
            "golden digital laser connection bridging global currencies, 35mm film still, no text"
        ),
        "eyebrow": "BERKELEY, CALIFORNIA // 2017",
        "headline": "THE KIMCHI PREMIUM",
        "emphasis": "+30% DAILY SPREAD",
        "subtext": "Exploiting global price gaps between Tokyo and California to launch Alameda.",
        "accent": "Emerald"
    },
    {
        "seg": 9,
        "time": "02:40 - 03:00",
        "chapter": "CHAPTER 1: THE INFINITE MONEY GLITCH",
        "script": (
            "In 2019, Sam realized that trading on other exchanges was limited. He wanted to own the casino. "
            "He launched FTX: 'Built by traders, for traders.' His pitch was institutional execution, low fees, "
            "and a mathematically infallible auto-liquidation risk engine."
        ),
        "visual_prompt": (
            "Cinematic shot of a high-tech trading terminal displaying an institutional crypto exchange interface, "
            "glowing order books, green and red depth charts, futuristic metallic branding, 35mm film still, no text"
        ),
        "eyebrow": "EXCHANGE ARCHITECTURE // 2019",
        "headline": "THE DIGITAL CASINO",
        "emphasis": "BUILT BY TRADERS",
        "subtext": "Promising retail traders an automated risk engine that eliminated bad debt.",
        "accent": "Cyan"
    },
    {
        "seg": 10,
        "time": "03:00 - 03:20",
        "chapter": "CHAPTER 1: THE INFINITE MONEY GLITCH",
        "script": (
            "To finance rapid expansion, Sam minted his own cryptocurrency: the FTT token. "
            "FTX created hundreds of millions of tokens out of thin air, locked up the vast majority to starve the circulating supply, "
            "and engineered the public market price straight into the stratosphere."
        ),
        "visual_prompt": (
            "Cinematic macro shot of an intricately engraved dark gold digital token spinning on a reflective glass surface, "
            "golden circuitry and neon blue holographic telemetry, 35mm macro cinematography, no text"
        ),
        "eyebrow": "ALGORITHMIC MECHANICS // TOKENOMICS",
        "headline": "THE FTT TOKEN FLYWHEEL",
        "emphasis": "PRINTING FAKE WEALTH",
        "subtext": "Starving public supply to manipulate market capitalization into the tens of billions.",
        "accent": "Amber"
    },
    {
        "seg": 11,
        "time": "03:20 - 03:40",
        "chapter": "CHAPTER 1: THE INFINITE MONEY GLITCH",
        "script": (
            "Then came the financial sleight of hand. Alameda Research took billions in these illiquid, "
            "self-created FTT tokens and pledged them as collateral to borrow real customer US dollars and Bitcoin from FTX. "
            "It was an infinite money glitch backed by paper smoke."
        ),
        "visual_prompt": (
            "Cinematic 3D concept: A glowing gold coin balancing precariously on a collapsing house of credit cards, "
            "deep dark void background, volumetric smoke, dramatic high-contrast lighting, 35mm film still, no text"
        ),
        "eyebrow": "LEVERAGE CASCADE // COLLATERAL FRAUD",
        "headline": "THE INFINITE GLITCH",
        "emphasis": "BORROWING REAL DOLLARS",
        "subtext": "Using illiquid paper tokens to withdraw billions in customer cash.",
        "accent": "Crimson"
    },
    {
        "seg": 12,
        "time": "03:40 - 04:00",
        "chapter": "CHAPTER 1: THE INFINITE MONEY GLITCH",
        "script": (
            "To prevent Alameda from ever getting wiped out during a market crash, Sam instructed his chief engineer "
            "to hardcode a backdoor into FTX's database: a variable named allow_negative_balance set to true. "
            "Alameda was exempt from liquidation."
        ),
        "visual_prompt": (
            "Cinematic extreme macro close-up of computer screen code in darkness, amber text highlighting allow_negative_balance = true, "
            "green cursor blinking, authentic forensic code inspection cinematography, 35mm film still, no text"
        ),
        "eyebrow": "FORENSIC CODE AUDIT // GIT REPOSITORY",
        "headline": "ALLOW_NEGATIVE_BALANCE",
        "emphasis": "COLLATERAL-FREE CREDIT",
        "subtext": "Retail accounts were liquidated instantly; Alameda was given an infinite credit line.",
        "accent": "Crimson"
    },
    {
        "seg": 13,
        "time": "04:00 - 04:20",
        "chapter": "CHAPTER 1: THE INFINITE MONEY GLITCH",
        "script": (
            "While everyday retail accounts were mercilessly liquidated on a 5% drop, Alameda was allowed "
            "to run a sixty-five-billion-dollar line of credit with zero margin calls. "
            "They were gambling with customer life savings on high-risk venture bets, with zero accountability."
        ),
        "visual_prompt": (
            "Cinematic concept: A massive industrial bank vault door swung wide open, showing an empty cavernous chamber inside with "
            "red emergency lights flashing, dramatic chiaroscuro thriller lighting, 35mm film still, no text"
        ),
        "eyebrow": "SHADOW COMMINGLING // AUDIT",
        "headline": "$65 BILLION CREDIT LINE",
        "emphasis": "ZERO MARGIN CALLS",
        "subtext": "Customer deposits were treated as free capital for high-risk speculative bets.",
        "accent": "Crimson"
    },

    # --- CHAPTER 2: THE SEDUCTION OF WALL STREET (04:20 - 06:40) ---
    {
        "seg": 14,
        "time": "04:20 - 04:40",
        "chapter": "CHAPTER 2: THE SEDUCTION OF WALL STREET",
        "script": (
            "By 2021, FTX went on the most aggressive marketing binge in corporate history. "
            "They paid one hundred and thirty-five million dollars for the naming rights to the Miami Heat's NBA arena, "
            "slapping the FTX logo across downtown Miami."
        ),
        "visual_prompt": (
            "Cinematic wide exterior shot of a massive futuristic sports arena glowing under neon cyan and purple city lights at night, "
            "palms swaying, crowds entering under giant glowing corporate signage, 35mm film still, no text"
        ),
        "eyebrow": "MIAMI, FLORIDA // 2021",
        "headline": "THE $135M ARENA DEAL",
        "emphasis": "BUYING MAINSTREAM TRUST",
        "subtext": "Plastering the FTX logo across professional sports to lure retail investors.",
        "accent": "Cyan"
    },
    {
        "seg": 15,
        "time": "04:40 - 05:00",
        "chapter": "CHAPTER 2: THE SEDUCTION OF WALL STREET",
        "script": (
            "They bought a multi-million-dollar Super Bowl commercial starring Larry David, warning viewers "
            "not to miss out on the next big revolution. They signed NFL legend Tom Brady, Steph Curry, "
            "and Naomi Osaka as equity brand ambassadors."
        ),
        "visual_prompt": (
            "Cinematic shot of a Hollywood television studio soundstage, bright cinema spotlights, director chairs, "
            "monitors displaying commercial takes, high-gloss commercial cinematography, 35mm film still, no text"
        ),
        "eyebrow": "SUPER BOWL ADS // HOLLYWOOD",
        "headline": "DON'T MISS OUT",
        "emphasis": "CELEBRITY ENDORSEMENTS",
        "subtext": "A-list cultural icons convinced millions that FTX was as safe as a commercial bank.",
        "accent": "Amber"
    },
    {
        "seg": 16,
        "time": "05:00 - 05:20",
        "chapter": "CHAPTER 2: THE SEDUCTION OF WALL STREET",
        "script": (
            "Wall Street succumbed completely. The world's top institutional funds—Sequoia, Temasek, "
            "the Ontario Teachers' Pension Plan, and SoftBank—competed to wire billions of dollars into FTX, "
            "skipping basic accounting audits and demanding zero board seats."
        ),
        "visual_prompt": (
            "Cinematic shot of high-end corporate skyscraper boardroom overlooking Manhattan skyline at night, "
            "luxurious leather binders, polished glass tables reflecting green financial stock tickers, 35mm film still, no text"
        ),
        "eyebrow": "VENTURE CAPITAL BLINDSPOT",
        "headline": "INSTITUTIONAL FOMO",
        "emphasis": "$1.9B IN UNCHECKED EQUITY",
        "subtext": "Top venture firms handed over billions without demanding independent accounting audits.",
        "accent": "Emerald"
    },
    {
        "seg": 17,
        "time": "05:20 - 05:40",
        "chapter": "CHAPTER 2: THE SEDUCTION OF WALL STREET",
        "script": (
            "Sequoia famously published a glowing manifesto worshipping Sam. They recounted a pitch meeting "
            "where Sam played League of Legends on his laptop while answering partner questions, concluding: "
            "'I love this founder. He has an 11 out of 10 intellect.'"
        ),
        "visual_prompt": (
            "Cinematic close-up of high-end printed venture capital manifesto on heavy cream cardstock, golden embossed text, "
            "moody spotlighting from library desk lamp, 35mm film grain, no text"
        ),
        "eyebrow": "SEQUOIA CAPITAL // MANIFESTO",
        "headline": "THE 11 OUT OF 10 FOUNDER",
        "emphasis": "THE GAMER PITCH",
        "subtext": "Venture partners mistook casual disrespect for transcendent mathematical genius.",
        "accent": "Amber"
    },
    {
        "seg": 18,
        "time": "05:40 - 06:00",
        "chapter": "CHAPTER 2: THE SEDUCTION OF WALL STREET",
        "script": (
            "In Washington, Sam mastered political bribery under the guise of civic duty. He became the "
            "second-largest individual donor to Democrats, while his co-CEO funneled matching millions to Republicans, "
            "buying complete bipartisan political immunity."
        ),
        "visual_prompt": (
            "Cinematic tracking shot through marble corridors of the US Capitol, long dramatic shadows between neoclassical columns, "
            "warm golden chandeliers, political thriller cinematography, 35mm film still, no text"
        ),
        "eyebrow": "WASHINGTON D.C. // K STREET",
        "headline": "BIPARTISAN CAPTURE",
        "emphasis": "$70M IN CAMPAIGN CASH",
        "subtext": "Funding both political parties simultaneously to insulate the firm from regulatory action.",
        "accent": "Cyan"
    },
    {
        "seg": 19,
        "time": "06:00 - 06:20",
        "chapter": "CHAPTER 2: THE SEDUCTION OF WALL STREET",
        "script": (
            "Sam drafted the DCCPA bill, lobbying regulators to force all crypto transactions through centralized exchanges "
            "like FTX, while effectively criminalizing decentralized finance. He was constructing a government-enforced monopoly."
        ),
        "visual_prompt": (
            "Cinematic close-up of legal legislative bill draft with red editorial pen markups on mahogany desk, "
            "gavel and official Congressional seal in soft focus background, dramatic beam lighting, 35mm film still, no text"
        ),
        "eyebrow": "CONGRESSIONAL LOBBYING // DCCPA",
        "headline": "WEAPONIZING REGULATION",
        "emphasis": "OUTLAWING COMPETITORS",
        "subtext": "Drafting legislation to suffocate decentralized finance while crowning FTX the sole gatekeeper.",
        "accent": "Amber"
    },
    {
        "seg": 20,
        "time": "06:20 - 06:40",
        "chapter": "CHAPTER 2: THE SEDUCTION OF WALL STREET",
        "script": (
            "By early 2022, Sam Bankman-Fried was untouchable. He was the golden boy who could do no wrong. "
            "No one looked at the balance sheet. No one verified the reserves. Because after all, who would suspect "
            "the world's most generous philanthropist was operating a Ponzi scheme?"
        ),
        "visual_prompt": (
            "Cinematic high-contrast portrait silhouette of tech founder standing in front of floor-to-ceiling glass penthouse overlooking ocean, "
            "golden halo backlight, cold dramatic shadows, prestige documentary aesthetic, 35mm film still, no text"
        ),
        "eyebrow": "HUBRIS // NASSAU PENTHOUSE",
        "headline": "THE UNTOUCHABLE TITAN",
        "emphasis": "BLIND TRUST",
        "subtext": "No one verified custody because the illusion was too profitable to question.",
        "accent": "Emerald"
    },

    # --- CHAPTER 3: THE 72-HOUR BANK RUN (06:40 - 09:20) ---
    {
        "seg": 21,
        "time": "06:40 - 07:00",
        "chapter": "CHAPTER 3: THE 72-HOUR BANK RUN",
        "script": (
            "The first crack appeared in May 2022 when the Terra Luna ecosystem imploded, wiping out sixty billion dollars. "
            "Crypto lenders like Celsius and Voyager faced instant insolvency. What the public didn't know was that Alameda "
            "had suffered catastrophic losses."
        ),
        "visual_prompt": (
            "Cinematic metaphor: An enormous red digital domino toppling onto a field of financial circuit boards, "
            "sparks flying, emergency crimson lighting, moody dark background, 35mm film still, no text"
        ),
        "eyebrow": "MARKET CONTAGION // MAY 2022",
        "headline": "THE TERRA LUNA CRASH",
        "emphasis": "$60B LIQUIDATION SHOCK",
        "subtext": "When algorithmic stablecoins collapsed, Alameda's trading balance suffered a fatal wound.",
        "accent": "Crimson"
    },
    {
        "seg": 22,
        "time": "07:00 - 07:20",
        "chapter": "CHAPTER 3: THE 72-HOUR BANK RUN",
        "script": (
            "Instead of letting Alameda fail, Sam secretly plugged the hole using customer funds from FTX. "
            "Billions of client deposits were transferred to Alameda's accounts to pay off margin lenders. "
            "The crime was now irreversible."
        ),
        "visual_prompt": (
            "Cinematic visual: Two digital glass containers connected by a dark underground siphon tube, "
            "green liquid customer funds draining rapidly into a glowing crimson tank, 35mm thriller lighting, no text"
        ),
        "eyebrow": "SECRET BAILOUT // COMMINGLED DEPOSITS",
        "headline": "PLUGGING THE BLACK HOLE",
        "emphasis": "$8B CUSTOMER SIPHON",
        "subtext": "Stealing client deposits to pay off Alameda's third-party institutional loans.",
        "accent": "Crimson"
    },
    {
        "seg": 23,
        "time": "07:20 - 07:40",
        "chapter": "CHAPTER 3: THE 72-HOUR BANK RUN",
        "script": (
            "On November 2nd, 2022, CoinDesk published a leaked balance sheet from Alameda Research. "
            "The report sent shockwaves through the industry: out of fourteen billion dollars in assets, "
            "the vast majority was illiquid FTT tokens minted by FTX."
        ),
        "visual_prompt": (
            "Cinematic shot of confidential leaked financial dossier on dark wooden desk, harsh angle desk lamp, "
            "red highlighter marker circling balance sheet line items, true crime investigative aesthetic, 35mm film still, no text"
        ),
        "eyebrow": "COINDESK SCOOP // NOV 2, 2022",
        "headline": "THE SMOKING GUN DOSSIER",
        "emphasis": "THE BALANCE SHEET LEAK",
        "subtext": "Revealing that Alameda was insolvent on paper without inflated FTX tokens.",
        "accent": "Amber"
    },
    {
        "seg": 24,
        "time": "07:40 - 08:00",
        "chapter": "CHAPTER 3: THE 72-HOUR BANK RUN",
        "script": (
            "The executioner arrived on Sunday, November 6th. Changpeng Zhao, the CEO of rival exchange Binance, "
            "tweeted that due to recent revelations, Binance had decided to liquidate its entire half-billion-dollar holding of FTT."
        ),
        "visual_prompt": (
            "Cinematic macro shot of smartphone screen glowing in dark room displaying social media liquidation statement, "
            "sharp glass reflection, moody cold blue and red lighting, 35mm film still, no text"
        ),
        "eyebrow": "BINANCE // NOV 6, 2022",
        "headline": "THE EXECUTION TWEET",
        "emphasis": "TOTAL FTT DUMP",
        "subtext": "CZ announced Binance was liquidating its entire $580M FTT reserve.",
        "accent": "Crimson"
    },
    {
        "seg": 25,
        "time": "08:00 - 08:20",
        "chapter": "CHAPTER 3: THE 72-HOUR BANK RUN",
        "script": (
            "That single tweet triggered an immediate bank run. Millions of users panicked, rushing to the FTX website "
            "and slamming the withdrawal button. Over seventy-two hours, six billion dollars in withdrawal requests poured in. "
            "FTX didn't have the money."
        ),
        "visual_prompt": (
            "Cinematic shot of panicked traders at digital workstations in darkness, flashing red screens displaying 'WITHDRAWAL DELAYED', "
            "motion blur, emergency alert strobe reflections, 35mm documentary film still, no text"
        ),
        "eyebrow": "THE 72-HOUR BANK RUN",
        "headline": "$6,000,000,000 CRASH",
        "emphasis": "LIQUIDITY FREEZE",
        "subtext": "Retail investors rushed to pull funds while exchange cold wallets emptied to zero.",
        "accent": "Crimson"
    },
    {
        "seg": 26,
        "time": "08:20 - 08:40",
        "chapter": "CHAPTER 3: THE 72-HOUR BANK RUN",
        "script": (
            "Behind closed doors, Sam panicked. In encrypted Signal group chats, he frantically pleaded with Wall Street banks, "
            "sovereign wealth funds, and venture capitalists for an emergency eight-billion-dollar rescue package. "
            "Every single firm turned him away."
        ),
        "visual_prompt": (
            "Cinematic close-up of encrypted messaging app chat screen in dark penthouse, messages showing frantic capital requests, "
            "cold sweat on hands, tension-filled political thriller cinematography, 35mm film still, no text"
        ),
        "eyebrow": "ENCRYPTED SIGNAL CHATS // RESCUE PLEAS",
        "headline": "BEGGING FOR $8 BILLION",
        "emphasis": "EVERYONE SAID NO",
        "subtext": "Wall Street and Middle Eastern sovereign funds inspected the hole and walked away.",
        "accent": "Amber"
    },
    {
        "seg": 27,
        "time": "08:40 - 09:00",
        "chapter": "CHAPTER 3: THE 72-HOUR BANK RUN",
        "script": (
            "In desperation, Sam signed a non-binding acquisition letter with Binance. But within twenty-four hours of "
            "inspecting FTX's internal books, Binance walked away, stating: 'The issues are beyond our control or ability to help.'"
        ),
        "visual_prompt": (
            "Cinematic shot of an unsigned corporate merger contract discarded on a boardroom table, fountain pen rolled aside, "
            "shadows stretching across dark leather conference room, 35mm film still, no text"
        ),
        "eyebrow": "FAILED BAILOUT // NOV 9, 2022",
        "headline": "BINANCE WALKS AWAY",
        "emphasis": "BEYOND OUR CONTROL",
        "subtext": "After 24 hours of due diligence, Binance discovered an irrecoverable multi-billion dollar hole.",
        "accent": "Crimson"
    },
    {
        "seg": 28,
        "time": "09:00 - 09:20",
        "chapter": "CHAPTER 3: THE 72-HOUR BANK RUN",
        "script": (
            "On November 11th, 2022, FTX officially halted withdrawals and filed for Chapter 11 bankruptcy. "
            "Thirty-two billion dollars in company valuation vanished. Over one million everyday depositors were locked out, "
            "watching their life savings evaporate overnight."
        ),
        "visual_prompt": (
            "Cinematic wide shot of the Delaware Federal Bankruptcy Courthouse at dusk, cold rain falling on stone steps, "
            "dark grey sky, somber documentary lighting, 35mm film still, photorealistic 8k, no text"
        ),
        "eyebrow": "DISTRICT OF DELAWARE // NOV 11, 2022",
        "headline": "CHAPTER 11 BANKRUPTCY",
        "emphasis": "$32,000,000,000 ZEROED",
        "subtext": "Over one million global creditors lost access to life savings as the platform went dark.",
        "accent": "Crimson"
    },

    # --- CHAPTER 4 & EPILOGUE: THE RECKONING & THE LESSON (09:20 - 12:00) ---
    {
        "seg": 29,
        "time": "09:20 - 09:40",
        "chapter": "CHAPTER 4: THE RECKONING",
        "script": (
            "To oversee the liquidation, the court appointed John J. Ray III, the veteran restructuring lawyer "
            "who cleaned up Enron. In his sworn congressional declaration, John Ray wrote: 'Never in my career have I seen "
            "such an utter failure of corporate controls.'"
        ),
        "visual_prompt": (
            "Cinematic portrait of a veteran bankruptcy auditor in dark suit seated before rows of legal boxes filled with documents, "
            "stern expression, dramatic high-contrast lighting, 35mm film still, no text"
        ),
        "eyebrow": "CONGRESSIONAL DECLARATION // AUDIT",
        "headline": "THE JOHN RAY VERDICT",
        "emphasis": "WORSE THAN ENRON",
        "subtext": "'Never in my 40-year career have I seen such a complete absence of financial controls.'",
        "accent": "Amber"
    },
    {
        "seg": 30,
        "time": "09:40 - 10:00",
        "chapter": "CHAPTER 4: THE RECKONING",
        "script": (
            "There were no audited books, no list of bank accounts, and no board oversight. "
            "Multi-million-dollar wire transfers were approved with emojis on Slack. Corporate expenses were tracked "
            "on casual QuickBooks software, while customer money bought luxury real estate."
        ),
        "visual_prompt": (
            "Cinematic forensic concept: A disorganized pile of corporate ledgers and invoices stamped 'UNVERIFIED', "
            "glowing digital chat interface showing emoji approvals, forensic documentary lighting, 35mm film still, no text"
        ),
        "eyebrow": "INTERNAL CONTROLS FORENSICS",
        "headline": "ACCOUNTING BY EMOJI",
        "emphasis": "ZERO AUDITED BOOKS",
        "subtext": "Multi-million dollar corporate disbursements approved with casual chat emojis.",
        "accent": "Crimson"
    },
    {
        "seg": 31,
        "time": "10:00 - 10:20",
        "chapter": "CHAPTER 4: THE RECKONING",
        "script": (
            "On December 12th, 2022, Royal Bahamas Police officers surrounded Sam Bankman-Fried's luxury penthouse. "
            "He was arrested, handcuffed, and transported to the notorious Fox Hill prison before being extradited "
            "to the United States in federal custody."
        ),
        "visual_prompt": (
            "Cinematic shot of police cruiser emergency lights reflecting on wet Nassau pavement at night, "
            "officers escorting suspect in handcuffs to unmarked vehicle, true crime documentary cinematography, 35mm film still, no text"
        ),
        "eyebrow": "NASSAU, THE BAHAMAS // DEC 12, 2022",
        "headline": "THE MIDNIGHT ARREST",
        "emphasis": "FEDERAL INDICTMENT",
        "subtext": "Extradited in handcuffs to face criminal wire fraud and money laundering charges.",
        "accent": "Crimson"
    },
    {
        "seg": 32,
        "time": "10:20 - 10:40",
        "chapter": "CHAPTER 4: THE RECKONING",
        "script": (
            "In Manhattan federal court, federal prosecutors unsealed a sweeping indictment charging Sam with wire fraud, "
            "securities fraud, and conspiracy. He pleaded not guilty, claiming he was simply an incompetent manager "
            "who got in over his head."
        ),
        "visual_prompt": (
            "Cinematic shot of the Southern District of New York federal courthouse exterior in Manhattan, "
            "imposing granite columns, reporters and broadcast cameras gathered on courthouse steps, 35mm film still, no text"
        ),
        "eyebrow": "SOUTHERN DISTRICT OF NEW YORK",
        "headline": "THE FEDERAL INDICTMENT",
        "emphasis": "7 FELONY COUNTS",
        "subtext": "Charging the former wunderkind with orchestrating one of the largest financial frauds in history.",
        "accent": "Cyan"
    },
    {
        "seg": 33,
        "time": "10:40 - 11:00",
        "chapter": "CHAPTER 4: THE RECKONING",
        "script": (
            "His closest confidants turned against him. Alameda CEO Caroline Ellison and FTX co-founder Gary Wang "
            "took the stand, testifying under oath that Sam had directly ordered them to alter code, falsify balance sheets, "
            "and secretly siphon customer deposits."
        ),
        "visual_prompt": (
            "Cinematic shot of federal courtroom witness stand in dark polished wood, microphone and sworn Bible, "
            "dramatic sunbeam cutting through tall court windows, high-stakes judicial thriller cinematography, 35mm film still, no text"
        ),
        "eyebrow": "MANHATTAN FEDERAL COURT // TRIAL",
        "headline": "THE INNER CIRCLE FLIPS",
        "emphasis": "DIRECT EVIDENCE",
        "subtext": "Key executives testified under oath that Sam ordered the theft of customer funds.",
        "accent": "Amber"
    },
    {
        "seg": 34,
        "time": "11:00 - 11:20",
        "chapter": "CHAPTER 4: THE RECKONING",
        "script": (
            "In November 2023, after four hours of jury deliberation, Sam Bankman-Fried was found guilty on all seven criminal counts. "
            "Judge Lewis Kaplan sentenced him to twenty-five years in federal prison and ordered the forfeiture of eleven billion dollars."
        ),
        "visual_prompt": (
            "Cinematic macro shot of a dark polished walnut judge's gavel resting on federal court bench, "
            "dramatic chiaroscuro lighting, deep shadows, 35mm film still, photorealistic 8k, no text"
        ),
        "eyebrow": "JUDICIAL SENTENCING // MANHATTAN",
        "headline": "GUILTY ON ALL COUNTS",
        "emphasis": "25 YEARS IN PRISON",
        "subtext": "Federal court orders 25-year sentence and $11,000,000,000 in forfeiture.",
        "accent": "Crimson"
    },
    {
        "seg": 35,
        "time": "11:20 - 11:40",
        "chapter": "EPILOGUE: THE INVESTOR CODEX",
        "script": (
            "The collapse of FTX isn't just about crypto; it is a timeless lesson in market psychology. "
            "Whenever an institution promises guaranteed yield, zero risk, and revolutionary safety while refusing "
            "transparent proof of reserves, you are the exit liquidity."
        ),
        "visual_prompt": (
            "Cinematic metaphor: Heavy titanium hardware security key and proof-of-reserves cryptographic ledger "
            "sitting in an illuminated secure glass case, warm green integrity lighting, 35mm film still, no text"
        ),
        "eyebrow": "THE INVESTOR CODEX // RISK DISCIPLINE",
        "headline": "NOT YOUR KEYS, NOT YOUR COINS",
        "emphasis": "THE GOLDEN RULE",
        "subtext": "Yield without custody is fiction. Always demand verifiable cryptographic proof of reserves.",
        "accent": "Emerald"
    },
    {
        "seg": 36,
        "time": "11:40 - 12:00",
        "chapter": "EPILOGUE: THE INVESTOR CODEX",
        "script": (
            "At The Bull Print, we don't worship personas, billionaire founder mythologies, or sponsored marketing hype. "
            "We audit the order flow, we track institutional footprints, and we decode the fine print—before the illusion collapses."
        ),
        "visual_prompt": (
            "Cinematic wide shot of The Bull Print executive financial intelligence center at night, panoramic floor-to-ceiling glass "
            "overlooking glowing global financial district, clean dark teak desk with glowing forensic audit report, 35mm film still, no text"
        ),
        "eyebrow": "THE BULL PRINT // FINANCIAL INTELLIGENCE",
        "headline": "AUDIT THE ORDER FLOW",
        "emphasis": "NEVER TRUST PERSONAS",
        "subtext": "Institutional research and forensic market breakdowns. The Bull Print.",
        "accent": "Emerald"
    }
]

if __name__ == "__main__":
    print(f"Total Segments: {len(SEGMENTS)}")
    total_words = sum(len(s["script"].split()) for s in SEGMENTS)
    print(f"Total Spoken Words: {total_words} (~{round(total_words/len(SEGMENTS), 1)} words per 20s beat)")
