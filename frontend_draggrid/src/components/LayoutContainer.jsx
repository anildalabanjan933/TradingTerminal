// =============================================================
// 📄 FILE: frontend_draggrid/src/components/LayoutContainer.jsx
// =============================================================
// VERSION: v8.2.0 — Stage 6G (Top Bars + Trade Drawer Re-integration)
// PURPOSE:
// ✅  Adds Top Toolbar, Chart Toolbar, and Bottom Trade Panel
// ✅  Keeps Drag + Resize Grid from Stage 6F
// ✅  One-screen 1080 p fit (no scroll)
// =============================================================

import React, { useState, useEffect } from "react";
import GridLayout from "react-grid-layout";
import "react-grid-layout/css/styles.css";
import "react-resizable/css/styles.css";
import "./layoutContainer.css";

export default function LayoutContainer() {
  const defaultLayout = [
    { i: "chart1", x: 0, y: 0, w: 3, h: 2 },
    { i: "chart2", x: 3, y: 0, w: 3, h: 2 },
    { i: "watch1", x: 0, y: 2, w: 3, h: 2 },
    { i: "watch2", x: 3, y: 2, w: 3, h: 2 },
  ];
  const [layout, setLayout] = useState(() => {
    const saved = localStorage.getItem("stage6g_layout");
    return saved ? JSON.parse(saved) : defaultLayout;
  });
  const [drawerOpen, setDrawerOpen] = useState(false);

  const handleLayoutChange = (l) => {
    setLayout(l);
    localStorage.setItem("stage6g_layout", JSON.stringify(l));
  };

  const toggleDrawer = () => setDrawerOpen(!drawerOpen);

  return (
    <div className="frame6g">
      {/* 🔹 Fixed Top Bar */}
      <div className="topbar">
        <span className="logo">💹 Trading Terminal</span>
        <div className="topbar-actions">
          <button>📊 Sector Rotation</button>
          <button>🔥 Wealth</button>
          <button>🧮 Backtest</button>
          <button>🗒 Journal</button>
        </div>
        <span className="status-dot">● Online</span>
      </div>

      {/* 🔹 Chart Toolbar Row */}
      <div className="chart-toolbar">
        <select>
          <option>1 min</option>
          <option>5 min</option>
          <option>15 min</option>
        </select>
        <button>📈 Candle</button>
        <button>✏ Draw</button>
        <button>⚙ Settings</button>
      </div>

      {/* 🔹 Grid Section */}
      <div className="grid-wrapper">
        <GridLayout
          className="layout"
          layout={layout}
          cols={6}
          rowHeight={160}
          width={window.innerWidth}
          onLayoutChange={handleLayoutChange}
          draggableHandle=".chart-header"
        >
          <div key="chart1" className="chart-box">
            <div className="chart-header">📈 Chart 1</div>
          </div>
          <div key="chart2" className="chart-box">
            <div className="chart-header">📈 Chart 2</div>
          </div>
          <div key="watch1" className="chart-box">
            <div className="chart-header">📊 Watch 1</div>
          </div>
          <div key="watch2" className="chart-box">
            <div className="chart-header">📊 Watch 2</div>
          </div>
        </GridLayout>
      </div>

      {/* 🔹 Bottom Trade Drawer */}
      <div className={`trade-drawer ${drawerOpen ? "open" : ""}`}>
        <div className="trade-header">
          <span>💥 Trade Panel</span>
          <button onClick={toggleDrawer}>
            {drawerOpen ? "⬇ Close" : "⬆ Open"}
          </button>
        </div>
        <div className="trade-body">
          <button className="buy">BUY</button>
          <button className="sell">SELL</button>
          <button className="close">CLOSE ALL</button>
        </div>
      </div>
    </div>
  );
}
