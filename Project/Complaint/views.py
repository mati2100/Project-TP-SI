from django.shortcuts import render, redirect
from .models import Complaint
from .forms import ComplaintForm
from Profiles.decorators import token_required


@token_required
def ComplaintListView(request):
    complaints = Complaint.objects.all()
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