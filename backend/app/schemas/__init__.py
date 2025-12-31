"""
Импорт всех schemas
"""
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserPublicResponse,
)
from app.schemas.service import (
    ServiceBase,
    ServiceCreate,
    ServiceUpdate,
    ServiceResponse,
    ServiceDetailResponse,
)
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderDetailResponse,
)
from app.schemas.message import (
    MessageCreate,
    MessageResponse,
    MessageDetailResponse,
)
from app.schemas.review import (
    ReviewCreate,
    ReviewResponse,
    ReviewDetailResponse,
)

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserPublicResponse",
    # Service
    "ServiceBase",
    "ServiceCreate",
    "ServiceUpdate",
    "ServiceResponse",
    "ServiceDetailResponse",
    # Order
    "OrderCreate",
    "OrderUpdate",
    "OrderResponse",
    "OrderDetailResponse",
    # Message
    "MessageCreate",
    "MessageResponse",
    "MessageDetailResponse",
    # Review
    "ReviewCreate",
    "ReviewResponse",
    "ReviewDetailResponse",
]
