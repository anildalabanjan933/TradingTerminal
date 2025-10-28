# ==============================================================
# 🔒 CORE 1 — TOPBAR & TAB-ROW LOCK (v6.3.5)
# ==============================================================
# PURPOSE:
#   • Restore Top Bar visibility
#   • Remove duplicate Tab Row
#   • Close gap between Top Bar and Tabs
# ==============================================================

import streamlit as st

def apply_topbar_tab_lock():
    st.markdown(
        """
        <style>
        /* --- Ensure top bar visible and fixed --- */
        .top-stack {
            display:flex !important;
            flex-direction:column !important;
            margin:0 !important;
            padding:0 !important;
            width:100% !important;
            background:white !important;
            border-bottom:1px solid #ccc !important;
            z-index:999 !important;
        }

        /* --- Fuse Top Bar and Tab Row --- */
        [data-testid="stTabs"] {
            margin-top:0 !important;
            padding-top:0 !important;
            border-top:none !important;
        }

        /* --- Remove empty elements or phantom gaps --- */
        div:empty {
            display:none !important;
            height:0 !important;
            margin:0 !important;
            padding:0 !important;
        }

        /* --- Remove duplicate tab-lists --- */
        [data-baseweb="tab-list"]:not(:first-of-type) {
            display:none !important;
        }

        /* --- Hide “Active Workspace” lines --- */
        p:has(span:contains("Active Workspace")),
        p:contains("Active Workspace") {
            display:none !important;
        }

        /* --- Tighten spacing between top-stack and main area --- */
        section.main > div:first-child {
            margin-top:0 !important;
            padding-top:0 !important;
        }
        </style>

        <script>
        (function(){
            function cleanTopBar(){
                // remove any duplicate tab containers dynamically
                const tabs=document.querySelectorAll('[data-baseweb="tab-list"]');
                if(tabs.length>1){
                    for(let i=1;i<tabs.length;i++) tabs[i].remove();
                }
            }
            window.addEventListener("load", cleanTopBar);
            const obs=new MutationObserver(()=>cleanTopBar());
            obs.observe(document.body,{childList:true,subtree:true});
            console.log("✅ Core1: Top-Bar + Tab-Row Lock active");
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )
