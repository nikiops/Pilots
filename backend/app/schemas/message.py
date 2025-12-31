"""
Pydantic схемы для Message
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class MessageCreate(BaseModel):
    """Для создания сообщения"""
    text: str
    attachments: Optional[str] = None  # JSON список URL'ов


class MessageResponse(BaseModel):
    """Ответ API с данными сообщения"""
    id: int
    order_id: int
    author_id: int
    text: str
    attachments: Optional[str]
    is_edited: bool
    is_deleted: bool
    created_at: datetime
    edited_at: Optional[datetime]

    class Config:
        from_attributes = True


class MessageDetailResponse(MessageResponse):
    """Сообщение с информацией об авторе"""
    author: Optional[dict] = None
