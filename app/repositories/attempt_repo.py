from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.attempt import Attempt
from app.schemas.attempt import AttemptCreate, AttemptUpdate


class AttemptRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj_in: AttemptCreate) -> Attempt:
        db_obj = Attempt(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get(self, attempt_id: str) -> Optional[Attempt]:
        return self.db.get(Attempt, attempt_id)

    def list_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Attempt]:
        return list(
            self.db.execute(
                select(Attempt)
                .where(Attempt.user_id == user_id)
                .offset(skip)
                .limit(limit)
            ).scalars()
        )

    def update(self, db_obj: Attempt, obj_in: AttemptUpdate) -> Attempt:
        data = obj_in.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def mark_completed(self, db_obj: Attempt) -> Attempt:
        db_obj.is_completed = True
        db_obj.completed_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: Attempt) -> None:
        self.db.delete(db_obj)
        self.db.commit()