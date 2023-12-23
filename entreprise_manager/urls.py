from django.urls import path # importer les urls du projet

from . import views

app_name = 'entreprise_manager' # important pour le namespace



urlpatterns = [

    path('demande/', views.entreprise_manager, name="demande-stage"),
   
]