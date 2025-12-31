"""
HTTP клиент для взаимодействия с backend API
"""
import httpx
import os
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

# URL backend сервера
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


class APIClient:
    """Асинхронный HTTP клиент для работы с API"""
    
    def __init__(self, base_url: str = BACKEND_URL, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
    
    @asynccontextmanager
    async def _request(self, method: str, endpoint: str, **kwargs):
        """Контекстный менеджер для HTTP запросов"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = f"{self.base_url}{endpoint}"
            response = await client.request(method, url, **kwargs)
            yield response
    
    # ============ ПОЛЬЗОВАТЕЛИ ============
    
    async def register_user(self, telegram_id: int, username: Optional[str] = None, 
                           first_name: Optional[str] = None) -> Dict[str, Any]:
        """Регистрация пользователя"""
        data = {
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name
        }
        async with self._request("POST", "/api/users/", json=data) as response:
            response.raise_for_status()
            return response.json()
    
    async def get_user(self, telegram_id: int) -> Dict[str, Any]:
        """Получить профиль пользователя по telegram_id"""
        async with self._request("GET", f"/api/users/telegram/{telegram_id}") as response:
            response.raise_for_status()
            return response.json()
    
    async def get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """Получить профиль пользователя по ID"""
        async with self._request("GET", f"/api/users/{user_id}") as response:
            response.raise_for_status()
            return response.json()
    
    async def search_users(self, username: str) -> list:
        """Поиск пользователей по имени"""
        params = {"username": username}
        async with self._request("GET", "/api/users/search/by-name", params=params) as response:
            response.raise_for_status()
            return response.json()
    
    # ============ УСЛУГИ ============
    
    async def get_service(self, service_id: int) -> Dict[str, Any]:
        """Получить информацию об услуге"""
        async with self._request("GET", f"/api/services/{service_id}") as response:
            response.raise_for_status()
            return response.json()
    
    async def list_services(self, category: Optional[str] = None, 
                           skip: int = 0, limit: int = 50) -> list:
        """Список всех услуг с фильтрацией"""
        params: dict = {"skip": skip, "limit": limit}
        if category:
            params["category"] = category
        async with self._request("GET", "/api/services/", params=params) as response:
            response.raise_for_status()
            return response.json()
    
    async def search_services(self, query: str, skip: int = 0, 
                             limit: int = 50) -> list:
        """Поиск услуг по названию"""
        params = {"query": query, "skip": skip, "limit": limit}
        async with self._request("GET", "/api/services/search/", params=params) as response:
            response.raise_for_status()
            return response.json()
    
    async def get_seller_services(self, seller_id: int) -> list:
        """Получить услуги продавца"""
        async with self._request("GET", f"/api/services/seller/{seller_id}/") as response:
            response.raise_for_status()
            return response.json()
    
    async def create_service(self, seller_id: int, title: str, description: str,
                            category: str, price: float, execution_days: int = 7,
                            revision_count: int = 2, tags: Optional[list] = None,
                            preview_url: Optional[str] = None) -> Dict[str, Any]:
        """Создать новую услугу"""
        data = {
            "seller_id": seller_id,
            "title": title,
            "description": description,
            "category": category,
            "price": price,
            "execution_days": execution_days,
            "revision_count": revision_count,
            "tags": tags or [],
            "preview_url": preview_url
        }
        async with self._request("POST", "/api/services/", json=data) as response:
            response.raise_for_status()
            return response.json()
    
    # ============ ЗАКАЗЫ ============
    
    async def create_order(self, buyer_id: int, service_id: int) -> Dict[str, Any]:
        """Создать новый заказ"""
        data = {
            "buyer_id": buyer_id,
            "service_id": service_id
        }
        async with self._request("POST", "/api/orders/", json=data) as response:
            response.raise_for_status()
            return response.json()
    
    async def get_order(self, order_id: int) -> Dict[str, Any]:
        """Получить информацию о заказе"""
        async with self._request("GET", f"/api/orders/{order_id}") as response:
            response.raise_for_status()
            return response.json()
    
    async def get_buyer_orders(self, buyer_id: int, status_filter: Optional[str] = None,
                              skip: int = 0, limit: int = 50) -> list:
        """Получить заказы покупателя"""
        params: dict = {"skip": skip, "limit": limit}
        if status_filter:
            params["status_filter"] = status_filter
        async with self._request("GET", f"/api/orders/buyer/{buyer_id}/", params=params) as response:
            response.raise_for_status()
            return response.json()
    
    async def get_seller_orders(self, seller_id: int, status_filter: Optional[str] = None,
                               skip: int = 0, limit: int = 50) -> list:
        """Получить заказы продавца"""
        params: dict = {"skip": skip, "limit": limit}
        if status_filter:
            params["status_filter"] = status_filter
        async with self._request("GET", f"/api/orders/seller/{seller_id}/", params=params) as response:
            response.raise_for_status()
            return response.json()
    
    async def pay_order(self, order_id: int) -> Dict[str, Any]:
        """Оплатить заказ (создать escrow)"""
        async with self._request("POST", f"/api/orders/{order_id}/pay") as response:
            response.raise_for_status()
            return response.json()
    
    async def cancel_order(self, order_id: int, reason: str) -> Dict[str, Any]:
        """Отменить заказ"""
        data = {"reason": reason}
        async with self._request("POST", f"/api/orders/{order_id}/cancel", json=data) as response:
            response.raise_for_status()
            return response.json()
    
    async def update_order(self, order_id: int, status: Optional[str] = None,
                          deadline: Optional[str] = None) -> Dict[str, Any]:
        """Обновить статус или дедлайн заказа"""
        data = {}
        if status:
            data["status"] = status
        if deadline:
            data["deadline"] = deadline
        async with self._request("PUT", f"/api/orders/{order_id}", json=data) as response:
            response.raise_for_status()
            return response.json()
    
    # ============ СООБЩЕНИЯ ============
    
    async def send_message(self, order_id: int, author_id: int, text: str,
                          attachments: Optional[list] = None) -> Dict[str, Any]:
        """Отправить сообщение в чат заказа"""
        data = {
            "author_id": author_id,
            "text": text,
            "attachments": attachments or []
        }
        async with self._request("POST", f"/api/orders/{order_id}/messages/", json=data) as response:
            response.raise_for_status()
            return response.json()
    
    async def get_messages(self, order_id: int, skip: int = 0, 
                          limit: int = 100) -> list:
        """Получить сообщения из чата заказа"""
        params = {"skip": skip, "limit": limit}
        async with self._request("GET", f"/api/orders/{order_id}/messages/", params=params) as response:
            response.raise_for_status()
            return response.json()
    
    # ============ ОТЗЫВЫ ============
    
    async def create_review(self, order_id: int, reviewer_id: int, 
                           reviewed_user_id: int, rating: int, 
                           text: Optional[str] = None) -> Dict[str, Any]:
        """Создать отзыв"""
        data = {
            "reviewer_id": reviewer_id,
            "reviewed_user_id": reviewed_user_id,
            "rating": rating,
            "text": text
        }
        async with self._request("POST", f"/api/orders/{order_id}/review/", json=data) as response:
            response.raise_for_status()
            return response.json()
    
    async def get_top_rated_sellers(self, limit: int = 10) -> list:
        """Получить топ продавцов по рейтингу"""
        params = {"limit": limit}
        async with self._request("GET", "/api/reviews/top-rated/", params=params) as response:
            response.raise_for_status()
            return response.json()
    
    async def get_user_reviews(self, user_id: int, skip: int = 0, 
                              limit: int = 50) -> list:
        """Получить отзывы о пользователе"""
        params = {"skip": skip, "limit": limit}
        async with self._request("GET", f"/api/reviews/user/{user_id}/reviews/", params=params) as response:
            response.raise_for_status()
            return response.json()


# Глобальный экземпляр клиента
api_client = APIClient()
