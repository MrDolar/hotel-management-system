from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    AI_API_KEY: str = ""
    AI_BASE_URL: str = "https://api.openai.com/v1"
    AI_MODEL: str = "gpt-3.5-turbo"
    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440
    DATABASE_URL: str = "sqlite:///./app.db"
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
