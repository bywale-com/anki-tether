from __future__ import annotations

import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def _test_env(monkeypatch, tmp_path):
    monkeypatch.setenv("STUDY_USERNAME", "tester")
    monkeypatch.setenv("STUDY_PASSWORD", "secret")
    monkeypatch.setenv("SESSION_SECRET", "test-secret-not-for-prod")
    monkeypatch.setenv("IMPORT_TOKEN", "import-secret")
    monkeypatch.setenv("SECURE_COOKIES", "false")
    monkeypatch.setenv("ANKI_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("ANKI_COLLECTION", str(tmp_path / "data" / "collection.anki2"))
    monkeypatch.chdir(ROOT)
    # Reload config after env changes
    from app import config

    config.STUDY_USERNAME = "tester"
    config.STUDY_PASSWORD = "secret"
    config.SESSION_SECRET = "test-secret-not-for-prod"
    config.IMPORT_TOKEN = "import-secret"
    config.SECURE_COOKIES = False
    config.DATA_DIR = tmp_path / "data"
    config.COLLECTION_PATH = tmp_path / "data" / "collection.anki2"
    yield
