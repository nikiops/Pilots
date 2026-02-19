import asyncio
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, CHANNEL_ID


async def create_post() -> None:
    """Создает пост с кнопкой скачивания в канале.
    
    Кнопка проверяет подписку при нажатии:
    - Подписан → скачивает файл
    - Не подписан → просит подписаться
    """
    bot = Bot(token=BOT_TOKEN)
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📥 СКАЧАТЬ ГАЙД",
                    callback_data="channel_download"  # Callback для проверки подписки
                )
            ]
        ]
    )
    
    text = (
        "📥 <b>ГАЙД ДЛЯ БОРТПРОВОДНИКОВ</b>\n\n"
        "🎉 Полный справочник доступен!\n\n"
        "✅ <b>Подписчики канала</b> → Нажмите кнопку и скачайте\n"
        "❌ <b>Еще не подписали?</b> → Сначала подпишитесь, затем скачайте\n\n"
        "Нажмите кнопку ниже:"
    )
    
    try:
        message = await bot.send_message(
            CHANNEL_ID,
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        print(f"✅ Пост создан! ID сообщения: {message.message_id}")
        
        # Попытка закрепить пост
        try:
            await bot.pin_chat_message(CHANNEL_ID, message.message_id)
            print("✅ Пост закреплён в канале!")
        except Exception as pin_error:
            print(f"⚠️  Не удалось закрепить (нужны права админа)")
            print(f"   Закрепите сообщение вручную: правый клик → Закрепить")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(create_post())
