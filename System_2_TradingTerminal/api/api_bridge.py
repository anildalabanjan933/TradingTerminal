# ==============================================================================
# ⚡ API BRIDGE — Phase 25.7 → Local Mock Data Feed
# FastAPI backend to connect React frontend with live mock market data
# ==============================================================================
# FILE: Streamlit_TradingSystems/System_2_TradingTerminal/api/api_bridge.py
# ==============================================================================

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import time
import random
import asyncio
from typing import Dict, Any, List

# ------------------------------------------------------------------------------
# 🧠 Initialize app
# ------------------------------------------------------------------------------
app = FastAPI(title="Trading Terminal Backend API", version="1.1.0")

# Allow React frontend (localhost:8080)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# 📊 Helper: Mock Market Data (replace with real Fyers/FNO feed later)
# ------------------------------------------------------------------------------
def generate_market_data(symbol: str) -> Dict[str, Any]:
    price = round(random.uniform(22000, 23000), 2)
    change = round(random.uniform(-150, 150), 2)
    return {
        "symbol": symbol,
        "price": price,
        "change": change,
        "percent": round((change / price) * 100, 2),
        "timestamp": time.strftime("%H:%M:%S"),
    }

# ------------------------------------------------------------------------------
# 🧩 REST API Routes
# ------------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "✅ Trading Terminal Backend is Live", "time": time.strftime("%H:%M:%S")}

# ----- Market Summary -----
@app.get("/api/market_summary")
def market_summary() -> Dict[str, List[Dict[str, Any]]]:
    symbols = ["NIFTY", "BANKNIFTY", "RELIANCE", "INFY", "TCS"]
    data = [generate_market_data(sym) for sym in symbols]
    return {"summary": data}

# ----- Watchlist -----
@app.get("/api/get_watchlist")
def get_watchlist() -> Dict[str, List[Dict[str, Any]]]:
    symbols = ["NIFTY", "BANKNIFTY", "RELIANCE", "INFY", "TCS"]
    data = [generate_market_data(sym) for sym in symbols]
    return {"watchlist": data}

# ----- Positions -----
@app.get("/api/get_positions")
def get_positions():
    positions = [
        {"symbol": "NIFTY", "qty": 1, "pnl": 452.3},
        {"symbol": "BANKNIFTY", "qty": 2, "pnl": -123.4},
    ]
    return {"positions": positions, "timestamp": time.strftime("%H:%M:%S")}

# ----- Place Order -----
@app.post("/api/place_order")
def place_order(order: Dict[str, Any]):
    return {
        "status": "success",
        "details": order,
        "timestamp": time.strftime("%H:%M:%S"),
    }

# ----- Chart Data (mock candles) -----
@app.get("/api/chart_data")
def chart_data(symbol: str = "NIFTY"):
    candles = []
    base_price = 22500
    for i in range(30):
        o = base_price + random.uniform(-100, 100)
        c = o + random.uniform(-50, 50)
        h = max(o, c) + random.uniform(10, 30)
        l = min(o, c) - random.uniform(10, 30)
        candles.append({"time": i, "open": o, "high": h, "low": l, "close": c})
    return {"symbol": symbol, "data": candles}

# ------------------------------------------------------------------------------
# 🔄 WebSocket (Live price stream)
# ------------------------------------------------------------------------------
@app.websocket("/ws/market")
async def websocket_market(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            packet = {
                "symbol": "NIFTY",
                "price": round(random.uniform(22000, 23000), 2),
                "timestamp": time.strftime("%H:%M:%S"),
            }
            await ws.send_text(json.dumps(packet))
            await asyncio.sleep(1)
    except Exception as e:
        print("WebSocket closed:", e)
        await ws.close()

# ------------------------------------------------------------------------------
# 🚀 ENTRY POINT
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("api_bridge:app", host="0.0.0.0", port=9000, reload=True)
