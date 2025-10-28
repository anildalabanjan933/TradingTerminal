// ==============================================================================
// ⚡ FRONTEND → BACKEND CONNECTOR
// Streamlit_TradingSystems/frontend_draggrid/src/api/backend.js
// ==============================================================================

const BASE_URL = "http://localhost:9000"; // FastAPI base URL

// ---------------------- Helper: Safe Fetch Wrapper ----------------------
async function safeFetch(url, options = {}) {
  try {
    const res = await fetch(url, options);
    if (!res.ok) throw new Error(`Request failed: ${res.status}`);
    return res.json();
  } catch (err) {
    console.error(`❌ Fetch error for ${url}:`, err);
    return null;
  }
}

// ---------------------- GET: Market Summary ----------------------
export async function getMarketSummary() {
  const data = await safeFetch(`${BASE_URL}/api/market_summary`);
  if (data && data.summary) console.log("📊 Market summary feed:", data.summary);
  return data;
}

// ---------------------- GET: Watchlist ----------------------
export async function getWatchlist() {
  const data = await safeFetch(`${BASE_URL}/api/get_watchlist`);
  if (data && data.watchlist) console.log("📋 Watchlist feed:", data.watchlist);
  return data;
}

// ---------------------- GET: Positions ----------------------
export async function getPositions() {
  const data = await safeFetch(`${BASE_URL}/api/get_positions`);
  return data;
}

// ---------------------- POST: Place Order ----------------------
export async function placeOrder(order) {
  const data = await safeFetch(`${BASE_URL}/api/place_order`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(order),
  });
  return data;
}

// ---------------------- GET: Chart Data ----------------------
export async function getChartData(symbol = "NIFTY") {
  const data = await safeFetch(`${BASE_URL}/api/chart_data?symbol=${symbol}`);
  return data;
}

// ---------------------- WEBSOCKET: Live Feed ----------------------
export function connectLiveFeed(onMessage) {
  const socket = new WebSocket("ws://localhost:9000/ws/market"); // ✅ same origin
  socket.onopen = () => console.log("🔌 Live feed connected");
  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (onMessage) onMessage(data);
    } catch (err) {
      console.error("❌ WebSocket parse error:", err);
    }
  };
  socket.onerror = (err) => console.error("❌ WebSocket error:", err);
  socket.onclose = () => console.log("🔌 Live feed closed");
  return socket;
}
