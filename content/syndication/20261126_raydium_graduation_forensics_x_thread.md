# X / TWITTER THREAD: Raydium Token Launchpad Graduation Threshold Market Cap: Complete Solana Bonding Curve Forensics

1/8 🧵 How Solana Launchpad Bonding Curves Graduate to @RaydiumProtocol:

Ever wondered why the graduation threshold on Solana token curves sits at exactly 85 SOL? What exact market cap does that equal, and what happens to the liquidity?

Here is the on-chain technical breakdown 👇

---

2/8 🔢 The Initial Curve State:

Every token launches with 1,000,000,000 (1 Billion) tokens:
• 800M (80%) placed on the bonding curve
• 200M (20%) reserved in escrow for the Raydium pool
• 30 virtual SOL added to prevent infinite first-buy slippage

---

3/8 🎯 The 85 SOL Target:

As buyers buy along $x \cdot y = k$, real SOL accumulates.

The threshold is reached when exactly 85 real SOL is deposited.

Depending on SOL price ($150-$210), this sets the graduation market cap between $69,000 and $88,000.

---

4/8 🚀 The Atomic Migration Block:

When 85 SOL hits, the contract atomically:
1. Freezes the bonding curve
2. Takes ~6 SOL migration fee
3. Deposits ~79 SOL + 200M tokens into a Raydium CPMM pool

---

5/8 🔥 Unruggable Liquidity:

The Raydium LP tokens minted in this transaction are sent straight to Solana's burn address (`11111111111111111111111111111111`).

The liquidity is permanently locked and cannot be pulled by developers.

---

6/8 🛡️ Crucial Security Audit Checklist:

Before trading any token near graduation, verify:
✅ Mint Authority = None (no new tokens can be created)
✅ Freeze Authority = None (wallets cannot be blacklisted)
✅ Top 10 holders hold <15% total supply

---

7/8 ⚖️ For Indian Web3 Traders:

Remember: Every profitable swap on Raydium/DEX is taxed at 30% + 4% cess under Section 115BBH. Losses on other rugs cannot offset your wins. Trade accordingly.

---

8/8 📡 Monitor live new token drops, audit tags, and graduation alerts on @TheBullPrint New Crypto Radar: https://bullprintmedia.com/crypto-radar

---

