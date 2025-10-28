# ==============================================================
# 📁 LEFT SIDEBAR PANEL — Stage 10.7 (Path Fix + Load Wrapper)
# ==============================================================

import streamlit as st
from shared.style_manager import apply_global_style

def render_left_sidebar():
    apply_global_style()

    st.markdown(
        """
        <style>
        /* Sidebar toggle button (☰) */
        .sidebar-toggle {
            position: fixed;
            top: 70px;
            left: 15px;
            background: #111;
            color: white;
            border-radius: 6px;
            border: none;
            padding: 6px 10px;
            cursor: pointer;
            z-index: 1100;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
        }

        /* Sidebar body placeholder */
        .sidebar-body {
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            width: 280px;
            background: #0d0d0d;
            color: white;
            padding: 60px 16px;
            transform: translateX(-100%);
            transition: transform 0.3s ease;
            z-index: 1000;
        }

        .sidebar-body.active {
            transform: translateX(0);
        }

        .sidebar-body h4 {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            margin-bottom: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Placeholder sidebar toggle + JS (will be functional in Stage 11.0)
    st.markdown(
        """
        <button class="sidebar-toggle" id="sidebarToggle">☰</button>
        <div class="sidebar-body" id="sidebarBody">
            <h4>Sidebar Placeholder</h4>
            <p>Stage 11.0 → will include Fyers Connect, Layout Manager, Settings</p>
        </div>

        <script>
        const toggle = window.parent.document.getElementById('sidebarToggle');
        const body = window.parent.document.getElementById('sidebarBody');
        if (toggle && body) {
            toggle.addEventListener('click', () => {
                body.classList.toggle('active');
            });
        }
        </script>
        """,
        unsafe_allow_html=True,
    )

# ✅ Load wrapper for dashboard import
def load():
    render_left_sidebar()
