"""
Pydantic схемы для Order
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.order import OrderStatus


class OrderCreate(BaseModel):
    """Для создания заказа (покупка услуги)"""
    service_id: int
    buyer_comment: Optional[str] = None


class OrderUpdate(BaseModel):
    """Для обновления заказа"""
    status: Optional[OrderStatus] = None
    seller_result: Optional[str] = None
    buyer_comment: Optional[str] = None


class OrderResponse(BaseModel):
    """Ответ API с данными заказа"""
    id: int
    buyer_id: int
    seller_id: int
    service_id: int
    price: float
    platform_fee_percent: float
    seller_gets: float
    status: OrderStatus
    is_paid: bool
    payment_date: Optional[datetime]
    deadline: Optional[datetime]
    revisions_used: int
    revisions_allowed: int
    created_at: datetime
    completed_at: Optional[datetime]
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderDetailResponse(OrderResponse):
    """Подробная информация о заказе"""
    buyer: Optional[dict] = None
    seller: Optional[dict] = None
    service: Optional[dict] = None
    messages_count: int = 0
    review: Optional[dict] = None
