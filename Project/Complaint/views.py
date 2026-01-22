from django.shortcuts import render, redirect
from .models import Complaint
from .forms import ComplaintForm
from Profiles.decorators import token_required


@token_required
def ComplaintListView(request):
    complaints = Complaint.objects.all()

    query = request.GET.get('q')
    search_by = request.GET.get('by')

    if query:
        if search_by == 'number':
            complaints = complaints.filter(complaint_number__icontains=query)
        elif search_by == 'status':
            complaints = complaints.filter(complaint_status__icontains=query)
        elif search_by == 'client':
            complaints = complaints.filter(client__client_firstname__icontains=query) | complaints.filter(client__client_familyname__icontains=query)
        elif search_by == 'shipment':
            complaints = complaints.filter(shipment__shipment_number__icontains=query)

    order = request.GET.get('order')
    if order == 'date_asc':
        complaints = complaints.order_by('complaint_date')
    elif order == 'date_desc':
        complaints = complaints.order_by('-complaint_date')
        
    return render(request, 'complaint_list.html', {'complaints': complaints})
@token_required
def ComplaintCreateView(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm()
    
    return render(request, 'complaint_form.html', {
        'form': form,
        'title': 'Create New Complaint'
    })
@token_required
def ComplaintUpdateView(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm(instance=complaint)
    
    return render(request, 'complaint_form.html', {
        'form': form,
        'title': 'Update Complaint',
        'complaint': complaint
    })
@token_required
def ComplaintDeleteView(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    
    if request.method == 'POST':
        complaint.delete()
        return redirect('complaint_list')
    
    return render(request, 'complaint_confirm_delete.html', {'complaint': complaint})