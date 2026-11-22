from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Annotated, Any

from fastapi import FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, BeforeValidator, Field

from app import auth, collection, config

templates = Jinja2Templates(directory="app/templates")
DeckFilter = Annotated[
    Annotated[int, Field(ge=1, le=2**63 - 1)] | None,
    BeforeValidator(lambda value: None if value == "" else value),
]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    yield
    collection.close_collection()


app = FastAPI(title="Anki Tether", docs_url=None, redoc_url=None, lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


class ImportCard(BaseModel):
    front: str = Field(min_length=1)
    back: str = Field(min_length=1)
    guid: str | None = None
    deck: str | None = None
    source_file: str | None = None
    source_ref: str | None = None
    origin: str | None = None
    tags: list[str] = Field(default_factory=list)


class ImportPayload(BaseModel):
    cards: list[ImportCard] = Field(default_factory=list)


def _auth_or_login(request: Request):
    if not config.auth_configured():
        return None, JSONResponse(
            {"error": "Set STUDY_USERNAME, STUDY_PASSWORD, and SESSION_SECRET before accessing study data."},
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
        request=request,
        name="login.html",
        context={"error": error, "csrf": request.cookies.get(auth.CSRF_COOKIE, "")},
    )


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if not auth.credentials_valid(username, password):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={ "error": "Invalid username or password.", "csrf": ""},
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
        request=request,
        name="home.html",
        context={
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
        request=request,
        name="review.html",
        context={
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


@app.get("/browse", response_class=HTMLResponse)
def browse(
    request: Request,
    deck: DeckFilter = None,
    q: str = Query("", max_length=150),
    page: int = Query(1, ge=1),
):
    user, err = _auth_or_login(request)
    if err:
        return err
    query = q.strip()
    result = collection.browse_cards(deck, query, page)
    if result is None:
        raise HTTPException(404, "Deck not found")
    filters = {"q": query, "page": result["page"]}
    if deck is not None:
        filters["deck"] = deck
    return templates.TemplateResponse(
        request=request,
        name="browse.html",
        context={"user": user, "result": result, "deck": deck, "query": query, "filters": filters},
    )


@app.get("/browse/{card_id}", response_class=HTMLResponse)
def browse_detail(
    request: Request,
    card_id: int,
    deck: DeckFilter = None,
    q: str = Query("", max_length=150),
    page: int = Query(1, ge=1),
):
    user, err = _auth_or_login(request)
    if err:
        return err
    card = collection.browse_card(card_id) if 0 < card_id < 2**63 else None
    if card is None:
        raise HTTPException(404, "Card not found")
    filters = {"q": q, "page": page}
    if deck is not None:
        filters["deck"] = deck
    return templates.TemplateResponse(
        request=request,
        name="browse_detail.html",
        context={"user": user, "card": card, "filters": filters},
    )


@app.get("/stats", response_class=HTMLResponse)
def stats_page(request: Request, days: int = 7):
    user, err = _auth_or_login(request)
    if err:
        return err
    return templates.TemplateResponse(
        request=request,
        name="stats.html",
        context={
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
    if not config.IMPORT_TOKEN or not hmac.compare_digest(token.encode(), config.IMPORT_TOKEN.encode()):
        raise HTTPException(status_code=401, detail="Invalid import token")
    if not payload.cards:
        return {"ok": True, "created": 0, "updated": 0, "skipped": 0, "total": 0}
    result = collection.upsert_notes([card.model_dump(exclude_none=True) for card in payload.cards])
    return {"ok": True, **result}


@app.get("/source")
def source_notice():
    return {
        "license": "AGPL-3.0-or-later",
        "note": "This service links the official Anki Python library. Corresponding source is the Git repository that built this image.",
    }
