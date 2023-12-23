import os

from django.forms import ModelForm
from django.forms import ModelForm, TextInput, EmailInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserInfo
from django import forms
from django.forms.utils import ErrorList

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

#from .models import Profile






class ParagraphErrorList(ErrorList):

# gerer la maniere dont apparait les erreur ici les fait apparaitre sous forme de paragraphe au lieu de <li></li>
# appeler la fonction au niveau de la vu registerpage

    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return  ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="smail error">%s</p>' % e for e in self])


class CreateUserform(UserCreationForm):

    first_name = forms.CharField(label="Nom", max_length=50, min_length=2,required=True, widget=forms.TextInput(attrs={
        'class' : 'input-form',
        'placeholder' : 'Nom',
        'autocomplete' : 'on',
        
    }))

    last_name = forms.CharField(label="Prénom",max_length=50, min_length=2,required=True, widget=forms.TextInput(attrs={
        'class' : 'input-form',
        'placeholder' : 'Prénom',
        'autocomplete' : 'on',
    }))

    username = forms.CharField(label="Nom d'utilisateur",max_length=50, min_length=2,required=True, widget=forms.TextInput(attrs={
        'class' : 'input-form',
        'placeholder' : 'username',
        'autocomplete' : 'off',
        
    }))


    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class' : 'input-form',
        'placeholder' : 'Email',
        'autocomplete' : 'off',
    }))

    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={
        'class' : 'form-control, input-form',
        'placeholder' : 'password',
        'id' : 'password_pwd1',
    }))

    password2 = forms.CharField(label="Confirmation du mot de passe", widget=forms.PasswordInput(attrs={
        'class' : 'input-form',
        'placeholder' : 'confirm password',
        'id': 'password_pwd2',
    }))
    """
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            raise forms.ValidationError("This email has already been registered. Please reset your password")
        return email
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class UserLettreForm(forms.ModelForm):

    cv = forms.FileField(label="Curiculum Vitae", widget=forms.FileInput(attrs={
        'class' : '',

    }))

    lettre_motivation = forms.FileField(label="Lettre de motivation", widget=forms.FileInput(attrs={
        'class' : '',

    }))

    img_verify = forms.ImageField(label="Image de verification", widget=forms.FileInput(attrs={
        'class' : '',

    }))

    """ def clean_cv(self):
        cv = str(self.cleaned_data.get('cv'))

        # Récupérer l'extension du fichier
        extension = os.path.splitext(cv)[1]
        # Récupérer la taille du fichier
        taille_octets = os.path.getsize(self.cleaned_data.get('cv').path)

        # Convertir la taille en mégaoctets
        taille_mo = taille_octets / 1024 / 1024  # 1 Mo = 1024*1024 octets

        # Imprimer la taille en mégaoctets avec deux décimales
        print(f"La taille du fichier {cv} est de {taille_mo:.2f} Mo")

    """
        #if extension != ".pdf":
            #raise forms.ValidationError("Veuillez charger un fichier au format pdf")
        
        #if taille_mo > 2:
            #raise forms.ValidationError("La taille dufichier doit etre inférieure ou égale à 3Mo")
        
        #return cv
    


    class Meta:
        model = UserInfo
        fields = ['lettre_motivation', 'cv', 'img_verify']



#formulaire de mise a jour des identifiants username,firstname, lastname et email
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='first_name',max_length=50, min_length=2, required=True)

    last_name = forms.CharField(label='last_name',max_length=50, min_length=2, required=True)
    email = forms.EmailField(label='Email', required=True)

    username= forms.CharField(label='Username', min_length=4, max_length=35)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class UserUpdateLettreForm(forms.ModelForm):
    lettre_motivation = forms.FileField()
    cv = forms.FileField()



    class Meta:
        model = UserInfo
        fields = ['cv', 'lettre_motivation', ]



class ResendConfirmationForm(forms.Form):
    email = forms.EmailField(label='Email',required=True, widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'email',
        'autocomplete' : 'on',
    }))


