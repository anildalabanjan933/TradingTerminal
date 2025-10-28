import streamlit as st
import os

st.set_page_config(layout="wide", page_title="React Smoke Test")
st.write("🚀 React Smoke Test Starting...")

bundle_path = os.path.join(
    os.path.dirname(__file__),
    "assets",
    "js",
    "dist",
    "bundle.js"
)

st.write("Bundle path:", bundle_path)
if not os.path.exists(bundle_path):
    st.error("❌ bundle.js NOT FOUND — React can't mount.")
else:
    st.success("✅ bundle.js FOUND.")
    with open(bundle_path, "r", encoding="utf-8") as f:
        js_code = f.read(400)  # show start of file
    st.code(js_code)

st.markdown(
    """
    <div id="root" style="height:400px;width:100%;background:#1e1e1e;color:#ccc;">
    React injection test area
    </div>
    <script>
    console.log('🧩 Streamlit HTML loaded');
    </script>
    """,
    unsafe_allow_html=True
)
