from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat import ChatSession
from app.schemas.chat_session import ChatSessionCreate


class ChatSessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj_in: ChatSessionCreate) -> ChatSession:
        db_obj = ChatSession(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get(self, session_id: str) -> Optional[ChatSession]:
        return self.db.get(ChatSession, session_id)

    def list_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[ChatSession]:
        return list(
            self.db.execute(
                select(ChatSession)
                .where(ChatSession.user_id == user_id)
                .offset(skip)
                .limit(limit)
            ).scalars()
        )

    def delete(self, db_obj: ChatSession) -> None:
        self.db.delete(db_obj)
        self.db.commit()