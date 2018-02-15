# Importations
from random import choice, random

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import transaction

import googlemaps

from api.models import Lieu as ApiLieu, Horaire
from .models import Lieu, Type, Log


# Fonctions
def get_gmaps():
    # Connexion
    return googlemaps.Client(
        key=settings.MAPS["API_KEY"],
        queries_per_second=settings.MAPS["QUERIES_PER_SECONDS"]
    )


def random_point():
    # Choix de la bbox
    bbox = choice(settings.MAPS["BBOX"])

    # Choix d'un point à l'intérieur
    lat = min(bbox[0][0], bbox[1][0]) + random() * abs(bbox[1][0] - bbox[0][0])
    lng = min(bbox[0][1], bbox[1][1]) + random() * abs(bbox[1][1] - bbox[0][1])

    return lat, lng


@transaction.atomic
def majLieu(gmaps, lieu):
    # Requete
    donnees = gmaps.place(place_id=lieu.google_id, language=settings.MAPS["LANGUAGE"])
    donnees = donnees["result"]

    # Maj
    lieu = _maj(gmaps, lieu, donnees)
    lieu.logs.create(type=Log.MISE_A_JOUR)


@transaction.atomic
def _maj(gmaps, lieu, donnees):
    # Changement !
    if lieu.google_id != donnees["place_id"]:
        # Suppression !
        lieu.lieu.delete()

        # Récupération / création du lieu
        lieu, cree = Lieu.objects.get_or_create(google_id=donnees["place_id"])

        if cree:
            lieu.lieu = ApiLieu()

    # Maj des infos
    lieu.lieu.latitude = donnees["geometry"]["location"]["lat"]
    lieu.lieu.longitude = donnees["geometry"]["location"]["lat"]
    lieu.lieu.nom = donnees["name"]

    lieu.lieu.telephone = donnees.get("international_phone_number", "")
    lieu.lieu.note = donnees.get("rating", None)
    lieu.lieu.site = donnees.get("website", None)
    lieu.lieu.prix = donnees.get("price_level", None)

    adresse = donnees.get("address_components", None)
    if adresse is not None:
        for p in adresse:
            if "street_number" in p["types"]:
                lieu.lieu.numero = p["long_name"]
            elif "route" in p["types"]:
                lieu.lieu.route = p["long_name"]
            elif "locality" in p["types"]:
                lieu.lieu.ville = p["long_name"]
            elif "postal_code" in p["types"]:
                lieu.lieu.codepostal = p["long_name"]
            elif "administrative_area_level_2" in p["types"]:
                lieu.lieu.departement = p["long_name"]
            elif "administrative_area_level_1" in p["types"]:
                lieu.lieu.region = p["long_name"]
            elif "country" in p["types"]:
                lieu.lieu.pays = p["short_name"].upper()

    # Gestion de la photo
    photos = donnees.get("photo", None)
    if photos is not None:
        photo = photos[0]
        img = gmaps.place_photo(
            photo_reference=photo["photo_reference"],
            max_width=min(photo["width"], settings.MAPS["PHOTO_MAX_WIDTH"])
        )

        lieu.lieu.photo.save(photo["photo_reference"], ContentFile(img))
        lieu.lieu.save()

    else:
        # Suppression du fichier
        lieu.lieu.photo.delete()

    # Gestion des types
    types = [Type.objects.get_or_create(nom=nom)[0] for nom in donnees["types"]]

    lieu.types.set(types)
    lieu.lieu.types.set([t.api for t in types if t.api is not None])

    lieu.lieu.save()
    lieu.save()

    # Gestion des horaires
    Horaire.objects.filter(lieu=lieu.lieu).delete()

    horaires = donnees.get("opening_hours", None)
    if horaires is not None:
        for p in horaires.get("periods", []):
            h = Horaire()

            h.lieu = lieu.lieu
            h.jour = p["open"]["day"]
            h.open = int(p["open"]["time"], 10)

            close = p.get("close", None)
            if close is not None:
                h.close = int(close["time"], 10)

            h.save()

    return lieu
