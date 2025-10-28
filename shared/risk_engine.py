"""
Day 28 — Risk Engine + Position Sync (Fixed)
File: shared/risk_engine.py
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================================
# ⚙️ CORE RISK CALCULATIONS
# ==========================================================
def calculate_position_size(entry, sl, capital, risk_pct):
    """Auto-calculate position size based on capital and SL distance."""
    if sl <= 0 or entry <= 0:
        return 0
    risk_amount = (capital * risk_pct) / 100
    per_unit_risk = abs(entry - sl)
    if per_unit_risk == 0:
        return 0
    qty = max(int(risk_amount // per_unit_risk), 1)
    return qty


def calculate_charges(qty, price, side="BUY"):
    """Estimate brokerage, taxes, and slippage for paper & real P&L."""
    turnover = qty * price
    brokerage = min(20, 0.0003 * turnover)
    stt = 0.00025 * turnover
    exchange_fee = 0.0000345 * turnover
    gst = 0.18 * (brokerage + exchange_fee)
    stamp = 0.00015 * turnover if side == "BUY" else 0
    slippage = 0.0005 * turnover  # 0.05% assumed
    total = brokerage + stt + exchange_fee + gst + stamp + slippage
    return round(total, 2)


def validate_daily_loss(current_loss, max_daily_loss):
    """Block trading if max daily loss reached."""
    if current_loss >= max_daily_loss:
        st.error("🚫 Max daily loss reached — trading blocked for the day.")
        return False
    return True


# ==========================================================
# 🔄 POSITION SYNC + P&L TRACKER
# ==========================================================
def sync_positions(order, trade_logs_path):
    """Sync open positions & update P&L."""
    os.makedirs(os.path.dirname(trade_logs_path), exist_ok=True)
    df = pd.read_csv(trade_logs_path) if os.path.exists(trade_logs_path) else pd.DataFrame()

    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": order["symbol"],
        "side": order["side"],
        "qty": order["qty"],
        "entry": order["price"],
        "sl": order.get("sl", 0.0),
        "target": order.get("target", 0.0),
        "charges": calculate_charges(order["qty"], order["price"], order["side"]),
        "status": "Open",
    }

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(trade_logs_path, index=False)
    return df


def calculate_pnl(entry, exit_price, qty, charges):
    """Compute net P&L after brokerage, tax, and slippage."""
    gross = (exit_price - entry) * qty
    net = gross - charges
    return round(net, 2)


# ==========================================================
# 📦 RISK SNAPSHOT
# ==========================================================
def get_risk_snapshot(trade_logs_path, capital, max_daily_loss):
    """Return real-time portfolio exposure and losses."""
    if not os.path.exists(trade_logs_path):
        return {"open_positions": 0, "daily_loss": 0, "margin_used": 0}

    df = pd.read_csv(trade_logs_path)

    # ✅ Fix: ensure 'status' column exists
    if "status" not in df.columns:
        df["status"] = "Open"

    open_trades = df[df["status"] == "Open"]
    margin_used = (open_trades["qty"] * open_trades["entry"]).sum()
    pnl_today = 0

    if "exit" in df.columns:
        df["pnl"] = (df["exit"] - df["entry"]) * df["qty"] - df["charges"]
        pnl_today = df["pnl"].sum()

    exposure = round((margin_used / capital) * 100, 2) if capital > 0 else 0
    valid = validate_daily_loss(abs(pnl_today), max_daily_loss)
    return {
        "open_positions": len(open_trades),
        "margin_used": margin_used,
        "exposure_pct": exposure,
        "daily_loss": round(pnl_today, 2),
        "trade_allowed": valid,
    }


# ==========================================================
# 🧪 SMOKE TEST
# ==========================================================
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Smoke Test — Risk Engine + Position Sync (Day 28)")

    capital = st.number_input("Capital (₹)", 0.0, 10000000.0, 100000.0)
    risk_pct = st.slider("Risk % per trade", 0.0, 5.0, 1.0)
    entry = st.number_input("Entry", 0.0, 30000.0, 22000.0)
    sl = st.number_input("StopLoss", 0.0, 30000.0, 21900.0)

    qty = calculate_position_size(entry, sl, capital, risk_pct)
    st.write(f"Auto Quantity → **{qty}** units")

    order = {"symbol": "NSE:NIFTY50", "side": "BUY", "qty": qty, "price": entry, "sl": sl, "target": 22100}
    trade_path = "Streamlit_TradingSystems/System_2_TradingTerminal/logs/trade_logs.csv"
    if st.button("Sync Order"):
        df = sync_positions(order, trade_path)
        st.dataframe(df.tail())

    snap = get_risk_snapshot(trade_path, capital, max_daily_loss=5000)
    st.write("📊 Risk Snapshot:", snap)
