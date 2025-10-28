// ============================================================================
// 📁 LEFT SIDEBAR — Phase 22.1 (Shutter Placement + Toggle)
// ============================================================================
// Collapsible side menu placeholder.  Includes vertical toggle button and
// dummy menu blocks (Fyers Connect, Layout, Settings) for spatial alignment.
// ============================================================================

import React, { useState } from "react";

export default function LeftSidebar() {
  const [open, setOpen] = useState(true);

  return (
    <div
      style={{
        height: "100%",
        display: "flex",
        flexDirection: "row",
      }}
    >
      {/* Toggle Button */}
      <div
        onClick={() => setOpen(!open)}
        style={{
          width: "26px",
          background: "#111317",
          color: "#33b249",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          cursor: "pointer",
          borderRight: "1px solid #2a2d31",
        }}
        title={open ? "Hide sidebar" : "Show sidebar"}
      >
        {open ? "«" : "»"}
      </div>

      {/* Sidebar Body */}
      <div
        style={{
          width: open ? "220px" : "0px",
          transition: "width 0.25s ease",
          overflow: "hidden",
          background: "#121416",
          borderRight: "1px solid #2a2d31",
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-start",
          padding: open ? "10px" : "0px",
          color: "#ddd",
          fontFamily: "Inter, sans-serif",
          fontSize: "14px",
        }}
      >
        <div style={{ fontWeight: 600, color: "#9be07e", marginBottom: "10px" }}>
          ⚙️ Terminal Controls
        </div>
        <div style={{ marginBottom: "6px" }}>Fyers Connect</div>
        <div style={{ marginBottom: "6px" }}>Layout Manager</div>
        <div style={{ marginBottom: "6px" }}>Alert Setup</div>
        <div style={{ marginBottom: "6px" }}>Color Settings</div>
        <div style={{ marginBottom: "6px" }}>General Settings</div>
        <div style={{ marginBottom: "6px" }}>Strategy & Help</div>
      </div>
    </div>
  );
}
