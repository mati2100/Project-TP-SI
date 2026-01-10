from django.db import models

class Vehicle(models.Model):
    STATUS_CHOICES = [('available', 'Available'), ('in_use', 'In Use'), ('maintenance', 'Under Maintenance'), ('out_of_service', 'Out of Service')]
    TYPE_CHOICES = [('truck', 'Truck'), ('van', 'Van'),('motorcycle', 'Motorcycle')]
    
    vehicle_registration_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='truck')
    vehicle_capacity = models.DecimalField(max_digits=10, decimal_places=2) 
    vehicle_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='available')
    vehicle_model = models.CharField(max_length=100)
    vehicle_year = models.IntegerField()
    vehicle_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.vehicle_registration_number} ({self.vehicle_type})"
    
    def get_status_color(self):
        status_colors = {
            'available': 'green',
            'in_use': 'orange',
            'maintenance': 'red',
            'out_of_service': 'gray',
        }
        return status_colors.get(self.vehicle_status, 'black')
    
    def get_tours(self):
        from DeliveryTour.models import DeliveryTour
        return DeliveryTour.objects.filter(vehicle=self)