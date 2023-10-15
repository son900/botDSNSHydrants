"""
Telegram bot handlers.
"""
from typing import List

from aiogram import types, Dispatcher, F
import aiogram.utils.markdown as fmt
from aiogram.filters import Command

from src.hydrants.dependencies import get_hydrants_service
from src.telegram.bot.keyboards import get_menu_keyboard, get_hydrant_keyboard


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

    await message.answer(
        fmt.text(
            fmt.text("Для пошуку найближчих джерел ППВ відправте Ваше"),
            fmt.text(f"місцезнаходження, або натисніть кнопку {fmt.hbold('Найближчі від мене')}\n"),
            fmt.text(f"Пошук за номером, та/або типом: {fmt.hbold('ПГ-1, ' 'ПГ-131, ' '131')}\n"),
            fmt.text(f"Уточнення населеного пункту: {fmt.hbold('смт. Солоне, ' 'смт. Петриківка')}"),
            fmt.text(f"(назва населеного пункту може бути частковою, наприклад: {fmt.hbold('петр')})"),
            fmt.hcode("Також пошук здійснюється за адресою, вказаною для прив'язки, чи описом вододжерела."),
            sep="\n",

        ),
        parse_mode="HTML",
        reply_markup=await get_menu_keyboard(),

    )


async def search(message: types.Message):
    """
    Searching hydrant handler.
    """
    if len(str(message.text)) >= 3:

        hydrants_service = get_hydrants_service()
        hydrants: List = await hydrants_service.hydrants_search(
            search_query=str(message.text)
        )
        if not hydrants:
            await message.answer(
                "За Вашим запитом нічого не знайдено.",
                reply_markup=await get_menu_keyboard(),

            )
        for hydrant in hydrants:
            await message.answer(
                fmt.text(
                    fmt.text(f"{fmt.hbold('Технічний стан:')} {hydrant.technical_condition}"),
                    fmt.text(f"{fmt.hbold('Тип гідранта:')}  {hydrant.type_hydrant}"),
                    fmt.text(f"{fmt.hbold('Вид розташування:')} {hydrant.type_location}"),
                    fmt.text(f"{fmt.hbold('Тип водомережі:')} {hydrant.type_water_network}"),
                    fmt.text(f"{fmt.hbold('Діаметра:')} {hydrant.type_diameter}"),
                    fmt.hbold("Прив'язка до адреси:"),
                    fmt.hcode(str(hydrant.address)),
                    fmt.hbold("Опис:"),
                    fmt.hcode(str(hydrant.description)),
                    sep="\n",

                ),
                parse_mode="HTML",
                reply_markup=get_hydrant_keyboard(
                    coordinates=hydrant.coordinates
                )
            )
    else:
        await message.answer(
            "Введіть щонайменше 3 символи.",
            reply_markup=await get_menu_keyboard(),

        )


async def search_by_location(message: types.Message):
    """
    Searching hydrant by location handler.
    """
    hydrants_service = get_hydrants_service()
    hydrants: List = await hydrants_service.hydrants_search_by_location(
        latitude=str(message.location.latitude),
        longitude=str(message.location.longitude)
    )
    if not hydrants:
        await message.answer(
            "За Вашим запитом нічого не знайдено.",
            reply_markup=await get_menu_keyboard(),

        )
    for hydrant in hydrants:
        await message.answer(
            fmt.text(
                fmt.text(f"{fmt.hbold('Технічний стан:')} {hydrant.technical_condition}"),
                fmt.text(f"{fmt.hbold('Тип гідранта:')}  {hydrant.type_hydrant}"),
                fmt.text(f"{fmt.hbold('Вид розташування:')} {hydrant.type_location}"),
                fmt.text(f"{fmt.hbold('Тип водомережі:')} {hydrant.type_water_network}"),
                fmt.text(f"{fmt.hbold('Діаметра:')} {hydrant.type_diameter}"),
                fmt.hbold("Прив'язка до адреси:"),
                fmt.hcode(str(hydrant.address)),
                fmt.hbold("Опис:"),
                fmt.hcode(str(hydrant.description)),
                sep="\n",

            ),
            parse_mode="HTML",
            reply_markup=get_hydrant_keyboard(
                coordinates=hydrant.coordinates
            )
        )


async def init_message(dp: Dispatcher):
    """
    Create handlers filter.
    """

    # register command
    dp.message.register(start, Command(commands=["start"]))
    dp.message.register(helps, Command(commands=["help"]))
    dp.message.register(search, F.text.regexp(r'.*'))
    dp.message.register(search_by_location, F.location)
