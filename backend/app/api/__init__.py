"""
API маршруты приложения
"""
from app.api.users import router as users_router
from app.api.services import router as services_router
from app.api.orders import router as orders_router
from app.api.messages import router as messages_router
from app.api.reviews import router as reviews_router

__all__ = [
    "users_router",
    "services_router",
    "orders_router",
    "messages_router",
    "reviews_router",
]
