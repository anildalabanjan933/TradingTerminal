# ==============================================================
# 📄 FILE: Streamlit_TradingSystems/core_layout_skeleton.py
# ==============================================================
# VERSION: v7.3.3 — ReactGrid Sidebar + Snap Alignment Active
# PURPOSE:
#   Integrates frontend_draggrid React grid with full 6×6 alignment
#   and smooth sidebar toggle (TradingView-style)
# ==============================================================

import streamlit as st
from streamlit.components.v1 import html
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Trading Terminal — ReactGrid v7.3.3",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    html, body {
        margin: 0 !important;
        padding: 0 !important;
        height: 100% !important;
        width: 100% !important;
        overflow: hidden !important;
        background: #f8f9fb !important;
    }
    [data-testid="stHeader"], [data-testid="stToolbar"], footer {display: none !important;}
    .block-container {padding: 0 !important; margin: 0 !important;}
    button {cursor: pointer;}
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div style='text-align:center;font-size:14px;color:#333;padding:4px 0;'>
    Connection: <b>Online</b> | Mode: <b>Compact</b> | Version: <b>v7.3.3</b>
    <span style='float:right;padding-right:28px;'>Account: Demo&nbsp;&nbsp;Time: 21:45 IST</span>
</div>
""", unsafe_allow_html=True)

# ---------- TABS ----------
st.markdown("""
<div style='text-align:center;margin:6px 0;'>
    <b>Intraday</b> | Sector Rotation | Wealth | Journal | Backtest | HA Terminal
</div>
""", unsafe_allow_html=True)

# ---------- TOOLBAR ----------
st.markdown("""
<div style='display:flex;justify-content:center;gap:10px;
            padding:6px 0;border-top:1px solid #ddd;border-bottom:1px solid #ddd;'>
    <button>Symbol</button><button>Interval</button><button>Indicators</button>
    <button>Drawings</button><button>Chart Type</button><button>Settings</button>
</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR TOGGLE ----------
st.markdown("""
<div style='position:fixed;top:120px;left:6px;z-index:999;'>
    <button id='sidebar-toggle' style='border:none;background:#2563eb;color:white;
            border-radius:4px;width:22px;height:22px;font-size:12px;'>⇄</button>
</div>
<script>
document.getElementById("sidebar-toggle").addEventListener("click", () => {
    window.parent.postMessage({type:"toggleSidebar"}, "*");
});
</script>
""", unsafe_allow_html=True)

# ---------- REACT GRID LOADER ----------
bundle_path = os.path.join("frontend_draggrid", "public", "bundle.js")
if os.path.exists(bundle_path):
    with open(bundle_path, "r", encoding="utf-8") as f:
        js_code = f.read()
else:
    st.error("❌ bundle.js not found. Please rebuild with `npx webpack --mode production`.")
    st.stop()

# ---------- RENDER REACT GRID ----------
html(
    f"""
    <div id="root"></div>
    <script>{js_code}</script>
    """,
    height=850,
)

# ---------- FOOTER ----------
st.markdown("""
<div style='text-align:center;margin-top:6px;border-top:1px solid #ddd;
            padding-top:4px;color:#444;'>Trade Panel + Risk Manager</div>
""", unsafe_allow_html=True)

# ---------- SUCCESS STATUS ----------
st.success("✅ v7.3.3 — React Sidebar + SnapAlign grid active.")
