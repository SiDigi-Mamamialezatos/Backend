from fastapi import HTTPException, status 
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.repositories import user_repository
from app.core import security

def register(session: Session, payload: RegisterRequest):
    existing_user = user_repository.get_by_email(session, payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered!"
        )

    hashed_password = security.hash_password(payload.password)

    user = user_repository.create(
        session,
        email=payload.email,
        password_hash=hashed_password,
        full_name=payload.full_name,
        phone_number=payload.phone_number
    )

    return {"message": "User registered successfully", "user_id": str(user.id)}