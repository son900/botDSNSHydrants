"""
URL configuration for config project.

"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path("", lambda request: redirect("hydrants/")),
    path("hydrants/", include("src.hydrants.urls", namespace="hydrants")),
    path("admin/", admin.site.urls),
]
