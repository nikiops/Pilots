import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from handlers import router as main_router

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(main_router)

async def on_startup():
    logger.info("Bot started")
    commands = [
        types.BotCommand(command="start", description="Start"),
        types.BotCommand(command="help", description="Help"),
        types.BotCommand(command="profile", description="Profile"),
    ]
    await bot.set_my_commands(commands)

async def on_shutdown():
    logger.info("Bot stopped")

async def main():
    await on_startup()
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await on_shutdown()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
