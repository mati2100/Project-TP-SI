from django.urls import path
from . import views

urlpatterns = [
    path('agent/login/', views.login_view, name='login'),
    path('agent/add/', views.addagent_view, name='register'),
     path('agent/forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('agent/verify-code/', views.verify_code_view, name='verify_code'),
    path('agent/new-password/', views.new_password_view, name='new_password'),
]
