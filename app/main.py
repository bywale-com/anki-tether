from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app import auth, collection, config

templates = Jinja2Templates(directory="app/templates")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    yield
    collection.close_collection()


app = FastAPI(title="Anki Tether", docs_url=None, redoc_url=None, lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


class ImportPayload(BaseModel):
    cards: list[dict[str, Any]] = Field(default_factory=list)


def _auth_or_login(request: Request):
    if not config.auth_configured():
        return None, JSONResponse(
            {"error": "Set STUDY_USERNAME and STUDY_PASSWORD before accessing study data."},
            status_code=503,
        )
    user = auth.current_user(request)
    if not user:
        return None, auth.login_redirect()
    return user, None


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request, error: str | None = None):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": error, "csrf": request.cookies.get(auth.CSRF_COOKIE, "")},
    )


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if not auth.credentials_valid(username, password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password.", "csrf": ""},
            status_code=401,
        )
    response = RedirectResponse("/", status_code=303)
    auth.set_session(response, username)
    return response


@app.post("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    auth.clear_session(response)
    return response


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user, err = _auth_or_login(request)
    if err:
        return err
    decks = collection.deck_summaries()
    stats = collection.stats_summary()
    perf = collection.performance(7)
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "user": user,
            "decks": decks,
            "stats": stats,
            "perf": perf,
            "csrf": request.cookies.get(auth.CSRF_COOKIE, ""),
        },
    )


@app.post("/study/{deck_id}")
def start_study(request: Request, deck_id: int, csrf: str = Form("")):
    user, err = _auth_or_login(request)
    if err:
        return err
    auth.verify_csrf(request, csrf)
    collection.select_deck(deck_id)
    return RedirectResponse("/review", status_code=303)


@app.get("/review", response_class=HTMLResponse)
def review(request: Request, show: int = 0):
    user, err = _auth_or_login(request)
    if err:
        return err
    payload = collection.next_card()
    return templates.TemplateResponse(
        "review.html",
        {
            "request": request,
            "user": user,
            "payload": payload,
            "show_answer": bool(show) and payload and not payload.get("done"),
            "csrf": request.cookies.get(auth.CSRF_COOKIE, ""),
        },
    )


@app.post("/review/answer")
def review_answer(
    request: Request,
    card_id: int = Form(...),
    rating: str = Form(...),
    csrf: str = Form(""),
):
    user, err = _auth_or_login(request)
    if err:
        return err
    auth.verify_csrf(request, csrf)
    try:
        collection.answer_card(card_id, rating)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    return RedirectResponse("/review", status_code=303)


@app.get("/stats", response_class=HTMLResponse)
def stats_page(request: Request, days: int = 7):
    user, err = _auth_or_login(request)
    if err:
        return err
    return templates.TemplateResponse(
        "stats.html",
        {
            "request": request,
            "user": user,
            "stats": collection.stats_summary(),
            "perf": collection.performance(days),
            "csrf": request.cookies.get(auth.CSRF_COOKIE, ""),
        },
    )


@app.post("/api/import")
def import_cards(request: Request, payload: ImportPayload):
    import hmac

    header = request.headers.get("authorization", "")
    token = header.removeprefix("Bearer ").strip()
    if not config.IMPORT_TOKEN or not hmac.compare_digest(token, config.IMPORT_TOKEN):
        raise HTTPException(status_code=401, detail="Invalid import token")
    if not payload.cards:
        return {"ok": True, "created": 0, "updated": 0, "skipped": 0, "total": 0}
    result = collection.upsert_notes(payload.cards)
    return {"ok": True, **result}


@app.get("/source")
def source_notice():
    return {
        "license": "AGPL-3.0-or-later",
        "note": "This service links the official Anki Python library. Corresponding source is the Git repository that built this image.",
    }
