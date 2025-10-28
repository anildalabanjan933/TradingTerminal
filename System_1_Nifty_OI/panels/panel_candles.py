"""
System_1_Nifty_OI/panels/panel_candles.py
-----------------------------------------
Candles + TOI placeholder panel for the demo.

INSTRUCTIONS (follow exactly):
1) Delete the existing file at System_1_Nifty_OI/panels/panel_candles.py
2) Paste this entire content as the new file.
3) Run streamlit (if not running): python -m streamlit run System_1_Nifty_OI/dashboard real.py
4) Panel renders in DEMO/mock mode using random/mock data.

Notes:
- Uses matplotlib only (no seaborn).
- No hard-coded colors are set (matplotlib defaults used).
- Designed to be robust if real data arrives later; accepts `data` dict with keys:
    - 'prices': list-like of floats
    - 'times': list-like of datetimes/strings
    - 'volumes': list-like of ints
If not provided, it generates a mock series.
"""

from __future__ import annotations
from typing import Optional, Any, Dict
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random
import numpy as np
from datetime import datetime, timedelta

def _make_mock_series(n=60, start_price=22250.0):
    times = [datetime.now() - timedelta(minutes=(n - i)) for i in range(n)]
    prices = []
    p = float(start_price)
    for _ in range(n):
        # small random walk
        p += random.uniform(-8, 8)
        prices.append(round(p, 2))
    volumes = [int(abs(random.gauss(5000, 2000))) for _ in range(n)]
    return times, prices, volumes

def _plot_price_volume(times, prices, volumes, figsize=(9, 3.5)):
    # Convert times to matplotlib date format
    md_times = mdates.date2num(times)

    fig = plt.Figure(figsize=figsize, dpi=100)
    ax_price = fig.add_axes([0.05, 0.30, 0.92, 0.65])  # left, bottom, width, height
    ax_vol = fig.add_axes([0.05, 0.08, 0.92, 0.20], sharex=ax_price)

    # Price line (no explicit color)
    ax_price.plot_date(md_times, prices, "-", linewidth=1)
    ax_price.set_ylabel("Price")
    ax_price.xaxis_date()
    ax_price.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax_price.grid(axis="y", linestyle=":", linewidth=0.5)

    # Volume as bar
    ax_vol.bar(md_times, volumes, width=0.0006 * len(md_times) + 0.0002)
    ax_vol.set_ylabel("Vol")
    ax_vol.set_xlabel("Time")
    ax_vol.grid(axis="y", linestyle=":", linewidth=0.3)

    # Auto-rotate date labels
    for label in ax_price.get_xticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment('right')

    fig.tight_layout()
    return fig

def render(key: Optional[str] = None, data: Optional[Dict[str, Any]] = None):
    """
    Renders the Candles + TOI panel into the current Streamlit context.
    Accepts `data` dict (optional) — if missing, mock data is used.
    """
    st.session_state.setdefault("panel_candles_loaded", True)
    st.write("")  # small spacer

    try:
        if data and isinstance(data, dict):
            prices = data.get("prices", None)
            times = data.get("times", None)
            volumes = data.get("volumes", None)
        else:
            prices = times = volumes = None

        if not prices or not times or not volumes or len(prices) < 6:
            times, prices, volumes = _make_mock_series(n=80, start_price=data.get("last_price", 22250.0) if data else 22250.0)

        # Plot
        fig = _plot_price_volume(times, prices, volumes, figsize=(9, 4))
        st.pyplot(fig)

        # Right below, a small TOI (Time-of-Interest) summary box (mock)
        with st.expander("TOI / Quick levels (demo)"):
            # Simple mock levels computed from price series
            current = prices[-1]
            high = max(prices)
            low = min(prices)
            range_pct = ((high - low) / (low + 1e-9)) * 100
            st.write(f"Current: **{current:,}**")
            st.write(f"High: {high:,}  Low: {low:,}")
            st.write(f"Range (high-low): {range_pct:.2f}%")
            # Mock predicted early move band
            st.markdown("**Early move band (demo):**")
            st.write(f"{round(current - (range_pct/10),1):,}  →  {round(current + (range_pct/10),1):,}")

    except Exception as e:
        st.error("panel_candles failed to render: " + str(e))
        # provide minimal fallback UI so dashboard doesn't break
        st.write("Fallback: simple price text")
        try:
            if data and "last_price" in data:
                st.write("Price:", data["last_price"])
        except Exception:
            pass

# Allow this module to be imported and also called directly for quick dev testing
if __name__ == "__main__":
    # Quick local dev test (prints nothing in Streamlit context)
    times, prices, vols = _make_mock_series()
    fig = _plot_price_volume(times, prices, vols)
    fig.savefig("panel_candles_demo.png")
    print("Wrote panel_candles_demo.png (local test).")
