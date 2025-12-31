"""
Pydantic схемы для User (валидация и ответы API)
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Базовые данные пользователя"""
    first_name: str = Field(..., min_length=1, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = None
    skills: Optional[str] = None


class UserCreate(UserBase):
    """Для создания пользователя (регистрация)"""
    telegram_id: int
    telegram_username: Optional[str] = None
    avatar_url: Optional[str] = None


class UserUpdate(BaseModel):
    """Для обновления профиля"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    """Ответ API с данными пользователя"""
    id: int
    telegram_id: int
    telegram_username: Optional[str]
    avatar_url: Optional[str]
    is_active: bool
    is_banned: bool
    rating: float
    total_reviews: int
    balance: float
    total_earned: float
    total_spent: float
    completed_orders: int
    cancelled_orders: int
    created_at: datetime
    updated_at: datetime
    last_active: datetime

    class Config:
        from_attributes = True


class UserPublicResponse(BaseModel):
    """Публичный профиль пользователя (для других)"""
    id: int
    first_name: str
    last_name: Optional[str]
    telegram_username: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    skills: Optional[str]
    rating: float
    total_reviews: int
    completed_orders: int
    created_at: datetime

    class Config:
        from_attributes = True
