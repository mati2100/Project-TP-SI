from django import forms
from .models import Driver

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            'driver_first_name', 
            'driver_last_name',
            'driver_email', 
            'driver_phone_number', 
            'driver_address',
            'driver_license_number', 
            'driver_availability', 
            'driver_hire_date',
            'driver_active'
        ]
