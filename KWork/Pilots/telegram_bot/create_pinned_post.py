import asyncio
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, CHANNEL_ID, CHANNEL_USERNAME


async def create_post() -> None:
    """Создает пост с кнопкой в канале."""
    bot = Bot(token=BOT_TOKEN)
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📥 СКАЧАТЬ ГАЙД",
                    url=f"https://t.me/@LAPSHENKINA_guide_bot?start=download"
                )
            ]
        ]
    )
    
    text = (
        "🎉 Гайд для бортпроводников доступен!\n\n"
        "Нажмите кнопку ниже чтобы скачать полный гайд"
    )
    
    try:
        message = await bot.send_message(
            CHANNEL_ID,
            text,
            reply_markup=keyboard
        )
        print(f"✅ Пост создан! ID сообщения: {message.message_id}")
        print("Закрепите сообщение в канале вручную (правый клик → Закрепить)")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(create_post())
