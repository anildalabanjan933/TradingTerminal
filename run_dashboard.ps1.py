# ============================================================
# 🚀 Run Trading Terminal — Unified Dashboard (v5.5.5)
# Location: D:\Streamlit_TradingSystems\run_dashboard.ps1
# ============================================================

Write-Host "🔹 Activating virtual environment..." -ForegroundColor Cyan
Set-Location "D:\Streamlit_TradingSystems"
.\.venv\Scripts\Activate.ps1

Write-Host "✅ Virtual environment activated." -ForegroundColor Green
Write-Host "🔹 Starting Streamlit dashboard..." -ForegroundColor Cyan

# Run full unified dashboard
streamlit run "System_2_TradingTerminal\dashboard.py" --server.runOnSave=false

Write-Host "✅ Dashboard running. Open http://localhost:8501 in your browser." -ForegroundColor Yellow
