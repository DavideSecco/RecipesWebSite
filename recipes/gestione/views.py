from audioop import reverse
from django.shortcuts import render

from gestione.models import Ricetta
from django.urls import reverse_lazy
from django.views.generic import *

# Create your views here.

class Lista_ricette_views(ListView):
    model = Ricetta
    template_name = "lista_ricette.html"

    def get_totale_ricette(self):
        count = 0
        for i in Ricetta.objects.all():
            count = count + 1
        return count 


class CreateRicettaView(CreateView):
    model = Ricetta
    template_name = "gestione/crea_ricetta.html"
    fields = "__all__" # i campi che voglio rendere editabili dall'utente
    success_url = reverse_lazy("listaricette")


class DetailRicettaView(DetailView):
    model = Ricetta
    template_name = "gestione/ricetta.html"


class UpdateRicettaView(UpdateView):
    model = Ricetta
    template_name = "gestione/update_ricetta.html"
    fields = "__all__"
    # success_url = reverse_lazy("listaricette")

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse_lazy("ricetta",kwargs={'pk': pk})


class DeleteRicettaView(DeleteView):
    model = Ricetta
    template_name = "gestione/cancella_ricetta.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["Ricetta"] = "Ricetta"
        return context

    def get_success_url(self):
        return reverse_lazy("listaricette")    