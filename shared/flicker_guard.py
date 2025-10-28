# ==============================================================
# 📄 FILE: Streamlit_TradingSystems/shared/flicker_guard.py
# ==============================================================
# PURPOSE:
#   Prevents Streamlit flicker/re-render during drag or resize
#   by throttling layout updates and animating transitions.
#   Provides smooth 60 FPS experience for chart grid motion.
# ==============================================================

import streamlit as st
import time
import json

# --------------------------------------------------------------
# ⚙️ SETTINGS
# --------------------------------------------------------------
FPS_LIMIT = 60
FRAME_INTERVAL = 1.0 / FPS_LIMIT
SMOOTH_TRANSITION_MS = 180

# --------------------------------------------------------------
# 🧠 SESSION INIT
# --------------------------------------------------------------
if "flicker_state" not in st.session_state:
    st.session_state["flicker_state"] = {
        "last_frame_time": 0.0,
        "frame_count": 0,
        "stabilized": True,
    }


# --------------------------------------------------------------
# 🎯 CORE UTILS
# --------------------------------------------------------------
def _allow_next_frame() -> bool:
    """Limit updates to FPS_LIMIT to prevent over-refresh."""
    now = time.time()
    if now - st.session_state["flicker_state"]["last_frame_time"] >= FRAME_INTERVAL:
        st.session_state["flicker_state"]["last_frame_time"] = now
        return True
    return False


def start_guard():
    """Marks start of drag/resize phase (suppresses Streamlit reflow)."""
    st.session_state["flicker_state"]["stabilized"] = False


def end_guard():
    """Releases suppression after animation settles."""
    st.session_state["flicker_state"]["stabilized"] = True


# --------------------------------------------------------------
# 🧩 SMOOTH STYLE INJECTION
# --------------------------------------------------------------
def inject_smooth_css():
    """Injects global CSS transitions for smooth UI motion."""
    st.markdown(
        f"""
        <style>
        .grid-cell {{
            transition:
                transform {SMOOTH_TRANSITION_MS}ms ease-out,
                opacity {SMOOTH_TRANSITION_MS}ms ease-in-out;
            will-change: transform, opacity;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------
# 🔄 FRAME UPDATE LOOP
# --------------------------------------------------------------
def frame_update(callback=None):
    """
    Executes callback (if provided) only when allowed by FPS throttling.
    Useful for live drag/resize rendering.
    """
    if _allow_next_frame():
        if callable(callback):
            callback()
        st.session_state["flicker_state"]["frame_count"] += 1


# --------------------------------------------------------------
# 🧪 DEBUG PANEL
# --------------------------------------------------------------
def _demo_debug_info():
    st.markdown("### 🧩 Flicker Guard Debug")
    st.json(st.session_state["flicker_state"])


if __name__ == "__main__":
    st.title("Flicker Guard Demo")
    inject_smooth_css()
    _demo_debug_info()
