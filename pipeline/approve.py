from __future__ import annotations

from typing import Any

from pipeline.store import load_all_units, load_drafts, load_queue, save_drafts, save_queue

from pipeline.validate import source_matches


def set_status(card_ids: list[str] | None, status: str, high_confidence_only: bool = False) -> dict[str, Any]:
    cards = load_drafts()
    queue = load_queue()
    changed = 0
    units = {unit["id"]: unit for unit in load_all_units()}
    for card in cards:
        if card_ids is not None and card["id"] not in card_ids:
            continue
        if high_confidence_only and not card.get("eligible_auto_approve"):
            continue
        if status == "approved" and (card.get("validation") != "passed" or not source_matches(card, units)):
            continue
        card["status"] = status
        queue.setdefault("cards", {}).setdefault(card["id"], {})["status"] = status
        changed += 1
    save_drafts(cards)
    save_queue(queue)
    return {"status": status, "changed": changed}


def approved_cards() -> list[dict[str, Any]]:
    units = {unit["id"]: unit for unit in load_all_units()}
    return [
        card for card in load_drafts()
        if card.get("status") == "approved"
        and card.get("validation") == "passed"
        and source_matches(card, units)
    ]
