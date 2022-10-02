from django.contrib import admin
from .models import Recensione, Ricetta, Ingredient, RicettePreferite

# Register your models here.

admin.site.register(Ricetta)
admin.site.register(Ingredient)
admin.site.register(Recensione)
admin.site.register(RicettePreferite)
