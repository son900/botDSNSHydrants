# -*- coding: utf-8 -*-
"""
Module for the management command 'init_project'.
"""
import asyncio

from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from aiogram import Bot
from src.hydrants.models import Hydrant
from config import settings
from src.hydrants.dependencies import get_hydrants_import_service


class Command(BaseCommand):
    """
    Command for basic data initialization.
    """

    def handle(self, test_mode=False, *args, **options):
        """
        Handle command.
        """
        self._create_superuser()
        self._import_hydrants()
        async_to_sync(self.set_webhook)()

    @staticmethod
    def _create_superuser():
        """
        Create superuser.
        """
        user, created = User.objects.update_or_create(
            is_superuser=True,
            defaults={
                "username": settings.SUPERUSER_USERNAME,
                "is_staff": True,
                "is_active": True,
            },
        )
        user.set_password(settings.SUPERUSER_PASSWORD)
        user.save()

    @staticmethod
    def _import_hydrants():
        """
        Import hydrants.
        """
        if not Hydrant.objects.all().exists():
            # get hydrants import service
            hydrants_import_service = get_hydrants_import_service()

            # start import
            hydrants_import_service.start_import()

    @staticmethod
    async def set_webhook():
        """
        Check and set new webhook.
        """
        # get webhook url
        webhook_url: str = settings.WEBHOOK_URL
        bot = Bot(token=settings.API_TOKEN)
        webhook_info = await bot.get_webhook_info()

        if webhook_info.url != webhook_url:
            await bot.set_webhook(url=webhook_url)
        await bot.session.close()
