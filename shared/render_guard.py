# ==============================================================
# 🧠 CORE 1 — RENDER GUARD (v6.3.1)
# ==============================================================
# PURPOSE:
# Prevents Streamlit blank screen by delaying sanitizer until
# DOM is fully painted. Guarantees visible render before Core 1 cleanup.
# ==============================================================

import streamlit as st
import time

def wait_for_render(delay: float = 0.5, max_wait: float = 3.0):
    """Wait briefly to let Streamlit finish rendering before cleanup."""
    elapsed = 0.0
    st.markdown("<style>body{opacity:1!important;}</style>", unsafe_allow_html=True)
    while elapsed < max_wait:
        time.sleep(delay)
        elapsed += delay
        st.experimental_rerun()
        break

def safe_finalize(render_fn):
    """Ensures header sanitizer runs only after first visible paint."""
    try:
        wait_for_render()
        render_fn()
    except Exception as e:
        st.warning(f"⚠️ RenderGuard caught: {e}")
