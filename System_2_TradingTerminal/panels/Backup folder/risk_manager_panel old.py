# ============================================================
# 📄 FILE: panels/risk_manager_panel old.py
# ============================================================
# Phase 4.9.1 — Risk Manager Panel (Session-State Bridge)
# ============================================================
# PURPOSE:
# - Calculate risk, qty, margin, R:R live
# - Push data to st.session_state["risk_params"]
# - Provide real-time safety checks for Alert Manager bridge
# - Works in mock/safe mode (no Fyers dependency)
# ============================================================

import streamlit as st
import datetime
import random

# -------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------
def calc_rr(entry, sl, target):
    try:
        return round(abs((target - entry) / (entry - sl)), 2)
    except ZeroDivisionError:
        return 0.0


def calc_auto_qty(capital, risk_pct, entry, sl):
    diff = abs(entry - sl)
    if diff == 0:
        return 0
    risk_amt = capital * (risk_pct / 100)
    return int(risk_amt / diff)


def calc_margin(qty, entry, leverage):
    try:
        return round((qty * entry) / leverage, 2)
    except ZeroDivisionError:
        return 0.0


def mock_brokerage_plan():
    return {"Fyers": {"brokerage": 20, "gst": 18, "stt": 0.1, "stamp": 0.015}}


def calc_brokerage(qty, entry, exit_price, plan):
    trade_value = qty * (entry + exit_price) / 2
    b = plan["brokerage"]
    gst = plan["gst"] / 100
    stt = plan["stt"] / 100
    stamp = plan["stamp"] / 100
    total = b + (b * gst) + (trade_value * (stt + stamp))
    return round(total, 2)


# -------------------------------------------------------
# UPDATE SHARED RISK PARAMS IN SESSION STATE
# -------------------------------------------------------
def update_risk_state(capital, risk_pct, entry, sl, target, leverage):
    rr = calc_rr(entry, sl, target)
    qty = calc_auto_qty(capital, risk_pct, entry, sl)
    margin_used = calc_margin(qty, entry, leverage)
    plan = mock_brokerage_plan()["Fyers"]
    charges = calc_brokerage(qty, entry, target, plan)

    safe = True
    if margin_used > capital * 0.9:
        safe = False

    st.session_state["risk_params"] = {
        "capital": capital,
        "risk_pct": risk_pct,
        "qty": qty,
        "rr": rr,
        "margin_used": margin_used,
        "safe": safe,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
    }


# -------------------------------------------------------
# MAIN PANEL RENDER
# -------------------------------------------------------
def render():
    st.subheader("💰 Risk & Money Management (Phase 4.9.1 Bridge Active)")

    # --- Mock live LTP ---
    ltp = round(100 + random.uniform(-3, 3), 2)

    # --- Inputs ---
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        capital = st.number_input("Total Capital (₹)", value=100000.0, step=1000.0)
        risk_pct = st.slider("Risk per Trade (%)", 0.1, 5.0, 1.0)
    with col2:
        entry = st.number_input("Entry Price", value=ltp, step=0.1)
        sl = st.number_input("Stop Loss", value=ltp - 2, step=0.1)
    with col3:
        target = st.number_input("Target", value=ltp + 4, step=0.1)
        leverage = st.slider("Leverage (×)", 1, 100, 10)

    # --- Calculations ---
    rr = calc_rr(entry, sl, target)
    qty = calc_auto_qty(capital, risk_pct, entry, sl)
    margin_used = calc_margin(qty, entry, leverage)
    plan = mock_brokerage_plan()["Fyers"]
    charges = calc_brokerage(qty, entry, target, plan)
    pnl = (target - entry) * qty - charges
    pnl_color = "#00d26a" if pnl > 0 else "#ff4d4d"

    # --- Push data to session_state ---
    update_risk_state(capital, risk_pct, entry, sl, target, leverage)
    risk = st.session_state["risk_params"]

    # --- Display metrics ---
    st.markdown("---")
    st.markdown(f"""
    **🎯 R:R Ratio:** `{rr}`  
    **📦 Auto Quantity:** `{qty}` | **💵 Margin Used:** ₹ {margin_used:,}  
    **💰 Net P&L (after charges):** <span style='color:{pnl_color};font-weight:600;'>₹ {round(pnl,2)}</span>  
    **🕒 Last Sync:** `{risk['timestamp']}`
    """, unsafe_allow_html=True)

    if not risk["safe"]:
        st.error("❌ Margin exceeds 90% of capital — trade blocked.")
    else:
        st.success("✅ Within safe risk limit.")

    st.markdown("---")
    st.markdown("### ⚙️ Auto-Link Settings")
    st.checkbox("Auto link with Trade Panel", value=True)
    st.checkbox("Auto apply SL/Target updates", value=True)
    st.checkbox("Auto-block trades beyond daily risk limit", value=True)

    st.caption(f"Session-State Bridge Active → alert_order_manager.py | {datetime.datetime.now().strftime('%H:%M:%S')}")


# -------------------------------------------------------
# LOCAL TEST
# -------------------------------------------------------
if __name__ == "__main__":
    st.set_page_config(page_title="Risk Manager (Bridge Mode)", layout="wide")
    render()
