# ==============================================================
# 📄 FILE: Streamlit_TradingSystems/System_2_TradingTerminal/panels/risk_manager_panel.py
# ==============================================================
# VERSION: v7.2.1 — Polish Phase (Fade-in Unified Card)
# PURPOSE:
# Bottom-left Risk & Money Management panel beside Trade Panel
# Calculates SL%, Target%, R:R, Auto Qty from Risk%
# ==============================================================

import streamlit as st
from shared.style_manager import animated_card

# ==============================================================
# 🎨 STYLE — RISK MANAGER PANEL
# ==============================================================

def _inject_risk_panel_css():
    st.markdown("""
    <style>
    .risk-panel {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 340px;
        height: 260px;
        background: var(--background);
        border-top: 1px solid var(--border_color);
        border-right: 1px solid var(--border_color);
        box-shadow: -2px -2px 10px rgba(0,0,0,0.1);
        border-top-right-radius: var(--radius-lg);
        animation: fadeIn var(--fade-duration) ease-in-out;
        overflow: hidden;
        z-index: 98;
    }

    .risk-header {
        background: var(--header_bg);
        border-bottom: 1px solid var(--border_color);
        padding: 6px 10px;
        font-weight: 600;
        font-size: 13px;
    }

    .risk-body {
        padding: 10px;
        display: flex;
        flex-direction: column;
        gap: var(--gap-sm);
    }

    .risk-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 13px;
    }

    .risk-row input {
        width: 90px;
        padding: 4px 6px;
        border-radius: var(--radius-sm);
        border: 1px solid var(--border_color);
        font-size: 13px;
    }

    .risk-button {
        background: var(--accent);
        color: white;
        border: none;
        padding: 6px 10px;
        border-radius: var(--radius-md);
        cursor: pointer;
        font-size: 12px;
        font-weight: 500;
        transition: all var(--transition-fast);
    }

    .risk-button:hover {
        background: var(--accent_soft);
    }

    .risk-summary {
        background: var(--background_alt);
        border-radius: var(--radius-md);
        padding: 6px 8px;
        margin-top: var(--gap-sm);
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================
# ⚙️ RISK MANAGER COMPONENT
# ==============================================================

def render_risk_manager():
    _inject_risk_panel_css()

    risk_percent = st.session_state.get("risk_percent", 1)
    sl_percent = st.session_state.get("sl_percent", 0.5)
    target_percent = st.session_state.get("target_percent", 1.5)
    rr_ratio = round(target_percent / sl_percent, 2)
    qty = int(100 * risk_percent / sl_percent)

    risk_html = f"""
    <div class="risk-panel fade-in">
        <div class="risk-header">🧮 Risk Manager</div>
        <div class="risk-body">
            <div class="risk-row">
                <label>Risk %:</label>
                <input type="number" value="{risk_percent}" step="0.1"/>
            </div>
            <div class="risk-row">
                <label>Stop Loss %:</label>
                <input type="number" value="{sl_percent}" step="0.1"/>
            </div>
            <div class="risk-row">
                <label>Target %:</label>
                <input type="number" value="{target_percent}" step="0.1"/>
            </div>
            <button class="risk-button">Auto Calculate</button>
            <div class="risk-summary">
                <b>R:R Ratio:</b> {rr_ratio} <br/>
                <b>Suggested Qty:</b> {qty}
            </div>
        </div>
    </div>
    """
    st.markdown(risk_html, unsafe_allow_html=True)

# ==============================================================
# ✅ TEST (STANDALONE)
# ==============================================================

if __name__ == "__main__":
    from shared.style_manager import load_styles
    load_styles()
    render_risk_manager()
