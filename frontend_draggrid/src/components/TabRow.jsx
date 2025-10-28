// ============================================================================
// 🧭 TAB ROW — Phase 22.0 (Trading Terminal Tab Navigation)
// ============================================================================
// Displays horizontal tabs: Intraday / Sector Rotation / Wealth / Journal /
// Backtest / HA Terminal. Each tab will later toggle main content panels.
// ============================================================================

import React, { useState } from "react";

export default function TabRow() {
  const [active, setActive] = useState("Intraday");

  const tabs = [
    "Intraday",
    "Sector Rotation",
    "Wealth",
    "Journal",
    "Backtest",
    "HA Terminal",
  ];

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "#121416",
        borderBottom: "1px solid #2a2d31",
        display: "flex",
        alignItems: "center",
        justifyContent: "flex-start",
        gap: "24px",
        padding: "0 16px",
        color: "#ccc",
        fontFamily: "Inter, sans-serif",
        fontSize: "14px",
        fontWeight: 500,
      }}
    >
      {tabs.map((tab) => (
        <div
          key={tab}
          onClick={() => setActive(tab)}
          style={{
            padding: "6px 10px",
            borderRadius: "6px",
            cursor: "pointer",
            background: active === tab ? "#33b249" : "transparent",
            color: active === tab ? "#fff" : "#aaa",
            fontWeight: active === tab ? 600 : 400,
            transition: "all 0.2s ease",
          }}
        >
          {tab}
        </div>
      ))}
    </div>
  );
}
