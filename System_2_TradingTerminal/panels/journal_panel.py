# ============================================================
# 📄 FILE: panels/journal_panel.py
# ============================================================
# Phase 4.9.2 — Journal ↔ Wealth Sync Automation (Mock Bridge)
# ============================================================
# PURPOSE:
# - Auto-log all trades with analytics + equity curve
# - Push each closed trade to session_state["portfolio"]
# - Used by wealth_creation_panel.py for live portfolio sync
# - Safe: no API or DB writes (local CSV + memory)
# ============================================================

import os, sys, datetime, pandas as pd, random, streamlit as st, plotly.graph_objects as go
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared import ui_sync_manager, fyers_auth

DATA_PATH = os.path.join(
    "Streamlit_TradingSystems", "System_2_TradingTerminal", "data", "trade_journal.csv"
)

# -------------------------------------------------------
# HELPERS
# -------------------------------------------------------
def load_journal():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame(
        columns=[
            "Time","Symbol","Side","Qty","Entry","Exit","P&L",
            "R:R","Mode","Notes","Emotion","Mistake","Growth"
        ]
    )

def save_journal(df: pd.DataFrame):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

# -------------------------------------------------------
# BRIDGE: Update portfolio in session_state
# -------------------------------------------------------
def update_portfolio_state(symbol, entry, exit_price, pnl, mode):
    """Push each logged trade to a mock portfolio DataFrame in session_state."""
    if "portfolio" not in st.session_state:
        st.session_state["portfolio"] = pd.DataFrame(
            columns=["Symbol","Entry","CMP","%Gain","Days","Mode","Bias","Note","Realized","Unrealized"]
        )

    df = st.session_state["portfolio"]
    cmp_val = exit_price if exit_price else entry
    gain_pct = round(((cmp_val - entry) / entry) * 100, 2)
    new = pd.DataFrame([{
        "Symbol": symbol,
        "Entry": entry,
        "CMP": cmp_val,
        "%Gain": gain_pct,
        "Days": random.randint(1, 20),
        "Mode": mode,
        "Bias": "Bullish" if pnl >= 0 else "Bearish",
        "Note": "Auto-sync from Journal",
        "Realized": pnl,
        "Unrealized": 0.0
    }])
    st.session_state["portfolio"] = pd.concat([df, new], ignore_index=True)
    st.session_state["portfolio"].drop_duplicates(subset=["Symbol","Entry"], keep="last", inplace=True)

# -------------------------------------------------------
# TRADE LOGGING
# -------------------------------------------------------
def log_trade(symbol, side, qty, entry, exit_price, pnl, rr, mode):
    df = load_journal()
    new = pd.DataFrame([{
        "Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Symbol": symbol,
        "Side": side,
        "Qty": qty,
        "Entry": entry,
        "Exit": exit_price,
        "P&L": pnl,
        "R:R": rr,
        "Mode": mode,
        "Notes": "",
        "Emotion": "",
        "Mistake": "",
        "Growth": ""
    }])
    df = pd.concat([df, new], ignore_index=True)
    save_journal(df)

    # --- Push to wealth bridge ---
    update_portfolio_state(symbol, entry, exit_price, pnl, mode)
    return df

# -------------------------------------------------------
# ANALYTICS
# -------------------------------------------------------
def render_equity_curve(df: pd.DataFrame):
    if df.empty:
        st.info("No trades logged yet.")
        return
    eq = df["P&L"].cumsum()
    fig = go.Figure([go.Scatter(y=eq, mode="lines+markers", name="Equity")])
    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6eef8")
    )
    st.plotly_chart(fig, use_container_width=True)

def render_summary(df: pd.DataFrame):
    if df.empty:
        st.info("No trades logged yet.")
        return
    total = len(df)
    wins = len(df[df["P&L"] > 0])
    losses = total - wins
    win_rate = (wins / total) * 100 if total else 0
    avg_rr = df["R:R"].mean() if total else 0
    st.markdown(
        f"📊 **Total Trades:** {total} | 🏆 **Win Rate:** {win_rate:.1f}% | ⚖️ **Avg R:R:** {avg_rr:.2f}"
    )

# -------------------------------------------------------
# DETAIL + NOTES
# -------------------------------------------------------
def render_detail(df: pd.DataFrame):
    if df.empty:
        return
    options = df["Symbol"] + " – " + df["Time"]
    trade = st.selectbox("Select Trade", list(reversed(options)))
    row = df.iloc[df.index[options == trade][0]]
    st.markdown(
        f"### 🧾 {row['Symbol']} | {row['Side']} | P&L ₹{row['P&L']:.2f}"
    )
    st.text_area("📝 Notes", value=row["Notes"], key="notes")
    st.selectbox("🎯 Emotion", ["","Calm","Fear","Greed","FOMO","Overconfidence"], key="emo")
    st.selectbox("💡 Mistake", ["","None","Late Entry","Early Exit","Impulse"], key="mist")
    st.selectbox("🚀 Growth", ["","Rule Followed","Improved SL","Better Timing"], key="growth")

# -------------------------------------------------------
# MAIN PANEL (JOURNAL TAB)
# -------------------------------------------------------
def render():
    # Initialize mock portfolio state if missing
    if "portfolio" not in st.session_state:
        st.session_state["portfolio"] = pd.DataFrame(
            columns=["Symbol","Entry","CMP","%Gain","Days","Mode","Bias","Note","Realized","Unrealized"]
        )

    fyers_auth.get_fyers_client()  # ensure auth state

    st.markdown("""
        <style>
        .journal-box{
            background:rgba(30,30,33,0.92);
            border-radius:12px;
            padding:16px 20px;
            color:#e8ecf2;
            font-family:'Inter',sans-serif;
        }
        .journal-title{
            font-size:20px;font-weight:600;
            padding-bottom:4px;color:#fff;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='journal-box'>", unsafe_allow_html=True)
    st.markdown("<div class='journal-title'>📘 Trade Journal — Analytics & Logs</div>", unsafe_allow_html=True)

    df = load_journal()
    tab1, tab2 = st.tabs(["📋 Journal Table", "📈 Analytics Dashboard"])

    with tab1:
        render_summary(df)
        st.dataframe(df, use_container_width=True, hide_index=True)
        render_detail(df)
        if st.button("🗑 Clear Journal (Reset)"):
            save_journal(pd.DataFrame(columns=df.columns))
            st.warning("Journal cleared.")
            st.session_state["portfolio"] = pd.DataFrame(columns=[
                "Symbol","Entry","CMP","%Gain","Days","Mode","Bias","Note","Realized","Unrealized"
            ])
            st.info("Linked wealth portfolio also cleared.")

    with tab2:
        render_equity_curve(df)
        render_summary(df)
        st.markdown("#### ➕ Add Mock Trade (Test only)")
        if st.button("➕ Add Sample Trade"):
            symbol = random.choice(["NIFTY","RELIANCE","HDFCBANK"])
            entry, exit_price = 100, 104
            pnl = (exit_price - entry) * 10
            df = log_trade(symbol, "Buy", 10, entry, exit_price, pnl, 2.0, "Paper")
            st.success(f"Added {symbol} trade → synced to Wealth panel")
            st.rerun()

    st.caption(f"Phase 4.9.2 | Journal ↔ Wealth Sync Bridge Active | {datetime.datetime.now().strftime('%H:%M:%S')}")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# LOCAL TEST
# -------------------------------------------------------
if __name__ == "__main__":
    st.set_page_config(page_title="Trade Journal (Bridge Mode)", layout="wide")
    render()
