# ==============================================================
# 📄 FILE: Streamlit_TradingSystems/shared/core_frame_guard.py
# ==============================================================
# PURPOSE:
# Prevent blank-screen issues and unsafe DOM access by delaying all
# JS injections (divider + animator) until Streamlit’s DOM is ready.
# Acts as a universal guard for Core UI Framework.
# ==============================================================

import streamlit as st
from streamlit.components.v1 import html

# ==============================================================
# 🧩 FUNCTION: init_core_frame_guard
# ==============================================================

def init_core_frame_guard():
    """Injects DOM-ready guard to ensure safe JS loading."""
    if "_frame_guard_active" in st.session_state:
        return
    st.session_state["_frame_guard_active"] = True

    css = """
    <style>
    .frame-guard-ready {
        opacity: 0;
        pointer-events: none;
        position: fixed;
        bottom: 0;
        right: 0;
        width: 1px;
        height: 1px;
    }
    </style>
    """

    js = """
    <script>
    (function(){
        if(window.__coreFrameGuardLoaded) return;
        window.__coreFrameGuardLoaded = true;
        console.log("[FrameGuard] Initializing safe DOM watcher...");

        function safeLog(msg){ console.log("[FrameGuard]", msg); }

        function waitForDOM(callback, retries=40){
            try{
                const doc = window.parent?.document || document;
                if(!doc){
                    if(retries>0) setTimeout(()=>waitForDOM(callback, retries-1), 250);
                    return;
                }
                const grid = doc.querySelector('.grid-container');
                const chart = doc.querySelector('.chart-area, .charts-area');
                if(grid && chart){
                    safeLog("DOM ready ✅");
                    callback(doc);
                } else if(retries>0){
                    setTimeout(()=>waitForDOM(callback, retries-1), 300);
                } else {
                    safeLog("⚠ Timeout waiting for DOM");
                }
            }catch(e){ console.warn("[FrameGuard] waitForDOM error:", e); }
        }

        waitForDOM(function(doc){
            try{
                const marker = doc.createElement('div');
                marker.className = 'frame-guard-ready';
                marker.id = 'frame-guard-marker';
                doc.body.appendChild(marker);

                const evt = new Event('core-frame-ready');
                doc.dispatchEvent(evt);
                safeLog("DOM ready event dispatched ✅");
            }catch(e){ console.warn("[FrameGuard] Injection failed:", e); }
        });
    })();
    </script>
    """

    html(css + js, height=0)
    print("✅ [core_frame_guard] Active — Safe DOM guard injected successfully.")


# ==============================================================
# 🔁 FUNCTION: guard_safe_call
# ==============================================================

def guard_safe_call(loader_func):
    """Safely executes visual initializers (e.g., animator/divider injectors)."""
    try:
        loader_func()
    except Exception as e:
        print(f"[core_frame_guard] ⚠ Suppressed runtime error: {e}")


# ==============================================================
# 🚀 AUTO-INITIALIZATION + SAFE LATE LOAD
# ==============================================================

try:
    init_core_frame_guard()
except Exception as e:
    print(f"[core_frame_guard] ❌ Initialization failed: {e}")

# 🧩 Safe Late Load Trigger (prevents blank screen)
try:
    from shared import core_frame_animator
    if "_anim_triggered" not in st.session_state:
        st.session_state["_anim_triggered"] = True
        core_frame_animator.init_core_frame_animator()
        print("✅ [core_frame_guard] Animator safely triggered after DOM ready.")
except Exception as e:
    print(f"[core_frame_guard] ⚠ Late load skip: {e}")
