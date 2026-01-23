from django.db import models
from django.utils import timezone

class Shipment(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'),('in_transit', 'In Transit'),('at_sorting_center', 'At Sorting Center'),('out_for_delivery', 'Out for Delivery'),('delivered', 'Delivered'),('failed', 'Delivery Failed'),]
    
    shipment_tracking_number = models.CharField(max_length=30, unique=True, db_index=True)

    shipment_total_weight = models.DecimalField(max_digits=10, decimal_places=2)  # en kg
    shipment_total_volume = models.DecimalField(max_digits=10, decimal_places=2)  # en m³

    shipment_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    shipment_expected_delivery_date = models.DateField(null=True, blank=True)
    shipment_delivery_date = models.DateField(null=True, blank=True)
    shipment_notes = models.TextField()

    shipment_created_at = models.DateTimeField(auto_now_add=True)

    #foreign keys
    driver = models.ForeignKey('Drivers.Driver', on_delete=models.SET_NULL, null=True, blank=True)
    destination = models.ForeignKey('Services.Destination', on_delete=models.SET_NULL, null=True, blank=True)
    service_type = models.ForeignKey('Services.ServiceType', on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey('Clientes.Client', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicles.Vehicle', on_delete=models.SET_NULL, null=True, blank=True)  
    invoice = models.ForeignKey('Invoice.Invoice', on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"Shipment #{self.shipment_number} - {self.client.client_familyname} {self.client.client_firstname}"
    
    def save(self, *args, **kwargs):
        from Services.models import Destination, ServiceType
        try:
            destination = Destination.objects.get(id=self.destination.id)
            service_type = ServiceType.objects.get(id=self.service_type.id)
            self.estimated_amount = (
                destination.base_fare +
                (self.shipment_weight * service_type.st_weight_rate) +
                (self.shipment_volume * service_type.st_volume_rate)
            )
        except:
            pass
        
        super().save(*args, **kwargs)