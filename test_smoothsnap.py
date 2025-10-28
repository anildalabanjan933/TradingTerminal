# ==============================================================
# 📄 FILE: D:\Streamlit_TradingSystems\test_smoothsnap.py
# ==============================================================
# PURPOSE:
#   Full smoke test for v7.1.3 — SmoothSnap Grid + Panel Controls + Sidebar + Tabs
# ==============================================================

import streamlit as st
from shared.dashboard_grid_engine import render_dashboard
from shared.drag_engine import render_drag_engine
from shared.panel_manager import render_all_panel_controls
from System_2_TradingTerminal.panels.left_sidebar import render_left_sidebar, render_mode_tabs

# --------------------------------------------------------------
# 🔧 PAGE CONFIG
# --------------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="SmoothSnap Grid + Sidebar + Tabs Test",
)

# --------------------------------------------------------------
# 🧩 TEST DASHBOARD PANELS
# --------------------------------------------------------------
st.markdown("### 🧩 v7.1.3 — SmoothSnap Grid + Panel Controls + Sidebar + Tabs")

panels = {
    "chart1": "<div style='height:100%;display:flex;align-items:center;justify-content:center;font-weight:600;'>Chart 1</div>",
    "chart2": "<div style='height:100%;display:flex;align-items:center;justify-content:center;font-weight:600;'>Chart 2</div>",
    "chart3": "<div style='height:100%;display:flex;align-items:center;justify-content:center;font-weight:600;'>Chart 3</div>",
    "chart4": "<div style='height:100%;display:flex;align-items:center;justify-content:center;font-weight:600;'>Chart 4</div>",
    "watch1": "<div style='height:100%;display:flex;align-items:center;justify-content:center;font-weight:600;'>Watchlist 1</div>",
    "watch2": "<div style='height:100%;display:flex;align-items:center;justify-content:center;font-weight:600;'>Watchlist 2</div>",
}

# --------------------------------------------------------------
# 🚀 RENDER ENGINE + GRID
# --------------------------------------------------------------
render_drag_engine()      # Inject JS persistence bridge
render_dashboard(panels)  # Render SmoothSnap grid + controls

# --------------------------------------------------------------
# 🎛 PANEL CONTROL UI
# --------------------------------------------------------------
render_all_panel_controls(list(panels.keys()))

# --------------------------------------------------------------
# ⬅️ LEFT SIDEBAR + 🧭 MODE TABS
# --------------------------------------------------------------
render_left_sidebar()
render_mode_tabs()

# --------------------------------------------------------------
# 🧠 DEBUG OUTPUT
# --------------------------------------------------------------
st.write("✅ Drag / resize / hide / reset panels + toggle sidebar & mode tabs to verify behavior.")
st.json(st.session_state)
