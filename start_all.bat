@echo off
chcp 65001 > nul
color 0A

echo.
echo ============================================
echo   🚀 TgWork - Полный запуск системы
echo ============================================
echo.

REM Проверка и установка зависимостей только если требуется
echo 📦 Проверяю зависимости Backend...
cd /d d:\TgWork\TgWork\backend
pip install -q fastapi==0.115.0 uvicorn==0.30.0 sqlalchemy==2.0.23 sqlmodel==0.0.14 python-dotenv==1.0.1 pydantic==2.12.5 pydantic-settings==2.3.0 python-jose==3.3.0 passlib==1.7.4 python-multipart==0.0.6 requests==2.32.0 httpx==0.27.0 cryptography==42.0.0
if %errorlevel% neq 0 (
    echo ❌ Ошибка Backend зависимостей
    pause
    exit /b 1
)

echo 📦 Проверяю зависимости Telegram Bot...
cd /d d:\TgWork\TgWork\telegram-bot
pip install -q aiogram==3.23.0 python-dotenv==1.0.1 httpx==0.27.0
if %errorlevel% neq 0 (
    echo ❌ Ошибка Bot зависимостей
    pause
    exit /b 1
)

echo ✅ Все зависимости готовы!
echo.

REM Запуск сервисов
echo 🚀 Запуск сервисов...
echo.

REM WebApp сервер
echo 📱 Запуск WebApp сервера на localhost:3000...
start "WebApp Server" cmd /k "cd /d d:\TgWork\TgWork\telegram-bot\webapp && python server.py"
timeout /t 1 /nobreak

REM Backend API
echo 🔧 Запуск Backend API на localhost:5000...
start "Backend API" cmd /k "cd /d d:\TgWork\TgWork\backend && python -m uvicorn app.main:app --reload --port 5000"
timeout /t 2 /nobreak

REM Telegram Bot
echo 🤖 Запуск Telegram бота...
start "Telegram Bot" cmd /k "cd /d d:\TgWork\TgWork\telegram-bot && python main.py"

timeout /t 2 /nobreak

echo.
echo ============================================
echo   ✅ ВСЕ СЕРВИСЫ ЗАПУЩЕНЫ!
echo ============================================
echo.
echo 🌐 АДРЕСА:
echo   📱 WebApp:        http://localhost:3000
echo   🔧 Backend API:   http://localhost:5000
echo   🤖 Telegram Bot:  @your_bot_name
echo.
echo 📝 ИНСТРУКЦИИ:
echo   1. Откройся в Telegram боте
echo   2. Отправь команду: /profile
echo   3. Нажми кнопку "Открыть профиль"
echo   4. Профиль откроется в WebApp!
echo.
echo 💡 ЕСЛИ ОШИБКИ:
echo   • Закрой все 3 окна
echo   • Проверь что .env файл содержит твой TELEGRAM_BOT_TOKEN
echo   • Запусти бат файл снова
echo.
echo 🛑 ДЛЯ ОСТАНОВКИ:
echo   • Закрой все 3 окна терминалов
echo.
pause
