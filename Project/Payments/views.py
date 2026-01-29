from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Payment
from .forms import PaymentForm
from Invoice.pdf_utils import generate_payment_receipt_pdf

def PaymentListView(request):
    payments = Payment.objects.all()
    return render(request, 'payment_list.html', {'payments': payments})

def PaymentCreateView(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            payment.discount_balance()
            #  Go back to where user came from
            return redirect(request.GET.get("next", "payment_list"))
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
                    client_due_balance=F('client_due_balance') + old_amount - payment.payment_amount
                )
            #  Go back to where user came from
            return redirect(request.GET.get("next", "payment_list"))
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
            client_due_balance=F('client_due_balance') + payment.payment_amount
        )
        payment.delete()
        #  Go back to where user came from
        return redirect(request.GET.get("next", "payment_list"))
    
    return render(request, 'payment_confirm_delete.html', {'payment': payment})

def payment_download_pdf(request, payment_id):
    """Download payment receipt as PDF"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    # Generate PDF
    pdf_buffer = generate_payment_receipt_pdf(payment)
    
    # Create response (detect whether generator returned HTML or actual PDF bytes)
    content = pdf_buffer.getvalue()
    content_stripped = content.lstrip()
    if content_stripped.startswith(b'<!DOCTYPE') or content_stripped.startswith(b'<html'):
        # Generator returned HTML - serve as HTML so browser can render it
        response = HttpResponse(content, content_type='text/html; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="Receipt_{payment.payment_number}.html"'
    else:
        response = HttpResponse(content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Receipt_{payment.payment_number}.pdf"'

    return response

def payment_view_pdf(request, payment_id):
    """View payment receipt as PDF in browser"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    # Generate PDF
    pdf_buffer = generate_payment_receipt_pdf(payment)
    
    # Create response (detect whether generator returned HTML or actual PDF bytes)
    content = pdf_buffer.getvalue()
    content_stripped = content.lstrip()
    if content_stripped.startswith(b'<!DOCTYPE') or content_stripped.startswith(b'<html'):
        # Generator returned HTML - render in browser
        response = HttpResponse(content, content_type='text/html; charset=utf-8')
        response['Content-Disposition'] = f'inline; filename="Receipt_{payment.payment_number}.html"'
    else:
        response = HttpResponse(content, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Receipt_{payment.payment_number}.pdf"'

    return response