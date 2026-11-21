from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pipeline.paths import DRAFTS_DIR, MANIFEST_PATH, QUEUE_PATH, UNITS_DIR, ensure_dirs


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_manifest() -> dict[str, Any]:
    ensure_dirs()
    return read_json(MANIFEST_PATH, {"files": {}})


def save_manifest(manifest: dict[str, Any]) -> None:
    write_json(MANIFEST_PATH, manifest)


def unit_path(unit_id: str) -> Path:
    return UNITS_DIR / f"{unit_id}.json"


def save_units(units: list[dict[str, Any]]) -> None:
    ensure_dirs()
    for unit in units:
        write_json(unit_path(unit["id"]), unit)


def load_all_units() -> list[dict[str, Any]]:
    ensure_dirs()
    units = []
    for path in sorted(UNITS_DIR.glob("*.json")):
        units.append(read_json(path, {}))
    return [u for u in units if u]


def save_drafts(cards: list[dict[str, Any]]) -> None:
    ensure_dirs()
    by_id = {c["id"]: c for c in cards}
    for card in by_id.values():
        write_json(DRAFTS_DIR / f"{card['id']}.json", card)


def load_drafts() -> list[dict[str, Any]]:
    ensure_dirs()
    cards = []
    for path in sorted(DRAFTS_DIR.glob("*.json")):
        cards.append(read_json(path, {}))
    return [c for c in cards if c]


def load_queue() -> dict[str, Any]:
    ensure_dirs()
    return read_json(QUEUE_PATH, {"cards": {}})


def save_queue(queue: dict[str, Any]) -> None:
    write_json(QUEUE_PATH, queue)
