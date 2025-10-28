# ==============================================================
# 🎨 STYLE MANAGER — Stage 10.7 (Global Typography + Theme)
# ==============================================================

import streamlit as st

# --------------------------------------------------------------
# Apply consistent global typography + theme
# --------------------------------------------------------------
def apply_global_style():
    st.markdown(
        """
        <style>
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            color: #111111;
        }
        /* Dark/Light base toggle ready */
        body[data-theme="dark"], .dark-theme {
            background-color: #0d0d0d !important;
            color: #ffffff !important;
        }
        .light-theme {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        /* Smooth transitions for theme change */
        * {
            transition: background-color 0.25s ease, color 0.25s ease;
        }
        /* Button visuals */
        button, .stButton>button {
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
            padding: 6px 12px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------
# Optional helper for color tokens (future visual pass)
# --------------------------------------------------------------
def get_color_tokens(mode="light"):
    if mode == "dark":
        return {
            "bg": "#0d0d0d",
            "text": "#ffffff",
            "border": "#333333",
            "accent": "#0084ff",
        }
    else:
        return {
            "bg": "#ffffff",
            "text": "#000000",
            "border": "#e0e0e0",
            "accent": "#111111",
        }
