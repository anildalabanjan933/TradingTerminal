# System_1_Nifty_OI/panels/panel_template.py
# -----------------------------------------
# Simple panel template for Nifty OI dashboard.
# Delete old file and paste this full file as replacement.
#
# This panel exposes `def render(st)` which the dashboard calls.
# Keep this simple and easy to read for non-engineers.

from __future__ import annotations
import streamlit as st
import time
import math
import random

def _generate_fake_price_series(n=60, start=20000.0):
    """Generate a tiny fake price series for placeholder charting."""
    prices = [start]
    for i in range(1, n):
        # small random walk
        change = random.uniform(-0.25, 0.25)
        prices.append(max(1, prices[-1] + change))
    return prices

def render(st: "streamlit") -> None:
    """
    Render function: dashboard will call panels.panel_template.render(st)
    Keep this function side-effect free except for Streamlit drawing calls.
    """
    try:
        st.subheader("Panel: Template — Price Preview")
        st.markdown(
            """
            This is a safe, beginner-friendly panel template.
            Use this as a starting point for your real panels (chart, OI, strategy).
            """
        )

        # small top-row summary boxes
        col1, col2, col3 = st.columns(3)
        col1.metric("Market", "NIFTY 50")
        col2.metric("Last Price", f"{_generate_fake_price_series(1, 19500)[0]:.2f}")
        col3.metric("Bias", "Neutral")

        st.write("")  # spacer

        # Placeholder line chart using Streamlit built-in chart
        prices = _generate_fake_price_series(n=90, start=19500.0)
        st.line_chart({"Price": prices}, use_container_width=True)

        st.write("")  # small spacer

        # Basic controls and test
        with st.expander("Panel Tools / Test"):
            if st.button("Run panel self-check"):
                st.info("Running panel self-check...")
                time.sleep(0.4)
                st.success("Panel template OK — rendering worked.")

            st.write("Panel tips:")
            st.markdown(
                """
                - Replace the chart with your real TOI / OI chart code.  
                - Keep a `render(st)` function so `dashboard real.py` can call it safely.  
                - Wrap heavy operations (API calls) with timeouts and caching.
                """
            )

        # Safe footer note
        st.caption("Template panel — safe to edit. If you break it, dashboard will show an error inside this panel only.")

    except Exception as e:
        # Show friendly error message inside panel (prevents whole page from blanking)
        st.error("Panel encountered an error while rendering.")
        st.write(f"Short error: {e}")
        # show more details for debugging if user wants it
        with st.expander("Show technical details"):
            import traceback
            st.code(traceback.format_exc())
