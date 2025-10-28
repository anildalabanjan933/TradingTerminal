"""
Day 26 — Alert Logic (Heikin-Ashi Body Cross / Real Price)
File: shared/alert_logic.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
from datetime import datetime

# ==========================================================
# ⚙️ CORE ALERT FUNCTIONS
# ==========================================================
def heikin_ashi_transform(df: pd.DataFrame):
    """Convert OHLC to Heikin-Ashi format."""
    ha_df = df.copy()
    ha_df["HA_Close"] = (df["open"] + df["high"] + df["low"] + df["close"]) / 4
    ha_df["HA_Open"] = (df["open"].shift(1) + df["close"].shift(1)) / 2
    ha_df["HA_High"] = ha_df[["high", "HA_Open", "HA_Close"]].max(axis=1)
    ha_df["HA_Low"] = ha_df[["low", "HA_Open", "HA_Close"]].min(axis=1)
    ha_df.dropna(inplace=True)
    return ha_df


def check_ha_body_cross(df: pd.DataFrame, line_value: float):
    """Detect HA body crossing line."""
    if len(df) < 2:
        return False
    prev = df.iloc[-2]
    curr = df.iloc[-1]
    # Cross when previous body below and current body above (or vice versa)
    cross_up = (prev["HA_Close"] < line_value) and (curr["HA_Open"] > line_value or curr["HA_Close"] > line_value)
    cross_down = (prev["HA_Close"] > line_value) and (curr["HA_Open"] < line_value or curr["HA_Close"] < line_value)
    return cross_up or cross_down


def check_ha_body_touch(df: pd.DataFrame, line_value: float):
    """Detect HA body touch (open ≤ line ≤ close)."""
    if len(df) == 0:
        return False
    curr = df.iloc[-1]
    return curr["HA_Open"] <= line_value <= curr["HA_Close"] or curr["HA_Close"] <= line_value <= curr["HA_Open"]


def check_price_cross(df: pd.DataFrame, line_value: float):
    """Detect real price cross with open/high/low/close."""
    if len(df) < 2:
        return False
    prev = df.iloc[-2]
    curr = df.iloc[-1]
    cross_up = (prev["close"] < line_value) and (curr["close"] > line_value)
    cross_down = (prev["close"] > line_value) and (curr["close"] < line_value)
    return cross_up or cross_down


def check_price_touch(df: pd.DataFrame, line_value: float):
    """Detect real price touch (low ≤ line ≤ high)."""
    if len(df) == 0:
        return False
    curr = df.iloc[-1]
    return curr["low"] <= line_value <= curr["high"]

# ==========================================================
# ⚡ ALERT GENERATION
# ==========================================================
def generate_alert(event_type: str, symbol: str, line_key: str, line_value: float):
    """Build alert payload."""
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event": event_type,
        "symbol": symbol,
        "line": line_key,
        "price": round(line_value, 2)
    }


def dispatch_alert(alert: dict, mode="popup", webhook_url=None):
    """Send or show alert."""
    msg = f"⚠️ {alert['symbol']} | {alert['line'].upper()} {alert['event']} @ {alert['price']}"
    if mode == "popup":
        st.warning(msg)
    elif mode == "toast":
        st.toast(msg)
    elif mode == "webhook" and webhook_url:
        try:
            requests.post(webhook_url, json=alert, timeout=3)
        except Exception:
            st.error("❌ Webhook failed.")
    else:
        st.info(msg)


# ==========================================================
# 🔍 MAIN MONITOR LOOP
# ==========================================================
def monitor_chart(df: pd.DataFrame, meta: dict, use_heikin_ashi=True, sensitivity="Strict"):
    """Check chart for any HA body or real price cross/touch events."""
    alerts = []
    if df.empty:
        return alerts

    if use_heikin_ashi:
        df = heikin_ashi_transform(df)

    for line_key in ["entry", "sl", "target"]:
        value = meta.get(line_key)
        if not value or value <= 0:
            continue

        if use_heikin_ashi:
            crossed = check_ha_body_cross(df, value)
            touched = check_ha_body_touch(df, value)
        else:
            crossed = check_price_cross(df, value)
            touched = check_price_touch(df, value)

        if crossed:
            alerts.append(generate_alert("cross", meta["symbol"], line_key, value))
        elif sensitivity == "Lenient" and touched:
            alerts.append(generate_alert("touch", meta["symbol"], line_key, value))

    for alert in alerts:
        dispatch_alert(alert, mode="toast")

    return alerts


# ==========================================================
# 🧪 SMOKE TEST
# ==========================================================
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Smoke Test — Alert Logic (Day 26)")

    data = {
        "open": np.random.uniform(21900, 22000, 100),
        "high": np.random.uniform(22000, 22100, 100),
        "low": np.random.uniform(21800, 21900, 100),
        "close": np.random.uniform(21900, 22000, 100),
    }
    df = pd.DataFrame(data)
    df["time"] = pd.date_range(end=datetime.now(), periods=100, freq="1min")

    meta = {"symbol": "NSE:NIFTY50", "entry": 21950, "sl": 21900, "target": 22050}
    st.write("✅ Running cross/touch detection...")
    alerts = monitor_chart(df, meta, use_heikin_ashi=True, sensitivity="Lenient")
    st.write(alerts)
