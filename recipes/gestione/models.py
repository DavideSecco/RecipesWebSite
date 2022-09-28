
import datetime
from email.mime import image
from email.policy import default
from random import choices
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

DIFFICOLTA_CHOICES = (("1", "Bassa"), ("2","Media"), ("3","Alta"))

PORTATA_CHOICES = (("1", "Antipasto"), ("2", "Primo"), ("3", "Secondo"), ("4", "Dolce"))

class Ricetta(models.Model):
    nome = models.CharField(max_length=50)
    difficoltá = models.CharField(max_length=50, choices=DIFFICOLTA_CHOICES, default="Bassa")
    portata = models.CharField(max_length=50, choices = PORTATA_CHOICES, default="Primo")
    costo = models.IntegerField(default=0)
    tempo_preparazione = models.IntegerField(default=0)
    tempo_cottura = models.IntegerField(default=0)
    porzioni = models.IntegerField(default=1)
    vegetariano = models.BooleanField(default = False)
    vegano = models.BooleanField(default = False)
    gluten_free = models.BooleanField(default = False)
    immagine = models.ImageField(null=True, blank=True, default=None)
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


UNITA_DI_MISURA_CHOICES = (("1", "grammi"), ("2", "unitá"), ("3", "ml"))

class Ingredient(models.Model):
    nome = models.CharField(max_length=50)
    quantitá = models.IntegerField()
    unita_di_misura = models.CharField(default="grammi", choices=UNITA_DI_MISURA_CHOICES, max_length=50)

    ricetta = models.ForeignKey(Ricetta, on_delete=models.CASCADE, related_name="ingredients")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Ingredienti"



    