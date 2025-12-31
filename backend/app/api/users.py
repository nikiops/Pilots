"""
API маршруты для управления пользователями
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserResponse, UserPublicResponse
from datetime import datetime

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя через Telegram
    
    Требуется:
    - telegram_id: уникальный ID из Telegram
    - first_name: имя пользователя
    - telegram_username: юзернейм (опционально)
    - avatar_url: URL аватара (опционально)
    """
    # Проверяем, не существует ли пользователь уже
    existing_user = db.query(User).filter(User.telegram_id == user_data.telegram_id).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким Telegram ID уже существует"
        )
    
    # Создаём нового пользователя
    new_user = User(
        telegram_id=user_data.telegram_id,
        telegram_username=user_data.telegram_username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        avatar_url=user_data.avatar_url,
        bio=user_data.bio,
        skills=user_data.skills,
        created_at=datetime.utcnow(),
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Получить полный профиль пользователя (только свой профиль)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    # Обновляем last_active
    user.last_active = datetime.utcnow()
    db.commit()
    
    return user


@router.get("/telegram/{telegram_id}", response_model=UserResponse)
async def get_user_by_telegram_id(telegram_id: int, db: Session = Depends(get_db)):
    """Получить профиль по Telegram ID"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    user.last_active = datetime.utcnow()
    db.commit()
    
    return user


@router.get("/public/{user_id}", response_model=UserPublicResponse)
async def get_user_public_profile(user_id: int, db: Session = Depends(get_db)):
    """Получить публичный профиль пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """Обновить свой профиль"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    # Обновляем поля (только если они переданы)
    if user_data.first_name is not None:
        user.first_name = user_data.first_name
    if user_data.last_name is not None:
        user.last_name = user_data.last_name
    if user_data.bio is not None:
        user.bio = user_data.bio
    if user_data.skills is not None:
        user.skills = user_data.skills
    if user_data.avatar_url is not None:
        user.avatar_url = user_data.avatar_url
    
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    return user


@router.get("/", response_model=list[UserPublicResponse])
async def list_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """Получить список активных пользователей"""
    users = db.query(User).filter(
        User.is_active == True,
        User.is_banned == False
    ).offset(skip).limit(limit).all()
    
    return users


@router.get("/search/by-name", response_model=list[UserPublicResponse])
async def search_users_by_name(q: str, db: Session = Depends(get_db)):
    """Поиск пользователей по имени"""
    if len(q) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поисковый запрос должен быть минимум 2 символа"
        )
    
    users = db.query(User).filter(
        User.is_active == True,
        User.is_banned == False,
        (User.first_name.ilike(f"%{q}%") | User.last_name.ilike(f"%{q}%"))
    ).limit(20).all()
    
    return users


@router.post("/{user_id}/ban", status_code=status.HTTP_200_OK)
async def ban_user(user_id: int, db: Session = Depends(get_db)):
    """Заблокировать пользователя (только админ)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    user.is_banned = True
    user.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Пользователь заблокирован"}


@router.post("/{user_id}/unban", status_code=status.HTTP_200_OK)
async def unban_user(user_id: int, db: Session = Depends(get_db)):
    """Разблокировать пользователя (только админ)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    user.is_banned = False
    user.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Пользователь разблокирован"}
