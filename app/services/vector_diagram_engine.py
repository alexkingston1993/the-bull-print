#!/usr/bin/env python3
"""
app/services/vector_diagram_engine.py
The Bull Print — PaperBanana-Style Vector & SVG Financial Diagram Engine.

Generates publication-quality financial flowcharts, money trails, and regulatory diagrams
instead of generic boxes or basic Matplotlib plots:
- Clean SVG vectors with crisp gradients, drop shadows, and modern typography
- Step-by-step monetary cascades (e.g. ₹10 Lakh Claim -> 50% Room Over-Limit -> ₹4.88 Lakh Loss)
- Converts directly to high-DPI raster layers for video compositing
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.asset_ledger import AssetConsistencyLedger


class VectorDiagramEngine:
    """
    PaperBanana-style SVG generator for institutional financial diagrams.
    """
    def __init__(self):
        self.ledger = AssetConsistencyLedger()

    def generate_proportionate_deduction_cascade_svg(
        self,
        total_bill: int = 1000000,
        room_sublimit: int = 5000,
        room_actual: int = 10000,
        insurer_payout: int = 512000,
        out_of_pocket: int = 488000
    ) -> str:
        """
        Creates a high-end vector flowchart illustrating the mathematical cascade
        of an insurance proportionate room rent deduction penalty.
        """
        c = self.ledger.COLORS
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600">
  <defs>
    <filter id="cardShadow" x="-10%" y="-10%" width="125%" height="125%">
      <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#050811" flood-opacity="0.35"/>
    </filter>
    <linearGradient id="emeraldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c.EMERALD_ACCENT}"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
    <linearGradient id="crimsonGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c.CRIMSON_ACCENT}"/>
      <stop offset="100%" stop-color="#B91C1C"/>
    </linearGradient>
  </defs>

  <!-- Background Base -->
  <rect width="100%" height="100%" fill="none"/>

  <!-- Step 1 Node: Total Claim -->
  <g transform="translate(60, 60)" filter="url(#cardShadow)">
    <rect width="280" height="150" rx="16" fill="{c.BG_IVORY}" stroke="{c.TEXT_LIGHT}" stroke-width="2"/>
    <text x="24" y="40" font-family="{self.ledger.TYPOGRAPHY.FONT_BODY}" font-weight="700" font-size="14" fill="{c.TEXT_MUTED}">STEP 01 · TOTAL INVOICE</text>
    <text x="24" y="80" font-family="{self.ledger.TYPOGRAPHY.FONT_BODY}" font-weight="900" font-size="28" fill="{c.TEXT_NAVY}">Rs. {total_bill:,}</text>
    <text x="24" y="115" font-family="{self.ledger.TYPOGRAPHY.FONT_BODY}" font-size="14" fill="{c.TEXT_MUTED}">Hospital billed amount</text>
  </g>

  <!-- Arrow 1 -> 2 -->
  <path d="M 340 135 L 430 135" stroke="{c.TEXT_MUTED}" stroke-width="3" stroke-dasharray="6,6" marker-end="url(#arrow)"/>

  <!-- Step 2 Node: The Clause Trigger -->
  <g transform="translate(450, 60)" filter="url(#cardShadow)">
    <rect width="320" height="150" rx="16" fill="{c.SURFACE_PANEL}" stroke="{c.GOLD_ACCENT}" stroke-width="2"/>
    <text x="24" y="40" font-family="{self.ledger.TYPOGRAPHY.FONT_BODY}" font-weight="700" font-size="14" fill="{c.GOLD_ACCENT}">CLAUSE 4.2 TRIGGER</text>
    <text x="24" y="80" font-family="{self.ledger.TYPOGRAPHY.FONT_BODY}" font-weight="900" font-size="26" fill="#FFFFFF">Room: Rs. {room_actual:,}/day</text>
    <text x="24" y="115" font-family="{self.ledger.TYPOGRAPHY.FONT_BODY}" font-size="13" fill="{c.TEXT_LIGHT}">Entitlement: Rs. {room_sublimit:,}/day (50% Over-Limit)</text>
  </g>

  <!-- Arrow 2 -> 3 -->
  <path d="M 770 135 L 860 135" stroke="{c.CRIMSON_ACCENT}" stroke-width="3"/>

  <!-- Step 3 Node: The 50% Bill Slash -->
  <g transform="translate(880, 60)" filter="url(#cardShadow)">
    <rect width="260" height="150" rx="16" fill="url(#crimsonGrad)" stroke="{c.CRIMSON_GLOW}" stroke-width="2"/>
    <text x="20" y="40" font-family="{self.ledger.TYPOGRAPHY.FONT_BODY}" font-weight="700" font-size="13" fill="#FEE2E2">AUTOMATED PENALTY</text>
    <text x="20" y="82" font-family="{self.ledger.TYPOGRAPHY.FONT_BODY}" font-weight="900" font-size="30" fill="#FFFFFF">50% CUT</text>
    <text x="20" y="118" font-family="{self.ledger.TYPOGRAPHY.FONT_BODY}" font-size="13" fill="#FEE2E2">All Surgeon &amp; ICU fees cut</text>
  </g>

  <!-- Bottom Split Outcome -->
  <!-- Insurer Pays -->
  <g transform="translate(180, 320)" filter="url(#cardShadow)">
    <rect width="380" height="160" rx="18" fill="{c.SURFACE_DARK}" stroke="{c.EMERALD_ACCENT}" stroke-width="2"/>
    <text x="28" y="45" font-family="{self.ledger.TYPOGRAPHY.FONT_BODY}" font-weight="700" font-size="14" fill="{c.EMERALD_ACCENT}">INSURER PAYOUT (51.2%)</text>
    <text x="28" y="95" font-family="{self.ledger.TYPOGRAPHY.FONT_BODY}" font-weight="900" font-size="34" fill="#FFFFFF">Rs. {insurer_payout:,}</text>
    <text x="28" y="132" font-family="{self.ledger.TYPOGRAPHY.FONT_BODY}" font-size="14" fill="{c.TEXT_LIGHT}">Settled after sub-limit proportionate cuts</text>
  </g>

  <!-- Policyholder Loss -->
  <g transform="translate(640, 320)" filter="url(#cardShadow)">
    <rect width="380" height="160" rx="18" fill="{c.SURFACE_DARK}" stroke="{c.CRIMSON_ACCENT}" stroke-width="2"/>
    <text x="28" y="45" font-family="{self.ledger.TYPOGRAPHY.FONT_BODY}" font-weight="700" font-size="14" fill="{c.CRIMSON_ACCENT}">OUT-OF-POCKET DAMAGE (48.8%)</text>
    <text x="28" y="95" font-family="{self.ledger.TYPOGRAPHY.FONT_BODY}" font-weight="900" font-size="34" fill="{c.CRIMSON_GLOW}">Rs. {out_of_pocket:,}</text>
    <text x="28" y="132" font-family="{self.ledger.TYPOGRAPHY.FONT_BODY}" font-size="14" fill="{c.TEXT_LIGHT}">Paid by family for Rs. 5,000 room upgrade</text>
  </g>
</svg>"""
        return svg

    def export_diagram_svg(self, dest_path: Path):
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        svg_content = self.generate_proportionate_deduction_cascade_svg()
        dest_path.write_text(svg_content, encoding="utf-8")
        return dest_path


if __name__ == "__main__":
    engine = VectorDiagramEngine()
    out = Path("output/diagrams/proportionate_deduction_cascade.svg")
    engine.export_diagram_svg(out)
    print(f"Generated Vector Diagram: {out}")
