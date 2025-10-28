// ============================================================================
// 🧱 TERMINAL FRAME — Phase 22.2 (Right Dual-Watchlist Integrated)
// ============================================================================
// Adds RightStack.jsx to create two watchlists in right column.
// Now full 1 : 1 panel layout: TopBar → TabRow → Toolbar → LeftSidebar → Charts → RightStack → Trade + Risk.
// ============================================================================

import React from "react";
import TopBar from "./TopBar.jsx";
import TabRow from "./TabRow.jsx";
import ChartToolbar from "./ChartToolbar.jsx";
import ChartArea from "./ChartArea.jsx";
import TradePanel from "./TradePanel.jsx";
import RiskManager from "./RiskManager.jsx";
import LeftSidebar from "./LeftSidebar.jsx";
import RightStack from "./RightStack.jsx";
import "./terminalFrame.css";

export default function TerminalFrame() {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateRows: "6% 5% 7% 60% 22%",
        gridTemplateColumns: "auto 45% 20% 20%",
        gap: "6px",
        height: "100vh",
        width: "100vw",
        background: "#0b0c0e",
        overflow: "hidden",
        fontFamily: "Inter, sans-serif",
      }}
    >
      {/* Top Header */}
      <div style={{ gridColumn: "1 / span 4", gridRow: "1" }}>
        <TopBar />
      </div>

      {/* Tab Row */}
      <div style={{ gridColumn: "1 / span 4", gridRow: "2" }}>
        <TabRow />
      </div>

      {/* Toolbar */}
      <div style={{ gridColumn: "1 / span 4", gridRow: "3" }}>
        <ChartToolbar />
      </div>

      {/* Left Sidebar */}
      <div style={{ gridColumn: "1", gridRow: "4 / span 2" }}>
        <LeftSidebar />
      </div>

      {/* Chart Area */}
      <div style={{ gridColumn: "2 / span 2", gridRow: "4" }}>
        <ChartArea />
      </div>

      {/* Right Dual Watchlist Stack */}
      <div style={{ gridColumn: "4", gridRow: "4 / span 2" }}>
        <RightStack />
      </div>

      {/* Bottom Panels */}
      <div style={{ gridColumn: "2 / span 1", gridRow: "5" }}>
        <TradePanel />
      </div>
      <div style={{ gridColumn: "3 / span 1", gridRow: "5" }}>
        <RiskManager />
      </div>
    </div>
  );
}
