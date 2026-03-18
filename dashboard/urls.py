from django.urls import path
from dashboard.views import custom_login, dashboard, custom_logout
from invoices import views

urlpatterns = [
    path('', custom_login, name='custom_login'),  # Set login as the home page
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', custom_logout, name='custom_logout'),
    path('invoice/<int:id>/', views.invoice_detail, name='invoice_detail'),
]
