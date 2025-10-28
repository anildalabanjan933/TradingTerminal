import os

# === ROOT PATH ===
BASE_DIR = "Streamlit_TradingSystems/System_2_TradingTerminal"

# === FOLDER STRUCTURE ===
folders = [
    f"{BASE_DIR}/panels",
    f"{BASE_DIR}/data/intraday_data",
    f"{BASE_DIR}/data/swing_data",
    f"{BASE_DIR}/data/sector_data",
    f"{BASE_DIR}/assets/icons",
    f"{BASE_DIR}/assets/css",
    f"{BASE_DIR}/assets/charts",
    f"{BASE_DIR}/logs",
    f"{BASE_DIR}/tests",
    f"{BASE_DIR}/docs",
    f"{BASE_DIR}/snapshots",
    "Streamlit_TradingSystems/shared"
]

# === FILES (placeholders) ===
files = {
    f"{BASE_DIR}/dashboard.py": "",
    f"{BASE_DIR}/app_config.json": "{}",
    f"{BASE_DIR}/panels/__init__.py": "",
    f"{BASE_DIR}/panels/top_bar_panel.py": "",
    f"{BASE_DIR}/panels/left_sidebar.py": "",
    f"{BASE_DIR}/panels/chart_layout_panel.py": "",
    f"{BASE_DIR}/panels/chart_toolbar.py": "",
    f"{BASE_DIR}/panels/alert_order_manager.py": "",
    f"{BASE_DIR}/panels/watchlist_scanner_panel.py": "",
    f"{BASE_DIR}/panels/risk_manager_panel.py": "",
    f"{BASE_DIR}/panels/journal_panel.py": "",
    f"{BASE_DIR}/panels/trade_panel.py": "",
    f"{BASE_DIR}/panels/wealth_creation_panel.py": "",
    f"{BASE_DIR}/panels/sector_rotation_panel.py": "",
    f"{BASE_DIR}/panels/layout_editor_panel.py": "",
    f"{BASE_DIR}/data/fyers_env.json": "{}",
    f"{BASE_DIR}/data/temp_state.json": "{}",
    f"{BASE_DIR}/logs/trade_logs.csv": "date, symbol, side, qty, price, pnl\n",
    f"{BASE_DIR}/logs/alert_logs.csv": "timestamp, alert_type, symbol, message\n",
    f"{BASE_DIR}/logs/error_logs.txt": "",
    f"{BASE_DIR}/tests/smoke_test.py": "# basic smoke test placeholder\n",
    f"{BASE_DIR}/tests/performance_test.py": "# performance test placeholder\n",
    f"{BASE_DIR}/docs/README.md": "# Documentation Folder\n",
    "Streamlit_TradingSystems/shared/fyers_auth.py": "# FYERS auth helper\n",
    "Streamlit_TradingSystems/shared/layout_tokens.py": "# Layout metrics & grid tokens\n",
    "Streamlit_TradingSystems/shared/utils.py": "# Common helper utilities\n",
    "Streamlit_TradingSystems/shared/constants.py": "# Shared constants\n",
    "Streamlit_TradingSystems/shared/style_manager.py": "# Styling helper for Streamlit\n",
    f"{BASE_DIR}/README.md": "# Trading Terminal System\n"
}

# === CREATE STRUCTURE ===
for folder in folders:
    os.makedirs(folder, exist_ok=True)

for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Trading Terminal folder structure successfully created!")
print(f"📁 Root: {os.path.abspath(BASE_DIR)}")
