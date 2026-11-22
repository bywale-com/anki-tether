from __future__ import annotations

import hashlib
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

import nh3

from app import config
from app.card_format import CARD_HTML_TAGS
from app.math_render import render_math

NOTE_TYPE = "COIS-1020"
FIELD_NAMES = ["Front", "Back", "Source", "Origin"]

_lock = threading.Lock()
_col = None


CARD_CSS = """
.card {
  font-family: system-ui, sans-serif;
  font-size: 1.05rem;
  line-height: 1.45;
  text-align: left;
  color: #111;
  background: #fff;
}
pre, code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 0.92rem;
  white-space: pre-wrap;
  word-break: break-word;
}
pre {
  overflow-x: auto;
  max-width: 100%;
  padding: 0.6rem;
  background: #f4f4f5;
  border-radius: 8px;
}
.meta { font-size: 0.8rem; color: #555; margin-top: 1rem; }
"""

FRONT_TMPL = "{{Front}}"
BACK_TMPL = "{{FrontSide}}<hr id=answer>{{Back}}<div class=meta>{{Origin}} · {{Source}}</div>"


def _import_anki():
    try:
        from anki.collection import Collection
        from anki.scheduler.v3 import CardAnswer
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "The official `anki` package is required for the study app. "
            "Install with: pip install 'anki-tether[app]' (Python 3.12 recommended)."
        ) from exc
    return Collection, CardAnswer


def ensure_data_dir() -> Path:
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    config.COLLECTION_PATH.parent.mkdir(parents=True, exist_ok=True)
    return config.DATA_DIR


def _ensure_note_type(col) -> None:
    models = col.models
    existing = models.by_name(NOTE_TYPE)
    if existing:
        return
    nt = models.new(NOTE_TYPE)
    for field in FIELD_NAMES:
        models.add_field(nt, models.new_field(field))
    tmpl = models.new_template("Card 1")
    tmpl["qfmt"] = FRONT_TMPL
    tmpl["afmt"] = BACK_TMPL
    models.add_template(nt, tmpl)
    nt["css"] = CARD_CSS
    models.add(nt)


def _ensure_v3(col) -> None:
    if col.sched_ver() != 2:
        col.upgrade_to_v2_scheduler()
    if not col.v3_scheduler():
        col.set_v3_scheduler(True)


def open_collection():
    global _col
    Collection, _ = _import_anki()
    ensure_data_dir()
    if _col is None:
        _col = Collection(str(config.COLLECTION_PATH))
        _ensure_v3(_col)
        _ensure_note_type(_col)
        deck_id = _ensure_deck(_col, config.DEFAULT_DECK)
        if _col.decks.current()["id"] == 1 and not _col.find_cards("deck:Default"):
            _col.decks.set_current(deck_id)
        _col.save()
    return _col


def close_collection() -> None:
    global _col
    with _lock:
        if _col is not None:
            _col.close()
            _col = None


@contextmanager
def locked_collection() -> Iterator[Any]:
    with _lock:
        yield open_collection()


def _ensure_deck(col, name: str) -> int:
    existing = col.decks.by_name(name)
    if existing:
        return existing["id"]
    deck_id = col.decks.id(name)
    return int(deck_id)


def deck_summaries() -> list[dict[str, Any]]:
    with locked_collection() as col:
        tree = col.sched.deck_due_tree()
        rows = []

        def walk(node, prefix=""):
            name = node.name
            full = f"{prefix}::{name}" if prefix else name
            if name != "Default" or node.new_count or node.learn_count or node.review_count:
                rows.append(
                    {
                        "id": int(node.deck_id),
                        "name": full or name,
                        "new": int(node.new_count),
                        "learn": int(node.learn_count),
                        "review": int(node.review_count),
                    }
                )
            for child in node.children:
                walk(child, full if name else prefix)

        for child in tree.children:
            walk(child)
        if not rows:
            rows.append({"id": 1, "name": config.DEFAULT_DECK, "new": 0, "learn": 0, "review": 0})
        return rows


def select_deck(deck_id: int) -> None:
    with locked_collection() as col:
        col.decks.set_current(deck_id)
        col.save()


def _card_payload(col, queued_card) -> dict[str, Any]:
    from anki.cards import Card

    card = Card(col)
    card._load_from_backend_card(queued_card.card)
    card.start_timer()
    return {
        "card_id": int(card.id),
        "question": render_math(nh3.clean(card.question(), tags=CARD_HTML_TAGS, attributes={})),
        "answer": render_math(nh3.clean(card.answer(), tags=CARD_HTML_TAGS, attributes={})),
        "states": queued_card.states,
        "queue": str(queued_card.queue),
    }


def next_card() -> dict[str, Any] | None:
    with locked_collection() as col:
        queued = col.sched.get_queued_cards(fetch_limit=1)
        counts = {
            "new": int(queued.new_count),
            "learn": int(queued.learning_count),
            "review": int(queued.review_count),
        }
        if not queued.cards:
            return {"done": True, "counts": counts, "card": None}
        card = _card_payload(col, queued.cards[0])
        return {"done": False, "counts": counts, "card": card}


