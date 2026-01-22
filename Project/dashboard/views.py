from django.contrib.auth.decorators import login_required
from django.shortcuts import render , redirect

from django.shortcuts import render, redirect

def index(request):
    if 'agent_id' not in request.session:
        return redirect('/add/')  # redirect if not logged in
    return render(request, "dashboard/index.html")