from django.db import models

from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    readableText=models.CharField(max_length=64, null=False, blank=False)
    # Imagem ?
    # Icone ?