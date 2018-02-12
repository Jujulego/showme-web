# Importations
from django.db import models


# Models
class Type(models.Model):
    # Attributs
    nom = models.CharField(max_length=100)
    pluriel = models.CharField(max_length=100)
    blacklist = models.BooleanField(default=False, null=False, blank=True)