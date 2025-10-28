# ==============================================================
# 📄 FILE: shared/dashboard_grid_engine.py
# 🔧 PURPOSE: 6×6 Grid Renderer + Drag/Resize Engine (Final Skeleton Alignment)
# ==============================================================

import streamlit as st
from streamlit.components.v1 import html
from shared.layout_tokens import TOKENS, LAYOUT_MAP, get_token

# --------------------------------------------------------------
# 🧱 Core Layout Renderer
# --------------------------------------------------------------
def render_grid(panels):
    """
    panels: dict -> {"panel_key": st.container(), ...}
    Renders full TradingView-style 0-gap skeleton
    """
    st.markdown("""
    <style>
        /* Root reset */
        html, body, [class*="stApp"] {
            margin:0 !important;
            padding:0 !important;
            background-color: %s !important;
            color:%s !important;
            font-weight:%s !important;
            font-family:%s !important;
        }

        /* Remove Streamlit padding/gaps */
        .block-container {
            padding:0 !important;
            margin:0 !important;
            width:100vw !important;
            max-width:100vw !important;
        }

        /* Panel base */
        .grid-panel {
            border:%spx solid %s;
            border-radius:%spx;
            box-sizing:border-box;
            overflow:hidden;
        }

        /* Compact panel titles */
        .panel-title {
            height:%spx;
            line-height:%spx;
            padding:0 6px;
            font-size:13px;
        }

        /* Top bars unified height */
        .topbar, .tabrow, .charttoolbar {
            height:%spx !important;
        }

        /* Smooth drag-line (same color as border) */
        .drag-line {
            position:absolute;
            background:%s;
            opacity:0.8;
            z-index:999;
        }

        /* Responsive zoom fit */
        @media (max-width:1920px) {
            body, .block-container { zoom:1.0; }
        }
        @media (max-width:1600px) {
            body, .block-container { zoom:0.9; }
        }
        @media (max-width:1366px) {
            body, .block-container { zoom:0.8; }
        }
    </style>
    """ % (
        TOKENS["background_color"],
        TOKENS["text_color"],
        TOKENS["font_weight"],
        TOKENS["font_family"],
        TOKENS["border_width"],
        TOKENS["border_color"],
        TOKENS["border_radius"],
        TOKENS["panel_title_height"],
        TOKENS["panel_title_height"],
        TOKENS["topbar_height"],
        TOKENS["border_color"],
    ), unsafe_allow_html=True)

    # Grid layout render using CSS grid (6×6)
    html("""
    <div id="grid-root" style="
        display:grid;
        grid-template-rows: repeat(6, 1fr);
        grid-template-columns: repeat(6, 1fr);
        gap:%spx;
        height:100vh;
        width:100vw;
        position:relative;">
    </div>
    """ % TOKENS["gap"])

# --------------------------------------------------------------
# 🧩 Drag & Resize Logic (Snap-line based)
# --------------------------------------------------------------
def enable_drag_resize():
    html(f"""
    <script>
        const grid = document.getElementById('grid-root');
        let activeLine = null;

        grid.addEventListener('mousemove', (e) => {{
            if (e.target.classList.contains('grid-panel')) {{
                // show snap line same color as border
                if(!activeLine){{
                    activeLine = document.createElement('div');
                    activeLine.className='drag-line';
                    activeLine.style.background='{TOKENS["border_color"]}';
                    grid.appendChild(activeLine);
                }}
                activeLine.style.width='2px';
                activeLine.style.height='100%';
                activeLine.style.left=e.pageX+'px';
                activeLine.style.top='0px';
            }}
        }});

        grid.addEventListener('mouseleave', ()=>{{
            if(activeLine){{ activeLine.remove(); activeLine=null; }}
        }});
    </script>
    """, height=0)
