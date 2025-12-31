"""
Модель отзыва и рейтинга
"""
from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


class Review(Base):
    """
    Модель отзыва/рейтинга
    Заказчик оставляет отзыв после завершения заказа
    """
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    
    # Заказ
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True, index=True)
    order = relationship("Order", back_populates="review")
    
    # Автор и объект отзыва
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # Кто оставил
    reviewed_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # Кого оценили
    
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="reviews_given")
    reviewed_user = relationship("User", foreign_keys=[reviewed_user_id], back_populates="reviews_received")
    
    # Рейтинг (1-5 звёзд)
    rating = Column(Integer, nullable=False)
    
    # Текст отзыва
    text = Column(Text, nullable=True)
    
    # Даты
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        CheckConstraint('rating >= 1 and rating <= 5', name='check_rating_range'),
    )

    def __repr__(self):
        return f"<Review {self.id}: {self.rating} stars>"
