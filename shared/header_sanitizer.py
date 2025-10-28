# ==============================================================
# 🧹 CORE 1 — HEADER SANITIZER (v6.3.4)
# ==============================================================
# PURPOSE:
#   • Remove duplicate tab containers (real-time)
#   • Fix residual top-bar gap permanently
# ==============================================================

import streamlit as st

def sanitize_headers():
    st.markdown(
        """
        <style>
        header, footer, [data-testid="stDecoration"],
        [data-testid="stHeader"], [data-testid="stToolbarActions"],
        [data-testid="stStatusWidget"], [data-testid="stSidebarNav"] {
            display:none!important;
        }

        html, body, [data-testid="stAppViewContainer"], section.main,
        .block-container {
            margin:0!important;
            padding:0!important;
            border:none!important;
            width:100%!important;
            max-width:100%!important;
            background:white!important;
        }

        [data-testid="stTabs"] {
            margin-top:0!important;
            padding-top:0!important;
        }

        [data-baseweb="tab-list"]:not(:first-of-type) {
            display:none!important;
        }

        p:has(span:contains("Active Workspace")),
        p:contains("Active Workspace") {
            display:none!important;
        }

        div:empty {
            display:none!important;
            height:0!important;
            margin:0!important;
            padding:0!important;
        }
        </style>

        <script>
        (function(){
            function cleanDupTabs(){
                document.querySelectorAll("div").forEach(el=>{
                    if(el.offsetHeight>0 && el.offsetHeight<120 &&
                       window.getComputedStyle(el).backgroundColor==="rgba(0, 0, 0, 0)" &&
                       el.children.length<=3){
                        if(el.nextElementSibling && el.nextElementSibling.innerHTML.includes("data-baseweb"))
                            el.remove();
                    }
                });
                let tabs=document.querySelectorAll('[data-baseweb="tab-list"]');
                if(tabs.length>1){
                    for(let i=1;i<tabs.length;i++) tabs[i].remove();
                }
            }
            window.addEventListener("load", cleanDupTabs);
            const root=document.body;
            const obs=new MutationObserver(()=>cleanDupTabs());
            obs.observe(root,{childList:true,subtree:true});
            console.log("✅ Core 1 observer active — removes top gaps & duplicate tabs in real time");
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )
