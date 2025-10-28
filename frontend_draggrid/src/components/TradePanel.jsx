// ============================================================================
// 💰 TRADE PANEL — Phase 25.64
// Compact header + mock order buttons
// ============================================================================

import React from "react";
import "./PanelCommon.css";

export default function TradePanel() {
  return (
    <div className="panel-content trade-panel">
      <div className="panel-header">💹 Trade Panel</div>
      <div className="trade-body">
        <div className="order-row">
          <label>Symbol</label>
          <input type="text" placeholder="RELIANCE" />
        </div>
        <div className="order-row">
          <label>Qty</label>
          <input type="number" defaultValue={1} />
        </div>
        <div className="button-row">
          <button className="buy">BUY</button>
          <button className="sell">SELL</button>
          <button className="closeall">CLOSE ALL</button>
        </div>
      </div>
    </div>
  );
}
