from django.urls import re_path, path # importer les urls du projet

from . import views

app_name = 'catalogue' # important pour le namespace



urlpatterns = [

    path('', views.main, name="home"),

    path('search-modele/', views.search_modele, name="search-modele"),
    path('search-categorie/', views.search_categorie, name="search-categorie"),
    path('categorie/modele/<detail_modele_id>/', views.detail_modele, name="detail_modele"),


    path('categorie/<detail_categorie_id>/', views.detail_categorie, name="detail_categorie"),    #pb d'url

    path('about/', views.aboutpage, name="about"),
    path('categorie/', views.categoriepage, name="home-catalogue"),


]