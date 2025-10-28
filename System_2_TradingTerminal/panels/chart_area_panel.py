# ==============================================================
# 📄 FILE: Streamlit_TradingSystems/System_2_TradingTerminal/panels/chart_area_panel.py
# ==============================================================
# VERSION: v7.5.0 — Stage 3 (Edge-to-Edge Chart Grid Lock)
# PURPOSE:
# Central 4-chart grid + 2 watchlists — internal labels only, no gaps
# ==============================================================

import streamlit as st

# ==============================================================
# 🎨 STYLE — EDGE-TO-EDGE DARK GRID
# ==============================================================
def _inject_chart_css():
    st.markdown("""
    <style>
    .chart-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        grid-template-rows: repeat(6, 1fr);
        gap: 0;
        width: 100vw;
        height: calc(100vh - 138px); /* below top 3 bars */
        background: #0d1117;
        overflow: hidden;
    }
    .chart-cell {
        border: 1px solid #222;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
        font-size: 14px;
        color: #9aa0a6;
        user-select: none;
    }
    .chart-cell:hover {
        background: #161b22;
        color: #fff;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================
# ⚙️ COMPONENT
# ==============================================================
def render_chart_area():
    _inject_chart_css()

    grid_html = """
    <div class="chart-grid">
<!-- Row 2 -->
<div class="chart-cell" style="grid-column: 1 / span 2; grid-row: 2;">📈 Chart 1</div>
<div class="chart-cell" style="grid-column: 3 / span 2; grid-row: 2;">📈 Chart 2</div>
<div class="chart-cell" style="grid-column: 5 / span 2; grid-row: 2;">📋 Watchlist 1</div>

<!-- Row 3 -->
<div class="chart-cell" style="grid-column: 1 / span 2; grid-row: 3;">📊 Chart 3</div>
<div class="chart-cell" style="grid-column: 3 / span 2; grid-row: 3;">📊 Chart 4</div>
<div class="chart-cell" style="grid-column: 5 / span 2; grid-row: 3;">📋 Watchlist 2</div>
    </div>
    """
    st.markdown(grid_html, unsafe_allow_html=True)

# ==============================================================
# ✅ END OF FILE
# ==============================================================

