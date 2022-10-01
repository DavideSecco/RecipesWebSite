from audioop import reverse
from gc import get_objects
from http.client import HTTPResponse
from multiprocessing import context
from pickle import TRUE
# from typing_extensions import Required
from urllib import request
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User

from django.urls import reverse_lazy
from django.views.generic import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory, inlineformset_factory
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound


# Create your views here.

# Lista ricetta pubbliche e private:
class Lista_ricette_views(ListView):
    model = Ricetta
    template_name = "lista_ricette.html"

    def get_totale_ricette(self):
        count = 0
        for i in Ricetta.objects.all():
            count = count + 1
        return count 

class ListaRicettePrivateViews(LoginRequiredMixin, ListView):
    model = Ricetta
    template_name = "lista_ricette.html"

    def get_queryset(self):
        Data = Ricetta.objects.filter(utente = self.request.user)
        return Data


# DETAIL RICETTA: 
def ricetta_detail_view(request, pk):
    ricetta = Ricetta.objects.get(pk=pk)
    ingredienti = Ingredient.objects.filter(ricetta = pk).values
    context = {
        'ricetta' : ricetta,
        'ingredienti' : ingredienti
    }
    return render(request, "gestione/ricetta_details.html", context)

# CREATE & UPDATE: https://www.youtube.com/watch?v=PICYTJqj__o&t=16s
# Per aggiungere ingredienti dinamicamente a una ricetta: https://www.youtube.com/watch?v=JIvJL1HizP4
@login_required
def ricetta_create_view(request):
    form = RicettaForm(request.POST or None, request.FILES or None)
    IngredientFormSet = inlineformset_factory(Ricetta, Ingredient, fields=("nome", "quantitá", "unita_di_misura"), extra=1)

    if request.method == "POST":
        if 'save' in request.POST:
            if form.is_valid():
                obj = form.save(commit = False)
                obj.utente = request.user
                obj.save()
                formset = IngredientFormSet(request.POST or None, instance=form.instance)
                if formset.is_valid():
                    formset.save()
                
            print("Ho eseguito il metodo post")
            # return redirect('listaricette')
            return redirect('updatericettaavanzato', pk = obj.id)
        else:
            return redirect('listaricette')
    
    
    if request.method == "GET":
        formset = IngredientFormSet()
        context = {
            "form": form,
            'formset': formset
        }
        print("Ho eseguito il metodo get")
        return render(request, "gestione/create_update_ricetta_avanzato.html", context)

@login_required
def ricetta_update_view(request, pk=None):
    try:
        ricetta = Ricetta.objects.get(id=pk, utente = request.user)
    except Ricetta.DoesNotExist:
        return render(request, "gestione/pagina_di_errore.html")

    form = RicettaForm(request.POST or None, request.FILES  or None, instance=ricetta)
    IngredientFormSet = inlineformset_factory(Ricetta, Ingredient, fields=("nome", "quantitá", "unita_di_misura" ), 
                        extra=1, can_delete=True, can_delete_extra=True, validate_max=0)
    
    if request.method == "POST":
        # Premo su pulsante save
        if 'save' in request.POST:
            if form.is_valid:
                form.save()
                formset = IngredientFormSet(request.POST or None, instance=ricetta)

                # https://stackoverflow.com/questions/66877831/django-inline-formset-field-required-not-required-setting-in-view
                # modify all the fields
                for form in formset:
                    for field in form.fields.values():
                        field.required = False
                        
                
                """
                Siccome dal ciclo sopra abbiamo redo tutti i campi non obbligatori il parametro extra=1 ogni volta
                aggiunge un form anche se quelli precendenti sono vuoti.
                Per questo dopo aver controllato che il formset sia valido, controllo che tutti i forms siano stati
                compilati senza quindi far si che ogni volta che si salva venga creato un form nuovo in piú
                """
                # la funzione é scritta molto male, ma non so come fare in modo pythonico
                # https://stackoverflow.com/questions/31849379/deleting-form-from-django-formset --> non c'é modo di eliminare un form da formset
                #b = True
                if formset.is_valid() :
                    # print("Il formset é valido")
                    # if formset.has_changed():
                    #     formset.save()
                    # for form in formset:
                    #     if form.cleaned_data['nome'] == None and form.cleaned_data['quantitá'] == None:
                    #         #form.delete()
                    #         b = False
                    # if b == True:
                        formset.save()
                else: 
                    print("il formset NON é valido: " + formset.errors)

                return redirect('updatericettaavanzato', pk = ricetta.id)
        else: 
            return redirect('ricetta', pk = ricetta.id)
    
    if request.method == "GET":
        formset = IngredientFormSet(instance=ricetta)
        context = {
            "form": form,
            "object": ricetta,
            'formset': formset
        }
        print("Ho eseguito il metodo get")
        return render(request, "gestione/create_update_ricetta_avanzato.html", context)
    
def ricetta_delete_view(request, pk):
    try:
        obj = Ricetta.objects.get(id=pk, utente = request.user)
    except Ricetta.DoesNotExist:
        return render(request, "gestione/pagina_di_errore.html")
    
    if request.method == "POST":
        obj.delete()
        return redirect ("listaricette")

    context = {
        "object" : obj
    }
    return render (request, "gestione/cancella_ricetta.html", context=context)


# RICERCA E RISULTATI RICERCA
# https://www.youtube.com/watch?v=G-Rct7Na0UQ
# https://www.youtube.com/watch?v=vU0VeFN-abU
def search_advanced(request):
    form = SearchForm()   
    qs = Ricetta.objects.all()

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            nome_query           = form.cleaned_data.get("nome" or None)
            difficolta_query     = form.cleaned_data.get("difficolta" or None)
            portata_query        = form.cleaned_data.get("portata")
            costo_max_query      = form.cleaned_data.get("costo_max")
            t_prep_query         = form.cleaned_data.get("t_prep")
            is_vegetarian_query  = form.cleaned_data.get("is_vegetarian")
            is_vegan_query       = form.cleaned_data.get("is_vegan")
            is_gluten_free_query = form.cleaned_data.get("is_gluten_free")

            # Nome
            if nome_query != '' and nome_query is not None:
                qs = qs.filter(nome__icontains = nome_query)

            # difficoltá
            if difficolta_query != "0" and difficolta_query is not None:
                qs = qs.filter(difficoltá__icontains = difficolta_query)

            # portata
            if portata_query != "0" and portata_query is not None:
                qs = qs.filter(portata__icontains = portata_query)

            # Costo max
            if costo_max_query != '' and costo_max_query is not None:
                qs = qs.filter(costo__lt = costo_max_query)

            # Tempo preparazione
            if t_prep_query != '' and t_prep_query is not None:
                qs = qs.filter(tempo_preparazione__lt = t_prep_query)

            # Vegetariano
            if is_vegetarian_query == True:
                qs = qs.filter(vegetariano = is_vegetarian_query)
            
            # Vegano
            if is_vegan_query == True:
                qs = qs.filter(vegano = is_vegan_query)
    
            # Gluten free
            if is_gluten_free_query == True:
                qs = qs.filter(gluten_free = is_gluten_free_query)

    context = {
        "form" : form,
        "object_list" : qs
    }

    return render (request, "gestione/search_advanced.html", context=context)
