# Importations
from django.urls import register_converter, path

from .converters import ReelConverter
from . import views


# Converters
register_converter(ReelConverter, 'reel')

# Urls
urlpatterns = [
    # Lieux
    path("<reel:latitude>:<reel:longitude>/<int:distance>/", views.lieux, name="lieux"),

    # Objets
    path("lieu/<int:lieu_id>/", views.lieu,  name="lieu"),

    path("types/",              views.types, name="types"),
    path("type/<int:type_id>/", views.type,  name="type"),
]
