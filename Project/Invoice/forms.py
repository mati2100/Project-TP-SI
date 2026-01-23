from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'invoice_number', 
            'invoice_issue_date', 
            'invoice_subtotal', 
            'invoice_tax_amount', 
            'invoice_total_amount',
            'invoice_status',
            'client',
        ]
