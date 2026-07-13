from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core import security  # ADJUST import path if different
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

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

    def login(self, email: str, password: str) -> dict:
        user = self.authenticate(email, password)
        access_token = security.create_access_token(subject=user.id)
        return {"access_token": access_token, "token_type": "bearer"}

    def get_or_404(self, user_id: str) -> User:
        user = self.repo.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
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