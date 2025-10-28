# ==============================================================
# 📄 FILE: Streamlit_TradingSystems/shared/panel_manager.py
# ==============================================================
# VERSION: v7.1.2 — PanelControl (Hide / Resize / Reset)
# PURPOSE:
#   Provides per-panel control buttons integrated with SmoothSnap grid.
#   Features:
#     • Hide / Show panel
#     • Reset size / position to defaults
#     • Soft highlight when active
# ==============================================================

import streamlit as st

# ==============================================================
# 🧠 INIT
# ==============================================================

if "layout_state" not in st.session_state:
    st.session_state["layout_state"] = {}
if "hidden_panels" not in st.session_state:
    st.session_state["hidden_panels"] = set()

# ==============================================================
# 🧩 PANEL CONTROL HANDLERS
# ==============================================================

def toggle_visibility(panel_id: str):
    """Toggle visibility of a panel."""
    hidden = st.session_state.get("hidden_panels", set())
    if panel_id in hidden:
        hidden.remove(panel_id)
    else:
        hidden.add(panel_id)
    st.session_state["hidden_panels"] = hidden


def reset_panel(panel_id: str):
    """Reset a panel’s layout to default."""
    defaults = {"row": 1, "col": 1, "row_span": 2, "col_span": 2}
    st.session_state["layout_state"][panel_id] = defaults
    if panel_id in st.session_state.get("hidden_panels", set()):
        st.session_state["hidden_panels"].remove(panel_id)
    st.toast(f"♻️ {panel_id} reset to default")


def resize_panel(panel_id: str, scale: str):
    """Resize panel relative to current size (small / large)."""
    cur = st.session_state["layout_state"].get(
        panel_id, {"row": 1, "col": 1, "row_span": 2, "col_span": 2}
    )
    factor = 1 if scale == "reset" else (0.8 if scale == "small" else 1.2)
    cur["row_span"] = max(1, min(6, int(cur["row_span"] * factor)))
    cur["col_span"] = max(1, min(6, int(cur["col_span"] * factor)))
    st.session_state["layout_state"][panel_id] = cur
    st.toast(f"🔧 {panel_id} resized to {scale}")


# ==============================================================
# 🎨 RENDER PANEL CONTROL BAR
# ==============================================================

def render_panel_controls(panel_id: str):
    """Render compact control buttons for one panel."""
    col1, col2, col3, col4 = st.columns([2, 2, 2, 6])
    with col1:
        if st.button("👁 Hide", key=f"{panel_id}_hide", use_container_width=True):
            toggle_visibility(panel_id)
    with col2:
        if st.button("↔ Resize", key=f"{panel_id}_resize", use_container_width=True):
            resize_panel(panel_id, "large")
    with col3:
        if st.button("♻ Reset", key=f"{panel_id}_reset", use_container_width=True):
            reset_panel(panel_id)


# ==============================================================
# 🚀 MAIN ENTRY
# ==============================================================

def render_all_panel_controls(panels: list):
    """
    Render controls for all panels currently visible.
    panels: list of panel IDs, e.g. ["chart1", "chart2", "watch1"]
    """
    st.markdown("### 🎛 Panel Control Center")

    for pid in panels:
        hidden = pid in st.session_state.get("hidden_panels", set())
        st.markdown(f"#### {pid.upper()} {'(Hidden)' if hidden else ''}")
        render_panel_controls(pid)

    if st.button("🧹 Reset All Panels"):
        st.session_state["layout_state"].clear()
        st.session_state["hidden_panels"] = set()
        st.toast("✅ All panels restored")


# ==============================================================
# ✅ TEST MODE
# ==============================================================

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Panel Manager Test")
    st.write("🎛 Panel Manager UI Test")
    panels = ["chart1", "chart2", "chart3", "watch1", "watch2"]
    render_all_panel_controls(panels)
    st.json(st.session_state)
