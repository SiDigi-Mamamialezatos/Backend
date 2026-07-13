from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.badge import Badge
from app.repositories.badge_repo import BadgeRepository
from app.schemas.badge import BadgeCreate, BadgeUpdate


class BadgeService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BadgeRepository(db)

    def create(self, obj_in: BadgeCreate) -> Badge:
        return self.repo.create(obj_in)

    def get_or_404(self, badge_id: str) -> Badge:
        badge = self.repo.get(badge_id)
        if not badge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Badge not found"
            )
        return badge

    def list(self, skip: int = 0, limit: int = 100) -> List[Badge]:
        return self.repo.list(skip=skip, limit=limit)

    def update(self, badge_id: str, obj_in: BadgeUpdate) -> Badge:
        badge = self.get_or_404(badge_id)
        return self.repo.update(badge, obj_in)

    def delete(self, badge_id: str) -> None:
        badge = self.get_or_404(badge_id)
        self.repo.delete(badge)