# File: Streamlit_TradingSystems/shared/profile_manager.py
import json, os, io, datetime
import streamlit as st
from PIL import Image
from pathlib import Path

PROFILE_FILE = Path("Streamlit_TradingSystems/System_2_TradingTerminal/data/profile_store.json")
SNAPSHOT_DIR = Path("Streamlit_TradingSystems/System_2_TradingTerminal/snapshots")
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

def _load_profiles():
    if PROFILE_FILE.exists():
        try:
            return json.loads(PROFILE_FILE.read_text())
        except Exception:
            return {}
    return {}

def _save_profiles(data: dict):
    PROFILE_FILE.write_text(json.dumps(data, indent=2))

def save_current_profile(name: str, layout_tokens: dict, theme: dict, active_symbols: list):
    profiles = _load_profiles()
    profiles[name] = {
        "timestamp": datetime.datetime.now().isoformat(),
        "layout_tokens": layout_tokens,
        "theme": theme,
        "symbols": active_symbols
    }
    _save_profiles(profiles)
    st.toast(f"💾 Profile '{name}' saved successfully!")

def load_profile(name: str):
    profiles = _load_profiles()
    profile = profiles.get(name)
    if not profile:
        st.warning(f"Profile '{name}' not found.")
        return None
    st.toast(f"✅ Profile '{name}' loaded.")
    return profile

def list_profiles() -> list:
    return list(_load_profiles().keys())

def delete_profile(name: str):
    profiles = _load_profiles()
    if name in profiles:
        del profiles[name]
        _save_profiles(profiles)
        st.toast(f"🗑️ Deleted profile '{name}'")

def take_snapshot(layout_image_bytes: bytes = None):
    """Capture and save snapshot image (if provided) or blank placeholder."""
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = SNAPSHOT_DIR / f"snapshot_{ts}.png"
    if layout_image_bytes:
        Image.open(io.BytesIO(layout_image_bytes)).save(path)
    else:
        img = Image.new("RGB", (640, 360), color=(30, 30, 30))
        img.save(path)
    st.toast(f"📷 Snapshot saved → {path.name}")
    return path

def sidebar_ui():
    st.subheader("📁 Preset Profiles & Snapshots")
    col1, col2 = st.columns([3,1])
    with col1:
        selected = st.selectbox("Load Profile", ["(Select)"] + list_profiles())
    with col2:
        if st.button("Load"):
            if selected != "(Select)":
                load_profile(selected)
    name = st.text_input("Profile Name", "")
    if st.button("💾 Save Profile") and name:
        from Streamlit_TradingSystems.shared import layout_tokens
        save_current_profile(
            name=name,
            layout_tokens=layout_tokens.__dict__,
            theme={"mode": st.session_state.get("theme_mode", "dark")},
            active_symbols=st.session_state.get("active_symbols", [])
        )
    if st.button("🧹 Delete Profile") and name:
        delete_profile(name)
    if st.button("📸 Take Snapshot"):
        take_snapshot()

# Auto restore last used profile
def auto_restore_last():
    profiles = _load_profiles()
    if not profiles:
        return None
    last = sorted(profiles.items(), key=lambda x: x[1]["timestamp"], reverse=True)[0]
    return last[1]
