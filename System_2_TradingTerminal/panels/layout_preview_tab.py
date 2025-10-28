import streamlit as st
import streamlit.components.v1 as components
import os

def layout_preview_tab():
    st.title("📊 Layout Preview – Trading Terminal")

    # --- Minimal styling to remove Streamlit padding ---
    st.markdown("""
    <style>
        .block-container, .stApp, iframe, html, body {
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Correct file path for inline version ---
    html_file = os.path.join(
        "Streamlit_TradingSystems",
        "System_2_TradingTerminal",
        "tests",
        "trading_terminal_grid_test_inline.html"
    )

    # --- Show path info for verification ---
    st.success(f"✅ Current layout file path — `{os.path.abspath(html_file)}`")

    # --- Load and render inline HTML ---
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            html_code = f.read()
        components.html(html_code, height=1080, scrolling=False)
    except Exception as e:
        st.error(f"❌ Layout preview file not found or invalid: {e}")
