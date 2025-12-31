"""
Обработчики callback запросов (нажатие inline кнопок)
"""
from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api_client import api_client
import logging

logger = logging.getLogger(__name__)
router = Router()

# ============ ГЛАВНОЕ МЕНЮ ============

@router.callback_query(F.data == "main_menu")
async def callback_main_menu(query: types.CallbackQuery):
    """Вернуться в главное меню"""
    await query.message.edit_text(
        "TgWork - Frilanc birzha\n\nVyberi deystvie iz menyu:"
    )
    await query.answer()

# ============ УСЛУГИ ============

@router.callback_query(F.data.startswith("service_"))
async def callback_service_detail(query: types.CallbackQuery):
    """Показать детали услуги"""
    service_id = int(query.data.split("_")[1])
    
    try:
        service = await api_client.get_service(service_id)
        seller = await api_client.get_user_profile(service.get("seller_id"))
        
        text = f"Usluga: {service.get('title')}\n"
        text += f"Tsena: {service.get('price')} RUB\n"
        text += f"Dney: {service.get('execution_days')}\n"
        text += f"Prodavets: {seller.get('first_name')}\n"
        text += f"Rejting: {seller.get('rating')}/5"
        
        buttons = [
            [InlineKeyboardButton(text="Zakaza", callback_data=f"order_service_{service_id}")],
            [InlineKeyboardButton(text="Nazad", callback_data="main_menu")]
        ]
        
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    except Exception as e:
        await query.message.edit_text(f"Oshibka: {e}")
    
    await query.answer()

# ============ ЗАКАЗЫ ============

@router.callback_query(F.data.startswith("order_service_"))
async def callback_order_service(query: types.CallbackQuery):
    """Создать заказ"""
    service_id = int(query.data.split("_")[2])
    
    try:
        order = await api_client.create_order(query.from_user.id, service_id)
        
        text = f"Zakaz sodan! ID: {order.get('id')}\nSumma: {order.get('price')} RUB"
        buttons = [
            [InlineKeyboardButton(text="Oplatit", callback_data=f"pay_order_{order.get('id')}")],
            [InlineKeyboardButton(text="Nazad", callback_data="main_menu")]
        ]
        
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    except Exception as e:
        await query.message.edit_text(f"Oshibka: {e}")
    
    await query.answer()

@router.callback_query(F.data.startswith("pay_order_"))
async def callback_pay_order(query: types.CallbackQuery):
    """Оплатить заказ"""
    order_id = int(query.data.split("_")[2])
    
    try:
        order = await api_client.pay_order(order_id)
        
        text = f"Zakaz oplachen! ID: {order_id}\nStatus: {order.get('status')}"
        buttons = [
            [InlineKeyboardButton(text="Chat", callback_data=f"chat_order_{order_id}")],
            [InlineKeyboardButton(text="Nazad", callback_data="main_menu")]
        ]
        
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    except Exception as e:
        await query.message.edit_text(f"Oshibka: {e}")
    
    await query.answer()

@router.callback_query(F.data.startswith("chat_order_"))
async def callback_chat_order(query: types.CallbackQuery):
    """Чат заказа"""
    order_id = int(query.data.split("_")[2])
    
    try:
        messages = await api_client.get_messages(order_id, limit=5)
        
        text = f"Chat zakaza {order_id}:\n\n"
        if messages:
            for msg in messages[-3:]:
                text += f"- {msg.get('text', 'N/A')}\n"
        else:
            text += "Net soobshenniy"
        
        buttons = [
            [InlineKeyboardButton(text="Napisat", callback_data=f"message_{order_id}")],
            [InlineKeyboardButton(text="Nazad", callback_data="main_menu")]
        ]
        
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    except Exception as e:
        await query.message.edit_text(f"Oshibka: {e}")
    
    await query.answer()

# ============ ПРОФИЛЬ ============

@router.callback_query(F.data == "main_menu")
async def callback_main_menu_profile(query: types.CallbackQuery):
    """Обработка нажатия на кнопку профиля"""
    from keyboards import get_profile_menu
    
    try:
        user_id = query.from_user.id
        user = await api_client.get_user_profile(user_id)
        
        text = f"👤 <b>Ваш профиль</b>\n\n"
        text += f"Имя: <b>{user.get('name', 'Не указано')}</b>\n"
        text += f"Username: @{user.get('username', 'N/A')}\n"
        text += f"Рейтинг: ⭐ {user.get('rating', 0)}/5.0\n"
        text += f"Услуг: {user.get('services_count', 0)}\n"
        text += f"Заказов: {user.get('completed_orders', 0)}\n"
        
        await query.message.edit_text(text, reply_markup=get_profile_menu())
    except Exception as e:
        logger.error(f"Ошибка профиля: {e}")
        await query.message.edit_text(f"❌ Ошибка при загрузке профиля: {str(e)}")
    
    await query.answer()

@router.callback_query(F.data == "edit_profile")
async def callback_edit_profile(query: types.CallbackQuery):
    """Редактирование профиля"""
    await query.message.edit_text(
        "✏️ <b>Редактирование профиля</b>\n\n"
        "Функция будет реализована в следующих версиях.\n"
        "Сейчас вы можете обновить профиль через WebApp."
    )
    await query.answer()

@router.callback_query()
async def callback_unknown(query: types.CallbackQuery):
    """Неизвестный callback"""
    await query.answer("Neizvestnaya komanda", show_alert=True)
