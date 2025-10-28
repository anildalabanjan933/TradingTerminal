# ============================================================
# 🧭 chart_toolbar.old.py — Phase 5.7.0  (Step 3A Final Toolbar Locked)
# ============================================================

import streamlit as st

# ============================================================
# 🧩 Render Chart Toolbar  (TradingView-style unified bar)
# ============================================================
def render():
    st.markdown(
        """
        <style>
        /* --- fixed position below Tab Row --- */
        .chart-toolbar {
            position: fixed;
            top: 68px;                 /* directly under Tab Row 34 + 34 px */
            left: 0;
            width: 100%;
            height: 38px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            background: #ffffff;
            border-bottom: 1px solid #e5e7eb;
            padding: 0 10px;
            z-index: 9997;
            font-family: 'Inter', sans-serif;
            font-size: 12.5px;
        }
        .toolbar-group {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .toolbar-btn {
            background: #f1f5f9;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            padding: 2px 8px;
            cursor: pointer;
            font-weight: 500;
            transition: 0.15s;
        }
        .toolbar-btn:hover {background:#e2e8f0;}
        .expander {
            position: absolute;
            top: 42px;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 6px 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            z-index: 9996;
            font-size: 12px;
            display: none;
        }
        .expander.show {display:block;}
        .buy-btn {
            background:#16a34a; color:#fff;
            border:none; padding:4px 10px; border-radius:6px;
            font-weight:600; cursor:pointer;
        }
        .sell-btn {
            background:#dc2626; color:#fff;
            border:none; padding:4px 10px; border-radius:6px;
            font-weight:600; cursor:pointer;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------
    # Layout groups
    # ------------------------------------------------------------
    left, center, right = st.columns([2.4, 5, 2.6])

    # ---------------- Left group ----------------
    with left:
        st.markdown(
            """
            <div class="toolbar-group">
                <input type="text" value="NIFTY" style="
                    width:80px; padding:2px 4px; border:1px solid #d1d5db;
                    border-radius:6px; font-size:12px; text-align:center;">
                <span title="Refresh"><b>🔄</b></span>
                <select style="padding:2px 4px; border-radius:6px;">
                    <option>1m</option><option>3m</option><option>5m</option>
                    <option>10m</option><option>15m</option><option>30m</option>
                    <option>1h</option><option>2h</option><option>4h</option>
                    <option>1D</option><option>1W</option><option>1M</option>
                </select>
                <select style="padding:2px 4px; border-radius:6px;">
                    <option>Candle</option><option>Heikin Ashi</option>
                    <option>Point & Figure</option><option>Line</option><option>Area</option>
                </select>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------------- Center group ----------------
    with center:
        st.markdown(
            """
            <div class="toolbar-group">
                <button class="toolbar-btn" title="Indicators">📊 Indicators ⭐</button>
                <button class="toolbar-btn" title="Drawing Tools">✏️ Draw</button>
                <button class="toolbar-btn" title="Chart Settings">⚙️ Settings</button>
                <button class="toolbar-btn" title="Alerts">🔔 Alerts</button>
                <button class="toolbar-btn" title="Layout Selector">🧩 Layout</button>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------------- Right group ----------------
    with right:
        st.markdown(
            """
            <div class="toolbar-group" style="justify-content:flex-end;">
                <button class="buy-btn" title="Buy Order">BUY</button>
                <button class="sell-btn" title="Sell Order">SELL</button>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ------------------------------------------------------------
    # Spacer to prevent chart overlap
    # ------------------------------------------------------------
    st.markdown("<div style='height:38px;'></div>", unsafe_allow_html=True)

# ============================================================
# 🔍 Smoke Test
# ============================================================
if __name__ == "__main__":
    st.set_page_config(page_title="Chart Toolbar Test", layout="wide")
    render()
    st.write("✅ Step 3A — Chart Toolbar rendered successfully and locked.")
