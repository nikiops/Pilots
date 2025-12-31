"""
Модель пользователя
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    """
    Модель пользователя платформы
    
    Может быть одновременно заказчиком и исполнителем
    """
    __tablename__ = "users"

    # Основные поля
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    telegram_username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Профиль
    bio = Column(Text, nullable=True)
    skills = Column(String(1000), nullable=True)  # Теги, разделённые запятой
    
    # Статус и рейтинг
    is_active = Column(Boolean, default=True, index=True)
    is_banned = Column(Boolean, default=False)
    
    # Рейтинг (0-5)
    rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    
    # Финансы
    balance = Column(Float, default=0.0)  # Внутренний баланс
    total_earned = Column(Float, default=0.0)  # Всего заработано
    total_spent = Column(Float, default=0.0)  # Всего потрачено
    
    # Статистика
    completed_orders = Column(Integer, default=0)
    cancelled_orders = Column(Integer, default=0)
    
    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    services = relationship("Service", back_populates="seller")
    orders_as_buyer = relationship("Order", foreign_keys="Order.buyer_id", back_populates="buyer")
    orders_as_seller = relationship("Order", foreign_keys="Order.seller_id", back_populates="seller")
    reviews_given = relationship("Review", foreign_keys="Review.reviewer_id", back_populates="reviewer")
    reviews_received = relationship("Review", foreign_keys="Review.reviewed_user_id", back_populates="reviewed_user")
    messages = relationship("Message", back_populates="author")
    transactions = relationship("Transaction", back_populates="user")

    def __repr__(self):
        return f"<User {self.telegram_id}: {self.first_name}>"
