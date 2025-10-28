# ============================================================
# 📄 FILE: panels/wealth_creation_panel.py
# ============================================================
# Phase 4.9.2 — Journal ↔ Wealth Sync Automation (Receiver)
# ============================================================
# PURPOSE:
# - Display portfolio synced from Journal (via session_state["portfolio"])
# - Auto-merge trades logged in Journal into Wealth table
# - Maintain local JSON backup (wealth_data.json)
# - Keep presets, snapshots, goal tracker, and tax summary
# ============================================================

import streamlit as st, pandas as pd, numpy as np, datetime, json, random, plotly.graph_objects as go
from pathlib import Path
from fpdf import FPDF

# ---------------------------------------------------------------
# 🔗 FILE PATHS
# ---------------------------------------------------------------
DATA_PATH = Path("Streamlit_TradingSystems/System_2_TradingTerminal/data/wealth_data.json")
PRESET_PATH = Path("Streamlit_TradingSystems/shared/wealth_presets.json")
SNAPSHOT_DIR = Path("Streamlit_TradingSystems/System_2_TradingTerminal/data/snapshots")

# ---------------------------------------------------------------
# 🔧 CORE HELPERS
# ---------------------------------------------------------------
def load_portfolio():
    if DATA_PATH.exists():
        return pd.read_json(DATA_PATH)
    return pd.DataFrame(columns=["Symbol","Entry","CMP","%Gain","Days","Mode","Bias","Note","Realized","Unrealized"])

def save_portfolio(df):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_json(DATA_PATH, indent=2, orient="records")

def update_cmp(df):
    df = df.copy()
    for i in df.index:
        move = random.uniform(-2, 2)
        df.loc[i, "CMP"] = round(df.loc[i, "CMP"] * (1 + move / 100), 2)
        df.loc[i, "%Gain"] = round((df.loc[i, "CMP"] - df.loc[i, "Entry"]) / df.loc[i, "Entry"] * 100, 2)
        df.loc[i, "Unrealized"] = round(df.loc[i, "%Gain"], 2)
    return df

# ---------------------------------------------------------------
# 🧩 BRIDGE: Merge Journal Trades
# ---------------------------------------------------------------
def merge_portfolio_with_session(df):
    """Merge any new Journal trades from session_state['portfolio'] into wealth view."""
    if "portfolio" in st.session_state and not st.session_state["portfolio"].empty:
        journal_df = st.session_state["portfolio"].copy()
        combined = pd.concat([df, journal_df], ignore_index=True)
        combined.drop_duplicates(subset=["Symbol","Entry"], keep="last", inplace=True)
        combined.reset_index(drop=True, inplace=True)
        save_portfolio(combined)
        return combined
    return df

# ---------------------------------------------------------------
# 💾 Preset System
# ---------------------------------------------------------------
def save_preset_profile(name, settings):
    PRESET_PATH.parent.mkdir(parents=True, exist_ok=True)
    presets = json.loads(PRESET_PATH.read_text()) if PRESET_PATH.exists() else {}
    presets[name] = settings
    PRESET_PATH.write_text(json.dumps(presets, indent=2))
    st.success(f"Preset '{name}' saved.")

def load_presets():
    if PRESET_PATH.exists():
        return json.loads(PRESET_PATH.read_text())
    return {}

# ---------------------------------------------------------------
# 📸 Snapshot Tool
# ---------------------------------------------------------------
def take_snapshot(df):
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_file = SNAPSHOT_DIR / f"snapshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Wealth Dashboard Snapshot", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(200, 10, f"Captured: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Portfolio Overview", ln=True)
    pdf.set_font("Arial", "", 10)
    for _, r in df.iterrows():
        pdf.cell(0, 8, f"{r['Symbol']} | CMP ₹{r['CMP']} | Gain {r['%Gain']}%", ln=True)
    pdf.output(str(snapshot_file))
    return snapshot_file

# ---------------------------------------------------------------
# 📊 Portfolio Summary
# ---------------------------------------------------------------
def render_portfolio_summary(df):
    st.subheader("📊 Portfolio Summary")
    if df.empty:
        st.info("No holdings yet.")
        return
    st.metric("Total Holdings", len(df))
    st.metric("Avg Gain (%)", round(df["%Gain"].mean(), 2))
    st.metric("Total Unrealized (%)", round(df["Unrealized"].sum(), 2))
    fig = go.Figure(go.Bar(
        x=df["Symbol"],
        y=df["Unrealized"],
        marker_color=np.where(df["Unrealized"] > 0, "limegreen", "red")
    ))
    fig.update_layout(template="plotly_dark", height=300, title="Unrealized Gains by Stock")
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------
# 🧾 Tax Summary
# ---------------------------------------------------------------
def compute_tax_summary(df):
    if df.empty:
        return pd.DataFrame(columns=["Type","Amount"])
    total_pnl = df["Realized"].sum() + df["Unrealized"].sum()
    brokerage = abs(total_pnl * 0.0003)
    stt = abs(total_pnl * 0.001)
    gst = brokerage * 0.18
    stamp = abs(total_pnl * 0.00002)
    net = total_pnl - (brokerage + stt + gst + stamp)
    return pd.DataFrame([
        ["Brokerage", brokerage],
        ["STT", stt],
        ["GST", gst],
        ["Stamp Duty", stamp],
        ["Net Profit After Tax", net]
    ], columns=["Type","Amount"]).round(2)

