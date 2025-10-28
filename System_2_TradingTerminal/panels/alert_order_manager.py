# ============================================================
# 📄 FILE: panels/alert_order_manager.py
# ============================================================
# Phase 4.9.1 — Alert ↔ Risk Manager Bridge (Mock Session-State)
# ============================================================
# PURPOSE:
# - Display global trade lines (Entry/SL/Target)
# - Auto-pull risk metrics from session_state["risk_params"]
# - Show live Auto-Qty, R:R, Margin, and Risk Guard
# - Simulate order trigger (Paper/Mock)
# ============================================================

import streamlit as st
import datetime
import random

# ---------------------------------------------
# MOCK PRICE
# ---------------------------------------------
def mock_price():
    return round(100 + random.uniform(-3, 3), 2)

# ---------------------------------------------
# FETCH RISK PARAMS FROM SESSION STATE
# ---------------------------------------------
def get_risk_params():
    """Reads current risk settings from session_state or creates mock defaults."""
    default_risk = {
        "capital": 100000,
        "risk_pct": 1.0,
        "qty": 50,
        "rr": 2.0,
        "margin_used": 10000,
        "safe": True
    }
    if "risk_params" not in st.session_state:
        st.session_state["risk_params"] = default_risk
    return st.session_state["risk_params"]

# ---------------------------------------------
# RENDER TRADE LINES
# ---------------------------------------------
def render_trade_lines():
    st.markdown("""
    <style>
    .trade-line {
        width: 100%;
        height: 2px;
        position: relative;
        margin: 18px 0;
        border-radius: 2px;
    }
    .entry {background: #00d26a;}
    .stop {background: #ff4d4d;}
    .target {background: #007bff;}
    .line-label {
        position: absolute;
        left: 0;
        top: -18px;
        font-size: 12px;
        font-family: 'Inter', sans-serif;
        color: #e6eef8;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='trade-line entry'><span class='line-label'>ENTRY</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='trade-line stop'><span class='line-label'>STOP LOSS</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='trade-line target'><span class='line-label'>TARGET</span></div>", unsafe_allow_html=True)

# ---------------------------------------------
# MAIN RENDER FUNCTION
# ---------------------------------------------
def render():
    st.subheader("🧭 Alert + Order Manager — Risk Bridge Active")
    st.caption("Phase 4.9.1 | Linked to Mock Risk Manager")

    # Mock price & lines
    price = mock_price()
    render_trade_lines()

    st.metric("Current Price", f"₹ {price}")

    # Input fields
    col1, col2, col3 = st.columns(3)
    with col1:
        entry = st.number_input("Entry", value=price, step=0.1, format="%.2f")
    with col2:
        sl = st.number_input("Stop Loss", value=price - 2, step=0.1, format="%.2f")
    with col3:
        target = st.number_input("Target", value=price + 4, step=0.1, format="%.2f")

    # Fetch current risk parameters
    risk = get_risk_params()

    # Display bridge metrics
    st.markdown("---")
    st.markdown(f"""
    **💰 Capital:** ₹ {risk['capital']:,} | **Risk %:** {risk['risk_pct']} %  
    **📦 Auto Qty:** `{risk['qty']}` | **🎯 R:R Ratio:** `{risk['rr']}`  
    **💵 Margin Used:** ₹ {risk['margin_used']:,}  
    """)
    if not risk["safe"]:
        st.error("❌ Risk Guard Active — Trade Blocked (Exceeds Daily Limit)")
    else:
        st.success("✅ Risk Parameters OK — Trade Allowed")

    # Settings
    st.markdown("---")
    mode = st.radio("Trigger Mode", ["Price Cross", "HA Body Cross", "HA Body Touch"], horizontal=True)
    trail = st.selectbox("Trailing SL Mode", ["None", "Step %", "ATR", "Fixed %"], index=0)
    st.checkbox("Enable Sound Alert", value=True)
    st.checkbox("Popup Notification", value=True)

    # Trigger button with guard
    st.markdown("---")
    trigger_col, log_col = st.columns([1,3])
    with trigger_col:
        if st.button("🚀 Simulate Trigger"):
            if risk["safe"]:
                msg = f"✅ Order Triggered @ {datetime.datetime.now().strftime('%H:%M:%S')} | Mode: {mode}"
                st.session_state["last_order"] = {
                    "time": datetime.datetime.now().strftime('%H:%M:%S'),
                    "entry": entry, "sl": sl, "target": target,
                    "qty": risk["qty"], "mode": mode
                }
                st.success(msg)
            else:
                st.error("❌ Order Blocked by Risk Guard ⚠️")

    with log_col:
        if "last_order" in st.session_state:
            order = st.session_state["last_order"]
            st.info(f"Last Order → Qty {order['qty']} @ {order['entry']} (Mode: {order['mode']})")

    st.caption(f"Updated {datetime.datetime.now().strftime('%H:%M:%S')} | Bridge Mock Active")

# ---------------------------------------------
# SMOKE TEST
# ---------------------------------------------
if __name__ == "__main__":
    st.set_page_config(page_title="Alert + Order Manager Bridge", layout="wide")
    render()
