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

                if formset.is_valid():
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
def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            sstring = form.cleaned_data.get("search_string")
            where = form.cleaned_data.get("search_where")
            return redirect("searchresults", sstring, where)
    else:
        form = SearchForm()
    
    return render(request,template_name="gestione/search_page.html",context={"form":form})


class SearchResultsList(ListView):
    model = Ricetta
    template_name = "gestione/search_results.html"

    def get_queryset(self):
        sstring = self.request.resolver_match.kwargs["sstring"]
        where = self.request.resolver_match.kwargs["where"]

        if "Ricette" in where:
            qq = Ricetta.objects.filter(nome__icontains=sstring)

        return qq


