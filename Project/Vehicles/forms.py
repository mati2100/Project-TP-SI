from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'vehicle_registration_number', 'vehicle_type', 'vehicle_model',
            'vehicle_capacity','vehicle_status', 'vehicle_year', 'vehicle_active'
        ]
