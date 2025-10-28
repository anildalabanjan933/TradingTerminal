# ==============================================================
# 📄 FILE: Streamlit_TradingSystems/shared/order_engine.py
# 🔹 ORDER EXECUTION ENGINE — v5.3.0 (Live-Ready Build Freeze)
# ==============================================================

import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime
import os

# ==============================================================
# ⚙️ ORDER VALIDATION
# ==============================================================
def validate_order(order, risk_limits):
    """Validate quantity, risk, and daily loss before order execution."""
    if not risk_limits:
        return True, "OK"

    if order["risk_pct"] > risk_limits.get("max_risk_pct", 2):
        return False, "❌ Exceeds max risk %"

    if risk_limits.get("daily_loss", 0) + order["expected_loss"] > risk_limits.get("max_daily_loss", 10000):
        return False, "❌ Exceeds daily loss limit"

    if order["qty"] <= 0:
        return False, "❌ Invalid quantity"

    return True, "OK"


# ==============================================================
# 🧾 PAPER TRADE EXECUTION
# ==============================================================
def execute_paper_trade(order):
    """Simulate paper trade for testing (instant execution)."""
    trade = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": order["symbol"],
        "side": order["side"],
        "qty": order["qty"],
        "entry": order["price"],
        "sl": order.get("sl", 0.0),
        "target": order.get("target", 0.0),
        "mode": "Paper",
        "status": "Executed",
    }
    _log_trade(trade)
    st.success(f"🧾 Paper Trade Executed → {order['side']} {order['symbol']} @ {order['price']}")
    return trade


# ==============================================================
# 🚀 REAL TRADE EXECUTION (WITH SAFETY + SNAPSHOT)
# ==============================================================
def execute_real_trade(order, fyers=None):
    """Execute real trade via FYERS API with confirmation & snapshot."""
    if fyers is None:
        st.error("❌ Fyers API not connected.")
        return None

    # Confirm before placing real trade
    st.warning("🚨 REAL TRADE MODE ENABLED — Confirm before execution.")
    confirm = st.checkbox("✅ I confirm I want to execute this real trade.", key=f"confirm_{order['symbol']}")
    if not confirm:
        st.stop()
        st.info("⚠️ Trade cancelled — user confirmation required.")
        return None

    try:
        order_payload = {
            "symbol": order["symbol"],
            "qty": order["qty"],
            "type": 2 if order["side"] == "BUY" else 3,
            "side": 1 if order["side"] == "BUY" else -1,
            "limitPrice": order.get("price", 0),
            "stopPrice": order.get("sl", 0),
            "validity": "DAY",
            "offlineOrder": "false",
        }

        response = fyers.place_order(order_payload)

        # Log trade
        trade_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": order["symbol"],
            "side": order["side"],
            "qty": order["qty"],
            "entry": order.get("price", 0),
            "sl": order.get("sl", 0),
            "target": order.get("target", 0),
            "mode": "Real",
            "status": "Executed",
        }
        _log_trade(trade_data)

        # Save safety snapshot
        snapshot_path = "Streamlit_TradingSystems/System_2_TradingTerminal/snapshots/phase_5_3_0_order_freeze.json"
        os.makedirs(os.path.dirname(snapshot_path), exist_ok=True)
        with open(snapshot_path, "w", encoding="utf-8") as f:
            json.dump({"last_real_trade": trade_data}, f, indent=2)

        st.success(f"✅ Real Trade Placed → {order['side']} {order['symbol']} ({response})")
        return response
    except Exception as e:
        _log_error(f"Real order failed: {e}")
        st.error(f"❌ Order Failed: {e}")
        return None


# ==============================================================
# 📦 MAIN ENTRYPOINT — UNIFIED HANDLER
# ==============================================================
def place_order(symbol, side, qty, price, sl, target, mode="Paper", fyers=None, risk_limits=None):
    """Unified handler for both Paper and Real trades."""
    order = {
        "symbol": symbol,
        "side": side.upper(),
        "qty": qty,
        "price": price,
        "sl": sl,
        "target": target,
        "risk_pct": 1.0,
        "expected_loss": abs(price - sl) * qty,
    }

    valid, msg = validate_order(order, risk_limits)
    if not valid:
        st.error(msg)
        return None

    if mode == "Paper":
        return execute_paper_trade(order)
    elif mode == "Real":
        # Safety: require explicit Real mode confirmation in session state
        if st.session_state.get("trade_mode", "Paper") != "Real":
            st.error("🚫 Real Mode not enabled — switch from sidebar first.")
            return None
        return execute_real_trade(order, fyers)
    else:
        st.error("❌ Unknown mode.")
        return None


# ==============================================================
# 🧮 LOGGING UTILITIES
# ==============================================================
def _log_trade(trade):
    log_path = "Streamlit_TradingSystems/System_2_TradingTerminal/logs/trade_logs.csv"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    df = pd.DataFrame([trade])
    if os.path.exists(log_path):
        df.to_csv(log_path, mode="a", header=False, index=False)
    else:
        df.to_csv(log_path, index=False)


def _log_error(message):
    error_path = "Streamlit_TradingSystems/System_2_TradingTerminal/logs/error_logs.txt"
    os.makedirs(os.path.dirname(error_path), exist_ok=True)
    with open(error_path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} — {message}\n")


# ==============================================================
# 🧪 SMOKE TEST (LOCAL)
# ==============================================================
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Smoke Test — Order Execution Engine v5.3.0")

    symbol = st.text_input("Symbol", "NSE:NIFTY50")
    side = st.selectbox("Side", ["BUY", "SELL"])
    qty = st.number_input("Quantity", 0, 10000, 50)
    price = st.number_input("Price", 0.0, 30000.0, 22000.0)
    sl = st.number_input("StopLoss", 0.0, 30000.0, 21900.0)
    target = st.number_input("Target", 0.0, 30000.0, 22100.0)
    mode = st.selectbox("Mode", ["Paper", "Real"])

    if st.button("Place Order"):
        result = place_order(symbol, side, qty, price, sl, target, mode)
        st.write(result)
