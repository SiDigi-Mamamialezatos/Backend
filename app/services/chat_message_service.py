from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.chat import ChatMessage
from app.models.user import User
from app.repositories.chat_message_repo import ChatMessageRepository
from app.repositories.chat_session_repo import ChatSessionRepository
from app.schemas.chat_message import ChatMessageCreate


class ChatMessageService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ChatMessageRepository(db)
        self.session_repo = ChatSessionRepository(db)

    def create(self, obj_in: ChatMessageCreate, current_user: User) -> ChatMessage:
        session = self.session_repo.get(obj_in.chat_session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found"
            )
        if session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to post to this chat session",
            )
        return self.repo.create(obj_in)

    def get_or_404(self, message_id: str) -> ChatMessage:
        message = self.repo.get(message_id)
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat message not found"
            )
        return message

    def list_by_session(
        self, chat_session_id: str, current_user: User, skip: int = 0, limit: int = 100
    ) -> List[ChatMessage]:
        session = self.session_repo.get(chat_session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found"
            )
        if session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to view this chat session",
            )
        return self.repo.list_by_session(chat_session_id, skip=skip, limit=limit)

    def delete(self, message_id: str) -> None:
        message = self.get_or_404(message_id)
        self.repo.delete(message)