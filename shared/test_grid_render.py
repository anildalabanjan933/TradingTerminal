# ==============================================================
# 📄 File: Streamlit_TradingSystems/shared/test_grid_render.py
# 🔹 Purpose: Verify dashboard_grid_engine grid layout works visually
# ==============================================================

import streamlit as st
from Streamlit_TradingSystems.shared import layout_tokens, dashboard_grid_engine

st.set_page_config(page_title="Grid Engine Test", layout="wide")

st.title("🧩 Grid Engine Smoke Test")
st.write("If you see 6×6 colored boxes aligned neatly on one screen → Grid Engine works ✅")

# Generate dummy layout tokens
dummy_layout = {
    f"Box{i}": {
        "row": ((i - 1) // 6) + 1,
        "col": ((i - 1) % 6) + 1,
        "row_span": 1,
        "col_span": 1,
    }
    for i in range(1, 37)
}
layout_tokens.LAYOUT = dummy_layout

# Dummy registry to render colored boxes
def dummy_registry():
    import random
    colors = ["#007BFF", "#28A745", "#FFC107", "#DC3545", "#17A2B8", "#6F42C1"]
    return {f"Box{i}": (lambda c=color: st.markdown(
        f"<div style='background:{c};width:100%;height:100%;border-radius:6px;'></div>",
        unsafe_allow_html=True
    )) for i, color in enumerate(colors * 6, start=1)}

dashboard_grid_engine.get_panel_registry = dummy_registry

# Render grid
dashboard_grid_engine.render_layout()

st.markdown("---")
st.caption("✅ If all 36 boxes fit in a clean 6×6 grid, layout engine works correctly.")
