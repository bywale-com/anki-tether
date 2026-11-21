from __future__ import annotations

import hashlib
import re
from html import unescape
from pathlib import Path
from typing import Any

import pymupdf

from pipeline.paths import SOURCE_DIR, ensure_dirs
from pipeline.store import load_all_units, load_manifest, save_manifest, save_units, unit_path

CODE_HINT = re.compile(
    r"^\s*(using\s+System|namespace\s+|public\s+|private\s+|protected\s+|static\s+|"
    r"class\s+|void\s+|int\s+|string\s+|bool\s+|double\s+|char\s+|if\s*\(|for\s*\(|"
    r"while\s*\(|foreach\s*\(|switch\s*\(|return\s+|Console\.|new\s+|\{|\}|;)\s*",
    re.I,
)
OUTPUT_HINT = re.compile(r"^\s*output\s*:?\s*$", re.I)


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def unit_id(source: str, page: int, index: int, kind: str, text: str) -> str:
    raw = f"{source}|{page}|{index}|{kind}|{text[:80]}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def _clean(text: str) -> str:
    text = unescape(text.replace("\xa0", " "))
    text = text.replace("\ufffd", "'")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def _is_code_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if CODE_HINT.match(s):
        return True
    if s in {"{", "}"}:
        return True
    if s.endswith(";") and any(ch.isalpha() for ch in s):
        return True
    return False


def extract_pdf(path: Path, rel: str) -> dict[str, Any]:
    failures: list[str] = []
    units: list[dict[str, Any]] = []
    try:
        doc = pymupdf.open(path)
    except Exception as exc:  # noqa: BLE001
        return {"source": rel, "units": [], "failures": [f"open failed: {exc}"]}

    source_hash = file_hash(path)
    chapter = _clean(path.stem)
    for page_index, page in enumerate(doc):
        try:
            text = page.get_text("text")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{rel}:p{page_index + 1}: {exc}")
            continue
        if not text:
            continue
        lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
        heading = _clean(lines[0]) if lines else f"Page {page_index + 1}"
        # Skip slide numbers that are the only extra content
        body_lines = [ln for ln in lines[1:] if not re.fullmatch(r"\d{1,3}", ln.strip())]
        units.extend(
            _units_from_lines(
                rel=rel,
                source_hash=source_hash,
                chapter=chapter,
                page=page_index + 1,
                heading=heading,
                lines=body_lines or lines,
            )
        )
    doc.close()
    return {"source": rel, "units": units, "failures": failures, "source_hash": source_hash}


def _units_from_lines(
    rel: str,
    source_hash: str,
    chapter: str,
    page: int,
    heading: str,
    lines: list[str],
) -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []
    buf: list[str] = []
    mode = "text"

    def flush():
        nonlocal buf, mode
        if not buf:
            return
        text = "\n".join(buf).strip()
        if not text:
            buf = []
            return
        kind = "code" if mode == "code" else "output" if mode == "output" else _classify_text(heading, text)
        uid = unit_id(rel, page, len(units), kind, text)
        units.append(
            {
                "id": uid,
                "source_file": rel.replace("\\", "/"),
                "source_hash": source_hash,
                "chapter": chapter,
                "section": heading,
                "page": page,
                "anchor": f"page-{page}",
                "content_type": kind,
                "text": text,
                "code_intent": _code_intent(kind, text),
                "status": "extracted",
            }
        )
        buf = []

    heading_unit = {
        "id": unit_id(rel, page, 0, "heading", heading),
        "source_file": rel.replace("\\", "/"),
        "source_hash": source_hash,
        "chapter": chapter,
        "section": heading,
        "page": page,
        "anchor": f"page-{page}",
        "content_type": "heading",
        "text": heading,
        "code_intent": "none",
        "status": "extracted",
    }
    units.append(heading_unit)

    for line in lines:
        if OUTPUT_HINT.match(line):
            flush()
            mode = "output"
            continue
        if _is_code_line(line) and mode != "output":
            if mode != "code":
                flush()
                mode = "code"
            buf.append(line)
            continue
        if mode in {"code", "output"} and not _is_code_line(line) and mode != "output":
            flush()
            mode = "text"
        if mode == "output":
            buf.append(line)
            continue
        buf.append(line)
        mode = "text"
    flush()
    return units


def _classify_text(heading: str, text: str) -> str:
    blob = f"{heading}\n{text}".lower()
    if any(k in blob for k in ("exercise", "lab", "hands dirty", "practice", "your turn")):
        return "exercise"
    if text.count("\n") >= 2 and all(len(ln) < 160 for ln in text.splitlines()[:8]):
        return "list"
    return "paragraph"


def _code_intent(kind: str, text: str) -> str:
    if kind != "code":
        return "none"
    lowered = text.lower()
    if any(k in lowered for k in ("error", "will not compile", "invalid", "does not compile")):
        return "error_demo"
    if "pseudo" in lowered:
        return "pseudocode"
    return "compiles"


def discover_pdfs(root: Path | None = None) -> list[Path]:
    base = root or SOURCE_DIR
    return sorted(p for p in base.rglob("*.pdf") if p.is_file())


def ingest(force: bool = False, root: Path | None = None) -> dict[str, Any]:
    ensure_dirs()
    manifest = load_manifest()
    changed: list[str] = []
    unchanged: list[str] = []
    failures: list[str] = []
    all_units: list[dict[str, Any]] = []
    files_meta = manifest.setdefault("files", {})

    previous_units = load_all_units()
    sources = {path.relative_to(root or SOURCE_DIR).as_posix(): path for path in discover_pdfs(root)}
    removed = sorted(set(files_meta) - sources.keys())
    replaced = set(removed)
    for rel in removed:
        del files_meta[rel]
    for rel, path in sources.items():
        digest = file_hash(path)
        prev = files_meta.get(rel)
        if not force and prev and prev.get("sha256") == digest:
            unchanged.append(rel)
            continue
        result = extract_pdf(path, rel)
        failures.extend(result["failures"])
        replaced.add(rel)
        if result["failures"]:
            files_meta.pop(rel, None)
            continue
        save_units(result["units"])
        all_units.extend(result["units"])
        files_meta[rel] = {
            "sha256": digest,
            "unit_count": len(result["units"]),
            "pages": len({unit["page"] for unit in result["units"]}),
        }
        changed.append(rel)

    current_ids = {unit["id"] for unit in all_units}
    for unit in previous_units:
        if unit["source_file"] in replaced and unit["id"] not in current_ids:
            unit_path(unit["id"]).unlink(missing_ok=True)
    save_manifest(manifest)
    return {
        "changed": changed,
        "unchanged": unchanged,
        "removed": removed,
        "failures": failures,
        "units_written": len(all_units),
    }
