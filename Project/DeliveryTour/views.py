from django.shortcuts import render, redirect
from .models import DeliveryTour
from .forms import DeliveryTourForm

def DeliveryTourListView(request):
    tours = DeliveryTour.objects.all()
    return render(request, 'deliverytour_list.html', {'tours': tours})

def DeliveryTourCreateView(request):
    if request.method == 'POST':
        form = DeliveryTourForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('deliverytour_list')
    else:
        form = DeliveryTourForm()
    
    return render(request, 'deliverytour_form.html', {
        'form': form,
        'title': 'Create New Delivery Tour'
    })

def DeliveryTourUpdateView(request, tour_id):
    tour = DeliveryTour.objects.get(id=tour_id)
    
    if request.method == 'POST':
        form = DeliveryTourForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('deliverytour_list')
    else:
        form = DeliveryTourForm(instance=tour)
    
    return render(request, 'deliverytour_form.html', {
        'form': form,
        'title': 'Update Delivery Tour',
        'tour': tour
    })

def DeliveryTourDeleteView(request, tour_id):
    tour = DeliveryTour.objects.get(id=tour_id)
    
    if request.method == 'POST':
        tour.delete()
        return redirect('deliverytour_list')
    
    return render(request, 'deliverytour_confirm_delete.html', {'tour': tour})