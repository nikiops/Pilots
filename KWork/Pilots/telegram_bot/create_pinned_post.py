"""
Служебный скрипт для создания сообщения с кнопкой в закреплённый пост
Запустите этот скрипт один раз, и он пришлёт сообщение в канал с готовой кнопкой
"""

import asyncio
from config import BOT_TOKEN, CHANNEL_ID
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_pinned_post():
    """Создаёт сообщение для закреплённого поста"""
    bot = Bot(token=BOT_TOKEN)
    
    # Создаём кнопку
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="📥 СКАЧАТЬ ГАЙД",
            callback_data="download_file"
        )
    )
    
    # Отправляем сообщение в канал
    message = await bot.send_message(
        chat_id=CHANNEL_ID,
        text=(
            "📄 **ГАЙД ДЛЯ БОРТПРОВОДНИКОВ**\n\n"
            "Здесь вы найдёте полную информацию о том, как работать эффективно.\n\n"
            "❗ **Важно:** гайд доступен только для подписчиков канала.\n\n"
            "Нажмите кнопку ниже чтобы скачать!"
        ),
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )
    
    print(f"✅ Сообщение отправлено в канал!")
    print(f"📌 ID сообщения: {message.message_id}")
    print(f"Закрепите это сообщение (правый клик на сообщение → Закрепить)")
    
    await bot.session.close()


if __name__ == "__main__":
    print("🚀 Создаю сообщение для закреплённого поста...")
    asyncio.run(create_pinned_post())
