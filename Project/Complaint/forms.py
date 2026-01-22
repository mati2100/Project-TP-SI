from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'client', 'shipment', 'invoice','complaint_number',
            'complaint_category', 'complaint_description',
            'complaint_status', 'complaint_priority',
        ]
