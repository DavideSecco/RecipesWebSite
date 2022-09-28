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
    # LISTA RICETTE
    path("lista_ricette/", Lista_ricette_views.as_view(), name="listaricette"),
    path("lista_ricette_private/", views.ListaRicettePrivateViews.as_view(), name="listaricetteprivate"),

    # DETAIL RICETTA
    path("ricetta/<pk>/", views.ricetta_detail_view, name="ricetta"),
    
    # CREATE & UPDATE
    path("crea_ricetta_avanzato/", views.ricetta_create_view, name="crearicettaavanzato"),
    path("update_ricetta_avanzato/<pk>/", views.ricetta_update_view, name="updatericettaavanzato"),

    # DELETE
    path("cancella_ricetta/<pk>/", views.DeleteRicettaView.as_view(), name="deletericetta"),
    
    # RICERCA E RISULTATI RICERCA
    path("seach/", search, name="search"),
    path("searchresults/<str:sstring>/<str:where>/", views.SearchResultsList.as_view(), name="searchresults"),
]