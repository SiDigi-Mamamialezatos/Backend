from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .deps import get_db, get_current_user
from app.models.user import User
from app.chatbot.chatbot_service import ChatbotService
from app.chatbot.schemas import ChatbotMessageResponse
from app.schemas.chat_message import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatMessageWithBotCreate,
)
from app.services.chat_message_service import ChatMessageService

router = APIRouter(prefix="/chat-messages", tags=["chat-messages"])


@router.post("/", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
def create_chat_message(
    obj_in: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ChatMessageService(db).create(obj_in, current_user)


@router.post(
    "/ask",
    response_model=ChatbotMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def ask_chatbot(
    obj_in: ChatMessageWithBotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Post a user message and let the topic-bound bot reply.

    The user message and the assistant reply are both persisted under the
    existing chat session so the conversation history stays intact.
    """
    return ChatbotService(db).send_message(
        chat_session_id=obj_in.chat_session_id,
        module_slug=obj_in.module_slug,
        content=obj_in.content,
        current_user=current_user,
    )


@router.get("/{message_id}", response_model=ChatMessageResponse)
def get_chat_message(message_id: str, db: Session = Depends(get_db)):
    return ChatMessageService(db).get_or_404(message_id)


@router.get("/session/{chat_session_id}", response_model=List[ChatMessageResponse])
def list_chat_messages_by_session(
    chat_session_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ChatMessageService(db).list_by_session(
        chat_session_id, current_user, skip=skip, limit=limit
    )


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat_message(message_id: str, db: Session = Depends(get_db)):
    ChatMessageService(db).delete(message_id)