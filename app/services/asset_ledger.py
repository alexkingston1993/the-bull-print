#!/usr/bin/env python3
"""
app/services/asset_ledger.py
The Bull Print — ArcReel-Style Asset Consistency Ledger.

Maintains 100% strict cross-shot visual consistency across 12-minute masterclasses:
- Brand color palettes (high-key soft ivory, royal navy, vibrant emerald, warning gold, crimson)
- Typography scales and font family declarations
- Card geometry (border radiuses, glassmorphism backdrops, border weights)
- Reusable visual components (IRDAI audit pills, forensic clause highlighters, damage ledgers)
"""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class ColorPalette:
    BG_IVORY: str = "#F8FAFC"
    TEXT_NAVY: str = "#0F172A"
    TEXT_MUTED: str = "#64748B"
    TEXT_LIGHT: str = "#E2E8F0"
    EMERALD_ACCENT: str = "#10B981"
    EMERALD_GLOW: str = "#34D399"
    GOLD_ACCENT: str = "#F59E0B"
    GOLD_GLOW: str = "#FBBF24"
    CRIMSON_ACCENT: str = "#EF4444"
    CRIMSON_GLOW: str = "#F87171"
    SURFACE_DARK: str = "#0B1120"
    SURFACE_PANEL: str = "#1E293B"


@dataclass(frozen=True)
class TypographyTokens:
    FONT_HEADLINE: str = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    FONT_MONO: str = "'JetBrains Mono', 'Courier New', monospace"
    FONT_BODY: str = "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
    
    # Weight standards
    WEIGHT_HEAVY: int = 900
    WEIGHT_BOLD: int = 700
    WEIGHT_MEDIUM: int = 500
    WEIGHT_REGULAR: int = 400


@dataclass(frozen=True)
class GeometryTokens:
    CARD_RADIUS_LG: int = 24
    CARD_RADIUS_MD: int = 16
    CARD_RADIUS_SM: int = 10
    PILL_RADIUS: int = 9999
    BORDER_WIDTH_SUBTLE: str = "1px solid rgba(255, 255, 255, 0.12)"
    BORDER_WIDTH_ACCENT: str = "2px solid #10B981"
    GLASS_BACKDROP: str = "rgba(15, 23, 42, 0.72)"
    GLASS_BLUR: str = "blur(16px)"


class AssetConsistencyLedger:
    """
    Central design system registry.
    Ensures identical styles across HTML/CSS templates, SVG generators, and Python renderers.
    """
    COLORS = ColorPalette()
    TYPOGRAPHY = TypographyTokens()
    GEOMETRY = GeometryTokens()

    @classmethod
    def get_tailwind_config_snippet(cls) -> str:
        """Returns standard Tailwind color definitions for HTML templates."""
        return f"""
        theme: {{
            extend: {{
                colors: {{
                    ivory: '{cls.COLORS.BG_IVORY}',
                    navy: '{cls.COLORS.TEXT_NAVY}',
                    emeraldAccent: '{cls.COLORS.EMERALD_ACCENT}',
                    goldAccent: '{cls.COLORS.GOLD_ACCENT}',
                    crimsonAccent: '{cls.COLORS.CRIMSON_ACCENT}',
                    surfaceDark: '{cls.COLORS.SURFACE_DARK}',
                    surfacePanel: '{cls.COLORS.SURFACE_PANEL}'
                }}
            }}
        }}
        """

    @classmethod
    def get_css_root_variables(cls) -> str:
        """Returns CSS custom properties for browser render engines."""
        return f"""
        :root {{
            --bg-ivory: {cls.COLORS.BG_IVORY};
            --text-navy: {cls.COLORS.TEXT_NAVY};
            --text-muted: {cls.COLORS.TEXT_MUTED};
            --emerald-accent: {cls.COLORS.EMERALD_ACCENT};
            --emerald-glow: {cls.COLORS.EMERALD_GLOW};
            --gold-accent: {cls.COLORS.GOLD_ACCENT};
            --crimson-accent: {cls.COLORS.CRIMSON_ACCENT};
            --surface-dark: {cls.COLORS.SURFACE_DARK};
            --surface-panel: {cls.COLORS.SURFACE_PANEL};
            --glass-backdrop: {cls.GEOMETRY.GLASS_BACKDROP};
            --glass-blur: {cls.GEOMETRY.GLASS_BLUR};
        }}
        """


if __name__ == "__main__":
    ledger = AssetConsistencyLedger()
    print("AssetConsistencyLedger loaded successfully.")
    print("Emerald Accent:", ledger.COLORS.EMERALD_ACCENT)
