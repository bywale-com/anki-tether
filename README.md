# Anki Tether — COIS-1020 study system

Self-hosted, single-user Anki study app for a phone browser, plus a PDF flashcard pipeline for **COIS-1020H**.

The study UI uses the **official Anki Python library** (v3 scheduler). The unofficial `aitsc/ankiweb` desktop-in-a-browser port is not used; see `ARCHITECTURE.md`.

Lecture **PDFs** in `source-material/` are ingested. Matching HTML files in `source-html/` are left untouched and unused.

## Local setup

Python 3.12 is required for the study app (`anki` wheels). The pipeline can run on 3.10+ with PyMuPDF.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[app,dev]"
```

Set `STUDY_USERNAME`, a strong `STUDY_PASSWORD`, and a random `SESSION_SECRET` for study access. Set a separate random `IMPORT_TOKEN` to enable card imports. Generate random secrets with `python -c "import secrets; print(secrets.token_urlsafe(32))"`. Use `SECURE_COOKIES=false` only for local HTTP.

```bash
# Windows PowerShell
$env:STUDY_USERNAME="wale"
$env:STUDY_PASSWORD="choose-a-long-password"
$env:SESSION_SECRET="long-random"
$env:IMPORT_TOKEN="long-random"
$env:SECURE_COOKIES="false"
$env:ANKI_DATA_DIR="$PWD\data"
$env:ANKI_COLLECTION="$PWD\data\collection.anki2"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
```

On Bash, export the four credential variables, then run:

```bash
SECURE_COOKIES=false python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
```

Open http://127.0.0.1:8000 — unauthenticated visitors are sent to `/login`. `/healthz` stays public.

Docker (same single-writer model):

```bash
docker compose up --build
```

## Environment variables

| Variable | Purpose |
| --- | --- |
| `STUDY_USERNAME` / `STUDY_PASSWORD` | Required for study pages |
| `SESSION_SECRET` | Signs the session cookie |
| `IMPORT_TOKEN` | Bearer token for `POST /api/import` (GitHub Actions) |
| `ANKI_DATA_DIR` / `ANKI_COLLECTION` | Collection files (use `/data` on Railway) |
| `SECURE_COOKIES` | `true` behind HTTPS |
| `AI_API_KEY` / `AI_API_BASE_URL` / `AI_MODEL` | Optional OpenAI-compatible generation |
| `STUDY_APP_URL` | Pipeline publish target |

Never put collection files, passwords, or API keys in git.

## Source ingestion

```bash
python -m pipeline ingest          # new/changed PDFs only
python -m pipeline generate --no-ai
python -m pipeline validate
python -m pipeline coverage
python -m pipeline approve --high-confidence
python -m pipeline publish --url http://127.0.0.1:8000  # reads IMPORT_TOKEN from the environment
```

Or `python -m pipeline run --no-ai --approve-high-confidence`.

- Deterministic cards come from definitions, lists, C# samples, and `Output:` blocks.
- Independently generated practice prompts are labeled as such and are not lecture quotations.
- AI drafts (if a key is set) always need manual approval. Passing JSON validation does **not** mean an AI answer is correct.
- Optional `python -m pipeline validate --compile-csharp` uses a local `dotnet` SDK in a temp directory. It is for CI/dev, not the Railway host, and it refuses snippets that look like they touch files/network/processes.

Inspect `pipeline-data/drafts/`, `pipeline-data/reports/validation.json`, and `pipeline-data/reports/coverage.json` before publishing. PDF text extraction can omit diagrams and alter visual line breaks. Review code examples against the source pages and use the coverage report to find topics that still need cards.

## Approval and publication

Draft statuses: `draft` → `approved` / `rejected` / `invalid` / `needs_review` → `published`.

High-confidence deterministic cards can be approved in batch. For a reviewed batch, run `python -m pipeline approve --ids ID1 ID2` with the draft IDs you accept. Add `--reject` with the IDs you reject. Run `python -m pipeline publish` with `STUDY_APP_URL` and `IMPORT_TOKEN` set in the shell.

A source change invalidates the previous approval. When the regenerated question retains the same ID, publishing the newly approved draft updates the existing note. A changed question or page can produce a different ID. Review the proposed replacement and its old note before publishing. Source removal leaves existing Anki notes and review history intact.

Publication calls the running app (collection already open) rather than writing SQLite from CI:

```http
POST /api/import
Authorization: Bearer <IMPORT_TOKEN>
```

The same `guid` updates an existing note’s fields and **does not reset** scheduling.

## Railway

1. Push the application changes to the branch Railway will deploy in `bywale-com/anki-tether`.
2. Create or link a Railway service to that GitHub repository and branch. Use the Dockerfile builder.
3. In Railway, attach a **volume** to the study service and set its mount path to `/data`. Railway creates this mount from the service settings.
4. Set `STUDY_USERNAME`, `STUDY_PASSWORD`, `SESSION_SECRET`, `IMPORT_TOKEN`, `ANKI_DATA_DIR=/data`, `ANKI_COLLECTION=/data/collection.anki2`, and `SECURE_COOKIES=true` in Railway. Uvicorn binds to the injected `PORT` or falls back to 8000.
5. Generate a public HTTPS URL.
6. Confirm `/healthz` is 200 without login, and `/` redirects to `/login`.
7. Redeploy once and confirm `/data/collection.anki2` still has the same notes and `revlog` (volume, not the container filesystem).

`railway.toml` watch patterns are limited to app/pipeline/Docker files so **PDF-only commits should not redeploy** the service. Content publish is the GitHub `content-pipeline` workflow.

Keep **one replica**. Do not scale horizontally; SQLite/Anki is single-writer.

### GitHub secrets for publishing

- `STUDY_APP_URL` — Railway HTTPS origin
- `IMPORT_TOKEN` — same as Railway
- Optional `AI_API_KEY`, `AI_API_BASE_URL`, `AI_MODEL`

PDF pushes generate a `pipeline-review-batch` artifact. GitHub Actions caches extraction and draft state per branch. For explicit manual approval, download and extract the artifact into a clean checkout at the artifact's commit so its `units/`, `drafts/`, reports, and two JSON state files are under `pipeline-data/`. Re-run ingestion and validation on the current source revision before publishing if a later PDF commit has landed.

Actions → **content-pipeline** → Run workflow supports batch approval and publication of eligible deterministic drafts. Use the artifact and CLI instructions above to publish individually reviewed cards, including AI-assisted drafts. A local publication does not write back to the Actions cache. Reimporting the same GUID leaves review history intact.

## Backup and restore

Stop the application writer before taking a filesystem backup. Run this from a machine or maintenance process with access to the mounted volume:

```bash
ANKI_DATA_DIR=/data BACKUP_DIR=/path/to/backup-disk python scripts/backup_collection.py
```

Keep a copy off the Railway volume. The script includes the collection and any media files next to it.

To restore, stop the app, preserve a copy of the current files, then restore the collection and media together before restarting. Confirm the previous reviews in the stats page.

## End-to-end acceptance procedure

This has **not** been run against a live Railway project from this session.

1. Add a PDF under `source-material/` (do not edit app code).
2. Commit and push to the dedicated GitHub repo, or run **content-pipeline** manually.
3. Verify that the `pipeline-review-batch` artifact contains units from the new PDF, draft cards with page references, and the validation and coverage reports. Review the drafts against the PDF.
4. Extract the artifact into `pipeline-data/` as described above. Approve specific IDs and publish them to the Railway HTTPS origin with the CLI.
5. On your phone, open the Railway URL, sign in, study the new cards (show answer → Again/Hard/Good/Easy).
6. Restart/redeploy the Railway service. Sign in again; due/learning counts and previous reviews must still be there.

## Tests

```bash
pytest
```

Anki-backed tests skip if `anki` is not installed. Pipeline tests use the real lecture PDFs. The HTTP integration test uses a temporary Anki collection and verifies review history across app restarts.

## Course-performance reminder

The home/stats **95%** figure is first-attempt review success in a time window. It is not proof you can write C# labs. Lab prompts are intentionally unanswered.
