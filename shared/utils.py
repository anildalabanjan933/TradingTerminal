# === shared/utils.py ===
import json, os, datetime, time, threading, shutil, gc, psutil
import streamlit as st

# ===============================================================
# ⚙️ UNIVERSAL UTILITY MODULE — Optimized for System 2 (Phase 5.1.0)
# ===============================================================

# ---------- JSON HANDLERS ----------
def read_json(path: str):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def write_json(path: str, data: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------- TIMESTAMP ----------
def timestamp(fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(fmt)

# ---------- LOCAL CACHE ----------
@st.cache_data(ttl=60)
def cached_read_json(path: str):
    return read_json(path)

@st.cache_data(ttl=10)
def cached_random_df(rows=10):
    import pandas as pd, numpy as np, random
    np.random.seed(42)
    return pd.DataFrame({
        "time": pd.date_range(datetime.datetime.now() - datetime.timedelta(minutes=rows),
                              periods=rows, freq="1min"),
        "price": [random.uniform(100, 200) for _ in range(rows)]
    })

# ---------- CACHE & MEMORY ----------
def clear_streamlit_cache():
    """Force clear Streamlit cache + trim memory."""
    st.cache_data.clear()
    gc.collect()
    log_event("Cache cleared manually.")

def log_performance(tag="Perf"):
    """Log CPU & RAM usage snapshot."""
    mem = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent(interval=0.1)
    log_event(f"[{tag}] Memory {mem:.1f}% | CPU {cpu:.1f}%")

# ---------- ASYNC REFRESH MOCK ----------
class AsyncRefresher:
    def __init__(self, interval_sec=5):
        self.interval = interval_sec
        self._data = None
        self._last_update = 0
        self._lock = threading.Lock()

    def _fetch(self):
        import random
        start = time.perf_counter()
        data = {"NIFTY": 22000 + random.randint(-50, 50), "timestamp": timestamp()}
        log_event(f"Async fetch in {(time.perf_counter()-start)*1000:.2f} ms")
        return data

    def get_data(self):
        with self._lock:
            now = time.time()
            if now - self._last_update > self.interval:
                self._data = self._fetch()
                self._last_update = now
            return self._data

# ---------- FILE OPS ----------
def safe_write(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def safe_read(path: str) -> str:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# ---------- MOCK FYERS FETCH ----------
def mock_fetch_symbol_data(symbol="NIFTY", points=30):
    import pandas as pd, numpy as np
    base = 22000
    close = np.cumsum(np.random.randn(points)) + base
    open_ = close + np.random.randn(points)
    high = close + abs(np.random.randn(points))
    low = close - abs(np.random.randn(points))
    vol = np.random.randint(1000, 5000, points)
    ts = pd.date_range(datetime.datetime.now() - datetime.timedelta(minutes=points),
                       periods=points, freq="1min")
    return pd.DataFrame({"time": ts, "open": open_, "high": high,
                         "low": low, "close": close, "volume": vol})

# ---------- SYSTEM LOGGER ----------
def log_event(msg, logfile="Streamlit_TradingSystems/System_2_TradingTerminal/logs/system_log.txt"):
    os.makedirs(os.path.dirname(logfile), exist_ok=True)
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp()}] {msg}\n")

# ===============================================================
# 🧩 Phase 4.9.5 — Auto-Backup + Recovery System
# ===============================================================
BACKUP_DIR = "Streamlit_TradingSystems/System_2_TradingTerminal/logs/backups"
TARGET_FILES = [
    "Streamlit_TradingSystems/shared/layout_presets.json",
    "Streamlit_TradingSystems/System_2_TradingTerminal/data/trade_journal.csv",
    "Streamlit_TradingSystems/System_2_TradingTerminal/data/wealth_data.json",
]

def create_backup():
    """Create timestamped backup of key files."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bundle = os.path.join(BACKUP_DIR, f"backup_{ts}")
    os.makedirs(bundle, exist_ok=True)
    for file in TARGET_FILES:
        if os.path.exists(file):
            shutil.copy(file, os.path.join(bundle, os.path.basename(file)))
    cleanup_old_backups()
    log_event(f"Auto-backup completed → {bundle}")
    return bundle

def cleanup_old_backups(keep_last=3):
    """Keep last N backup folders."""
    backups = sorted(
        [os.path.join(BACKUP_DIR, d) for d in os.listdir(BACKUP_DIR)],
        key=os.path.getmtime, reverse=True)
    for old in backups[keep_last:]:
        shutil.rmtree(old, ignore_errors=True)

def list_backups():
    if not os.path.exists(BACKUP_DIR):
        return []
    return sorted(os.listdir(BACKUP_DIR), reverse=True)

def restore_last_backup():
    """Restore the most recent backup."""
    backups = list_backups()
    if not backups:
        log_event("No backups found.")
        return False
    latest = os.path.join(BACKUP_DIR, backups[0])
    for file in os.listdir(latest):
        src = os.path.join(latest, file)
        dst = [t for t in TARGET_FILES if os.path.basename(t) == file]
        if dst:
            shutil.copy(src, dst[0])
    log_event(f"Backup restored from {latest}")
    return True

# ===============================================================
# 🚀 Phase 5.1.0 — Runtime Optimization Toolkit
# ===============================================================
def auto_optimize_runtime():
    """Clear cache, log perf stats, create quick backup."""
    clear_streamlit_cache()
    log_performance("AutoOptimize")
    create_backup()
    log_event("Runtime optimization cycle complete.")

# ---------- DEMO / SMOKE ----------
if __name__ == "__main__":
    print("✅ Utils optimized build ready.")
    log_performance()
    path = create_backup()
    print("Backup folder:", path)
    auto_optimize_runtime()
# ==============================================================
# 🧩 get_icon() — simple icon resolver for UI buttons
# ==============================================================

def get_icon(name: str) -> str:
    """
    Returns a small Unicode / emoji icon string used in the dashboard.
    Ensures consistent visuals across all panels.
    """
    icon_map = {
        "layout1": "🗔",
        "layout2": "🗖",
        "layout4": "🗗",
        "save": "💾",
        "reset": "♻️",
        "refresh": "🔁",
        "risk": "🧮",
        "chart": "📈",
        "scanner": "🔍",
        "settings": "⚙️",
        "alert": "🚨",
        "trade": "💹",
    }
    return icon_map.get(name.lower(), "⬜")
