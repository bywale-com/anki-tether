# Architecture

Personal COIS-1020 study tool: official Anki scheduling in a small authenticated browser UI, plus a GitHub-driven PDF → card pipeline.

## Why not aitsc/ankiweb?

The unofficial [aitsc/ankiweb](https://github.com/aitsc/ankiweb) port *does* wrap Anki’s Python library and FastAPI, and it reuses the real desktop reviewer. It is still a poor foundation for this project:

- It is documented as **single-user, local-first, LAN-ready**, not a hardened public service.
- It exposes a **full AnkiConnect write API** on a second port — unsafe on a public Railway URL without a large security retrofit.
- It vendors Anki’s compiled desktop frontend (version-pinned to `anki==25.9.4` + matching `aqt` assets). That UI is not built for one-handed phone use.
- Setup needs Python 3.12, fetching web assets, and a Node shell bundle. Maintenance tracks a hobby port (AGPL, trademark-colliding name, no affiliation with Ankitects).
- Password auth is described by the author as a **light LAN gate**.

Adapting it for Railway would mean stripping AnkiConnect, rebuilding CSS for mobile, locking workers, and owning an unofficial fork. That is more work and more risk than a thin official pylib wrapper.

Official **desktop Anki** is not converted into a web app here.

## Chosen components

| Piece | Role | Why it exists |
| --- | --- | --- |
| Official `anki` Python package (pylib + Rust backend) | Collection, v3 scheduler, revlog | Native Anki card semantics; no custom SRS |
| FastAPI + Jinja + one CSS file | Login, decks, review, stats | Small enough to make touch targets and code wrapping work on a phone |
| SQLite collection on a Railway volume at `/data` | Persistence | Anki’s own file; survives redeploy if the volume is mounted |
| Uvicorn `--workers 1` + process lock | Single writer | Anki collections are not safe for concurrent writers |
| `pipeline/` CLI | PDF ingest → JSON IR → cards → validate → approve | Content changes must not require app code changes |
| GitHub Actions `content-pipeline.yml` | Runs on `source-material/**` or workflow_dispatch | Source of truth for new lectures; does not rebuild Railway |
| Authenticated `POST /api/import` | Publish approved cards into the live collection | Same process that serves reviews, so the collection is already open |

AI card generation is optional (`AI_API_KEY`). Deterministic cards run without a model.

## Content path

Lecture **PDFs** under `source-material/` are the source of truth (PowerPoint exports). HTML correlates exist under `source-html/` and are **not** ingested — they are accessibility dumps of the same slides, with code split across `<p>` tags.

`HTML/PDF source → extract units JSON → generate drafts → validate → approve → POST /api/import`

Stable `guid` values update existing notes instead of duplicating them. Review history stays on the cards. If a published note’s source hash changes, the draft is flagged `needs_review`.

## 95% metric

**First-attempt success:** among cards that have at least one `revlog` entry in the selected window (default 7 days), the share whose *first* rating in that window is Hard, Good, or Easy (not Again).

This is not FSRS predicted retention. Completing programming labs independently is a separate criterion and is not computed from flashcard scores.

## Licensing

Linking Anki pylib makes the running service AGPL-3.0-or-later. `/source` points at the corresponding source.
