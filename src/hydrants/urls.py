"""
Hydrants urls.
"""
from django.urls import path, include

from src.hydrants.views import HydrantsImportView

app_name = "hydrants"

urlpatterns = [
    path("", HydrantsImportView.as_view(), name="import"),
]
