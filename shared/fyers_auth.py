"""
Phase 3.9.2 — FYERS API Connect (Auto Auth + Token Refresh)
============================================================
Handles complete Fyers V3 connection:
• Auto-login using TOTP + PIN
• Auto-generate & refresh access token
• Save tokens to data/fyers_env.json
• Provide authenticated Fyers client for all panels
"""

from fyers_apiv3 import fyersModel
import os, json, hashlib, pyotp, requests
from urllib import parse
import streamlit as st
from datetime import datetime

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
APP_ID = "5KPEU4DI4M"
APP_TYPE = "100"
CLIENT_ID = f"{APP_ID}-{APP_TYPE}"
SECRET_KEY = "PE25ZHXSGE"
PIN = "1979"
TOTP_SECRET_KEY = "KNCLVJTUDC6K74CQRR7EXSP56VBTE3EQ"
REDIRECT_URI = "https://trade.fyers.in/api-login/redirect-uri/index.html"

# URLs
BASE_URL = "https://api-t2.fyers.in/vagator/v2"
TOKEN_URL = "https://api-t1.fyers.in/api/v3/token"
VALIDATE_URL = "https://api-t1.fyers.in/api/v3/validate-authcode"

# Data file
DATA_PATH = os.path.join("Streamlit_TradingSystems", "System_2_TradingTerminal", "data", "fyers_env.json")


# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def _hash_app_secret() -> str:
    raw = f"{APP_ID}-{APP_TYPE}:{SECRET_KEY}"
    return hashlib.sha256(raw.encode()).hexdigest()


def _save_env(token: str):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump({
            "client_id": CLIENT_ID,
            "access_token": f"{CLIENT_ID}:{token}",
            "last_refresh": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }, f, indent=2)
    st.success("✅ Fyers access token saved successfully.")


# --------------------------------------------------
# LOGIN FLOW (AUTO)
# --------------------------------------------------
def get_auth_code() -> str:
    step1 = requests.post(f"{BASE_URL}/send_login_otp", json={"fy_id": "YA03116", "app_id": "2"}).json()
    key1 = step1.get("request_key")

    otp = pyotp.TOTP(TOTP_SECRET_KEY).now()
    step2 = requests.post(f"{BASE_URL}/verify_otp", json={"request_key": key1, "otp": otp}).json()
    key2 = step2.get("request_key")

    step3 = requests.post(f"{BASE_URL}/verify_pin", json={"request_key": key2, "identity_type": "pin", "identifier": PIN}).json()
    bearer = step3["data"]["access_token"]

    headers = {"Authorization": f"Bearer {bearer}"}
    payload = {
        "fyers_id": "YA03116",
        "app_id": APP_ID,
        "redirect_uri": REDIRECT_URI,
        "appType": APP_TYPE,
        "response_type": "code"
    }
    step4 = requests.post(TOKEN_URL, json=payload, headers=headers).json()
    url = step4.get("Url")
    return parse.parse_qs(parse.urlparse(url).query)['auth_code'][0]


def get_access_token(auth_code: str) -> str:
    payload = {"grant_type": "authorization_code", "appIdHash": _hash_app_secret(), "code": auth_code}
    resp = requests.post(VALIDATE_URL, json=payload).json()
    return resp.get("access_token")


def refresh_fyers_token():
    st.info("🔁 Refreshing Fyers token...")
    try:
        auth_code = get_auth_code()
        token = get_access_token(auth_code)
        _save_env(token)
        st.success("✅ Token refreshed successfully.")
        return token
    except Exception as e:
        st.error(f"❌ Fyers refresh failed: {e}")
        return None


# --------------------------------------------------
# LOAD FYERS CLIENT
# --------------------------------------------------
def get_fyers_client():
    """Return authenticated FyersModel instance."""
    if not os.path.exists(DATA_PATH):
        st.warning("⚠️ No access token found. Please login first.")
        return None

    with open(DATA_PATH, "r") as f:
        env = json.load(f)
    access_token = env.get("access_token")
    client_id = env.get("client_id", CLIENT_ID)

    try:
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path=".")
        return fyers
    except Exception as e:
        st.error(f"❌ Fyers client init failed: {e}")
        return None


# --------------------------------------------------
# STREAMLIT PANEL
# --------------------------------------------------
def render():
    st.subheader("🔐 FYERS API Connect (Phase 3.9.2)")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔁 Refresh Token"):
            refresh_fyers_token()
    with col2:
        if st.button("🧪 Test Connection"):
            fyers = get_fyers_client()
            if fyers:
                try:
                    res = fyers.quotes(data={"symbols": "NSE:NIFTY50-INDEX"})
                    st.json(res)
                except Exception as e:
                    st.error(e)
    with col3:
        if st.button("📁 View Token File"):
            if os.path.exists(DATA_PATH):
                st.code(open(DATA_PATH).read())
            else:
                st.info("No token file yet.")

    st.caption("Auto-refreshes token using TOTP + PIN | Saves to fyers_env.json | Used by all panels.")


# --------------------------------------------------
# STANDALONE TEST
# --------------------------------------------------
if __name__ == "__main__":
    st.set_page_config(page_title="FYERS Auth", layout="wide")
    render()
# --------------------------------------------------
# AUTO TOKEN STATUS CHECK
# --------------------------------------------------
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r") as f:
        env = json.load(f)
    if "access_token" in env and env["access_token"]:
        st.success("🟢 FYERS token detected and loaded.")
    else:
        st.warning("⚠️ No access token found. Please login first.")
else:
    st.warning("⚠️ Token file not found. Please login first.")
# ==============================================================
# ✅ SAFE UI WRAPPER (for Streamlit panels)
# ==============================================================
import streamlit as st

def render_fyers_auth():
    """
    Streamlit-safe FYERS auth section.
    Shows current token status and lets user trigger refresh or test connection
    without exposing secrets in the UI.
    """
    st.subheader("🔐 FYERS API Connect")
    token_path = "Streamlit_TradingSystems/System_2_TradingTerminal/data/fyers_env.json"

    # Status
    if os.path.exists(token_path):
        try:
            with open(token_path, "r") as f:
                env = json.load(f)
            if env.get("access_token"):
                st.success("🟢 FYERS token detected.")
            else:
                st.warning("⚠️ Token file empty. Please refresh.")
        except Exception as e:
            st.error(f"Cannot read token file: {e}")
    else:
        st.warning("⚠️ Token file not found. Please login first.")

    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Refresh Token"):
            st.info("Token refresh flow placeholder — handled in backend automation.")
    with col2:
        if st.button("🧪 Test Connection"):
            st.info("Connection test placeholder — full API bridge handled in backend.")

    st.caption("Auto-refresh handled internally using TOTP + PIN backend process.")
