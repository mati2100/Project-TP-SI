from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaymentListView, name='payment_list'),
    path('create/', views.PaymentCreateView, name='payment_create'),
    path('update/<int:payment_id>/', views.PaymentUpdateView, name='payment_update'),
    path('delete/<int:payment_id>/', views.PaymentDeleteView, name='payment_delete'),
    path('download/<int:payment_id>/', views.payment_download_pdf, name='payment_download_pdf'),
    path('view/<int:payment_id>/', views.payment_view_pdf, name='payment_view_pdf'),
]