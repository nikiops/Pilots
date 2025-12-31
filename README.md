# TgWork - Фриланс-биржа в Telegram

Telegram WebApp + бот, адаптированная фриланс-биржа по принципу Kwork.

## Структура проекта

- **backend/** - FastAPI сервер, БД (SQLite для MVP), API
- **frontend/** - HTML/JS WebApp для Telegram
- **telegram-bot/** - Telegram бот на Aiogram 3.x
- **docs/** - Документация

## Требования

- Python 3.11+
- Windows / macOS / Linux

## ⚡ Быстрый старт (MVP)

### 1️⃣ Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # или source venv/bin/activate на Linux/macOS
python -m pip install fastapi uvicorn[standard] sqlalchemy pydantic python-dotenv
python run.py
```

API будет доступен на **http://localhost:8000**

Документация API: **http://localhost:8000/docs**

### 2️⃣ Telegram Bot

```bash
cd telegram-bot
python -m venv venv
venv\Scripts\activate
python -m pip install aiogram python-dotenv aiohttp

# Скопировать .env.example в .env и добавить свой TELEGRAM_BOT_TOKEN
cp .env.example .env
# Отредактировать .env и добавить токен

python main.py
```

### 3️⃣ Frontend (WebApp)

Просто откройте [frontend/index.html](frontend/index.html) в браузере или разместите на веб-сервере.

Для локального тестирования:

```bash
# Если есть Python
cd frontend
python -m http.server 8080

# Или используйте любой другой простой HTTP сервер
```

Доступен на **http://localhost:8080**

---

## 📋 Этапы разработки

### ✅ Этап 1: Структура проекта (ГОТОВО)
- Созданы папки backend, frontend, telegram-bot
- Инициализированы конфигурации
- Подготовлены файлы зависимостей

### ✅ Этап 2: Локальный запуск (В ПРОЦЕССЕ)
- [x] Backend venv + зависимости
- [x] Telegram Bot venv + зависимости  
- [x] Frontend (простая HTML версия)
- [ ] Тестирование всех компонентов

### 🔜 Этап 3: Модели БД (User, Service, Order)

### 🔜 Этап 4: API эндпоинты

### 🔜 Этап 5: Интеграция Telegram

---

## 🎯 Tier-List приоритетов

- **S-Tier (MVP)**: Регистрация, Профили, Услуги, Заказы, Эскроу, Чат
- **A-Tier**: Репутация, Поиск, Категории, Комиссия
- **B-Tier**: Арбитраж, Выплаты, Админка
- **C-Tier**: Подписки, NFT, API для партнёров

---

## 🔐 Окружение

Скопируй `.env.example` в `.env` и отредактируй:

```env
# Backend
DATABASE_URL=sqlite:///./tgwork.db
SECRET_KEY=your_super_secret_key_change_this
DEBUG=True

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

---

## 📚 Далее

На Этапе 3 создадим модели БД и начнём разработку ядра приложения.
