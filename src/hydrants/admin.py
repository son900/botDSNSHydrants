from django.contrib import admin
from src.hydrants.models import Hydrant, Subdivision, Owner

# Register your models here.

admin.site.register(Hydrant)
admin.site.register(Subdivision)
admin.site.register(Owner)
