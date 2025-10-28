// ======================================================================
// 🧩 APP.JSX — Phase 1.2 • Animated Sidebar Push + Arrow Toggle
// ======================================================================
import React, { useState, useEffect, useCallback } from "react";
import GridLayout from "react-grid-layout";
import { saveLayout, loadLayout, resetLayout } from "./stateManager";
import "react-grid-layout/css/styles.css";
import "react-resizable/css/styles.css";
import { createRoot } from "react-dom/client";

// ----------------------------------------------------------------------
// 🔹 Default 6×6 Layout
// ----------------------------------------------------------------------
const defaultLayout = [
  { i: "top_bar", x: 0, y: 0, w: 6, h: 1, static: true },
  { i: "tab_row", x: 0, y: 1, w: 6, h: 1, static: true },
  { i: "chart_toolbar", x: 0, y: 2, w: 6, h: 1, static: true },
  { i: "left_sidebar", x: 0, y: 3, w: 1, h: 3 },
  { i: "chart_area", x: 1, y: 3, w: 4, h: 3 },
  { i: "right_column", x: 5, y: 3, w: 1, h: 3 },
  { i: "bottom_drawer", x: 0, y: 6, w: 6, h: 1 },
];

const sectionNames = {
  top_bar: "Top Bar",
  tab_row: "Tab Row",
  chart_toolbar: "Chart Toolbar",
  left_sidebar: "Left Sidebar",
  chart_area: "Chart Area",
  right_column: "Right Column (Scanner + Watchlists)",
  bottom_drawer: "Trade + Risk Drawer",
};

// ----------------------------------------------------------------------
// 🔹 Main Component
// ----------------------------------------------------------------------
function App() {
  const [layout, setLayout] = useState(() => loadLayout() || defaultLayout);
  const [sidebarVisible, setSidebarVisible] = useState(true);
  const [viewport, setViewport] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  // 🧮 Row height
  const computeRowHeight = useCallback(() => Math.floor(viewport.height / 7), [viewport.height]);
  const [rowHeight, setRowHeight] = useState(computeRowHeight);

  useEffect(() => {
    const onResize = () => setViewport({ width: window.innerWidth, height: window.innerHeight });
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  useEffect(() => setRowHeight(computeRowHeight()), [viewport, computeRowHeight]);

  const handleLayoutChange = (newLayout) => {
    setLayout(newLayout);
    saveLayout(newLayout);
  };

  const handleReset = () => {
    resetLayout();
    setLayout(defaultLayout);
    setSidebarVisible(true);
  };

  // ------------------------------------------------------------------
  // 🧭 Sidebar toggle logic (animated shutter + push)
  // ------------------------------------------------------------------
  const toggleSidebar = () => {
    setSidebarVisible((prev) => !prev);
  };

  // ------------------------------------------------------------------
  // 🔹 UI Render
  // ------------------------------------------------------------------
  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        background: "#ffffff",
        color: "#000",
        fontFamily: "Inter, sans-serif",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: "8px 12px",
          color: "#000",
          fontSize: "14px",
          borderBottom: "1px solid #ccc",
          background: "#f9f9f9",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <div>
          💹 <b>Trading Terminal — Phase 1.2 Animated Sidebar + Push</b>
        </div>
        <div>
          <button
            onClick={handleReset}
            style={{
              background: "#007bff",
              color: "#fff",
              border: "none",
              padding: "4px 10px",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Reset Layout
          </button>
        </div>
      </div>

      {/* Main Container */}
      <div
        style={{
          position: "relative",
          width: "100%",
          height: "100%",
          display: "flex",
          transition: "all 0.4s ease-in-out",
        }}
      >
        {/* Animated Sidebar */}
        <div
          style={{
            width: sidebarVisible ? "16%" : "0",
            minWidth: sidebarVisible ? "200px" : "0",
            background: "#f4f4f4",
            borderRight: sidebarVisible ? "1px solid #ccc" : "none",
            overflow: "hidden",
            transition: "all 0.4s ease-in-out",
            boxShadow: sidebarVisible ? "2px 0 5px rgba(0,0,0,0.1)" : "none",
          }}
        >
          <div style={{ padding: "10px", textAlign: "center", fontWeight: 500 }}>
            📂 Sidebar
          </div>
        </div>

        {/* Chart + Right Column Grid */}
        <div
          style={{
            flexGrow: 1,
            transition: "all 0.4s ease-in-out",
            paddingLeft: sidebarVisible ? "0" : "0",
          }}
        >
          <GridLayout
            className="layout"
            layout={layout}
            cols={6}
            rowHeight={rowHeight}
            width={viewport.width}
            onLayoutChange={handleLayoutChange}
            draggableHandle=".drag-handle"
            margin={[4, 4]}
            containerPadding={[0, 0]}
          >
            {layout.map((item) => (
              <div
                key={item.i}
                style={{
                  background: item.static ? "#f1f1f1" : "#ffffff",
                  border: "1px solid #ddd",
                  borderRadius: "6px",
                  boxShadow: "0 2px 4px rgba(0,0,0,0.05)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "#333",
                  fontSize: "15px",
                  fontWeight: 500,
                  transition: "all 0.3s ease",
                }}
              >
                <span
                  className="drag-handle"
                  style={{
                    cursor: "move",
                    marginRight: "8px",
                    color: "#007bff",
                    fontWeight: "bold",
                  }}
                >
                  ⠿
                </span>
                {sectionNames[item.i] || item.i}
              </div>
            ))}
          </GridLayout>
        </div>

        {/* Toggle Arrow Button */}
        <button
          onClick={toggleSidebar}
          style={{
            position: "absolute",
            left: sidebarVisible ? "200px" : "0",
            top: "50%",
            transform: "translateY(-50%)",
            background: "#007bff",
            color: "#fff",
            border: "none",
            borderRadius: "0 6px 6px 0",
            padding: "6px 8px",
            cursor: "pointer",
            transition: "all 0.3s ease-in-out",
            zIndex: 10,
          }}
          title={sidebarVisible ? "Hide Sidebar" : "Show Sidebar"}
        >
          {sidebarVisible ? "◀" : "▶"}
        </button>
      </div>
    </div>
  );
}

// ----------------------------------------------------------------------
// 🔹 React 18 Root
// ----------------------------------------------------------------------
const root = createRoot(document.getElementById("react-frame-root"));
root.render(<App />);
