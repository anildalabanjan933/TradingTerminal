# ==============================================================
# 📄 FILE: shared/grid_alignment.py
# ==============================================================
# PURPOSE:
#   Provides grid snapping, ghost overlay, and alignment math
#   for TradingView-style drag + resize behavior.
#   Works with drag_engine.py + resize_observer.py.
# ==============================================================

import streamlit as st
import json
import math
import time

# --------------------------------------------------------------
# ⚙️ GRID CONFIG
# --------------------------------------------------------------
GRID_ROWS = 6
GRID_COLS = 6
GHOST_FADE_MS = 150
SNAP_THRESHOLD = 1 / 12  # half a grid cell

# --------------------------------------------------------------
# 🧠 INIT
# --------------------------------------------------------------
if "grid_overlay_state" not in st.session_state:
    st.session_state.grid_overlay_state = {
        "visible": False,
        "target_cell": None,
        "alpha": 0.0,
        "active_panel": None,
        "last_snap_time": 0.0,
    }

# --------------------------------------------------------------
# 🎯 HELPERS
# --------------------------------------------------------------
def _nearest_grid_cell(x_norm: float, y_norm: float):
    """Return nearest (row, col) in 6×6 grid."""
    col = min(GRID_COLS - 1, max(0, round(x_norm * GRID_COLS)))
    row = min(GRID_ROWS - 1, max(0, round(y_norm * GRID_ROWS)))
    return row, col


def _cell_to_norm(row: int, col: int):
    return col / GRID_COLS, row / GRID_ROWS


def _animate_fade_in(alpha, step=0.1):
    return min(1.0, alpha + step)


def _animate_fade_out(alpha, step=0.1):
    return max(0.0, alpha - step)


# --------------------------------------------------------------
# ✨ SNAP ENGINE
# --------------------------------------------------------------
def compute_snap_target(x_norm: float, y_norm: float):
    """Compute grid cell target for given fractional coordinates."""
    row, col = _nearest_grid_cell(x_norm, y_norm)
    st.session_state.grid_overlay_state.update({
        "visible": True,
        "target_cell": (row, col),
        "alpha": _animate_fade_in(st.session_state.grid_overlay_state["alpha"]),
        "last_snap_time": time.time()
    })
    return row, col


def fade_out_overlay():
    """Fades out overlay when drag/resize ends."""
    alpha = _animate_fade_out(st.session_state.grid_overlay_state["alpha"])
    st.session_state.grid_overlay_state.update({
        "visible": alpha > 0.05,
        "alpha": alpha
    })


# --------------------------------------------------------------
# 🧩 VISUAL SNAP PAYLOAD (→ React)
# --------------------------------------------------------------
def get_overlay_payload():
    """
    Returns JSON payload consumed by React overlay layer.
    Example:
        {
          "visible": true,
          "row": 3,
          "col": 2,
          "alpha": 0.8
        }
    """
    state = st.session_state.grid_overlay_state
    row, col = state["target_cell"] or (None, None)
    payload = {
        "visible": state["visible"],
        "row": row,
        "col": col,
        "alpha": round(state["alpha"], 2),
        "timestamp": round(state["last_snap_time"], 2)
    }
    return json.dumps(payload)


# --------------------------------------------------------------
# 🔄 COMBINED UPDATE — LIVE SYNC LOOP
# --------------------------------------------------------------
def update_alignment(x_norm: float, y_norm: float, active_panel: str):
    """Called every drag/resize frame."""
    st.session_state.grid_overlay_state["active_panel"] = active_panel
    compute_snap_target(x_norm, y_norm)


def finalize_snap():
    """Finalize snap and fade overlay."""
    fade_out_overlay()
    st.session_state.grid_overlay_state["active_panel"] = None


# --------------------------------------------------------------
# 🧪 DEBUG PANEL
# --------------------------------------------------------------
def _demo_debug_info():
    st.markdown("### 🧩 Grid Alignment Debug")
    st.json(st.session_state.grid_overlay_state)


if __name__ == "__main__":
    st.title("Grid Alignment Demo")
    _demo_debug_info()
