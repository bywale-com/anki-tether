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


def test_live_review_and_import_survive_app_restart():
    from fastapi.testclient import TestClient

    from app.main import app

    coll.close_collection()
    card = {
        "guid": "live-review",
        "front": "<pre><code>int x = 2;</code></pre><script>alert(1)</script>",
        "back": "A unique answer",
    }
    headers = {"Authorization": "Bearer import-secret"}
    credentials = {"username": "tester", "password": "secret"}
    with TestClient(app, follow_redirects=False) as client:
        assert client.get("/").headers["location"] == "/login"
        assert client.post("/api/import", json={"cards": [card]}, headers=headers).json()["created"] == 1
        assert client.post("/login", data=credentials).status_code == 303
        assert "COIS-1020" in client.get("/").text
        deck_id = next(d["id"] for d in coll.deck_summaries() if d["name"] == "COIS-1020")
        csrf = client.cookies["anki_tether_csrf"]
        assert client.post(f"/study/{deck_id}", data={"csrf": csrf}).status_code == 303
        question = client.get("/review").text
        assert "int x = 2;" in question
        assert "alert(1)" not in question
        assert "A unique answer" not in question
        assert "A unique answer" in client.get("/review?show=1").text
        cid = coll.next_card()["card"]["card_id"]
        assert client.post("/review/answer", data={"csrf": csrf, "card_id": cid, "rating": "good"}).status_code == 303

    with TestClient(app, follow_redirects=False) as client:
        assert client.post("/login", data=credentials).status_code == 303
        assert client.get("/stats").status_code == 200
        card["back"] = "Updated answer"
        result = client.post("/api/import", json={"cards": [card]}, headers=headers)
        assert result.json()["updated"] == 1
        assert coll.stats_summary()["reviews_logged"] == 1
        with coll.locked_collection() as col:
            assert col.get_card(cid).reps == 1
