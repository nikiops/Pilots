"""
API маршруты для управления услугами
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Service, User, ServiceStatus
from app.schemas import ServiceCreate, ServiceUpdate, ServiceResponse, ServiceDetailResponse
from datetime import datetime

router = APIRouter(prefix="/api/v1/services", tags=["Services"])


@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(service_data: ServiceCreate, seller_id: int, db: Session = Depends(get_db)):
    """
    Создать новую услугу
    
    Требуется:
    - seller_id: ID продавца (фрилансера)
    - title: название услуги (мин 10 символов)
    - description: описание (мин 20 символов)
    - category: категория (Дизайн, Программирование и т.д.)
    - price: цена (больше 0)
    """
    # Проверяем, существует ли продавец
    seller = db.query(User).filter(User.id == seller_id).first()
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Продавец не найден"
        )
    
    if seller.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Заблокированный пользователь не может создавать услуги"
        )
    
    # Создаём услугу
    new_service = Service(
        seller_id=seller_id,
        title=service_data.title,
        description=service_data.description,
        category=service_data.category,
        tags=service_data.tags,
        price=service_data.price,
        execution_days=service_data.execution_days,
        revision_count=service_data.revision_count,
        preview_url=service_data.preview_url,
        status=ServiceStatus.PENDING,  # На модерации по умолчанию
        created_at=datetime.utcnow(),
    )
    
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    
    return new_service


@router.get("/{service_id}", response_model=ServiceDetailResponse)
async def get_service(service_id: int, db: Session = Depends(get_db)):
    """Получить полную информацию об услуге"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Услуга не найдена"
        )
    
    # Только активные услуги видны публично (или владелец может видеть свою)
    if service.status != ServiceStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Услуга недоступна"
        )
    
    # Добавляем информацию о продавце
    seller = service.seller
    service_dict = {
        **{col.name: getattr(service, col.name) for col in service.__table__.columns},
        "seller": {
            "id": seller.id,
            "first_name": seller.first_name,
            "avatar_url": seller.avatar_url,
            "rating": seller.rating,
            "completed_orders": seller.completed_orders,
        }
    }
    
    return service_dict


@router.get("/", response_model=list[ServiceResponse])
async def list_services(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Получить список услуг с фильтрацией
    
    Параметры:
    - category: фильтр по категории (опционально)
    - skip: пропустить записей
    - limit: максимум записей (макс 100)
    """
    limit = min(limit, 100)
    
    query = db.query(Service).filter(Service.status == ServiceStatus.ACTIVE)
    
    if category:
        query = query.filter(Service.category.ilike(f"%{category}%"))
    
    services = query.offset(skip).limit(limit).all()
    return services


@router.get("/search/", response_model=list[ServiceResponse])
async def search_services(
    q: str,
    db: Session = Depends(get_db)
):
    """
    Поиск услуг по названию, описанию и тегам
    
    Параметры:
    - q: поисковый запрос (минимум 2 символа)
    """
    if len(q) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поисковый запрос должен быть минимум 2 символа"
        )
    
    services = db.query(Service).filter(
        Service.status == ServiceStatus.ACTIVE,
        (Service.title.ilike(f"%{q}%") | 
         Service.description.ilike(f"%{q}%") |
         Service.tags.ilike(f"%{q}%"))
    ).limit(50).all()
    
    return services


@router.put("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: int,
    service_data: ServiceUpdate,
    seller_id: int,
    db: Session = Depends(get_db)
):
    """Обновить услугу (только владелец)"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Услуга не найдена"
        )
    
    # Проверяем, что это владелец
    if service.seller_id != seller_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете редактировать только свои услуги"
        )
    
    # Обновляем поля
    if service_data.title is not None:
        service.title = service_data.title
    if service_data.description is not None:
        service.description = service_data.description
    if service_data.category is not None:
        service.category = service_data.category
    if service_data.tags is not None:
        service.tags = service_data.tags
    if service_data.price is not None:
        service.price = service_data.price
    if service_data.execution_days is not None:
        service.execution_days = service_data.execution_days
    if service_data.revision_count is not None:
        service.revision_count = service_data.revision_count
    if service_data.preview_url is not None:
        service.preview_url = service_data.preview_url
    if service_data.status is not None:
        service.status = service_data.status
    
    service.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(service)
    
    return service


@router.delete("/{service_id}", status_code=status.HTTP_200_OK)
async def delete_service(
    service_id: int,
    seller_id: int,
    db: Session = Depends(get_db)
):
    """Удалить услугу (только владелец)"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Услуга не найдена"
        )
    
    if service.seller_id != seller_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы можете удалять только свои услуги"
        )
    
    db.delete(service)
    db.commit()
    
    return {"message": "Услуга удалена"}


@router.get("/seller/{seller_id}/", response_model=list[ServiceResponse])
async def get_seller_services(
    seller_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Получить все услуги продавца"""
    services = db.query(Service).filter(
        Service.seller_id == seller_id,
        Service.status == ServiceStatus.ACTIVE
    ).offset(skip).limit(limit).all()
    
    return services
