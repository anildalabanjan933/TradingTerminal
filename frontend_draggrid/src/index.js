// ===============================================================
// ✅ React Entry Point — index.js (Restored)
// ===============================================================

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css"; // Global styles (includes TopBar CSS etc.)

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
