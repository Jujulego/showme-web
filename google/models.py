# Importations
from datetime import datetime, timedelta, time

from django.db import models


# Modèles
class Type(models.Model):
    # Champs
    nom = models.CharField(max_length=100, editable=False)
    api = models.ForeignKey('api.Type', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    # Méthodes spéciales
    def __str__(self):
        return self.nom


class Log(models.Model):
    # Attributs
    RECHERCHE = 1
    MISE_A_JOUR = 2

    TYPES = (
        (RECHERCHE, "Recherche"),
        (MISE_A_JOUR, "Mise à jour"),
    )

    # Champs
    date = models.DateTimeField(auto_now_add=True, editable=False)
    type = models.SmallIntegerField(null=False, editable=False, choices=TYPES)


class Lieu(models.Model):
    # Champs
    google_id = models.CharField(max_length=255, editable=False, unique=True, db_index=True)
    lieu = models.ForeignKey('api.Lieu', on_delete=models.CASCADE, related_name='+', db_index=True)
    types = models.ManyToManyField(Type, blank=True)

    maj = models.BooleanField(default=False, blank=True)
    der_maj = models.DateField(auto_now_add=True, blank=True, editable=False)
    logs = models.ManyToManyField(Log, editable=False)

    # Méta
    class Meta:
        verbose_name_plural = "lieux"

    # Méthodes spéciales
    def __str__(self):
        return self.google_id

    # Propriétés
    def a_jour(self):
        # noinspection PyTypeChecker
        return (not self.maj) and (datetime.now() - timedelta(days=30) < datetime.combine(self.der_maj, time()))

    a_jour.boolean = True
