from django import forms
from .models import Driver

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            'driver_name', 'driver_email', 'driver_phone', 'driver_address',
            'driver_license', 'license_type', 'driver_active', 'driver_available'
        ]
