from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_familyname', 'client_firstname', 'client_email', 'client_phone', 
                 'client_address', 'client_city', 'client_country', 'client_actif', 'notes']