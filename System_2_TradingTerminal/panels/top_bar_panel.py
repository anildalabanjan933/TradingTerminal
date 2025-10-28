# ==============================================================
# 🎨 TRADING TERMINAL — TOP BAR + TAB ROW (Stage 2 Final Polish)
# File: panels/top_bar_panel.py
# ==============================================================

import streamlit as st

# ==============================================================
# 🧱  RENDER FUNCTION
# ==============================================================

def render_top_bar():
    """Top bar + tab row with hover animation, smooth underline, and alignment polish."""

    # ---- Fixed constants ----
    BAR_HEIGHT = 44
    PAD_X = 16
    FONT = "Montserrat, sans-serif"
    FONT_SIZE = "13px"
    ACCENT = "#00C2A8"
    BG = "#0E1117"
    TEXT = "#FFFFFF"

    # ==========================================================
    # Embedded CSS
    # ==========================================================
    st.markdown(
        f"""
        <style>
            .tt-bar, .tt-tabs {{
                height:{BAR_HEIGHT}px;
                font-family:{FONT};
                font-size:{FONT_SIZE};
                color:{TEXT};
                background:{BG};
            }}

            /* -------- TOP BAR -------- */
            .tt-bar {{
                position:fixed;
                top:0;left:0;right:0;
                display:flex;
                justify-content:space-between;
                align-items:center;
                padding:0 {PAD_X}px;
                border-bottom:1px solid rgba(255,255,255,0.06);
                z-index:1000;
            }}
            .tt-title {{
                font-weight:600;
                color:{ACCENT};
                letter-spacing:0.3px;
            }}
            .tt-right {{
                display:flex;
                align-items:center;
                gap:14px;
            }}
            .tt-pill {{
                padding:3px 10px;
                border-radius:12px;
                background:rgba(255,255,255,0.08);
                font-weight:500;
                color:#AAAAAA;
            }}

            /* -------- TAB ROW -------- */
            .tt-tabs {{
                position:fixed;
                top:{BAR_HEIGHT}px;
                left:0;right:0;
                display:flex;
                justify-content:center;
                align-items:center;
                gap:2px;
                border-bottom:1px solid rgba(255,255,255,0.06);
                z-index:999;
                overflow:hidden;
            }}
            .tt-tab {{
                position:relative;
                padding:0 22px;
                height:{BAR_HEIGHT}px;
                display:flex;
                align-items:center;
                justify-content:center;
                cursor:pointer;
                transition:color 0.25s ease;
                color:{TEXT};
            }}
            .tt-tab::after {{
                content:'';
                position:absolute;
                bottom:0;left:50%;
                width:0%;height:2px;
                background:{ACCENT};
                transition:all 0.25s ease;
                transform:translateX(-50%);
            }}
            .tt-tab:hover {{
                background:rgba(0,194,168,0.08);
            }}
            .tt-tab:hover::after {{
                width:60%;
            }}
            .tt-tab.active {{
                color:{ACCENT};
                font-weight:600;
            }}
            .tt-tab.active::after {{
                width:100%;
            }}
        </style>

        <!-- ================= TOP BAR ================= -->
        <div class="tt-bar">
            <div class="tt-title">Trading Terminal</div>
            <div class="tt-right">
                <span style="color:#00E676;">NIFTY +0.84%</span>
                <span>RSI 1D 45 | 1H 55 | 15m 48 | 5m 51 | 3m 60</span>
                <span style="color:#00E676;">DOW +0.62%</span>
                <span style="color:#00E676;">SGX +0.45%</span>
                <span style="color:#FF5252;">VIX −1.12%</span>
                <span class="tt-pill">Paper Mode</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Spacer below top bar
    st.markdown(f"<div style='height:{BAR_HEIGHT}px'></div>", unsafe_allow_html=True)

    # ==========================================================
    # TAB ROW
    # ==========================================================
    tabs = [
        "Intraday",
        "Sector Rotation",
        "Wealth",
        "Journal",
        "Backtest",
        "HA Terminal",
        "Scanner",
    ]
    active_tab = st.session_state.get("active_tab", "Intraday")

    tab_html = "<div class='tt-tabs'>"
    for t in tabs:
        cls = "tt-tab active" if t == active_tab else "tt-tab"
        tab_html += f"<div class='{cls}'>{t}</div>"
    tab_html += "</div>"

    st.markdown(tab_html, unsafe_allow_html=True)

    # Spacer below both bars
    st.markdown(f"<div style='height:{BAR_HEIGHT}px'></div>", unsafe_allow_html=True)


# ==============================================================
# 🚀 ENTRY POINT
# ==============================================================

def render():
    try:
        render_top_bar()
    except Exception as e:
        st.error(f"⚠️ Top bar render error: {e}")

# ==============================================================
# ✅ END OF FILE
# ==============================================================
