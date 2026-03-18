from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from invoices.models import Invoice
from django.db.models import Q
from utils.decorators import superuser_required


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'custom_login.html')

@superuser_required
def dashboard(request):
    query = request.GET.get('q')  # Get the search query from the request
    if query:
        invoices_list = Invoice.objects.filter(
            Q(invoice_number__icontains=query) |
            Q(client__name__icontains=query)
        ).order_by('-date_created')  # Modify the ordering if needed
    else:
        invoices_list = Invoice.objects.all().order_by('-date_created')  # Default list if no search

    paginator = Paginator(invoices_list, 20)  # Show 20 invoices per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # Pass the paginated invoices
    }
    return render(request, 'dashboard.html', context)

def custom_logout(request):
    logout(request)
    return redirect('custom_login')
