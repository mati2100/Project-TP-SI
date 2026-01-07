from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('add/', views.addagent_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('verify-code/', views.verify_code_view, name='verify_code'),
    path('new-password/', views.new_password_view, name='new_password'),
]
