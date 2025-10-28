# ==============================================================
# 📄 FILE: Streamlit_TradingSystems/System_2_TradingTerminal/panels/watchlist_scanner_panel.py
# ==============================================================
# VERSION: v9.0.1 — Stage 9.0 (Polish + Z-Index + Align)
# PURPOSE:
# ✅ Shows Scanner + Watchlists flush with chart
# ✅ Fixed z-index / render order (always visible)
# ✅ Unified fonts / colors / no header gaps
# ==============================================================

import streamlit as st
from streamlit.components.v1 import html

def render_watchlist_scanner_stack():
    html("""
    <style>
    /* === Right-Column Wrapper === */
    .right-stack {
        position: fixed;
        top: 138px;                       /* below top bars */
        right: 0;
        width: 340px;
        height: calc(100vh - 180px);      /* above trade panel */
        display: flex;
        flex-direction: column;
        background: #ffffff;
        border-left: 1px solid #dcdcdc;
        overflow: hidden;
        z-index: 450;                     /* ensure above chart */
        box-sizing: border-box;
    }

    /* === Individual Panels === */
    .stack-panel {
        flex: 1;
        border-bottom: 1px solid #e6e6e6;
        padding: 10px 14px;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: #222;
        overflow-y: auto;
    }
    .stack-panel:last-child { border-bottom: none; }

    /* === Titles === */
    .panel-title {
        font-weight: 600;
        color: #111;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* === Rows === */
    .symbol-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 3px 0;
        border-bottom: 1px solid #f1f1f1;
    }
    .symbol-row:last-child { border-bottom: none; }
    .symbol-row span { color: #333; }
    </style>

    <div class="right-stack">
        <div class="stack-panel">
            <div class="panel-title">🔍 Scanner</div>
            <div class="symbol-row"><span>INFY</span><span>+0.65%</span></div>
            <div class="symbol-row"><span>TCS</span><span>+0.42%</span></div>
            <div class="symbol-row"><span>HDFCBANK</span><span>-0.18%</span></div>
        </div>

        <div class="stack-panel">
            <div class="panel-title">📋 Watchlist 1</div>
            <div class="symbol-row"><span>NIFTY</span><span>+0.82%</span></div>
            <div class="symbol-row"><span>BANKNIFTY</span><span>+0.74%</span></div>
            <div class="symbol-row"><span>SBIN</span><span>-0.25%</span></div>
        </div>

        <div class="stack-panel">
            <div class="panel-title">📊 Watchlist 2</div>
            <div class="symbol-row"><span>RELIANCE</span><span>+0.51%</span></div>
            <div class="symbol-row"><span>ICICIBANK</span><span>+0.27%</span></div>
            <div class="symbol-row"><span>ITC</span><span>-0.12%</span></div>
        </div>
    </div>
    """)
