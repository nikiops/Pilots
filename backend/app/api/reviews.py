"""
API маршруты для управления отзывами
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Review, Order, User, OrderStatus
from app.schemas import ReviewCreate, ReviewResponse, ReviewDetailResponse
from datetime import datetime

router = APIRouter(prefix="/api/v1/orders", tags=["Reviews"])


@router.post("/{order_id}/review/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    order_id: int,
    review_data: ReviewCreate,
    reviewer_id: int,
    db: Session = Depends(get_db)
):
    """
    Оставить отзыв на выполненный заказ
    
    Требуется:
    - order_id: ID заказа
    - reviewer_id: ID автора отзыва (покупатель)
    - rating: оценка от 1 до 5
    - text: текст отзыва (опционально)
    """
    # Проверяем заказ
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )
    
    # Проверяем, что заказ завершён
    if order.status != OrderStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Можно оставить отзыв только на завершённый заказ"
        )
    
    # Проверяем, что это покупатель
    if order.buyer_id != reviewer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только покупатель может оставить отзыв"
        )
    
    # Проверяем, нет ли уже отзыва на этот заказ
    existing_review = db.query(Review).filter(Review.order_id == order_id).first()
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="На этот заказ уже есть отзыв"
        )
    
    # Создаём отзыв
    new_review = Review(
        order_id=order_id,
        reviewer_id=reviewer_id,
        reviewed_user_id=order.seller_id,
        rating=review_data.rating,
        text=review_data.text,
        created_at=datetime.utcnow(),
    )
    
    db.add(new_review)
    db.flush()
    
    # Обновляем рейтинг продавца
    seller = order.seller
    
    # Получаем все отзывы продавца
    all_reviews = db.query(Review).filter(Review.reviewed_user_id == seller.id).all()
    
    # Считаем среднюю оценку
    if all_reviews:
        total_rating = sum(r.rating for r in all_reviews)
        avg_rating = total_rating / len(all_reviews)
        seller.rating = round(avg_rating, 2)
        seller.total_reviews = len(all_reviews)
    
    seller.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(new_review)
    
    return new_review


@router.get("/{order_id}/review/", response_model=ReviewDetailResponse)
async def get_review(order_id: int, db: Session = Depends(get_db)):
    """Получить отзыв на заказ"""
    review = db.query(Review).filter(Review.order_id == order_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отзыв не найден"
        )
    
    # Добавляем информацию об авторе и объекте отзыва
    review_dict = {
        "id": review.id,
        "order_id": review.order_id,
        "reviewer_id": review.reviewer_id,
        "reviewed_user_id": review.reviewed_user_id,
        "rating": review.rating,
        "text": review.text,
        "created_at": review.created_at,
        "reviewer": {
            "id": review.reviewer.id,
            "first_name": review.reviewer.first_name,
            "avatar_url": review.reviewer.avatar_url,
        },
        "reviewed_user": {
            "id": review.reviewed_user.id,
            "first_name": review.reviewed_user.first_name,
            "avatar_url": review.reviewed_user.avatar_url,
        }
    }
    
    return review_dict


@router.get("/user/{user_id}/reviews/", response_model=list[ReviewDetailResponse])
async def get_user_reviews(
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Получить все отзывы пользователя"""
    # Проверяем пользователя
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    limit = min(limit, 100)
    
    reviews = db.query(Review).filter(
        Review.reviewed_user_id == user_id
    ).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
    
    # Добавляем информацию об авторах
    result = []
    for review in reviews:
        review_dict = {
            "id": review.id,
            "order_id": review.order_id,
            "reviewer_id": review.reviewer_id,
            "reviewed_user_id": review.reviewed_user_id,
            "rating": review.rating,
            "text": review.text,
            "created_at": review.created_at,
            "reviewer": {
                "id": review.reviewer.id,
                "first_name": review.reviewer.first_name,
                "avatar_url": review.reviewer.avatar_url,
            },
            "reviewed_user": {
                "id": review.reviewed_user.id,
                "first_name": review.reviewed_user.first_name,
                "avatar_url": review.reviewed_user.avatar_url,
            }
        }
        result.append(review_dict)
    
    return result


@router.get("/top-rated/", response_model=list[dict])
async def get_top_rated_sellers(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Получить список топ-рейтинговых продавцов"""
    limit = min(limit, 50)
    
    sellers = db.query(User).filter(
        User.is_active == True,
        User.is_banned == False,
        User.completed_orders > 0
    ).order_by(User.rating.desc()).limit(limit).all()
    
    result = []
    for seller in sellers:
        result.append({
            "id": seller.id,
            "first_name": seller.first_name,
            "avatar_url": seller.avatar_url,
            "rating": seller.rating,
            "total_reviews": seller.total_reviews,
            "completed_orders": seller.completed_orders,
        })
    
    return result


@router.get("/by-rating/", response_model=list[dict])
async def get_reviews_by_rating(
    rating: int,
    db: Session = Depends(get_db)
):
    """Получить отзывы с определённой оценкой"""
    if rating < 1 or rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Оценка должна быть от 1 до 5"
        )
    
    reviews = db.query(Review).filter(
        Review.rating == rating
    ).order_by(Review.created_at.desc()).limit(50).all()
    
    result = []
    for review in reviews:
        result.append({
            "id": review.id,
            "order_id": review.order_id,
            "reviewer": {
                "first_name": review.reviewer.first_name,
                "avatar_url": review.reviewer.avatar_url,
            },
            "reviewed_user": {
                "id": review.reviewed_user.id,
                "first_name": review.reviewed_user.first_name,
            },
            "rating": review.rating,
            "text": review.text,
            "created_at": review.created_at,
        })
    
    return result
