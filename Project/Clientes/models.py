from django.db import models
from django.utils import timezone

class Client(models.Model):
    client_lastname = models.CharField(max_length=50)
    client_firstname = models.CharField(max_length=50)
    client_email = models.EmailField(unique=True)
    client_phone = models.CharField(max_length=20)
    client_address = models.TextField()
    
    client_due_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    client_created_at = models.DateTimeField(auto_now_add=True)

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
    def get_reclaimss(self):
        from Reclaims.models import Reclaims
        return Reclaims.objects.filter(client=self)