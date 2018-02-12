# Importations
from django.contrib.gis.db import models


# Modèles
class Lieu(models.Model):
    # Attributs
    PRIX = (
        (None, "----------"),
        (0, "Gratuit"),
        (1, "Bon marché"),
        (2, "Modéré"),
        (3, "Cher"),
        (4, "Très cher"),
    )

    # Champs obligatoires
    position = models.PointField(spatial_index=True)
    nom = models.CharField(max_length=255, db_index=True, default="Inconnu", blank=True)

    # Champs additionnels
    telephone = models.CharField(max_length=20, default="", blank=True, verbose_name="téléphone")
    note = models.FloatField(null=True, blank=True)
    site = models.URLField(max_length=500, null=True, blank=True)
    prix = models.SmallIntegerField(default=None, blank=True, choices=PRIX)
    photo = models.ImageField(upload_to="photos/", max_length=500, null=True, blank=True)

    # Méta
    class Meta:
        verbose_name_plural = "lieux"

    # Méthodes
    def a_photo(self):
        return self.photo.name

    a_photo.short_description = "photo"
    a_photo.admin_order_field = "photo"
    a_photo.boolean = True

    # Propriétés
    # - latitude
    @property
    def latitude(self):
        return self.position.y

    @latitude.setter
    def latitude(self, lat):
        self.position.y = lat

    # - longitude
    @property
    def longitude(self):
        return self.position.x

    @longitude.setter
    def longitude(self, lng):
        self.position.x = lng


class Type(models.Model):
    # Champs
    nom = models.CharField(max_length=100)
    pluriel = models.CharField(max_length=100)
    blacklist = models.BooleanField(default=False, null=False, blank=True)


class Horaire(models.Model):
    # Attributs
    JOURS = (
        (0, "dimanche"),
        (1, "lundi"),
        (2, "mardi"),
        (3, "mercredi"),
        (4, "jeudi"),
        (5, "vendredi"),
        (6, "samedi"),
    )

    # Champs
    jour = models.SmallIntegerField(choices=JOURS)
    open = models.SmallIntegerField(verbose_name="ouverture")
    close = models.SmallIntegerField(verbose_name="fermeture", default=0)
