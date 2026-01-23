from django.shortcuts import render, redirect
from .models import Payment
from .forms import PaymentForm

def PaymentListView(request):
    payments = Payment.objects.all()
    return render(request, 'payment_list.html', {'payments': payments})

def PaymentCreateView(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            payment.discount_balance()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    
    return render(request, 'payment_form.html', {
        'form': form,
        'title': 'Create New Payment'
    })

def PaymentUpdateView(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    
    if request.method == 'POST':
        old_amount = payment.payment_amount
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            from Clientes.models import Client
            from django.db.models import F
            payment = form.save()
            if old_amount != payment.payment_amount:
                Client.objects.filter(id=payment.client.id).update(
                    balance=F('balance') + old_amount - payment.payment_amount
                )
            return redirect('payment_list')
    else:
        form = PaymentForm(instance=payment)
    
    return render(request, 'payment_form.html', {
        'form': form,
        'title': 'Update Payment',
        'payment': payment
    })

def PaymentDeleteView(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    
    if request.method == 'POST':
        from Clientes.models import Client
        from django.db.models import F
        Client.objects.filter(id=payment.client.id).update(
            balance=F('balance') + payment.payment_amount
        )
        payment.delete()
        return redirect('payment_list')
    
    return render(request, 'payment_confirm_delete.html', {'payment': payment})