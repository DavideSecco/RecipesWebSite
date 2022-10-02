from audioop import reverse
from gc import get_objects
from http.client import HTTPResponse
from multiprocessing import context
from pickle import TRUE
from pyexpat.errors import messages
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


class ListaRicettePreferiteViews(LoginRequiredMixin, ListView):
    model = Ricetta
    template_name = "lista_ricette.html"

    def get_queryset(self):
        ids_ricette_preferite = RicettePreferite.objects.filter(utente = self.request.user).values_list('ricetta')
        Data = Ricetta.objects.filter(id__in = ids_ricette_preferite)
        return Data


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
                        
                if formset.is_valid() :
                    formset.save()
                else: 
                    print("il formset NON é valido: " + formset.errors)

                return redirect('updatericettaavanzato', pk = ricetta.id)
        else: 
            return redirect('ricetta', ricetta_id = ricetta.id)
    
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


# DETAIL RICETTA: 
def ricetta_detail_view(request, ricetta_id):
    ricetta = Ricetta.objects.get(pk=ricetta_id)
    ingredienti = Ingredient.objects.filter(ricetta = ricetta_id).values

    recensioni_della_ricetta = Recensione.objects.filter(ricetta = ricetta)
    numero_recensioni = recensioni_della_ricetta.exclude(punteggio=0).count()
    somma_punteggi = 0
    for recensione in recensioni_della_ricetta:
        if recensione.punteggio != "-":
            somma_punteggi = somma_punteggi + recensione.punteggio
    
    if numero_recensioni != 0: 
        media_recensioni = somma_punteggi / numero_recensioni
    else:
        media_recensioni = 0


    try:
        recensione = Recensione.objects.get(utente = request.user.id, ricetta__id = ricetta_id)
        form = RecensioneForm(request.POST or None, instance=recensione)
    except Recensione.DoesNotExist:
        form = RecensioneForm(request.POST or None, request.FILES  or None)

    if request.method == "POST":
        try:
            recensione = Recensione.objects.get(utente = request.user.id, ricetta__id = ricetta_id)
            if form.is_valid():
                form.save()
                return redirect("ricetta", ricetta_id = ricetta_id)
            else: 
                print("Form non é diventato valido dopo aggiornamento del punteggio")
        except Recensione.DoesNotExist:
            if form.is_valid():
                data = Recensione()
                data.punteggio = form.instance.punteggio
                print("METODO POST: CREAZIONE RECENSIONE: salvo in recensione (instance): " +  str(data.punteggio))
                data.punteggio = form.cleaned_data['punteggio']
                print("METODO POST: CREAZIONE RECENSIONE: salvo in recensione (cleaned_data): " +  str(data.punteggio))
                data.ricetta_id = ricetta_id
                data.utente = request.user
                data.save()
                return redirect("ricetta", ricetta_id = ricetta_id)
            else:
                print("il form non è valido")


    if request.method == 'GET':
        if 'Aggiungi ai preferiti' in request.GET:
            try:
                ricetta_preferita = RicettePreferite.objects.get(utente = request.user, ricetta = ricetta)
                print("Questa ricetta era giá nei preferiti")
            except RicettePreferite.DoesNotExist:
                ricetta_preferita = RicettePreferite(utente = request.user, ricetta = ricetta)
                ricetta_preferita.save()
                print("Dovrei aver salvato la ricetta preferita")
                
            print(RicettePreferite.objects.all().count())
    
    context = {
        'ricetta' : ricetta,
        'ingredienti' : ingredienti,
        "form" : form,
        "media_recensioni" : media_recensioni,
        "numero_recensioni" : numero_recensioni
    }
    return render(request, "gestione/ricetta_details.html", context)



