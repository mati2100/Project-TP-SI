from django.db import models

class Destination(models.Model):
    
    destination_city = models.CharField(max_length=50)
    destination_state = models.CharField(max_length=50)
    destination_country = models.CharField(max_length=50)
    destination_base_fare = models.DecimalField(max_digits=10, decimal_places=2)

    destination_created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.destination_city}, {self.destination_country}"
class ServiceType(models.Model):
    PRIORITY_CHOICES = [('high', 'High'),('medium', 'Medium'),('low', 'Low'),]

    service_type_name = models.CharField(max_length=50)
    service_type_description = models.TextField()

    service_type_volume_surcharge = models.DecimalField(max_digits=10, decimal_places=2)  
    service_type_weight_surcharge = models.DecimalField(max_digits=10, decimal_places=2)  

    service_type_priority_level = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='medium')

    service_type_created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_service_type_name_display()} Service"