# -*- coding: utf-8 -*-
"""
Hydrants dependencies.
"""
from functools import lru_cache

from src.hydrants.models import Hydrant, Subdivision, Owner
from src.hydrants.services.import_service import HydrantsImportService


@lru_cache()
def get_hydrants_import_service() -> HydrantsImportService:
    """
    Get HydrantsImportService.

    :return: HydrantsImportService

    """
    return HydrantsImportService(
        hydrant_model=Hydrant,
        subdivision_model=Subdivision,
        owner_model=Owner
    )