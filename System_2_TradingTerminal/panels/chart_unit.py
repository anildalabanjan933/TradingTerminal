"""
Day 24 — Chart Engine Integration (Plotly + Trade Line Overlay)
File: panels/chart_unit.py
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import uuid
from datetime import datetime, timedelta

# === GLOBAL SETTINGS ===
DEFAULT_TIMEFRAMES = ["1m", "3m", "5m", "15m", "30m", "1h", "4h", "1D"]
DEFAULT_CHART_TYPES = ["Candlestick", "Heikin Ashi", "Line", "Area"]
LINE_COLORS = {"entry": "#00C853", "sl": "#FF1744", "target": "#2979FF"}

# === STATE HANDLERS ===
def _ensure_state(chart_id: str):
    base = f"chart_unit::{chart_id}"
    if base + "::meta" not in st.session_state:
        st.session_state[base + "::meta"] = {
            "symbol": "NSE:NIFTY50",
            "timeframe": "5m",
            "chart_type": "Heikin Ashi",
            "crosshair": True,
            "show_wick": True,
            "entry": None,
            "sl": None,
            "target": None,
        }
    st.session_state.setdefault(base + "::uid", str(uuid.uuid4())[:8])
    return base


def _get_meta(chart_id: str):
    base = _ensure_state(chart_id)
    return st.session_state[base + "::meta"]


# === DATA GENERATOR (Mock for smoke test) ===
def _generate_sample_data(n=150):
    np.random.seed(7)
    t = pd.date_range(datetime.now() - timedelta(minutes=n), periods=n, freq="1min")
    base = 21900 + np.cumsum(np.random.randn(n))
    o = base + np.random.randn(n)
    h = o + np.random.rand(n) * 12
    l = o - np.random.rand(n) * 12
    c = o + np.random.randn(n)
    return pd.DataFrame({"time": t, "open": o, "high": h, "low": l, "close": c})


# === HEIKIN ASHI CONVERSION ===
def _heikin_ashi(df):
    ha_df = df.copy()
    ha_df["HA_Close"] = (df["open"] + df["high"] + df["low"] + df["close"]) / 4
    ha_df["HA_Open"] = (df["open"].shift(1) + df["close"].shift(1)) / 2
    ha_df["HA_High"] = ha_df[["high", "HA_Open", "HA_Close"]].max(axis=1)
    ha_df["HA_Low"] = ha_df[["low", "HA_Open", "HA_Close"]].min(axis=1)
    ha_df.dropna(inplace=True)
    return ha_df


# === PLOTLY CHART RENDERER ===
def _render_plot(meta, df):
    fig = go.Figure()
    chart_type = meta["chart_type"]

    if chart_type == "Heikin Ashi":
        df = _heikin_ashi(df)
        fig.add_trace(go.Candlestick(
            x=df["time"], open=df["HA_Open"], high=df["HA_High"],
            low=df["HA_Low"], close=df["HA_Close"],
            increasing_line_color="#26a69a", decreasing_line_color="#ef5350",
            name="Heikin Ashi", showlegend=False
        ))
    elif chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(
            x=df["time"], open=df["open"], high=df["high"],
            low=df["low"], close=df["close"],
            increasing_line_color="#26a69a", decreasing_line_color="#ef5350",
            name="Candlestick", showlegend=False
        ))
    elif chart_type == "Line":
        fig.add_trace(go.Scatter(x=df["time"], y=df["close"],
                                 mode="lines", name="Line", line=dict(color="#42a5f5")))
    elif chart_type == "Area":
        fig.add_trace(go.Scatter(x=df["time"], y=df["close"],
                                 fill="tozeroy", line=dict(color="#64b5f6"), name="Area"))

    # === GLOBAL TRADE LINES ===
    for key, color in LINE_COLORS.items():
        val = meta.get(key)
        if val and val > 0:
            fig.add_hline(y=val, line_color=color, line_width=1.4,
                          annotation_text=key.upper(),
                          annotation_position="right", annotation_font_size=12)

    fig.update_layout(
        height=420,
        margin=dict(l=5, r=5, t=25, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_rangeslider_visible=False,
        font=dict(size=12),
    )
    return fig


# === MAIN ENTRYPOINT ===
def render_chart_unit(parent, chart_id: str, default_symbol: str = "NSE:NIFTY50"):
    base = _ensure_state(chart_id)
    meta = _get_meta(chart_id)
    meta["symbol"] = meta.get("symbol") or default_symbol

    with parent:
        st.markdown(f"### {meta['symbol']} • {meta['timeframe']} • {meta['chart_type']}")

        # Sample Data (Live feed later)
        df = _generate_sample_data(200)

        # Chart settings layout
        set_cols = st.columns([3, 1, 1])
        with set_cols[1]:
            meta["entry"] = st.number_input("Entry", 0.0, 30000.0, value=meta.get("entry") or 0.0, step=10.0)
        with set_cols[2]:
            meta["sl"] = st.number_input("StopLoss", 0.0, 30000.0, value=meta.get("sl") or 0.0, step=10.0)
            meta["target"] = st.number_input("Target", 0.0, 30000.0, value=meta.get("target") or 0.0, step=10.0)

        # Render chart
        fig = _render_plot(meta, df)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.caption(
            f"🟢 Entry: {meta.get('entry') or '—'} | 🔴 SL: {meta.get('sl') or '—'} | 🔵 Target: {meta.get('target') or '—'}  "
            f"• Crosshair: {'ON' if meta['crosshair'] else 'OFF'} | Wick: {'Shown' if meta['show_wick'] else 'Hidden'}"
        )


# === SMOKE TEST ===
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Smoke Test — Chart Engine (Day 24)")
    c = st.container()
    render_chart_unit(c, "chart1", "NSE:NIFTY50")
