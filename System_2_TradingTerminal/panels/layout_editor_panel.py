# ==============================================================
# 📄 File: panels/layout_editor_panel.py
# 🔹 FULL LAYOUT EDITOR PANEL — GRID + STYLE + PRESET MANAGER (v3.4)
# ==============================================================

import streamlit as st
import json, os, time, random

# ✅ Fixed absolute path to shared layout_tokens.py
BASE_DIR = "D:/Streamlit_TradingSystems"
LAYOUT_FILE = os.path.join(BASE_DIR, "shared", "layout_tokens.py")

# ==============================================================
# 🧭 Path Debug Block
# ==============================================================
st.write("Current layout file path →", os.path.abspath(LAYOUT_FILE))

# ============================================================== #
# ⚙️ Load & Save Helpers
# ============================================================== #
def load_layout():
    if not os.path.exists(LAYOUT_FILE):
        return {}
    with open(LAYOUT_FILE, "r", encoding="utf-8") as f:
        text = f.read()
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except Exception:
        return {}

def save_layout(layout):
    os.makedirs(os.path.dirname(LAYOUT_FILE), exist_ok=True)
    with open(LAYOUT_FILE, "w", encoding="utf-8") as f:
        f.write("# Auto-generated layout tokens\n")
        f.write("LAYOUT = " + json.dumps(layout, indent=2)
                .replace("true", "True")
                .replace("false", "False"))
    st.success("💾 Layout saved successfully!")

