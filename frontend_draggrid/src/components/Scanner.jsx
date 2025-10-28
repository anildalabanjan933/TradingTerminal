// ============================================================================
// 🔍 SCANNER PANEL — Phase 21.1 (Component Snap Integration)
// ============================================================================
// Displays a simplified intraday scanner preview table.
// Final version will load live scan logic from backend modules.
// ============================================================================

import React from "react";

export default function Scanner() {
  const headerStyle = {
    background: "#191c21",
    color: "#9be07e",
    padding: "8px 10px",
    fontWeight: 600,
    borderBottom: "1px solid #2a2d31",
  };

  const rowStyle = {
    display: "flex",
    justifyContent: "space-between",
    padding: "6px 10px",
    borderBottom: "1px solid #2a2d31",
    color: "#e5e5e5",
    fontSize: "13px",
    fontFamily: "Inter, sans-serif",
  };

  const dummyData = [
    { symbol: "HDFCBANK", bias: "Bullish", score: "+82" },
    { symbol: "ICICIBANK", bias: "Bearish", score: "-45" },
    { symbol: "SBIN", bias: "Bullish", score: "+63" },
    { symbol: "KOTAKBANK", bias: "Neutral", score: "0" },
  ];

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "#121416",
        border: "1px solid #2a2d31",
        borderRadius: "8px",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Header */}
      <div style={headerStyle}>🔍 Intraday Scanner</div>

      {/* Table rows */}
      <div style={{ flex: 1, overflowY: "auto" }}>
        {dummyData.map((item, i) => (
          <div key={i} style={rowStyle}>
            <span>{item.symbol}</span>
            <span style={{ color: item.bias === "Bullish" ? "#33b249" : item.bias === "Bearish" ? "#ff5757" : "#bbb" }}>
              {item.bias}
            </span>
            <span>{item.score}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
