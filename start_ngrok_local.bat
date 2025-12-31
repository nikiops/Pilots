@echo off
chcp 65001 > nul
color 0A

echo.
echo ============================================
echo   🚀 TgWork - Локальный запуск + NGROK
echo ============================================
echo.

REM Проверка зависимостей
echo 📦 Проверяю зависимости...
cd /d d:\TgWork\TgWork\backend
pip install -q fastapi==0.115.0 uvicorn==0.30.0 sqlalchemy==2.0.23 sqlmodel==0.0.14 python-dotenv==1.0.1 pydantic==2.12.5 pydantic-settings==2.3.0 python-jose==3.3.0 passlib==1.7.4 python-multipart==0.0.6 requests==2.32.0 httpx==0.27.0 cryptography==42.0.0 > nul 2>&1

cd /d d:\TgWork\TgWork\telegram-bot
pip install -q aiogram==3.23.0 python-dotenv==1.0.1 httpx==0.27.0 > nul 2>&1

echo ✅ Зависимости готовы!
echo.

REM NGROK для WebApp (публичный доступ)
echo 🌍 Запуск NGROK туннеля для WebApp...
start "NGROK WebApp" cmd /k "ngrok http 3000"
timeout /t 2 /nobreak

REM WebApp сервер (локально)
echo 📱 Запуск WebApp на localhost:3000...
start "WebApp" cmd /k "cd /d d:\TgWork\TgWork\telegram-bot\webapp && python server.py"
timeout /t 1 /nobreak

REM Backend API (локально)
echo 🔧 Запуск Backend API на localhost:5000...
start "Backend API" cmd /k "cd /d d:\TgWork\TgWork\backend && python -m uvicorn app.main:app --reload --port 5000"
timeout /t 2 /nobreak

REM Telegram Bot (локально)
echo 🤖 Запуск Telegram Bot...
start "Telegram Bot" cmd /k "cd /d d:\TgWork\TgWork\telegram-bot && python main.py"

timeout /t 2 /nobreak

echo.
echo ============================================
echo   ✅ ВСЕ СЕРВИСЫ ЗАПУЩЕНЫ!
echo ============================================
echo.
echo 🖥️  ЛОКАЛЬНЫЕ СЕРВИСЫ (на этом ПК):
echo   📱 WebApp:        http://localhost:3000
echo   🔧 Backend API:   http://localhost:5000
echo   🤖 Telegram Bot:  запущен и слушает команды
echo.
echo 🌍 NGROK ПУБЛИЧНЫЙ ДОСТУП:
echo   📱 WebApp NGROK:  https://ff6c95186261.ngrok-free.app
echo              ↑ (скопируй эту ссылку если нужна публичная)
echo.
echo 💡 КАК ТЕСТИРОВАТЬ:
echo   1. Откройся в Telegram боте (@твой_бот)
echo   2. Отправь команду: /profile
echo   3. Нажми кнопку "📱 Открыть профиль"
echo   4. WebApp откроется через NGROK (публичная ссылка)
echo.
echo 📝 ВАЖНО:
echo   • WebApp работает через NGROK (https)
echo   • Backend локально (http на 5000)
echo   • Telegram Bot работает локально
echo   • Оставляй окно NGROK открытым!
echo.
echo 🛑 ДЛЯ ОСТАНОВКИ:
echo   Закрой все 4 окна
echo.
pause