# ---------------------------------------------------------------
# ⚙️ Manual Tools
# ---------------------------------------------------------------
def manual_tools(df):
    st.subheader("⚙️ Manual Tools")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔄 Refresh CMP"):
            df = update_cmp(df); save_portfolio(df); st.success("CMP updated.")
    with c2:
        if st.button("💾 Backup Snapshot"):
            snap = take_snapshot(df)
            st.success(f"Snapshot saved: {snap.name}")
    with c3:
        if st.button("🧹 Reset Portfolio"):
            save_portfolio(pd.DataFrame(columns=df.columns))
            st.session_state["portfolio"] = pd.DataFrame(columns=df.columns)
            st.warning("Portfolio cleared (including linked journal).")
    return load_portfolio()

# ---------------------------------------------------------------
# 🎯 Goal Tracker
# ---------------------------------------------------------------
def render_goal_tracker(df, goal_value):
    st.subheader("🎯 Goal Tracker")
    progress = min(df["Unrealized"].sum() / goal_value * 100 if not df.empty else 0, 100)
    st.progress(progress / 100)
    st.caption(f"Progress: {progress:.1f}% of goal achieved.")
    if progress >= 100:
        st.success("🏁 Goal achieved! Congratulations!")
    elif progress >= 90:
        st.warning("⚠️ Nearing goal — consider partial booking!")

# ---------------------------------------------------------------
# 🧮 MAIN PANEL
# ---------------------------------------------------------------
def render_wealth_creation_panel():
    st.markdown("### 💼 Wealth Creation Dashboard — Phase 4.9.2 (Bridge Active)")

    # Load + Merge Journal trades
    df = load_portfolio()
    df = merge_portfolio_with_session(df)
    df = update_cmp(df)
    save_portfolio(df)

    tax_df = compute_tax_summary(df)

    # --- Preset Section ---
    st.markdown("#### 💾 Preset Profiles")
    presets = load_presets()
    cols = st.columns(3)
    with cols[0]:
        if presets:
            preset_sel = st.selectbox("Load Preset", list(presets.keys()))
            if st.button("🔁 Apply Preset"):
                p = presets[preset_sel]
                st.session_state["goal_value"] = p.get("goal", 50)
                st.success(f"Preset '{preset_sel}' applied.")
    with cols[1]:
        new_name = st.text_input("Preset Name", "MyProfile")
        if st.button("💾 Save Current as Preset"):
            current = {"goal": st.session_state.get("goal_value", 50)}
            save_preset_profile(new_name, current)
    with cols[2]:
        if st.button("📸 Take Snapshot Now"):
            snap = take_snapshot(df)
            st.success(f"Snapshot saved: {snap.name}")

    # --- Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Portfolio", "🎯 Goals", "🧾 Tax Summary", "📁 Snapshots"])
    with tab1:
        render_portfolio_summary(df)
        df = manual_tools(df)
    with tab2:
        goal_value = st.session_state.get("goal_value", 50)
        goal_value = st.number_input("Portfolio Growth Goal (%)", 10, 200, goal_value)
        st.session_state["goal_value"] = goal_value
        render_goal_tracker(df, goal_value)
    with tab3:
        st.subheader("🧾 Tax Breakdown")
        st.dataframe(tax_df, use_container_width=True)
    with tab4:
        st.subheader("📁 Saved Snapshots")
        if SNAPSHOT_DIR.exists():
            files = sorted(SNAPSHOT_DIR.glob("*.pdf"), reverse=True)
            for f in files[-5:]:
                st.write(f"📄 {f.name}")
        else:
            st.info("No snapshots yet.")

    # 🔒 Final Lock Notice
    st.markdown("---")
    st.caption("Linked with Journal via session_state['portfolio'] (Mock Bridge Active)")
    st.caption(f"📅 Last Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ---------------------------------------------------------------
# 🧪 Smoke Entry
# ---------------------------------------------------------------
if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Wealth Creation Dashboard (Bridge)")
    render_wealth_creation_panel()
