"""recipes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import search
from django.contrib import admin
from django.urls import path, include
from .views import *
from gestione import views

urlpatterns = [
    path("lista_ricette/", Lista_ricette_views.as_view(), name="listaricette"),
    path("ricetta/<pk>/", views.DetailRicettaView.as_view(), name="ricetta"),
    path("update_ricetta/<pk>/", views.UpdateRicettaView.as_view(), name="updatericetta"),
    path("cancella_ricetta/<pk>/", views.DeleteRicettaView.as_view(), name="deletericetta"),
    
    path("seach/", search, name="search"),
    path("searchresults/<str:sstring>/<str:where>/", views.SearchResultsList.as_view(), name="searchresults"),

    path("crea_ricetta_avanzato/", views.CreateRicettaAvanzatoView.as_view(), name="crearicettaavanzato")

    
]