# ==============================================================
# 🚀 Trading Terminal Launcher (Fixes Import Path Permanently)
# ==============================================================

import os, sys, subprocess

# --- Set working directory to project root ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)

# --- Add root to PYTHONPATH ---
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# --- Launch Streamlit from correct root path ---
cmd = [
    "streamlit", "run",
    os.path.join("System_2_TradingTerminal", "dashboard real.py"),
]
subprocess.run(cmd)
