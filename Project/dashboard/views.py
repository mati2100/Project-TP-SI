from django.contrib.auth.decorators import login_required
from Profiles.decorators import token_required
from django.shortcuts import render , redirect

@token_required
def index(request):
    return render(request, "dashboard/index.html")