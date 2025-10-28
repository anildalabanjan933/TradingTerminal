# ==============================================================================
# 📈 TRADING TERMINAL — CHART AREA + OVERLAY PANELS (Stage 4 Final Build)
# File: panels/chart_layout_panel.py
# ==============================================================================
# Purpose:
# - Create core 1 / 2 / 4 chart layout area
# - Integrate floating overlay panels (Indicators / Tools / Alerts / Settings)
# - All overlays appear *inside* chart area without pushing layout
# ==============================================================================

import streamlit as st

def render_chart_area():
    """Main chart workspace with 4-chart grid + overlay menus."""

    # --- UI constants ---
    FONT = "Montserrat, sans-serif"
    BG = "#0E1117"
    BAR_HEIGHT = 44
    ACCENT = "#00C2A8"

    st.markdown(
        f"""
        <style>
            /* ================== CHART GRID ================== */
            .chart-container {{
                position: relative;
                top:{BAR_HEIGHT*3}px; /* below 3 fixed bars */
                background:{BG};
                display:grid;
                grid-template-columns: 1fr 1fr;
                grid-template-rows: 1fr 1fr;
                gap:6px;
                height: calc(100vh - {BAR_HEIGHT*3 + 60}px);
                padding:6px;
                box-sizing:border-box;
            }}
            .chart-box {{
                background:#111317;
                border:1px solid rgba(255,255,255,0.08);
                border-radius:6px;
                display:flex;
                align-items:center;
                justify-content:center;
                color:#888;
                font-family:{FONT};
                font-size:14px;
                position:relative;
                overflow:hidden;
            }}
            .chart-box:hover {{
                border-color:{ACCENT};
            }}

            /* ================== OVERLAYS ================== */
            .overlay {{
                position:absolute;
                top:50px;
                left:50%;
                transform:translateX(-50%);
                width:420px;
                background:#1a1c20;
                border:1px solid rgba(255,255,255,0.12);
                border-radius:8px;
                padding:14px 16px;
                color:white;
                font-family:{FONT};
                z-index:9999;
                box-shadow:0 6px 20px rgba(0,0,0,0.4);
            }}
            .overlay h4 {{
                margin-top:0;margin-bottom:8px;
                color:{ACCENT};
                font-weight:600;
            }}
            .overlay button {{
                margin:3px;
                padding:4px 8px;
                background:rgba(255,255,255,0.08);
                border:none;
                border-radius:4px;
                cursor:pointer;
                color:white;
            }}
            .overlay button:hover {{
                background:rgba(0,194,168,0.15);
                color:{ACCENT};
            }}
            .overlay-close {{
                position:absolute;
                top:6px;right:8px;
                background:none;
                color:#aaa;
                border:none;
                font-size:16px;
                cursor:pointer;
            }}
            .overlay-close:hover {{ color:{ACCENT}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---- Session toggles ----
    if "show_overlay" not in st.session_state:
        st.session_state.show_overlay = None

    # ---- Toolbar event bridge (placeholder) ----
    # In final version, each button from chart_toolbar toggles these keys
    query = st.experimental_get_query_params()
    overlay = query.get("overlay", [None])[0]
    if overlay:
        st.session_state.show_overlay = overlay

    # ---- Chart grid ----
    st.markdown(
        """
        <div class="chart-container">
            <div class="chart-box" id="chart1">Chart 1</div>
            <div class="chart-box" id="chart2">Chart 2</div>
            <div class="chart-box" id="chart3">Chart 3</div>
            <div class="chart-box" id="chart4">Chart 4</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Overlays (pop-ups) ----
    overlay_html = ""

    if st.session_state.show_overlay == "indicators":
        overlay_html = f"""
        <div class="overlay">
            <button class="overlay-close" onclick="window.parent.postMessage({{type:'close_overlay'}},'*')">✖</button>
            <h4>📈 Indicators</h4>
            <button>SMA 10</button><button>SMA 21</button><button>SMA 50</button><button>SMA 200</button><br>
            <button>RSI</button><button>MACD</button><button>PSAR</button><button>ADX</button><button>VWAP</button>
        </div>
        """

    elif st.session_state.show_overlay == "tools":
        overlay_html = f"""
        <div class="overlay">
            <button class="overlay-close" onclick="window.parent.postMessage({{type:'close_overlay'}},'*')">✖</button>
            <h4>✏ Drawing Tools</h4>
            <button>Trend Line</button><button>H-Line</button><button>V-Line</button><br>
            <button>Fib Retrace</button><button>Channel</button><button>Box</button><br>
            <button>Text</button><button>Measure</button><button>Magnet ON/OFF</button>
        </div>
        """

    elif st.session_state.show_overlay == "alerts":
        overlay_html = f"""
        <div class="overlay">
            <button class="overlay-close" onclick="window.parent.postMessage({{type:'close_overlay'}},'*')">✖</button>
            <h4>🔔 Alerts</h4>
            <label>Condition &gt;</label>
            <select style='width:100%;margin-bottom:6px;'>
                <option>Price Above</option>
                <option>Price Below</option>
                <option>Cross Over</option>
            </select>
            <input type='text' placeholder='Value / Indicator' style='width:100%;margin-bottom:6px;padding:4px;'>
            <button>Create Alert</button>
        </div>
        """

    elif st.session_state.show_overlay == "settings":
        overlay_html = f"""
        <div class="overlay">
            <button class="overlay-close" onclick="window.parent.postMessage({{type:'close_overlay'}},'*')">✖</button>
            <h4>⚙ Chart Settings</h4>
            <strong>Global</strong><br>
            <button>Grid ON/OFF</button><button>Watermark</button><button>Dark/Light</button><br><br>
            <strong>Candle</strong><br>
            <button>Wick ON/OFF</button><button>Body Opacity</button><button>Volume Overlay</button><br><br>
            <strong>Heikin Ashi</strong><br>
            <button>Wick ON/OFF</button><button>Smoothing</button><button>Color Scheme</button><br><br>
            <strong>Line / Area</strong><br>
            <button>Thickness</button><button>Opacity</button><button>Gradient Fill</button><br><br>
            <strong>Point & Figure</strong><br>
            <button>Box Size</button><button>Reversal</button><button>Color Rule</button>
        </div>
        """

    if overlay_html:
        st.markdown(overlay_html, unsafe_allow_html=True)

    # ---- JS Bridge for closing overlays ----
    st.markdown(
        """
        <script>
        window.addEventListener("message", (event) => {
            if (event.data.type === "close_overlay") {
                window.parent.postMessage({type:'clear_overlay'}, '*');
            }
        });
        </script>
        """,
        unsafe_allow_html=True,
    )

# ==============================================================================
# 🚀 ENTRY POINT
# ==============================================================================
def render():
    try:
        render_chart_area()
    except Exception as e:
        st.error(f"⚠️ Chart Area Render Error → {e}")

# ==============================================================================
# ✅ END OF FILE
# ==============================================================================
