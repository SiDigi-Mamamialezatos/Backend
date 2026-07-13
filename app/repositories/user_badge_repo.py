from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user_badge import UserBadge
from app.schemas.user_badge import UserBadgeCreate


class UserBadgeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj_in: UserBadgeCreate) -> UserBadge:
        """Raises IntegrityError if (user_id, badge_id) already exists (unique constraint)."""
        db_obj = UserBadge(**obj_in.model_dump())
        self.db.add(db_obj)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise
        self.db.refresh(db_obj)
        return db_obj

    def get(self, user_badge_id: str) -> Optional[UserBadge]:
        return self.db.get(UserBadge, user_badge_id)

    def list_by_user(self, user_id: str) -> List[UserBadge]:
        return list(
            self.db.execute(
                select(UserBadge).where(UserBadge.user_id == user_id)
            ).scalars()
        )

    def delete(self, db_obj: UserBadge) -> None:
        self.db.delete(db_obj)
        self.db.commit()