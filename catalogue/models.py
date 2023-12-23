from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os, shutil


# Create your models here.


class Categories(models.Model):
    # robe, chemisier, combinaison...
    nom_categorie = models.CharField('nom de la categorie', max_length=50)
    created_at_categorie = models.DateTimeField('date creation de la categorie', auto_now_add=True)

    date_de_publication_categorie = models.DateField('date de publication de la categorie ', default="2022-11-10")
    image_categorie = models.ImageField('image de la categorie du modele', upload_to=f'categories/')

    class Meta:
        verbose_name = "categorie"

    def __str__(self):
        return self.nom_categorie

    def save(self, *args, **kwargs):  # remplacer la methode de sauvegarde por ajouter des fonctionaliter au save parent
        super(Categories, self).save(*args, **kwargs)

        # chemin actuel de l'image
        chemin_actuel = str(self.image_categorie)
        # print(chemin_actuel)
        picture_name = chemin_actuel.split('/')[-1]
        # print(picture_name)

        new_dossier = f'media/categories/{self.nom_categorie}'
        # print(new_dossier)
        # chemin par defaut de l'enregistrement de l'image
        default_chemin = f'media/categories/{picture_name}'
        # print(default_chemin)
        # nouveau chemin de l'enregistrement de l'Image
        new_chemin = f'{new_dossier}/{picture_name}'
        # print(new_chemin)

        if not os.path.isdir(new_dossier):
            os.makedirs(new_dossier)

        if os.path.isfile(default_chemin):
            new_chemin_actuel = f'categories/{self.nom_categorie}/{picture_name}'
            shutil.move(default_chemin, new_chemin)
            self.image_categorie = new_chemin_actuel
            self.save()

        img = Image.open(self.image_categorie.path)  # on ouvre l'image acctuelle et on va redimentionner

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)  # redimentioner 300/300
            img.save(self.image_categorie.path)

#le modele ici fait référence à l'entreprise cette classe répertorie donc les in formation sur les entreprises
class Modeles(models.Model):
    nom_modele = models.CharField("nom de l'entreprise", max_length=50)
    email_entreprise = models.EmailField("email de l'entreprise", max_length=50)
    created_at_modele = models.DateTimeField('date creation du modele', auto_now_add=True)



    date_de_publication = models.DateField('date de publication du modele ', default="2022-11-10")

    experience_level = models.CharField("experience level", max_length=50)
    short_job_description = models.TextField("courte job description")
    job_description = models.TextField("job description")


    categorie = models.ForeignKey(Categories, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #image = models.ImageField('image du modele',upload_to='categories/')  # enregistrer l'image dans le dossier de la categorie selectioner


    class Meta:
        verbose_name = "entreprise"

    def __str__(self):
        return self.nom_modele + f' ({self.categorie.nom_categorie})'


class ServicesEntreprise(models.Model):
    services = models.CharField("les services de l'entreprise", max_length=50)
    modele = models.ForeignKey(Modeles, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "service de l'entreprise"

    def __str__(self):
        return self.services

class Partenaire(models.Model):
    nom_partenaire = models.CharField("nom des partenaires", max_length=20)
    logo_partenaire = models.ImageField("logo partenaire", upload_to="partenaire/")

    def __str__(self):
        return self.nom_partenaire

class MailSend(models.Model):
    NON_DEFINI = 'non-defini'
    ACCEPTE = 'accepte'
    REFUSE = 'refuse'

    STATUS_CHOICES = [
        (NON_DEFINI, 'Non Defini'),
        (ACCEPTE, 'Accepté'),
        (REFUSE, 'Refusé'),
    ]

    
    status_demande = models.CharField(max_length=10, choices=STATUS_CHOICES, default=NON_DEFINI,)
    created_at = models.DateTimeField("date d'envoie de la demande", auto_now_add=True)
    #update_status_at = models.DateTimeField("date de mise à jour statut", default=Today)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entreprise = models.ForeignKey(Modeles, on_delete=models.CASCADE)

    def __str__(self):
        return "mail envoyer :" + self.status_demande

