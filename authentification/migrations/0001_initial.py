# Generated by Django 4.1 on 2023-12-23 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "lettre_motivation",
                    models.FileField(
                        upload_to="utilisateur/", verbose_name="lettre de motivation"
                    ),
                ),
                (
                    "cv",
                    models.FileField(
                        upload_to="utilisateur/", verbose_name="curiculum vitae"
                    ),
                ),
                (
                    "img_verify",
                    models.ImageField(
                        upload_to="utilisateur/", verbose_name="image de verification"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name": "info utilisateur",},
        ),
    ]
