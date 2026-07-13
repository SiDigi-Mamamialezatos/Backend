from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from pwdlib import PasswordHash

from .config import settings

# Using Argon2id
password_context = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode = {
        "exp": expire,
        "sub": subject,
    }
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """Returns the decoded payload (with 'sub' = the subject passed into
    create_access_token) or None if the token is invalid/expired."""
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None