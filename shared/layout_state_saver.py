# ==============================================================
# 📄 FILE: Streamlit_TradingSystems/shared/layout_state_saver.py
# ==============================================================
# PURPOSE:
#   Persists layout positions, spans, and grid settings
#   after drag or resize operations.
#   Automatically restores previous layout on reload.
# ==============================================================

import streamlit as st
import json
from pathlib import Path
import time

# --------------------------------------------------------------
# ⚙️ FILE CONFIG
# --------------------------------------------------------------
LAYOUT_SAVE_PATH = Path(__file__).resolve().parents[2] / "System_2_TradingTerminal" / "data" / "temp_state.json"

# --------------------------------------------------------------
# 🧠 SESSION INIT
# --------------------------------------------------------------
if "layout_state" not in st.session_state:
    st.session_state["layout_state"] = {}

# --------------------------------------------------------------
# 💾 SAVE LAYOUT STATE
# --------------------------------------------------------------
def save_layout_state(panel_id: str, layout_cfg: dict):
    """
    Saves updated panel layout into session + disk.
    Example layout_cfg:
    {
        'row': 1, 'col': 2,
        'row_span': 2, 'col_span': 3
    }
    """
    layout_state = st.session_state.get("layout_state", {})
    layout_state[panel_id] = layout_cfg
    st.session_state["layout_state"] = layout_state

    try:
        LAYOUT_SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LAYOUT_SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(layout_state, f, indent=2)
    except Exception as e:
        st.warning(f"⚠️ Layout save failed: {e}")


# --------------------------------------------------------------
# 📂 LOAD LAYOUT STATE
# --------------------------------------------------------------
def load_layout_state():
    """Loads persisted layout_state.json into Streamlit session."""
    if not LAYOUT_SAVE_PATH.exists():
        return {}

    try:
        with open(LAYOUT_SAVE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        st.session_state["layout_state"] = data
        return data
    except Exception as e:
        st.warning(f"⚠️ Layout load failed: {e}")
        return {}


# --------------------------------------------------------------
# ♻️ RESET TO DEFAULT
# --------------------------------------------------------------
def reset_layout():
    """Resets current layout to default (clears file + session)."""
    st.session_state["layout_state"] = {}
    if LAYOUT_SAVE_PATH.exists():
        try:
            LAYOUT_SAVE_PATH.unlink()
        except Exception:
            pass


# --------------------------------------------------------------
# 🧩 AUTO-SAVE HANDLER
# --------------------------------------------------------------
def auto_save_if_changed(throttle_sec: float = 2.0):
    """
    Automatically saves layout when st.session_state changes.
    Throttled to avoid disk writes every frame.
    """
    last_save = st.session_state.get("_last_layout_save", 0.0)
    now = time.time()
    if now - last_save < throttle_sec:
        return

    layout_state = st.session_state.get("layout_state", {})
    if layout_state:
        try:
            with open(LAYOUT_SAVE_PATH, "w", encoding="utf-8") as f:
                json.dump(layout_state, f, indent=2)
            st.session_state["_last_layout_save"] = now
        except Exception as e:
            st.warning(f"⚠️ Auto-save error: {e}")


# --------------------------------------------------------------
# 🧪 DEBUG / TEST HARNESS
# --------------------------------------------------------------
def _demo_debug_info():
    st.markdown("### 🧩 Layout State Saver Debug")
    st.json(st.session_state.get("layout_state", {}))
    st.markdown(f"**File path:** `{LAYOUT_SAVE_PATH}`")


if __name__ == "__main__":
    st.title("Layout State Saver Demo")
    _demo_debug_info()
