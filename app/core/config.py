from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    JWT_SECRET: str = ''
    JWT_EXPIRE_MINUTES: int = 60
    JWT_ALGORITHM: str
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/users/auth/google/callback"
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        extra="ignore"
    
settings = Settings()