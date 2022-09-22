from django.shortcuts import render
from django.views.generic import *
from gestione.models import Ricetta
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

# Create your views here.

class Home_page_views(TemplateView):
    template_name = "home.html"

class UserCreateView(CreateView):
    form_class= UserCreationForm
    template_name= "user_create.html"
    success_url= reverse_lazy("login")