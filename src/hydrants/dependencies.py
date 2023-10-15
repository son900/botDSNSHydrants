# -*- coding: utf-8 -*-
"""
Hydrants dependencies.
"""
from functools import lru_cache

from src.hydrants.models import Hydrant, Subdivision, Owner
from src.hydrants.services.hydrants_service import HydrantsService
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


@lru_cache()
def get_hydrants_service() -> HydrantsService:
    """
    Get HydrantsService.

    :return: HydrantsService

    """
    return HydrantsService(
        hydrant_model=Hydrant,
        subdivision_model=Subdivision,
        owner_model=Owner
    )
