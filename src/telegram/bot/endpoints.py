"""
Telegram bot endpoints.
"""
import asyncio
import json

from django.http import JsonResponse
from ninja import NinjaAPI
from aiogram import Bot, types, Dispatcher

from src.telegram.bot.handlers import init_message

telegram_router = NinjaAPI()

dp = Dispatcher()


@telegram_router.post("/bot/{token}")
def bot_webhook(request, token: str):
    """
    Endpoint webhook bot.
    """
    asyncio.run(init_message(dp))
    update = json.loads(request.body)
    bot = Bot(token=token)
    telegram_update = types.Update(**update)
    asyncio.run(dp.feed_update(bot=bot, update=telegram_update))
    asyncio.run(bot.session.close())
    return JsonResponse({}, status=200)
