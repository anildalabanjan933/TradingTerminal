// ============================================================================
// ⚙️ AUTO-FILL ENGINE — Phase 25.62
//  Computes responsive gridTemplate when sidebar / bottom panels hide or show.
// ============================================================================

import { useMemo } from "react";

export default function AutoFillEngine({ sidebarVisible, bottomVisible }) {
  const gridTemplate = useMemo(() => {
    const sidebarWidth = sidebarVisible ? "240px" : "0px";
    const rightWidth = "300px";
    const bottomHeight = bottomVisible ? "160px" : "0px";

    return {
      display: "grid",
      width: "100vw",
      height: "100vh",
      background: "#0f1116",
      gridTemplateAreas: `
        "topbar topbar topbar"
        "tabrow tabrow tabrow"
        "toolbar toolbar toolbar"
        "leftsidebar chart rightstack"
        "trade trade risk"
      `,
      gridTemplateRows: "32px 32px 32px 1fr " + bottomHeight,
      gridTemplateColumns: sidebarWidth + " 1fr " + rightWidth,
      transition: "all 0.25s ease",
    };
  }, [sidebarVisible, bottomVisible]);

  return { gridTemplate };
}
