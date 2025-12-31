"""
Обработчики команд Telegram бота
"""
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api_client import api_client
from keyboards import get_main_menu, get_services_keyboard, get_order_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

# ============ КОМАНДА /START ============

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start - регистрация или приветствие"""
    user = message.from_user
    if not user:
        await message.answer("❌ Ошибка: не удалось получить информацию о пользователе")
        return
    
    try:
        # Пытаемся получить пользователя из БД
        existing_user = await api_client.get_user(user.id)
        await message.answer(
            f"👋 С возвращением, {existing_user.get('first_name', 'друг')}!\n\n"
            f"💼 TgWork - фриланс-биржа в Telegram\n"
            f"📊 Твой рейтинг: {existing_user.get('rating', 0)}/5\n"
            f"💰 Баланс: {existing_user.get('balance', 0)} ₽",
            reply_markup=get_main_menu()
        )
    except Exception as e:
        # Новый пользователь - регистрируем
        logger.info(f"Регистрация нового пользователя {user.id}")
        try:
            new_user = await api_client.register_user(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name
            )
            await message.answer(
                f"👋 Добро пожаловать на TgWork!\n\n"
                f"🎉 Ты успешно зарегистрирован!\n"
                f"📍 Твой ID: {new_user.get('id')}\n\n"
                f"Теперь ты можешь:\n"
                f"✅ Искать услуги\n"
                f"✅ Создавать заказы\n"
                f"✅ Публиковать свои услуги",
                reply_markup=get_main_menu()
            )
        except Exception as reg_error:
            logger.error(f"Ошибка регистрации: {reg_error}")
            await message.answer(
                "❌ Ошибка при регистрации. Попробуй позже.",
                reply_markup=get_main_menu()
            )

# ============ КОМАНДА /HELP ============

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Справка по использованию бота"""
    help_text = """
🆘 **Справка по использованию TgWork**

**Основные команды:**
/start - Начать работу
/help - Эта справка
/profile - Посмотреть профиль
/services - Мои услуги
/orders - Мои заказы
/search - Поиск услуг

**Как пользоваться:**

1️⃣ **Ищешь услугу?**
   → /search ищешь по названию
   → Выбираешь из результатов
   → Создаёшь заказ

2️⃣ **Продаёшь услугу?**
   → /services (добавь свою)
   → Указываешь цену и описание
   → Жди заказы!

3️⃣ **В процессе работы:**
   → Общайся с заказчиком в чате
   → Отправляй результаты
   → Получай оценку

**Вопросы?**
Напиши /support или обратись к администратору.
"""
    await message.answer(help_text, parse_mode="Markdown")

# ============ КОМАНДА /PROFILE ============

@router.message(Command("profile"))
async def cmd_profile(message: types.Message):
    """Показать профиль пользователя через WebApp"""
    from keyboards import get_profile_menu
    
    user = message.from_user
    if not user:
        await message.answer("❌ Ошибка получения информации о пользователе")
        return
    
    try:
        profile = await api_client.get_user(user.id)
        
        profile_text = f"""
👤 <b>Ваш профиль</b>

📍 ID: {profile.get('id')}
👤 Имя: {profile.get('first_name', 'N/A')}
💬 Username: @{profile.get('username', 'нет')}
⭐ Рейтинг: {profile.get('rating', 0)}/5
📦 Заказов: {profile.get('completed_orders', 0)}
💰 Баланс: {profile.get('balance', 0)} ₽
💸 Заработано: {profile.get('total_earned', 0)} ₽
"""
        
        await message.answer(
            profile_text,
            parse_mode="HTML",
            reply_markup=get_profile_menu()
        )
    
    except Exception as e:
        logger.error(f"Ошибка получения профиля: {e}")
        await message.answer(f"❌ Ошибка: {str(e)}")

# ============ КОМАНДА /SEARCH ============

@router.message(Command("search"))
async def cmd_search(message: types.Message):
    """Начать поиск услуг"""
    await message.answer(
        "🔍 Введи название или категорию услуги:\n\n"
        "Примеры: логотип, копирайтинг, сайт, дизайн"
    )
    # Переходим в состояние ожидания ввода поискового запроса
    # Это обработаем в следующем обработчике

# ============ ТЕКСТОВЫЕ СООБЩЕНИЯ (поиск) ============

