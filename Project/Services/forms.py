from django import forms
from .models import Destination, ServiceType

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = [
            'destination_city',
            'destination_state',
            'destination_country', 
            'destination_base_fare']

class ServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = [
            'service_type_name', 
            'service_type_description', 
            'service_type_volume_surcharge', 
            'service_type_weight_surcharge', 
            'service_type_priority_level']