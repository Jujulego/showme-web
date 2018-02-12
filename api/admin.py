# Importations
from django.contrib import admin
from django.db.models import Q

from .models import *


# Register your models here.
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    # Liste
    list_display = ("nom", "pluriel")
    search_fields = ("nom",)


@admin.register(Lieu)
class LieuAdmin(admin.ModelAdmin):
    # Filtres
    class PhotoFiltre(admin.SimpleListFilter):
        # Attributs
        title = "photo"
        parameter_name = "photo"

        # Méthodes
        def lookups(self, request, model_admin):
            return [
                ("v", "avec"),
                ("f", "sans"),
            ]

        def queryset(self, request, queryset):
            if self.value() == "v":
                return queryset.filter(~Q(photo=""))
            elif self.value() == "f":
                return queryset.filter(photo="")

            return queryset

    # Liste
    list_display = ("nom", "latitude", "longitude", "a_photo")
    list_filter = (PhotoFiltre,)
    search_fields = ("nom",)
