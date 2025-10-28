# ==============================================================
# 📄 FILE: panels/tab_toolbar_stack.py
# Phase 6.2.0-F23 — Remove Toolbar↔Tabs Gap (Circular-Safe)
# ==============================================================

import streamlit as st
from panels import chart_toolbar  # ✅ only import toolbar here (no tab_row_panel)

def render(tab_row_callback):
    """
    Renders the unified chart toolbar + tab row block.
    The tab row is rendered through the callback to avoid circular import.
    """

    # Tighten vertical connection between toolbar and tabs
    st.markdown("""
    <style>
    /* Remove spacing between chart toolbar and tab row */
    [data-testid="stVerticalBlock"] > div:has(div[data-testid="stTabs"]) {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    div[data-testid="stVerticalBlock"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stHorizontalBlock"] {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 🔝 Render Toolbar
    chart_toolbar.render()

    # 🔽 Render Tabs via safe callback
    tab_row_callback()
