from dataclasses import field
from django import forms

from gestione.models import Ricetta, Ingredient
from django.forms import formset_factory


class SearchForm(forms.Form):
    CHOICE_LIST = [("Ricette", "Seach in Ricette")]

    search_string = forms.CharField(label="Search String", max_length=100, required=True) #min_lenght=3,
    search_where = forms.ChoiceField(label="Search Where?", required=True, choices=CHOICE_LIST)


"""
(per tutti i punti si fa riferimenti al problema perché nell'esempio del prof i modelli sono 2)
- Entrambi i form ereditano da forms.ModelForm
- Entrambi i form hanno una variabile chiamata description. Non è necessaria.
- Entrambi i form hanno specificato gli attributi model e fields nella loro Meta classe interna. Similmente a quanto accadeva nelle CreateViews
- In entrambi i form abbiamo fatto override del metodo clean: questo ci consente di implementare validazione aggiuntiva sugli input dell’utente.
- La validazione standard è già stata eseguita prima del metodo clean. In particolare i dati pre-validati sono disponibili in self.cleaned_data. Il quale è un dizionario le cui chiavi corrispondono agli attributi (stringa) del model
specificato.
- Gli errori che aggiungiamo in clean, se scatenati, compariranno nel render del browser e impediranno la sottomissione dei dati POST.
    ○ self.add_error(“campo interessato”,”stringa associata all’errore”)
"""

class CreateRicettaForm(forms.ModelForm):
    
    description_create = "Create a new Ricetta!"
    description_update = "Update a Ricetta!"

    #def clean(self):
        #if (len(self.cleaned_data["nome"]) < 3):
        #    self.add_error("nome","Error: ricetta text must be at least 5 characters long")
    
        #return self.cleaned_data

    class Meta:
        model = Ricetta
        exclude = ["utente",]


class IngredientForm(forms.ModelForm):
        
    class Meta:
        model = Ingredient
        exclude = ('ricetta',)

"""
IngredientFormSet = forms.inlineformset_factory(Ricetta, Ingredient, form=IngredientForm)
# IngredientFormSet = formset_factory(Ingredient, formset=IngredientForm)
data = {
    'form-TOTAL_FORMS': '1501',
    'form-INITIAL_FORMS': '2',
    'form-MIN_NUM_FORMS': '2'
}
formset = IngredientFormSet(data) 
formset.is_valid()
"""