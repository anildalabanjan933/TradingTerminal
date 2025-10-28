// ================================================================
// 📦 STATE MANAGER — Layout Save / Load / Reset (Phase 0.5)
// ================================================================

const STORAGE_KEY = "tt_draggrid_layout_v1";

/**
 * Save layout to localStorage
 * @param {Array} layout - Current grid layout
 */
export function saveLayout(layout) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(layout));
    console.log("💾 Layout saved →", layout);
  } catch (err) {
    console.error("❌ Save layout failed:", err);
  }
}

/**
 * Load layout from localStorage
 * @returns {Array|null}
 */
export function loadLayout() {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    if (!data) return null;
    const layout = JSON.parse(data);
    console.log("📦 Layout loaded →", layout);
    return layout;
  } catch (err) {
    console.error("❌ Load layout failed:", err);
    return null;
  }
}

/**
 * Reset layout to default
 */
export function resetLayout() {
  localStorage.removeItem(STORAGE_KEY);
  console.log("🧹 Layout reset → default applied");
}
