// ============================================================================
// 📄 FILE: DynamicLayoutSkeleton.jsx — FINAL POLISHED 1:1 ALIGNMENT (Fixed Toolbar)
// ============================================================================

import React, { useState, useEffect } from "react";
import TopBarsSkeleton from "./TopBarsSkeleton";
import ChartGridSkeleton from "./ChartGridSkeleton";
import RightColumnSkeleton from "./RightColumnSkeleton";
import BottomPanelSkeleton from "./BottomPanelSkeleton";
import LeftToolbar from "./LeftToolbar";

export default function DynamicLayoutSkeleton() {
  const [layoutProfile, setLayoutProfile] = useState("Scalper");
  const [isLocked, setIsLocked] = useState(false);
  const [layoutConfig, setLayoutConfig] = useState({
    watchlistWidth: 28,
    bottomHeight: 150,
  });

  // ------------------ Load Saved Layout ------------------
  useEffect(() => {
    const saved = localStorage.getItem("trading_layout");
    if (saved) {
      const parsed = JSON.parse(saved);
      setLayoutProfile(parsed.profile || "Scalper");
      setLayoutConfig(parsed.layout || layoutConfig);
    }
  }, []);

  // ------------------ Save / Reset ------------------
  const saveLayout = () =>
    localStorage.setItem(
      "trading_layout",
      JSON.stringify({ profile: layoutProfile, layout: layoutConfig })
    );

  const resetLayout = () => {
    const defaults = {
      Scalper: { watchlistWidth: 28, bottomHeight: 150 },
      Swing: { watchlistWidth: 24, bottomHeight: 180 },
      Writer: { watchlistWidth: 30, bottomHeight: 160 },
    };
    setLayoutConfig(defaults[layoutProfile] || defaults.Scalper);
  };

  const handleProfileChange = (p) => {
    setLayoutProfile(p);
    resetLayout();
  };

  const gridTemplateColumns = `60px 1fr ${layoutConfig.watchlistWidth}%`;

  // ------------------ RENDER ------------------
  return (
    <div
      className="layout-root"
      style={{
        width: "100vw",
        height: "100vh",
        background: "#0c0c0c",
        overflow: "hidden",
      }}
    >
      {/* ---------- FIXED CONTROL BAR ---------- */}
      <div
        className="layout-controlbar"
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          width: "100%",
          height: 32,
          display: "flex",
          alignItems: "center",
          background: "#0f0f0f",
          borderBottom: "1px solid #222",
          padding: "4px 8px",
          gap: 8,
          fontSize: 12,
          zIndex: 100,
        }}
      >
        <button
          onClick={() => setIsLocked(!isLocked)}
          style={{
            background: isLocked ? "#333" : "#1a1a1a",
            color: isLocked ? "#aaa" : "#0ff",
            border: "1px solid #333",
            padding: "2px 6px",
            cursor: "pointer",
          }}
        >
          {isLocked ? "Locked 🔒" : "Unlocked 🔓"}
        </button>

        <select
          value={layoutProfile}
          onChange={(e) => handleProfileChange(e.target.value)}
          style={{
            background: "#1a1a1a",
            border: "1px solid #333",
            color: "#ccc",
            padding: "2px 6px",
          }}
        >
          <option value="Scalper">Scalper</option>
          <option value="Swing">Swing</option>
          <option value="Writer">Writer</option>
        </select>

        <button onClick={saveLayout}>💾 Save</button>
        <button onClick={resetLayout}>♻ Reset</button>

        <span style={{ marginLeft: "auto", color: "#777", fontStyle: "italic" }}>
          Layout Editable • {layoutProfile} Mode
        </span>
      </div>

      {/* ---------- MAIN BODY BELOW FIXED TOOLBAR ---------- */}
      <div
        className="layout-body"
        style={{
          display: "flex",
          flexDirection: "column",
          height: "100%",
          paddingTop: 32, // push below fixed toolbar
        }}
      >
        {/* HEADER (Top Bar + Tabs + Chart Toolbar) */}
        <div
          className="layout-header"
          style={{
            flex: "0 0 76px",
            borderBottom: "1px solid #222",
            background: "#101010",
            zIndex: 2,
          }}
        >
          <TopBarsSkeleton />
        </div>

        {/* MAIN GRID */}
        <div
          className="layout-main"
          style={{
            display: "grid",
            gridTemplateColumns,
            flex: 1,
            overflow: "hidden",
            height: "calc(100vh - 32px - 76px)", // subtract toolbar + header
          }}
        >
          {/* LEFT TOOLBAR */}
          <div className="left-sidebar" style={{ borderRight: "1px solid #222" }}>
            <LeftToolbar />
          </div>

          {/* CENTER CHART + BOTTOM */}
          <div
            className="center-column"
            style={{
              display: "flex",
              flexDirection: "column",
              overflow: "hidden",
              background: "#0c0c0c",
            }}
          >
            <div
              className="chart-section"
              style={{
                flex: 1,
                overflow: "hidden",
              }}
            >
              <ChartGridSkeleton />
            </div>

            <div
              className="bottom-section"
              style={{
                flex: "0 0 auto",
                height: layoutConfig.bottomHeight,
                borderTop: "1px solid #222",
                background: "#0d0d0d",
              }}
            >
              <BottomPanelSkeleton />
            </div>
          </div>

          {/* RIGHT WATCHLIST */}
          <div
            className="right-sidebar"
            style={{
              borderLeft: "1px solid #222",
              background: "#0d0d0d",
              overflowY: "auto",
            }}
          >
            <RightColumnSkeleton />
          </div>
        </div>
      </div>
    </div>
  );
}
