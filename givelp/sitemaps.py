from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from catalogue.models import Modeles

class ModeleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Modeles.objects.all()

    def location(self, obj):
        return reverse('catalogue:detail_categorie', args=[obj.pk])






