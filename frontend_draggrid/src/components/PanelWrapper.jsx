// ===============================================================
// 📄 FILE: frontend/src/components/PanelWrapper.jsx
// 🔧 PURPOSE: Unified panel container with square edges + compact header
// ===============================================================

import React from "react";

const PanelWrapper = ({ id, title, children }) => {
  return (
    <div className="tv-panel" id={`panel-${id}`}>
      {title && <div className="tv-panel-title">{title}</div>}
      <div className="tv-panel-body">{children}</div>
    </div>
  );
};

export default PanelWrapper;
