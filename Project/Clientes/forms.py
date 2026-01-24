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
                  ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # empty labels placeholders
        self.fields['client_lastname'].widget.attrs.update({'placeholder': 'Enter last name'})
        self.fields['client_firstname'].widget.attrs.update({'placeholder': 'Enter first name'})
        self.fields['client_email'].widget.attrs.update({'placeholder': 'Enter email address'})
        self.fields['client_phone'].widget.attrs.update({'placeholder': 'Enter phone number'})
        self.fields['client_address'].widget.attrs.update({'placeholder': 'Enter address'})