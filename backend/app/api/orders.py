"""
API маршруты для управления заказами
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Order, Service, User, OrderStatus, Transaction, TransactionType, TransactionStatus
from app.schemas import OrderCreate, OrderUpdate, OrderResponse, OrderDetailResponse
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, buyer_id: int, db: Session = Depends(get_db)):
    """
    Создать заказ (купить услугу)
    
    Требуется:
    - buyer_id: ID заказчика
    - service_id: ID услуги
    - buyer_comment: комментарий заказчика (опционально)
    """
    # Проверяем, существует ли услуга
    service = db.query(Service).filter(Service.id == order_data.service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Услуга не найдена"
        )
    
    # Проверяем, что услуга активна
    if service.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Услуга недоступна для заказа"
        )
    
    # Проверяем, что покупатель существует
    buyer = db.query(User).filter(User.id == buyer_id).first()
    if not buyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Покупатель не найден"
        )
    
    if buyer.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Заблокированный пользователь не может создавать заказы"
        )
    
    # Проверяем, что покупатель не заказывает у себя
    if service.seller_id == buyer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вы не можете заказать услугу у себя"
        )
    
    # Создаём заказ
    price = service.price
    platform_fee_percent = 10.0  # 10% комиссия платформы
    platform_fee = price * (platform_fee_percent / 100)
    seller_gets = price - platform_fee
    
    new_order = Order(
        buyer_id=buyer_id,
        seller_id=service.seller_id,
        service_id=order_data.service_id,
        price=price,
        platform_fee_percent=platform_fee_percent,
        seller_gets=seller_gets,
        status=OrderStatus.WAITING_PAYMENT,
        buyer_comment=order_data.buyer_comment,
        deadline=datetime.utcnow() + timedelta(days=service.execution_days),
        revisions_allowed=service.revision_count,
        created_at=datetime.utcnow(),
    )
    
    db.add(new_order)
    db.flush()  # Чтобы получить ID заказа
    
    # Создаём транзакцию эскроу
    escrow_transaction = Transaction(
        user_id=buyer_id,
        order_id=new_order.id,
        type=TransactionType.ORDER_ESCROW,
        amount=price,
        status=TransactionStatus.PENDING,
        description=f"Эскроу для заказа услуги: {service.title}",
        created_at=datetime.utcnow(),
    )
    
    db.add(escrow_transaction)
    db.commit()
    db.refresh(new_order)
    
    return new_order


@router.get("/{order_id}", response_model=OrderDetailResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """Получить информацию о заказе"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )
    
    # Подготавливаем полный ответ
    order_dict = {
        **{col.name: getattr(order, col.name) for col in order.__table__.columns},
        "buyer": {
            "id": order.buyer.id,
            "first_name": order.buyer.first_name,
            "avatar_url": order.buyer.avatar_url,
        },
        "seller": {
            "id": order.seller.id,
            "first_name": order.seller.first_name,
            "avatar_url": order.seller.avatar_url,
        },
        "service": {
            "id": order.service.id,
            "title": order.service.title,
            "category": order.service.category,
        },
        "messages_count": len(order.messages),
        "review": None,
    }
    
    if order.review:
        order_dict["review"] = {
            "id": order.review.id,
            "rating": order.review.rating,
            "text": order.review.text,
        }
    
    return order_dict


@router.get("/buyer/{buyer_id}/", response_model=list[OrderResponse])
async def get_buyer_orders(
    buyer_id: int,
    skip: int = 0,
    limit: int = 50,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить все заказы покупателя"""
    query = db.query(Order).filter(Order.buyer_id == buyer_id)
    
    if status_filter:
        query = query.filter(Order.status == status_filter)
    
    orders = query.offset(skip).limit(limit).all()
    return orders


@router.get("/seller/{seller_id}/", response_model=list[OrderResponse])
async def get_seller_orders(
    seller_id: int,
    skip: int = 0,
    limit: int = 50,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить все заказы продавца"""
    query = db.query(Order).filter(Order.seller_id == seller_id)
    
    if status_filter:
        query = query.filter(Order.status == status_filter)
    
    orders = query.offset(skip).limit(limit).all()
    return orders


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Обновить заказ (изменить статус, отправить результат)"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )
    
    # Проверяем, что это участник заказа
    if user_id not in [order.buyer_id, order.seller_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не участник этого заказа"
        )
    
    # Обновляем поля
    if order_data.status is not None:
        # Логика изменения статусов
        if order_data.status == OrderStatus.COMPLETED:
            # Когда заказ завершён, выплачиваем продавцу
            order.completed_at = datetime.utcnow()
            
            # Создаём транзакцию выплаты
            release_transaction = Transaction(
                user_id=order.seller_id,
                order_id=order.id,
                type=TransactionType.ORDER_RELEASE,
                amount=order.seller_gets,
                status=TransactionStatus.COMPLETED,
                description=f"Выплата за завершённый заказ",
                created_at=datetime.utcnow(),
                completed_at=datetime.utcnow(),
            )
            db.add(release_transaction)
            
            # Обновляем баланс продавца
            order.seller.balance += order.seller_gets
            order.seller.total_earned += order.seller_gets
            
            # Обновляем статистику
            order.seller.completed_orders += 1
            order.service.total_orders += 1
            
            order.is_paid = True
        
        order.status = order_data.status
    
    if order_data.seller_result is not None:
        order.seller_result = order_data.seller_result
    
    if order_data.buyer_comment is not None:
        order.buyer_comment = order_data.buyer_comment
    
    order.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(order)
    
    return order


@router.post("/{order_id}/pay", status_code=status.HTTP_200_OK)
async def pay_for_order(order_id: int, buyer_id: int, db: Session = Depends(get_db)):
    """Оплатить заказ"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )
    
    if order.buyer_id != buyer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только покупатель может оплатить заказ"
        )
    
    if order.is_paid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Заказ уже оплачен"
        )
    
    # Проверяем баланс покупателя
    buyer = db.query(User).filter(User.id == buyer_id).first()
    if buyer.balance < order.price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недостаточно средств на балансе"
        )
    
    # Списываем деньги со счёта покупателя
    buyer.balance -= order.price
    buyer.total_spent += order.price
    
    # Обновляем транзакцию эскроу
    escrow_tx = db.query(Transaction).filter(
        Transaction.order_id == order_id,
        Transaction.type == TransactionType.ORDER_ESCROW
    ).first()
    
    if escrow_tx:
        escrow_tx.status = TransactionStatus.COMPLETED
        escrow_tx.completed_at = datetime.utcnow()
    
    # Изменяем статус заказа
    order.is_paid = True
    order.payment_date = datetime.utcnow()
    order.status = OrderStatus.IN_PROGRESS
    order.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Заказ оплачен, работа начинается"}


@router.post("/{order_id}/cancel", status_code=status.HTTP_200_OK)
async def cancel_order(order_id: int, user_id: int, db: Session = Depends(get_db)):
    """Отменить заказ (только если не оплачен)"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )
    
    if user_id not in [order.buyer_id, order.seller_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не участник этого заказа"
        )
    
    if order.is_paid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Оплаченный заказ нельзя отменить"
        )
    
    order.status = OrderStatus.CANCELLED
    order.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Заказ отменён"}
