from django.contrib import admin
from .models import Ricetta, Ingredient

# Register your models here.

admin.site.register(Ricetta)
admin.site.register(Ingredient)
