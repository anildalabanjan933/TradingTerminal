import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";

// 🔄 Keep checking until Streamlit has injected <div id="react-frame-root">
function attachReactRoot() {
  const rootEl = document.getElementById("react-frame-root");

  if (rootEl) {
    try {
      const root = ReactDOM.createRoot(rootEl);
      root.render(<App />);
      console.log("✅ React successfully mounted on #react-frame-root");
    } catch (err) {
      console.error("❌ Mount failed:", err);
    }
  } else {
    // Retry every 500 ms until the element exists
    console.warn("⏳ Waiting for Streamlit to create #react-frame-root…");
    setTimeout(attachReactRoot, 500);
  }
}

attachReactRoot();
