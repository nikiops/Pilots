@echo off
REM Запуск Telegram бота
REM Этот файл автоматически запустит бота и будет держать окно открытым

title Telegram Bot - Download Guide
color 0A

echo.
echo ========================================
echo    Telegram Bot запущен!
echo ========================================
echo.
echo Channel: @LAPSHENKINA
echo Скачивания логируются в файл downloads.txt
echo.
echo Нажмите Ctrl+C чтобы остановить бота
echo.

python bot.py

pause
