# ============================================================
# 🎨 style_injector.py — Phase 4.3.1 UI Polish & Alignment Pass
# ============================================================

import streamlit as st

def inject_global_styles():
    """
    Injects polished CSS across the Trading Terminal UI.
    Enhances alignment, spacing, typography, and hover effects.
    """
    st.markdown("""
    <style>

    /* ======== GLOBAL LAYOUT RESET ======== */
    html, body, [class*="block-container"] {
        padding: 0 !important;
        margin: 0 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif !important;
        background-color: #f9fafb !important;
        color: #0f172a !important;
    }

    /* ======== HEADER / TOP BAR ======== */
    h3, h4, h5 {
        font-weight: 600 !important;
        letter-spacing: 0.2px !important;
        color: #0f172a !important;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background-color: #e0f2fe !important;
        color: #0369a1 !important;
        border-radius: 8px 8px 0 0 !important;
        font-weight: 600 !important;
    }
    .stTabs [role="tab"] {
        padding: 0.4rem 1rem !important;
        font-size: 14px !important;
        border-radius: 6px 6px 0 0 !important;
    }

    /* ======== SIDEBAR ======== */
    section[data-testid="stSidebar"] {
        background-color: #f1f5f9 !important;
        border-right: 1px solid #e2e8f0 !important;
        padding-top: 10px !important;
    }
    section[data-testid="stSidebar"] h2 {
        font-size: 15px !important;
        margin-bottom: 6px !important;
        font-weight: 600 !important;
        color: #0f172a !important;
    }
    section[data-testid="stSidebar"] button {
        margin-bottom: 6px !important;
    }

    /* ======== BUTTONS ======== */
    div[data-testid="stButton"] > button {
        border-radius: 8px !important;
        background: #0284c7 !important;
        color: #fff !important;
        border: none !important;
        padding: 0.45rem 0.9rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stButton"] > button:hover {
        background: #0369a1 !important;
        transform: translateY(-1px);
    }

    /* ======== GRID & PANEL ALIGNMENT ======== */
    #layout-grid {
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        background-color: #f8fafc !important;
    }
    .drag-panel {
        border-radius: 10px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08) !important;
        background: #fff !important;
        transition: all 0.25s ease-in-out !important;
    }
    .drag-panel:hover {
        box-shadow: 0 3px 10px rgba(0,0,0,0.12) !important;
        transform: translateY(-2px) !important;
    }

    /* ======== DIVIDERS & LINES ======== */
    hr {
        border-color: #e2e8f0 !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
    }

    /* ======== METRICS ======== */
    div[data-testid="stMetricValue"] {
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #0f172a !important;
    }

    /* ======== ALERT / INFO BOXES ======== */
    .stAlert > div {
        border-radius: 8px !important;
        padding: 0.6rem 0.9rem !important;
        font-size: 14px !important;
    }

    /* ======== SCROLLBAR ======== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background-color: rgba(0,0,0,0.2);
        border-radius: 8px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background-color: rgba(0,0,0,0.3);
    }

    /* ======== CHART AREA POLISH ======== */
    .element-container:has(canvas) {
        border-radius: 8px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }

    /* ======== MINI CHART / FOOTER ALIGN ======== */
    footer {
        visibility: hidden !important;
    }

    </style>
    """, unsafe_allow_html=True)
