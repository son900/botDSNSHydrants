"""
URL configuration for config project.

"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static

from config import settings
from src.telegram.bot.endpoints import telegram_router


urlpatterns = [
    path("", lambda request: redirect("admin/")),
    path("admin/", admin.site.urls),
    path("api/", telegram_router.urls)
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)