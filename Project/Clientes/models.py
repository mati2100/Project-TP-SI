from django.db import models
from django.utils import timezone

class Client(models.Model):
    client_nom = models.CharField(max_length=100, verbose_name="Nom")
    client_prenom = models.CharField(max_length=100, verbose_name="Prénom")
    client_email = models.EmailField(verbose_name="Adresse email",unique=True)
    client_phone = models.CharField(max_length=20, verbose_name="Téléphone")
    client_address = models.TextField(verbose_name="Adresse complète")
    client_city = models.CharField(max_length=100, verbose_name="Ville")
    client_country = models.CharField(max_length=100, verbose_name="Pays", default="Algérie")
    client_registration_date = models.DateTimeField(auto_now_add=True)
    client_actif = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.client_nom} {self.client_prenom} - {'Actif' if self.client_actif else 'Inactif'}"

    