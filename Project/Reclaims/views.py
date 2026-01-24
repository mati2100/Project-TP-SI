from django.shortcuts import render, redirect
from .models import Reclaim
from .forms import ReclaimForm
from Profiles.decorators import token_required


@token_required
def ReclaimListView(request):
    reclaims = Reclaim.objects.all()

    query = request.GET.get('q')
    search_by = request.GET.get('by')

    if query:
        if search_by == 'number':
            reclaims = reclaims.filter(Reclaim_number__icontains=query)
        elif search_by == 'status':
            reclaims = reclaims.filter(Reclaim_status__icontains=query)
        elif search_by == 'client':
            reclaims = reclaims.filter(client__client_firstname__icontains=query) | reclaims.filter(client__client_familyname__icontains=query)
        elif search_by == 'shipment':
            reclaims = reclaims.filter(shipment__shipment_number__icontains=query)

    order = request.GET.get('order')
    if order == 'date_asc':
        reclaims = reclaims.order_by('Reclaim_date')
    elif order == 'date_desc':
        reclaims = reclaims.order_by('-Reclaim_date')
        
    return render(request, 'Reclaim_list.html', {'reclaims': reclaims})
@token_required
def ReclaimCreateView(request):
    if request.method == 'POST':
        form = ReclaimForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Reclaim_list')
    else:
        form = ReclaimForm()
    
    return render(request, 'Reclaim_form.html', {
        'form': form,
        'title': 'Create New Reclamation'
    })
@token_required
def ReclaimUpdateView(request, reclaim_id):
    reclaim = Reclaim.objects.get(id=reclaim_id)
    
    if request.method == 'POST':
        form = ReclaimForm(request.POST, instance=reclaim)
        if form.is_valid():
            form.save()
            return redirect('Reclaim_list')
    else:
        form = ReclaimForm(instance=reclaim)
    
    return render(request, 'Reclaim_form.html', {
        'form': form,
        'title': 'Update Reclaim',
        'reclaim': reclaim
    })
@token_required
def ReclaimDeleteView(request, reclaim_id):
    reclaim = Reclaim.objects.get(id=reclaim_id)
    
    if request.method == 'POST':
        reclaim.delete()
        return redirect('Reclaim_list')
    
    return render(request, 'Reclaim_confirm_delete.html', {'reclaim': reclaim})