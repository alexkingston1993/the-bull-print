# TARGET SUBREDDITS: r/IndianStreetBets, r/IndiaInvestments
# TITLE: [Forensic DD] The Section 115BBH Trap: Why ₹1L Profit on BTC + ₹60k Loss on ETH Leaves You With ₹31,200 Tax and No Set-Off (Full Math & Schedule VDA Breakdown)

### Background & Why Most Retail Crypto Traders Get It Wrong

With tax filing deadlines and AIS reporting becoming fully automated with Indian exchanges (CoinDCX, WazirX, CoinSwitch), there is a massive misconception among Indian retail traders regarding how crypto gains are taxed under the Income Tax Act, 1961.

Many traders assume: *"I bought BTC, made ₹1,00,000. I bought ETH, lost ₹60,000. My net gain is ₹40,000, so I pay tax on ₹40,000."*

**Under Section 115BBH, that calculation is illegal and will trigger an automated scrutiny notice from the IT department.**

Here is the exact forensic math, statutory sub-clauses, and how to file Schedule VDA without getting penalized.

---

### 1. The Statutory Iron Curtain: Section 115BBH(2)

Under Section 115BBH(1), any income arising from the transfer of a Virtual Digital Asset (VDA) is taxed at a flat rate of **30%** plus a **4% Health & Education cess**, bringing the baseline effective rate to **31.20%**.

The trap lies in **Section 115BBH(2)**:
1. **Zero Deduction Except Cost of Acquisition**: You cannot claim brokerage, exchange withdrawal fees, gas fees, depreciation, internet bills, or electricity. Only the purchase price is deductible.
2. **Zero Loss Set-Off**: Loss from the transfer of one VDA cannot be set off against income from another VDA.
3. **Zero Loss Carry Forward**: VDA losses cannot be carried forward to subsequent financial years.
4. **No Basic Exemption Shield**: Even if your total annual income is below ₹3,00,000 (New Regime), your crypto gains are taxed at 30% from rupee one.

---

### 2. The Forensic Ledger: 3 Scenarios Calculated

| Parameter | Scenario A: Pure ₹1L Gain | Scenario B: ₹1L Gain + ₹60k Loss | Scenario C: Equity Equivalent (LTCG) |
| :--- | :--- | :--- | :--- |
| **Gross Profit (BTC)** | +₹1,00,000 | +₹1,00,000 | +₹1,00,000 |
| **Gross Loss (ETH)** | ₹0 | -₹60,000 | -₹60,000 |
| **Taxable Income** | **₹1,00,000** | **₹1,00,000** *(Loss Disallowed)* | **₹40,000** *(Loss Offset Allowed)* |
| **Base Tax** | ₹30,000 (30%) | ₹30,000 (30%) | ₹0 *(Under ₹1.25L Exemption)* |
| **4% Cess** | ₹1,200 | ₹1,200 | ₹0 |
| **Total Tax Payable** | **₹31,200** | **₹31,200** | **₹0** |
| **Net In Hand Post-Tax**| **₹68,800** | **₹8,800** *(Real Net Profit)* | **₹40,000** |
| **Effective Tax on In-Hand Profit** | 31.2% | **78.0%** | **0.0%** |

Notice Scenario B: Your actual wallet profit was ₹40,000 (₹1L gain minus ₹60k loss). But because the ₹60,000 ETH loss is quarantined and disallowed under 115BBH(2)(b), you must hand over ₹31,200 to the government. **You keep just ₹8,800—an effective tax rate of 78% on your net gains!**

---

### 3. The 1% TDS Trap under Section 194S

Every Indian exchange deducts 1% TDS on the **gross sell transaction value**, not the profit.
- If you buy ₹10,00,000 of crypto and sell for ₹11,00,000, TDS is 1% of ₹11,00,000 = **₹11,000**.
- You can claim credit for this ₹11,000 against your ₹31,200 tax liability when filing ITR-2, but only if the TDS reflects in your **Form 26AS / Annual Information Statement (AIS)**.
- If you trade on foreign/offshore exchanges (Binance, Bybit, KuCoin), they do not deduct 194S TDS. However, Indian banks and FIU-India track P2P UPI transfers and LRS remittances. Not reporting these trades in Schedule VDA is treated as tax evasion under Section 270A (50% to 200% penalty).

---

### 4. How to Correctly Report in ITR-2 (Schedule VDA)

If you have crypto income, you **cannot file ITR-1 (Sahaj)**. You must file **ITR-2** (or ITR-3 if trading is treated as business income):
1. **Date of Acquisition & Transfer**: Every single trade lot must have its buy timestamp and sell timestamp.
2. **Head of Income**: Select "Capital Gains" -> "Schedule VDA".
3. **Cost of Acquisition**: Enter exact purchase price in INR.
4. **Consideration Received**: Enter exact sell price in INR.
5. **Reconciliation**: Compare gross sale values against AIS code `E-28` (Receipt from transfer of virtual digital assets). Any mismatch triggers an automated defective return notice under Section 139(9).

---

### Discussion & Practitioner Takeaway

If you are an active crypto trader in India, holding losing positions until a different tax year or churn-trading altcoins will bleed your capital through disallowed offsets and 1% TDS drag.

Have you reconciled your AIS for FY 2025-26? How are you handling offshore DEX and hardware wallet transactions?

*Forensic research prepared by The Bull Print Macro & Tax Desk. Full detailed balance sheet and statutory models available on bullprintmedia.com/posts/how-much-tax-on-1-lakh-crypto-profit-in-india-section-115bbh*