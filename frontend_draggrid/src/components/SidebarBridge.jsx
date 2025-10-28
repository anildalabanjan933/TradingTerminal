// =============================================================
// 📄 FILE: frontend_draggrid/src/components/SidebarBridge.jsx
// =============================================================
// PURPOSE:
// Stage 6B — Two-way sync Streamlit ↔ React for sidebar state
// =============================================================

import React, { useState, useEffect } from "react";
import "../styles/sidebarBridge.css";

const SidebarBridge = () => {
  const [isOpen, setIsOpen] = useState(false);

  // --- 1️⃣ React listens for messages FROM Streamlit
  useEffect(() => {
    const listener = (event) => {
      if (!event.data || !event.data.type) return;

      if (event.data.type === "streamlit:set_sidebar_state") {
        setIsOpen(event.data.payload.open);
      }
    };
    window.addEventListener("message", listener);
    return () => window.removeEventListener("message", listener);
  }, []);

  // --- 2️⃣ Toggle and send message TO Streamlit
  const toggleSidebar = () => {
    const next = !isOpen;
    setIsOpen(next);
    window.parent.postMessage(
      {
        type: "streamlit:sidebar_state",
        payload: { open: next },
      },
      "*"
    );
  };

  return (
    <div className={`react-sidebar ${isOpen ? "open" : ""}`}>
      <div className="sidebar-header">
        <button className="toggle-btn" onClick={toggleSidebar}>
          {isOpen ? "⬅ Hide Sidebar" : "➡ Show Sidebar"}
        </button>
      </div>

      <div className="sidebar-content">
        <h4>📊 React ↔ Streamlit Bridge Active</h4>
        <p>Current State: {isOpen ? "Open ✅" : "Closed ❌"}</p>
        <p style={{ fontSize: "12px", color: "#555" }}>
          Toggle the button above — Streamlit receives updates instantly.
        </p>
      </div>
    </div>
  );
};

export default SidebarBridge;
