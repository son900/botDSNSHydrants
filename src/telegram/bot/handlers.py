"""
Telegram bot handlers.
"""
from aiogram import types, Dispatcher, F
import aiogram.utils.markdown as fmt
from aiogram.filters import Command

from src.telegram.bot.keyboards import get_menu_keyboard


async def start(message: types.Message):
    """
    Start command.
    """

    await message.answer(
        "Введіть запит, або виберіть дію.",
        reply_markup=await get_menu_keyboard(),

    )


async def helps(message: types.Message):
    """
    Help command.
    """

    await message.answer(fmt.text(
        "Для пошуку найближчих джерел ППВ відправте Ваше \n"
        "місцезнаходження, або натисніть кнопку 'Найближчі від мене'.\n\n"
        "Пошук за номером, та/або типом: 'ПГ-1', 'пв 12', '123'.\n\n"
        "Уточнення населеного пункту: 'Полтава 12', 'Кременчук ПГ-2', "
        "назва населеного пункту може бути частковою, наприклад: 'глоб'\n\n"
        "Також пошук здійснюється за адресою, вказаною для прив'язки, чи описом вододжерела."
    ),

        reply_markup=await get_menu_keyboard(),

    )


async def reply(message: types.Message):
    """
    Start command.
    """

    await message.answer(
        "Вы отправили мне следующий текст: " + message.text,
        reply_markup=await get_menu_keyboard(),

    )


async def handle_location(message: types.Message):
    await message.answer(
        f"Вы отправили геолокацию: Широта: {message.location.latitude}, Долгота: {message.location.longitude}"
    )


async def init_message(dp: Dispatcher):
    """
    Create handlers filter.
    """

    # register command
    dp.message.register(start, Command(commands=["start"]))
    dp.message.register(helps, Command(commands=["help"]))
    dp.message.register(reply, F.text.regexp(r'.*'))
    dp.message.register(handle_location, F.location)

