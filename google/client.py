# Importations
from random import choice, random

from django.conf import settings
from django.contrib.gis.geos import Point
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


def remplir_db(gmaps):
    # Requêtes
    resultat = gmaps.places_nearby(location=random_point(), radius=settings.MAPS["SEARCH_RADIUS"])
    lieux = resultat.get("results", [])
    suite = resultat.get("next_page_token", None)

    while suite is not None:
        resultat = gmaps.places_nearby(location=random_point(), radius=settings.MAPS["SEARCH_RADIUS"])
        lieux.extend(resultat.get("results", []))
        suite = resultat.get("next_page_token", None)

    # Ajout des lieux
    log = Log()
    log.type = Log.RECHERCHE
    log.save()

    for donnees in lieux:
        try:
            lieu = Lieu.objects.get(google_id=donnees["place_id"])

        except Lieu.DoesNotExist:
            lieu = Lieu()
            lieu.google_id = donnees["place_id"]
            lieu.lieu = ApiLieu()

        _maj(gmaps, lieu, donnees)

        lieu.logs.add(log)


@transaction.atomic
def maj_lieu(gmaps, lieu):
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
    api_lieu = lieu.lieu;
    api_lieu.position = Point(donnees["geometry"]["location"]["lng"], donnees["geometry"]["location"]["lat"])
    api_lieu.nom = donnees["name"]

    api_lieu.telephone = donnees.get("international_phone_number", "")
    api_lieu.note = donnees.get("rating", None)
    api_lieu.site = donnees.get("website", None)
    api_lieu.prix = donnees.get("price_level", None)

    adresse = donnees.get("address_components", None)
    if adresse is not None:
        for p in adresse:
            if "street_number" in p["types"]:
                api_lieu.numero = p["long_name"]
            elif "route" in p["types"]:
                api_lieu.route = p["long_name"]
            elif "locality" in p["types"]:
                api_lieu.ville = p["long_name"]
            elif "postal_code" in p["types"]:
                api_lieu.codepostal = p["long_name"]
            elif "administrative_area_level_2" in p["types"]:
                api_lieu.departement = p["long_name"]
            elif "administrative_area_level_1" in p["types"]:
                api_lieu.region = p["long_name"]
            elif "country" in p["types"]:
                api_lieu.pays = p["short_name"].upper()

    # Gestion de la photo
    photos = donnees.get("photo", None)
    if photos is not None:
        photo = photos[0]
        img = gmaps.place_photo(
            photo_reference=photo["photo_reference"],
            max_width=min(photo["width"], settings.MAPS["PHOTO_MAX_WIDTH"])
        )

        api_lieu.photo.save(photo["photo_reference"], ContentFile(img))
        api_lieu.save()

    else:
        # Suppression du fichier
        api_lieu.photo.delete()

    # Sauvegarde
    api_lieu.save()

    lieu.lieu = api_lieu
    lieu.save()

    # Gestion des types
    types = [Type.objects.get_or_create(nom=nom)[0] for nom in donnees["types"]]

    lieu.types.set(types)
    lieu.lieu.types.set([t.api for t in types if t.api is not None])

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
