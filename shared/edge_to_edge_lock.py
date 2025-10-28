# ==============================================================
# 🎨 CORE 1 — EDGE TO EDGE LOCK (v6.3.2)
# ==============================================================
# PURPOSE:
#   True 1080p edge-to-edge layout (no top/bottom/side gaps)
#   Removes duplicate tab bar and outer padding automatically.
# ==============================================================

import streamlit as st

def apply_edge_to_edge_lock():
    st.markdown(
        """
        <style>
        /* --- Remove all body margins and padding --- */
        html, body, [data-testid="stAppViewContainer"],
        [data-testid="stHeader"], [data-testid="stDecoration"],
        section.main, .block-container {
            margin:0!important;
            padding:0!important;
            border:none!important;
            width:100%!important;
            max-width:100%!important;
            background:white!important;
        }

        /* --- Remove internal Streamlit block spacing --- */
        [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
            margin:0!important;
            padding:0!important;
            gap:0!important;
        }

        /* --- Force panels and columns to fill width --- */
        .stColumn, .element-container {
            padding:0!important;
            margin:0!important;
        }

        /* --- Remove duplicate tab rows --- */
        [data-baseweb="tab-list"]:not(:first-of-type) {
            display:none!important;
        }

        /* --- Ensure footer sticks to bottom cleanly --- */
        .stMarkdown {margin-bottom:0!important;}

        /* --- Lock everything to full viewport height --- */
        body, html {
            height:100vh!important;
            overflow-y:auto!important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
