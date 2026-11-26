"""Durable timed sessions around Anki's native deck queue."""

from contextlib import contextmanager
from datetime import datetime, timezone
import time
from uuid import uuid4

from app import collection, timed_store

PROCESS = uuid4().hex
OPEN = {"active", "paused"}
MODES = {"countdown": "Beat the Clock", "stopwatch": "Track My Time"}
RATINGS = {"again", "hard", "good", "easy"}
MIN_ACCURACY = 90


def _now():
    return datetime.now(timezone.utc).isoformat()


def _elapsed(session):
    base = session["elapsed_ms"]
    if session["status"] == "active" and session["process"] == PROCESS:
        return base + max(0, (time.monotonic_ns() - session["tick"]) // 1_000_000)
    return base


def _finish(session, status, elapsed=None):
    session["elapsed_ms"] = _elapsed(session) if elapsed is None else elapsed
    session["status"] = status
    session["finished_at"] = _now()
    timed_store.save(session)


def _reconcile(session):
    if session.get("pending"):
        session.pop("pending")
        _finish(session, "interrupted")
    elif session["status"] in OPEN:
        if session["process"] != PROCESS:
            _finish(session, "interrupted")
        elif session["status"] == "active" and session["budget_ms"] and _elapsed(session) >= session["budget_ms"]:
            _finish(session, "expired", session["budget_ms"])
    return session


def active_id():
    with collection.locked_collection():
        session_id = timed_store.active_id()
        if session_id:
            session = timed_store.read(session_id)
            if session and _reconcile(session)["status"] in OPEN:
                return session_id
    return None


@contextmanager
def _selected(col, did):
    changed = col.decks.current()["id"] != did
    if changed:
        col.decks.set_current(did)
    try:
        yield
    finally:
        if changed:
            col.undo()


def _queue(col, did):
    with _selected(col, did):
        initial = col.sched.get_queued_cards()
        limit = initial.new_count + initial.learning_count + initial.review_count
        return col.sched.get_queued_cards(fetch_limit=max(1, limit)).cards


def setup(did):
    with collection.locked_collection() as col:
        deck = col.decks.get(did, default=False)
        return (deck["name"], len(_queue(col, did))) if deck else None


def start(did, session_id, mode, target, minutes):
    with collection.locked_collection() as col:
        existing = timed_store.read(session_id)
        if existing:
            return existing["id"]
        active = timed_store.active_id()
        if active:
            return active
        deck = col.decks.get(did, default=False)
        if not deck:
            raise LookupError("Deck not found")
        cards = list(dict.fromkeys(card.card.id for card in _queue(col, did)))
        count = len(cards) if target is None else target
        if mode not in MODES or not 1 <= count <= len(cards):
            raise ValueError("Choose a target within the currently eligible cards.")
        if mode == "countdown" and (minutes is None or not 1 <= minutes <= 180):
            raise ValueError("Choose a countdown from 1 to 180 minutes.")
        session = {
            "id": session_id, "deck_id": did, "title": deck["name"], "mode": mode,
            "target": cards[:count], "budget_ms": minutes * 60_000 if mode == "countdown" else None,
            "process": PROCESS, "tick": time.monotonic_ns(), "elapsed_ms": 0,
            "started_at": _now(), "status": "active", "paused": False, "events": [],
            "nonce": uuid4().hex,
        }
        timed_store.save(session)
        return session_id


def _score(session):
    first = {}
    completed = set()
    again = 0
    for event in session["events"]:
        cid, rating = event["card"], event["rating"]
        first.setdefault(cid, rating)
        if rating == "again":
            again += 1
        else:
            completed.add(cid)
    return completed, sum(rating != "again" for rating in first.values()), again


def _next(col, session):
    completed, _, _ = _score(session)
    remaining = set(session["target"]) - completed
    if not col.decks.get(session["deck_id"], default=False):
        return None
    return next((item for item in _queue(col, session["deck_id"]) if item.card.id in remaining), None)


def _group(session):
    return session["deck_id"], session["mode"], len(session["target"]), session["budget_ms"]


def _view(col, session):
    completed, correct, again = _score(session)
    count = len(session["target"])
    elapsed = _elapsed(session)
    ranked = session["status"] == "completed" and not session["paused"] and correct * 100 >= MIN_ACCURACY * count
    deck = col.decks.get(session["deck_id"], default=False)
    return {
        **session, "title": deck["name"] if deck else session["title"], "deck_exists": bool(deck),
        "count": count, "completed": len(completed), "accuracy": correct * 100 / count, "again": again,
        "ratings": len(session["events"]), "elapsed": elapsed,
        "remaining": max(0, session["budget_ms"] - elapsed) if session["budget_ms"] else None,
        "ranked": ranked, "label": _label(session, ranked),
    }


def _label(session, ranked):
    status = session["status"]
    if status == "completed":
        if session["paused"]:
            return "Completed — unranked (paused)"
        return "Completed" if ranked else "Completed — below accuracy threshold"
    return {
        "active": "In progress", "paused": "Paused", "expired": "Time's up",
        "exhausted": "Incomplete — queue exhausted", "stopped": "Stopped early",
        "interrupted": "Interrupted",
    }[status]


def snapshot(session_id, review=False):
    with collection.locked_collection() as col:
        session = timed_store.read(session_id)
        if not session:
            return None
        _reconcile(session)
        card = None
        if review and session["status"] == "active":
            queued = _next(col, session)
            if queued:
                card = collection._card_payload(col, queued)
            else:
                _finish(session, "exhausted")
        result = _view(col, session)
        result["card"] = card
        result["can_undo"] = _can_undo(col, session)
        if result["ranked"]:
            prior = (_view(col, item) for item in timed_store.history() if item["id"] != session_id
                     and item.get("finished_at", "") < session["finished_at"] and _group(item) == _group(session))
            result["personal_best"] = all(not item["ranked"] or item["elapsed"] > result["elapsed"] for item in prior)
        return result


def _undo_label(session):
    return "Timed review " + session["id"]


def _can_undo(col, session):
    return (session["status"] in {"active", "completed", "exhausted"} and session["process"] == PROCESS
            and bool(session["events"]) and timed_store.active_id() in {None, session["id"]}
            and col.undo_status().undo == _undo_label(session))


def act(session_id, action, nonce, card_id=None, rating=None):
    with collection.locked_collection() as col:
        session = timed_store.read(session_id)
        if not session:
            raise LookupError("Timed session not found")
        _reconcile(session)
        if nonce != session["nonce"]:
            return
        status = session["status"]
        if action == "undo" and _can_undo(col, session):
            session["pending"] = True
            timed_store.save(session)
            col.undo()
            session["events"].pop()
            if status != "active":
                session["status"] = "active"
                session["tick"] = time.monotonic_ns()
                session.pop("finished_at", None)
            session.pop("pending")
        elif action == "rate" and status == "active":
            queued = _next(col, session)
            if not queued or queued.card.id != card_id or rating not in RATINGS:
                return
            elapsed = _elapsed(session)
            if session["budget_ms"] and elapsed >= session["budget_ms"]:
                _finish(session, "expired", session["budget_ms"])
                return
            # The next request treats a crash between Anki commit and the ledger as interrupted.
            session["pending"] = True
            session["elapsed_ms"] = elapsed
            session["tick"] = time.monotonic_ns()
            timed_store.save(session)
            collection.rate_queued(col, queued, rating, session["deck_id"], _undo_label(session))
            session["events"].append({"card": card_id, "rating": rating})
            session.pop("pending")
            if len(_score(session)[0]) == len(session["target"]):
                session["nonce"] = uuid4().hex
                _finish(session, "completed", elapsed)
                return
        elif action == "pause" and status == "active":
            session["elapsed_ms"] = _elapsed(session)
            session["paused"] = True
            session["status"] = "paused"
        elif action == "resume" and status == "paused":
            session["tick"] = time.monotonic_ns()
            session["status"] = "active"
        elif action == "stop" and status in OPEN:
            session["nonce"] = uuid4().hex
            _finish(session, "stopped")
            return
        else:
            return
        session["nonce"] = uuid4().hex
        timed_store.save(session)


def board(deck, mode, target):
    with collection.locked_collection() as col:
        history = [_view(col, _reconcile(session)) for session in timed_store.history()]
        attempts = [item for item in history if item["status"] not in OPEN]
        decks = {item["deck_id"]: item["title"] for item in history}
        decks.update({d.id: d.name for d in col.decks.all_names_and_ids()})
        groups = {}
        for item in reversed(attempts):
            if ((deck and item["deck_id"] != deck) or (mode and item["mode"] != mode)
                or (target and item["count"] != target)):
                continue
            groups.setdefault(_group(item), []).append(item)
        return {
            "decks": sorted(decks.items(), key=lambda pair: pair[1].casefold()),
            "targets": sorted({item["count"] for item in attempts}),
            "groups": list(groups.values()),
            "history": sorted((item for group in groups.values() for item in group),
                              key=lambda item: item["finished_at"], reverse=True),
        }
