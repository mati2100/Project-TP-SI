from django.db import models

class Driver(models.Model):
    driver_first_name = models.CharField(max_length=50)
    driver_last_name = models.CharField(max_length=50)
    driver_email = models.EmailField(unique=True)
    driver_phone_number = models.CharField(max_length=20)
    driver_address = models.TextField()
    driver_license_number = models.CharField(max_length=50, unique=True)
    
    driver_availability = models.BooleanField(default=True)
    driver_hire_date = models.DateField()
    driver_active = models.BooleanField(default=True)

    driver_created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.driver_first_name} {self.driver_last_name} ({self.driver_license_number})"
   