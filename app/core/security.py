# =============================================================
# app/core/security.py — UPDATED
# Changes: added create_refresh_token logic reference
# Everything else untouched
# =============================================================

from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from pwdlib import PasswordHash

from .config import settings

password_context = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode = {
        "exp": expire,
        "sub": str(subject),        # ← ensure str, UUIDs need this
        "type": "access",           # ← add type so refresh tokens can't be used as access
    }
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != "access":     # ← reject refresh tokens used as access
            return None
        return payload
    except jwt.PyJWTError:
        return None