from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os, shutil


# Create your models here.


class ManagerInfo(models.Model):
    entreprise_manager = models.BooleanField("Entreprise manager", default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Entreprise manager"

    def __str__(self):
        return str(self.user) + str(self.pk)