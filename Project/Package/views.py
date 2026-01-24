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
def PackageUpdateView(request, package_id):
    package = Package.objects.get(id=package_id)
    
    if request.method == 'POST':
        form = PackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            return redirect('package_list')
    else:
        form = PackageForm(instance=package)
    
    return render(request, 'package_form.html', {
        'form': form,
        'title': 'Update Package',
        'package': package
    })

@token_required
def PackageDeleteView(request, tour_id):
    tour = Package.objects.get(id=tour_id)
    
    if request.method == 'POST':
        tour.delete()
        return redirect('package_list')
    
    return render(request, 'package_confirm_delete.html', {'tour': tour})