# Importations
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.db.models import Q

from .models import *


# Register your models here.
@admin.register(Lieu)
class LieuAdmin(OSMGeoAdmin):
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
    class TypeFiltre(admin.SimpleListFilter):
        # Attributs
        title = "categorie"
        parameter_name = "categorie"

        # Méthodes
        def lookups(self, request, model_admin):
            qs = Type.objects.all().only('id', 'nom')
            return [(t.id, t.nom) for t in qs]

        def queryset(self, request, queryset):
            if self.value():
                return queryset.filter(types__id=self.value())

            return queryset

    # Carte
    openlayers_url = "https://openlayers.org/api/2.13.1/OpenLayers.js"

    # Liste
    list_display = ("nom", "latitude", "longitude", "a_photo")
    list_filter = (TypeFiltre,PhotoFiltre)
    search_fields = ("nom",)

    # Edition
    fieldsets = (
        ("Informations", {
            "fields": ("nom", "types", "position", ("latitude", "longitude")),
        }),
        ("Adresse", {
            "fields": (("numero", "route"), ("codepostal", "ville"), "departement", "region", "pays"),
            "classes": ("collapse",),
        }),
        ("Informations additionnelles", {
            "fields": ("telephone", "note", "site", "prix"),
            "classes": ("collapse",),
        })
    )

    filter_horizontal = ("types",)
    readonly_fields = ("latitude", "longitude")


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    # Liste
    list_display = ("nom", "pluriel")
    search_fields = ("nom",)
