import os, streamlit as st, streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🧭 React Trace Diagnostic")

bundle_path = os.path.join(
    os.path.dirname(__file__),
    "assets", "js", "dist", "bundle.js"
)
st.write("Bundle path:", bundle_path)
exists = os.path.exists(bundle_path)
st.write("Found:", exists)

if exists:
    with open(bundle_path, "r", encoding="utf-8") as f:
        js = f.read()

    html = f"""
    <html>
    <head>
        <style>html,body{{margin:0;height:100%;background:#111;color:#eee;}}</style>
    </head>
    <body>
        <div id="terminal-root"
             style="height:400px;width:100%;border:1px solid #555;background:#1e1e1e">
             <p>✅ HTML injected — waiting for React</p>
        </div>
        <script>
        console.log("📦 bundle start");
        try {{
            {js}
            console.log("✅ bundle executed");
        }} catch(e) {{
            console.error("🔥 bundle failed", e);
            const el=document.getElementById("terminal-root");
            el.innerHTML="<p style='color:red'>JS error: "+e.message+"</p>";
        }}
        </script>
    </body>
    </html>
    """
    components.html(html, height=600, scrolling=False)
else:
    st.error("bundle.js missing")
