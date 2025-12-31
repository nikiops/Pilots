"""
Клавиатуры и меню для Telegram бота
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# WebApp URL для профиля (запусти: python telegram-bot/webapp/server.py)
WEBAPP_URL = "http://localhost:8080/profile.html"

def get_main_menu() -> ReplyKeyboardMarkup:
    """Главное меню"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Найти услугу")],
            [KeyboardButton(text="📦 Мои заказы"), KeyboardButton(text="👨‍💼 Мои услуги")],
            [KeyboardButton(text="👤 Профиль"), KeyboardButton(text="❓ Помощь")],
        ],
        resize_keyboard=True
    )

def get_profile_menu() -> InlineKeyboardMarkup:
    """Меню профиля с WebApp"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📱 Открыть профиль (WebApp)",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )],
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_profile")],
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="main_menu")]
    ])

def get_services_keyboard(services: list) -> InlineKeyboardMarkup:
    """Клавиатура со списком услуг"""
    buttons = []
    for service in services[:5]:
        buttons.append([
            InlineKeyboardButton(
                text=f"📦 {service.get('title')[:30]}... ({service.get('price')} ₽)",
                callback_data=f"service_{service.get('id')}"
            )
        ])
    
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_order_keyboard(order_id: int, order_status: str, user_role: str) -> InlineKeyboardMarkup:
    """Клавиатура для управления заказом"""
    buttons = []
    
    # Кнопки в зависимости от статуса и роли
    if user_role == "buyer" and order_status == "WAITING_PAYMENT":
        buttons.append([InlineKeyboardButton(text="💳 Оплатить заказ", callback_data=f"pay_order_{order_id}")])
    
    if order_status in ["IN_PROGRESS", "WAITING_PAYMENT"]:
        buttons.append([InlineKeyboardButton(text="💬 Написать сообщение", callback_data=f"message_{order_id}")])
    
    if order_status == "UNDER_REVIEW" and user_role == "buyer":
        buttons.append([InlineKeyboardButton(text="⭐ Оставить отзыв", callback_data=f"review_{order_id}")])
    
    if order_status in ["WAITING_PAYMENT", "IN_PROGRESS"]:
        buttons.append([InlineKeyboardButton(text="❌ Отменить заказ", callback_data=f"cancel_order_{order_id}")])
    
    buttons.append([InlineKeyboardButton(text="⬅️ Назад к заказам", callback_data="orders_list")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_rating_keyboard(order_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для выбора рейтинга"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⭐", callback_data=f"rate_1_{order_id}"),
            InlineKeyboardButton(text="⭐⭐", callback_data=f"rate_2_{order_id}"),
            InlineKeyboardButton(text="⭐⭐⭐", callback_data=f"rate_3_{order_id}"),
        ],
        [
            InlineKeyboardButton(text="⭐⭐⭐⭐", callback_data=f"rate_4_{order_id}"),
            InlineKeyboardButton(text="⭐⭐⭐⭐⭐", callback_data=f"rate_5_{order_id}"),
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"order_{order_id}")]
    ])

def get_service_detail_keyboard(service_id: int, is_owner: bool = False) -> InlineKeyboardMarkup:
    """Клавиатура для детальной страницы услуги"""
    buttons = []
    
    if is_owner:
        buttons.append([InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit_service_{service_id}")])
        buttons.append([InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete_service_{service_id}")])
    else:
        buttons.append([InlineKeyboardButton(text="🛒 Заказать", callback_data=f"order_service_{service_id}")])
    
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="search_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_top_sellers_keyboard(sellers: list) -> InlineKeyboardMarkup:
    """Клавиатура со списком топ продавцов"""
    buttons = []
    for seller in sellers[:5]:
        buttons.append([
            InlineKeyboardButton(
                text=f"⭐{seller.get('rating', 0)}/5 - {seller.get('first_name', 'Продавец')}",
                callback_data=f"seller_{seller.get('id')}"
            )
        ])
    
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_yes_no_keyboard(action_id: str) -> InlineKeyboardMarkup:
    """Клавиатура с кнопками Да/Нет"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да", callback_data=f"yes_{action_id}"),
            InlineKeyboardButton(text="❌ Нет", callback_data=f"no_{action_id}"),
        ]
    ])
