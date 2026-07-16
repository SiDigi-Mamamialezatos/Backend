from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.chat import ChatMessage
from app.models.user import User
from app.repositories.chat_message_repo import ChatMessageRepository
from app.schemas.chat_message import ChatMessageCreate
from app.schemas.chat_session import ChatSessionCreate
from app.services.chat_message_service import ChatMessageService
from app.services.chat_session_service import ChatSessionService
from app.chatbot.guardrail import guardrail_check
from app.chatbot.llm_client import LLMClient
from app.chatbot.modules import ChatbotModule, get_module
from app.core.config import settings


class ChatbotService:
    """Topic-bound FAQ chatbot.

    - Knowledge comes from static prompt + FAQ files (no DB/vector lookup).
    - Conversation history is read from the existing ChatMessage table.
    - Module is selected per request via `module_slug` (no schema change).
    """

    def __init__(self, db: Session):
        self.db = db
        self.session_service = ChatSessionService(db)
        self.message_service = ChatMessageService(db)
        self.message_repo = ChatMessageRepository(db)
        self.llm = LLMClient()

    def create_session(
        self, user_id: str, module_slug: str, current_user: User
    ) -> dict:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot create a chat session for another user",
            )

        module = get_module(module_slug)

        session = self.session_service.create(
            ChatSessionCreate(user_id=user_id), current_user
        )

        intro_create = ChatMessageCreate(
            chat_session_id=session.id,
            role="assistant",
            content=module.faq_intro,
        )
        intro = self.message_service.create(intro_create, current_user)

        return {
            "session_id": session.id,
            "module_slug": module.slug,
            "intro_message_id": intro.id,
            "intro_content": intro.content,
        }

    def send_message(
        self,
        chat_session_id: str,
        module_slug: str,
        content: str,
        current_user: User,
    ) -> ChatMessage:
        module = get_module(module_slug)

        # ownership check
        self.session_service.get_owned_or_404(chat_session_id, current_user)

        # lightweight guardrail: skip LLM for obvious off-topic/unsafe inputs
        blocked_reply = guardrail_check(content, module.name)
        if blocked_reply:
            reply = blocked_reply
        else:
            history = self._load_history(chat_session_id)
            messages = self._build_llm_messages(module, history, content)
            try:
                reply = self.llm.chat(messages)
            except Exception as exc:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"LLM error: {exc}",
                ) from exc

        # persist user message after LLM succeeds (no orphan user messages)
        user_create = ChatMessageCreate(
            chat_session_id=chat_session_id,
            role="user",
            content=content,
        )
        self.message_service.create(user_create, current_user)

        assistant_create = ChatMessageCreate(
            chat_session_id=chat_session_id,
            role="assistant",
            content=reply,
        )
        return self.message_service.create(assistant_create, current_user)

    def _load_history(self, chat_session_id: str) -> List[ChatMessage]:
        return self.message_repo.list_by_session(
            chat_session_id, limit=settings.LLM_HISTORY_LIMIT
        )

    def _build_llm_messages(
        self,
        module: ChatbotModule,
        history: List[ChatMessage],
        current_content: str,
    ) -> List[dict]:
        messages = [{"role": "system", "content": module.system_prompt}]
        for msg in history:
            if msg.role in ("user", "assistant"):
                messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": current_content})
        return messages
