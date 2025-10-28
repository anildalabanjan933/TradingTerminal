// ============================================================================
// 📊 RIGHT STACK — Phase 22.2 (Dual Watchlist Placement)
// ============================================================================
// Splits right column into two panels: Watchlist 1 (top) and Watchlist 2 (bottom)
// Pure layout structure — visual alignment only (no data wiring yet).
// ============================================================================

import React from "react";
import Watchlist from "./Watchlist.jsx";

export default function RightStack() {
  return (
    <div
      style={{
        height: "100%",
        width: "100%",
        display: "flex",
        flexDirection: "column",
        gap: "6px",
      }}
    >
      {/* Watchlist 1 */}
      <div style={{ flex: 1 }}>
        <Watchlist />
      </div>

      {/* Watchlist 2 */}
      <div style={{ flex: 1 }}>
        <Watchlist />
      </div>
    </div>
  );
}
