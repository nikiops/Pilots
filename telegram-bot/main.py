"""
Главный файл Telegram бота
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
from dotenv import load_dotenv

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


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    user = message.from_user
    if user is None:
        await message.answer("Ошибка: не удалось получить информацию о пользователе")
        return
    
    first_name = user.first_name or "друг"
    await message.answer(
        f"Привет, {first_name}! 👋\n\n"
        f"Добро пожаловать на TgWork - фриланс-биржу в Telegram!\n\n"
        f"Твой Telegram ID: {user.id}"
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = """
    🔧 Доступные команды:
    
    /start - Начать работу
    /profile - Мой профиль
    /services - Мои услуги
    /help - Справка
    """
    await message.answer(help_text)


async def main():
    """Главная функция"""
    logger.info("Бот запущен")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
