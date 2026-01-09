from django.urls import path
from . import views

urlpatterns = [
    path('', views.ClientListView, name='client_list'),
    path('create/', views.ClientCreateView, name='client_create'),
    path('update/<int:client_id>/', views.ClientUpdateView, name='client_update'),
    path('delete/<int:client_id>/', views.ClientDeleteView, name='client_delete'),
]