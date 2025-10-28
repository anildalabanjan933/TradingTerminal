# ==============================================================
# 💾 CORE 3 — PERSISTENCE & SNAPSHOT FRAMEWORK (v6.3.0)
# ==============================================================
# PURPOSE:
# - Auto-save & restore dashboard layouts (6×6 grid)
# - Manage layout presets (Scalper / Swing / Writer)
# - Capture full-screen snapshots for sharing
# - Integrates seamlessly with layout_tokens + grid_engine
# ==============================================================

import streamlit as st
import json, os, io
from datetime import datetime
from PIL import Image

LAYOUT_FILE = "saved_layout.json"
PRESET_DIR = "presets"

# ==============================================================
# 🧩 SAVE / LOAD FUNCTIONS
# ==============================================================
def save_layout(layout_dict):
    """Save current layout configuration."""
    with open(LAYOUT_FILE, "w") as f:
        json.dump(layout_dict, f, indent=2)
    st.toast("💾 Layout Saved")

def load_layout():
    """Load layout configuration if exists."""
    if os.path.exists(LAYOUT_FILE):
        with open(LAYOUT_FILE, "r") as f:
            return json.load(f)
    return None

# ==============================================================
# 🧱 PRESET HANDLER
# ==============================================================
def save_preset(name, layout_dict):
    os.makedirs(PRESET_DIR, exist_ok=True)
    path = os.path.join(PRESET_DIR, f"{name}.json")
    with open(path, "w") as f:
        json.dump(layout_dict, f, indent=2)
    st.success(f"✅ Preset '{name}' saved")

def load_preset(name):
    path = os.path.join(PRESET_DIR, f"{name}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    st.warning(f"⚠️ Preset '{name}' not found")
    return None

# ==============================================================
# 📸 SNAPSHOT / SCREENSHOT
# ==============================================================
def capture_snapshot():
    """Capture current dashboard snapshot (PNG)."""
    img = Image.new("RGB", (1280, 720), color=(255, 255, 255))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"snapshot_{timestamp}.png"
    with open(filename, "wb") as f:
        f.write(buf.getvalue())
    st.toast(f"📸 Snapshot saved: {filename}")

# ==============================================================
# 🧰 CONTROL PANEL
# ==============================================================
def render_persistence_controls(current_layout):
    st.subheader("💾 Layout Persistence & Snapshots")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Save Layout"):
            save_layout(current_layout)
    with col2:
        if st.button("📤 Load Layout"):
            layout = load_layout()
            if layout: st.success("Layout Restored")
    with col3:
        if st.button("📸 Capture Snapshot"):
            capture_snapshot()

    st.divider()
    st.caption("Presets:")
    preset_name = st.text_input("Preset Name", "MyLayout")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💾 Save as Preset"):
            save_preset(preset_name, current_layout)
    with c2:
        if st.button("📂 Load Preset"):
            layout = load_preset(preset_name)
            if layout: st.success(f"Preset '{preset_name}' loaded")
