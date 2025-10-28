# ==============================================================
# 💰 TRADE PANEL — Stage 10.7 (Visual Polish + Style Fix)
# ==============================================================

import streamlit as st
from shared.style_manager import apply_global_style

def render_trade_panel():
    apply_global_style()

    st.markdown(
        """
        <style>
        .trade-panel {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 60px;
            background-color: #0d0d0d;
            color: white;
            border-top: 1px solid #333;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 18px;
            z-index: 900;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
        }
        .trade-panel .left {
            display: flex;
            gap: 10px;
        }
        .trade-panel .right {
            display: flex;
            gap: 8px;
        }
        .trade-btn {
            border: none;
            border-radius: 6px;
            padding: 6px 12px;
            cursor: pointer;
            font-weight: 600;
        }
        .buy { background: #1db954; color: white; }
        .sell { background: #e53935; color: white; }
        .close { background: #555; color: white; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ✅ Trade Panel UI
    st.markdown(
        """
        <div class="trade-panel">
            <div class="left">
                <span>💹 Positions: 0 | P&L: ₹0.00</span>
            </div>
            <div class="right">
                <button class="trade-btn buy">BUY</button>
                <button class="trade-btn sell">SELL</button>
                <button class="trade-btn close">CLOSE ALL</button>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ✅ Load wrapper for dashboard import
def load():
    render_trade_panel()
