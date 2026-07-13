from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Pure data-access layer. No password hashing, no HTTP concerns —
    that belongs in services/user_service.py."""

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        name: str,
        email: str,
        hashed_password: str,
        age: Optional[int] = None,
    ) -> User:
        db_obj = User(
            name=name,
            email=email,
            hashed_password=hashed_password,
            age=age,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get(self, user_id: str) -> Optional[User]:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()

    def list(self, skip: int = 0, limit: int = 100) -> List[User]:
        return list(
            self.db.execute(select(User).offset(skip).limit(limit)).scalars()
        )

    def update(self, db_obj: User, **fields) -> User:
        """Caller is responsible for hashing any new password before
        passing it in (e.g. fields={"hashed_password": ...})."""
        for field, value in fields.items():
            if value is not None:
                setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: User) -> None:
        self.db.delete(db_obj)
        self.db.commit()