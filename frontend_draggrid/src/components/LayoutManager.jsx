// ============================================================================
// 💹 LAYOUT MANAGER — Phase 25.69-A (Corrected Final Version)
//  ✅ No syntax errors
//  ✅ All four panels visible
//  ✅ Drag / Resize / Maximize
//  ✅ Compact top bars + dark theme
// ============================================================================

import React, { useEffect, useRef } from "react";
import { GoldenLayout } from "golden-layout";
import "golden-layout/dist/css/goldenlayout-base.css";
import "./layout.css";

import ChartArea from "./ChartArea";
import Watchlist from "./Watchlist";
import TradePanel from "./TradePanel";
import RiskManager from "./RiskManager";

export default function LayoutManager() {
  const containerRef = useRef(null);

  useEffect(() => {
    // ------------------------------------------------------------------------
    // 🧩 DEFAULT GOLDEN-LAYOUT CONFIG
    // ------------------------------------------------------------------------
    const config = {
      root: {
        type: "column",
        content: [
          {
            type: "row",
            height: 70,
            content: [
              {
                type: "component",
                width: 22,
                componentType: "Watchlist",
                title: "📜 Watchlist",
              },
              {
                type: "component",
                width: 78,
                componentType: "ChartArea",
                title: "📈 Chart Area",
              },
            ],
          },
          {
            type: "row",
            height: 30,
            content: [
              {
                type: "component",
                componentType: "TradePanel",
                title: "💹 Trade Panel",
              },
              {
                type: "component",
                componentType: "RiskManager",
                title: "🛡 Risk Manager",
              },
            ],
          },
        ],
      },
    }; // ✅ closed properly

    // ------------------------------------------------------------------------
    // 🚀 INITIALIZE GOLDEN LAYOUT (v2)
    // ------------------------------------------------------------------------
    const layout = new GoldenLayout(containerRef.current);

    // Register React Components
    layout.registerComponentConstructor("ChartArea", (container) => {
      container.element.appendChild(createNode(<ChartArea />));
    });
    layout.registerComponentConstructor("Watchlist", (container) => {
      container.element.appendChild(createNode(<Watchlist />));
    });
    layout.registerComponentConstructor("TradePanel", (container) => {
      container.element.appendChild(createNode(<TradePanel />));
    });
    layout.registerComponentConstructor("RiskManager", (container) => {
      container.element.appendChild(createNode(<RiskManager />));
    });

    // Load + refresh layout
    layout.clear();
    layout.loadLayout(config);
    layout.updateSize();

    const handleResize = () => layout.updateSize();
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      layout.destroy();
    };
  }, []);

  // --------------------------------------------------------------------------
  // 🧰 Helper — Convert React Element → DOM Node
  // --------------------------------------------------------------------------
  const createNode = (reactElement) => {
    const el = document.createElement("div");
    import("react-dom").then((ReactDOM) => {
      ReactDOM.render(reactElement, el);
    });
    return el;
  };

  // --------------------------------------------------------------------------
  // 🎨 Render Structure
  // --------------------------------------------------------------------------
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        width: "100vw",
        height: "100vh",
        background: "#0f1116",
      }}
    >
      {/* ===== TOP 3 FIXED BARS ===== */}
      <div className="topbar">🧭 Top Bar</div>
      <div className="tabrow">📁 Tab Row</div>
      <div className="toolbar">🛠 Chart Toolbar</div>

      {/* ===== MAIN LAYOUT AREA ===== */}
      <div
        ref={containerRef}
        id="golden-layout-root"
        style={{
          flexGrow: 1,
          background: "#0f1116",
        }}
      />
    </div>
  );
}
