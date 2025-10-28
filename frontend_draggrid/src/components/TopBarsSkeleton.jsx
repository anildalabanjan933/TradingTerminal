// ============================================================================
// 📄 FILE: TopBarsSkeleton.jsx
// Fix alignment — dedicated stacked bars (Top, Tab, Toolbar)
// ============================================================================

import React from "react";

export default function TopBarsSkeleton() {
  return (
    <div style={{ display: "flex", flexDirection: "column", width: "100%" }}>
      {/* 🧭 Top Bar (24 px) */}
      <div
        style={{
          height: 24,
          background: "#121212",
          borderBottom: "1px solid #222",
          display: "flex",
          alignItems: "center",
          paddingLeft: 8,
          fontSize: 11,
          color: "#ccc",
        }}
      >
        🧭 Top Bar (24 px)
      </div>

      {/* 📁 Tab Row (24 px) */}
      <div
        style={{
          height: 24,
          background: "#141414",
          borderBottom: "1px solid #222",
          display: "flex",
          alignItems: "center",
          paddingLeft: 8,
          gap: 10,
          fontSize: 11,
          color: "#ccc",
        }}
      >
        📁 Tab Row (24 px)
        <span>Intraday</span>
        <span>Sector Rotation</span>
        <span>Wealth</span>
        <span>Journal</span>
        <span>Backtest</span>
      </div>

      {/* ⚙ Chart Toolbar (28 px) */}
      <div
        style={{
          height: 28,
          background: "#151515",
          borderBottom: "1px solid #222",
          display: "flex",
          alignItems: "center",
          paddingLeft: 8,
          gap: 10,
          fontSize: 11,
          color: "#ccc",
        }}
      >
        ⚙ Chart Toolbar (28 px)
        <span>Symbol</span>
        <span>TF</span>
        <span>Type</span>
        <span>Indicators</span>
        <span>Layout</span>
      </div>
    </div>
  );
}
