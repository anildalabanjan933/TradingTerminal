"""
Streamlit_TradingSystems/System_1_Nifty_OI/layout_tokens.py

Purpose:
- Central source of truth for all layout and style constants for System_1 (Nifty OI).
- Defines the 6×6 grid system, default row/col spans, and styling tokens.
- Keeps UI consistent across the system and supports the Layout Editor.
"""

from dataclasses import dataclass
from typing import Dict

# Grid dimensions (permanent rule)
GRID_ROWS = 6
GRID_COLS = 6


@dataclass
class SectionLayout:
    """Represents position and size of one dashboard section in the 6×6 grid."""
    row: int
    col: int
    row_span: int
    col_span: int


# Default positions for common sections in System_1 (Nifty OI)
DEFAULT_LAYOUT: Dict[str, SectionLayout] = {
    "kpi_strip": SectionLayout(row=1, col=1, row_span=1, col_span=6),
    "oi_chart": SectionLayout(row=2, col=1, row_span=2, col_span=3),
    "candlestick_chart": SectionLayout(row=2, col=4, row_span=2, col_span=3),
    "trade_panel": SectionLayout(row=4, col=1, row_span=2, col_span=3),
    "strategy_panel": SectionLayout(row=4, col=4, row_span=2, col_span=3),
}


# Global style tokens
TOKENS = {
    "card_radius": "2xl",
    "shadow": "md",
    "padding": "p-3",
    "gap": "gap-4",
    "font_family": "sans-serif",
    "headline_size": "xl",
    "text_size": "base",
}


def get_default_layout() -> Dict[str, SectionLayout]:
    """Return the default layout mapping."""
    return DEFAULT_LAYOUT


def get_tokens() -> Dict[str, str]:
    """Return the global style tokens."""
    return TOKENS


# --- Smoke test ---
def smoke_test_import() -> str:
    return "layout_tokens OK"


if __name__ == "__main__":
    print("Layout tokens helper")
    print("Grid size:", GRID_ROWS, "×", GRID_COLS)
    print("Default layout keys:", list(DEFAULT_LAYOUT.keys()))
    print("Tokens:", TOKENS)
