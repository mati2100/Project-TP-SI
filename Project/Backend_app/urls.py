from django.urls import path
from . import views

urlpatterns = [
    path('agent/login/', views.login_view, name='login'),
    path('agent/add/', views.addagent_view, name='register'),
]
