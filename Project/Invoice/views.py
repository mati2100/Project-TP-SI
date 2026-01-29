from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Invoice
from .forms import InvoiceForm
from .pdf_utils import generate_invoice_pdf
from Profiles.decorators import token_required


@token_required
def InvoiceListView(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoice_list.html', {'invoices': invoices})

@token_required
def InvoiceCreateView(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.save()
            form.save_m2m()
            #  Go back to where user came from
            return redirect(request.GET.get("next", "invoice_list"))
    else:
        form = InvoiceForm()
    
    return render(request, 'invoice_form.html', {
        'form': form,
        'title': 'Create New Invoice'
    })

@token_required
def InvoiceUpdateView(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    
    if request.method == 'POST':
        
        old_total = invoice.invoice_total_amount
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            from django.db.models import F
            from Clientes.models import Client
            invoice = form.save()
            if old_total != invoice.invoice_total_amount:
                Client.objects.filter(id=invoice.client.id).update(
                    client_due_balance=F('client_due_balance') - old_total + invoice.invoice_total_amount
                )
                #  Go back to where user came from
            return redirect(request.GET.get("next", "invoice_list"))
    else:
        form = InvoiceForm(instance=invoice)
    
    return render(request, 'invoice_form.html', {
        'form': form,
        'title': 'Update Invoice',
        'invoice': invoice
    })

@token_required
def InvoiceDeleteView(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    
    if request.method == 'POST':
        from Clientes.models import Client
        from django.db.models import F
        Client.objects.filter(id=invoice.client.id).update(
            client_due_balance=F('client_due_balance') - invoice.invoice_total_amount
        )
        invoice.delete()
        return redirect('invoice_list')
    
    return render(request, 'invoice_confirm_delete.html', {'invoice': invoice})