# ==============================================================
# 📄 FILE: shared/drag_engine.py
# ==============================================================
# PURPOSE:
#   Implements TradingView-style drag motion for dashboard panels.
#   Works with resize_observer.py + grid_alignment.py + dashboard_grid_engine.py
#   to create smooth, GPU-accelerated drag + snap behavior.
# ==============================================================

from streamlit.runtime.scriptrunner import get_script_run_ctx
import streamlit as st
import json
import time

# --------------------------------------------------------------
# 🔧 CONFIGURATION
# --------------------------------------------------------------
GRID_ROWS = 6
GRID_COLS = 6
GRID_CELL_SIZE = 1 / GRID_COLS    # normalized fraction (0-1)
ANIMATION_EASE_MS = 180
FPS_LIMIT = 60

# --------------------------------------------------------------
# 🧠 SESSION INIT
# --------------------------------------------------------------
if "drag_state" not in st.session_state:
    st.session_state.drag_state = {
        "active_panel": None,
        "dragging": False,
        "start_pos": (0, 0),
        "current_pos": (0, 0),
        "grid_target": None,
    }

# --------------------------------------------------------------
# 🎯 HELPER FUNCTIONS
# --------------------------------------------------------------
def _throttle_frame(last_time: float, fps_limit: int = FPS_LIMIT) -> bool:
    """Return True if we can render a new frame (limits CPU)."""
    now = time.time()
    return now - last_time >= 1.0 / fps_limit


def _emit_layout_update(panel_id: str, new_layout: dict):
    """Update Streamlit session layout_state after drop."""
    layout_state = st.session_state.get("layout_state", {})
    layout_state[panel_id] = new_layout
    st.session_state["layout_state"] = layout_state


def _snap_to_grid(x_norm: float, y_norm: float, w_norm: float, h_norm: float):
    """Snap fractional coordinates to nearest 1/6 grid cell."""
    snap_x = round(x_norm * GRID_COLS) / GRID_COLS
    snap_y = round(y_norm * GRID_ROWS) / GRID_ROWS
    snap_w = round(w_norm * GRID_COLS) / GRID_COLS
    snap_h = round(h_norm * GRID_ROWS) / GRID_ROWS
    return snap_x, snap_y, snap_w, snap_h


# --------------------------------------------------------------
# 🖱️ EVENT HANDLERS (CALLED FROM FRONTEND)
# --------------------------------------------------------------
def start_drag(panel_id: str, start_x: float, start_y: float):
    """Begin dragging a panel."""
    st.session_state.drag_state.update({
        "active_panel": panel_id,
        "dragging": True,
        "start_pos": (start_x, start_y),
        "current_pos": (start_x, start_y)
    })


def update_drag(panel_id: str, delta_x: float, delta_y: float):
    """Update live position while dragging."""
    state = st.session_state.drag_state
    if not state["dragging"] or state["active_panel"] != panel_id:
        return

    last_update = state.get("last_frame_time", 0.0)
    if not _throttle_frame(last_update):
        return
    state["last_frame_time"] = time.time()

    cur_x, cur_y = state["start_pos"]
    new_x = cur_x + delta_x
    new_y = cur_y + delta_y
    state["current_pos"] = (new_x, new_y)

    # Visual transform (frontend handled via JS)
    st.session_state.drag_state = state


def end_drag(panel_id: str, w_norm: float, h_norm: float):
    """End drag and snap to grid."""
    state = st.session_state.drag_state
    if state["active_panel"] != panel_id:
        return

    x_norm, y_norm = state["current_pos"]
    snap_x, snap_y, snap_w, snap_h = _snap_to_grid(x_norm, y_norm, w_norm, h_norm)
    _emit_layout_update(panel_id, {
        "row": int(snap_y * GRID_ROWS),
        "col": int(snap_x * GRID_COLS),
        "row_span": max(1, int(snap_h * GRID_ROWS)),
        "col_span": max(1, int(snap_w * GRID_COLS))
    })

    # Reset drag state
    st.session_state.drag_state.update({
        "active_panel": None,
        "dragging": False,
        "grid_target": (snap_x, snap_y),
        "current_pos": (snap_x, snap_y)
    })


# --------------------------------------------------------------
# 🧩 FRONTEND PAYLOAD (BRIDGE TO REACT / JS)
# --------------------------------------------------------------
def get_frontend_payload():
    """Expose current drag state as JSON for React bridge."""
    return json.dumps(st.session_state.drag_state)


# --------------------------------------------------------------
# 🧪 TEST HARNESS
# --------------------------------------------------------------
def _demo_debug_info():
    st.markdown("### 🧩 Drag Engine Debug")
    st.json(st.session_state.drag_state)
    if "layout_state" in st.session_state:
        st.markdown("**Layout State:**")
        st.json(st.session_state.layout_state)


if __name__ == "__main__":
    st.title("Drag Engine Demo")
    _demo_debug_info()
