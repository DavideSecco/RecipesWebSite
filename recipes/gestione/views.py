from audioop import reverse
from urllib import request
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User

from gestione.models import Ricetta
from django.urls import reverse_lazy
from django.views.generic import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

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
        print("request = " + self.request.user.username)
        print("prova")
        print(self.request.user)
        Data = Ricetta.objects.filter(utente = self.request.user)
        return Data

    
class CreateRicettaAvanzatoView(LoginRequiredMixin, CreateView):
    model = Ricetta
    template_name = "gestione/crea_ricetta_avanzato.html"
    form_class = CreateRicettaForm
    success_url = reverse_lazy("listaricette") 

    def form_valid(self, form):
        form.instance.utente = self.request.user
        return super().form_valid(form)


class UpdateRicettaAvanzatoView(UpdateView):
    template_name = "gestione/update_ricetta_avanzato.html"
    form_class = CreateRicettaForm
    model = Ricetta
    # success_url = reverse_lazy("listaricette")

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse_lazy("ricetta",kwargs={'pk': pk})

class DetailRicettaView(DetailView):
    model = Ricetta
    template_name = "gestione/ricetta_details.html"


class DeleteRicettaView(DeleteView):
    model = Ricetta
    template_name = "gestione/cancella_ricetta.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["Ricetta"] = "Ricetta"
        return context

    def get_success_url(self):
        return reverse_lazy("listaricette")    


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

