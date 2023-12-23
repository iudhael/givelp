import os

from django.forms import ModelForm, TextInput, EmailInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from catalogue.models import MailSend
from django import forms



#from .models import Profile



class UpdateStatusDemandeForm(ModelForm):
    status_demande = forms.ChoiceField(label="", choices=MailSend.STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    #demande_pk = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = MailSend
        fields = ['status_demande', ]



