from django.shortcuts import render, redirect
from .models import Invoice
from .forms import InvoiceForm

def InvoiceListView(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoice_list.html', {'invoices': invoices})

def InvoiceCreateView(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            invoice.calculate_amounts()  # Calculer les montants
            return redirect('invoice_list')
    else:
        form = InvoiceForm()
    
    return render(request, 'invoice_form.html', {
        'form': form,
        'title': 'Create New Invoice'
    })

def InvoiceUpdateView(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            invoice.calculate_amounts()
            return redirect('invoice_list')
    else:
        form = InvoiceForm(instance=invoice)
    
    return render(request, 'invoice_form.html', {
        'form': form,
        'title': 'Update Invoice',
        'invoice': invoice
    })

def InvoiceDeleteView(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    
    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice_list')
    
    return render(request, 'invoice_confirm_delete.html', {'invoice': invoice})