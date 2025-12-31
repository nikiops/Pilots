@echo off
chcp 65001 > nul
color 0A

echo.
echo ============================================
echo   🚀 TgWork + NGROK - Полный запуск
echo ============================================
echo.

REM Проверка и установка зависимостей
echo 📦 Проверяю зависимости Backend...
cd /d d:\TgWork\TgWork\backend
pip install -q fastapi==0.115.0 uvicorn==0.30.0 sqlalchemy==2.0.23 sqlmodel==0.0.14 python-dotenv==1.0.1 pydantic==2.12.5 pydantic-settings==2.3.0 python-jose==3.3.0 passlib==1.7.4 python-multipart==0.0.6 requests==2.32.0 httpx==0.27.0 cryptography==42.0.0

echo 📦 Проверяю зависимости Telegram Bot...
cd /d d:\TgWork\TgWork\telegram-bot
pip install -q aiogram==3.23.0 python-dotenv==1.0.1 httpx==0.27.0

echo ✅ Зависимости готовы!
echo.
echo ============================================
echo   🌐 NGROK ТУННЕЛЬ
echo ============================================
echo.

REM NGROK только для WebApp
echo 🌍 Запуск NGROK для WebApp (порт 3000)...
start "NGROK WebApp" cmd /k "ngrok http 3000"
timeout /t 3 /nobreak

echo.
echo ============================================
echo   🚀 ЛОКАЛЬНЫЕ СЕРВИСЫ
echo ============================================
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
echo 🌐 ЛОКАЛЬНЫЕ АДРЕСА:
echo   📱 WebApp:        http://localhost:3000
echo   🔧 Backend API:   http://localhost:5000
echo   🤖 Telegram Bot:  работает
echo.
echo 🌍 NGROK ПУБЛИЧНЫЕ АДРЕСА:
echo   Скопируй URL из окна NGROK:
echo   📱 WebApp:  https://xxxx.ngrok.io (скопируй эту ссылку!)
echo   🔧 Backend: http://localhost:5000 (локально, не нужно)
echo.
echo 📝 ЧТО ДЕЛАТЬ ДАЛЬШЕ:
echo   1. В окне NGROK WebApp скопируй URL (https://...)
echo   2. Отправь мне эту ссылку в сообщение
echo   3. В окне NGROK Backend скопируй URL (https://...)
echo   4. Отправь мне и эту ссылку
echo   5. Я обновлю код и бот будет работать!
echo.
echo 💡 ВАЖНО:
echo   • Telegram приложение требует HTTPS (NGROK дает HTTPS)
echo   • Оставляй окна NGROK открытыми
echo   • Коды из NGROK меняются при перезапуске
echo.
echo 🛑 ДЛЯ ОСТАНОВКИ:
echo   Закрой все окна (включая NGROK)
echo.
pause
