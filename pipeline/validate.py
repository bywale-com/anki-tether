from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from pipeline.paths import REPORTS_DIR, ensure_dirs
from pipeline.store import load_all_units, load_drafts, save_drafts, write_json

REQUIRED = ["id", "guid", "front", "back", "source_file", "origin", "kind"]


def _near_dup_key(text: str) -> str:
    norm = re.sub(r"<[^>]+>", " ", text)
    norm = re.sub(r"\s+", " ", norm).strip().lower()
    return hashlib.sha1(norm.encode()).hexdigest()


def source_matches(card: dict[str, Any], units: dict[str, dict[str, Any]]) -> bool:
    unit = units.get(card.get("unit_id"))
    return bool(
        unit
        and card.get("source_hash") == unit["source_hash"]
        and card.get("source_file") == unit["source_file"]
        and card.get("source_ref") == f"{unit['source_file']}#page-{unit['page']}"
    )


def validate(compile_csharp: bool = False) -> dict[str, Any]:
    ensure_dirs()
    cards = load_drafts()
    issues: list[dict[str, Any]] = []
    units = {unit["id"]: unit for unit in load_all_units()}
    seen_front: dict[str, str] = {}
    seen_guid: dict[str, str] = {}

    for card in cards:
        card_issues = []
        card["eligible_auto_approve"] = False
        for field in REQUIRED:
            if not card.get(field):
                card_issues.append(f"missing {field}")
        if card.get("generation_issue"):
            card_issues.append(card["generation_issue"])
        if not source_matches(card, units):
            card_issues.append("missing or stale source reference")
            card["validation"] = "failed"
            card["issues"] = card_issues
            issues.append({"id": card["id"], "issues": card_issues})
            continue
        key = _near_dup_key(card.get("front", ""))
        if key in seen_front:
            card_issues.append(f"near-duplicate of {seen_front[key]}")
        else:
            seen_front[key] = card["id"]
        guid = card.get("guid")
        if guid in seen_guid:
            card_issues.append(f"duplicate guid {guid}")
        else:
            seen_guid[guid] = card["id"]
        if compile_csharp and card.get("code_intent") == "compiles":
            snippet = _extract_code(card.get("front", ""))
            if snippet:
                if not shutil.which("dotnet"):
                    card["compile_status"] = "skipped_no_dotnet"
                result = try_compile(snippet)
                if result:
                    card_issues.append(result)
                    card["compile_status"] = "failed"
                elif shutil.which("dotnet"):
                    card["compile_status"] = "ok"
        if card_issues:
            card["validation"] = "failed"
            card["issues"] = card_issues
            if card.get("status") == "draft":
                card["status"] = "invalid"
            issues.append({"id": card["id"], "issues": card_issues})
        else:
            card["validation"] = "passed"
            card["issues"] = []
            if card.get("status") == "invalid":
                card["status"] = "draft"
            if card.get("confidence") == "high" and card.get("generation") == "deterministic" and card.get("status") == "draft":
                card["eligible_auto_approve"] = True
            if card.get("generation") == "ai":
                card["eligible_auto_approve"] = False
                card.setdefault("issues", []).append(
                    "AI draft: structural validation is not proof of lecture fidelity"
                )
    save_drafts(cards)
    report = {
        "total": len(cards),
        "passed": sum(1 for c in cards if c.get("validation") == "passed"),
        "failed": len(issues),
        "issues": issues,
    }
    write_json(REPORTS_DIR / "validation.json", report)
    return report


def _extract_code(html: str) -> str | None:
    m = re.search(r"<code>(.*?)</code>", html, re.S)
    if not m:
        return None
    text = m.group(1)
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    return text


def try_compile(snippet: str) -> str | None:
    """Compile in a throwaway directory if `dotnet` exists. Never run on an open host with untrusted IO."""
    if not shutil.which("dotnet"):
        return None
    if any(tok in snippet for tok in ("File.", "Process.", "HttpClient", "WebClient", "Socket")):
        return "refused to compile snippet with I/O or process APIs"
    wrapped = snippet
    if "Main(" not in snippet:
        wrapped = (
            "using System;\npublic class Probe {\npublic static void Main() {\n"
            + snippet
            + "\n}\n}\n"
        )
    with tempfile.TemporaryDirectory(prefix="csharp-probe-") as tmp:
        proj = Path(tmp)
        (proj / "Probe.cs").write_text(wrapped, encoding="utf-8")
        (proj / "Probe.csproj").write_text(
            """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
  </PropertyGroup>
</Project>
""",
            encoding="utf-8",
        )
        try:
            proc = subprocess.run(
                ["dotnet", "build", "--nologo", "-v", "q"],
                cwd=tmp,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return "dotnet build timed out"
        if proc.returncode != 0:
            err = (proc.stdout + proc.stderr)[-500:]
            return f"dotnet build failed: {err}"
    return None
