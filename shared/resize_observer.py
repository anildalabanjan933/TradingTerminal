# ==============================================================
# 📄 FILE: shared/resize_observer.py
# ==============================================================
# PURPOSE:
#   TradingView-style resize logic with smooth snapping.
#   Works in tandem with drag_engine.py and grid_alignment.py
# ==============================================================

import streamlit as st
import json
import time

# --------------------------------------------------------------
# ⚙️ GRID SETTINGS
# --------------------------------------------------------------
GRID_ROWS = 6
GRID_COLS = 6
MIN_CELL_SIZE = 1 / 6
FPS_LIMIT = 60

# --------------------------------------------------------------
# 🧠 INIT
# --------------------------------------------------------------
if "resize_state" not in st.session_state:
    st.session_state.resize_state = {
        "active_panel": None,
        "resizing": False,
        "start_size": (0.0, 0.0),
        "current_size": (0.0, 0.0),
        "grid_target": None,
    }

# --------------------------------------------------------------
# 🎯 HELPERS
# --------------------------------------------------------------
def _throttle_frame(last_time: float, fps_limit: int = FPS_LIMIT) -> bool:
    now = time.time()
    return now - last_time >= 1.0 / fps_limit


def _emit_size_update(panel_id: str, new_size: dict):
    layout_state = st.session_state.get("layout_state", {})
    if panel_id not in layout_state:
        layout_state[panel_id] = {}
    layout_state[panel_id].update(new_size)
    st.session_state["layout_state"] = layout_state


def _snap_dim_to_grid(w_norm: float, h_norm: float):
    w_snap = round(w_norm * GRID_COLS) / GRID_COLS
    h_snap = round(h_norm * GRID_ROWS) / GRID_ROWS
    w_snap = max(MIN_CELL_SIZE, w_snap)
    h_snap = max(MIN_CELL_SIZE, h_snap)
    return w_snap, h_snap


# --------------------------------------------------------------
# 🖱️ EVENT HANDLERS
# --------------------------------------------------------------
def start_resize(panel_id: str, start_w: float, start_h: float):
    st.session_state.resize_state.update({
        "active_panel": panel_id,
        "resizing": True,
        "start_size": (start_w, start_h),
        "current_size": (start_w, start_h),
    })


def update_resize(panel_id: str, delta_w: float, delta_h: float):
    state = st.session_state.resize_state
    if not state["resizing"] or state["active_panel"] != panel_id:
        return

    last_update = state.get("last_frame_time", 0.0)
    if not _throttle_frame(last_update):
        return
    state["last_frame_time"] = time.time()

    w0, h0 = state["start_size"]
    state["current_size"] = (max(0.05, w0 + delta_w), max(0.05, h0 + delta_h))
    st.session_state.resize_state = state


def end_resize(panel_id: str):
    state = st.session_state.resize_state
    if state["active_panel"] != panel_id:
        return

    w_norm, h_norm = state["current_size"]
    w_snap, h_snap = _snap_dim_to_grid(w_norm, h_norm)
    _emit_size_update(panel_id, {
        "width": w_snap,
        "height": h_snap,
        "row_span": max(1, int(h_snap * GRID_ROWS)),
        "col_span": max(1, int(w_snap * GRID_COLS)),
    })

    st.session_state.resize_state.update({
        "active_panel": None,
        "resizing": False,
        "grid_target": (w_snap, h_snap),
        "current_size": (w_snap, h_snap),
    })


# --------------------------------------------------------------
# 🧩 FRONTEND PAYLOAD
# --------------------------------------------------------------
def get_frontend_payload():
    """Expose current resize state to React bridge."""
    return json.dumps(st.session_state.resize_state)


# --------------------------------------------------------------
# 🧪 DEBUG / TEST VIEW
# --------------------------------------------------------------
def _demo_debug_info():
    st.markdown("### 🧩 Resize Observer Debug")
    st.json(st.session_state.resize_state)
    if "layout_state" in st.session_state:
        st.markdown("**Layout State:**")
        st.json(st.session_state.layout_state)


if __name__ == "__main__":
    st.title("Resize Engine Demo")
    _demo_debug_info()
