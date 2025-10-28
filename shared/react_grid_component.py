# ==============================================================
# 📄 FILE: shared/react_grid_component.py
# VERSION: v7.3.6 — Safe React Mount via Components (Final Fix)
# PURPOSE:
# Properly execute compiled React bundle inside Streamlit iframe
# ==============================================================

import os
import streamlit as st
import streamlit.components.v1 as components

def render_react_grid():
    """Embed React Grid from bundle.js correctly within Streamlit iframe."""
    bundle_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "System_2_TradingTerminal",
        "assets",
        "js",
        "dist",
        "bundle.js"
    )

    if not os.path.exists(bundle_path):
        st.error("❌ bundle.js not found at: " + bundle_path)
        return

    # Instead of loading JS inline, serve it as a base64 <iframe> HTML block
    with open(bundle_path, "r", encoding="utf-8") as f:
        bundle_code = f.read()

    html = f"""
    <html>
    <head>
        <meta charset="UTF-8" />
        <title>Trading Terminal React Grid</title>
        <style>
            html, body {{
                height: 100%;
                margin: 0;
                padding: 0;
                background: #0b0e12;
                overflow: hidden;
            }}
            #terminal-root {{
                height: 100vh;
                width: 100vw;
                background: #0b0e12;
            }}
        </style>
    </head>
    <body>
        <div id="terminal-root"></div>
        <script>
        {bundle_code}
        console.log("✅ React Grid initialized inside iframe");
        </script>
    </body>
    </html>
    """

    components.html(html, height=900, scrolling=False)
