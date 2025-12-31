"""
API маршруты для управления сообщениями в чате заказа
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Message, Order
from app.schemas import MessageCreate, MessageResponse, MessageDetailResponse
from datetime import datetime

router = APIRouter(prefix="/api/v1/orders", tags=["Messages"])


@router.post("/{order_id}/messages/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    order_id: int,
    message_data: MessageCreate,
    author_id: int,
    db: Session = Depends(get_db)
):
    """
    Отправить сообщение в чате заказа
    
    Требуется:
    - order_id: ID заказа
    - author_id: ID автора сообщения
    - text: текст сообщения
    - attachments: вложения (JSON, опционально)
    """
    # Проверяем заказ
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )
    
    # Проверяем, что автор - участник заказа
    if author_id not in [order.buyer_id, order.seller_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не участник этого заказа"
        )
    
    # Создаём сообщение
    new_message = Message(
        order_id=order_id,
        author_id=author_id,
        text=message_data.text,
        attachments=message_data.attachments,
        created_at=datetime.utcnow(),
    )
    
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    return new_message


@router.get("/{order_id}/messages/", response_model=list[MessageDetailResponse])
async def get_messages(
    order_id: int,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Получить историю сообщений заказа
    
    Параметры:
    - order_id: ID заказа
    - user_id: ID пользователя (для проверки доступа)
    - skip: пропустить сообщений
    - limit: максимум сообщений
    """
    # Проверяем заказ
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )
    
    # Проверяем доступ (если user_id передан)
    if user_id and user_id not in [order.buyer_id, order.seller_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете смотреть сообщения этого заказа"
        )
    
    limit = min(limit, 1000)
    
    messages = db.query(Message).filter(
        Message.order_id == order_id,
        Message.is_deleted == False
    ).order_by(Message.created_at.desc()).offset(skip).limit(limit).all()
    
    # Переворачиваем для корректного порядка (новые снизу)
    messages.reverse()
    
    # Добавляем информацию об авторе
    result = []
    for msg in messages:
        msg_dict = {
            "id": msg.id,
            "order_id": msg.order_id,
            "author_id": msg.author_id,
            "text": msg.text,
            "attachments": msg.attachments,
            "is_edited": msg.is_edited,
            "is_deleted": msg.is_deleted,
            "created_at": msg.created_at,
            "edited_at": msg.edited_at,
            "author": {
                "id": msg.author.id,
                "first_name": msg.author.first_name,
                "avatar_url": msg.author.avatar_url,
            }
        }
        result.append(msg_dict)
    
    return result


@router.put("/{order_id}/messages/{message_id}", response_model=MessageResponse)
async def edit_message(
    order_id: int,
    message_id: int,
    message_data: MessageCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Отредактировать сообщение (только автор, в течение 15 минут)"""
    # Проверяем заказ
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )
    
    # Проверяем сообщение
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.order_id == order_id
    ).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сообщение не найдено"
        )
    
    # Проверяем, что это автор сообщения
    if message.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете редактировать только свои сообщения"
        )
    
    # Проверяем, прошло ли больше 15 минут
    time_diff = datetime.utcnow() - message.created_at
    if time_diff.total_seconds() > 15 * 60:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Сообщение можно редактировать только 15 минут после отправки"
        )
    
    # Редактируем
    message.text = message_data.text
    message.is_edited = True
    message.edited_at = datetime.utcnow()
    
    db.commit()
    db.refresh(message)
    
    return message


@router.delete("/{order_id}/messages/{message_id}", status_code=status.HTTP_200_OK)
async def delete_message(
    order_id: int,
    message_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Удалить сообщение (только автор)"""
    # Проверяем заказ
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )
    
    # Проверяем сообщение
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.order_id == order_id
    ).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сообщение не найдено"
        )
    
    # Проверяем, что это автор сообщения
    if message.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете удалять только свои сообщения"
        )
    
    # Мягкое удаление (не удаляем физически, только помечаем как удалённое)
    message.is_deleted = True
    message.text = "[Сообщение удалено]"
    
    db.commit()
    
    return {"message": "Сообщение удалено"}
