#!/bin/bash
# Скрипт для быстрого запуска всех компонентов

echo "🚀 TgWork MVP - Быстрый старт"
echo "=============================="
echo ""

# Backend
echo "1️⃣ Запуск Backend (FastAPI)..."
cd backend
python -m venv venv
source venv/bin/activate  # Для Windows используйте: venv\Scripts\activate
python -m pip install -q fastapi uvicorn[standard] sqlalchemy pydantic python-dotenv
echo "Backend зависимости установлены ✓"
echo ""

# Telegram Bot
echo "2️⃣ Запуск Telegram Bot..."
cd ../telegram-bot
python -m venv venv
source venv/bin/activate
python -m pip install -q aiogram python-dotenv aiohttp
echo "Bot зависимости установлены ✓"
echo ""

# Frontend
echo "3️⃣ Frontend готов к использованию"
echo "Откройте: file://$(pwd)/../frontend/index.html"
echo ""

echo "=============================="
echo "✅ Все компоненты готовы!"
echo ""
echo "Запуск:"
echo "  Backend:  cd backend && python run.py"
echo "  Bot:      cd telegram-bot && python main.py"
echo "  Frontend: Откройте frontend/index.html в браузере"
