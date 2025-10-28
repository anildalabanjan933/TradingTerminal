// ============================================================================
// 📋 WATCHLIST PANEL — Phase 25.64
// Compact header + mock list items
// ============================================================================

import React from "react";
import "./PanelCommon.css";

export default function Watchlist() {
  const items = [
    { name: "NIFTY", change: "+0.45%" },
    { name: "BANKNIFTY", change: "-0.32%" },
    { name: "RELIANCE", change: "+0.55%" },
    { name: "INFY", change: "-0.21%" },
    { name: "TCS", change: "+0.43%" },
  ];

  return (
    <div className="panel-content watchlist">
      <div className="panel-header">📜 Watchlist</div>
      <div className="list-body">
        {items.map((i) => (
          <div key={i.name} className="list-row">
            <span>{i.name}</span>
            <span className={i.change.includes("+") ? "green" : "red"}>
              {i.change}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
