from audioop import reverse
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
    ricetta = Ricetta.objects.get(pk=pk)
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
    
# DELETE ricetta: sempre vanno aggiunti gli ingredienti
class DeleteRicettaView(DeleteView):
    model = Ricetta
    template_name = "gestione/cancella_ricetta.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["Ricetta"] = "Ricetta"
        return context

    def get_success_url(self):
        return reverse_lazy("listaricette")    


# RICERCA E RISULTATI RICERCA
# https://www.youtube.com/watch?v=G-Rct7Na0UQ
def search(request):
    initial = {
            'sstring': r'^$',
            "meno_tempo_di_preparazione" : "100",
            "is_vegetarian": False
    }
    form = SearchForm(initial=initial)

    if request.method == "POST":
        form = SearchForm(request.POST, initial=initial)
        if form.is_valid():
            sstring = form.cleaned_data.get("search_string" or None)
            print("quasta é la stringa:" + sstring)
            is_vegetarian = form.cleaned_data.get("is_vegetarian")
            meno_tempo_di_preparazione = form.cleaned_data.get("meno_tempo_di_preparazione")
            # return redirect("searchresults", sstring, is_vegetarian, meno_tempo_di_preparazione) 
            return redirect()
    
    context = {
        "form": form
    }
    return render(request,template_name="gestione/search_page.html",context=context)


class SearchResultsList(ListView):
    model = Ricetta
    template_name = "lista_ricette.html"

    def get_queryset(self):
        sstring = self.request.resolver_match.kwargs["sstring"]
        
        is_vegetarian = self.request.resolver_match.kwargs['is_vegetarian']
        meno_tempo_di_preparazione = self.request.resolver_match.kwargs["meno_tempo_di_preparazione"]

        if sstring == '':
            qs = Ricetta.objects.filter(vegetariano=is_vegetarian, 
                                        tempo_preparazione__lt = meno_tempo_di_preparazione)  
        else: 
            qs = Ricetta.objects.filter(nome__icontains=sstring, 
                                        vegetariano=is_vegetarian, 
                                        tempo_preparazione__lt = meno_tempo_di_preparazione)  
        return qs
