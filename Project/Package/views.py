from django.shortcuts import render, redirect
from .models import Package
from .forms import PackageForm
from Profiles.decorators import token_required


@token_required
def PackageListView(request):
    packages = Package.objects.all()
    return render(request, 'package_list.html', {'packages': packages})

@token_required
def PackageCreateView(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('package_list')
    else:
        form = PackageForm()
    
    return render(request, 'package_form.html', {
        'form': form,
        'title': 'Create New Package'
    })

@token_required
def PackageUpdateView(request, tour_id):
    tour = Package.objects.get(id=tour_id)
    
    if request.method == 'POST':
        form = PackageForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('package_list')
    else:
        form = PackageForm(instance=tour)
    
    return render(request, 'package_form.html', {
        'form': form,
        'title': 'Update Package',
        'tour': tour
    })

@token_required
def PackageDeleteView(request, tour_id):
    tour = Package.objects.get(id=tour_id)
    
    if request.method == 'POST':
        tour.delete()
        return redirect('package_list')
    
    return render(request, 'package_confirm_delete.html', {'tour': tour})