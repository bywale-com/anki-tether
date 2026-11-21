from __future__ import annotations

import hmac
import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from itsdangerous import BadSignature, URLSafeTimedSerializer

from app import config

SESSION_COOKIE = "anki_tether_session"
CSRF_COOKIE = "anki_tether_csrf"


def serializer() -> URLSafeTimedSerializer:
    secret = config.SESSION_SECRET
    if not secret:
        raise RuntimeError("SESSION_SECRET is required")
    return URLSafeTimedSerializer(secret, salt="anki-tether-session")


def create_session_token(username: str) -> str:
    return serializer().dumps({"u": username, "n": secrets.token_hex(8)})


def read_session_token(token: str) -> str | None:
    if not config.auth_configured():
        return None
    try:
        data = serializer().loads(token, max_age=60 * 60 * 24 * 14)
    except BadSignature:
        return None
    username = data.get("u")
    if username != config.STUDY_USERNAME:
        return None
    return username


def credentials_valid(username: str, password: str) -> bool:
    if not config.auth_configured():
        return False
    user_ok = hmac.compare_digest(username.encode(), config.STUDY_USERNAME.encode())
    pass_ok = hmac.compare_digest(password.encode(), config.STUDY_PASSWORD.encode())
    return user_ok and pass_ok


def current_user(request: Request) -> str | None:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return None
    return read_session_token(token)


def require_user(request: Request) -> str:
    if not config.auth_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="STUDY_USERNAME and STUDY_PASSWORD must be set before serving study data.",
        )
    user = current_user(request)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user


def require_user_page(request: Request) -> str:
    try:
        return require_user(request)
    except HTTPException as exc:
        if exc.status_code == 401:
            raise HTTPException(status_code=401, headers={"X-Redirect": "/login"}) from exc
        raise


UserDep = Annotated[str, Depends(require_user)]


def set_session(response, username: str) -> None:
    token = create_session_token(username)
    response.set_cookie(
        SESSION_COOKIE,
        token,
        httponly=True,
        samesite="lax",
        secure=config.SECURE_COOKIES,
        max_age=60 * 60 * 24 * 14,
        path="/",
    )
    response.set_cookie(
        CSRF_COOKIE,
        secrets.token_urlsafe(32),
        httponly=False,
        samesite="lax",
        secure=config.SECURE_COOKIES,
        max_age=60 * 60 * 24 * 14,
        path="/",
    )


def clear_session(response) -> None:
    response.delete_cookie(SESSION_COOKIE, path="/")
    response.delete_cookie(CSRF_COOKIE, path="/")


def verify_csrf(request: Request, token: str | None) -> None:
    cookie = request.cookies.get(CSRF_COOKIE, "")
    if not token or not cookie or not hmac.compare_digest(token.encode(), cookie.encode()):
        raise HTTPException(status_code=400, detail="Invalid CSRF token")


def login_redirect() -> RedirectResponse:
    return RedirectResponse("/login", status_code=303)
