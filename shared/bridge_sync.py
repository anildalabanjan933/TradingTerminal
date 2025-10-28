# ==============================================================
# 📄 FILE: Streamlit_TradingSystems/shared/bridge_sync.py
# ==============================================================
# PURPOSE:
# Stage 6B — Receive sidebar state updates from React
# ==============================================================

import streamlit as st
import json

def sidebar_state_bridge():
    """Handles Streamlit ↔ React sidebar state sync."""
    if "sidebar_state" not in st.session_state:
        st.session_state.sidebar_state = False

    # This script listens for postMessage from React
    st.markdown(
        """
        <script>
        window.addEventListener("message", (e) => {
            if (e.data?.type === "streamlit:sidebar_state") {
                const open = e.data.payload.open;
                window.parent.postMessage({
                    type: "streamlit:set_sidebar_state",
                    payload: { open: open }
                }, "*");
                Streamlit.setComponentValue(open);
            }
        });
        </script>
        """,
        unsafe_allow_html=True,
    )
