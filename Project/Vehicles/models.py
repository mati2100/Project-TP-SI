from django.db import models

class Vehicle(models.Model):
    STATUS_CHOICES = [('available', 'Available'), ('in_use', 'In Use'), ('maintenance', 'Under Maintenance'), ('out_of_service', 'Out of Service')]
    TYPE_CHOICES = [('truck', 'Truck'), ('van', 'Van'),('motorcycle', 'Motorcycle')]
    
    vehicle_registration_number = models.CharField(max_length=50, unique=True)

    vehicle_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='truck')
    vehicle_brand = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_year = models.IntegerField()

    vehicle_license_plate = models.CharField(max_length=50, unique=True)
    vehicle_capacity = models.DecimalField(max_digits=10, decimal_places=2) 
    vehicle_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='available')
    vehicle_fuel_mileage = models.DecimalField(max_digits=10, decimal_places=2)

    vehicle_start_date = models.DateField(null=True, blank=True)
    vehicle_end_date = models.DateField(null=True, blank=True)
    vehicle_active = models.BooleanField(default=True)

    vehicle_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.registration_number} ({self.type})"
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
        from Package.models import Package
        return Package.objects.filter(vehicle=self)