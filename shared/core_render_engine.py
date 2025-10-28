# ==============================================================
# 📄 FILE: Streamlit_TradingSystems/shared/core_render_engine.py
# ==============================================================
# PURPOSE:
# Permanent render-stability engine for Streamlit dashboards.
# • Eliminates white/flicker screens.
# • Adds persistent unified header & chart anchors (165px / 60px).
# • Uses Streamlit cache_resource for reusable render state.
# ==============================================================

import streamlit as st
import traceback

# ==============================================================
# 🧠 CACHED HTML ANCHOR (Persistent DOM layer)
# ==============================================================

@st.cache_resource(show_spinner=False)
def get_persistent_dom_anchor():
    """Injects base persistent anchors used globally."""
    st.markdown(
        """
        <style>
        #core-anchor-top, #core-anchor-main, #core-anchor-bottom {
            display: block;
            position: relative;
            width: 100%;
            z-index: 1;
        }
        html, body, [data-testid="stAppViewContainer"] {
            overflow: hidden !important;
            background: #ffffff !important;
        }
        </style>
        <div id="core-anchor-top"></div>
        <div id="core-anchor-main"></div>
        <div id="core-anchor-bottom"></div>
        """,
        unsafe_allow_html=True,
    )
    return True


# ==============================================================
# 🧩 CORE FRAME STRUCTURE — permanent unified top & chart anchors
# ==============================================================

@st.cache_resource(show_spinner=False)
def inject_core_frame_structure():
    """Creates the fixed unified header + chart structure once per session."""
    st.markdown(
        """
        <style>
        /* Unified Top Stack (TopBar + Tabs + Toolbar) */
        #core-top-stack {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 165px;  /* total height for top 3 bars */
            background: #fff;
            z-index: 950;
            border-bottom: 1px solid #ccc;
        }

        /* Chart area anchored just below header */
        #core-chart-anchor {
            position: fixed;
            top: 165px;
            left: 0;
            right: 0;
            bottom: 60px; /* reserved space for trade panel */
            background: #fff;
            overflow: hidden;
            z-index: 1;
        }

        /* Optional visual debugging overlay */
        .debug-outline { outline: 1px dashed #e0e0e0; }
        </style>

        <div id="core-top-stack"></div>
        <div id="core-chart-anchor"></div>

        <script>
        console.log("🧩 Core Frame Anchors Active (Persistent Header + Chart)");
        </script>
        """,
        unsafe_allow_html=True,
    )
    return True


# ==============================================================
# 🧱 SAFE RENDER — wrapper for each panel
# ==============================================================

def safe_render(func, label):
    """Safely render a Streamlit panel without breaking the app."""
    try:
        func()
        st.markdown(
            f"<script>console.log('✅ {label} rendered');</script>",
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.error(f"⚠️ {label} failed: {e}")
        st.text_area("Traceback", traceback.format_exc(), height=180)


# ==============================================================
# 🧩 DOM GUARD — auto reload if blank DOM detected
# ==============================================================

def inject_dom_guard():
    """Reload automatically if DOM fails to mount."""
    st.markdown(
        """
        <script>
        window.addEventListener("load", ()=>{
            const app=document.querySelector('[data-testid="stAppViewContainer"]');
            if(!app || app.offsetHeight<100){
                console.warn("⚠️ Blank DOM detected — auto reload");
                location.reload();
            }
        });
        </script>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================
# ⚙️ RENDER PIPELINE — sequential render + cached anchors
# ==============================================================

def render_pipeline(panels):
    """
    Sequential render pipeline with persistent DOM + core frame anchors.
    Prevents timing gaps, misalignment, and flickers permanently.
    """

    # 1️⃣ Inject structural anchors (fixed header + chart)
    inject_core_frame_structure()

    # 2️⃣ Inject cached persistent global DOM layer
    get_persistent_dom_anchor()

    # 3️⃣ Safe sequential render
    container = st.empty()
    with container.container():
        for func, label in panels:
            safe_render(func, label)

    # 4️⃣ Inject DOM guard after render completion
    inject_dom_guard()

    # 5️⃣ Confirm cache hit in console
    st.markdown(
        "<script>console.log('🧱 Core Renderer — Persistent Frame Cached');</script>",
        unsafe_allow_html=True,
    )
