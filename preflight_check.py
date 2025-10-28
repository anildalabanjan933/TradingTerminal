# preflight_check.py
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent

REQUIRED_PATHS = [
    ROOT / "docs" / "master_spec.md",
    ROOT / "docs" / "build_plan.md",
    ROOT / "shared" / "layout_tokens.py",
    ROOT / "shared" / "utils.py",
    ROOT / "shared" / "logger.py",
    ROOT / "System_1_Nifty_OI" / "demo_data" / "sample.csv",
    ROOT / "demo_data_schema.txt",
]

def run_preflight():
    missing = []
    for p in REQUIRED_PATHS:
        if not p.exists():
            missing.append(str(p.relative_to(ROOT)))
    if missing:
        print("❌ Missing required files/folders:")
        for m in missing:
            print("   -", m)
        print("\nAction: create the missing files shown above and re-run `python preflight_check.py`.")
        sys.exit(1)
    print("✅ All required files exist. Project baseline ready.")

if __name__ == "__main__":
    run_preflight()
