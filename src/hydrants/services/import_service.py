# -*- coding: utf-8 -*-
"""
Hydrants import service.
"""
import logging
from typing import Type

from openpyxl.worksheet import worksheet

from src.core.services.base_service import BaseImportService
from src.hydrants.models import Hydrant, Subdivision, Owner

logger = logging.getLogger(__name__)


class HydrantsImportService(BaseImportService):
    """
    Hydrants import and update service.
    """

    hydrant_model: Type[Hydrant]
    subdivision_model: Type[Subdivision]
    owner_model: Type[Owner]

    def __init__(
        self,
        hydrant_model: Type[Hydrant],
        subdivision_model: Type[Subdivision],
        owner_model: Type[Owner],
    ):
        """
        Set models for import service.
        """
        self.hydrant_model = hydrant_model
        self.subdivision_model = subdivision_model
        self.owner_model = owner_model

    def read_data(
        self,
        sheet: worksheet,
    ):
        """
        Read the file with categories data.
        """
        hydrants_list = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if all(cell is None for cell in row):
                continue
            if row[9] is None:
                continue
            hydrants_list.append(
                {
                    "technical_condition": row[0],
                    "type_hydrant": row[1],
                    "type_location": row[2],
                    "address": row[5],
                    "type_water_network": row[6],
                    "type_diameter": row[7],
                    "description": row[8],
                    "coordinates": row[9]
                }
            )
        return hydrants_list

    def bulk_create_or_update_hydrants(
            self,
            hydrants_list: list,
    ) -> None:
        """
        Bulk create or update hydrants.
        """
        # get all hydrants
        countries = self.hydrant_model.objects.all()

        # create bulk list from hydrant classes
        bulk_list = [
            self.hydrant_model(
                technical_condition=hydrant.get("technical_condition"),
                type_hydrant=hydrant.get("type_hydrant"),
                type_location=hydrant.get("type_location"),
                type_water_network=hydrant.get("type_water_network"),
                type_diameter=hydrant.get("type_diameter"),
                address=hydrant.get("address"),
                description=hydrant.get("description"),
                coordinates=hydrant.get("coordinates")
            )
            for hydrant in hydrants_list
        ]

        # bulk create and update hydrants
        # self.hydrant_model.objects.bulk_create(
        #     bulk_list,
        #     update_conflicts=True,
        #     unique_fields=["coordinates"],
        #     update_fields=[
        #         "technical_condition",
        #         "type_hydrant",
        #         "type_location",
        #         "type_water_network",
        #         "type_diameter",
        #         "address",
        #         "description",
        #     ],
        # )

        self.hydrant_model.objects.bulk_create(
            bulk_list,
            ignore_conflicts=True,

        )




