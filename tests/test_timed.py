from uuid import uuid4

from fastapi.testclient import TestClient
import pytest

from app import collection, timed
from app.main import app


@pytest.fixture
def deck():
    pytest.importorskip("anki")
    collection.close_collection()
    collection.upsert_notes([
        {"deck": "Course::Topic", "front": "First question", "back": "Answer"},
        {"deck": "Course::Topic", "front": "Second question", "back": "Answer"},
        {"deck": "Other", "front": "Other question", "back": "Answer"},
    ])
    with collection.locked_collection() as col:
        did = col.decks.by_name("Course")["id"]
    yield did
    collection.close_collection()


def _rate(sid, rating):
    state = timed.snapshot(sid, review=True)
    timed.act(sid, "rate", state["nonce"], state["card"]["card_id"], rating)
    return state


def test_timed_real_queue_again_undo_and_frozen_scope(deck):
    assert timed.setup(deck) == ("Course", 2)
    sid = timed.start(deck, uuid4().hex, "stopwatch", 1, None)
    first = _rate(sid, "again")
    assert timed.snapshot(sid)["completed"] == 0
    timed.act(sid, "rate", first["nonce"], first["card"]["card_id"], "again")
    assert timed.snapshot(sid)["ratings"] == 1
    state = timed.snapshot(sid)
    timed.act(sid, "undo", state["nonce"])
    assert timed.snapshot(sid)["ratings"] == 0
    _rate(sid, "easy")
    complete = timed.snapshot(sid)
    assert complete["personal_best"]
    assert complete["target"] == [first["card"]["card_id"]]
    assert collection.stats_summary()["reviews_logged"] == 1
    timed.act(sid, "undo", complete["nonce"])
    assert timed.snapshot(sid)["status"] == "active"
    assert collection.stats_summary()["reviews_logged"] == 0


def test_pause_expiry_restart_and_board_groups(deck, monkeypatch):
    tick = 0
    monkeypatch.setattr(timed.time, "monotonic_ns", lambda: tick)
    sid = timed.start(deck, uuid4().hex, "countdown", 1, 5)
    tick += 1_000_000_000
    state = timed.snapshot(sid)
    timed.act(sid, "pause", state["nonce"])
    tick += 80_000_000_000
    assert timed.snapshot(sid)["elapsed"] == 1000
    timed.act(sid, "resume", timed.snapshot(sid)["nonce"])
    _rate(sid, "easy")
    assert not timed.snapshot(sid)["ranked"]
    expiry = timed.start(deck, uuid4().hex, "countdown", 1, 10)
    tick += 600_000_000_000
    assert timed.snapshot(expiry)["status"] == "expired"
    assert len(timed.board(deck, "countdown", 1)["groups"]) == 2
    active = timed.start(deck, uuid4().hex, "stopwatch", 1, None)
    monkeypatch.setattr(timed, "PROCESS", "restarted")
    collection.close_collection()
    assert timed.snapshot(active)["status"] == "interrupted"
    assert timed.active_id() is None
    assert timed.snapshot(sid)["status"] == "completed"


def test_timed_http_flow_and_ordinary_review_guard(deck):
    with TestClient(app, follow_redirects=False) as client:
        assert client.get("/time-board").status_code == 303
        client.post("/login", data={"username": "tester", "password": "secret"})
        csrf = client.cookies["anki_tether_csrf"]
        assert client.get(f"/study/{deck}/timed").status_code == 200
        data = {"csrf": csrf, "attempt": uuid4().hex, "mode": "stopwatch", "target": "2"}
        attempt = client.post(f"/study/{deck}/timed", data=data)
        url = attempt.headers["location"]
        assert client.post(f"/study/{deck}/timed", data=data).headers["location"] == url
        assert client.post(f"/study/{deck}", data={"csrf": csrf}).headers["location"] == url
        assert "0 / 2" in client.get(url).text
        assert "Good" in client.get(url + "?show=1").text
        sid = url.split("/")[-1]
        for _ in range(2):
            state = timed.snapshot(sid, review=True)
            data = {"csrf": csrf, "nonce": state["nonce"], "action": "rate",
                    "rating": "good", "card_id": state["card"]["card_id"]}
            assert client.post(url, data=data).status_code == 303
            assert client.post(url, data=data).status_code == 303
        assert "New personal best" in client.get(url).text
        assert "Personal best" in client.get(f"/time-board?deck={deck}&target=2").text
        assert collection.stats_summary()["reviews_logged"] == 2


def test_again_can_reappear_and_finish_unranked(deck):
    sid = timed.start(deck, uuid4().hex, "stopwatch", 1, None)
    first = _rate(sid, "again")
    second = _rate(sid, "easy")
    assert second["card"]["card_id"] == first["card"]["card_id"]
    result = timed.snapshot(sid)
    assert result["status"] == "completed"
    assert result["completed"] == 1
    assert result["accuracy"] == 0
    assert result["again"] == 1 and result["ratings"] == 2
    assert not result["ranked"]
