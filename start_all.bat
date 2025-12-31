@echo off
chcp 65001 > nul
color 0A

echo.
echo ============================================
echo   🚀 TgWork - Полный запуск системы
echo ============================================
echo.

REM Установка зависимостей Backend
echo 📦 Устанавливаю зависимости Backend...
cd /d d:\TgWork\TgWork\backend
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Ошибка установки Backend зависимостей
    pause
    exit /b 1
)

REM Установка зависимостей Telegram Bot
echo 📦 Устанавливаю зависимости Telegram Bot...
cd /d d:\TgWork\TgWork\telegram-bot
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Ошибка установки Bot зависимостей
    pause
    exit /b 1
)

echo.
echo ✅ Все зависимости установлены!
echo.

REM Запуск WebApp сервера
echo 📱 Запуск WebApp сервера на localhost:8080...
start "WebApp Server" cmd /k "cd /d d:\TgWork\TgWork\telegram-bot\webapp && python server.py"

REM Небольшая пауза перед следующим сервером
timeout /t 2 /nobreak

REM Запуск Backend API
echo 🔧 Запуск Backend API на localhost:8000...
start "Backend API" cmd /k "cd /d d:\TgWork\TgWork\backend && python -m uvicorn app.main:app --reload --port 8000"

REM Небольшая пауза перед ботом
timeout /t 2 /nobreak

REM Запуск Telegram бота
echo 🤖 Запуск Telegram бота...
start "Telegram Bot" cmd /k "cd /d d:\TgWork\TgWork\telegram-bot && python main.py"

REM Небольшая пауза перед сообщением
timeout /t 2 /nobreak

echo.
echo ============================================
echo   ✅ Все сервисы запущены!
echo ============================================
echo.
echo 📝 Открыты 3 окна терминалов:
echo   1️⃣  WebApp Server - http://localhost:8080
echo   2️⃣  Backend API - http://localhost:8000
echo   3️⃣  Telegram Bot - @your_bot
echo.
echo 🧪 Для тестирования:
echo   • Напиши боту команду: /profile
echo   • Нажми на кнопку "Открыть профиль"
echo   • Должен открыться WebApp внутри Telegram
echo.
echo 🛑 Чтобы остановить всё:
echo   • Закрой все 3 окна терминалов
echo.
pause
