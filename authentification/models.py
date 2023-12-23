from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os, shutil


# Create your models here.

class UserInfo(models.Model):
    lettre_motivation = models.FileField("lettre de motivation", upload_to='utilisateur/')
    cv = models.FileField("curiculum vitae", upload_to='utilisateur/')
    img_verify = models.ImageField("image de verification",upload_to='utilisateur/')
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "info utilisateur"

    def __str__(self):
        return str(self.user) + str(self.pk) 




    def save(self, *args, **kwargs):  # remplacer la methode de sauvegarde por ajouter des fonctionaliter au save parent
        super(UserInfo, self).save(*args, **kwargs)

        # chemin actuel de l'image
        chemin_actuel_ml = str(self.lettre_motivation)
        chemin_actuel_cv = str(self.cv)
        chemin_actuel_img = str(self.img_verify)
        print(chemin_actuel_img)
        
        document_name_ml = chemin_actuel_ml.split('/')[-1]
        document_name_cv = chemin_actuel_cv.split('/')[-1]
        document_name_img = chemin_actuel_img.split('/')[-1]
        

        

        new_dossier = f'media/utilisateur/{self.pk}'
        # print(new_dossier)
        # chemin par defaut de l'enregistrement de l'image
        default_chemin_ml = f'media/utilisateur/{document_name_ml}'
        default_chemin_cv = f'media/utilisateur/{document_name_cv}'
        default_chemin_img = f'media/utilisateur/{document_name_img}'
        # print(default_chemin)
        # nouveau chemin de l'enregistrement de l'Image
        new_chemin_ml = f'{new_dossier}/{document_name_ml}'
        new_chemin_cv = f'{new_dossier}/{document_name_cv}'
        new_chemin_img = f'{new_dossier}/{document_name_img}'
        # print(new_chemin)

        if not os.path.isdir(new_dossier):
            os.makedirs(new_dossier)

        if os.path.isfile(default_chemin_ml):
            new_chemin_actuel_ml = f'utilisateur/{self.pk}/{document_name_ml}'
            shutil.move(default_chemin_ml, new_chemin_ml)
            self.lettre_motivation = new_chemin_actuel_ml
            self.save()

        if os.path.isfile(default_chemin_cv):
            new_chemin_actuel_cv = f'utilisateur/{self.pk}/{document_name_cv}'
            shutil.move(default_chemin_cv, new_chemin_cv)
            self.cv = new_chemin_actuel_cv
            self.save()

        if os.path.isfile(default_chemin_img):
            new_chemin_actuel_img = f'utilisateur/{self.pk}/{document_name_img}'
            shutil.move(default_chemin_img, new_chemin_img)
            self.img_verify = new_chemin_actuel_img
            self.save()
