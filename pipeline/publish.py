from __future__ import annotations

import os
from typing import Any

import httpx

from pipeline.approve import approved_cards
from pipeline.store import load_drafts, load_queue, save_drafts, save_queue


def to_import_payload(cards: list[dict[str, Any]]) -> dict[str, Any]:
    body = []
    for card in cards:
        body.append(
            {
                "guid": card["guid"],
                "deck": card["deck"],
                "front": card["front"],
                "back": card["back"],
                "source_file": card.get("source_file"),
                "source_ref": card.get("source_ref"),
                "origin": card.get("origin"),
                "tags": card.get("tags") or [],
            }
        )
    return {"cards": body}


def publish(url: str | None = None, token: str | None = None) -> dict[str, Any]:
    url = url or os.environ.get("STUDY_APP_URL")
    token = token or os.environ.get("IMPORT_TOKEN")
    if not url or not token:
        raise RuntimeError("STUDY_APP_URL and IMPORT_TOKEN are required to publish")
    cards = approved_cards()
    if not cards:
        return {"ok": True, "published": 0, "message": "no approved cards"}
    endpoint = url.rstrip("/") + "/api/import"
    response = httpx.post(
        endpoint,
        json=to_import_payload(cards),
        headers={"Authorization": f"Bearer {token}"},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    if data.get("ok") is not True or data.get("total") != len(cards):
        raise RuntimeError("Study app did not acknowledge the full import batch")
    drafts = load_drafts()
    queue = load_queue()
    approved_ids = {c["id"] for c in cards}
    for card in drafts:
        if card["id"] in approved_ids:
            card["status"] = "published"
            queue.setdefault("cards", {}).setdefault(card["id"], {})["status"] = "published"
    save_drafts(drafts)
    save_queue(queue)
    return {"ok": True, "result": data, "published": len(cards)}
