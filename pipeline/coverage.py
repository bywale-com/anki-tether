from __future__ import annotations

from collections import defaultdict
from typing import Any

from pipeline.paths import REPORTS_DIR
from pipeline.store import load_all_units, load_drafts, write_json


def coverage() -> dict[str, Any]:
    units = load_all_units()
    cards = load_drafts()
    by_section: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"units": 0, "cards": 0, "source_file": "", "pages": set()}
    )
    unit_ids_with_cards = {c.get("unit_id") for c in cards}
    for unit in units:
        key = f"{unit['source_file']}::{unit['section']}"
        row = by_section[key]
        row["units"] += 1
        row["source_file"] = unit["source_file"]
        row["pages"].add(unit["page"])
        row["section"] = unit["section"]
        if unit["id"] in unit_ids_with_cards:
            row["cards"] += 1
    rows = []
    missing = []
    for key, row in sorted(by_section.items()):
        rec = {
            "key": key,
            "section": row["section"],
            "source_file": row["source_file"],
            "units": row["units"],
            "cards": row["cards"],
            "pages": sorted(row["pages"]),
        }
        rows.append(rec)
        if rec["cards"] == 0:
            missing.append(rec)
    report = {
        "sections": len(rows),
        "covered": sum(1 for r in rows if r["cards"] > 0),
        "unaddressed": missing,
        "rows": rows,
    }
    write_json(REPORTS_DIR / "coverage.json", report)
    return report
