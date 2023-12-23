
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import  force_str #force_text
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from catalogue.models import Categories


from catalogue.views import today_date
from . tokens import generateToken
from .forms import CreateUserform, ParagraphErrorList, UserUpdateForm, ResendConfirmationForm, UserLettreForm, \
    UserUpdateLettreForm
from django.contrib.auth.decorators import login_required
from givelp.utils import send_email
import random
from catalogue.models import Partenaire,  MailSend
from .models import UserInfo




# Create your views here.
"""

def index(request, *args, **kwargs):
    return render(request, 'authentification/register.html')
"""


"""def main(request):
    categories = Categories.objects.filter(date_de_publication_categorie__lt=today_date).order_by('nom_categorie')
    categorie_objs = list(categories)

    random.shuffle(categorie_objs)
    categorie_objs = categorie_objs[:3]

    # print(categorie_objs)
    navbar = "home"
    context = {
        'categorie_objs': categorie_objs,
        "navbar": navbar,
    }

    return render(request, 'catalogue/home.html', context)"""


@login_required(login_url='authentification:login')
def profileuser(request):
    demande_non_definis = MailSend.objects.filter(user=request.user, status_demande="non-defini")
    demande_acceptes = MailSend.objects.filter(user=request.user, status_demande="accepte")
    demande_refuses = MailSend.objects.filter(user=request.user, status_demande="refuse")

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        user_lettre_form = UserUpdateLettreForm(request.POST, request.FILES, instance=request.user.userinfo)

        # enregistrer si le formulaire est valide
        if user_form.is_valid() and user_lettre_form.is_valid():
            user_form.save()
            user_lettre_form.save


            messages.success(request, 'Account has been updated!! ')

            return redirect('authentification/profile.html')

    else:
        user_form = UserUpdateForm(instance=request.user)
        user_lettre_form = UserUpdateLettreForm(instance=request.user.userinfo)


    navbar ="profil"
    partenaires = Partenaire.objects.all()
    context = {
        'user_form': user_form,
        'user_lettre_form' : user_lettre_form,
        'demande_non_definis' : demande_non_definis,
        'demande_acceptes' : demande_acceptes,
        'demande_refuses' : demande_refuses,
        'navbar' : navbar,
        'partenaires': partenaires,

    }

    return render(request, 'authentification/profile.html', context)


def registerpage(request):
    navbar = "register"

    # si la personne est autentifié
    if request.user.is_authenticated:
        return redirect('catalogue:home')
    else:

        form = CreateUserform()
        form_info = UserLettreForm()
        #form_valid = False
        if request.method == 'POST':
            form = CreateUserform(request.POST, error_class=ParagraphErrorList)
            form_info = UserLettreForm(request.POST, request.FILES, error_class=ParagraphErrorList)
            print(form_info['cv'].value())

            if form.is_valid() and form_info.is_valid():

                user = form.save(commit=False)# avec commit on n'eregistre pas mais on stocke
                user.is_active = False
                user.save()


                lettre_motivation = form_info.cleaned_data.get('lettre_motivation')
                cv = form_info.cleaned_data.get('cv')
                img_verify = form_info.cleaned_data.get('img_verify')
                print(f'img:{img_verify}')

                # Créer un objet UserInfo en associant l'username
                form_info = UserInfo(lettre_motivation=lettre_motivation, cv=cv, img_verify=img_verify, user=user )
                form_info.save()

                
                #recuperation du username pour le message de confirmation
                name = form.cleaned_data.get('first_name')
                email_user = form.cleaned_data.get('email')
                #nom = form.cleaned_data.get('last_name')
                #prenom = form.cleaned_data.get('first_name')

                #send_email(nom, prenom, username, email_user, request, user)

                send_email(name, email_user, request, user)


                return redirect('catalogue:home')
            else:
                messages.error(request, 'Nous avons noté des erreurs dans ce formulaire')
    
    context = {
        "form": form,
        "navbar" : navbar,

        "form_info" : form_info,
        

        }
    return render(request, 'authentification/register.html', context)
  


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('catalogue:home')
    else:
        if request.method == 'POST':
            #demander le nom et le passe
            username = request.POST.get('username')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me')

            #print(username)
            #print(password)

            #verifier si l'utilisateur existe dans la bdd
            user = authenticate(request, username=username, password=password)
            if user is not None:
                my_user = User.objects.get(username=username)
                if my_user.is_active == False:
                        messages.error(request, 'You have not confirm your  email do it, in order to activate your account')
                        return redirect('login')

            #si il existe on le redirige a la page d'acceuil
            if user is not None:
                login(request, user)
                if remember_me:
                    messages.success(request, f'Hello  {request.user}')
                    response = redirect('catalogue:home')
                    response.set_cookie('username', username, max_age=3600 * 24 * 30)  # 1 mois
                    response.set_cookie('password', password, max_age=3600 * 24 * 30)
                    request.session.set_expiry(86400*30)
                    return response
                else:
                    messages.success(request, f'Hello  {request.user}')
                    request.session.set_expiry(86400)
                    return redirect('home')
                #username = user.username

            else:
                #dans le cas ou l'utilisateur n'existe pas ou a mal taper ses identifiants un message est envoyé
                messages.info(request, 'Username OR Password is incorrect')

    navbar = "login"
    context = {
        "navbar": navbar,
       
        }
    return render(request, 'authentification/login.html', context)    

def logoutuser(request):
    logout(request)
    messages.success(request, 'logout successfully!')
    #return redirect('catalogue:home')
    response = HttpResponseRedirect(request.META['HTTP_REFERER'])
    response.delete_cookie('username')
    response.delete_cookie('password')

    return response




def resend_confirmation(request):
    if request.method == 'POST':
        form = ResendConfirmationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).last()
            #print(user.username)
            if user:
                if user.is_active == False:
                    send_email(user.username, email, request, user)

                    messages.success(request, "Mail envoyer avec succes !")
                    return redirect('authentification:login')
                else:
                    messages.error(request, "Ce compte à déjà été activé !")
                    return redirect('authentification:login')
            else:
                messages.error(request,"Ce mail n'a pas été retrouvé !")
                return redirect('authentification:register')
    else:
        form = ResendConfirmationForm()

    context = {'form': form}

    return render(request, 'authentification/resend_confirmation.html', context)



















def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generateToken.check_token(user, token):
        user.is_active  = True        
        user.save()
        messages.success(request, "You are account is activated you can login by filling the form below.")
        return redirect("authentification:login")
    else:
        messages.success(request, 'Activation failed please try again')
        return redirect('catalogue:home')
