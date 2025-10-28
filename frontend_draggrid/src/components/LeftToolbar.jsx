// ============================================================================
// 📄 FILE: LeftToolbar.jsx — Phase 26.1 Fix (Perfect vertical alignment)
// ============================================================================
import React from "react";

export default function LeftToolbar() {
  const tools = [
    "📊",
    "🔔",
    "📋",
    "🎯",
    "⚙️",
    "🧠",
    "❓",
  ];

  return (
    <div
      className="left-toolbar"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "space-between",
        height: "100%",
        padding: "8px 0",
        background: "#0e0e0e",
        borderRight: "1px solid #222",
      }}
    >
      <div
        className="toolbar-top"
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 10,
          alignItems: "center",
        }}
      >
        {tools.map((icon, idx) => (
          <div
            key={idx}
            style={{
              width: 40,
              height: 40,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#aaa",
              border: "1px solid #222",
              borderRadius: 6,
              cursor: "pointer",
            }}
          >
            {icon}
          </div>
        ))}
      </div>

      <div
        className="toolbar-footer"
        style={{
          fontSize: 10,
          color: "#555",
          textAlign: "center",
          paddingBottom: 6,
        }}
      >
        v1.0
      </div>
    </div>
  );
}
