# Importations
from datetime import datetime, timedelta, time

from django.db import models

# Modèles
class Type(models.Model):
    # Attributs
    name = models.CharField(max_length=100, editable=False)
    api = models.ForeignKey('api.Type', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')


class Lieu(models.Model):
    # Attributs
    google_id = models.CharField(max_length=255, editable=False, unique=True, db_index=True)
    lieu = models.ForeignKey('api.Lieu', on_delete=models.CASCADE, related_name='+', db_index=True)

    maj = models.BooleanField(default=False, blank=True)
    der_maj = models.DateField(auto_now_add=True, blank=True, editable=False)

    # Méta
    class Meta:
        verbose_name_plural = "lieux"

    # Propriétés
    def a_jour(self):
        return (not self.maj) and (datetime.now() - timedelta(days=30) < datetime.combine(self.der_maj, time()))

    a_jour.boolean = True
