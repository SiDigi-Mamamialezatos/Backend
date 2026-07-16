from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FAQItem(BaseModel):
    q: str
    a: str


class FAQResponse(BaseModel):
    module_slug: str
    module_name: str
    faqs: list[FAQItem]


class ModuleInfo(BaseModel):
    slug: str
    name: str


class ModulesResponse(BaseModel):
    modules: list[ModuleInfo]


class ChatbotSessionCreate(BaseModel):
    user_id: str
    module_slug: str


class ChatbotSessionResponse(BaseModel):
    session_id: str
    module_slug: str
    intro_message_id: str
    intro_content: str


class ChatbotMessageRequest(BaseModel):
    chat_session_id: str
    module_slug: str
    content: str


class ChatbotMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    chat_session_id: str
    role: str
    content: str
    created_at: datetime
