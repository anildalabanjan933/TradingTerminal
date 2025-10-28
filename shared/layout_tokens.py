# ==============================================================
# 📄 FILE: shared/layout_tokens.py
# 🔧 PURPOSE: Central layout constants (heights, widths, gaps, theme)
# ==============================================================

# 6×6 grid coordinate sizing (viewport responsive)
GRID_ROWS = 6
GRID_COLS = 6

# --------------------------------------------------------------
# 🎨 Visual Tokens (Skeleton Alignment Final Fix)
# --------------------------------------------------------------
TOKENS = {
    "gap": 0,                     # 0-gap edge-to-edge layout
    "border_radius": 0,           # sharp corners for all panels
    "border_width": 1,
    "border_color": "#D0D0D0",    # light neutral border for visibility on white bg
    "background_color": "#FFFFFF",# default white background
    "text_color": "#000000",      # normal black text, not bold
    "font_weight": "normal",
    "font_family": "Inter, sans-serif",
    "panel_title_height": 18,     # compact title bars
    "topbar_height": 38,
    "tabrow_height": 38,
    "toolbar_height": 38,
    "tradepanel_height": 140,
    "riskpanel_height": 140,
    "sidebar_width": 240,
    "watchlist_min_height": 180,
    "scanner_min_height": 180,
}

# --------------------------------------------------------------
# 🧭 Auto Fit Behavior
# --------------------------------------------------------------
ZOOM_MIN = 0.67   # 67 %
ZOOM_MAX = 1.25   # 125 %
ZOOM_BASE = 1.0

# --------------------------------------------------------------
# 📏 Default Layout Map (6×6 grid coordinates)
# --------------------------------------------------------------
LAYOUT_MAP = {
    "top_bar":      {"row": 1, "col": 1, "row_span": 1, "col_span": 6},
    "tab_row":      {"row": 2, "col": 1, "row_span": 1, "col_span": 6},
    "chart_toolbar":{"row": 3, "col": 1, "row_span": 1, "col_span": 6},
    "chart_area":   {"row": 4, "col": 1, "row_span": 2, "col_span": 4},
    "watchlist":    {"row": 4, "col": 5, "row_span": 1, "col_span": 2},
    "scanner":      {"row": 5, "col": 5, "row_span": 1, "col_span": 2},
    "trade_panel":  {"row": 6, "col": 1, "row_span": 1, "col_span": 3},
    "risk_manager": {"row": 6, "col": 4, "row_span": 1, "col_span": 3},
}

# --------------------------------------------------------------
# 🧩 Helpers
# --------------------------------------------------------------
def get_token(key: str):
    return TOKENS.get(key)

def layout_for(section: str):
    return LAYOUT_MAP.get(section, {})
