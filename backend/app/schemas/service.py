"""
Pydantic схемы для Service
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.service import ServiceStatus


class ServiceBase(BaseModel):
    """Базовые данные услуги"""
    title: str = Field(..., min_length=10, max_length=255)
    description: str = Field(..., min_length=20)
    category: str = Field(..., min_length=3, max_length=100)
    tags: Optional[str] = None
    price: float = Field(..., gt=0)
    execution_days: int = Field(default=7, ge=1, le=365)
    revision_count: int = Field(default=2, ge=0, le=10)
    preview_url: Optional[str] = None


class ServiceCreate(ServiceBase):
    """Для создания услуги"""
    pass


class ServiceUpdate(BaseModel):
    """Для обновления услуги"""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    price: Optional[float] = None
    execution_days: Optional[int] = None
    revision_count: Optional[int] = None
    preview_url: Optional[str] = None
    status: Optional[ServiceStatus] = None


class ServiceResponse(ServiceBase):
    """Ответ API с данными услуги"""
    id: int
    seller_id: int
    status: ServiceStatus
    total_orders: int
    average_rating: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ServiceDetailResponse(ServiceResponse):
    """Подробная информация об услуге (с данными продавца)"""
    seller: Optional[dict] = None  # Будет заполнено вручную из User
