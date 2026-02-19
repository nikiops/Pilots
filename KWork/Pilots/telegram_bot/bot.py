"""
Telegram бот для проверки подписки и скачивания PDF с отслеживанием скачиваний
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from config import BOT_TOKEN, CHANNEL_ID, CHANNEL_USERNAME, PDF_PATH, PDF_NAME, LOG_FILE

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, FSInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Включаем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ============ СЛУЖЕБНЫЕ ФУНКЦИИ ============

def log_download(user_id: int, username: str | None) -> None:
    """Логирует скачивание файла"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | User ID: {user_id} | Username: @{username if username else 'anonymous'}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
    
    logger.info(f"✅ Скачивание логировано: {user_id} (@{username})")


async def check_subscription(user_id: int) -> bool:
    """
    Проверяет, подписан ли пользователь на канал
    """
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # Пользователь подписан, если он не в статусе "left" или "kicked"
        return member.status in ["member", "administrator", "creator", "restricted"]
    except Exception as e:
        logger.error(f"Ошибка при проверке подписки: {e}")
        return False


def get_subscribe_keyboard() -> types.InlineKeyboardMarkup:
    """Клавиатура для подписки"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="📢 Подписаться на канал",
            url=f"https://t.me/{CHANNEL_USERNAME}"
        )
    )
    return builder.as_markup()


def get_download_keyboard() -> types.InlineKeyboardMarkup:
    """Клавиатура для скачивания"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="📥 СКАЧАТЬ ГАЙД",
            callback_data="download_file"
        )
    )
    return builder.as_markup()


# ============ ОБРАБОТЧИКИ КОМАНД ============

@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    """Обработчик команды /start"""
    await message.answer(
        "👋 Привет! Я помогу тебе скачать гайд для бортпроводников.\n\n"
        "Нажми кнопку ниже:",
        reply_markup=get_download_keyboard()
    )


@dp.message(Command("debug"))
async def cmd_debug(message: types.Message) -> None:
    """Служебная команда для поиска ID канала"""
    if message.from_user is None:
        return
    await message.answer(
        f"🔧 DEBUG INFO:\n"
        f"Ваш ID: <code>{message.from_user.id}</code>\n"
        f"ID канала в config.py должен быть: <code>{CHANNEL_ID}</code>\n"
        f"Username канала: <code>@{CHANNEL_USERNAME}</code>",
        parse_mode="HTML"
    )


@dp.message(Command("stats"))
async def cmd_stats(message: types.Message) -> None:
    """Показывает статистику скачиваний"""
    try:
        if Path(LOG_FILE).exists():
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                downloads = f.readlines()
            count = len(downloads)
            await message.answer(
                f"📊 Статистика скачиваний:\n"
                f"Всего скачиваний: <b>{count}</b>",
                parse_mode="HTML"
            )
        else:
            await message.answer("Ещё никто не скачивал файл")
    except Exception as e:
        await message.answer(f"❌ Ошибка при чтении статистики: {e}")


# ============ ОБРАБОТЧИКИ КНОПОК ============

@dp.callback_query(F.data == "download_file")
async def handle_download(callback_query: types.CallbackQuery) -> None:
    """Обработчик нажатия кнопки скачивания"""
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    
    # Проверяем подписку
    is_subscribed = await check_subscription(user_id)
    
    if is_subscribed:
        # Пользователь подписан - отправляем файл
        try:
            if not Path(PDF_PATH).exists():
                await callback_query.answer(
                    "❌ Файл не найден! Проверьте путь в config.py",
                    show_alert=True
                )
                logger.error(f"Файл не найден: {PDF_PATH}")
                return
            
            # Отправляем файл
            pdf_file = FSInputFile(PDF_PATH, filename=PDF_NAME)
            if callback_query.message is not None:
                await callback_query.message.answer_document(
                    pdf_file,
                    caption="📄 Вот ваш гайд! Если возникнут вопросы, пишите в комментариях."
                )
            
            # Логируем скачивание
            log_download(user_id, username)
            
            await callback_query.answer("✅ Файл отправлен!", show_alert=False)
            
        except Exception as e:
            logger.error(f"Ошибка при отправке файла: {e}")
            await callback_query.answer(
                f"❌ Ошибка при отправке файла: {e}",
                show_alert=True
            )
    else:
        # Пользователь не подписан
        await callback_query.answer("❌ Вам нужно подписаться на канал!", show_alert=False)
        if callback_query.message is not None:
            await callback_query.message.answer(
                "❌ Чтобы скачать гайд, сначала подпишитесь на канал @LAPSHENKINA",
                reply_markup=get_subscribe_keyboard()
            )


# ============ ЗАПУСК БОТА ============

async def main() -> None:
    """Главная функция"""
    logger.info(f"🤖 Бот запущен!")
    logger.info(f"📢 ID канала: {CHANNEL_ID}")
    logger.info(f"📝 PDF файл: {PDF_PATH}")
    logger.info(f"📊 Логи скачиваний: {LOG_FILE}")
    
    # Создаём директорию для логов если её нет
    Path(LOG_FILE).touch(exist_ok=True)
    
    try:
        await dp.start_polling(bot)  # type: ignore
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