def answer_card(card_id: int, rating: str) -> None:
    _, CardAnswer = _import_anki()
    rating_map = {
        "again": CardAnswer.AGAIN,
        "hard": CardAnswer.HARD,
        "good": CardAnswer.GOOD,
        "easy": CardAnswer.EASY,
    }
    if rating not in rating_map:
        raise ValueError("rating must be again, hard, good, or easy")
    with locked_collection() as col:
        queued = col.sched.get_queued_cards(fetch_limit=1)
        if not queued.cards:
            return
        current = queued.cards[0]
        from anki.cards import Card

        card = Card(col)
        card._load_from_backend_card(current.card)
        if int(card.id) != int(card_id):
            # Reload after another review; ignore stale answer rather than double-rate.
            return
        card.start_timer()
        built = col.sched.build_answer(
            card=card, states=current.states, rating=rating_map[rating]
        )
        col.sched.answer_card(built)
        col.save()


def _counts(col) -> dict[str, int]:
    queued = col.sched.get_queued_cards(fetch_limit=1)
    return {
        "new": int(queued.new_count),
        "learn": int(queued.learning_count),
        "review": int(queued.review_count),
    }


def counts() -> dict[str, int]:
    with locked_collection() as col:
        return _counts(col)


def performance(days: int = 7) -> dict[str, Any]:
    """First-attempt success rate over the selected window.

    A successful first attempt is a Hard/Good/Easy rating (ease 2-4) on the
    first review of that card in the window. Again (ease 1) is a miss.
    This is not predicted retention.
    """
    with locked_collection() as col:
        import time

        cutoff = int((time.time() - days * 86400) * 1000)
        rows = col.db.all(
            "SELECT cid, ease, id FROM revlog WHERE id >= ? ORDER BY id ASC",
            cutoff,
        )
        first: dict[int, int] = {}
        for cid, ease, _rid in rows:
            if cid not in first:
                first[cid] = ease
        total = len(first)
        success = sum(1 for ease in first.values() if ease >= 2)
        pct = (100.0 * success / total) if total else None
        return {
            "window_days": days,
            "cards_reviewed": total,
            "first_attempt_success": success,
            "first_attempt_percent": pct,
            "target_percent": 95.0,
            "meets_target": pct is not None and pct >= 95.0,
            "definition": (
                "Percentage of cards reviewed in this window whose first rating "
                "was Hard, Good, or Easy (not Again). Independent lab reproduction "
                "is tracked separately and is not inferred from this number."
            ),
        }


def stats_summary() -> dict[str, Any]:
    with locked_collection() as col:
        due = _counts(col)
        card_count = col.card_count()
        note_count = col.note_count()
        studied = col.db.scalar("SELECT COUNT(*) FROM revlog") or 0
        return {
            "cards": int(card_count),
            "notes": int(note_count),
            "reviews_logged": int(studied),
            **due,
        }


def stable_guid(parts: list[str]) -> str:
    raw = "\n".join(parts)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]


def upsert_notes(cards: list[dict[str, Any]]) -> dict[str, int]:
    created = updated = skipped = 0
    with locked_collection() as col:
        _ensure_note_type(col)
        model = col.models.by_name(NOTE_TYPE)
        for item in cards:
            deck_name = item.get("deck") or config.DEFAULT_DECK
            deck_id = _ensure_deck(col, deck_name)
            guid = item.get("guid") or stable_guid(
                [item.get("front", ""), item.get("source_file", ""), item.get("source_ref", "")]
            )
            nid = col.db.scalar("SELECT id FROM notes WHERE guid = ?", guid)
            fields = {
                "Front": item["front"],
                "Back": item["back"],
                "Source": item.get("source_ref") or item.get("source_file") or "",
                "Origin": item.get("origin") or "lecture",
            }
            tags = item.get("tags") or []
            if nid:
                note = col.get_note(nid)
                changed = (
                    any(note[k] != v for k, v in fields.items())
                    or {tag.casefold() for tag in note.tags} != {tag.casefold() for tag in tags}
                )
                # Authored batches own their deck metadata. Preserve existing PDF import behavior.
                move = []
                if guid.startswith("authored-"):
                    for cid in note.card_ids():
                        card = col.get_card(cid)
                        if (card.odid or card.did) != deck_id:
                            move.append(cid)
                if not changed and not move:
                    skipped += 1
                    continue
                if changed:
                    for k, v in fields.items():
                        note[k] = v
                    note.tags = list(tags)
                    col.update_note(note)
                if move:
                    col.set_deck(move, deck_id)
                updated += 1
            else:
                note = col.new_note(model)
                note.guid = guid
                for k, v in fields.items():
                    note[k] = v
                note.tags = list(tags)
                col.add_note(note, deck_id)
                created += 1
        col.save()
    return {"created": created, "updated": updated, "skipped": skipped, "total": len(cards)}
