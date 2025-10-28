// =============================================================
// 📄 FILE: frontend_draggrid/DragGrid.jsx
// =============================================================
// PURPOSE:
// ✅ 6×6 TradingView-style grid with snap lines + sidebar push
// ✅ Smooth drag / resize with visual feedback
// ✅ Layout auto-saves to localStorage
// =============================================================

import React, { useState, useEffect } from "react";
import GridLayout from "react-grid-layout";
import "react-grid-layout/css/styles.css";
import "react-resizable/css/styles.css";

// -------------------------------------------------------------
// 🔹 Default grid layout
// -------------------------------------------------------------
const defaultLayout = [
  { i: "chart1", x: 0, y: 0, w: 2, h: 2 },
  { i: "chart2", x: 2, y: 0, w: 2, h: 2 },
  { i: "chart3", x: 0, y: 2, w: 2, h: 2 },
  { i: "chart4", x: 2, y: 2, w: 2, h: 2 },
  { i: "watch1", x: 4, y: 0, w: 2, h: 2 },
  { i: "watch2", x: 4, y: 2, w: 2, h: 2 },
];

// -------------------------------------------------------------
// 🔹 Utility to render snap lines overlay
// -------------------------------------------------------------
const SnapOverlay = ({ cols, rows }) => {
  const colLines = [];
  const rowLines = [];

  for (let i = 1; i < cols; i++) {
    colLines.push(
      <div
        key={`v-${i}`}
        style={{
          position: "absolute",
          top: 0,
          bottom: 0,
          left: `${(i / cols) * 100}%`,
          width: 1,
          background: "rgba(0,255,255,0.15)",
        }}
      />
    );
  }
  for (let i = 1; i < rows; i++) {
    rowLines.push(
      <div
        key={`h-${i}`}
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: `${(i / rows) * 100}%`,
          height: 1,
          background: "rgba(0,255,255,0.15)",
        }}
      />
    );
  }

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        pointerEvents: "none",
      }}
    >
      {colLines}
      {rowLines}
    </div>
  );
};

// -------------------------------------------------------------
// 🔹 MAIN GRID COMPONENT
// -------------------------------------------------------------
export default function DragGrid() {
  const [layout, setLayout] = useState(defaultLayout);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [containerWidth, setContainerWidth] = useState(1200);

  // 🧠 Load layout from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("grid_layout");
    if (saved) setLayout(JSON.parse(saved));
  }, []);

  // 💾 Save on change
  useEffect(() => {
    localStorage.setItem("grid_layout", JSON.stringify(layout));
  }, [layout]);

  // 🔀 Sidebar toggle (push behavior)
  const toggleSidebar = () => {
    const newWidth = sidebarOpen ? 1200 : 1000;
    setSidebarOpen(!sidebarOpen);
    setContainerWidth(newWidth);
  };

  return (
    <div
      style={{
        height: "100vh",
        background: "#000",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Toggle Sidebar Button */}
      <button
        onClick={toggleSidebar}
        style={{
          position: "absolute",
          top: 20,
          left: 20,
          zIndex: 10,
          background: sidebarOpen ? "#0ff" : "#222",
          color: "#0ff",
          border: "1px solid #0ff",
          borderRadius: "6px",
          padding: "4px 10px",
          cursor: "pointer",
          fontFamily: "Inter, sans-serif",
        }}
      >
        {sidebarOpen ? "← Hide Sidebar" : "☰ Show Sidebar"}
      </button>

      {/* Sidebar Panel (push mode) */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: sidebarOpen ? "200px" : "0px",
          height: "100%",
          background: "#111",
          borderRight: sidebarOpen ? "1px solid #0ff" : "none",
          transition: "width 0.3s ease",
          overflow: "hidden",
          zIndex: 5,
        }}
      >
        {sidebarOpen && (
          <div style={{ color: "#0ff", padding: 10, fontFamily: "Inter" }}>
            <h4>📊 Sidebar</h4>
            <p style={{ fontSize: "13px", opacity: 0.8 }}>
              This sidebar pushes grid smoothly.
            </p>
          </div>
        )}
      </div>

      {/* Main Grid Area */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: sidebarOpen ? 200 : 0,
          right: 0,
          bottom: 0,
          transition: "left 0.3s ease",
        }}
      >
        <GridLayout
          className="layout"
          layout={layout}
          cols={6}
          rowHeight={150}
          width={containerWidth}
          margin={[6, 6]}
          isDraggable
          isResizable
          compactType={null}
          onLayoutChange={(l) => setLayout(l)}
        >
          {layout.map((item) => (
            <div
              key={item.i}
              style={{
                background: "#111",
                border: "1px solid #0ff",
                borderRadius: "8px",
                color: "#0ff",
                fontFamily: "Inter, sans-serif",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                transition: "all 0.2s ease-in-out",
              }}
            >
              {item.i.toUpperCase()}
            </div>
          ))}
        </GridLayout>
        {/* Overlay Snap Lines */}
        <SnapOverlay cols={6} rows={4} />
      </div>
    </div>
  );
}