@router.message(F.text)
async def handle_search_query(message: types.Message):
    """Обработка текстового ввода для поиска"""
    if message.text is None:
        await message.answer("❌ Ошибка: пусто")
        return
    
    query = message.text
    
    if query.startswith("/"):
        # Если это команда, игнорируем
        return
    
    try:
        # Ищем услуги
        services = await api_client.search_services(query, limit=10)
        
        if not services:
            await message.answer(f"❌ Услуг по запросу '{query}' не найдено")
            return
        
        # Показываем результаты
        response_text = f"🔍 **Результаты поиска по: '{query}'**\n\n"
        
        for idx, service in enumerate(services[:10], 1):
            response_text += (
                f"{idx}. **{service.get('title')}**\n"
                f"   💰 {service.get('price')} ₽\n"
                f"   👨‍💼 Продавец: {service.get('seller_username', 'N/A')}\n"
                f"   📌 Статус: {service.get('status', 'unknown')}\n"
                f"   ⭐ Рейтинг продавца: {service.get('seller_rating', 0)}\n"
                f"/service_{service.get('id')}\n\n"
            )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"📦 Услуга {i+1}", callback_data=f"service_{services[i].get('id')}")]
            for i in range(min(3, len(services)))
        ] + [
            [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
        ])
        
        await message.answer(response_text, parse_mode="Markdown", reply_markup=keyboard)
    
    except Exception as e:
        logger.error(f"Ошибка поиска: {e}")
        await message.answer(f"❌ Ошибка при поиске: {str(e)}")

# ============ КОМАНДА /ORDERS ============

@router.message(Command("orders"))
async def cmd_orders(message: types.Message):
    """Показать мои заказы"""
    user = message.from_user
    if not user:
        await message.answer("❌ Ошибка получения информации о пользователе")
        return
    
    try:
        # Получаем заказы где я покупатель
        buyer_orders = await api_client.get_buyer_orders(user.id, limit=5)
        # Получаем заказы где я продавец
        seller_orders = await api_client.get_seller_orders(user.id, limit=5)
        
        response_text = "📦 **Мои заказы**\n\n"
        
        if buyer_orders:
            response_text += "**👤 Как покупатель:**\n"
            for order in buyer_orders:
                response_text += (
                    f"  • Заказ #{order.get('id')} - {order.get('status')}\n"
                    f"    Сумма: {order.get('price')} ₽\n"
                )
        
        if seller_orders:
            response_text += "\n**👨‍💼 Как продавец:**\n"
            for order in seller_orders:
                response_text += (
                    f"  • Заказ #{order.get('id')} - {order.get('status')}\n"
                    f"    Сумма: {order.get('price')} ₽\n"
                )
        
        if not buyer_orders and not seller_orders:
            response_text += "У тебя пока нет заказов. Начни с поиска услуг! 🔍"
        
        await message.answer(response_text, parse_mode="Markdown")
    
    except Exception as e:
        logger.error(f"Ошибка получения заказов: {e}")
        await message.answer(f"❌ Ошибка: {str(e)}")

# ============ КОМАНДА /SERVICES ============

@router.message(Command("services"))
async def cmd_services(message: types.Message):
    """Мои услуги"""
    user = message.from_user
    if not user:
        await message.answer("❌ Ошибка получения информации о пользователе")
        return
    
    try:
        services = await api_client.get_seller_services(user.id)
        
        if not services:
            await message.answer(
                "📭 У тебя пока нет услуг.\n\n"
                "Создай первую услугу, чтобы начать зарабатывать! 💰",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="➕ Создать услугу", callback_data="create_service")],
                    [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
                ])
            )
            return
        
        response_text = "📦 **Твои услуги:**\n\n"
        for service in services:
            response_text += (
                f"**{service.get('title')}**\n"
                f"💰 Цена: {service.get('price')} ₽\n"
                f"📌 Статус: {service.get('status')}\n"
                f"⏱️ Дней на выполнение: {service.get('execution_days')}\n"
                f"/service_{service.get('id')}\n\n"
            )
        
        await message.answer(
            response_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="➕ Новая услуга", callback_data="create_service")],
                [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
            ])
        )
    
    except Exception as e:
        logger.error(f"Ошибка получения услуг: {e}")
        await message.answer(f"❌ Ошибка: {str(e)}")
