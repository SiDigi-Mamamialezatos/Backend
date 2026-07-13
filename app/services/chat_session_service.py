from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.chat import ChatSession
from app.models.user import User
from app.repositories.chat_session_repo import ChatSessionRepository
from app.schemas.chat_session import ChatSessionCreate


class ChatSessionService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ChatSessionRepository(db)

    def create(self, obj_in: ChatSessionCreate, current_user: User) -> ChatSession:
        if obj_in.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create a chat session for another user",
            )
        return self.repo.create(obj_in)

    def get_owned_or_404(self, session_id: str, current_user: User) -> ChatSession:
        session = self.repo.get(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found"
            )
        if session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to access this chat session",
            )
        return session

    def list_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[ChatSession]:
        return self.repo.list_by_user(user_id, skip=skip, limit=limit)

    def delete(self, session_id: str, current_user: User) -> None:
        session = self.get_owned_or_404(session_id, current_user)
        self.repo.delete(session)