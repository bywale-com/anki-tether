from __future__ import annotations

import hashlib
import json
import os
import re
from typing import Any

import httpx

from pipeline.store import load_all_units, load_drafts, save_drafts, save_queue, load_queue

TERM_LINE = re.compile(r"^(?P<term>[A-Z][^.\n]{2,80})$")


def card_id(parts: list[str]) -> str:
    return hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:20]


def deck_name(unit: dict[str, Any]) -> str:
    chapter = unit.get("chapter") or "COIS-1020"
    return f"COIS-1020::{chapter}"


def _code_html(code: str) -> str:
    escaped = (
        code.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return f"<pre><code>{escaped}</code></pre>"


def deterministic_cards(units: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    by_page: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for unit in units:
        by_page.setdefault((unit["source_file"], unit["page"]), []).append(unit)

    for unit in units:
        kind = unit["content_type"]
        if kind == "paragraph" or kind == "list":
            cards.extend(_definition_cards(unit))
        elif kind == "code":
            cards.extend(_code_cards(unit, by_page.get((unit["source_file"], unit["page"]), [])))
        elif kind == "exercise":
            cards.append(_exercise_prompt(unit))

    cards.extend(_independent_exercises(units))
    return _dedupe(cards)


def _definition_cards(unit: dict[str, Any]) -> list[dict[str, Any]]:
    text = unit["text"]
    lines = [ln.strip(" \t•-\u0007") for ln in text.splitlines() if ln.strip()]
    cards = []
    i = 0
    while i < len(lines):
        line = re.sub(r"^[\u0007•\-]+\s*", "", lines[i]).strip()
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        nxt = re.sub(r"^[\u0007•\-]+\s*", "", nxt).strip()
        # Pattern: term on one line, definition on the next
        if line and nxt and len(line) <= 80 and not line.endswith(".") and len(nxt) > 20:
            question = f"In {unit['section']}, what is <strong>{_esc(line)}</strong>?"
            answer = _esc(nxt)
            cards.append(_card(unit, "concept", question, answer, confidence="high"))
            i += 2
            continue
        i += 1
    if "is a" in text.lower() or "is an" in text.lower():
        for sent in re.split(r"(?<=\.)\s+", text.replace("\n", " ")):
            m = re.search(r"(.{3,60}?)\s+is (?:a|an|the)\s+(.{10,200})", sent, re.I)
            if m:
                term, definition = m.group(1).strip(" -•"), m.group(2).strip()
                cards.append(
                    _card(
                        unit,
                        "concept",
                        f"What is {_esc(term)}?",
                        _esc(definition.rstrip(".")),
                        confidence="high",
                    )
                )
    return cards


def _code_cards(unit: dict[str, Any], page_units: list[dict[str, Any]]) -> list[dict[str, Any]]:
    code = unit["text"]
    outputs = [u["text"] for u in page_units if u["content_type"] == "output"]
    cards = []
    intent = unit.get("code_intent") or "compiles"
    if outputs:
        cards.append(
            _card(
                unit,
                "code_output",
                "What does this C# fragment write to the console?<br>" + _code_html(code),
                _code_html(outputs[0]),
                confidence="high",
                extra={"code_intent": intent},
            )
        )
    else:
        cards.append(
            _card(
                unit,
                "syntax",
                "What is this C# fragment doing?<br>" + _code_html(code),
                f"From {_esc(unit['section'])} (p.{unit['page']}). Interpret the statements in order. Intent: {intent}.",
                confidence="medium",
                extra={"code_intent": intent},
            )
        )
    if intent == "error_demo":
        cards.append(
            _card(
                unit,
                "error",
                "Why is this C# fragment invalid or error-demonstrating?<br>" + _code_html(code),
                "Treat this as an error demonstration from the lecture, not as compiling code.",
                confidence="medium",
                extra={"code_intent": intent},
            )
        )
    return cards


def _exercise_prompt(unit: dict[str, Any]) -> dict[str, Any]:
    return _card(
        unit,
        "lab_prompt",
        "Practice prompt from the lecture (solve independently; do not treat this as a submitted lab):<br>"
        + _esc(unit["text"]),
        "No solution is published here. Reproduce the exercise yourself in Visual Studio / your C# environment.",
        confidence="high",
        origin="lecture_exercise",
        extra={"code_intent": "none"},
    )


def _independent_exercises(units: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Short practice prompts tagged as independently generated, not lecture text."""
    topics = []
    for unit in units:
        if unit["content_type"] == "heading" and len(unit["text"]) < 80:
            topics.append(unit)
    cards = []
    seen = set()
    for unit in topics:
        key = unit["text"].lower()
        if key in seen:
            continue
        seen.add(key)
        if any(w in key for w in ("loop", "while", "for ", "array", "method", "class", "if ", "variable")):
            prompt = (
                f"Independent practice (not lecture wording): write a short C# program that "
                f"demonstrates <strong>{_esc(unit['text'])}</strong>. Compile and run it yourself."
            )
            cards.append(
                _card(
                    unit,
                    "independent_exercise",
                    prompt,
                    "No pre-solved submission is provided. University coursework must be your own work.",
                    confidence="high",
                    origin="independent_exercise",
                )
            )
        if len(cards) >= 12:
            break
    return cards


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _card(
    unit: dict[str, Any],
    kind: str,
    front: str,
    back: str,
    confidence: str,
    origin: str = "lecture",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cid = card_id([unit["source_file"], str(unit["page"]), kind, front[:120]])
    card = {
        "id": cid,
        "guid": cid[:10],
        "kind": kind,
        "deck": deck_name(unit),
        "front": front,
        "back": back,
        "source_file": unit["source_file"],
        "source_ref": f"{unit['source_file']}#page-{unit['page']}",
        "source_hash": unit["source_hash"],
        "origin": origin,
        "generation": "deterministic",
        "confidence": confidence,
        "status": "draft",
        "tags": [kind, origin, f"p{unit['page']}"],
        "unit_id": unit["id"],
    }
    if extra:
        card.update(extra)
    return card


def _dedupe(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out = []
    for card in cards:
        key = re.sub(r"\s+", " ", card["front"] + "|" + card["back"]).lower()
        digest = hashlib.sha1(key.encode()).hexdigest()
        if digest in seen:
            continue
        seen.add(digest)
        out.append(card)
    return out


def ai_cards(units: list[dict[str, Any]]) -> list[dict[str, Any]]:
    api_key = os.environ.get("AI_API_KEY")
    base = os.environ.get("AI_API_BASE_URL") or "https://api.openai.com/v1"
    model = os.environ.get("AI_MODEL") or "gpt-4.1-mini"
    if not api_key:
        return []
    sample = [
        {
            "id": u["id"],
            "section": u["section"],
            "page": u["page"],
            "type": u["content_type"],
            "text": u["text"][:1200],
            "source_file": u["source_file"],
        }
        for u in units
        if u["content_type"] in {"paragraph", "list", "code", "exercise"}
    ][:40]
    if not sample:
        return []
    prompt = {
        "model": model,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Create atomic Anki cards for a C# course. Return JSON {cards:[{unit_id,kind,front,back,confidence}]} "
                    "Use only the supplied source. Mark uncertainty in the back. Never invent lecture facts. "
                    "Preserve C# exactly. Kinds: concept, syntax, code_output, error, control_flow, compare, methods."
                ),
            },
            {"role": "user", "content": json.dumps(sample)},
        ],
    }
    try:
        r = httpx.post(
            base.rstrip("/") + "/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json=prompt,
            timeout=60,
        )
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]
        data = json.loads(content[content.find("{") : content.rfind("}") + 1])
    except Exception:
        return []
    by_id = {u["id"]: u for u in units}
    cards = []
    for raw in data.get("cards", []):
        unit = by_id.get(raw.get("unit_id"))
        if not unit:
            continue
        cards.append(
            _card(
                unit,
                raw.get("kind") or "concept",
                raw.get("front") or "",
                (raw.get("back") or "")
                + "<p><em>AI-assisted draft — not certified accurate by structural validation alone.</em></p>",
                confidence=raw.get("confidence") or "low",
            )
        )
        cards[-1]["generation"] = "ai"
        cards[-1]["status"] = "draft"
    return cards


def generate(include_ai: bool = True) -> list[dict[str, Any]]:
    units = load_all_units()
    cards = deterministic_cards(units)
    if include_ai:
        cards.extend(ai_cards(units))
    existing = {c["id"]: c for c in load_drafts()}
    merged = []
    for card in cards:
        prev = existing.get(card["id"])
        if prev and prev.get("status") in {"approved", "published", "rejected"}:
            # Keep human decision; refresh content if source changed
            card["status"] = prev["status"]
            if prev.get("source_hash") != card.get("source_hash") and prev["status"] == "published":
                card["status"] = "needs_review"
                card["flag"] = "source_changed_after_publish"
        merged.append(card)
    save_drafts(merged)
    queue = load_queue()
    for card in merged:
        queue.setdefault("cards", {}).setdefault(card["id"], {"status": card["status"]})
        queue["cards"][card["id"]]["status"] = card["status"]
    save_queue(queue)
    return merged
