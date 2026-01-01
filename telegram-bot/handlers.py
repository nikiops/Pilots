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
    await message.answer(
        "🧹 **Очистка кеша TgWork**\n\n"
        "**Способ 1️⃣ (Быстрый):**\n"
        "1. Откройте WebApp\n"
        "2. Нажмите ☰ меню → 🧹 Очистить кеш\n"
        "3. Приложение перезагрузится\n\n"
        "**Способ 2️⃣ (Полная очистка):**\n"
        "1. Закройте WebApp\n"
        "2. Выйдите из Telegram ПОЛНОСТЬЮ\n"
        "3. Очистите кеш Telegram:\n"
        "   ⚙️ → Хранилище и кеш → Очистить кеш\n"
        "4. Откройте Telegram\n"
        "5. Запустите WebApp\n\n"
        "⏳ Подождите 10-15 сек на загрузке",
        parse_mode="Markdown"
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
