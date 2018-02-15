# Importations
from django.contrib import admin

from .models import Type, Lieu


# Register your models here.
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    # Liste
    list_display = ("nom",)
    search_fields = ("nom",)

    # Edition
    fields = ("nom", "api")
    readonly_fields = ("nom",)


@admin.register(Lieu)
class LieuAdmin(admin.ModelAdmin):
    # Liste
    list_display = ("lieu", "a_jour")
    search_fields = ("lieu__nom",)

    # Edition
    fields = ("google_id", "lieu", "types")

    filter_horizontal = ("types",)
    readonly_fields = ("google_id",)
