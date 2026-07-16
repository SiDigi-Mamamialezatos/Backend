from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .deps import get_current_user, get_db
from app.chatbot.chatbot_service import ChatbotService
from app.chatbot.modules import MODULES, get_module
from app.chatbot.schemas import (
    ChatbotMessageRequest,
    ChatbotMessageResponse,
    ChatbotSessionCreate,
    ChatbotSessionResponse,
    FAQResponse,
    ModuleInfo,
    ModulesResponse,
)
from app.models.user import User

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@router.get("/modules", response_model=ModulesResponse)
def list_modules():
    return ModulesResponse(
        modules=[ModuleInfo(slug=m.slug, name=m.name) for m in MODULES.values()]
    )


@router.get("/modules/{module_slug}/faq", response_model=FAQResponse)
def get_module_faq(module_slug: str):
    module = get_module(module_slug)
    return FAQResponse(
        module_slug=module.slug,
        module_name=module.name,
        faqs=module.faqs,
    )


@router.post(
    "/sessions",
    response_model=ChatbotSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_chatbot_session(
    obj_in: ChatbotSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ChatbotService(db).create_session(
        obj_in.user_id, obj_in.module_slug, current_user
    )


@router.post(
    "/sessions/{chat_session_id}/messages",
    response_model=ChatbotMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def send_chatbot_message(
    chat_session_id: str,
    obj_in: ChatbotMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ChatbotService(db).send_message(
        chat_session_id=chat_session_id,
        module_slug=obj_in.module_slug,
        content=obj_in.content,
        current_user=current_user,
    )
