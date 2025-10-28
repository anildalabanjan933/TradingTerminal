// ============================================================================
// 📄 FILE: ChartGridSkeleton.jsx
// PHASE 12 — FINAL VISUAL SMOKE TEST LOCK
// 1 : 1 Grid Layout + Toolbar Divider + Bottom Panel Edge Alignment
// ============================================================================

import React, { useEffect, useRef } from "react";
import "./base.css"; // base.css lives in same folder (confirmed)

export default function ChartGridSkeleton() {
  const gridRef = useRef(null);

  useEffect(() => {
    // Auto-fit grid height to fill space between top bars and bottom panels
    const handleResize = () => {
      if (!gridRef.current) return;

      // top-section = 76 px; bottom = 160 px; small safety margin (4 px)
      const topBars = 76;
      const bottomPanels = 160;
      const h = window.innerHeight - (topBars + bottomPanels + 4);
      gridRef.current.style.height = `${Math.max(h, 260)}px`;
    };

    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div ref={gridRef} className="chart-grid-wrapper">
      {/* Toolbar divider (thin line under toolbar) */}
      <div className="chart-toolbar-divider" />

      {/* 2×2 chart grid */}
      <div className="chart-grid">
        <div className="chart-cell" id="chart-a">Chart A</div>
        <div className="chart-cell" id="chart-b">Chart B</div>
        <div className="chart-cell" id="chart-c">Chart C</div>
        <div className="chart-cell" id="chart-d">Chart D</div>
      </div>
    </div>
  );
}
