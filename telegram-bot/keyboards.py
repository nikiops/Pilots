"""
Клавиатуры и меню для Telegram бота
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import os
from dotenv import load_dotenv

load_dotenv()

# WebApp URL для входа/профиля через NGROK
# Пытаемся получить из переменной окружения, если нет - используем fallback
WEBAPP_URL = os.getenv('NGROK_URL', 'https://localhost:3000/index.html')

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
            text="� ВОЙТИ В ПРИЛОЖЕНИЕ",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )],
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


