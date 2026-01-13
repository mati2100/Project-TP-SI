from django.urls import path
from . import views

urlpatterns = [
    path('', views.ComplaintListView, name='complaint_list'),
    path('create/', views.ComplaintCreateView, name='complaint_create'),
    path('update/<int:complaint_id>/', views.ComplaintUpdateView, name='complaint_update'),
    path('delete/<int:complaint_id>/', views.ComplaintDeleteView, name='complaint_delete'),
]