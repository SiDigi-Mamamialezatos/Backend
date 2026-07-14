# =============================================================
# app/services/user_service.py — UPDATED
# Changes:
#   - login() now returns refresh_token too
#   - added refresh() method
#   - added logout() method
#   - added google_login() method
# Everything else untouched
# =============================================================

from typing import List, Optional
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core import security
from app.models.user import User
from app.models.auth import OAuthProvider
from app.repositories.user_repo import UserRepository
from app.repositories.auth_repo import AuthRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)
        self.auth_repo = AuthRepository(db)  # ← new

    def register(self, obj_in: UserCreate) -> User:
        existing = self.repo.get_by_email(obj_in.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        hashed_password = security.hash_password(obj_in.password)
        return self.repo.create(
            name=obj_in.name,
            email=obj_in.email,
            hashed_password=hashed_password,
            age=obj_in.age,
        )

    def authenticate(self, email: str, password: str) -> User:
        user = self.repo.get_by_email(email)
        if not user or not security.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    # ── UPDATED: now returns refresh_token too ──
    def login(self, email: str, password: str, device_info: str = None) -> dict:
        user = self.authenticate(email, password)

        # update last_login
        user.last_login = datetime.now(timezone.utc)
        self.db.commit()

        access_token  = security.create_access_token(subject=user.id)
        refresh_token = self.auth_repo.create_refresh_token(user.id, device_info)

        return {
            "access_token":  access_token,
            "refresh_token": refresh_token,
            "token_type":    "bearer",
        }

    # ── NEW: rotate refresh token ───────────────
    def refresh(self, raw_refresh_token: str) -> dict:
        token_row = self.auth_repo.get_valid_refresh_token(raw_refresh_token)
        if not token_row:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        user = self.repo.get(token_row.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        # revoke old, issue new pair (rotation)
        self.auth_repo.revoke_refresh_token(raw_refresh_token)
        new_access  = security.create_access_token(subject=user.id)
        new_refresh = self.auth_repo.create_refresh_token(user.id, token_row.device_info)

        return {
            "access_token":  new_access,
            "refresh_token": new_refresh,
            "token_type":    "bearer",
        }

    # ── NEW: logout ─────────────────────────────
    def logout(self, raw_refresh_token: str) -> None:
        self.auth_repo.revoke_refresh_token(raw_refresh_token)

    # ── NEW: Google OAuth ───────────────────────
    def google_login(self, google_user: dict, device_info: str = None) -> dict:
        """
        google_user = { sub, email, name }
        from Google userinfo endpoint
        """
        
        provider_id = google_user.get("sub") or google_user.get("id")

        if not provider_id:
            raise HTTPException(
                status_code=400, 
                detail="Could not retrieve unique user identifier from Google response."
            )

        provider_email = google_user["email"]

        # Case 1: Google account already linked
        oauth_row = self.auth_repo.get_oauth_by_provider(OAuthProvider.google, provider_id)
        if oauth_row:
            user = self.repo.get(oauth_row.user_id)
            return self._issue_tokens(user, device_info)

        # Case 2: Email exists → link Google to existing account
        existing_user = self.repo.get_by_email(provider_email)
        if existing_user:
            self.auth_repo.create_oauth_link(
                user_id        = existing_user.id,
                provider       = OAuthProvider.google,
                provider_id    = provider_id,
                provider_email = provider_email,
            )
            self.db.commit()
            return self._issue_tokens(existing_user, device_info)

        # Case 3: Brand new user
        new_user = self.repo.create(
            name            = google_user.get("name", ""),
            email           = provider_email,
            hashed_password = "",           # no password for OAuth users
            age             = None,
        )
        new_user.email_verified = True
        self.auth_repo.create_oauth_link(
            user_id        = new_user.id,
            provider       = OAuthProvider.google,
            provider_id    = provider_id,
            provider_email = provider_email,
        )
        self.db.commit()
        return self._issue_tokens(new_user, device_info)

    def _issue_tokens(self, user: User, device_info: str = None) -> dict:
        user.last_login = datetime.now(timezone.utc)
        self.db.commit()
        return {
            "access_token":  security.create_access_token(subject=user.id),
            "refresh_token": self.auth_repo.create_refresh_token(user.id, device_info),
            "token_type":    "bearer",
        }

    # ── Unchanged below ─────────────────────────

    def get_or_404(self, user_id: str) -> User:
        user = self.repo.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def list(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.repo.list(skip=skip, limit=limit)

    def update(self, user_id: str, obj_in: UserUpdate) -> User:
        user = self.get_or_404(user_id)
        if obj_in.email and obj_in.email != user.email:
            existing = self.repo.get_by_email(obj_in.email)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )
        hashed_password: Optional[str] = None
        if obj_in.password:
            hashed_password = security.hash_password(obj_in.password)
        return self.repo.update(
            user,
            name=obj_in.name,
            email=obj_in.email,
            age=obj_in.age,
            hashed_password=hashed_password,
        )

    def delete(self, user_id: str) -> None:
        user = self.get_or_404(user_id)
        self.repo.delete(user)