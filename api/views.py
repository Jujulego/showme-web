# Importations
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.db.models import F
from django.shortcuts import get_object_or_404, render

from .models import Lieu, Type


# Vues
# - lieux
def lieux(request, latitude, longitude, distance):
    qs = Lieu.objects.all()\
        .annotate(distance=Distance(F("position"), Point(y=latitude, x=longitude, srid=4326)))\
        .filter(distance__lt=D(m=distance).m)\
        .order_by("distance")

    return render(request, "api/lieux.json", {"lieux": qs}, content_type="text/json; charset=utf8")


# - objets
def lieu(request, lieu_id):
    lieu = get_object_or_404(Lieu, pk=lieu_id)
    return render(request, "api/lieu.json", {"lieu": lieu}, content_type="text/json; charset=utf8")


def types(request):
    types = Type.objects.all()
    return render(request, "api/types.json", {"types": types}, content_type="text/json; charset=utf8")


def type(request, type_id):
    type = get_object_or_404(Type, pk=type_id)
    return render(request, "api/type.json", {"type": type}, content_type="text/json; charset=utf8")
