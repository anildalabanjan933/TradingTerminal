# ===============================================================
# 📄 FILE: panels/sector_rotation_panel.py
# ===============================================================
# Phase 4.9.3 — Sector Rotation ↔ Intraday Bridge
# ===============================================================
# PURPOSE:
# - One-click load symbol from Sector Rotation → Intraday Chart (Tab 1)
# - Bias, RSI, and TF sync both directions
# - Bridge log in session_state["bridge_sync"]
# ===============================================================

import streamlit as st, pandas as pd, numpy as np, random, datetime, time, json
import plotly.graph_objects as go
from pathlib import Path

LAYOUT_PATH = Path("Streamlit_TradingSystems/shared/layout_tokens.py")

# ---------------------------------------------------------------
# 🧮 Generate Mock Sector Data
# ---------------------------------------------------------------
def generate_mock_sector_data():
    sectors = [
        "NIFTY BANK", "NIFTY AUTO", "NIFTY IT",
        "NIFTY METAL", "NIFTY FMCG", "NIFTY PHARMA"
    ]
    data = []
    for s in sectors:
        sc = random.randint(0, 100)
        bias = (
            "Strong Bull" if sc >= 75 else
            "Bull" if sc >= 60 else
            "Neutral" if 45 <= sc <= 55 else
            "Bear" if sc >= 25 else "Strong Bear"
        )
        forecast = sc + random.randint(-10, 10)
        data.append({
            "Sector": s,
            "BiasScore": sc,
            "Bias": bias,
            "ForecastScore": max(0, min(100, forecast)),
            "Heat": round(random.uniform(-2, 2), 2)
        })
    return pd.DataFrame(data)

# ---------------------------------------------------------------
# 💾 Presets (save / load)
# ---------------------------------------------------------------
def save_preset(name, settings):
    p = LAYOUT_PATH.with_name("sector_presets.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(p.read_text()) if p.exists() else {}
    data[name] = settings
    p.write_text(json.dumps(data, indent=2))
    st.success(f"Preset '{name}' saved")

def load_presets():
    p = LAYOUT_PATH.with_name("sector_presets.json")
    return json.loads(p.read_text()) if p.exists() else {}

# ---------------------------------------------------------------
# 🔔 Detect Bias Changes + Bridge Sync
# ---------------------------------------------------------------
def detect_bias_changes(df):
    if "prev_bias" not in st.session_state:
        st.session_state["prev_bias"] = {r["Sector"]: r["Bias"] for _, r in df.iterrows()}
        return []
    prev = st.session_state["prev_bias"]
    changes = []
    for _, r in df.iterrows():
        s, b = r["Sector"], r["Bias"]
        if s in prev and prev[s] != b:
            changes.append((s, prev[s], b))
            prev[s] = b
    st.session_state["prev_bias"] = prev
    return changes

def bridge_sync(event_type, symbol, sector, bias, extra=None):
    if "bridge_sync" not in st.session_state:
        st.session_state["bridge_sync"] = []
    payload = {
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "type": event_type,
        "symbol": symbol,
        "sector": sector,
        "bias": bias,
        "extra": extra or {}
    }
    st.session_state["bridge_sync"].append(payload)
    return payload

# ---------------------------------------------------------------
# 🎨 Render Row and Dashboard
# ---------------------------------------------------------------
def render_sector_row(row):
    color = {
        "Strong Bull": "limegreen",
        "Bull": "green",
        "Neutral": "gray",
        "Bear": "orange",
        "Strong Bear": "red"
    }[row["Bias"]]
    st.markdown(
        f"**{row['Sector']}** — <span style='color:{color}'>{row['Bias']}</span> ({row['BiasScore']})",
        unsafe_allow_html=True
    )
    st.progress(row["BiasScore"] / 100)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📈 Open Chart", key=f"open_{row['Sector']}"):
            bridge_sync("open_chart", row["Sector"].split()[-1], row["Sector"], row["Bias"])
            st.success(f"Loaded → Intraday Chart : {row['Sector']}")
    with c2:
        if st.button("💼 Send to Wealth", key=f"wealth_{row['Sector']}"):
            bridge_sync("add_wealth", row["Sector"].split()[-1], row["Sector"], row["Bias"])
            st.info(f"Sent to Wealth Dashboard : {row['Sector']}")
    with c3:
        if st.button("🔔 Watch", key=f"watch_{row['Sector']}"):
            bridge_sync("set_alert", row["Sector"].split()[-1], row["Sector"], row["Bias"])
            st.warning(f"Alert created → {row['Sector']}")
    st.divider()

def render_forecast_dashboard(df):
    st.subheader("📊 Sector Forecast Dashboard")
    df["Δ"] = df["ForecastScore"] - df["BiasScore"]
    df["Direction"] = np.where(df["Δ"] > 0, "📈 Up", "📉 Down")
    st.dataframe(df[["Sector", "BiasScore", "ForecastScore", "Δ", "Direction"]],
                 use_container_width=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["Sector"], y=df["BiasScore"], name="Now", marker_color="gray"))
    fig.add_trace(go.Bar(x=df["Sector"], y=df["ForecastScore"], name="Forecast", marker_color="gold"))
    fig.update_layout(barmode="group", template="plotly_dark", height=300)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------
