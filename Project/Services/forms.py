from django import forms
from .models import Destination, ServiceType

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['dest_city', 'dest_country', 'dest_zone', 'base_fare']

class ServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = ['st_name', 'st_description', 'st_weight_rate', 'st_volume_rate']
