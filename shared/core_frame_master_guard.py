# ==============================================================
# 📄 FILE: Streamlit_TradingSystems/core_frame_master_guard.py
# ==============================================================
# VERSION: v6.5.10-FullEdgeLock
# PURPOSE:
# - 0 px padding on all sides (top, bottom, left, right)
# - Works persistently after refresh and rerun
# - Safe inside Streamlit’s sandbox (no JS)
# ==============================================================

import streamlit as st

st.set_page_config(
    page_title="Trading Terminal v6.5.10-FullEdgeLock",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Pure CSS override ---
st.markdown(
    """
    <style>
    /* Eliminate all Streamlit layout gaps */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stVerticalBlock"],
    .block-container, section.main > div {
        margin: 0 !important;
        padding: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        max-width: 100vw !important;
        max-height: 100vh !important;
        overflow: hidden !important;
        background: #f8f9fb !important;
        box-sizing: border-box !important;
    }

    /* Remove Streamlit's horizontal padding */
    div.block-container {
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }

    /* Header safe zone */
    [data-testid="stHeader"] {
        overflow: visible !important;
        padding-top: 4px !important;
        padding-bottom: 2px !important;
        z-index: 5 !important;
    }

    /* Hide scrollbars */
    ::-webkit-scrollbar { display: none !important; }

    /* Root container always fits full screen */
    #root, #root > div:first-child {
        height: 100vh !important;
        width: 100vw !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.write(
    "<div style='display:flex;align-items:center;justify-content:center;"
    "height:100%;color:#666;font-size:15px'>✅ <b>v6.5.10-FullEdgeLock</b> — "
    "True fullscreen active (0 px on all sides).</div>",
    unsafe_allow_html=True,
)
