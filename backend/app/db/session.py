"""
Инициализация БД и сессии
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import get_settings
from app.db.base import Base

settings = get_settings()


def get_db() -> Session:
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
