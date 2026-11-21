from __future__ import annotations

import os
from pathlib import Path


def env(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name, default)
    if value is not None and value == "":
        return default
    return value


def require_env(name: str) -> str:
    value = env(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


DATA_DIR = Path(env("ANKI_DATA_DIR", str(Path("data").resolve())) or "data")
COLLECTION_PATH = Path(
    env("ANKI_COLLECTION", str(DATA_DIR / "collection.anki2")) or (DATA_DIR / "collection.anki2")
)
HOST = env("HOST", "127.0.0.1") or "127.0.0.1"
PORT = int(env("PORT", "8000") or "8000")
STUDY_USERNAME = env("STUDY_USERNAME", "")
STUDY_PASSWORD = env("STUDY_PASSWORD", "")
SESSION_SECRET = env("SESSION_SECRET", "dev-only-insecure-secret")
IMPORT_TOKEN = env("IMPORT_TOKEN", "")
PIPELINE_DATA_DIR = Path(env("PIPELINE_DATA_DIR", "pipeline-data") or "pipeline-data")
DEFAULT_DECK = env("DEFAULT_DECK", "COIS-1020") or "COIS-1020"
SECURE_COOKIES = env("SECURE_COOKIES", "true").lower() in {"1", "true", "yes"}


def auth_configured() -> bool:
    return bool(STUDY_USERNAME and STUDY_PASSWORD)
