# Anki Tether — COIS-1020 study system

Self-hosted, single-user Anki study app for a phone browser, plus a PDF flashcard pipeline for **COIS-1020H**.

The study UI uses the **official Anki Python library** (v3 scheduler). The unofficial `aitsc/ankiweb` desktop-in-a-browser port is not used; see `ARCHITECTURE.md`.

Lecture **PDFs** in `source-material/` are ingested. Matching HTML files in `source-html/` are left untouched and unused.

## Local setup

Python 3.12 is required for the study app (`anki` wheels). The pipeline can run on 3.10+ with PyMuPDF.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -e ".[app,dev]"
copy .env.example .env   # then edit
```

Set at least `STUDY_USERNAME`, `STUDY_PASSWORD`, `SESSION_SECRET`, and `IMPORT_TOKEN`.

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
python -m pipeline publish --url http://127.0.0.1:8000 --token $env:IMPORT_TOKEN
```

Or `python -m pipeline run --no-ai --approve-high-confidence`.

- Deterministic cards come from definitions, lists, C# samples, and `Output:` blocks.
- Independently generated practice prompts are labeled as such and are not lecture quotations.
- AI drafts (if a key is set) always need manual approval. Passing JSON validation does **not** mean an AI answer is correct.
- Optional `python -m pipeline validate --compile-csharp` uses a local `dotnet` SDK in a temp directory. It is for CI/dev, not the Railway host, and it refuses snippets that look like they touch files/network/processes.

Inspect `pipeline-data/drafts/` and `pipeline-data/reports/coverage.json` before publishing.

## Approval and publication

Draft statuses: `draft` → `approved` / `rejected` / `invalid` / `needs_review` → `published`.

High-confidence **deterministic** cards can be approved in batch. Everything else should be read first.

Publication calls the running app (collection already open) rather than writing SQLite from CI:

```http
POST /api/import
Authorization: Bearer <IMPORT_TOKEN>
```

The same `guid` updates an existing note’s fields and **does not reset** scheduling.

## Railway

The Railway CLI is not installed in this environment, so production deploy is not executed here.

1. Create a GitHub repository that contains **this folder only** (do not use the parent Documents repo).
2. New Railway project from that repo. Builder: Dockerfile.
3. Add a **volume**, mount it at `/data`.
4. Set variables: `STUDY_USERNAME`, `STUDY_PASSWORD`, `SESSION_SECRET`, `IMPORT_TOKEN`, `ANKI_DATA_DIR=/data`, `ANKI_COLLECTION=/data/collection.anki2`, `SECURE_COOKIES=true`, `PORT` (Railway injects this).
5. Generate a public HTTPS URL.
6. Confirm `/healthz` is 200 without login, and `/` redirects to `/login`.
7. Redeploy once and confirm `/data/collection.anki2` still has the same notes and `revlog` (volume, not the container filesystem).

`railway.toml` watch patterns are limited to app/pipeline/Docker files so **PDF-only commits should not redeploy** the service. Content publish is the GitHub `content-pipeline` workflow.

Keep **one replica**. Do not scale horizontally; SQLite/Anki is single-writer.

### GitHub secrets for publishing

- `STUDY_APP_URL` — Railway HTTPS origin
- `IMPORT_TOKEN` — same as Railway
- Optional `AI_API_KEY`, `AI_API_BASE_URL`, `AI_MODEL`

Actions → **content-pipeline** → Run workflow → enable approve + publish when you want cards to go live.

## Backup and restore

Backup (from a machine that can see `/data`, or a Railway one-off):

```bash
python scripts/backup_collection.py
```

Or copy `/data/collection.anki2` and `/data/collection.media` off the volume.

Restore: stop the app (one writer), replace those files on the volume, start again. Do not restore while the process is open.

## End-to-end acceptance procedure

This has **not** been run against a live Railway project from this session.

1. Add a PDF under `source-material/` (do not edit app code).
2. Commit and push to the dedicated GitHub repo, or run **content-pipeline** manually.
3. Download the `pipeline-review-batch` artifact. Read drafts; reject anything inaccurate.
4. Re-run the workflow with `approve_high_confidence` and `publish` (after secrets are set), or publish locally with `python -m pipeline publish`.
5. On your phone, open the Railway URL, sign in, study the new cards (show answer → Again/Hard/Good/Easy).
6. Restart/redeploy the Railway service. Sign in again; due/learning counts and previous reviews must still be there.

## Tests

```bash
pytest
```

Anki-backed tests skip if `anki` is not installed. Pipeline tests use the real lecture PDFs.

## Course-performance reminder

The home/stats **95%** figure is first-attempt review success in a time window. It is not proof you can write C# labs. Lab prompts are intentionally unanswered.
