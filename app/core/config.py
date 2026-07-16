from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    JWT_SECRET: str = ''
    JWT_EXPIRE_MINUTES: int = 60
    JWT_ALGORITHM: str
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/users/auth/google/callback"
    FRONTEND_URL: str = "http://localhost:3000"

    # LLM (OpenAI-compatible API e.g. OpenAI, OpenCode, OpenRouter)
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.5
    LLM_MAX_TOKENS: int = 512
    LLM_HISTORY_LIMIT: int = 8

    class Config:
        env_file = ".env"
        extra="ignore"
    
settings = Settings()