from django.shortcuts import render
from django.views.generic import *

# Create your views here.

class home_page_views(TemplateView):
    template_name = "home.html"