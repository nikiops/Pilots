import asyncio
from pathlib import Path
from aiogram import Bot
from config import BOT_TOKEN, CHANNEL_ID, CHANNEL_USERNAME, PDF_PATH, LOG_FILE

bot: Bot | None = None
errors: list[str] = []
warnings: list[str] = []


async def test_config() -> None:
    """Проверяет конфигурацию бота."""
    global bot
    
    print("=" * 70)
    print("🔍 ПРОВЕРКА КОНФИГУРАЦИИ БОТА")
    print("=" * 70)
    print()
    
    try:
        # 1. Проверка токена
        print("1️⃣  Проверка токена...")
        bot = Bot(token=BOT_TOKEN)
        me = await bot.get_me()
        print(f"   ✅ Токен верный! Бот: @{me.username}")
        print()
        
        # 2. Проверка ID канала
        print("2️⃣  Проверка ID канала...")
        if isinstance(CHANNEL_ID, int) and CHANNEL_ID < 0:
            chat = await bot.get_chat(CHANNEL_ID)
            print(f"   ✅ ID канала правильно указан: {CHANNEL_ID}")
            print(f"   ✅ Канал найден: {chat.title}")
        else:
            errors.append("Ошибка: ID канала должно быть отрицательное целое число")
        print()
        
        # 3. Проверка имени канала
        print("3️⃣  Проверка имени канала...")
        if isinstance(CHANNEL_USERNAME, str) and CHANNEL_USERNAME:
            print(f"   ✅ Имя канала: @{CHANNEL_USERNAME}")
        else:
            errors.append("Ошибка: Имя канала не указано")
        print()
        
        # 4. Проверка PDF файла
        print("4️⃣  Проверка PDF файла...")
        if Path(PDF_PATH).exists():
            size = Path(PDF_PATH).stat().st_size / (1024 * 1024)
            print(f"   ✅ Файл найден: {PDF_PATH} ({size:.1f} MB)")
        else:
            errors.append(f"Файл {PDF_PATH} не найден в папке!")
        print()
        
        # 5. Проверка логов
        print("5️⃣  Проверка логов...")
        if Path(LOG_FILE).exists() or not Path(LOG_FILE).exists():
            print(f"   ℹ️  Логи будут созданы при первом скачивании")
        print()
        
    except Exception as e:
        errors.append(f"Ошибка: {str(e)}")
    finally:
        if bot is not None:
            await bot.session.close()
    
    # Вывод результатов
    print("=" * 70)
    print("📋 РЕЗУЛЬТАТЫ ПРОВЕРКИ")
    print("=" * 70)
    print()
    
    if errors:
        print("❌ ОШИБКИ (нужно исправить):")
        print()
        for error in errors:
            print(f"  ❌ {error}")
        print()
        print("❌ Исправьте ошибки выше перед запуском бота")
    else:
        print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
    
    print()
    print("=" * 70)
    print("📝 ТЕКУЩАЯ КОНФИГУРАЦИЯ")
    print("=" * 70)
    print(f"Токен: {BOT_TOKEN[:20]}***")
    print(f"ID канала: {CHANNEL_ID}")
    print(f"Имя канала: @{CHANNEL_USERNAME}")
    print(f"PDF файл: {PDF_PATH}")
    print(f"Логи: {LOG_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_config())
