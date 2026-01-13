from django.db import models

class Driver(models.Model):
    driver_name = models.CharField(max_length=100)
    driver_email = models.EmailField(unique=True)
    driver_phone = models.CharField(max_length=20)
    driver_address = models.TextField()
    driver_license = models.CharField(max_length=50, unique=True)
    license_type = models.CharField(max_length=50)
    driver_active = models.BooleanField(default=True)
    driver_available = models.BooleanField(default=True)
    hire_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.driver_name} ({self.driver_license})"
   
      # Méthode pour récupérer les tournées du chauffeur
    def get_tours(self):
        from DeliveryTour_app.models import DeliveryTour
        return DeliveryTour.objects.filter(driver=self)