from typing import List

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user_badge import UserBadge
from app.repositories.user_badge_repo import UserBadgeRepository
from app.repositories.badge_repo import BadgeRepository
from app.repositories.user_repo import UserRepository
from app.schemas.user_badge import UserBadgeCreate


class UserBadgeService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserBadgeRepository(db)
        self.badge_repo = BadgeRepository(db)
        self.user_repo = UserRepository(db)

    def award(self, obj_in: UserBadgeCreate) -> UserBadge:
        if not self.user_repo.get(obj_in.user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        if not self.badge_repo.get(obj_in.badge_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Badge not found"
            )
        try:
            return self.repo.create(obj_in)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has this badge",
            )

    def get_or_404(self, user_badge_id: str) -> UserBadge:
        user_badge = self.repo.get(user_badge_id)
        if not user_badge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User badge not found"
            )
        return user_badge

    def list_by_user(self, user_id: str) -> List[UserBadge]:
        return self.repo.list_by_user(user_id)

    def revoke(self, user_badge_id: str) -> None:
        user_badge = self.get_or_404(user_badge_id)
        self.repo.delete(user_badge)