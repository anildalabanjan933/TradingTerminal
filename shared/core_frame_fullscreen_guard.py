# ==============================================================
# 📄 FILE: Streamlit_TradingSystems/shared/core_frame_master_guard.py
# ==============================================================
# PURPOSE:
# ⚡ Ultra-Fast Master Guard (v6.5.1-Final)
#   → True fullscreen (0px gap)
#   → Instant sidebar overlay
#   → Smooth drag dividers
#   → Zero load delay or flicker
# ==============================================================

import streamlit as st
from streamlit.components.v1 import html

def init_core_frame_master_guard():
    """Instant fullscreen + sidebar + drag without re-render delay."""
    html("""
    <style>
    html, body, #root, .stApp, .stMain, .block-container,
    [data-testid="stAppViewContainer"], [data-testid="stVerticalBlock"],
    [data-testid="stAppViewBlockContainer"] {
        margin:0!important; padding:0!important;
        height:100vh!important; width:100vw!important;
        max-width:100vw!important;
        overflow:hidden!important;
        background:#fff!important;
        position:fixed!important; top:0; left:0;
    }
    header, footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
        display:none!important;
    }
    ::-webkit-scrollbar{display:none!important;}

    /* Sidebar */
    .sidebar-placeholder{
        position:fixed; top:120px; left:0; bottom:0;
        width:220px; background:#f5f6f8;
        border-right:1px solid #ddd;
        transform:translateX(-220px);
        transition:transform .25s ease-in-out;
        z-index:50;
    }
    .sidebar-placeholder.open{transform:translateX(0);}

    /* Dividers */
    .divider-line{position:absolute;background:rgba(120,120,120,.25);
        z-index:9999;user-select:none;transition:background-color .2s ease;}
    .divider-line:hover{background:rgba(80,140,255,.4);}
    .divider-h{height:6px;left:0;right:0;cursor:row-resize;}
    .divider-v{width:6px;top:0;bottom:0;cursor:col-resize;}

    .fast-badge{
        position:fixed;bottom:6px;right:12px;
        font-size:10px;color:#111;
        background:rgba(0,255,0,.12);border-radius:4px;
        padding:3px 6px;z-index:9999;
    }
    </style>
    <script>
    (()=>{if(window.__UltraGuard)return;window.__UltraGuard=1;
      const d=document;const b=d.body;

      // Sidebar toggle
      const sidebar=d.querySelector('.sidebar-placeholder');
      if(sidebar){
         d.addEventListener('keydown',e=>{
            if(e.key==='Tab'){sidebar.classList.toggle('open');}
         });
      }

      // Chart dividers
      const chart=d.querySelector('.chart-area');
      const right=d.querySelector('.right-column');
      if(chart){
        const r=chart.getBoundingClientRect();
        const v=d.createElement('div');v.className='divider-line divider-v';
        const h=d.createElement('div');h.className='divider-line divider-h';
        v.style.left=r.width/2+'px';h.style.top=r.height/2+'px';
        chart.appendChild(v);chart.appendChild(h);
        let dragV=0,dragH=0;
        v.onmousedown=e=>{dragV=1;b.style.cursor='col-resize';};
        h.onmousedown=e=>{dragH=1;b.style.cursor='row-resize';};
        window.onmouseup=()=>{dragV=dragH=0;b.style.cursor='';};
        window.onmousemove=e=>{
          const rc=chart.getBoundingClientRect();
          if(dragV){const dx=e.clientX-rc.left;chart.style.gridTemplateColumns=`${dx}px 1fr`;v.style.left=dx+'px';}
          if(dragH){const dy=e.clientY-rc.top;chart.style.gridTemplateRows=`${dy}px 1fr`;h.style.top=dy+'px';}
        };
      }

      // Watchlist divider
      if(right){
        const rc=right.getBoundingClientRect();
        const wh=d.createElement('div');wh.className='divider-line divider-h';
        wh.style.top=rc.height/2+'px';right.appendChild(wh);
        let drag=0;wh.onmousedown=e=>{drag=1;b.style.cursor='row-resize';};
        window.onmouseup=()=>{drag=0;b.style.cursor='';};
        window.onmousemove=e=>{
          if(!drag)return;
          const diff=e.clientY-rc.top;
          right.style.gridTemplateRows=`${diff}px 1fr`;wh.style.top=diff+'px';
        };
      }

      // Badge
      const mark=d.createElement('div');
      mark.className='fast-badge';mark.textContent='Ultra-Fast Guard Active';
      b.appendChild(mark);
      console.log('[Ultra-Fast Guard] Fullscreen + Sidebar + Dividers ready ⚡');
    })();
    </script>
    """, height=0)
    print("✅ [core_frame_master_guard] Ultra-Fast fullscreen, sidebar, drag active.")
