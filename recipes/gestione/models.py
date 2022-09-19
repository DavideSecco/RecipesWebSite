from django.db import models

# Create your models here.

class Ricetta(models.Model):
    nome = models.CharField(max_length=50)
    tempo = models.TimeField
    difficoltá = models.CharField(max_length=50)

    def __str__(self):
        out = self.nome