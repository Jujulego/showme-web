# Importations
from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    # Liste
    list_display = ("nom", "pluriel")
    search_fields = ("nom",)
