from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'vehicle_registration_number',
            'vehicle_type',
            'vehicle_model',
            'vehicle_brand',
            'vehicle_year',
            'vehicle_license_plate',
            'vehicle_capacity',
            'vehicle_status',
            'vehicle_fuel_mileage',
            'vehicle_start_date',
            'vehicle_end_date',
            'vehicle_active'
        ]
