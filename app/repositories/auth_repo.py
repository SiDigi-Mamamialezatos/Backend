# =============================================================
# app/repositories/auth_repo.py
# Handles refresh_token and user_oauth DB operations
# =============================================================

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.auth import RefreshToken, UserOAuth, OAuthProvider


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    # ── Refresh Token ─────────────────────────

    @staticmethod
    def _hash(raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode()).hexdigest()

    def create_refresh_token(self, user_id, device_info: str = None) -> str:
        raw = secrets.token_urlsafe(64)
        self.db.add(RefreshToken(
            user_id     = user_id,
            token_hash  = self._hash(raw),
            expires_at  = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            device_info = device_info,
        ))
        self.db.commit()
        return raw  # only time raw token is visible

    def get_valid_refresh_token(self, raw: str) -> RefreshToken | None:
        return self.db.query(RefreshToken).filter(
            RefreshToken.token_hash == self._hash(raw),
            RefreshToken.revoked    == False,
            RefreshToken.expires_at >  datetime.now(timezone.utc),
        ).first()

    def revoke_refresh_token(self, raw: str) -> None:
        token = self.db.query(RefreshToken).filter(
            RefreshToken.token_hash == self._hash(raw)
        ).first()
        if token:
            token.revoked    = True
            token.revoked_at = datetime.now(timezone.utc)
            self.db.commit()

    # ── OAuth ─────────────────────────────────

    def get_oauth_by_provider(self, provider: OAuthProvider, provider_id: str) -> UserOAuth | None:
        return self.db.query(UserOAuth).filter(
            UserOAuth.provider    == provider,
            UserOAuth.provider_id == provider_id,
        ).first()

    def create_oauth_link(self, user_id, provider: OAuthProvider, provider_id: str, provider_email: str) -> UserOAuth:
        row = UserOAuth(
            user_id        = user_id,
            provider       = provider,
            provider_id    = provider_id,
            provider_email = provider_email,
        )
        self.db.add(row)
        self.db.flush()
        return row