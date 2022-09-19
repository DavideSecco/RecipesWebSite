from django.db import models

# Create your models here.

class Ricetta(models.Model):
    nome = models.CharField(max_length=50)
    difficoltá = models.CharField(max_length=50)
    regime_alimentare = models.CharField(max_length=50, default="veg")
    portata = models.CharField(max_length=50, default="primo")
    costo = models.IntegerField(default=50)
    #tempo_preparazione = models.TimeField
    #tempo_cottura = models.TimeField(default="10", max_length=50)
    #porzioni = models.IntegerField(default=50)

    def __str__(self):
        out = self.nome

    class Meta:
        verbose_name_plural = "Ricette"