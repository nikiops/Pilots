"""
Главный файл Telegram бота для TgWork
"""
import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from handlers import router as main_router
from callbacks_v2 import router as callback_router

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в переменных окружения")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрируем обработчики
dp.include_router(main_router)
dp.include_router(callback_router)

async def on_startup():
    """Функция, вызываемая при запуске бота"""
    logger.info("✅ Бот запущен и готов к работе!")
    
    # Устанавливаем команды бота
    commands = [
        types.BotCommand(command="start", description="Начать работу"),
        types.BotCommand(command="help", description="Справка"),
        types.BotCommand(command="profile", description="Мой профиль"),
        types.BotCommand(command="search", description="Поиск услуг"),
        types.BotCommand(command="orders", description="Мои заказы"),
        types.BotCommand(command="services", description="Мои услуги"),
    ]
    await bot.set_my_commands(commands)

async def on_shutdown():
    """Функция, вызываемая при остановке бота"""
    logger.info("🛑 Бот остановлен")

async def main():
    """Главная функция"""
    logger.info("🚀 Запуск бота TgWork...")
    
    # Запускаем обработчик запуска
    await on_startup()
    
    try:
        # Запускаем polling
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
    finally:
        await on_shutdown()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
