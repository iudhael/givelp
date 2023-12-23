from django.shortcuts import render, get_object_or_404, redirect

from givelp import settings
from .models import *
import random
from datetime import date
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from givelp.utils import send_info_email

# Create your views here.

global today_date

today_date = date.today()
"""
def index(request):
    context = {


    }

    return render(request, 'catalogue/listing_categorie.html', context)
"""


def main(request):
    categories = Categories.objects.filter(date_de_publication_categorie__lt=today_date).order_by('nom_categorie')
    categorie_objs = list(categories)

    random.shuffle(categorie_objs)
    categorie_objs = categorie_objs[:6]

    # print(categorie_objs)
    navbar = "home"
    partenaires = Partenaire.objects.all()
    context = {
        'categorie_objs': categorie_objs,
        "navbar": navbar,
        'partenaires': partenaires,
    }

    return render(request, 'catalogue/home.html', context)


def aboutpage(request):
    navbar = "about"
    partenaires = Partenaire.objects.all()
    context = {
        'navbar': navbar,
        'partenaires': partenaires,
    }
    return render(request, 'catalogue/about.html', context)



def categoriepage(request):
    categories_list = Categories.objects.filter(date_de_publication_categorie__lt=today_date).order_by('-id')
    paginator = Paginator(categories_list, 6)
    if request.method == 'POST':
        page = request.POST.get('page')
        # print(page)
    else:
        page = request.GET.get('page')
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        # si la page n'est pas un entier delivrer la premier page
        categories = paginator.page(1)
    except EmptyPage:
        # si le num de page est en dehors de la list delivrer les items correpondant à la derniere page
        categories = paginator.page(paginator.num_pages)

    # print(categories)
    navbar = "ouroffer"
    partenaires = Partenaire.objects.all()
    context = {
        'categories': categories,
        'paginate': True,
        "navbar": navbar,
        'partenaires': partenaires,
    }
    return render(request, 'catalogue/listing_categorie.html', context)


def detail_categorie(request, detail_categorie_id):
    global categorie_name

    # print(detail_categorie_id)
    categorie_name = get_object_or_404(Categories, pk=detail_categorie_id)

    # print(categorie_name)

    # print(today_date)
    modele_categories_list = Modeles.objects.filter(categorie=categorie_name,
                                                    date_de_publication__lt=today_date).order_by('-id')
    paginator = Paginator(modele_categories_list, 4)

    if request.method == 'POST':
        page = request.POST.get('page')
        # print(page)
    else:
        page = request.GET.get('page')
    try:
        modele_categories = paginator.page(page)
    except PageNotAnInteger:
        # si la page n'est pas un entier delivrer la premier page
        modele_categories = paginator.page(1)
    except EmptyPage:
        # si le num de page est en dehors de la list delivrer les items correpondant à la derniere page
        modele_categories = paginator.page(paginator.num_pages)
    # print(modele_categories)
    navbar = "ouroffer"
    partenaires = Partenaire.objects.all()
    context = {
        'modele_categories': modele_categories,
        'categorie_name': categorie_name,
        'paginate': True,
        "navbar": navbar,
        'partenaires': partenaires,

    }
    return render(request, 'catalogue/listing_modele.html', context)


def detail_modele(request, detail_modele_id):



    modele_name = get_object_or_404(Modeles, pk=detail_modele_id)

    # print(modele_name)
    details_modeles = Modeles.objects.filter(pk=modele_name.pk, date_de_publication__lt=today_date).order_by('-id')
    print(details_modeles)


    

    if request.method == 'POST':
        if request.user.is_authenticated:
            #demander le nom et le passe
            type_stage = request.POST.get('radio')
            servive_stage = request.POST.get('select')


            #print(type_stage)
            #print(servive_stage)
            nom = request.user.first_name
            prenom = request.user.last_name
            username = request.user.username
            email_user = request.user.email


            chemin_cv = settings.MEDIA_ROOT + "/" + str(request.user.userinfo.cv)
            chemin_motiv_lettre = settings.MEDIA_ROOT + "/" + str(request.user.userinfo.lettre_motivation)


            email_entreprise = "adikpetoiudhael@gmail.com" #details_modeles('email_entreprise')


            value = send_info_email(request, nom, prenom, username, email_user,type_stage, servive_stage, chemin_cv, chemin_motiv_lettre, email_entreprise)

            #ajouter la demande à la table MailSend
            
            if value:
                MailSend.objects.create(user=request.user, entreprise=modele_name)     
        else:
            return redirect('authentification:login')




    # print(modeles)
    navbar = "ouroffer"
    partenaires = Partenaire.objects.all()
    context = {
        'details_modeles': details_modeles,
        'modele_name': modele_name,
        "navbar": navbar,
        'partenaires': partenaires,
    }
    return render(request, 'catalogue/detail_modele.html', context)



def search_categorie(request):
    query = request.GET.get('query')  # avec GET tous ce qui est taper dans l'url comme recherche est capturer
    query = query.lower()
    if not query:
        categories = Categories.objects.filter(date_de_publication_categorie__lt=today_date).order_by('nom_categorie')
        # print(categories)
    else:
        # title__icontains contient la requette qui est le titre mais pas exactement le titre de l'album si le titre est mal taper ou imcomplet
        categories = Categories.objects.filter(date_de_publication_categorie__lt=today_date,
                                               nom_categorie__icontains=query).order_by('nom_categorie')
        # print(categories)

        if not categories.exists():
            categories = Categories.objects.filter(date_de_publication_categorie__lt=today_date,
                                                   nom_categorie__icontains=query).order_by(
                'nom_categorie')  # chercher dans la table  les noms qui correspondent aux requette et renvoyer des album
            # print(categories)

    title = "Résultats pour la requête %s" % query
    partenaires = Partenaire.objects.all()
    context = {
        'categories': categories,
        'title': title,
        'partenaires': partenaires,
    }

    return render(request, 'catalogue/search_categorie.html', context)


def search_modele(request):
    # categorie_id = get_object_or_404(Categories, pk=detail_categorie_id)

    query = request.GET.get('query')  # avec GET tous ce qui est taper dans l'url comme recherche est capturer

    query = query.lower()
    if not query:
        modele_categories = Modeles.objects.filter(categorie=categorie_name,
                                                   date_de_publication__lt=today_date).order_by('nom_modele')
        # print(modele_categories)
    else:
        # title__icontains contient la requette qui est le titre mais pas exactement le titre de l'album si le titre est mal taper ou imcomplet
        modele_categories = Modeles.objects.filter(categorie=categorie_name, date_de_publication__lt=today_date,
                                                   nom_modele__icontains=query).order_by('nom_modele')
        # print(modele_categories)

        if not modele_categories.exists():
            modele_categories = Modeles.objects.filter(categorie=categorie_name, date_de_publication__lt=today_date,
                                                       nom_modele__icontains=query).order_by(
                'nom_modele')  # chercher dans la table  les noms qui correspondent aux requette et renvoyer des album
            # print(modele_categories)

    title = "Résultats pour la requête %s" % query
    partenaires = Partenaire.objects.all()
    context = {
        'modele_categories': modele_categories,
        'title': title,
        'partenaires': partenaires,
    }

    return render(request, 'catalogue/search_modele.html', context)