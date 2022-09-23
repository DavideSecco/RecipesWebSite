from django.contrib import admin
from .models import Ricetta, Ingredient

class IngredientInline(admin.TabularInline):
    model = Ingredient

@admin.register(Ricetta)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, ]

# Register your models here.
