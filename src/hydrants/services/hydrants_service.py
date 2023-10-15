# -*- coding: utf-8 -*-
"""
Service for twitter's models.
"""
import decimal
from typing import Type
from django.db.models import QuerySet, Q
from src.hydrants.models import Hydrant, Subdivision, Owner, TechnicalConditionChoices
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import Sqrt
from math import radians, cos


class HydrantsService:
    """
    Service for hydrants models.
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

    async def hydrants_search(
            self,
            search_query: str,
    ) -> list[Hydrant]:
        """
        Hydrants search by description or address.
        """
        query = Q(technical_condition=TechnicalConditionChoices.SERVICEABLE)
        if search_query:
            query = query & (Q(description__icontains=search_query) | Q(address__icontains=search_query))
        queryset: QuerySet = (
            self.hydrant_model.objects.filter(
                query,
            )
            .prefetch_related(
                "owner",
                "subdivision"
            )
        )
        return [obj async for obj in queryset][:10]

    async def hydrants_search_by_location(
            self,
            latitude: str,
            longitude: str
    ):
        """
        Hydrants search by description or address.
        """

        search_latitude = decimal.Decimal(latitude)
        search_longitude = decimal.Decimal(longitude)

        radius_km = 5

        latitude_float = ExpressionWrapper(F('latitude'), output_field=FloatField())
        longitude_float = ExpressionWrapper(F('longitude'), output_field=FloatField())

        queryset = self.hydrant_model.objects.annotate(
            distance=Sqrt(
                ExpressionWrapper(
                    (69.1 * (latitude_float - float(search_latitude))) ** 2 +
                    (69.1 * (float(search_longitude) - longitude_float) * cos(radians(float(search_latitude)))) ** 2,
                    output_field=FloatField()
                )
            )
        ).filter(
            distance__lte=radius_km,
            technical_condition=TechnicalConditionChoices.SERVICEABLE
        ).order_by(
            "distance"
        )
        return [obj async for obj in queryset][:10]

