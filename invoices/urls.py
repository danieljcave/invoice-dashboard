from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('invoice/<int:invoice_id>/pdf/', views.generate_invoice_pdf, name='generate_invoice_pdf'),
    path('invoice/<int:invoice_id>/pdf/view/', views.view_invoice_pdf, name='view_invoice_pdf'),
    path('invoice/<int:invoice_id>/send-email/', views.send_invoice_email, name='send_invoice_email'),
    path('create/', views.create_invoice, name='create_invoice'),
    path('invoice/<int:id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<int:id>/edit/', views.invoice_edit, name='edit_invoice'),
    path('invoice/<int:id>/delete/', views.invoice_delete, name='invoice_delete'),
    path('', views.client_list, name='client_list'),
    path('add/', views.create_client, name='create_client'),
    path('clients/<int:id>/edit/', views.edit_client, name='edit_client'),
    path('client/<int:id>/delete/', views.delete_client, name='delete_client'),
    path('dogs/', views.dog_list, name='dog_list'),
    path('dog/create/', views.create_dog, name='create_dog'),
    path('dog/<int:id>/edit/', views.edit_dog, name='edit_dog'),
    path('dog/<int:id>/delete/', views.delete_dog, name='delete_dog'),
    path('counter/', views.counter, name='counter'),
]
