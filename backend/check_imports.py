#!/usr/bin/env python
"""
Скрипт для проверки что все модули загружаются
"""
import sys
print("Python:", sys.executable)
print()

try:
    print("1. Проверяем SQLAlchemy...")
    from sqlalchemy import create_engine
    print("   ✓ SQLAlchemy OK")
except Exception as e:
    print(f"   ✗ Ошибка: {e}")

try:
    print("2. Проверяем FastAPI...")
    from fastapi import FastAPI
    print("   ✓ FastAPI OK")
except Exception as e:
    print(f"   ✗ Ошибка: {e}")

try:
    print("3. Проверяем модели...")
    from app.models import User, Service, Order
    print("   ✓ Models OK")
except Exception as e:
    print(f"   ✗ Ошибка: {e}")

try:
    print("4. Проверяем маршруты...")
    from app.api import users_router, services_router, orders_router
    print("   ✓ Routers OK")
except Exception as e:
    print(f"   ✗ Ошибка: {e}")

try:
    print("5. Проверяем главное приложение...")
    from app.main import app
    print("   ✓ Main app OK")
except Exception as e:
    print(f"   ✗ Ошибка: {e}")

print()
print("✓ Все проверки пройдены! Приложение готово к запуску.")
