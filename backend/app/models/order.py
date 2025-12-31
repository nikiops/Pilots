"""
Модель заказа
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum


class OrderStatus(str, enum.Enum):
    """Статусы заказа"""
    WAITING_PAYMENT = "waiting_payment"  # Ожидает оплаты
    IN_PROGRESS = "in_progress"  # В работе
    UNDER_REVIEW = "under_review"  # На проверке (ждёт ответа заказчика)
    COMPLETED = "completed"  # Завершён
    CANCELLED = "cancelled"  # Отменён
    DISPUTE = "dispute"  # Спор


class Order(Base):
    """
    Модель заказа
    Процесс: оплата -> работа -> проверка -> завершение
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    
    # Участники
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, index=True)
    
    buyer = relationship("User", foreign_keys=[buyer_id], back_populates="orders_as_buyer")
    seller = relationship("User", foreign_keys=[seller_id], back_populates="orders_as_seller")
    service = relationship("Service", back_populates="orders")
    
    # Финансы (эскроу)
    price = Column(Float, nullable=False)
    platform_fee_percent = Column(Float, default=10.0)  # Процент комиссии платформы
    seller_gets = Column(Float, nullable=False)  # Что получит продавец (после комиссии)
    
    # Деньги заморожены в эскроу до завершения заказа
    is_paid = Column(Boolean, default=False)
    payment_date = Column(DateTime, nullable=True)
    
    # Статус
    status = Column(SqlEnum(OrderStatus), default=OrderStatus.WAITING_PAYMENT, index=True)
    
    # Сроки
    deadline = Column(DateTime, nullable=True)  # Дедлайн (created_at + execution_days)
    
    # Данные заказа
    buyer_comment = Column(Text, nullable=True)  # Что хочет заказчик
    seller_result = Column(Text, nullable=True)  # Что сдал продавец
    
    # Правки
    revisions_used = Column(Integer, default=0)
    revisions_allowed = Column(Integer, default=2)
    
    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Отношения
    messages = relationship("Message", back_populates="order")
    review = relationship("Review", back_populates="order", uselist=False)
    transactions = relationship("Transaction", back_populates="order")

    def __repr__(self):
        return f"<Order {self.id}: {self.buyer_id} -> {self.seller_id}>"
