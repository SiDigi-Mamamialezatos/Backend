# =============================================================
# app/api/user_router.py — UPDATED
# Changes:
#   - login() passes device_info (user-agent)
#   - added POST /refresh
#   - added POST /logout
#   - added GET  /auth/google
#   - added GET  /auth/google/callback
# Everything else untouched
# =============================================================

from typing import List

import httpx
from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .deps import get_db, get_current_user
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


# ── New schemas (small, keep here for MVP) ────
class RefreshRequest(BaseModel):
    refresh_token: str

class LogoutRequest(BaseModel):
    refresh_token: str


# ── Unchanged ─────────────────────────────────

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(obj_in: UserCreate, db: Session = Depends(get_db)):
    return UserService(db).register(obj_in)


# ── UPDATED: passes device_info, returns refresh_token too ──
@router.post("/login")
def login(credentials: UserLogin, request: Request, db: Session = Depends(get_db)):
    return UserService(db).login(
        email       = credentials.email,
        password    = credentials.password,
        device_info = request.headers.get("user-agent"),
    )
    # now returns: { access_token, refresh_token, token_type }


# ── NEW: refresh ───────────────────────────────
@router.post("/refresh")
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    return UserService(db).refresh(payload.refresh_token)


# ── NEW: logout ────────────────────────────────
@router.post("/logout")
def logout(payload: LogoutRequest, db: Session = Depends(get_db)):
    UserService(db).logout(payload.refresh_token)
    return {"message": "Logged out successfully"}


# ── NEW: Google OAuth — step 1 redirect ────────
@router.get("/auth/google", include_in_schema=False)
def google_login():
    params = (
        f"client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
        f"&access_type=offline"
    )
    return RedirectResponse(f"https://accounts.google.com/o/oauth2/v2/auth?{params}")


# ── NEW: Google OAuth — step 2 callback ────────
@router.get("/auth/google/callback", include_in_schema=False)
async def google_callback(code: str, request: Request, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:

        # Exchange code → Google access token
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code":          code,
                "client_id":     settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri":  settings.GOOGLE_REDIRECT_URI,
                "grant_type":    "authorization_code",
            },
        )
        if token_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Google token exchange failed")

        # Get user info from Google
        user_resp = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {token_resp.json()['access_token']}"},
        )
        google_user = user_resp.json()  # { sub, email, name }

    tokens = UserService(db).google_login(
        google_user = google_user,
        device_info = request.headers.get("user-agent"),
    )

    # Redirect frontend with tokens in query params
    return RedirectResponse(
        f"{settings.FRONTEND_URL}/login"
        f"?access_token={tokens['access_token']}"
        f"&refresh_token={tokens['refresh_token']}"
    )


# ── Unchanged below ───────────────────────────

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    return UserService(db).get_or_404(user_id)


@router.get("/", response_model=List[UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return UserService(db).list(skip=skip, limit=limit)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    obj_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to update this user.")
    return UserService(db).update(user_id, obj_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to delete this user.")
    UserService(db).delete(user_id)