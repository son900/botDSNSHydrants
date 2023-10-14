from django.contrib import admin
from src.hydrants.models import Hydrant, Subdivision, Owner


# Register your models here.


class HydrantAdmin(admin.ModelAdmin):
    """
    Hydrant admin model.
    """

    search_fields = ("address",)
    list_display = ("address", "technical_condition", "type_hydrant", "type_location")


class OwnerAdmin(admin.ModelAdmin):
    """
    Owner admin model.
    """

    search_fields = ("name",)
    list_display = ("name",)


class SubdivisionAdmin(admin.ModelAdmin):
    """
    Subdivision admin model.
    """

    search_fields = ("name",)
    list_display = ("name",)


admin.site.register(Hydrant, HydrantAdmin)
admin.site.register(Subdivision, SubdivisionAdmin)
admin.site.register(Owner, OwnerAdmin)
