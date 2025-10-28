# ==============================================================
# 📄 FILE: panels/left_sidebar.old.py
# 🔹 LEFT SLIDER TOOLBAR — v6.3 (Live-Ready Build Freeze)
# ==============================================================
import streamlit as st
import datetime
import sys, os, json

# === Fix import paths ===
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
SHARED_PATH = os.path.join(PROJECT_ROOT, "shared")
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if SHARED_PATH not in sys.path:
    sys.path.insert(0, SHARED_PATH)

# === Shared Imports ===
from Streamlit_TradingSystems.shared import fyers_auth, style_manager, preset_manager, utils
from Streamlit_TradingSystems.System_2_TradingTerminal.panels import layout_editor_panel

# ==============================================================
# 🧭 SIDEBAR MAIN FUNCTION
# ==============================================================
def render_left_sidebar():
    with st.sidebar:
        st.button("◄ Close", key="close_sidebar")
        st.markdown("### Terminal Controls")

        # FYERS Connection Status
        try:
            _ = fyers_auth.get_fyers_client()
            st.success("🟢 FYERS Connected")
        except Exception:
            st.warning("🟡 FYERS Not Connected — Refresh Token")

        # ======================================================
        # 🔁 PAPER ↔ REAL MODE TOGGLE
        # ======================================================
        trade_mode = st.session_state.get("trade_mode", "Paper")
        toggle = st.toggle("🔁 Enable Real Trading Mode", value=(trade_mode == "Real"))
        new_mode = "Real" if toggle else "Paper"
        if new_mode != trade_mode:
            st.session_state["trade_mode"] = new_mode
            # Auto-freeze snapshot on real mode activation
            if new_mode == "Real":
                utils.save_snapshot(
                    "phase_5_3_0_freeze.json",
                    {"mode": "Real", "timestamp": datetime.datetime.now().isoformat()},
                )
                st.warning("🚨 REAL MODE ENABLED — Layout frozen & snapshot saved.")
            else:
                st.info("🧪 PAPER MODE ACTIVE — Safe simulation only.")

        st.divider()

        # ======================================================
        # SESSION & SETTINGS PANELS
        # ======================================================
        with st.expander("1️⃣ Session & Profile", expanded=False):
            st.text_input("User Name", "Trader_X")
            st.selectbox("Profile Mode", ["Intraday", "Swing", "Wealth"], index=0)
            st.radio("Trade Mode (Mirror)", ["Paper", "Real"], horizontal=True, key="mirror_mode")

        with st.expander("2️⃣ Layout Manager", expanded=False):
            st.radio("Chart Layout", ["1 Chart", "2 Charts", "4 Charts"], horizontal=True)
            st.checkbox("Sync Crosshair", True)
            st.checkbox("Sync Timeframes", True)
            st.checkbox("Snap to Grid", True)

        with st.expander("3️⃣ Fyers API", expanded=False):
            st.text_input("App ID", "XXXXXXXX", type="password")
            st.text_input("Secret ID", "XXXXXXXX", type="password")
            st.button("🔑 Login")
            st.button("🔄 Refresh Token")
            st.caption(f"Last Sync: {datetime.datetime.now().strftime('%H:%M:%S')}")

        with st.expander("4️⃣ Alert Settings", expanded=False):
            st.selectbox("Alert Type", ["Candle Cross", "HA Cross", "Body Touch"])
            st.selectbox("Sensitivity", ["Strict", "Lenient"])
            st.multiselect("Actions", ["Sound", "Popup", "Webhook", "Telegram"])

        with st.expander("5️⃣ Order Settings", expanded=False):
            st.selectbox("Order Type", ["Market", "Limit", "StopLoss", "Bracket"])
            st.number_input("Default Qty", min_value=1, value=1)
            st.checkbox("Auto StopLoss", True)
            st.checkbox("Auto Target", True)
            st.slider("Risk per Trade (%)", 0.5, 5.0, 1.0)

        with st.expander("6️⃣ General Settings", expanded=False):
            st.selectbox("Data Refresh", ["Realtime", "1s", "2s", "5s"], index=0)
            st.checkbox("Enable Cache", True)
            st.checkbox("Lightweight Mode", False)
            st.slider("Volume", 0, 100, 70)

        with st.expander("7️⃣ Hotkeys & Help", expanded=False):
            st.write("""
            **Shortcuts:**
            - H → Horizontal Line  
            - T → Trend Line  
            - 1/2/4 → Change Layout  
            - ⌫ → Delete Object  
            - Space → Next Symbol
            """)

        with st.expander("🎨 Style Manager", expanded=False):
            try:
                style_manager.style_manager_panel()
            except Exception as e:
                st.warning(f"Style Manager unavailable: {e}")

        with st.expander("🌸 Layout Editor", expanded=False):
            try:
                layout_editor_panel.render_layout_editor_panel()
            except Exception as e:
                st.warning(f"Layout Editor unavailable: {e}")

        with st.expander("💾 Preset & Snapshot Manager", expanded=False):
            try:
                preset_manager.preset_manager_panel()
            except Exception as e:
                st.warning(f"Preset Manager unavailable: {e}")

        # ======================================================
        # FOOTER
        # ======================================================
        st.markdown("---")
        st.caption(f"v6.3 | Last Save {datetime.datetime.now().strftime('%H:%M:%S')}")
        col1, col2 = st.columns(2)
        with col1:
            st.button("Apply All")
        with col2:
            st.button("Reset Sidebar")

        # Disable layout editing in Real Mode
        if st.session_state.get("trade_mode") == "Real":
            st.markdown("<b>Layout Locked 🔒</b>", unsafe_allow_html=True)


# ==============================================================
# 🔹 STANDALONE TEST MODE
# ==============================================================
if __name__ == "__main__":
    st.set_page_config(page_title="Left Sidebar — v6.3 Live Freeze", layout="wide")
    render_left_sidebar()
