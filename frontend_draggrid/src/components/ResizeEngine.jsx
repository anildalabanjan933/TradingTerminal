// ===============================================================
// 📄 FILE: frontend/src/components/ResizeEngine.jsx
// 🔧 PURPOSE: TradingView-style drag / resize snap-line logic
// ===============================================================

import React, { useEffect } from "react";

const ResizeEngine = () => {
  useEffect(() => {
    const grid = document.querySelector(".tv-grid-root");
    let line = null;

    const handleMove = (e) => {
      if (!line) {
        line = document.createElement("div");
        line.className = "tv-snap-line";
        grid.appendChild(line);
      }
      line.style.left = e.pageX + "px";
      line.style.height = "100%";
      line.style.top = 0;
    };

    const clearLine = () => {
      if (line) {
        line.remove();
        line = null;
      }
    };

    grid?.addEventListener("mousemove", handleMove);
    grid?.addEventListener("mouseleave", clearLine);
    return () => {
      grid?.removeEventListener("mousemove", handleMove);
      grid?.removeEventListener("mouseleave", clearLine);
    };
  }, []);

  return null;
};

export default ResizeEngine;
