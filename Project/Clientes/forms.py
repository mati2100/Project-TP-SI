from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_lastname', 
                  'client_firstname', 
                  'client_email', 
                  'client_phone', 
                  'client_address', 
                  'client_due_balance'
                  ]