"""
Модель сообщения в чате заказа
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class Message(Base):
    """
    Модель сообщения в чате заказа
    Используется для общения между заказчиком и исполнителем
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    
    # Заказ и автор
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    order = relationship("Order", back_populates="messages")
    author = relationship("User", back_populates="messages")
    
    # Содержание
    text = Column(Text, nullable=False)
    
    # Файлы/вложения
    attachments = Column(String(2000), nullable=True)  # JSON массив URL'ов файлов
    
    # Статус
    is_edited = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    
    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    edited_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Message {self.id}: order={self.order_id}>"
