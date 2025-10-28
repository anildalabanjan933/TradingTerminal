# ==============================================================================
# 💹 TRADING TERMINAL DASHBOARD — Phase 23.7
# Toolbar Alignment + Scroll Lock Polish (1:1 with React)
# ==============================================================================

import streamlit as st
import json, os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from System_2_TradingTerminal.panels.left_sidebar import load as left_sidebar
from System_2_TradingTerminal.panels.trade_panel import load as trade_panel
from System_2_TradingTerminal.panels.top_bar_panel import render as top_bar
from System_2_TradingTerminal.panels.chart_toolbar import render as chart_toolbar
from shared.style_manager import apply_global_style
from shared.layout_tokens import GRID_DEFAULTS

LAYOUT_FILE = os.path.join(os.path.dirname(__file__), "data", "layout_state.json")

# ------------------------------------------------------------------------------

def load_saved_layout():
    if os.path.exists(LAYOUT_FILE):
        with open(LAYOUT_FILE, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
            except Exception as e:
                print("⚠️ Layout load failed:", e)
    return GRID_DEFAULTS


def save_layout_state(layout):
    os.makedirs(os.path.dirname(LAYOUT_FILE), exist_ok=True)
    with open(LAYOUT_FILE, "w") as f:
        json.dump(layout, f, indent=2)
    print("💾 Layout state saved →", LAYOUT_FILE)


# ------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="Trading Terminal", layout="wide", initial_sidebar_state="collapsed")
    apply_global_style()

    # ==============================================================
    # 🔧 GLOBAL FIX — Fullscreen + No Scroll
    # ==============================================================
    st.markdown("""
    <style>
    html, body {
        margin:0!important;
        padding:0!important;
        height:100vh!important;
        overflow:hidden!important;
        background:#0E1117!important;
    }
    [data-testid="stAppViewContainer"] {
        overflow:hidden!important;
        height:100vh!important;
        padding:0!important;
        margin:0!important;
        background:#0E1117!important;
    }
    [data-testid="stHeader"], [data-testid="stToolbar"],
    #MainMenu, header, footer {display:none!important;}
    .block-container {padding:0!important;margin:0!important;}
    iframe {
        border:none;
        border-radius:0;
        width:100%;
        height:calc(100vh - 132px); /* three 44px bars */
        background:#0B0C0E;
        overflow:hidden;
    }
    </style>
    """, unsafe_allow_html=True)

    # ==============================================================
    # PANELS
    # ==============================================================
    left_sidebar()
    trade_panel()

    # ==============================================================
    # FIXED TOP BAR + TAB ROW + CHART TOOLBAR
    # ==============================================================
    top_bar()
    chart_toolbar()

    # ==============================================================
    # REACT GRID IFRAME — FIXED VIEW
    # ==============================================================
    react_app_path = "http://localhost:8080"
    st.markdown(f"""
    <iframe id="react-draggrid-iframe" src="{react_app_path}" allow="fullscreen"></iframe>
    """, unsafe_allow_html=True)

    # ==============================================================
    # OPTIONAL DEBUG
    # ==============================================================
    layout_state_key = "react_layout_state"
    if layout_state_key not in st.session_state:
        st.session_state[layout_state_key] = load_saved_layout()

    with st.expander("🧩 Layout Debug", expanded=False):
        st.json(st.session_state[layout_state_key])
        if st.button("💾 Save Layout Snapshot"):
            save_layout_state(st.session_state[layout_state_key])
            st.success("Layout snapshot saved successfully!")

    st.markdown("✅ **Phase 23.7 — Top + Tab + Toolbar Aligned · Scroll Locked · 1 : 1 React Match**")

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
