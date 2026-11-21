from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("anki")

from app import collection as coll  # noqa: E402


def test_review_persists_after_reopen(tmp_path, monkeypatch):
    monkeypatch.setattr(coll.config, "DATA_DIR", tmp_path)
    monkeypatch.setattr(coll.config, "COLLECTION_PATH", tmp_path / "collection.anki2")
    coll.close_collection()
    with coll.locked_collection() as col:
        coll._ensure_note_type(col)
        deck_id = coll._ensure_deck(col, "COIS-1020")
        model = col.models.by_name(coll.NOTE_TYPE)
        note = col.new_note(model)
        note.guid = "persist01"
        note["Front"] = "2+2?"
        note["Back"] = "4"
        note["Source"] = "test"
        note["Origin"] = "lecture"
        col.add_note(note, deck_id)
        col.save()
    payload = coll.next_card()
    assert payload and payload["card"]
    card_id = payload["card"]["card_id"]
    coll.answer_card(card_id, "good")
    reviews = coll.stats_summary()["reviews_logged"]
    assert reviews >= 1
    coll.close_collection()
    assert Path(coll.config.COLLECTION_PATH).exists()
    again = coll.stats_summary()["reviews_logged"]
    assert again == reviews


def test_upsert_updates_without_new_guid(tmp_path, monkeypatch):
    monkeypatch.setattr(coll.config, "DATA_DIR", tmp_path)
    monkeypatch.setattr(coll.config, "COLLECTION_PATH", tmp_path / "collection.anki2")
    coll.close_collection()
    card = {
        "guid": "stableguid",
        "deck": "COIS-1020::Ch",
        "front": "What is a loop?",
        "back": "Repeated execution",
        "source_ref": "file#page-1",
        "origin": "lecture",
        "tags": ["concept"],
    }
    first = coll.upsert_notes([card])
    assert first["created"] == 1
    card["back"] = "A structure that repeats a block"
    second = coll.upsert_notes([card])
    assert second["updated"] == 1
    assert second["created"] == 0
