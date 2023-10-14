"""
Telegram bot keyboards.
"""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def get_menu_keyboard():
    """
    Get menu keyboard.
    """
    kb = [
        [KeyboardButton(text="Найближчі вододжерела", request_location=True)],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)



