# ============================================================
# 📊 chart_layout_panel.old.py — Phase 5.9.0 (Step 3C — Chart Interactivity Layer + Smoke Test)
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime

# ============================================================
# ⚙️ Mock Data (replace later with live data)
# ============================================================
def get_mock_data(symbol="NIFTY"):
    n = 120
    df = pd.DataFrame({
        "time": pd.date_range(datetime.date.today(), periods=n, freq="5min"),
        "open": np.random.randint(100, 120, n),
    })
    df["close"] = df["open"] + np.random.randint(-3, 3, n)
    df["high"] = df[["open", "close"]].max(axis=1) + np.random.randint(0, 3, n)
    df["low"] = df[["open", "close"]].min(axis=1) - np.random.randint(0, 3, n)
    return df

# ============================================================
# 🎨 Render Single Chart (Ultra-Thin Lines + Responsive Scaling)
# ============================================================
def render_chart(symbol="NIFTY", chart_type="Candle", scale_factor=0.95):
    df = get_mock_data(symbol)
    fig = go.Figure()

    # --- Chart Type ---
    if chart_type in ["Candle", "Heikin Ashi"]:
        fig.add_trace(go.Candlestick(
            x=df["time"], open=df["open"], high=df["high"],
            low=df["low"], close=df["close"],
            increasing_line_color="#16a34a", decreasing_line_color="#dc2626",
            name=symbol
        ))
    elif chart_type == "Line":
        fig.add_trace(go.Scatter(x=df["time"], y=df["close"], mode="lines",
                                 line=dict(width=1, color="#1e3a8a"), name=symbol))
    elif chart_type == "Area":
        fig.add_trace(go.Scatter(x=df["time"], y=df["close"], fill="tozeroy",
                                 line=dict(width=1, color="#3b82f6"), name=symbol))
    elif chart_type == "Point & Figure":
        fig.add_trace(go.Scatter(x=df["time"], y=df["close"], mode="markers+lines",
                                 marker=dict(size=6), name=symbol))

    # --- Ultra-Thin Global Trade Lines ---
    entry = np.mean(df["close"]) + 1
    stop = np.mean(df["close"]) - 2
    target = np.mean(df["close"]) + 4
    x_tail = df["time"].iloc[-40:]

    for y, color, label in [
        (entry, "rgba(22,163,74,0.9)", "ENTRY"),
        (stop, "rgba(220,38,38,0.9)", "STOP"),
        (target, "rgba(37,99,235,0.9)", "TARGET")
    ]:
        fig.add_trace(go.Scatter(
            x=x_tail, y=[y]*len(x_tail),
            mode="lines+text",
            text=[label]*len(x_tail),
            textposition="top right",
            hovertemplate=f"{label}<br>Price=%{{y:.2f}}<extra></extra>",
            line=dict(color=color, width=0.3, dash="5px,5px"),  # ultra-thin + soft dash
            name=label
        ))

    fig.update_layout(
        height=int(280 * scale_factor),
        margin=dict(l=10, r=10, t=10, b=20),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        hovermode="x unified",
        template="plotly_white",
        dragmode="pan"
    )
    return fig

# ============================================================
# 🧭 Render Chart Grid + Detach/Attach Logic + Smoke Test
# ============================================================
def render():
    st.markdown("""
        <style>
        .chart-grid {margin-top:110px;}
        .context-note {font-size:12px; color:#64748b; padding:2px 0 8px 0;}
        .floating-overlay {
            position:fixed; top:90px; left:50%; transform:translateX(-50%);
            width:80%; height:420px; background:white;
            border:2px solid #2563eb; border-radius:10px;
            z-index:9998; padding:6px;
            box-shadow:0 4px 12px rgba(0,0,0,0.25);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Layout Controls ---
    layout_mode = st.radio("🧩 Chart Layout", ["1-Chart", "2-Chart", "4-Chart"], horizontal=True)
    detach_chart = st.checkbox("🔓 Detach Chart (Float View)", value=False)

    # --- Responsive Scaling for Dashboard ---
    scale_factor = 0.95 if st.session_state.get("in_dashboard", True) else 1.0

    # --- Render Overlay (Detached Chart) ---
    if detach_chart:
        st.markdown("""
            <div class='floating-overlay'>
                <h5 style='text-align:center; color:#2563eb;'>📈 Detached Chart — NIFTY (Interactive Mode)</h5>
            </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(render_chart("NIFTY", scale_factor=1.0), use_container_width=True)
        st.info("✅ Detached chart floating overlay mode active.")
        return

    # --- Main Grid Render ---
    st.markdown("<div class='chart-grid'></div>", unsafe_allow_html=True)

    if layout_mode == "1-Chart":
        st.plotly_chart(render_chart("NIFTY", scale_factor=scale_factor), use_container_width=True)
    elif layout_mode == "2-Chart":
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(render_chart("NIFTY", scale_factor=scale_factor), use_container_width=True)
        with c2:
            st.plotly_chart(render_chart("BANKNIFTY", scale_factor=scale_factor), use_container_width=True)
    else:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(render_chart("NIFTY", scale_factor=scale_factor), use_container_width=True)
        with c2:
            st.plotly_chart(render_chart("BANKNIFTY", scale_factor=scale_factor), use_container_width=True)
        c3, c4 = st.columns(2)
        with c3:
            st.plotly_chart(render_chart("FINNIFTY", scale_factor=scale_factor), use_container_width=True)
        with c4:
            st.plotly_chart(render_chart("MIDCPNIFTY", scale_factor=scale_factor), use_container_width=True)

    # --- Smoke Test for Line Sharpness ---
    st.markdown("### 🧪 Line Sharpness Smoke Test")
    st.info("👉 Verify lines appear thin & crisp (not thick or blurry). If they look perfect — ✅ PASS.")

    st.markdown("""
        <div class='context-note'>
        ✅ Chart Interactivity Layer active — detachable chart + thin-line scale correction.  
        Ready for Step 4 (Right Sidebar + Trade Panel Integration).
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# 🧪 Smoke Test Run
# ============================================================
if __name__ == "__main__":
    st.set_page_config(page_title="Chart Interactivity Layer Test", layout="wide")
    st.session_state["in_dashboard"] = True
    render()
    st.caption("✅ Step 3C — Chart Interactivity Layer + Line Sharpness Smoke Test rendered successfully.")
