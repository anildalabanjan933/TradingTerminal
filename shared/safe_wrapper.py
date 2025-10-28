# ==============================================================
# Streamlit_TradingSystems/shared/safe_wrapper.py
# ==============================================================
# Purpose:
# - Provide a safe decorator and helper utilities to render Streamlit
#   panels without crashing the entire dashboard when a panel throws.
# - Centralized location so all panels can import `safe_display`.
# ==============================================================

import streamlit as st
import traceback
import sys
import logging
from functools import wraps

# Basic logger for internal debugging (writes to console)
logger = logging.getLogger("safe_wrapper")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s — %(levelname)s — %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def safe_display(func):
    """
    Decorator to safely render Streamlit panel functions.
    If the decorated function raises an exception, show a compact
    error box and the traceback (scrollable) inside the Streamlit app
    instead of letting the whole app crash.

    Usage:
        @safe_display
        def render():
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Log for backend visibility
            logger.exception("Panel error in %s: %s", getattr(func, "__name__", str(func)), e)

            # User-friendly inline error in Streamlit
            st.error(f"⚠️ Panel error: {e}")
            tb = traceback.format_exc()
            # Show small scrollable traceback to help debugging
            st.text_area("Traceback (for debugging)", tb, height=220)
            # Optionally return None so caller can continue
            return None
    return wrapper


# Small helper to render a warning box (reusable)
def render_missing_dependency(name: str):
    """
    Render a consistent message when a dependency / function is missing.
    """
    st.warning(f"⚠️ Missing dependency or incomplete integration: {name}. See logs for details.")


# Export names
__all__ = ["safe_display", "render_missing_dependency"]
