from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .deps import get_db, get_current_user
from app.models.user import User
from app.schemas.chat_session import ChatSessionCreate, ChatSessionResponse
from app.services.chat_session_service import ChatSessionService

router = APIRouter(prefix="/chat-sessions", tags=["chat-sessions"])


@router.post("/", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
def create_chat_session(
    obj_in: ChatSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ChatSessionService(db).create(obj_in, current_user)


@router.get("/{session_id}", response_model=ChatSessionResponse)
def get_chat_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ChatSessionService(db).get_owned_or_404(session_id, current_user)


@router.get("/user/{user_id}", response_model=List[ChatSessionResponse])
def list_chat_sessions_by_user(
    user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return ChatSessionService(db).list_by_user(user_id, skip=skip, limit=limit)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ChatSessionService(db).delete(session_id, current_user)