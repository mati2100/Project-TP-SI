from django.db import models
from django.utils import timezone

class Client(models.Model):
    client_lastname = models.CharField(max_length=100, verbose_name="Nom")
    client_firstname = models.CharField(max_length=100, verbose_name="Prénom")
    client_email = models.EmailField(verbose_name="Adresse email",unique=True)
    client_phone = models.CharField(max_length=20, verbose_name="Téléphone")
    client_address = models.TextField(verbose_name="Adresse complète")
    client_city = models.CharField(max_length=100, verbose_name="Ville")
    client_country = models.CharField(max_length=100, verbose_name="Pays", default="Algérie")
    client_registration_date = models.DateTimeField(auto_now_add=True)
    client_actif = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.client_lastname} {self.client_firstname} - {'Actif' if self.client_actif else 'Inactif'}"

    # Méthode pour récupérer les expéditions du client
    def get_shipments(self):
        from Shipment.models import Shipment
        return Shipment.objects.filter(client=self)
    
    # Méthode pour récupérer les factures du client
    def get_invoices(self):
        from Invoice.models import Invoice
        return Invoice.objects.filter(client=self)
    
    # Méthode pour récupérer les réclamations du client
    def get_complaints(self):
        from Complaint.models import Complaint
        return Complaint.objects.filter(client=self)