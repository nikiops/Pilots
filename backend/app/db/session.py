"""
Инициализация БД и сессии
"""
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import get_settings
from app.db.base import Base

settings = get_settings()

# Создание engine и SessionLocal
DATABASE_URL = settings.database_url
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Зависимость для получения сессии БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Создание всех таблиц в БД"""
    # Импортируем модели здесь чтобы они были зарегистрированы
    from app.models import (
        User,
        Service,
        Order,
        Message,
        Review,
        Transaction,
    )
    
    # Создаём таблицы
    Base.metadata.create_all(bind=engine)
