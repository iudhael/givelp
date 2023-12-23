from django.shortcuts import render, get_object_or_404, redirect
from catalogue.models import Modeles, MailSend, Partenaire
from datetime import date
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import UpdateStatusDemandeForm


# Create your views here.

global today_date

today_date = date.today()

def user_is_entreprise_manager(function):
    def wrap(request, *args, **kwargs):
        if not request.user.managerinfo.entreprise_manager:
            return redirect('authentification:login')
        return function(request, *args, **kwargs)
    return wrap

@user_is_entreprise_manager
def entreprise_manager(request):
    entreprise = Modeles.objects.get(user=request.user)
    demande_non_definis = MailSend.objects.filter(status_demande="non-defini", entreprise=entreprise)
    demande_acceptes = MailSend.objects.filter(status_demande="accepte", entreprise=entreprise)
    demande_refuses = MailSend.objects.filter(status_demande="refuse", entreprise=entreprise)
    
    if request.method == 'POST':
        form = UpdateStatusDemandeForm(request.POST)
        if form.is_valid():
            # Traitement du formulaire ici
            demande_pk = request.POST.get('demande_pk')
            demande = MailSend.objects.get(pk=demande_pk)
            demande.status_demande = form.cleaned_data['status_demande']
            print(demande_pk)
            demande.save()
    else:
        form = UpdateStatusDemandeForm()

    navbar = "demandes"
    partenaires = Partenaire.objects.all()
    context = {
        'demande_non_definis': demande_non_definis,
        'demande_acceptes': demande_acceptes,
        'demande_refuses': demande_refuses,
        'form' : form,
        "navbar": navbar,
        'partenaires': partenaires,
    }
    return render(request, 'entreprise_manager/demande.html', context)