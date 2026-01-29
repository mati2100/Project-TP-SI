from django.shortcuts import render, redirect
from .models import Incident
from .forms import IncidentForm
from Profiles.decorators import token_required


@token_required
def IncidentListView(request):
    incidents = Incident.objects.all()
    return render(request, 'incident_list.html', {'incidents': incidents})

@token_required
def IncidentCreateView(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            form.save()
            #  Go back to where user came from
            return redirect(request.GET.get("next", "incident_list"))
    else:
        form = IncidentForm()
    
    return render(request, 'incident_form.html', {
        'form': form,
        'title': 'Create New Incident'
    })

@token_required
def IncidentUpdateView(request, incident_id):
    incident = Incident.objects.get(id=incident_id)
    
    if request.method == 'POST':
        form = IncidentForm(request.POST, instance=incident)
        if form.is_valid():
            form.save()
            #  Go back to where user came from
            return redirect(request.GET.get("next", "incident_list"))
    else:
        form = IncidentForm(instance=incident)
    
    return render(request, 'incident_form.html', {
        'form': form,
        'title': 'Update Incident',
        'incident': incident
    })

@token_required
def IncidentDeleteView(request, incident_id):
    incident = Incident.objects.get(id=incident_id)
    
    if request.method == 'POST':
        incident.delete()
        #  Go back to where user came from
        return redirect(request.GET.get("next", "incident_list"))
    
    return render(request, 'incident_confirm_delete.html', {'incident': incident})