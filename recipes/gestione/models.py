import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

REGIME_ALIMENTARE_CHOICES = (("1", "Vegetariano"), ("2","Vegano"), ("3","Nessuno"))

DIFFICOLTA_CHOICES = (("1", "Bassa"), ("2","Media"), ("3","Alta"))

PORTATA_CHOICES = (("1", "Antipasto"), ("2", "Primo"), ("3", "Secondo"), ("4", "Dolce"))

class Ricetta(models.Model):
    nome = models.CharField(max_length=50)
    difficoltá = models.CharField(max_length=50)
    regime_alimentare = models.CharField(max_length=50, choices = REGIME_ALIMENTARE_CHOICES, default="veg")
    portata = models.CharField(max_length=50, choices = PORTATA_CHOICES, default="primo")
    costo = models.IntegerField(default=50)
    tempo_preparazione = models.IntegerField(default=20)
    tempo_cottura = models.IntegerField(default=10)
    porzioni = models.IntegerField(default=2)
    utente = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True, default=None, related_name = "non_so_cosa_vada")

    def __str__(self):
        out = self.nome
        return out

    def chi_proprietario(self):
        if self.utente == None:
            return None
        else:
            return self.utente.username
            
    class Meta:
        verbose_name_plural = "Ricette"


class Ingrediente(models.Model):
    nome = models.CharField(max_length=50)
    calorie = models.IntegerField()
    unità_di_misura = models.CharField(default="grammi")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Ingredienti"


class Ricetta_Ingrediente(models.Model):
    ingrediente = models.ForeignKey(Ingrediente, on_delete = models.CASCADE, blank=True, null=True, default=None, related_name = "non_so_cosa_vada")
    ricetta = models.ForeignKey(Ricetta, on_delete = models.CASCADE, blank=True, null=True, default=None, related_name = "non_so_cosa_vada")
    quantità = models.IntegerField()

    

    