# ==============================================================
# 📄 FILE: Streamlit_TradingSystems/shared/layout_editor.py
# ==============================================================
# VERSION: v7.1.1 — EditorBridge (Live Layout Editor)
# PURPOSE:
#   In-dashboard Layout Editor to modify row, col, row_span, col_span
#   for each panel inside the 6×6 SmoothSnap grid.
# ==============================================================

import streamlit as st

# ==============================================================
# 🧠 INIT
# ==============================================================

if "layout_state" not in st.session_state:
    st.session_state["layout_state"] = {}

if "layout_tokens" not in st.session_state:
    st.session_state["layout_tokens"] = {}

# ==============================================================
# 🔧 HELPER
# ==============================================================

def update_panel_layout(pid: str, row: int, col: int, row_span: int, col_span: int):
    """Update layout_state for the given panel."""
    st.session_state["layout_state"][pid] = {
        "row": row,
        "col": col,
        "row_span": row_span,
        "col_span": col_span,
    }

# ==============================================================
# 🧩 RENDER LAYOUT EDITOR SIDEBAR
# ==============================================================

def render_layout_editor(panels: list):
    """
    panels: list of panel IDs, e.g. ["chart1", "chart2", "watch1"]
    Provides live grid editing controls for each panel.
    """
    st.sidebar.markdown("### 🧭 Layout Editor (6×6 Grid)")

    for pid in panels:
        st.sidebar.markdown(f"**{pid.upper()}**")
        col1, col2 = st.sidebar.columns(2)

        # current values
        cur = st.session_state["layout_state"].get(
            pid, {"row": 1, "col": 1, "row_span": 1, "col_span": 1}
        )

        with col1:
            row = st.number_input(f"{pid} row", 1, 6, cur["row"], key=f"{pid}_row")
            row_span = st.number_input(
                f"{pid} row span", 1, 6, cur["row_span"], key=f"{pid}_rowspan"
            )
        with col2:
            col = st.number_input(f"{pid} col", 1, 6, cur["col"], key=f"{pid}_col")
            col_span = st.number_input(
                f"{pid} col span", 1, 6, cur["col_span"], key=f"{pid}_colspan"
            )

        if st.button(f"💾 Save {pid}", key=f"{pid}_save", use_container_width=True):
            update_panel_layout(pid, row, col, row_span, col_span)
            st.toast(f"✅ {pid} layout updated", icon="🧩")

    st.sidebar.divider()
    if st.sidebar.button("♻️ Reset All Layouts", use_container_width=True):
        st.session_state["layout_state"].clear()
        st.toast("🔄 All layouts reset")

    st.sidebar.markdown("---")
    st.sidebar.info("Changes apply instantly to the active grid session.")

# ==============================================================
# ✅ TEST MODE
# ==============================================================

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Layout Editor Test")
    st.write("🧩 Layout Editor Test Page")
    panels = ["chart1", "chart2", "chart3", "watch1", "watch2"]
    render_layout_editor(panels)
    st.json(st.session_state["layout_state"])
