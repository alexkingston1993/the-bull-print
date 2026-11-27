# TARGET SUBREDDITS: r/CryptoCurrency, r/solana, r/IndianStreetBets
# TITLE: [Technical Forensics] The 85 SOL Graduation Threshold: How Solana Launchpad Bonding Curves Migrate to Raydium (Contract Math, Burn Proofs & Indian Tax Implications)

### What Exactly Happens at the 85 SOL Threshold?

On Solana token launchpads (Pump.fun, etc.), thousands of tokens launch daily with constant-product bonding curves ($x \cdot y = k$).

Retail traders often ask: *"At what exact market cap does a token graduate to Raydium? What happens to liquidity?"*

Here is the exact on-chain forensic breakdown of the mathematical thresholds, LP burn proofs, and Indian Section 115BBH tax liabilities on DEX swaps.

---

### 1. The Bonding Curve Math

Every token launches with a fixed supply of **1,000,000,000 (1 Billion) tokens**:
- **Curve Allocation**: 800,000,000 tokens (80%)
- **Raydium Migration Reserve**: 200,000,000 tokens (20%)
- **Virtual SOL Reserve**: 30 virtual SOL

As users buy, the price scales along the curve. When total real net SOL accumulated reaches **85 SOL**, the curve completes 100%.

---

### 2. Market Cap at Graduation

The market capitalization at graduation depends on SOL spot price:
- **At $150 SOL**: Fully Diluted Valuation (FDV) = **~$69,000**
- **At $180 SOL**: Fully Diluted Valuation (FDV) = **~$79,000**
- **At $210 SOL**: Fully Diluted Valuation (FDV) = **~$88,000**

---

### 3. The Atomic Migration Event

When 85 SOL is reached, the contract atomically executes:
1. Deducts 6 SOL protocol migration fee.
2. Deposits the remaining ~79 SOL paired with the 200,000,000 reserved tokens into a new **Raydium CPMM pool**.
3. **Mints LP tokens and sends them to the Solana dead address (`11111111111111111111111111111111`)**, permanently locking liquidity.
4. Mint authority and freeze authority are verified revoked (`None`).

---

### 4. Indian Tax Implications under Section 115BBH

If you trade Solana launchpad tokens from India:
- Swapping memecoins back to SOL or USDC is a taxable transfer under Section 2(47A).
- Gains are taxed at a flat **31.2%** under Section 115BBH.
- **Zero loss set-off**: If you make 20 SOL on one token and lose 15 SOL on another, you owe tax on the entire 20 SOL gain.
- **Gas fees and slippage cannot be deducted.**

*Technical forensics prepared by The Bull Print Web3 Desk: bullprintmedia.com/posts/raydium-token-launchpad-graduation-threshold-market-cap*