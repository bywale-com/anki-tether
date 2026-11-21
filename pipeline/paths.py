from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "source-material"
DATA_DIR = ROOT / "pipeline-data"
UNITS_DIR = DATA_DIR / "units"
DRAFTS_DIR = DATA_DIR / "drafts"
REPORTS_DIR = DATA_DIR / "reports"
MANIFEST_PATH = DATA_DIR / "manifest.json"
QUEUE_PATH = DATA_DIR / "review_queue.json"


def ensure_dirs() -> None:
    for path in (DATA_DIR, UNITS_DIR, DRAFTS_DIR, REPORTS_DIR):
        path.mkdir(parents=True, exist_ok=True)
