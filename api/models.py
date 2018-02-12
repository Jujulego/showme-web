# Importations
from django.db import models


# Modèles
class Type(models.Model):
    # Attributs
    nom = models.CharField(max_length=100)
    pluriel = models.CharField(max_length=100)
    blacklist = models.BooleanField(default=False, null=False, blank=True)


class Horaire(models.Model):
    #  Jours
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
