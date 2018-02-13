# Importations
from django.contrib.gis.db import models

from . import pays


# Modèles
class Type(models.Model):
    # Champs
    nom = models.CharField(max_length=100)
    pluriel = models.CharField(max_length=100)
    blacklist = models.BooleanField(default=False, null=False, blank=True)


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
    prix = models.SmallIntegerField(default=None, blank=True, null=True, choices=PRIX)
    photo = models.ImageField(upload_to="photos/", max_length=500, null=True, blank=True)

    # Adresse
    numero = models.CharField(max_length=100, default="", blank=True)
    route = models.CharField(max_length=150, default="", blank=True)
    ville = models.CharField(max_length=100, default="", blank=True)
    departement = models.CharField(max_length=50, default="", blank=True)
    region = models.CharField(max_length=50, default="", blank=True)
    pays = models.CharField(max_length=3, choices=pays.PAYS, default="IC", blank=True)
    codepostal = models.CharField(max_length=15, default="", blank=True)

    # Liens aux types
    types = models.ManyToManyField(Type, blank=True)

    # Méta
    class Meta:
        verbose_name_plural = "lieux"

    # Méthodes spéciales
    def __str__(self):
        if self.nom == "Inconnu":
            return "<Lieu: lat={:.6f}, lng={:.6f}>".format(self.latitude, self.longitude)

        return "<Lieu: {:s}>".format(self.nom)

    # Méthodes
    def a_photo(self):
        return self.photo.name != ""

    a_photo.short_description = "photo"
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

    # Lien au lieu
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE)
