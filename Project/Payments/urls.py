from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaymentListView, name='payment_list'),
    path('create/', views.PaymentCreateView, name='payment_create'),
    path('update/<int:invoice_id>/', views.PaymentUpdateView, name='payment_update'),
    path('delete/<int:invoice_id>/', views.PaymentDeleteView, name='payment_delete'),
]