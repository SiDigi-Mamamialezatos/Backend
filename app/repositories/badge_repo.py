from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.badge import Badge
from app.schemas.badge import BadgeCreate, BadgeUpdate


class BadgeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj_in: BadgeCreate) -> Badge:
        db_obj = Badge(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get(self, badge_id: str) -> Optional[Badge]:
        return self.db.get(Badge, badge_id)

    def list(self, skip: int = 0, limit: int = 100) -> List[Badge]:
        return list(
            self.db.execute(select(Badge).offset(skip).limit(limit)).scalars()
        )

    def update(self, db_obj: Badge, obj_in: BadgeUpdate) -> Badge:
        for field, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: Badge) -> None:
        self.db.delete(db_obj)
        self.db.commit()