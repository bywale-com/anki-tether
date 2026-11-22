"""Validate and publish Git-reviewed flashcard batches through the existing import API."""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

import httpx
from jsonschema import Draft202012Validator

from app.card_format import CARD_HTML_TAGS, MATH_DELIMITER

ROOT = Path(__file__).resolve().parents[1] / "cards"
MAX_FILE_BYTES = 512 * 1024
MAX_REQUEST_BYTES = 256 * 1024
VOID_TAGS = {"br", "hr"}
DECK_SEGMENT = re.compile(r"[\w][\w .(),&+'’/-]*")
COUNTS = ("created", "updated", "skipped")


class FlashcardText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.parts = []
        self.next_delimiter = None

    def handle_starttag(self, tag, attrs):
        if tag not in CARD_HTML_TAGS or attrs or self.next_delimiter is not None:
            raise ValueError("unsupported HTML or a tag inside a math expression")
        if tag not in VOID_TAGS:
            self.tags.append(tag)

    def handle_startendtag(self, tag, attrs):
        if tag not in VOID_TAGS:
            raise ValueError("only br and hr may be self-closing")
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if not self.tags or self.tags.pop() != tag or self.next_delimiter is not None:
            raise ValueError("unbalanced HTML")

    def handle_comment(self, data):
        raise ValueError("HTML comments are unsupported")

    def handle_decl(self, decl):
        raise ValueError("HTML declarations are unsupported")

    def handle_pi(self, data):
        raise ValueError("HTML processing instructions are unsupported")

    def unknown_decl(self, data):
        raise ValueError("HTML declarations are unsupported")

    def handle_data(self, data):
        self.parts.append(data)
        if {"code", "pre"}.intersection(self.tags):
            return
        start = None
        for token in MATH_DELIMITER.finditer(data):
            delimiter = token.group()
            if delimiter == r"\\":
                continue
            if delimiter in (r"\(", r"\[") and self.next_delimiter is None:
                self.next_delimiter = r"\)" if delimiter == r"\(" else r"\]"
                start = token.end()
            elif delimiter == self.next_delimiter and start is not None and data[start:token.start()].strip():
                if token.start() - start > 4000:
                    raise ValueError("math expression exceeds 4000 characters")
                self.next_delimiter = None
            else:
                raise ValueError("unbalanced or empty math delimiters")
        if self.next_delimiter is not None:
            raise ValueError("unclosed math expression")


def validate_text(text: str):
    parser = FlashcardText()
    parser.feed(text)
    parser.close()
    if parser.tags or not "".join(parser.parts).strip():
        raise ValueError("unclosed HTML or empty card text")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object member")
        result[key] = value
    return result


def invalid_constant(value):
    raise ValueError(f"invalid JSON constant {value}")


def read_json(path):
    with path.open("rb") as file:
        data = file.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("JSON file exceeds 512 KiB")
    document = json.loads(data.decode("utf-8"), object_pairs_hook=unique_object, parse_constant=invalid_constant)
    json.dumps(document, ensure_ascii=False).encode("utf-8")
    return document


def load_cards(root: Path | None = None) -> list[dict]:
    root = root or ROOT
    validator = Draft202012Validator(read_json(root / "schema.json"))
    cards = []
    seen = set()
    for path in sorted(root.rglob("*.json")):
        if path == root / "schema.json":
            continue
        try:
            batch = read_json(path)
            error = next(validator.iter_errors(batch), None)
            if error:
                location = ".".join(map(str, error.absolute_path)) or "batch"
                raise ValueError(f"{location} violates schema rule {error.validator}")
            course = batch["course"]
            deck = batch["deck"]
            segments = deck.split("::")
            if segments[0] != course or any(
                part != part.strip() or not DECK_SEGMENT.fullmatch(part) for part in segments
            ):
                raise ValueError("deck must start with the course and contain valid Anki deck segments")
            for card in batch["cards"]:
                card_id = card["id"]
                if card_id in seen:
                    raise ValueError(f"duplicate card ID: {card_id}")
                if len({tag.casefold() for tag in card.get("tags", [])}) != len(card.get("tags", [])):
                    raise ValueError(f"{card_id}: duplicate case-insensitive tags")
                for side in ("front", "back"):
                    try:
                        validate_text(card[side])
                    except ValueError as exc:
                        raise ValueError(f"{card_id} {side}: {exc}") from exc
                seen.add(card_id)
                digest = hashlib.sha256(card_id.encode("ascii")).hexdigest()
                cards.append({
                    "guid": f"authored-{digest}",
                    "deck": deck,
                    "front": card["front"],
                    "back": card["back"],
                    "origin": "authored",
                    "tags": card.get("tags", []),
                    "source_ref": card.get("source_ref") or course,
                })
        except (ValueError, UnicodeError, RecursionError, OSError) as exc:
            raise ValueError(f"{path.relative_to(root)}: {exc}") from exc
    return cards


def requests_for(cards):
    chunk = []
    size = len(b'{"cards":[]}')
    for card in cards:
        encoded = json.dumps(card, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        if len(encoded) + len(b'{"cards":[]}') > MAX_REQUEST_BYTES:
            raise ValueError("one card exceeds the request size limit")
        if chunk and size + len(encoded) + 1 > MAX_REQUEST_BYTES:
            yield len(chunk), b'{"cards":[' + b",".join(chunk) + b"]}"
            chunk = []
            size = len(b'{"cards":[]}')
        size += len(encoded) + bool(chunk)
        chunk.append(encoded)
    if chunk:
        yield len(chunk), b'{"cards":[' + b",".join(chunk) + b"]}"


def publish(cards, url, token, client):
    destination = urlsplit(url)
    if (destination.scheme != "https" and not (
        destination.scheme == "http" and destination.hostname in {"127.0.0.1", "::1", "localhost"}
    )) or not destination.hostname or destination.username is not None or destination.query or destination.fragment:
        raise ValueError("STUDY_APP_URL must be an HTTPS service URL (HTTP is allowed for loopback tests)")
    if not token:
        raise ValueError("IMPORT_TOKEN is required")
    totals = dict.fromkeys(COUNTS, 0)
    for count, body in requests_for(cards):
        try:
            response = client.post(
                url.rstrip("/") + "/api/import", content=body,
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            )
            response.raise_for_status()
            result = response.json()
            if (not isinstance(result, dict) or result.get("ok") is not True or result.get("total") != count
                or any(type(result.get(key)) is not int or result[key] < 0 for key in COUNTS)
                or sum(result[key] for key in COUNTS) != count):
                raise ValueError("invalid import acknowledgement")
        except (httpx.HTTPError, httpx.InvalidURL, ValueError) as exc:
            reason = f"HTTP {exc.response.status_code}" if isinstance(exc, httpx.HTTPStatusError) else type(exc).__name__
            print(json.dumps({**totals, "failed": count, "not_attempted": len(cards) - sum(totals.values()) - count}))
            raise ValueError(f"Import batch was not acknowledged ({reason}). Retry is safe.") from None
        for key in COUNTS:
            totals[key] += result[key]
    return {**totals, "failed": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "publish"))
    args = parser.parse_args()
    try:
        cards = load_cards()
        if args.command == "validate":
            print(f"Validated {len(cards)} authored cards")
        else:
            with httpx.Client(timeout=60, follow_redirects=False, trust_env=False) as client:
                print(json.dumps(publish(cards, os.getenv("STUDY_APP_URL", ""), os.getenv("IMPORT_TOKEN", ""), client)))
    except (ValueError, OSError) as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
