from django.shortcuts import render, redirect
from .models import Incident
from .forms import IncidentForm

def IncidentListView(request):
    incidents = Incident.objects.all()
    return render(request, 'incident_list.html', {'incidents': incidents})

def IncidentCreateView(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('incident_list')
    else:
        form = IncidentForm()
    
    return render(request, 'incident_form.html', {
        'form': form,
        'title': 'Create New Incident'
    })

def IncidentUpdateView(request, incident_id):
    incident = Incident.objects.get(id=incident_id)
    
    if request.method == 'POST':
        form = IncidentForm(request.POST, instance=incident)
        if form.is_valid():
            form.save()
            return redirect('incident_list')
    else:
        form = IncidentForm(instance=incident)
    
    return render(request, 'incident_form.html', {
        'form': form,
        'title': 'Update Incident',
        'incident': incident
    })

def IncidentDeleteView(request, incident_id):
    incident = Incident.objects.get(id=incident_id)
    
    if request.method == 'POST':
        incident.delete()
        return redirect('incident_list')
    
    return render(request, 'incident_confirm_delete.html', {'incident': incident})