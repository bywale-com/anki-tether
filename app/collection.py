from __future__ import annotations

from html import unescape
import hashlib
from urllib.parse import urlsplit
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

import nh3

from app import config, timed_store
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
        if not timed_store.active_id():
            col.decks.set_current(deck_id)


FLAG_REASONS = {
    "dont_understand": "Don't understand",
    "need_practice": "Need practice",
    "card_problem": "Card problem",
}
FLAG_CONFIG = "anki_tether_card_flags"


def _flags(col) -> dict[str, str]:
    return col.get_config(FLAG_CONFIG, {})


def set_card_flag(card_id: int, reason: str) -> bool:
    if reason and reason not in FLAG_REASONS:
        raise ValueError("Invalid flag reason")
    with locked_collection() as col:
        if not col.db.scalar("select 1 from cards where id = ?", card_id):
            return False
        flags = _flags(col)
        if reason:
            flags[str(card_id)] = reason
        else:
            flags.pop(str(card_id), None)
        col.set_config(FLAG_CONFIG, flags, undoable=False)
        return True


def _card_details(col, card) -> dict[str, Any]:
    deck = col.decks.get(card.odid or card.did, default=False)
    note = card.note()
    source = note["Source"].strip() if "Source" in note else ""
    try:
        url = urlsplit(source)
        source_url = source if url.scheme in {"http", "https"} and url.hostname and not url.username else ""
    except ValueError:
        source_url = ""
    return {
        "card_id": int(card.id),
        "deck": deck["name"] if deck else "",
        "tags": note.tags,
        "source": source,
        "source_url": source_url,
        "flag": _flags(col).get(str(card.id), ""),
    }


def _card_title(card) -> str:
    text = " ".join(unescape(nh3.clean(card.question(), tags=set(), attributes={})).split())
    return text[:160] + "…" if len(text) > 160 else text


