from django.urls import path
from . import views

urlpatterns = [
    path('', views.DeliveryTourListView, name='tour_list'),
    path('create/', views.DeliveryTourCreateView, name='tour_create'),
    path('update/<int:tour_id>/', views.DeliveryTourUpdateView, name='tour_update'),
    path('delete/<int:tour_id>/', views.DeliveryTourDeleteView, name='tour_delete'),
]