# 🧮 Main Panel
# ---------------------------------------------------------------
def render_sector_rotation_panel():
    st.markdown("### 📈 Sector Rotation ↔ Intraday Bridge (Phase 4.9.3)")

    # — Top Controls —
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    with c1: uni = st.selectbox("Universe", ["Nifty F&O", "Nifty 500", "Custom"])
    with c2: rsi = st.number_input("RSI Period", 5, 30, 14)
    with c3: tf = st.selectbox("Timeframe", ["3m", "5m", "10m", "15m", "30m", "1h", "Daily"], index=3)
    with c4: flt = st.selectbox("Filter", ["All", "Bullish Only", "Bearish Only", "Side (Alert Only)"])
    with c5: ref = st.selectbox("Auto-Refresh", ["Off", "5 s", "10 s", "30 s"], index=2)
    with c6:
        presets = load_presets(); names = list(presets.keys()) or ["None"]
        sel = st.selectbox("Load Preset", names)
        if st.button("💾 Save Preset"):
            save_preset("default", {"uni": uni, "rsi": rsi, "tf": tf, "flt": flt, "ref": ref})
        if sel != "None" and sel in presets:
            st.info(f"Loaded Preset → {sel}")
    with c7:
        if st.button("📷 Export CSV"):
            csv = generate_mock_sector_data().to_csv(index=False)
            st.download_button("Download CSV", data=csv, file_name="sector_snapshot.csv")

    st.divider()

    # — Auto Refresh —
    if ref != "Off":
        sec = int(ref.split()[0])
        if "last_refresh" not in st.session_state or time.time() - st.session_state["last_refresh"] > sec:
            st.session_state["last_refresh"] = time.time()
            st.session_state["data"] = generate_mock_sector_data()
    df = st.session_state.get("data", generate_mock_sector_data())

    # — Bias Changes —
    for s, old, new in detect_bias_changes(df):
        st.warning(f"Bias flip → {s}: {old} → {new}")
        bridge_sync("bias_flip", s, s, new)

    # — Filter —
    if flt == "Bullish Only":
        df = df[df["Bias"].str.contains("Bull")]
    elif flt == "Bearish Only":
        df = df[df["Bias"].str.contains("Bear")]
    elif "Side" in flt:
        df = df[df["Bias"] == "Neutral"]

    # — Render Dashboard + Rows —
    render_forecast_dashboard(df)
    for _, r in df.iterrows():
        render_sector_row(r)

    # — Bridge Log —
    st.markdown("#### 🔗 Bridge Sync Log (Intraday ↔ Sector ↔ Wealth)")
    log = st.session_state.get("bridge_sync", [])
    if not log:
        st.info("No bridge events yet.")
    else:
        for ev in log[-10:]:
            st.write(f"{ev['time']} | {ev['type']} → {ev['sector']} ({ev['bias']})")

    st.caption(f"⏱ {datetime.datetime.now().strftime('%H:%M:%S')} | {uni} | RSI {rsi}")

# ---------------------------------------------------------------
# 🧪 Smoke Entry
# ---------------------------------------------------------------
if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Sector Rotation ↔ Intraday Bridge")
    render_sector_rotation_panel()
