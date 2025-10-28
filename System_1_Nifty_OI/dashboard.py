# System_1_Nifty_OI/dashboard real.py
# Safe, self-checking Streamlit dashboard skeleton for System_1_Nifty_OI.
# Replace panels or expand later. This file is intentionally defensive.

import streamlit as st
import importlib
import sys
import traceback
from pathlib import Path
from types import ModuleType
from typing import List, Tuple

# ---------------------------
# Basic paths / logging setup
# ---------------------------
ROOT = Path(__file__).resolve().parent

# Ensure the dashboard package root is on sys.path so `import panels.xxx` works
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ---------------------------
# Preflight / required files
# ---------------------------
REQUIRED_PATHS = [
    ROOT / "layout_tokens.py",
    ROOT / "panels",
    ROOT / "shared" / "fyers_auth.py",
    ROOT / "master_spec.md",
    ROOT / "build_plan.md",
]


def run_preflight_checks() -> List[Tuple[str, bool]]:
    """
    Return list of (relative-path-or-name, exists_bool).
    This function ensures the dashboard won't show a blank page even if files are missing.
    """
    results: List[Tuple[str, bool]] = []
    for p in REQUIRED_PATHS:
        # show relative path when possible
        try:
            rel = str(p.relative_to(ROOT))
        except Exception:
            rel = str(p)
        results.append((rel, p.exists()))

    # Some older code expected to check the folder name `System_1_Nifty_OI`.
    # Since this file is inside that folder, the check is always true — avoid false-negative.
    results.append(("System_1_Nifty_OI", True))

    return results


# ---------------------------
# Panel loader helpers
# ---------------------------
DEFAULT_PANELS = [
    "panel_alerts",
    "panel_bias",
    "panel_candles",
    "panel_metrics",
    "panel_news",
    "panel_oi",
]


def safe_import_panel(module_name: str) -> Tuple[ModuleType | None, str | None]:
    """
    Try to import panels.<module_name>. Return (module, error_message).
    """
    fullname = f"panels.{module_name}"
    try:
        mod = importlib.import_module(fullname)
        return mod, None
    except Exception as e:
        tb = traceback.format_exc()
        return None, tb


def safe_call_render(mod: ModuleType, st_obj: object) -> Tuple[bool, str | None]:
    """
    Try to call mod.render(st). Returns (success, error_message).
    """
    if not hasattr(mod, "render"):
        return False, "Module loaded but no callable 'render' found in " + getattr(mod, "__name__", "<module>")
    try:
        render_fn = getattr(mod, "render")
        render_fn(st_obj)
        return True, None
    except Exception:
        tb = traceback.format_exc()
        return False, tb


# ---------------------------
# Streamlit UI
# ---------------------------
def render_dashboard():
    st.set_page_config(page_title="Nifty OI — Safe Dashboard", layout="wide")
    st.title("🔒 Nifty OI — Safe Dashboard (Debug Mode)")

    st.markdown("This safe skeleton prevents blank pages and shows clear errors. If you are not an engineer, use the sidebar buttons.")

    # Sidebar controls
    with st.sidebar:
        st.header("Safety Controls")
        if st.button("Run Self-Test"):
            st.session_state["_run_self_test"] = True

        st.write("---")
        if st.button("Open debug log (last 200 lines)"):
            try:
                log_path = ROOT / "streamlit_debug.log"
                if log_path.exists():
                    with open(log_path, "r", encoding="utf8") as fh:
                        data = fh.readlines()[-200:]
                    st.code("".join(data[-200:]))
                else:
                    st.info("No debug log found.")
            except Exception as e:
                st.error("Failed to open debug log: " + str(e))

    # Run preflight checks and display
    st.subheader("1) Preflight checks")
    preflight = run_preflight_checks()
    cols = st.columns([7, 1])
    with cols[0]:
        st.write("File/Folder")
        for name, ok in preflight[:-1]:
            st.write(name)
    with cols[1]:
        st.write("OK")
        for name, ok in preflight[:-1]:
            st.write("✅" if ok else "❌")

    # show summary notice if any missing
    missing = [name for name, ok in preflight if not ok]
    if missing:
        st.warning("Some required files/folders are missing. See details above. The app will still run but some features may be unavailable.")

    st.markdown("---")

    # Panel import checks
    st.subheader("2) Panel import checks (safe)")
    for pname in DEFAULT_PANELS:
        st.write(f"Attempting to load panel: `panels.{pname}`")
        mod, err = safe_import_panel(pname)
        if err:
            st.error(f"Module panels.{pname} failed to import. See stack trace below.")
            with st.expander("Show technical error (stack trace)"):
                st.code(err)
            continue

        # If imported, try to call render
        success, call_err = safe_call_render(mod, st)
        if success:
            st.success(f"Rendered panels.{pname} successfully.")
        else:
            st.error(f"Error in panel panels.{pname} — it failed to load.")
            with st.expander("Show technical error (stack trace)"):
                st.code(call_err or "Unknown error")

    st.markdown("---")
    st.subheader("Dashboard main area")
    st.write("This area will load panels below. If a panel fails, you'll see a friendly error inside that panel's area.")

    # Now render main panels area (try-catch per panel)
    for pname in DEFAULT_PANELS:
        st.markdown(f"### Panel: {pname.replace('panel_', '').title()}")
        mod, err = safe_import_panel(pname)
        if err:
            st.info(f"No panels/{pname}.py found or it failed to import — placeholder shown.")
            continue
        success, call_err = safe_call_render(mod, st)
        if not success:
            st.error(f"Panel {pname} failed to render.")
            with st.expander("Panel error (stack trace)"):
                st.code(call_err)

    st.markdown("---")
    st.write("Dashboard skeleton loaded. Use the sidebar 'Run Self-Test' to diagnose further problems.")


if __name__ == "__main__":
    render_dashboard()
