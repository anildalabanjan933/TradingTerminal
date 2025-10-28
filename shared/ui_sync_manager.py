# ============================================================
# 📦 FILE: Streamlit_TradingSystems/shared/ui_sync_manager.py
# ============================================================
# PURPOSE:
# Handles JS ↔ Streamlit communication for:
# - Saving and restoring panel positions/sizes via localStorage
# - Syncing layout tokens between reloads
# - Maintaining layout persistence after refresh
# ============================================================

import json
import streamlit as st
from streamlit.components.v1 import html


# ============================================================
# 🔧  FUNCTION: inject_ui_sync_js
# ============================================================
def inject_ui_sync_js(sync_key="layout_state"):
    """
    Injects a JavaScript bridge that:
    1️⃣ Listens for layout changes from Streamlit (Python → JS)
    2️⃣ Saves them in browser localStorage
    3️⃣ Restores them automatically on reload
    """
    js_code = f"""
    <script>
    const SYNC_KEY = "{sync_key}";

    // === Load existing layout on startup ===
    window.addEventListener("load", () => {{
        const savedLayout = localStorage.getItem(SYNC_KEY);
        if (savedLayout) {{
            const parsed = JSON.parse(savedLayout);
            window.parent.postMessage({{ type: "load-layout", data: parsed }}, "*");
            console.log("📦 Loaded layout from localStorage:", parsed);
        }} else {{
            console.log("ℹ️ No saved layout found for key:", SYNC_KEY);
        }}
    }});

    // === Listen for save requests from Streamlit ===
    window.addEventListener("message", (event) => {{
        if (event.data && event.data.type === "save-layout") {{
            const newLayout = event.data.data;
            localStorage.setItem(SYNC_KEY, JSON.stringify(newLayout));
            console.log("💾 Layout saved to localStorage:", newLayout);
        }}
        if (event.data && event.data.type === "clear-layout") {{
            localStorage.removeItem(SYNC_KEY);
            console.log("🧹 Layout cleared from localStorage");
        }}
    }});
    </script>
    """
    html(js_code, height=0)


# ============================================================
# 🔧  FUNCTION: save_layout_state
# ============================================================
def save_layout_state(layout_dict, sync_key="layout_state"):
    """
    Sends layout dictionary to JS side for saving.
    layout_dict = {
        'chart_1': {'row':1,'col':1,'row_span':3,'col_span':3},
        'watchlist': {'row':1,'col':4,'row_span':3,'col_span':2},
        ...
    }
    """
    st.session_state["_last_layout_state"] = layout_dict
    html(
        f"""
        <script>
        window.parent.postMessage({{
            type: "save-layout",
            data: {json.dumps(layout_dict)}
        }}, "*");
        </script>
        """,
        height=0,
    )


# ============================================================
# 🔧  FUNCTION: clear_layout_state
# ============================================================
def clear_layout_state(sync_key="layout_state"):
    """Clears saved layout in browser localStorage."""
    html(
        f"""
        <script>
        window.parent.postMessage({{
            type: "clear-layout"
        }}, "*");
        </script>
        """,
        height=0,
    )


# ============================================================
# 🔧  FUNCTION: load_saved_layout
# ============================================================
def load_saved_layout(sync_key="layout_state"):
    """
    Retrieves last saved layout (from session_state or mock load).
    Used to restore layout immediately after reload.
    """
    return st.session_state.get("_last_layout_state", {})


# ============================================================
# 🧠  EXAMPLE USAGE (for reference)
# ============================================================
# from shared.ui_sync_manager import inject_ui_sync_js, save_layout_state, load_saved_layout
#
# inject_ui_sync_js()  # call once in dashboard.py
# current_layout = load_saved_layout()
# if user_drags_panel:
#     save_layout_state(current_layout)
#
# ============================================================
# ✅ END OF FILE
# ============================================================
