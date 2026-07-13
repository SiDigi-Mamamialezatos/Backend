from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User

def get_by_id(session: Session, user_id: str) -> User | None:
    return session.scalar(select(User).where(User.id == user_id))