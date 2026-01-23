from django import forms
from .models import Package

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = [
            'package_weight', 
            'package_volume', 
            'package_description', 
            'package_value',
        ]
