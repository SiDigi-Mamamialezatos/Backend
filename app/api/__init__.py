from fastapi import APIRouter

from .user_router import router as user_router
from .module_router import router as module_router
from .material_router import router as material_router
from .attempt_router import router as attempt_router
from .badge_router import router as badge_router
from .user_badge_router import router as user_badge_router
from .chat_session_router import router as chat_session_router
from .chat_message_router import router as chat_message_router
from .chatbot_router import router as chatbot_router

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(module_router)
api_router.include_router(material_router)
api_router.include_router(attempt_router)
api_router.include_router(badge_router)
api_router.include_router(user_badge_router)
api_router.include_router(chat_session_router)
api_router.include_router(chat_message_router)
api_router.include_router(chatbot_router)

__all__ = ["api_router"]