"""
Pydantic схемы для Review
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ReviewCreate(BaseModel):
    """Для создания отзыва"""
    rating: int = Field(..., ge=1, le=5)
    text: Optional[str] = None


class ReviewResponse(BaseModel):
    """Ответ API с данными отзыва"""
    id: int
    order_id: int
    reviewer_id: int
    reviewed_user_id: int
    rating: int
    text: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewDetailResponse(ReviewResponse):
    """Отзыв с информацией об авторе"""
    reviewer: Optional[dict] = None
    reviewed_user: Optional[dict] = None
