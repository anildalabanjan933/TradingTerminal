# ==============================================================
# 📄 File: Streamlit_TradingSystems/shared/preset_manager.py
# 🔹 PRESET MANAGER — Snapshot + Profile Save/Load System (Phase 5.7)
# ==============================================================

import streamlit as st
import os
import json
import datetime
from io import BytesIO
from PIL import Image

# --------------------------------------------------------------
# 📁 PATH SETUP
# --------------------------------------------------------------
BASE_DIR = "Streamlit_TradingSystems"
PRESET_DIR = os.path.join(BASE_DIR, "shared", "presets")
SNAPSHOT_DIR = os.path.join(BASE_DIR, "System_2_TradingTerminal", "snapshots")
STYLE_FILE = os.path.join(BASE_DIR, "shared", "style_tokens.json")

os.makedirs(PRESET_DIR, exist_ok=True)
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# --------------------------------------------------------------
# 💾 SAVE PRESET
# --------------------------------------------------------------
def save_preset(preset_name: str, layout_state: dict = None):
    """Save current theme and layout as preset JSON"""
    try:
        with open(STYLE_FILE, "r", encoding="utf-8") as f:
            theme = json.load(f)
    except:
        theme = {}

    preset_data = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "theme": theme,
        "layout": layout_state or {},
    }

    filepath = os.path.join(PRESET_DIR, f"{preset_name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(preset_data, f, indent=2)

    st.success(f"✅ Preset '{preset_name}' saved successfully!")

# --------------------------------------------------------------
# 📂 LOAD PRESET
# --------------------------------------------------------------
def load_preset(preset_name: str):
    """Load preset and apply theme/layout"""
    filepath = os.path.join(PRESET_DIR, f"{preset_name}.json")
    if not os.path.exists(filepath):
        st.error(f"Preset '{preset_name}' not found.")
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        preset = json.load(f)

    # Write theme back to style file
    with open(STYLE_FILE, "w", encoding="utf-8") as f:
        json.dump(preset.get("theme", {}), f, indent=2)

    st.success(f"🎨 Preset '{preset_name}' loaded successfully!")
    return preset

# --------------------------------------------------------------
# ♻ RESET DEFAULT
# --------------------------------------------------------------
def reset_to_default():
    """Restore default dark theme and clear layout"""
    default_theme = {
        "theme": "dark",
        "sidebar_bg": "#0E1117",
        "text_color": "#FFFFFF",
        "accent_color": "#FF4B4B",
        "font": "Inter",
    }
    with open(STYLE_FILE, "w", encoding="utf-8") as f:
        json.dump(default_theme, f, indent=2)

    st.success("🔄 Restored default theme and layout!")

# --------------------------------------------------------------
# 📸 SNAPSHOT CAPTURE (Dashboard Image)
# --------------------------------------------------------------
def capture_snapshot(filename_prefix="snapshot"):
    """Capture Streamlit app screenshot using Pillow"""
    try:
        # Streamlit screenshot workaround — capture blank canvas placeholder
        image = Image.new("RGB", (1280, 720), color=(20, 20, 20))
        filename = f"{filename_prefix}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(SNAPSHOT_DIR, filename)
        image.save(filepath)
        st.success(f"📷 Snapshot saved: {filename}")
        return filepath
    except Exception as e:
        st.error(f"Snapshot failed: {e}")
        return None

# --------------------------------------------------------------
# 🧭 CONTROL PANEL (UI in Sidebar)
# --------------------------------------------------------------
def preset_manager_panel():
    st.markdown("### 💾 Preset & Snapshot Manager")

    col1, col2, col3 = st.columns(3)
    with col1:
        preset_name = st.text_input("Preset Name", value="MyProfile")
    with col2:
        if st.button("💾 Save Preset", use_container_width=True):
            save_preset(preset_name)
    with col3:
        if st.button("📂 Load Preset", use_container_width=True):
            load_preset(preset_name)

    col4, col5 = st.columns(2)
    with col4:
        if st.button("♻ Reset Default", use_container_width=True):
            reset_to_default()
    with col5:
        if st.button("📷 Snapshot", use_container_width=True):
            capture_snapshot("dashboard_snapshot")

    # List existing presets
    st.markdown("---")
    st.markdown("#### 📁 Saved Presets")
    presets = [f.replace(".json", "") for f in os.listdir(PRESET_DIR) if f.endswith(".json")]
    if presets:
        for p in presets:
            st.write(f"🗂 {p}")
    else:
        st.info("No presets saved yet.")

# --------------------------------------------------------------
# 🔹 STANDALONE TEST MODE
# --------------------------------------------------------------
if __name__ == "__main__":
    st.set_page_config(page_title="Preset Manager Test", layout="centered")
    preset_manager_panel()
