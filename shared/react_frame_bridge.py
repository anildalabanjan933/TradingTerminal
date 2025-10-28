import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# =============================================================
# 💹 TRADING TERMINAL — React Frame Bridge (Final Fullscreen Fix)
# =============================================================

def render_react_frame():
    """
    Renders the compiled React bundle inside Streamlit safely.
    Uses components.html() with dynamic height (100% viewport)
    to eliminate black bands once and for all.
    """

    root_dir = Path(__file__).resolve().parents[1]
    bundle_path = (
        root_dir
        / "System_2_TradingTerminal"
        / "assets"
        / "js"
        / "dist"
        / "bundle.js"
    )

    if not bundle_path.exists():
        st.error(f"⚠️ bundle.js not found at:\n{bundle_path}")
        return

    js_code = bundle_path.read_text(encoding="utf-8", errors="ignore")

    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <title>Trading Terminal Frame</title>
        <style>
          html, body {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background: #000;
            font-family: Arial, sans-serif;
          }}
          #react-frame-root {{
            width: 100%;
            height: 100%;
          }}
        </style>
      </head>
      <body>
        <div id="react-frame-root"></div>
        <script type="text/javascript">
          try {{
              console.log("✅ React bundle executing...");
              {js_code}
          }} catch (err) {{
              document.body.innerHTML =
                "<div style='color:white;text-align:center;margin-top:40vh'>❌ React frame load failed.</div>";
              console.error(err);
          }}
        </script>
      </body>
    </html>
    """

    # ✅ KEY FIX: Set height=window height (no cropping)
    components.html(html_code, height=0, scrolling=False)
    st.markdown(
        "<style>iframe {height:100vh!important;width:100vw!important;}</style>",
        unsafe_allow_html=True,
    )
