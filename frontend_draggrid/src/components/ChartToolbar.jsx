// ============================================================================
// 🧭 CHART TOOLBAR PANEL — Phase 21.1 (Component Snap Integration)
// ============================================================================
// Displays symbol search, timeframe buttons, and indicator placeholders.
// Visually aligned for 1:1 layout — connects later to backend chart controls.
// ============================================================================

import React from "react";

export default function ChartToolbar() {
  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "#14171c",
        borderBottom: "1px solid #2a2d31",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 16px",
        color: "#e5e5e5",
        fontFamily: "Inter, sans-serif",
        fontSize: "14px",
      }}
    >
      {/* Left: Symbol + Timeframe */}
      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
        <input
          type="text"
          placeholder="🔍 Symbol"
          style={{
            background: "#0b0c0e",
            border: "1px solid #333",
            borderRadius: "6px",
            padding: "4px 8px",
            color: "#f0f0f0",
            width: "120px",
          }}
        />
        <div style={{ display: "flex", gap: "6px" }}>
          {["1m", "3m", "5m", "15m", "1h", "1D"].map((tf) => (
            <button
              key={tf}
              style={{
                background: "#1c1f25",
                border: "1px solid #2e3238",
                color: "#ddd",
                padding: "3px 8px",
                borderRadius: "4px",
                cursor: "pointer",
              }}
            >
              {tf}
            </button>
          ))}
        </div>
      </div>

      {/* Right: Indicator + Layout icons */}
      <div style={{ display: "flex", alignItems: "center", gap: "14px" }}>
        <span>📈 Indicators</span>
        <span>📊 Layout</span>
        <span>⚙️ Settings</span>
      </div>
    </div>
  );
}
