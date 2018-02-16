# Importations
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe


from .models import Type, Lieu, Log


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
    fieldsets = (
        ('', {
            "fields": ("google_id", "lieu", "types"),
        }),
        ("Journal", {
            "fields": ("liens_logs",),
            "classes": ("collapse",),
        })
    )

    filter_horizontal = ("types",)
    readonly_fields = ("google_id", "liens_logs")

    # Méthodes
    def liens_logs(self, instance):
        html = "<table>"

        for log in instance.logs.order_by("date"):
            html += "<tr><td><a href=\"{:s}\">{:s}</a></td><td>{:s}</td></tr>".format(
                reverse("admin:google_log_change", args=(log.pk,)),
                str(log),
                Log.type2text(log.type)
            )
            pass

        html += "</table>"

        return mark_safe(html)

    liens_logs.short_description = "journal"


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    # Liste
    list_display = ("date", "type")
    list_filter = ("type",)

    # Edition
    fieldsets = (
        ("Informations", {
            "fields": ("date", "type"),
        }),
        ("Lieux", {
            "fields": ("liens_lieux",),
            "classes": ("collapse",),
        })
    )
    readonly_fields = ("date", "type", "liens_lieux")

    # Méthodes
    def liens_lieux(self, instance):
        html = "<p>"

        for lieu in instance.lieu_set.all():
            html += "<a href=\"{:s}\">{:s}</a><br/>".format(
                reverse("admin:google_lieu_change", args=(lieu.pk,)),
                lieu.lieu.nom
            )

        html += "</p>"

        return mark_safe(html)

    liens_lieux.short_description = "lieux"
