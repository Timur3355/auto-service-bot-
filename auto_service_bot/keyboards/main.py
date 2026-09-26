from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.services import SERVICES

def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="🔧 Калькулятор", callback_data="calc_start")],
        [InlineKeyboardButton(text="📅 Записаться", callback_data="book_start")]
    ])

def get_catalog_kb():
    btns = [[InlineKeyboardButton(text=f"{s['name']} ({s['price']}р)", callback_data=f"srv_{s['id']}")] for s in SERVICES]
    btns.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=btns)

def get_date_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сегодня", callback_data="d_today")],
        [InlineKeyboardButton(text="Завтра", callback_data="d_tomorrow")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
    ])
