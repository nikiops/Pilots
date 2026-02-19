import asyncio
import logging
from datetime import datetime
from pathlib import Path

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

from config import BOT_TOKEN, CHANNEL_ID, CHANNEL_USERNAME, PDF_PATH, PDF_NAME, LOG_FILE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def log_download(user_id: int, username: str | None) -> None:
    """Логирует скачивание в файл."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | User ID: {user_id} | Username: @{username}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)


async def check_subscription(user_id: int) -> bool:
    """Проверяет подписан ли пользователь на канал."""
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"Ошибка проверки подписки: {e}")
        return False


def get_subscribe_keyboard() -> types.InlineKeyboardMarkup:
    """Создает клавиатуру с кнопкой подписки."""
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="📢 Подписаться на канал",
                    url=f"https://t.me/{CHANNEL_USERNAME}"
                )
            ]
        ]
    )
    return keyboard


def get_download_keyboard() -> types.InlineKeyboardMarkup:
    """Создает клавиатуру с кнопкой скачивания."""
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="📥 СКАЧАТЬ ГАЙД",
                    callback_data="download_file"
                )
            ]
        ]
    )
    return keyboard


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    """Обработчик команды /start."""
    reply_markup = get_download_keyboard()
    await message.answer(
        f"🎉 Привет, {message.from_user.first_name}!\n\n"
        "Нажмите кнопку ниже чтобы скачать гайд",
        reply_markup=reply_markup
    )


@dp.message(Command("debug"))
async def cmd_debug(message: types.Message) -> None:
    """Отладочная информация."""
    is_subscribed = await check_subscription(message.from_user.id)
    text = (
        f"👤 Your ID: {message.from_user.id}\n"
        f"📝 Username: @{message.from_user.username or 'none'}\n"
        f"📢 ID канала: {CHANNEL_ID}\n"
        f"✅ Подписаны: {'Да' if is_subscribed else 'Нет'}"
    )
    await message.answer(text)


@dp.message(Command("stats"))
async def cmd_stats(message: types.Message) -> None:
    """Показывает статистику скачиваний."""
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        unique_users: set[str] = set()
        for line in lines:
            if "User ID:" in line:
                unique_users.add(line.strip())
        
        text = f"📊 Всего скачиваний: {len(lines)}\n📍 Уникальных пользователей: {len(unique_users)}"
        await message.answer(text)
    except FileNotFoundError:
        await message.answer("📊 Пока нет скачиваний")


@dp.callback_query(F.data == "download_file")
async def handle_download(callback_query: types.CallbackQuery) -> None:
    """Обработчик кнопки скачивания."""
    user_id = callback_query.from_user.id
    is_subscribed = await check_subscription(user_id)
    
    if is_subscribed:
        try:
            pdf_file = FSInputFile(PDF_PATH, filename=PDF_NAME)
            if callback_query.message is not None:
                await callback_query.message.answer_document(pdf_file)
            log_download(user_id, callback_query.from_user.username)
            await callback_query.answer("✅ Файл отправлен!")
        except FileNotFoundError:
            await callback_query.answer("❌ Файл не найден!", show_alert=True)
    else:
        reply_markup = get_subscribe_keyboard()
        if callback_query.message is not None:
            await callback_query.message.answer(
                "❌ Подпишитесь на канал @LAPSHENKINA чтобы скачать файл",
                reply_markup=reply_markup
            )
        await callback_query.answer("Сначала подпишитесь на канал", show_alert=True)


async def main() -> None:
    """Запуск бота с polling."""
    logger.info("🤖 Бот запущен!")
    logger.info(f"📱 @{(await bot.get_me()).username}")
    logger.info(f"📢 ID канала: {CHANNEL_ID}")
    logger.info(f"📝 PDF файл: {PDF_PATH}")
    logger.info(f"📊 Логи скачиваний: {LOG_FILE}")
    
    Path(LOG_FILE).touch(exist_ok=True)
    
    try:
        await dp.start_polling(bot)  # type: ignore
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
