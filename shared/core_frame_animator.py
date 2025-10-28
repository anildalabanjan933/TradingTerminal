# ==============================================================
# 📄 FILE: Streamlit_TradingSystems/shared/core_frame_animator.py
# ==============================================================
# PURPOSE:
# Adds smooth sidebar animation and drag-resize transitions.
# Works safely with core_layout_skeleton.py and core_frame_guard.py.
# ==============================================================

import streamlit as st
from streamlit.components.v1 import html
import uuid


# ==============================================================
# 🧩 FUNCTION: init_core_frame_animator
# ==============================================================

def init_core_frame_animator():
    """Injects global CSS + JS for sidebar and grid animation effects."""

    if "_anim_injected" in st.session_state:
        return
    st.session_state["_anim_injected"] = True

    uid = str(uuid.uuid4()).replace("-", "")

    css = """
    <style>
    /* Smooth transition for grid + sidebar */
    .grid-container, .chart-area, .right-column, .trade-panel {
        transition: all 0.3s ease-in-out !important;
    }

    .sidebar-placeholder {
        transition: transform 0.3s ease-in-out !important;
    }

    .sidebar-placeholder.closed {
        transform: translateX(-220px) !important;
    }

    .divider-line:hover {
        background: rgba(100,150,255,0.3) !important;
        cursor: col-resize;
    }
    </style>
    """

    # --------------------------------------------------------------
    # JS block (all braces escaped for f-string safety)
    # --------------------------------------------------------------
    js = """
    <script>
    (function() {
        if (window.__frameAnimatorLoaded) return;
        window.__frameAnimatorLoaded = true;

        const sidebar = parent.document.querySelector('.sidebar-placeholder');
        const grid = parent.document.querySelector('.grid-container');

        if (!sidebar || !grid) {
            console.log("[Animator] Sidebar or grid not found.");
            return;
        }

        // Sidebar toggle simulation for testing
        window.toggleSidebar = function() {
            sidebar.classList.toggle('closed');
        };

        // Reflow on resize (safe)
        window.addEventListener('resize', function() {
            try {
                if (grid) {
                    grid.style.width = '100%';
                    grid.style.height = '100vh';
                }
            } catch (e) {
                console.warn("[Animator] Resize error:", e);
            }
        });

        console.log("[Animator] Smooth animations active.");
    })();
    </script>
    """

    html(css + js, height=0)
    print(f"✅ [core_frame_animator] Smooth animation injected (ID: {uid})")
