"""
FastAPI приложение TgWork
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.db.base import Base
from app.db.session import engine
from app.api import users_router, services_router, orders_router, messages_router, reviews_router

app = FastAPI(
    title="TgWork API",
    description="Фриланс-биржа в Telegram",
    version="0.1.0"
)

# Инициализация БД при запуске
@app.on_event("startup")
async def startup():
    # Импортируем модели чтобы они зарегистрировались в Base
    from app.models import User, Service, Order, Message, Review, Transaction
    
    # Создаём таблицы
    Base.metadata.create_all(bind=engine)
    print("✓ База данных инициализирована")

# CORS middleware
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем все маршруты
app.include_router(users_router)
app.include_router(services_router)
app.include_router(orders_router)
app.include_router(messages_router)
app.include_router(reviews_router)


@app.get("/")
async def root():
    return {
        "message": "TgWork API v0.1.0",
        "status": "ready",
        "endpoints": {
            "users": "/api/v1/users",
            "services": "/api/v1/services",
            "orders": "/api/v1/orders",
            "documentation": "/docs",
            "openapi": "/openapi.json"
        }
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
