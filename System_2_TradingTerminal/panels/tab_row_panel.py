# ==============================================================
# 📄 FILE: panels/tab_row_panel.py
# Phase 6.2.0-F23a — Active Tab Row Renderer (Visible + Zero-Gap)
# ==============================================================

import streamlit as st

# --------------------------------------------------------------
# 🎨 Inject CSS — Clean Fusion with Top Bar (0 px vertical offset)
# --------------------------------------------------------------
def _inject_tab_style():
    st.markdown("""
    <style>
    /* Remove Streamlit default padding and margins */
    div[data-testid="stHorizontalBlock"],
    div[data-testid="stVerticalBlock"],
    div[data-testid="stVerticalBlock"] > div {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Eliminate vertical spacing above and below tabs */
    [data-testid="stTabs"] {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        background: white !important;
    }

    /* Perfect alignment of tab headers */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0 !important;
        justify-content: flex-start !important;
        align-items: center !important;
    }

    /* Style tab labels for visual clarity */
    .stTabs [data-baseweb="tab"] {
        padding: 4px 14px !important;
        font-weight: 600 !important;
        border-bottom: 2px solid transparent !important;
        color: #333 !important;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 2px solid #0078ff !important;
        color: #0078ff !important;
    }

    /* Prevent flicker or ghost background */
    [data-testid="stAppViewContainer"] {
        background: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --------------------------------------------------------------
# 🧩 MAIN RENDER FUNCTION — Visible Tabs + Layout Verification
# --------------------------------------------------------------
def render():
    _inject_tab_style()

    # Create interactive tabs
    tabs = st.tabs([
        "📊 Intraday",
        "📈 Sector Rotation",
        "💰 Wealth",
        "🧾 Journal",
        "🔍 Backtest",
        "🧮 HA Terminal"
    ])

    # Provide visible placeholder text in each tab
    with tabs[0]:
        st.markdown("<h4>📊 Intraday Workspace Loaded</h4>", unsafe_allow_html=True)
    with tabs[1]:
        st.markdown("<h4>📈 Sector Rotation Workspace</h4>", unsafe_allow_html=True)
    with tabs[2]:
        st.markdown("<h4>💰 Wealth Creation Dashboard</h4>", unsafe_allow_html=True)
    with tabs[3]:
        st.markdown("<h4>🧾 Trading Journal Module</h4>", unsafe_allow_html=True)
    with tabs[4]:
        st.markdown("<h4>🔍 Backtesting Center</h4>", unsafe_allow_html=True)
    with tabs[5]:
        st.markdown("<h4>🧮 HA Terminal — Analytics Hub</h4>", unsafe_allow_html=True)

    # Log message for verification
    st.markdown("""
    <script>console.log("✅ Tab Row Rendered — F23a Visible + Aligned");</script>
    """, unsafe_allow_html=True)
