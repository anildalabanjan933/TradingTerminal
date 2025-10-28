# ==============================================================
# 📄 File: Streamlit_TradingSystems/shared/perf_tuner.py
# 🔹 PERFORMANCE TUNER — Phase 6.0 (QA + Optimization Layer)
# ==============================================================

import streamlit as st
import os, json, datetime, gc

LOG_DIR = "Streamlit_TradingSystems/System_2_TradingTerminal/logs"
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------------------
# 🧩 CACHE CONFIGURATION
# --------------------------------------------------------------
def cache_config():
    """Set Streamlit global caching and page settings."""
    st.set_page_config(
        page_title="Trading Terminal — Optimized",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.cache_data.clear()
    st.cache_resource.clear()

# --------------------------------------------------------------
# 🧹 SESSION CLEANUP
# --------------------------------------------------------------
def cleanup_session(threshold_minutes: int = 10):
    """Auto-remove unused session_state keys after timeout."""
    if "last_cleanup" not in st.session_state:
        st.session_state["last_cleanup"] = datetime.datetime.now()

    now = datetime.datetime.now()
    last = st.session_state["last_cleanup"]
    delta = (now - last).total_seconds() / 60

    if delta > threshold_minutes:
        to_delete = [k for k in st.session_state.keys() if k.startswith("temp_")]
        for k in to_delete:
            del st.session_state[k]
        st.session_state["last_cleanup"] = now
        gc.collect()
        st.info(f"🧹 Session cleaned ({len(to_delete)} temp keys removed)")

# --------------------------------------------------------------
# 🪵 LOG ROTATION
# --------------------------------------------------------------
def rotate_logs():
    """Archive logs weekly to prevent disk growth."""
    for log_file in ["trade_logs.csv", "alert_logs.csv", "error_logs.txt"]:
        full_path = os.path.join(LOG_DIR, log_file)
        if os.path.exists(full_path):
            size_mb = os.path.getsize(full_path) / (1024 * 1024)
            if size_mb > 5:  # 5 MB threshold
                backup_name = log_file.replace(".", f"_{datetime.date.today()}.")
                os.rename(full_path, os.path.join(LOG_DIR, backup_name))
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write("")
                st.warning(f"🪵 Log rotated → {backup_name}")

# --------------------------------------------------------------
# ⚙️ MAIN OPTIMIZATION ROUTINE
# --------------------------------------------------------------
def optimize():
    """Run all performance routines silently on dashboard start."""
    try:
        cache_config()
        cleanup_session()
        rotate_logs()
    except Exception as e:
        st.warning(f"⚠️ Perf tuner warning: {e}")

# --------------------------------------------------------------
# 🔹 STANDALONE TEST
# --------------------------------------------------------------
if __name__ == "__main__":
    st.set_page_config(page_title="Perf Tuner Test", layout="wide")
    st.title("🧠 Performance Tuner — Diagnostic Mode")
    if st.button("Run Optimization"):
        optimize()
        st.success("✅ Optimization routine executed successfully.")
