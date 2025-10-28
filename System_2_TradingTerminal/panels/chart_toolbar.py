# ==============================================================================
# 📊 TRADING TERMINAL — CHART TOOLBAR (Stage 5.9 — Final Visual Lock)
# ==============================================================================
import streamlit as st
import streamlit.components.v1 as components

def render():
    """Render final, fully visible Chart Toolbar (aligned + on top)."""
    html_code = """
    <html>
    <head>
    <style>
    html, body {
        margin: 0;
        padding: 0;
        background: #0E1117;
        font-family: 'Montserrat', sans-serif;
        overflow: hidden;
    }
    .ctb-bar {
        position: fixed;
        top: 88px;  /* Below top bar + tab row */
        left: 0;
        right: 0;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 12px;
        background: #0E1117;
        border-top: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.08);
        z-index: 10000;  /* Ensure above iframe */
        box-shadow: 0 1px 2px rgba(0,0,0,0.4);
    }
    .ctb-section {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .ctb-group {
        display: flex;
        align-items: center;
        gap: 4px;
        background: rgba(255,255,255,0.03);
        border-radius: 6px;
        padding: 4px 6px;
    }
    .ctb-btn {
        height: 28px;
        line-height: 28px;
        padding: 0 10px;
        background: rgba(255,255,255,0.05);
        color: #EAEAEA;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 12.5px;
        transition: all .15s ease;
        white-space: nowrap;
    }
    .ctb-btn:hover {
        background: rgba(0,194,168,0.25);
        color: #00C2A8;
    }
    .ctb-input {
        height: 28px;
        padding: 0 8px;
        border-radius: 4px;
        border: 1px solid rgba(255,255,255,0.15);
        background: #141619;
        color: #EEE;
        width: 140px;
        font-size: 12.5px;
    }
    </style>
    </head>
    <body>
      <div class="ctb-bar">
        <div class="ctb-section">
            <input class="ctb-input" placeholder="🔍 Symbol..." />
            <div class="ctb-group">
                <button class="ctb-btn">1m</button><button class="ctb-btn">3m</button>
                <button class="ctb-btn">5m</button><button class="ctb-btn">15m</button>
                <button class="ctb-btn">30m</button><button class="ctb-btn">1h</button>
                <button class="ctb-btn">4h</button><button class="ctb-btn">1D</button>
                <button class="ctb-btn">1W</button>
            </div>
            <div class="ctb-group">
                <button class="ctb-btn">Candle</button><button class="ctb-btn">Heikin Ashi</button>
                <button class="ctb-btn">Line</button><button class="ctb-btn">Area</button>
                <button class="ctb-btn">P&amp;F</button>
            </div>
        </div>
        <div class="ctb-section">
            <div class="ctb-group">
                <button class="ctb-btn">📈</button><button class="ctb-btn">✏</button>
                <button class="ctb-btn">🔔</button><button class="ctb-btn">⚙</button>
            </div>
            <div class="ctb-group">
                <button class="ctb-btn">🗔 1</button><button class="ctb-btn">🗔 2</button><button class="ctb-btn">🗔 4</button>
            </div>
            <div class="ctb-group">
                <button class="ctb-btn">🔗 Sync ON</button>
                <button class="ctb-btn">🧠 HA Mode</button>
                <button class="ctb-btn">📉 Trail SL</button>
                <button class="ctb-btn">♻ Reset</button>
            </div>
        </div>
      </div>
    </body>
    </html>
    """

    # Render the toolbar with slightly more height for padding
    components.html(html_code, height=90, scrolling=False)
