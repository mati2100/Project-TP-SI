from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'client', 'payment_number' ,'payment_date' ,
            'payment_amount' ,'payment_method' ,'payment_status' ,
        ]
