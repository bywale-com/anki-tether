from __future__ import annotations

from fastapi.testclient import TestClient

from app import collection as coll
from app.main import app


def _stub_collection(monkeypatch):
    monkeypatch.setattr(coll, "deck_summaries", lambda: [
        {"id": 1, "name": "COIS-1020", "new": 1, "learn": 0, "review": 0}
    ])
    monkeypatch.setattr(coll, "stats_summary", lambda: {
        "cards": 1, "notes": 1, "reviews_logged": 0, "new": 1, "learn": 0, "review": 0
    })
    monkeypatch.setattr(coll, "performance", lambda days=7: {
        "window_days": days,
        "cards_reviewed": 0,
        "first_attempt_success": 0,
        "first_attempt_percent": None,
        "target_percent": 95.0,
        "meets_target": False,
        "definition": "test",
    })
    monkeypatch.setattr(coll, "next_card", lambda: {
        "done": False,
        "counts": {"new": 1, "learn": 0, "review": 0},
        "card": {"card_id": 99, "question": "Q?", "answer": "A.", "queue": "new"},
    })
    monkeypatch.setattr(coll, "select_deck", lambda deck_id: None)
    monkeypatch.setattr(coll, "answer_card", lambda card_id, rating: None)
    monkeypatch.setattr(coll, "upsert_notes", lambda cards: {
        "created": len(cards), "updated": 0, "skipped": 0, "total": len(cards)
    })
    monkeypatch.setattr(coll, "close_collection", lambda: None)


def test_healthz_unauthenticated():
    client = TestClient(app)
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_home_requires_login(monkeypatch):
    _stub_collection(monkeypatch)
    client = TestClient(app, follow_redirects=False)
    r = client.get("/")
    assert r.status_code == 303
    assert r.headers["location"] == "/login"


def test_login_and_review_flow(monkeypatch):
    _stub_collection(monkeypatch)
    client = TestClient(app)
    bad = client.post("/login", data={"username": "tester", "password": "nope"})
    assert bad.status_code == 401
    ok = client.post("/login", data={"username": "tester", "password": "secret"}, follow_redirects=False)
    assert ok.status_code == 303
    home = client.get("/")
    assert home.status_code == 200
    assert "COIS-1020" in home.text
    review = client.get("/review")
    assert review.status_code == 200
    assert "Q?" in review.text
    shown = client.get("/review?show=1")
    assert "A." in shown.text
    csrf = client.cookies.get("anki_tether_csrf")
    ans = client.post("/review/answer", data={"card_id": 99, "rating": "good", "csrf": csrf})
    assert ans.status_code == 200


def test_import_requires_token(monkeypatch):
    _stub_collection(monkeypatch)
    client = TestClient(app)
    r = client.post("/api/import", json={"cards": [{"front": "a", "back": "b"}]})
    assert r.status_code == 401
    r = client.post(
        "/api/import",
        json={"cards": [{"front": "a", "back": "b", "guid": "abc"}]},
        headers={"Authorization": "Bearer import-secret"},
    )
    assert r.status_code == 200
    assert r.json()["created"] == 1
