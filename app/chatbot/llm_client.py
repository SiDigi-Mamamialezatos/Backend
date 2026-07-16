from typing import List

from openai import OpenAI

from app.core.config import settings


class LLMClient:
    """OpenAI-compatible chat client.

    Works with OpenAI, OpenCode, OpenRouter, or any provider that exposes
    the `/chat/completions` endpoint.
    """

    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
        )

    def chat(
        self,
        messages: List[dict],
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Send messages and return the assistant's text reply."""
        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=messages,
            temperature=temperature or settings.LLM_TEMPERATURE,
            max_tokens=max_tokens or settings.LLM_MAX_TOKENS,
        )
        content = response.choices[0].message.content
        return content or "Maaf, aku belum bisa menjawab. Coba tanya lagi ya."
