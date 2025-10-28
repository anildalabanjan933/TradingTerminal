// ============================================================================
// 💹 LAYOUT ENGINE — TradingView-Style Custom Drag/Resize Grid
// Handles live drag lines (vertical + horizontal), proportional auto-fill.
// ============================================================================

import React, { useState, useRef, useEffect } from "react";
import "./LayoutEngine.css";

const LayoutEngine = () => {
  const [leftWidth, setLeftWidth] = useState(240);     // sidebar width
  const [rightWidth, setRightWidth] = useState(300);   // watchlist width
  const [bottomHeight, setBottomHeight] = useState(160);
  const containerRef = useRef(null);
  const vLineRef = useRef(null);
  const hLineRef = useRef(null);
  const dragging = useRef(null);

  // --- Mouse Handlers ---
  const startDrag = (e, type) => {
    dragging.current = { type, startX: e.clientX, startY: e.clientY };
    document.body.style.cursor = type === "vertical" ? "ew-resize" : "ns-resize";
  };

  const onDrag = (e) => {
    if (!dragging.current) return;
    const { type, startX, startY } = dragging.current;
    if (type === "vertical") {
      const delta = e.clientX - startX;
      setRightWidth((prev) => Math.max(180, prev - delta));
      dragging.current.startX = e.clientX;
    } else if (type === "horizontal") {
      const delta = e.clientY - startY;
      setBottomHeight((prev) => Math.max(120, prev - delta));
      dragging.current.startY = e.clientY;
    }
  };

  const stopDrag = () => {
    dragging.current = null;
    document.body.style.cursor = "default";
  };

  useEffect(() => {
    window.addEventListener("mousemove", onDrag);
    window.addEventListener("mouseup", stopDrag);
    return () => {
      window.removeEventListener("mousemove", onDrag);
      window.removeEventListener("mouseup", stopDrag);
    };
  }, []);

  // --- Grid Template Setup ---
  const gridStyle = {
    gridTemplateRows: `32px 32px 32px 1fr ${bottomHeight}px`,
    gridTemplateColumns: `${leftWidth}px 1fr ${rightWidth}px`,
  };

  return (
    <div className="layout-engine" ref={containerRef} style={gridStyle}>
      {/* === TOP BARS === */}
      <div className="topbar panel">Top Bar</div>
      <div className="tabrow panel">Tab Row</div>
      <div className="toolbar panel">Chart Toolbar</div>

      {/* === MAIN GRID === */}
      <div className="panel" style={{ gridRow: "4 / 6", gridColumn: "1 / 2" }}>
        Sidebar
      </div>
      <div className="panel" style={{ gridRow: "4 / 6", gridColumn: "2 / 3" }}>
        Chart Area
      </div>
      <div className="panel" style={{ gridRow: "4 / 6", gridColumn: "3 / 4" }}>
        Right Stack (Watchlist + Scanner)
      </div>

      {/* === BOTTOM PANELS === */}
      <div className="panel" style={{ gridRow: "5 / 6", gridColumn: "1 / 3" }}>
        Trade Panel
      </div>
      <div className="panel" style={{ gridRow: "5 / 6", gridColumn: "3 / 4" }}>
        Risk Manager
      </div>

      {/* === DRAG LINES === */}
      <div
        className="drag-line vertical"
        ref={vLineRef}
        style={{ right: `${rightWidth}px` }}
        onMouseDown={(e) => startDrag(e, "vertical")}
      />
      <div
        className="drag-line horizontal"
        ref={hLineRef}
        style={{ bottom: `${bottomHeight}px` }}
        onMouseDown={(e) => startDrag(e, "horizontal")}
      />
    </div>
  );
};

export default LayoutEngine;
