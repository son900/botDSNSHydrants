"""
Telegram bot keyboards.
"""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


async def get_menu_keyboard():
    """
    Get menu keyboard.
    """
    kb = [
        [KeyboardButton(text="Найближчі від мене", request_location=True)],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def get_hydrant_keyboard(coordinates: str):
    """
    Get hydrant keyboard.
    """
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Показати на карті",
        url=f"https://www.google.com/maps/search/?api=1&query={coordinates}"
    ))
    return builder.as_markup()

