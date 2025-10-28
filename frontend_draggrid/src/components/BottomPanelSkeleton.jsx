// ============================================================================
// 📄 FILE: BottomPanelSkeleton.jsx — Phase 26.1 (Perfect 50-50 alignment)
// ============================================================================
import React from "react";
import TradePanel from "./TradePanel";
import RiskManager from "./RiskManager";

export default function BottomPanelSkeleton() {
  return (
    <div
      className="bottom-panels"
      style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr", // equal halves
        height: "100%",
        background: "#0e0e0e",
        borderTop: "1px solid #222",
      }}
    >
      <div style={{ borderRight: "1px solid #222", overflow: "hidden" }}>
        <TradePanel />
      </div>
      <div style={{ overflow: "hidden" }}>
        <RiskManager />
      </div>
    </div>
  );
}
