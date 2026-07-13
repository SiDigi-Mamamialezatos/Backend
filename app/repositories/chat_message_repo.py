from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat import ChatMessage
from app.schemas.chat_message import ChatMessageCreate


class ChatMessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj_in: ChatMessageCreate) -> ChatMessage:
        db_obj = ChatMessage(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get(self, message_id: str) -> Optional[ChatMessage]:
        return self.db.get(ChatMessage, message_id)

    def list_by_session(
        self, chat_session_id: str, skip: int = 0, limit: int = 100
    ) -> List[ChatMessage]:
        return list(
            self.db.execute(
                select(ChatMessage)
                .where(ChatMessage.chat_session_id == chat_session_id)
                .order_by(ChatMessage.created_at)
                .offset(skip)
                .limit(limit)
            ).scalars()
        )

    def delete(self, db_obj: ChatMessage) -> None:
        self.db.delete(db_obj)
        self.db.commit()