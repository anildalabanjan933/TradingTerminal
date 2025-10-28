// ============================================================================
// 💹 FLEX RESIZE ENGINE — Phase 25.66 (Stable Final Layout)
//  ✅ TradingView-style layout with live drag/resize
//  ✅ Watchlist visible and resizable
//  ✅ Bottom panels aligned perfectly, no gap
// ============================================================================

import React from "react";
import Split from "react-split-grid";
import "./FlexResizeEngine.css";

// === Import actual panels ===
import ChartArea from "./ChartArea";
import Watchlist from "./Watchlist";
import TradePanel from "./TradePanel";
import RiskManager from "./RiskManager";

export default function FlexResizeEngine() {
  return (
    <div className="terminal-root">
      {/* ==== TOP 3 FIXED COMPACT ROWS ==== */}
      <div className="top-row topbar">Top Bar</div>
      <div className="top-row tabrow">Tab Row</div>
      <div className="top-row toolbar">Chart Toolbar</div>

      {/* ==== MAIN FLEXIBLE GRID AREA ==== */}
      <Split
        // one vertical split for main workspace and bottom panels
        render={({ getGridProps, getGutterProps }) => (
          <div
            className="main-grid"
            {...getGridProps()}
            style={{
              display: "grid",
              gridTemplateRows: "1fr 220px", // main + bottom
              height: "100%",
            }}
          >
            {/* === MAIN WORKSPACE ROW (CHART / WATCHLIST) === */}
            <Split
              direction="row"
              // handle drag between sidebar ↔ chart ↔ watchlist
              render={({ getGridProps: g, getGutterProps: gg }) => (
                <div
                  className="workspace"
                  {...g()}
                  style={{
                    display: "grid",
                    gridTemplateColumns: "240px 1fr 300px",
                    width: "100%",
                    height: "100%",
                  }}
                >
                  {/* Sidebar */}
                  <div className="panel sidebar">
                    <div className="panel-title">Sidebar</div>
                  </div>

                  {/* Vertical gutter between sidebar and chart */}
                  <div className="gutter vertical" {...gg("column", 1)} />

                  {/* Chart Area */}
                  <div className="panel chart">
                    <ChartArea />
                  </div>

                  {/* Vertical gutter between chart and watchlist */}
                  <div className="gutter vertical" {...gg("column", 2)} />

                  {/* Watchlist Panel */}
                  <div className="panel rightstack">
                    <Watchlist />
                  </div>
                </div>
              )}
            />

            {/* === Horizontal gutter between workspace and bottom === */}
            <div className="gutter horizontal" {...getGutterProps("row", 1)} />

            {/* === BOTTOM PANELS === */}
            <div
              className="bottom-panels"
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                height: "100%",
                width: "100%",
              }}
            >
              <div className="panel trade">
                <TradePanel />
              </div>
              <div className="panel risk">
                <RiskManager />
              </div>
            </div>
          </div>
        )}
      />
    </div>
  );
}
