from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from authentification.tokens import generateToken
from givelp import settings

def send_email(username,email_user,request,user):
    messages.success(request, f'{username}, your account has been successfully created. We have sent you an email.\n You must comfirm in order to activate your account.')

    # send the confirmation email
    current_site = get_current_site(request)
    email_suject = "confirm your email GUIVELP Login!"
    messageConfirm = render_to_string("emailConfimation.html", {
        'name': username,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generateToken.make_token(user)
    })

    email = EmailMessage(
        email_suject,
        messageConfirm,
        settings.EMAIL_HOST_USER,
        [email_user]
    )

    email.fail_silently = False
    value = email.send()
    if not value:
        messages.error(request, "Une erreur lors de l'envoie du mail")


def send_info_email(request, nom, prenom, username, email_user,type_stage, servive_stage,  cv, motiv_lettre, email_entreprise):
    messages.success(request, f'{username}, Mail envoyer avec success')

    # send the confirmation email
    current_site = get_current_site(request)
    email_suject = "demade de stage test test !"
    messageConfirm = render_to_string("emailDemande.html", {
        'nom': nom,
        'prenom': prenom,
        'name': username,
        'email_user' : email_user,
        'type_stage' : type_stage,
        'servive_stage' : servive_stage,

    })

    email = EmailMessage(
        email_suject,
        messageConfirm,
        settings.EMAIL_HOST_USER,
        [email_entreprise]
    )

    email.attach_file(cv)
    email.attach_file(motiv_lettre)
    email.fail_silently = False
    value = email.send()
    if not value:
        messages.error(request, "Une erreur lors de l'envoie du mail")
    return value
