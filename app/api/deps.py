"""
Shared FastAPI dependencies.

ADJUST THESE TWO IMPORTS to match your actual project layout — they're
guesses based on the `from db.core.config import settings` pattern you
used earlier:

    from db.session import SessionLocal   # your session factory
    from core import security             # your existing security module

If you already have a `get_db` / `get_current_user` elsewhere (e.g. in
api/deps.py), just delete this file and point the routers at yours instead.
"""

from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.sessions import SessionLocal  # noqa: adjust to your session factory
from app.core import security  # noqa: adjust to your security module's location
from app.models.user import User
from app.repositories.user_repo import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # ADJUST: assumes security.decode_access_token(token) -> dict | None
    # with a "sub" claim holding the user id. Swap for however your
    # security.create_access_token() encodes its payload.
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