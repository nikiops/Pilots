"""
Скрипт для проверки конфигурации перед запуском бота
Запустите: python test_config.py
"""

import asyncio
from pathlib import Path
from config import BOT_TOKEN, CHANNEL_ID, CHANNEL_USERNAME, PDF_PATH, LOG_FILE

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError


async def test_config() -> None:
    """Проверяет все параметры конфигурации"""
    
    print("\n" + "="*70)
    print("🔍 ПРОВЕРКА КОНФИГУРАЦИИ БОТА")
    print("="*70 + "\n")
    
    errors: list[str] = []
    warnings: list[str] = []
    
    # 1. Проверка токена
    print("1️⃣  Проверка токена...")
    bot: Bot | None = None
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":  # type: ignore
        errors.append("❌ BOT_TOKEN не заполнен в config.py!")
    elif ":" not in BOT_TOKEN:
        errors.append("❌ BOT_TOKEN имеет неправильный формат (должно быть число:строка)")
    else:
        try:
            bot = Bot(token=BOT_TOKEN)
            me = await bot.get_me()
            print(f"   ✅ Токен верный! Бот: @{me.username}")
        except TelegramAPIError as e:
            errors.append(f"❌ Ошибка в токене: {e}")
        finally:
            if bot:
                await bot.session.close()
    
    # 2. Проверка ID канала
    print("\n2️⃣  Проверка ID канала...")
    if isinstance(CHANNEL_ID, str):
        errors.append("❌ CHANNEL_ID должен быть числом, не строкой! Удалите кавычки в config.py")
    elif CHANNEL_ID > 0:
        errors.append("❌ CHANNEL_ID должен начинаться с -100 (это отрицательное число)")
    else:
        print(f"   ✅ ID канала правильно указан: {CHANNEL_ID}")
        
        # Пробуем подключиться к каналу
        if bot is not None:
            try:
                chat = await bot.get_chat(CHANNEL_ID)
                print(f"   ✅ Канал найден: {chat.title}")
            except TelegramAPIError as e:
                errors.append(f"❌ Не могу подключиться к каналу: {e}")
                errors.append("   💡 Убедитесь, что бот добавлен администратором в канал")
    
    # 3. Проверка имени канала
    print("\n3️⃣  Проверка имени канала...")
    if not CHANNEL_USERNAME or CHANNEL_USERNAME == "YOUR_CHANNEL_USERNAME":  # type: ignore
        warnings.append("⚠️  CHANNEL_USERNAME пустой (не критично, но рекомендуется заполнить)")
    else:
        print(f"   ✅ Имя канала: @{CHANNEL_USERNAME}")
    
    # 4. Проверка PDF файла
    print("\n4️⃣  Проверка PDF файла...")
    if not Path(PDF_PATH).exists():
        errors.append(f"❌ Файл {PDF_PATH} не найден в папке!")
        errors.append(f"   💡 Поместите ваш PDF в папку и переименуйте на '{PDF_PATH}'")
    else:
        file_size = Path(PDF_PATH).stat().st_size / (1024 * 1024)  # В МБ
        print(f"   ✅ PDF файл найден: {PDF_PATH}")
        print(f"     Размер: {file_size:.2f} МБ")
    
    # 5. Проверка лога файла
    print("\n5️⃣  Проверка логов...")
    log_path = Path(LOG_FILE)
    if log_path.exists():
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            log_lines = f.readlines()
        print(f"   ✅ Логи найдены: {len(log_lines)} скачиваний")
    else:
        print(f"   ℹ️  Логи будут созданы при первом скачивании")
    
    # Вывод результатов
    print("\n" + "="*70)
    print("📋 РЕЗУЛЬТАТЫ ПРОВЕРКИ")
    print("="*70 + "\n")
    
    if errors:
        print("❌ ОШИБКИ (нужно исправить):\n")
        for error in errors:
            print(f"  {error}")
        print()
    
    if warnings:
        print("⚠️  ПРЕДУПРЕЖДЕНИЯ (рекомендуется исправить):\n")
        for warning in warnings:
            print(f"  {warning}")
        print()
    
    if not errors:
        print("✅ ВСЁ ГОТОВО! Вы можете запустить бота:")
        print("   python bot.py")
        print()
    else:
        print("❌ Исправьте ошибки выше перед запуском бота")
        print()
    
    # Вывод текущей конфигурации
    print("="*70)
    print("📝 ТЕКУЩАЯ КОНФИГУРАЦИЯ")
    print("="*70)
    print(f"Токен: {'*' * len(BOT_TOKEN)}")
    print(f"ID канала: {CHANNEL_ID}")
    print(f"Имя канала: @{CHANNEL_USERNAME}")
    print(f"PDF файл: {PDF_PATH}")
    print(f"Логи: {LOG_FILE}")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(test_config())