def browse_cards(deck_id: int | None, query: str, page: int, flag: str = "") -> dict[str, Any] | None:
    from anki.collection import SearchNode

    page_size = 30
    with locked_collection() as col:
        decks = {deck.id: deck.name for deck in col.decks.all_names_and_ids()}
        search = []
        if deck_id is not None:
            if deck_id not in decks:
                return None
            search.append(SearchNode(deck=decks[deck_id]))
        if query:
            text = SearchNode(literal_text=query)
            tag = query.replace("\\", "\\\\").replace("*", "\\*").replace("_", "\\_")
            tag = tag.replace('"', '\\"')
            tagged = SearchNode(parsable_text=f'"tag:*{tag}*"')
            search.append(col.group_searches(text, tagged, joiner="OR"))
        ids = col.find_cards(col.build_search_string(*search) if search else "", order="c.id asc")
        flags = _flags(col)
        if flag:
            ids = [cid for cid in ids if flags.get(str(cid)) and (flag == "flagged" or flags[str(cid)] == flag)]
        pages = max(1, (len(ids) + page_size - 1) // page_size)
        page = min(page, pages)
        start = (page - 1) * page_size
        cards = []
        for cid in ids[start:start + page_size]:
            card = col.get_card(cid)
            cards.append({
                "id": cid,
                "title": _card_title(card),
                "deck": decks.get(card.odid or card.did, ""),
                "flag": flags.get(str(cid), ""),
            })
        return {"decks": decks, "cards": cards, "page": page, "pages": pages, "total": len(ids)}


def browse_card(card_id: int) -> dict[str, Any] | None:
    from anki.errors import NotFoundError

    with locked_collection() as col:
        try:
            card = col.get_card(card_id)
        except NotFoundError:
            return None
        return {**_card_sides(card), **_card_details(col, card)}


def _card_sides(card) -> dict[str, str]:
    return {
        "question": render_math(nh3.clean(card.question(), tags=CARD_HTML_TAGS, attributes={})),
        "answer": render_math(nh3.clean(card.answer(), tags=CARD_HTML_TAGS, attributes={})),
    }


def _card_payload(col, queued_card) -> dict[str, Any]:
    from anki.cards import Card

    card = Card(col)
    card._load_from_backend_card(queued_card.card)
    card.start_timer()
    return {
        **_card_details(col, card),
        **_card_sides(card),
        "states": queued_card.states,
        "queue": str(queued_card.queue),
    }


def _review_queue(col, all_due: bool):
    """Find a native queued card, temporarily selecting course roots in all-due mode."""
    from anki.scheduler_pb2 import QueuedCards

    selected = col.decks.current()["id"]
    if not all_due:
        queued = col.sched.get_queued_cards()
        return (queued.cards[0] if queued.cards else None), _counts_from_queue(queued), selected

    counts = {"new": 0, "learn": 0, "review": 0}
    next_card = None
    next_deck = selected
    for course in col.sched.deck_due_tree().children:
        counts["learn"] += course.learn_count
        counts["review"] += course.review_count
        if next_card is not None or not (course.learn_count or course.review_count):
            continue
        if course.deck_id != selected:
            col.decks.set_current(course.deck_id)
        try:
            queued = col.sched.get_queued_cards()
            if queued.cards and queued.cards[0].queue == QueuedCards.NEW:
                queued = col.sched.get_queued_cards(fetch_limit=queued.new_count + 1)
            next_card = next((card for card in queued.cards if card.queue != QueuedCards.NEW), None)
            next_deck = course.deck_id
        finally:
            # Undo only temporary deck selection, leaving the last review available.
            if course.deck_id != selected:
                col.undo()
    return next_card, counts, next_deck


def next_card(all_due: bool = False) -> dict[str, Any] | None:
    with locked_collection() as col:
        queued, counts, _ = _review_queue(col, all_due)
        card = _card_payload(col, queued) if queued else None
        return {"done": card is None, "counts": counts, "card": card}


REVIEW_UNDO_LABEL = "Anki Tether review"


def rate_queued(col, current, rating: str, deck_id: int, undo_label: str = REVIEW_UNDO_LABEL):
    _, CardAnswer = _import_anki()
    ratings = {"again": CardAnswer.AGAIN, "hard": CardAnswer.HARD, "good": CardAnswer.GOOD, "easy": CardAnswer.EASY}
    if rating not in ratings:
        raise ValueError("rating must be again, hard, good, or easy")
    selected = col.decks.current()["id"]
    undo_group = col.add_custom_undo_entry(undo_label)
    if deck_id != selected:
        col.decks.set_current(deck_id)
    try:
        card = col.get_card(current.card.id)
        card.start_timer()
        col.sched.answer_card(col.sched.build_answer(card=card, states=current.states, rating=ratings[rating]))
    finally:
        if deck_id != selected:
            col.decks.set_current(selected)
    col.merge_undo_entries(undo_group)


def answer_card(card_id: int, rating: str, all_due: bool = False) -> None:
    with locked_collection() as col:
        if timed_store.active_id():
            return
        current, _, deck_id = _review_queue(col, all_due)
        if current is not None and current.card.id == card_id:
            rate_queued(col, current, rating, deck_id)


def _can_undo_review(col) -> bool:
    return col.undo_status().undo == REVIEW_UNDO_LABEL


def can_undo_review() -> bool:
    with locked_collection() as col:
        return _can_undo_review(col)


def undo_review() -> bool:
    with locked_collection() as col:
        if timed_store.active_id() or not _can_undo_review(col):
            return False
        col.undo()
        return True


def _counts_from_queue(queued) -> dict[str, int]:
    return {
        "new": int(queued.new_count),
        "learn": int(queued.learning_count),
        "review": int(queued.review_count),
    }


def _counts(col) -> dict[str, int]:
    return _counts_from_queue(col.sched.get_queued_cards())


def counts() -> dict[str, int]:
    with locked_collection() as col:
        return _counts(col)


def _recall(ratings) -> dict[str, Any]:
    first = {}
    for cid, ease in ratings:
        first.setdefault(cid, ease)
    total = len(first)
    success = sum(ease >= 2 for ease in first.values())
    pct = 100.0 * success / total if total else None
    return {
        "cards_reviewed": total,
        "first_attempt_success": success,
        "first_attempt_percent": pct,
        "target_percent": 95.0,
        "meets_target": pct is not None and pct >= 95.0,
    }


def _window_cutoff(days: int) -> int:
    return int((time.time() - days * 86400) * 1000)


def performance(days: int = 7) -> dict[str, Any]:
    with locked_collection() as col:
        ratings = col.db.all(
            "select cid, ease from revlog where id >= ? and ease between 1 and 4 order by id",
            _window_cutoff(days),
        )
        return {
            **_recall(ratings),
            "window_days": days,
            "definition": (
                "Percentage of cards reviewed in this window whose first rating "
                "was Hard, Good, or Easy (not Again). Independent lab reproduction "
                "is tracked separately and is not inferred from this number."
            ),
        }


def learning_progress(days: int) -> dict[str, Any]:
    with locked_collection() as col:
        decks = {d.id: d.name for d in col.decks.all_names_and_ids()}
        courses = {
            decks[deck.deck_id]: {
                "name": decks[deck.deck_id],
                "due": deck.review_count + deck.learn_count,
                "ratings": [],
            }
            for deck in col.sched.deck_due_tree().children
            if deck.deck_id in decks
        }
        rows = col.db.all(
            """select r.cid, r.ease, case when c.odid > 0 then c.odid else c.did end
               from revlog r join cards c on c.id = r.cid
               where r.id >= ? and r.ease between 1 and 4 order by r.id""",
            _window_cutoff(days),
        )
        for cid, ease, did in rows:
            name = decks.get(did, "").split("::")[0]
            if name in courses:
                courses[name]["ratings"].append((cid, ease))

        flag_counts = dict.fromkeys(FLAG_REASONS, 0)
        for cid, reason in _flags(col).items():
            if reason in flag_counts and col.db.scalar("select 1 from cards where id = ?", int(cid)):
                flag_counts[reason] += 1

        recent = []
        for cid in col.db.list(
            """select r.cid from revlog r join cards c on c.id = r.cid
               where r.id >= ? and r.ease = 1
               group by r.cid order by max(r.id) desc limit 8""",
            _window_cutoff(days),
        ):
            card = col.get_card(cid)
            recent.append({"id": cid, "title": _card_title(card), "deck": decks.get(card.odid or card.did, "")})
        course_rows = []
        for course in courses.values():
            ratings = course.pop("ratings")
            if course["name"] == "Default" and not (course["due"] or ratings):
                continue
            course_rows.append({**course, "reviews": len(ratings), **_recall(ratings)})
        return {"courses": course_rows, "flags": flag_counts, "recent": recent}


def review_cursor() -> int:
    with locked_collection() as col:
        return col.db.scalar("select coalesce(max(id), 0) from revlog")


def session_summary(after: int) -> dict[str, Any]:
    with locked_collection() as col:
        reviews, cards, again = col.db.first(
            """select count(*), count(distinct cid), coalesce(sum(ease = 1), 0)
               from revlog where id > ? and ease between 1 and 4""",
            after,
        )
        return {"reviews": reviews, "cards": cards, "again": again}


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
