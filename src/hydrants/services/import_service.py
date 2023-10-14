# -*- coding: utf-8 -*-
"""
Hydrants import service.
"""
import logging
import os
from typing import Type

from django.core.exceptions import ObjectDoesNotExist
from openpyxl.worksheet import worksheet

from config import settings
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

    def start_import(self):
        """
        Start import process.
        """
        # get file path (file with hydrants.xlsx)
        file_path = os.path.join(settings.SAMPLES_DIR, "hydrants.xlsx")

        with open(file_path, "rb") as file:
            # get sheet
            sheet = self.get_sheet(file.read())

        # get data in sheet
        data = self._read_data(sheet)

        # create hydrants
        self._bulk_create_hydrants(
            hydrants_list=data[0]
        )

        # set relationship for hydrants
        self._set_relationship_for_hydrants(
            relationship_list=data[3],
            subdivisions_list=data[2],
            owners_list=data[1]
        )

    @staticmethod
    def _read_data(
        sheet: worksheet,
    ) -> tuple[list, list, list, list]:
        """
        Read the file with categories data.
        """
        hydrants_list: list = []
        owners_list: list = []
        subdivisions_list: list = []
        relationship_list: list = []

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
            if row[3]:
                owners_list.append(
                    {
                        "name": row[3]
                    }
                )
            if row[4]:
                subdivisions_list.append(
                    {
                        "name": row[4]
                    }
                )
            relationship_list.append(
                {
                    "coordinates": row[9],
                    "owner_name": row[3],
                    "subdivision_name": row[4],
                },
            )

        return hydrants_list, owners_list, subdivisions_list, relationship_list

    def _bulk_create_hydrants(
        self,
        hydrants_list: list,
    ) -> None:
        """
        Bulk create hydrants.
        """
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

        self.hydrant_model.objects.bulk_create(
            bulk_list,
            ignore_conflicts=True,
        )

    def _bulk_create_owners(
        self,
        owners_list: list,
    ) -> None:
        """
        Bulk create owners.
        """
        # create bulk list from owner classes
        bulk_list = [
            self.owner_model(
                name=owner.get("name"),
            )
            for owner in owners_list
        ]

        self.owner_model.objects.bulk_create(
            bulk_list,
            ignore_conflicts=True,
        )

    def _bulk_create_subdivisions(
        self,
        subdivisions_list: list,
    ) -> None:
        """
        Bulk create subdivisions.
        """
        # create bulk list from subdivisions classes
        bulk_list = [
            self.subdivision_model(
                name=subdivision.get("name"),
            )
            for subdivision in subdivisions_list
        ]

        self.subdivision_model.objects.bulk_create(
            bulk_list,
            ignore_conflicts=True,
        )

    def _set_relationship_for_hydrants(
            self,
            relationship_list: list,
            subdivisions_list: list,
            owners_list: list,
    ) -> None:
        """
        Set a relationship between owner, subdivision and hydrants.
        """
        # bulk create tags
        self._bulk_create_owners(
            owners_list=owners_list,
        )
        # bulk create keys
        self._bulk_create_subdivisions(
            subdivisions_list=subdivisions_list,
        )

        # get hydrant by coordinates and set owner and subdivision relationship
        for hydrant in relationship_list:
            coordinates = hydrant.get("coordinates")
            owner_name = hydrant.get("owner_name")
            subdivision_name = hydrant.get("subdivision_name")
            try:
                obj = self.hydrant_model.objects.get(
                    coordinates=coordinates,
                )
                # set owner to hydrant object
                owner = self.owner_model.objects.filter(name=owner_name)
                if owner.exists():
                    obj.owner = owner.first()

                # set subdivision to hydrant object
                subdivision = self.subdivision_model.objects.filter(name=subdivision_name)
                if subdivision.exists():
                    obj.subdivision = subdivision.first()

                # save object
                obj.save()

            except ObjectDoesNotExist:
                continue


