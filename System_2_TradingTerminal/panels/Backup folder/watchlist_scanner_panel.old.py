"""
Phase 3.9.1 — Watchlist ↔ Sync Manager Link
============================================
Adds full integration between Watchlist + Sync Manager:
• Selecting a stock instantly updates the global symbol.
• Charts and Top Bar auto-refresh via Sync Manager state.
• Mock mode supported for offline smoke testing.
• Scanner window kept as floating popup (unchanged visually).

"""

from __future__ import annotations
import streamlit as st
import datetime
import random
import os
import importlib.util
from typing import List, Dict, Any

# ------------------------------------------------------------
#  PATHS + SYNC MANAGER IMPORT
# ------------------------------------------------------------
SHARED_DIR = os.path.join("Streamlit_TradingSystems", "shared")
SYNC_PATH = os.path.join(SHARED_DIR, "ui_sync_manager.py")

def get_sync_manager():
    if not os.path.exists(SYNC_PATH):
        return None
    try:
        spec = importlib.util.spec_from_file_location("ui_sync_manager", SYNC_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore
        return module
    except Exception as e:
        st.error(f"[Watchlist] Failed to import Sync Manager: {e}")
        return None


# ------------------------------------------------------------
#  MOCK DATA GENERATOR
# ------------------------------------------------------------
def mock_watchlist(symbols: List[str]) -> List[Dict[str, Any]]:
    rows = []
    for s in symbols:
        pct = round(random.uniform(-2, 2), 2)
        bias = "🟢 Bull" if pct > 0 else "🔴 Bear"
        rows.append({
            "Symbol": s,
            "LTP": round(random.uniform(100, 2500), 2),
            "%Chg": pct,
            "Bias": bias,
            "RSI(15m)": random.randint(25, 75)
        })
    return rows


# ------------------------------------------------------------
#  WATCHLIST TABLE RENDER
# ------------------------------------------------------------
def render_watchlist(title: str, symbols: List[str], sync: Any | None = None):
    st.markdown(
        """
        <style>
        .watchlist-card{background:rgba(28,28,30,0.85);border-radius:12px;
        padding:8px 10px;margin-bottom:10px;color:#e6eef8;
        font-family:'Inter',sans-serif;box-shadow:0 0 8px rgba(0,0,0,0.25);}
        .watchlist-title{font-weight:700;font-size:14px;margin-bottom:4px;
        display:flex;justify-content:space-between;}
        table.wl{width:100%;border-collapse:collapse;font-size:13px;}
        table.wl td,table.wl th{padding:4px 6px;border-bottom:1px solid rgba(255,255,255,0.05);}
        tr:hover{background:rgba(255,255,255,0.06);}
        </style>
        """,
        unsafe_allow_html=True,
    )

    data = mock_watchlist(symbols)
    st.markdown(f"<div class='watchlist-card'><div class='watchlist-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown("<table class='wl'><tr><th>Symbol</th><th>LTP</th><th>%Chg</th><th>Bias</th><th>RSI(15m)</th><th>→</th></tr>", unsafe_allow_html=True)

    for row in data:
        color = "#00d26a" if row["%Chg"] > 0 else "#ff4d4d"
        cols = st.columns([3, 2, 2, 2, 2, 1])
        with cols[0]: st.write(row["Symbol"])
        with cols[1]: st.write(row["LTP"])
        with cols[2]: st.markdown(f"<span style='color:{color}'>{row['%Chg']}%</span>", unsafe_allow_html=True)
        with cols[3]: st.write(row["Bias"])
        with cols[4]: st.write(row["RSI(15m)"])
        with cols[5]:
            if st.button("📈", key=f"{title}_{row['Symbol']}"):
                if sync:
                    try:
                        sync.update_symbol(row["Symbol"])
                        st.toast(f"Loaded {row['Symbol']} → Charts + Top Bar updated", icon="📊")
                    except Exception as e:
                        st.error(f"Sync update failed: {e}")
                else:
                    st.info(f"(Mock) Would load {row['Symbol']}")

    st.markdown("</table></div>", unsafe_allow_html=True)


# ------------------------------------------------------------
#  SCANNER WINDOW
# ------------------------------------------------------------
def render_scanner_window():
    st.markdown(
        """
        <style>
        .scanner{position:fixed;top:80px;right:40px;width:360px;background:rgba(28,28,30,0.95);
        border-radius:12px;padding:10px 12px;box-shadow:0 0 12px rgba(0,0,0,0.5);
        z-index:9999;color:#e6eef8;font-family:'Inter',sans-serif;}
        .scanner h4{margin:0;font-size:14px;}
        </style>
        <div class='scanner'>
            <h4>🔍 Scanner Manager</h4><hr style="border:1px solid rgba(255,255,255,0.1)">
            <ul style="font-size:13px;margin-top:-4px;">
                <li>RSI Momentum ✅</li>
                <li>Breakout Stocks ✅</li>
                <li>Volume Spike ✅</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
#  MAIN ENTRY
# ------------------------------------------------------------
def render():
    st.subheader("📋 Watchlist ↔ Sync Manager Bridge (Phase 3.9.1)")
    sync = get_sync_manager()
    if sync is None:
        st.info("Sync Manager not found → running in mock mode.")
    col1, col2 = st.columns([3, 2], gap="small")

    with col1:
        render_watchlist("📈 Intraday Watchlist", ["TCS","INFY","RELIANCE","HDFCBANK","ICICIBANK"], sync)
    with col2:
        render_watchlist("💼 Swing Watchlist", ["HDFC","LT","SBIN","ITC","TATASTEEL"], sync)

    if st.toggle("📊 Open Scanner Window", value=False):
        render_scanner_window()

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(f"Last Updated: {datetime.datetime.now().strftime('%H:%M:%S')} | Phase 3.9.1 Integration Active")


# ------------------------------------------------------------
#  STANDALONE TEST
# ------------------------------------------------------------
if __name__ == "__main__":
    st.set_page_config(page_title="Watchlist ↔ Sync Manager Bridge", layout="wide")
    render()
