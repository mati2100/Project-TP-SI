from django.db import models

class Destination(models.Model):
    ZONE_CHOICES = [('local', 'Local'), ('regional', 'Regional'), ('national', 'National'),('international', 'International'),]
    
    dest_city = models.CharField(max_length=100)
    dest_country = models.CharField(max_length=100)
    dest_zone = models.CharField(max_length=50, choices=ZONE_CHOICES, default='national')
    base_fare = models.DecimalField(max_digits=10, decimal_places=2)

    
    def __str__(self):
        return f"{self.dest_city}, {self.dest_country} ({self.get_dest_zone_display()})"

class ServiceType(models.Model):
    TYPE_CHOICES = [('standard', 'Standard'),('express', 'Express'),('international', 'International'),]
    
    st_name = models.CharField(max_length=50, choices=TYPE_CHOICES, default='standard')
    st_description = models.TextField()
    st_weight_rate = models.DecimalField(max_digits=10, decimal_places=2)  # per kg
    st_volume_rate = models.DecimalField(max_digits=10, decimal_places=2)  # per m³
    
    def __str__(self):
        return f"{self.get_st_name_display()} Service"