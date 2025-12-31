"""
Модель услуги (кворка)
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum


class ServiceStatus(str, enum.Enum):
    """Статусы услуги"""
    PENDING = "pending"  # На модерации
    ACTIVE = "active"  # Активна
    REJECTED = "rejected"  # Отклонена
    HIDDEN = "hidden"  # Скрыта владельцем


class Service(Base):
    """
    Модель услуги/кворка
    Фрилансер публикует готовое предложение с фиксированной ценой
    """
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    
    # Владелец (продавец)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    seller = relationship("User", back_populates="services")
    
    # Информация об услуге
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)  # Дизайн, Программирование, etc
    tags = Column(String(500), nullable=True)  # Теги, разделённые запятой
    
    # Параметры
    price = Column(Float, nullable=False)  # Фиксированная цена
    execution_days = Column(Integer, default=7)  # Срок выполнения в днях
    revision_count = Column(Integer, default=2)  # Количество правок
    
    # Превью
    preview_url = Column(String(500), nullable=True)  # Картинка услуги
    
    # Статус
    status = Column(SqlEnum(ServiceStatus), default=ServiceStatus.PENDING, index=True)
    
    # Статистика
    total_orders = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    
    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Отношения
    orders = relationship("Order", back_populates="service")

    def __repr__(self):
        return f"<Service {self.id}: {self.title}>"
