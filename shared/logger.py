# shared/logger.py
# Simple file logger to capture debug info (safe & local).

import logging
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "streamlit_debug.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("StreamlitTradingSystems")

def get_logger():
    return logger
