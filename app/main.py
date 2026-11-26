from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Annotated, Any, Literal
from uuid import UUID, uuid4

from fastapi import FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, BeforeValidator, Field

from app import auth, collection, config, timed

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["flag_reasons"] = collection.FLAG_REASONS


def _duration(milliseconds: int) -> str:
    minutes, seconds = divmod(milliseconds // 1000, 60)
    hours, minutes = divmod(minutes, 60)
    prefix = f"{hours:02}:" if hours else ""
    return f"{prefix}{minutes:02}:{seconds:02}"


templates.env.filters["duration"] = _duration
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
    response.delete_cookie(REVIEW_CURSOR_COOKIE)
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


def _timed_redirect():
    session_id = timed.active_id()
    if session_id:
        return RedirectResponse(f"/timed/{session_id}", status_code=303)
    return None


def _timed_page(request, user, template, **context):
    return templates.TemplateResponse(request=request, name=template, context={
        "user": user, "csrf": request.cookies.get(auth.CSRF_COOKIE, ""),
        "modes": timed.MODES, **context,
    }, headers={"Cache-Control": "no-store"})


@app.get("/study/{deck_id}/timed", response_class=HTMLResponse)
def timed_setup(request: Request, deck_id: int):
    user, err = _auth_or_login(request)
    if err:
        return err
    active = _timed_redirect()
    if active:
        return active
    details = timed.setup(deck_id) if 0 < deck_id < 2**63 else None
    if not details:
        raise HTTPException(404, "Deck not found")
    title, eligible = details
    return _timed_page(request, user, "timed_setup.html", title=title, eligible=eligible,
                       deck_id=deck_id, attempt=uuid4().hex)


@app.post("/study/{deck_id}/timed")
def timed_start(
    request: Request, deck_id: int, attempt: UUID = Form(...),
    mode: Literal["countdown", "stopwatch"] = Form(...),
    target: str = Form(""), minutes: int | None = Form(None), csrf: str = Form(""),
):
    _, err = _auth_or_login(request)
    if err:
        return err
    auth.verify_csrf(request, csrf)
    active = _timed_redirect()
    if active:
        return active
    try:
        if not 0 < deck_id < 2**63:
            raise LookupError("Deck not found")
        session_id = timed.start(deck_id, attempt.hex, mode, int(target) if target else None, minutes)
    except LookupError as exc:
        raise HTTPException(404, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    return RedirectResponse(f"/timed/{session_id}", status_code=303)


@app.get("/timed/{session_id}", response_class=HTMLResponse)
def timed_review(request: Request, session_id: UUID, show: bool = False):
    user, err = _auth_or_login(request)
    if err:
        return err
    session = timed.snapshot(session_id.hex, review=True)
    if not session:
        raise HTTPException(404, "Timed session not found")
    return _timed_page(request, user, "timed_review.html", session=session, show=show)


@app.post("/timed/{session_id}")
def timed_action(
    request: Request, session_id: UUID,
    action: Literal["rate", "undo", "pause", "resume", "stop"] = Form(...),
    nonce: UUID = Form(...), card_id: int | None = Form(None),
    rating: Literal["again", "hard", "good", "easy"] | None = Form(None), csrf: str = Form(""),
):
    _, err = _auth_or_login(request)
    if err:
        return err
    auth.verify_csrf(request, csrf)
    try:
        timed.act(session_id.hex, action, nonce.hex, card_id, rating)
    except LookupError as exc:
        raise HTTPException(404, str(exc)) from exc
    return RedirectResponse(f"/timed/{session_id.hex}", status_code=303)


@app.get("/time-board", response_class=HTMLResponse)
def time_board(request: Request, deck: DeckFilter = None,
               mode: Literal["", "countdown", "stopwatch"] = "", target: DeckFilter = None):
    user, err = _auth_or_login(request)
    if err:
        return err
    return _timed_page(request, user, "time_board.html", board=timed.board(deck, mode, target),
                       deck=deck, mode=mode, target=target)


REVIEW_CURSOR_COOKIE = "anki_review_cursor"


def _begin_review(location: str) -> RedirectResponse:
    response = RedirectResponse(location, status_code=303)
    response.set_cookie(
        REVIEW_CURSOR_COOKIE, str(collection.review_cursor()),
        httponly=True, secure=config.SECURE_COOKIES, samesite="lax",
    )
    return response


@app.post("/study/{deck_id}")
def start_study(request: Request, deck_id: int, csrf: str = Form("")):
    user, err = _auth_or_login(request)
    if err:
        return err
    auth.verify_csrf(request, csrf)
    active = _timed_redirect()
    if active:
        return active
    collection.select_deck(deck_id)
    return _begin_review("/review")


@app.post("/study")
def start_due(request: Request, csrf: str = Form("")):
    _, err = _auth_or_login(request)
    if err:
        return err
    auth.verify_csrf(request, csrf)
    active = _timed_redirect()
    if active:
        return active
    return _begin_review("/review?all_due=1")


@app.get("/review", response_class=HTMLResponse)
def review(request: Request, show: int = 0, all_due: bool = False):
    user, err = _auth_or_login(request)
    if err:
        return err
    active = _timed_redirect()
    if active:
        return active
    payload = collection.next_card(all_due=True) if all_due else collection.next_card()
    cursor = request.cookies.get(REVIEW_CURSOR_COOKIE, "")
    fresh = not (cursor.isascii() and cursor.isdecimal() and len(cursor) <= 16)
    after = collection.review_cursor() if fresh else int(cursor)
    summary = collection.session_summary(after) if payload and payload["done"] else None
    response = templates.TemplateResponse(
        request=request,
        name="review.html",
        context={
            "user": user,
            "payload": payload,
            "all_due": all_due,
            "summary": summary,
            "can_undo": collection.can_undo_review(),
            "show_answer": bool(show) and payload and not payload.get("done"),
            "csrf": request.cookies.get(auth.CSRF_COOKIE, ""),
        },
    )
    if fresh:
        response.set_cookie(
            REVIEW_CURSOR_COOKIE, str(after), httponly=True,
            secure=config.SECURE_COOKIES, samesite="lax",
        )
    return response


@app.post("/review/answer")
def review_answer(
    request: Request,
    card_id: int = Form(...),
    rating: str = Form(...),
    all_due: bool = Form(False),
    csrf: str = Form(""),
):
    user, err = _auth_or_login(request)
    if err:
        return err
    auth.verify_csrf(request, csrf)
    active = _timed_redirect()
    if active:
        return active
    try:
        if all_due:
            collection.answer_card(card_id, rating, all_due=True)
        else:
            collection.answer_card(card_id, rating)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    return RedirectResponse("/review?all_due=1" if all_due else "/review", status_code=303)


@app.post("/review/undo")
def undo_review(request: Request, all_due: bool = Form(False), csrf: str = Form("")):
    _, err = _auth_or_login(request)
    if err:
        return err
    auth.verify_csrf(request, csrf)
    active = _timed_redirect()
    if active:
        return active
    if not collection.undo_review():
        raise HTTPException(409, "The last review is no longer available to undo")
    return RedirectResponse("/review?all_due=1" if all_due else "/review", status_code=303)


@app.get("/browse", response_class=HTMLResponse)
def browse(
    request: Request,
    deck: DeckFilter = None,
    q: str = Query("", max_length=150),
    page: int = Query(1, ge=1),
    flag: str = Query("", max_length=32),
):
    user, err = _auth_or_login(request)
    if err:
        return err
    query = q.strip()
    if flag not in ("", "flagged", *collection.FLAG_REASONS):
        raise HTTPException(400, "Invalid flag filter")
    result = collection.browse_cards(deck, query, page, flag)
    if result is None:
        raise HTTPException(404, "Deck not found")
    filters = {"q": query, "page": result["page"], "flag": flag}
    if deck is not None:
        filters["deck"] = deck
    return templates.TemplateResponse(
        request=request,
        name="browse.html",
        context={"user": user, "result": result, "deck": deck, "query": query, "filters": filters, "flag": flag},
    )


@app.get("/browse/{card_id}", response_class=HTMLResponse)
def browse_detail(
    request: Request,
    card_id: int,
    deck: DeckFilter = None,
    q: str = Query("", max_length=150),
    page: int = Query(1, ge=1),
    flag: str = Query("", max_length=32),
):
    user, err = _auth_or_login(request)
    if err:
        return err
    card = collection.browse_card(card_id) if 0 < card_id < 2**63 else None
    if card is None:
        raise HTTPException(404, "Card not found")
    filters = {"q": q, "page": page, "flag": flag}
    if deck is not None:
        filters["deck"] = deck
    return templates.TemplateResponse(
        request=request,
        name="browse_detail.html",
        context={"user": user, "card": card, "filters": filters, "csrf": request.cookies.get(auth.CSRF_COOKIE, "")},
    )


@app.post("/cards/{card_id}/flag")
def flag_card(
    request: Request,
    card_id: int,
    reason: str = Form(""),
    resolve: bool = Form(False),
    view: Literal["browse", "review", "answer"] = Form("browse"),
    all_due: bool = Form(False),
    csrf: str = Form(""),
):
    _, err = _auth_or_login(request)
    if err:
        return err
    auth.verify_csrf(request, csrf)
    try:
        if not 0 < card_id < 2**63 or not collection.set_card_flag(card_id, "" if resolve else reason):
            raise HTTPException(404, "Card not found")
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    target = {"review": "/review", "answer": "/review?show=1", "browse": f"/browse/{card_id}"}
    location = target[view]
    if all_due and view != "browse":
        location += "&all_due=1" if view == "answer" else "?all_due=1"
    return RedirectResponse(location, status_code=303)


@app.get("/stats", response_class=HTMLResponse)
def stats_page(request: Request, days: int = Query(7, ge=1, le=365)):
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
            "progress": collection.learning_progress(days),
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
