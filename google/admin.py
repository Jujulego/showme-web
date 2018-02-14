# Importations
from django.contrib import admin

from .models import Type, Lieu


# Register your models here.
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    # Liste
    list_display = ("name",)
    search_fields = ("name",)

    # Edition
    fields = ("name", "api")
    readonly_fields = ("name",)


@admin.register(Lieu)
class LieuAdmin(admin.ModelAdmin):
    # Liste
    list_display = ("lieu", "a_jour")
