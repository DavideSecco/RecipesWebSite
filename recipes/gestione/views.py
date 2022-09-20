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