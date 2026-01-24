from django.shortcuts import render, redirect
from .models import Invoice
from .forms import InvoiceForm
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
            from django.db.models import F
            from Clientes.models import Client
            invoice = form.save(commit=False)
            invoice.save()
            form.save_m2m()
            Client.objects.filter(id=invoice.client.id).update(
                client_due_balance=F('client_due_balance') + invoice.invoice_total_amount
            )
            return redirect('invoice_list')
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
            return redirect('invoice_list')
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