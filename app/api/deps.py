"""
Shared FastAPI dependencies.

ADJUST THESE TWO IMPORTS to match your actual project layout — they're
guesses based on the `from db.core.config import settings` pattern you
used earlier:

    from app.db.session import SessionLocal   # your session factory
    from app.core import security             # your existing security module

If you already have a `get_db` / `get_current_user` elsewhere (e.g. in
api/deps.py), just delete this file and point the routers at yours instead.
"""

from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.sessions import SessionLocal  # noqa: adjust to your session factory
from app.core import security  # noqa: adjust to your security module's location
from app.models.user import User
from app.repositories.user_repo import UserRepository

# Plain bearer-token scheme — no OAuth2 password flow. Swagger's
# "Authorize" button will just ask for a raw token to paste in.
# auto_error=False so a *missing* header also falls through to our own
# 401 below, instead of HTTPBearer's default 403.
bearer_scheme = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise credentials_exception

    token = credentials.credentials

    # ADJUST: assumes security.decode_access_token(token) -> dict | None
    # with a "sub" claim holding the user id.
    payload: Optional[dict] = security.decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = UserRepository(db).get(user_id)
    if user is None:
        raise credentials_exception

    return user