from django.shortcuts import render
from django.views.generic import *
from gestione.models import Ricetta

# Create your views here.

class Home_page_views(TemplateView):
    template_name = "home.html"


# Da qui in poi forse la sposterai