# ============================================================== #
# 🧩 Layout Editor UI
# ============================================================== #
def render_layout_editor_panel():
    st.markdown("### 🧩 Layout Editor — Full Grid + Style Manager (v3.4)")
    st.caption("Adjust layout, style, and presets directly from the UI — no code edits.")

    layout = load_layout()
    if not layout:
        st.warning("No layout found — saving defaults on next save.")
        layout = {}

    panels = [
        "TopBar", "LeftSidebar",
        "Chart1", "Chart2", "Chart3", "Chart4",
        "Watchlist1", "Watchlist2", "AlertPanel", "RiskPanel",
        "Journal", "TradePanel", "WealthPanel",
        "SectorRotation", "ScannerPanel", "LayoutEditor", "BacktestTab"
    ]

    selected = st.selectbox("Select Panel", panels, key=f"panel_{time.time_ns()}")

    if selected not in layout:
        layout[selected] = {"row": 1, "col": 1, "row_span": 1, "col_span": 1}

    cfg = layout[selected]

    # ========================= POSITION =========================
    st.subheader("📐 Grid Controls")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        cfg["row"] = st.number_input("Row", 1, 6, cfg.get("row", 1), key=f"row_{time.time_ns()}")
    with c2:
        cfg["col"] = st.number_input("Column", 1, 6, cfg.get("col", 1), key=f"col_{time.time_ns()}")
    with c3:
        cfg["row_span"] = st.number_input("Row Span", 1, 6, cfg.get("row_span", 1), key=f"rowspan_{time.time_ns()}")
    with c4:
        cfg["col_span"] = st.number_input("Col Span", 1, 6, cfg.get("col_span", 1), key=f"colspan_{time.time_ns()}")

    # ========================= STYLE =========================
    st.subheader("🎨 Style Controls")
    c1, c2, c3 = st.columns(3)
    with c1:
        cfg["background"] = st.color_picker("Background", cfg.get("background", "#FFFFFF"), key=f"bg_{time.time_ns()}")
        cfg["border_color"] = st.color_picker("Border Color", cfg.get("border_color", "#E0E0E0"), key=f"border_{time.time_ns()}")
    with c2:
        cfg["radius"] = st.slider("Border Radius", 0, 20, cfg.get("radius", 8), key=f"radius_{time.time_ns()}")
        cfg["shadow"] = st.slider("Shadow", 0, 10, cfg.get("shadow", 4), key=f"shadow_{time.time_ns()}")
    with c3:
        cfg["padding"] = st.slider("Padding", 0, 20, cfg.get("padding", 6), key=f"padding_{time.time_ns()}")
        cfg["gap"] = st.slider("Gap", 0, 20, cfg.get("gap", 6), key=f"gap_{time.time_ns()}")

    # ========================= TEXT =========================
    st.subheader("🅰️ Text Controls")
    c1, c2, c3 = st.columns(3)
    with c1:
        cfg["font_family"] = st.selectbox("Font", ["Inter", "Roboto", "Open Sans", "Poppins"],
                                          index=0, key=f"font_{time.time_ns()}")
    with c2:
        cfg["font_size"] = st.number_input("Font Size (px)", 10, 24, cfg.get("font_size", 14), key=f"fontsize_{time.time_ns()}")
    with c3:
        cfg["text_color"] = st.color_picker("Text Color", cfg.get("text_color", "#000000"), key=f"textcolor_{time.time_ns()}")

    # ========================= HEADER =========================
    st.subheader("🧭 Header Controls")
    c1, c2, c3, c4 = st.columns(4)
    with c1: cfg["show_header"] = st.checkbox("Show Header", cfg.get("show_header", True), key=f"showhdr_{time.time_ns()}")
    with c2: cfg["header_height"] = st.slider("Header Height", 20, 80, cfg.get("header_height", 38), key=f"hdrh_{time.time_ns()}")
    with c3: cfg["divider"] = st.checkbox("Bottom Divider", cfg.get("divider", True), key=f"divider_{time.time_ns()}")
    with c4: cfg["sticky"] = st.checkbox("Sticky", cfg.get("sticky", True), key=f"sticky_{time.time_ns()}")

    # ========================= PANEL =========================
    st.subheader("🎛 Panel Controls")
    c1, c2, c3, c4 = st.columns(4)
    with c1: cfg["draggable"] = st.checkbox("Draggable", cfg.get("draggable", True), key=f"drag_{time.time_ns()}")
    with c2: cfg["lock_resize"] = st.checkbox("Lock Resize", cfg.get("lock_resize", False), key=f"lockresize_{time.time_ns()}")
    with c3: cfg["transparency"] = st.slider("Transparency %", 0, 100, cfg.get("transparency", 0), key=f"transp_{time.time_ns()}")
    with c4: cfg["z_index"] = st.number_input("Z-Index", 0, 50, cfg.get("z_index", 5), key=f"zidx_{time.time_ns()}")

    st.caption("✅ Fully no-code — adjust, preview, and save instantly to layout_tokens.py")

    # ========================= ACTIONS =========================
    st.subheader("💾 Actions")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("✅ Apply & Save", key=f"applysave_{time.time_ns()}"):
            layout[selected] = cfg
            save_layout(layout)
    with c2:
        if st.button("🔄 Reset Selected", key=f"resetselected_{time.time_ns()}"):
            layout[selected] = {"row": 1, "col": 1, "row_span": 1, "col_span": 1}
            save_layout(layout)
            st.experimental_rerun()
    with c3:
        if st.button("🧹 Reset All Panels", key=f"resetall_{time.time_ns()}"):
            layout = {}
            save_layout(layout)
            st.experimental_rerun()
    with c4:
        if st.button("📤 Export JSON", key=f"exportjson_{time.time_ns()}"):
            st.download_button("Download", json.dumps(layout, indent=2), "layout_full.json",
                               key=f"downloadjson_{time.time_ns()}")

    # ========================= PRESETS =========================
    st.subheader("🌐 Global Presets")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Compact View", key=f"preset_compact_{time.time_ns()}"):
            for k in layout:
                layout[k]["gap"] = 2
            save_layout(layout)
    with c2:
        if st.button("Research Mode", key=f"preset_research_{time.time_ns()}"):
            for k in layout:
                layout[k]["row_span"] = 3
            save_layout(layout)
    with c3:
        if st.button("Focus Mode", key=f"preset_focus_{time.time_ns()}"):
            for k in layout:
                layout[k]["col_span"] = 6
            save_layout(layout)

    # ========================= PREVIEW =========================
    st.subheader("👁️ Live Grid Preview")
    if st.checkbox("Show Grid Preview", value=True, key=f"show_grid_preview_{time.time_ns()}"):
        grid_html = ""
        for _ in range(6):
            grid_html += (
                "<div style='display:flex;gap:2px;margin-bottom:2px;'>"
                + "".join(
                    [
                        "<div style='flex:1;border:1px solid #ccc;height:24px;background:#f0f0f0;'></div>"
                        for _ in range(6)
                    ]
                )
                + "</div>"
            )
        st.markdown(grid_html, unsafe_allow_html=True)

    st.caption("✅ Fully no-code — adjust, preview, and save instantly to layout_tokens.py")

# ============================================================== #
# 🚀 MAIN
# ============================================================== #
if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Layout Editor v3.4")
    render_layout_editor_panel()
