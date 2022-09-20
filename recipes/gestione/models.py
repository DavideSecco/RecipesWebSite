import datetime
from django.db import models

# Create your models here.

class Ricetta(models.Model):
    nome = models.CharField(max_length=50)
    difficoltá = models.CharField(max_length=50)
    regime_alimentare = models.CharField(max_length=50, default="veg")
    portata = models.CharField(max_length=50, default="primo")
    costo = models.IntegerField(default=50)
    tempo_preparazione = models.CharField(default="20", max_length=5)
    tempo_cottura = models.CharField(default="10", max_length=4)
    porzioni = models.IntegerField(default=50)

    def __str__(self):
        out = self.nome
        return out

    class Meta:
        verbose_name_plural = "Ricette"

    