from dataclasses import field
from email.policy import default
from django import forms

from gestione.models import Ricetta, Ingredient
from django.forms import formset_factory
from django.forms import BaseInlineFormSet
from django.forms import BaseFormSet


class SearchForm(forms.Form):
    nome = forms.CharField(label="Nome ricetta", max_length=100, required=False) #min_lenght=3,
    t_prep = forms.IntegerField(label="Tempo di preparazione massimo", required=False)
    is_vegetarian = forms.BooleanField(label = "Vegetariano", required=False)


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
