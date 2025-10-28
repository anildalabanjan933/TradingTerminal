// ===============================================================
// 📄 FILE: frontend/src/components/LayoutGrid.jsx
// 🔧 PURPOSE: Master 6×6 TradingView-style grid layout (0-gap, full-fit)
// ===============================================================

import React from "react";
import PanelWrapper from "./PanelWrapper";
import ResizeEngine from "./ResizeEngine";
import "./LayoutGrid.css";

const LayoutGrid = ({ panels }) => {
  return (
    <div className="tv-grid-root">
      {Object.keys(panels).map((key) => (
        <PanelWrapper key={key} id={key}>
          {panels[key]}
        </PanelWrapper>
      ))}
      <ResizeEngine />
    </div>
  );
};

export default LayoutGrid;
