from aiogram import Router, F, types
from aiogram.filters import Command
from keyboards import get_main_menu, get_profile_menu
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user = message.from_user
    if not user:
        await message.answer("Error: user info not found")
        return
    
    await message.answer(
        f"Hello, {user.first_name}!\n\n"
        f"Welcome to TgWork",
        reply_markup=get_profile_menu()
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = "TgWork Help\n\nCommands:\n/start - Start\n/help - Help\n/profile - Profile"
    await message.answer(help_text)

@router.message(Command("profile"))
async def cmd_profile(message: types.Message):
    await message.answer(
        "Open app to manage profile",
        reply_markup=get_profile_menu()
    )

@router.message(Command("clearcache"))
async def cmd_clearcache(message: types.Message):
    """Полная очистка кеша WebApp"""
    await message.answer(
        "🧹 **ПОЛНАЯ ОЧИСТКА КЕША**\n\n"
        "✅ **Метод 1 (Быстрый - в приложении):**\n"
        "1. Откройте WebApp\n"
        "2. Нажмите меню → 👤 Профиль\n"
        "3. Нажмите кнопку 🧹 Очистить кеш\n"
        "4. Подтвердите удаление\n\n"
        
        "✅ **Метод 2 (Если 1-й не помог):**\n"
        "1. Закройте WebApp (свайп вниз)\n"
        "2. Закройте этот чат\n"
        "3. Выйдите из Telegram ПОЛНОСТЬЮ\n"
        "4. Откройте Telegram\n"
        "5. Откройте чат с ботом\n"
        "6. Нажмите кнопку WebApp заново\n\n"
        
        "✅ **Метод 3 (Если ничего не помогло):**\n"
        "⚙️ Telegram → Настройки → Хранилище и кеш → Очистить кеш\n"
        "Потом повторите метод 2\n\n"
        
        "⏳ Подождите 10-15 секунд при загрузке!",
        parse_mode="Markdown"
    )

@router.message(Command("forceupdate"))
async def cmd_forceupdate(message: types.Message):
    """Команда для администратора - заставляет браузер загрузить новую версию"""
    # Проверяем что это администратор (user_id)
    admin_ids = [427049256]  # Добавите свой ID
    
    if message.from_user.id not in admin_ids:
        await message.answer("❌ Доступ запрещен")
        return
    
    # Увеличиваем версию
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    current_version = os.getenv('WEBAPP_VERSION', '1')
    try:
        new_version = str(int(current_version) + 1)
    except:
        new_version = '2'
    
    # Обновляем в памяти
    from keyboards import WEBAPP_VERSION
    globals()['WEBAPP_VERSION'] = new_version
    
    await message.answer(
        f"🔄 **Версия обновлена**\n\n"
        f"Старая версия: {current_version}\n"
        f"Новая версия: {new_version}\n\n"
        f"Браузеры загрузят свежий код при следующем открытии WebApp\n"
        f"Сообщите пользователям закрыть и открыть заново"
    )

@router.message(F.text)
async def handle_text(message: types.Message):
    text = message.text.lower()
    if "help" in text:
        await message.answer("Use /help command")
    else:
        await message.answer("Use /profile to open app", reply_markup=get_profile_menu())

@router.callback_query(F.data == "clear_cache")
async def callback_clear_cache(query: types.CallbackQuery):
    await query.answer("🧹 Очистка кеша...", show_alert=False)
    await cmd_clearcache(query.message)
