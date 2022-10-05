from dataclasses import field
from email.policy import default
from django import forms

from gestione.models import *
from django.forms import formset_factory
from django.forms import BaseInlineFormSet
from django.forms import BaseFormSet

DIFFICOLTA_CHOICES = (("0", ""), ("Bassa", "Bassa"), ("Media","Media"), ("Alta","Alta"))
# DIFFICOLTA_CHOICES = (("0", ""), ("1", "Bassa"), ("2","Media"), ("3","Alta"))

PORTATA_CHOICES = (("0", ""), ("1", "Antipasto"), ("2", "Primo"), ("3", "Secondo"), ("4", "Dolce"))

class SearchForm(forms.Form):
    nome = forms.CharField(label="Nome ricetta", max_length=100, required=False) #min_lenght=3,
    difficolta = forms.ChoiceField(label = "Difficolta", choices=DIFFICOLTA_CHOICES, required = False)
    portata = forms.ChoiceField(label="Pasto", choices=PORTATA_CHOICES, required=False)
    costo_max = forms.IntegerField(label="Costo Massimo", required=False)
    t_prep = forms.IntegerField(label="Tempo di preparazione massimo", required=False)
    is_vegetarian = forms.BooleanField(label = "Vegetariano", required=False)
    is_vegan = forms.BooleanField(label = "Vegano", required=False)
    is_gluten_free = forms.BooleanField(label = "Gluten free", required=False)

class RicettaForm(forms.ModelForm):  
    description_create = "Create a new Ricetta!"
    description_update = "Update a Ricetta!"

    class Meta:
        model = Ricetta
        exclude = ["utente",]


class IngredientForm(forms.ModelForm): 
    class Meta:
        model = Ingredient
        exclude = ('ricetta',)

PUNTEGGIO_CHOICES = ((0, "-"), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5))

class RecensioneForm(forms.ModelForm):
    punteggio = forms.ChoiceField(required=False, choices=PUNTEGGIO_CHOICES)

    class Meta:
        model = Recensione
        exclude = ("utente", 'ricetta')