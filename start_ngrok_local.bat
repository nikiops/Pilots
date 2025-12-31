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
cd /d d:\TgWork\TgWork\telegram-bot
pip install -q aiogram==3.23.0 python-dotenv==1.0.1 httpx==0.27.0 > nul 2>&1

echo ✅ Зависимости готовы!
echo.

REM NGROK для WebApp (публичный доступ)
echo 🌍 Запуск NGROK туннеля для WebApp...
start "NGROK WebApp" cmd /k "ngrok http 3000"
timeout /t 3 /nobreak

REM Получаем текущий NGROK URL и сохраняем в .env
echo 📍 Определяю NGROK URL...
cd /d d:\TgWork\TgWork\telegram-bot
python ngrok_helper.py
timeout /t 1 /nobreak

REM WebApp сервер (локально)
echo 📱 Запуск WebApp на localhost:3000...
start "WebApp" cmd /k "cd /d d:\TgWork\TgWork\telegram-bot\webapp && python server.py"
timeout /t 1 /nobreak

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
echo   🤖 Telegram Bot:  запущен и слушает команды
echo.
echo 🌍 NGROK ПУБЛИЧНЫЙ ДОСТУП:
echo   📱 WebApp NGROK:  https://ff6c95186261.ngrok-free.app
echo.
echo 💡 КАК ТЕСТИРОВАТЬ:
echo   1. Откройся в Telegram боте (@твой_бот)
echo   2. Отправь команду: /profile
echo   3. Нажми кнопку "🚀 ВОЙТИ В ПРИЛОЖЕНИЕ"
echo   4. WebApp откроется через NGROK (регистрация локальная)
echo.
echo 📝 ВАЖНО:
echo   • WebApp работает через NGROK (https)
echo   • Данные сохраняются в localStorage браузера
echo   • Telegram Bot работает локально
echo   • Оставляй окно NGROK открытым!
echo.
echo 🛑 ДЛЯ ОСТАНОВКИ:
echo   Закрой все 4 окна
echo.
pause
