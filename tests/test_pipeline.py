from __future__ import annotations

import json
from pathlib import Path

from pipeline.generate import deterministic_cards, generate
from pipeline.ingest import extract_pdf, ingest, unit_id
from pipeline.validate import validate
from pipeline.coverage import coverage
from pipeline.approve import set_status
from pipeline import paths as ppaths
from pipeline import store


def test_extract_preserves_csharp(tmp_path):
    src = Path("source-material/P6ch08v5_Methods Advanced Concepts.pdf")
    result = extract_pdf(src, src.name)
    assert not result["failures"]
    code_units = [u for u in result["units"] if u["content_type"] == "code"]
    assert code_units
    joined = "\n".join(u["text"] for u in code_units)
    assert "DisplayValueParameter" in joined
    assert "Console.WriteLine" in joined
    assert "int quantity = 4;" in joined


def test_ingest_tracks_hash_and_skips_unchanged(tmp_path, monkeypatch):
    monkeypatch.setattr(ppaths, "DATA_DIR", tmp_path)
    monkeypatch.setattr(ppaths, "UNITS_DIR", tmp_path / "units")
    monkeypatch.setattr(ppaths, "DRAFTS_DIR", tmp_path / "drafts")
    monkeypatch.setattr(ppaths, "REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr(ppaths, "MANIFEST_PATH", tmp_path / "manifest.json")
    monkeypatch.setattr(store, "UNITS_DIR", tmp_path / "units")
    monkeypatch.setattr(store, "DRAFTS_DIR", tmp_path / "drafts")
    monkeypatch.setattr(store, "MANIFEST_PATH", tmp_path / "manifest.json")
    monkeypatch.setattr(store, "QUEUE_PATH", tmp_path / "review_queue.json")
    from pipeline import ingest as ingest_mod

    monkeypatch.setattr(ingest_mod, "SOURCE_DIR", Path("source-material"))
    first = ingest_mod.ingest(force=True, root=Path("source-material"))
    assert first["changed"]
    second = ingest_mod.ingest(force=False, root=Path("source-material"))
    assert second["changed"] == []
    assert second["unchanged"]


def test_malformed_pdf_is_recorded(tmp_path):
    bad = tmp_path / "broken.pdf"
    bad.write_bytes(b"not a pdf")
    result = extract_pdf(bad, "broken.pdf")
    assert result["failures"]
    assert result["units"] == []


def test_generate_traceability_and_independent_label(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "UNITS_DIR", tmp_path / "units")
    monkeypatch.setattr(store, "DRAFTS_DIR", tmp_path / "drafts")
    monkeypatch.setattr(store, "QUEUE_PATH", tmp_path / "q.json")
    (tmp_path / "units").mkdir()
    src = Path("source-material/P4ch05v2__Loops.pdf")
    units = extract_pdf(src, src.name)["units"]
    store.save_units(units)
    cards = generate(include_ai=False)
    assert cards
    lecture = [c for c in cards if c["origin"] == "lecture"]
    independent = [c for c in cards if c["origin"] == "independent_exercise"]
    assert lecture
    assert all(c.get("source_ref") for c in lecture)
    assert independent
    assert all("not lecture" in c["front"].lower() or "Independent" in c["front"] for c in independent)


def test_duplicate_detection_and_reprocess(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "UNITS_DIR", tmp_path / "units")
    monkeypatch.setattr(store, "DRAFTS_DIR", tmp_path / "drafts")
    monkeypatch.setattr(store, "QUEUE_PATH", tmp_path / "q.json")
    from pipeline import paths as paths_mod
    from pipeline import validate as validate_mod

    monkeypatch.setattr(paths_mod, "REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr(validate_mod, "REPORTS_DIR", tmp_path / "reports")
    src = Path("source-material/P1ch01v3_Introduction.pdf")
    units = extract_pdf(src, src.name)["units"]
    store.save_units(units)
    first = generate(include_ai=False)
    ids = {c["id"] for c in first}
    second = generate(include_ai=False)
    assert {c["id"] for c in second} == ids
    report = validate()
    assert report["total"] == len(second)


def test_coverage_report(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "UNITS_DIR", tmp_path / "units")
    monkeypatch.setattr(store, "DRAFTS_DIR", tmp_path / "drafts")
    monkeypatch.setattr(store, "QUEUE_PATH", tmp_path / "q.json")
    from pipeline import coverage as cov_mod
    from pipeline import paths as paths_mod

    monkeypatch.setattr(paths_mod, "REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr(cov_mod, "REPORTS_DIR", tmp_path / "reports")
    src = Path("source-material/P5ch07_Methods.pdf")
    store.save_units(extract_pdf(src, src.name)["units"])
    generate(include_ai=False)
    report = coverage()
    assert report["sections"] > 0
    assert "covered" in report


def test_approve_high_confidence(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "UNITS_DIR", tmp_path / "units")
    monkeypatch.setattr(store, "DRAFTS_DIR", tmp_path / "drafts")
    monkeypatch.setattr(store, "QUEUE_PATH", tmp_path / "q.json")
    from pipeline import validate as validate_mod
    from pipeline import paths as paths_mod

    monkeypatch.setattr(paths_mod, "REPORTS_DIR", tmp_path / "reports")
    monkeypatch.setattr(validate_mod, "REPORTS_DIR", tmp_path / "reports")
    src = Path("source-material/P2ch02v2_Variables.pdf")
    store.save_units(extract_pdf(src, src.name)["units"])
    generate(include_ai=False)
    validate()
    result = set_status(None, "approved", high_confidence_only=True)
    assert result["changed"] >= 0
    approved = [c for c in store.load_drafts() if c["status"] == "approved"]
    for card in approved:
        assert card.get("eligible_auto_approve")


def test_unit_ids_stable():
    a = unit_id("f", 1, 0, "heading", "Hello")
    b = unit_id("f", 1, 0, "heading", "Hello")
    assert a == b


def test_changed_pdf_requires_new_approval_and_invalidates_stale_units(tmp_path, monkeypatch):
    import pymupdf

    from pipeline.approve import approved_cards
    from pipeline import validate as validate_mod

    for module, name, filename in (
        (store, "MANIFEST_PATH", "manifest.json"),
        (store, "QUEUE_PATH", "review_queue.json"),
        (store, "UNITS_DIR", "units"),
        (store, "DRAFTS_DIR", "drafts"),
        (validate_mod, "REPORTS_DIR", "reports"),
    ):
        monkeypatch.setattr(module, name, tmp_path / filename)

    sources = tmp_path / "sources"
    sources.mkdir()
    pdf = sources / "lesson.pdf"

    def write_pdf(definition, extra):
        with pymupdf.open() as doc:
            page = doc.new_page()
            page.insert_text((50, 50), f"Iteration\nA loop is a control structure that {definition}.\n{extra}")
            doc.save(pdf)

    write_pdf("repeats a sequence", "A branch is an alternate execution path.")
    assert ingest(root=sources)["changed"] == ["lesson.pdf"]
    generate(include_ai=False)
    validate()
    card = next(c for c in store.load_drafts() if c["front"] == "What is A loop?")
    assert set_status([card["id"]], "approved")["changed"] == 1

    write_pdf("repeats a block of statements", "")
    assert ingest(root=sources)["changed"] == ["lesson.pdf"]
    assert not approved_cards()
    assert all("alternate execution" not in u["text"] for u in store.load_all_units())
    generate(include_ai=False)
    validate()
    revised = next(c for c in store.load_drafts() if c["id"] == card["id"])
    assert revised["guid"] == card["guid"]
    assert revised["status"] == "needs_review"
    assert "repeats a block of statements" in revised["back"]
    assert not revised["eligible_auto_approve"]
    assert set_status([revised["id"]], "approved")["changed"] == 1
