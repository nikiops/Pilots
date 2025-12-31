"""
Настройки приложения
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    # Для быстрого MVP используем SQLite
    database_url: str = "sqlite:///./tgwork.db"
    
    # Redis (опционально для MVP)
    redis_url: str = "redis://localhost:6379/0"
    
    # JWT
    secret_key: str = "your_secret_key_change_this_in_production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Telegram
    telegram_bot_token: str = ""
    telegram_webhook_url: str = ""
    
    # Server
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    return Settings()
