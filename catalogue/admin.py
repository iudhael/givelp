from django.contrib import admin
from .models import *
# Register your models here.

class ServicesEntrepriseInline(admin.TabularInline):
    model = ServicesEntreprise
    fieldsets = [
        (None, {'fields': ['services', ]})
    ]
    extra = 1

class ModeleInline(admin.TabularInline):
    model = Modeles

    fieldsets = [
        (None, {'fields': ['nom_modele',
                           'email_entreprise',
                           'date_de_publication',
                           'experience_level',
                           'short_job_description',
                           'job_description',
                           ]})
    ]
    extra = 1

@admin.register(Categories)
class CategorieAdmin(admin.ModelAdmin):
    inlines = [ModeleInline,]
    readonly_fields = ["created_at_categorie"]
    search_fields = ['nom_categorie','created_at_categorie', 'date_de_publication_categorie', "creat"]

@admin.register(Modeles)
class ModeleAdmin(admin.ModelAdmin):
    inlines = [ServicesEntrepriseInline,]
    readonly_fields = ["created_at_modele"]
    search_fields = ['nom_modele', 'created_at_modele', 'date_de_publication', ]

admin.site.register(Partenaire)
admin.site.register(MailSend)
