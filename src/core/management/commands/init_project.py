# -*- coding: utf-8 -*-
"""
Module for the management command 'init_project'.
"""

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from config import settings


class Command(BaseCommand):
    """
    Command for basic data initialization.
    """

    def handle(self, test_mode=False, *args, **options):
        """
        Handle command.
        """
        self._create_superuser()

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

