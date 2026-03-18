import os
import base64
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .models import Invoice, LineItem, Client, Dog
from .forms import InvoiceForm, LineItemForm, InvoiceLineItemFormSet, ClientForm, DogForm
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.staticfiles import finders
from weasyprint import HTML
from django.db.models import Max
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import Lower
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from utils.decorators import superuser_required
import json


@superuser_required
def create_invoice(request):
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        formset = InvoiceLineItemFormSet(request.POST)

        if invoice_form.is_valid():
            # Save the invoice first to generate a primary key
            invoice = invoice_form.save(commit=False)
            invoice.invoice_number = str(invoice.client.current_invoice_number)
            invoice.client.current_invoice_number += 1
            invoice.client.save(update_fields=['current_invoice_number'])
            invoice.save()

            # Associate line items with the saved invoice
            formset = InvoiceLineItemFormSet(request.POST, instance=invoice)

            if formset.is_valid():
                # Save the line items
                formset.save()

                messages.success(request, 'Invoice created successfully.')
                return redirect('dashboard')
            else:
                messages.error(request, 'There was an error with the line items. Please review the form.')
        else:
            messages.error(request, 'There was an error with the invoice form. Please review the form.')

    else:
        invoice_form = InvoiceForm()
        formset = InvoiceLineItemFormSet()

    context = {
        'invoice_form': invoice_form,
        'formset': formset,
    }
    return render(request, 'create_invoice.html', context)


@superuser_required
def generate_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    logo_path = finders.find('images/logo.png')
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, 'rb') as logo_file:
            encoded_logo = base64.b64encode(logo_file.read()).decode('utf-8')
    else:
        encoded_logo = ''

    html_content = render_to_string('invoice_pdf_template.html', {
        'invoice': invoice,
        'encoded_logo': encoded_logo,
    })

    pdf_file = HTML(
        string=html_content,
        base_url=request.build_absolute_uri('/')
    ).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    return response

@superuser_required
def view_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    logo_path = finders.find('images/logo.png')
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, 'rb') as logo_file:
            encoded_logo = base64.b64encode(logo_file.read()).decode('utf-8')
    else:
        encoded_logo = ''

    html_content = render_to_string('invoice_pdf_template.html', {
        'invoice': invoice,
        'encoded_logo': encoded_logo,
    })

    pdf_file = HTML(
        string=html_content,
        base_url=request.build_absolute_uri('/')
    ).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="invoice_{invoice.invoice_number}.pdf"'
    return response

@superuser_required
def send_invoice_email(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    logo_path = finders.find('images/logo.png')
    if logo_path and os.path.exists(logo_path):
        try:
            with open(logo_path, 'rb') as logo_file:
                encoded_logo = base64.b64encode(logo_file.read()).decode('utf-8')
        except Exception as e:
            messages.error(request, f"Error encoding logo: {e}")
            encoded_logo = ''
    else:
        encoded_logo = ''
        messages.warning(request, "Logo not found, continuing without it.")
    
    # Extract the first name from the client's name
    client_name_parts = invoice.client.name.split()
    first_name = client_name_parts[0] if client_name_parts else invoice.client.name

    # Add the first name and other context
    context = {
        'invoice': invoice,
        'encoded_logo': encoded_logo,
        'first_name': first_name,
    }

    try:
        html_content = render_to_string('invoice_pdf_template.html', context)
        pdf_file = HTML(string=html_content).write_pdf()
    except Exception as e:
        messages.error(request, f"Error generating PDF: {e}")
        return redirect('dashboard')

    email_body = render_to_string('invoice_email_template.html', context)

    try:
        # Get the current month for the email subject
        current_month = datetime.now().strftime('%B')

        email = EmailMessage(
            subject=f'{current_month} Invoice',
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[invoice.client.email],
        )
        email.content_subtype = 'html'
        email.attach(f'Invoice_{invoice.invoice_number}.pdf', pdf_file, 'application/pdf')
        email.send()

        messages.success(request, f'Invoice #{invoice.invoice_number} has been sent to {invoice.client.email}.')
    except Exception as e:
        messages.error(request, f"Failed to send email: {e}")

    return redirect('dashboard')


@superuser_required
def invoice_detail(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    context = {
        'invoice': invoice
    }
    return render(request, 'invoice_detail.html', context)


@superuser_required
def invoice_edit(request, id):
    invoice = get_object_or_404(Invoice, id=id)  # Get the invoice or return 404

    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceLineItemFormSet(request.POST, instance=invoice)

        if invoice_form.is_valid() and formset.is_valid():
            try:
                # Save the updated invoice and its line items
                invoice_form.save()
                formset.save()  # Automatically handles add, update, and delete for line items

                messages.success(request, 'Invoice updated successfully.')
                return redirect('invoices:invoice_detail', id=invoice.id)
            except Exception as e:
                # Log the error for debugging
                print(f"Error saving invoice: {e}")
                messages.error(request, 'An error occurred while updating the invoice. Please try again.')
        else:
            # Debugging: Log form errors for troubleshooting
            if not invoice_form.is_valid():
                print("Invoice Form Errors:", invoice_form.errors)
            if not formset.is_valid():
                print("Formset Errors:", formset.errors)

            messages.error(request, 'There were errors in the form. Please review and try again.')
    else:
        # For GET requests, prepopulate the form and formset with the existing data
        invoice_form = InvoiceForm(instance=invoice)
        formset = InvoiceLineItemFormSet(instance=invoice)

    context = {
        'invoice_form': invoice_form,
        'formset': formset,
        'invoice': invoice,
    }
    return render(request, 'invoice_edit.html', context)


@superuser_required
def invoice_delete(request, id):
    invoice = get_object_or_404(Invoice, id=id)

    if request.method == 'POST':
        client = invoice.client  # Get the client associated with the invoice

        try:
            invoice.delete()  # Delete the invoice

            # Recalculate the current invoice number based on existing invoices
            max_invoice_number = client.invoices.aggregate(Max('invoice_number'))['invoice_number__max']

            if max_invoice_number:
                try:
                    # Ensure max_invoice_number is an integer
                    max_invoice_number = int(max_invoice_number)
                    client.current_invoice_number = max_invoice_number + 1
                except ValueError:
                    # Handle non-integer max_invoice_number gracefully
                    print(f"DEBUG: Non-integer max_invoice_number '{max_invoice_number}' encountered.")
                    client.current_invoice_number = 1
            else:
                # If no invoices remain, reset the current invoice number
                client.current_invoice_number = 1

            # Save the updated current invoice number
            client.save(update_fields=['current_invoice_number'])

            # Debugging: Log the successful update
            print(f"DEBUG: Updated current_invoice_number for client {client.id}: {client.current_invoice_number}")

            messages.success(request, f"Invoice #{invoice.invoice_number} has been deleted.")
        except Exception as e:
            # Handle unexpected errors gracefully
            print(f"ERROR: Failed to delete invoice {invoice.id}: {e}")
            messages.error(request, f"An error occurred while deleting Invoice #{invoice.invoice_number}. Please try again.")

        return redirect('dashboard')

    return render(request, 'invoice_delete_confirm.html', {'invoice': invoice})


@superuser_required
def client_list(request):
    query = request.GET.get('q', '')
    clients = Client.objects.all()

    if query:
        clients = clients.filter(
            Q(name__icontains=query) | 
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(city__icontains=query)
        )

    paginator = Paginator(clients, 20)  # Show 20 clients per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'client_list.html', context)


@superuser_required
def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client added successfully.')
            return redirect('invoices:client_list')  # Redirect to client list after adding
    else:
        form = ClientForm()
    return render(request, 'create_client.html', {'form': form})


@superuser_required
def edit_client(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, f'Client "{client.name}" has been updated successfully.')
            return redirect('invoices:client_list')  # Redirect back to the client list
        else:
            messages.error(request, 'There were errors in the form. Please correct them.')
    else:
        form = ClientForm(instance=client)

    context = {
        'form': form,
        'client': client,
    }
    return render(request, 'edit_client.html', context)


@superuser_required
def delete_client(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        client.delete()
        messages.success(request, f"Client {client.name} has been deleted.")
        return redirect('invoices:client_list')

    return render(request, 'delete_client.html', {'client': client})


@superuser_required
def dog_list(request):
    # Get all dogs with their related client data
    dogs = Dog.objects.select_related('client').all()
    
    # Paginate the dogs (20 dogs per page)
    paginator = Paginator(dogs, 20)  # Change '10' to the number of dogs you want per page
    page_number = request.GET.get('page', 1)  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the current page

    return render(request, 'dog_list.html', {'page_obj': page_obj})


@superuser_required
def create_dog(request):
    if request.method == 'POST':
        form = DogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dog created successfully.')
            return redirect('invoices:dog_list')
    else:
        form = DogForm()
    return render(request, 'create_dog.html', {'form': form})


@superuser_required
def edit_dog(request, id):
    dog = get_object_or_404(Dog, id=id)
    if request.method == 'POST':
        form = DogForm(request.POST, instance=dog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dog updated successfully.')
            return redirect('invoices:dog_list')
    else:
        form = DogForm(instance=dog)
    return render(request, 'edit_dog.html', {'form': form, 'dog': dog})


@superuser_required
def delete_dog(request, id):
    dog = get_object_or_404(Dog, id=id)
    if request.method == 'POST':
        dog.delete()
        messages.success(request, f'Dog {dog.name} has been deleted.')
        return redirect('invoices:dog_list')
    return render(request, 'delete_dog.html', {'dog': dog})

@superuser_required
@csrf_exempt
def counter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')

            if action == 'reset':
                # Reset all dogs' weekly walks to 0
                Dog.objects.update(weekly_walks=0)
                return JsonResponse({'success': True})

            # Other actions (increment, decrement, manual)
            dog_id = data.get('dog_id')
            dog = Dog.objects.filter(id=dog_id).first()
            if not dog:
                return JsonResponse({'success': False, 'error': 'Dog not found'})

            if action == 'increment':
                dog.weekly_walks += 1
            elif action == 'decrement' and dog.weekly_walks > 0:
                dog.weekly_walks -= 1
            elif action == 'manual':
                value = int(data.get('value', 0))
                dog.weekly_walks = max(0, value)

            dog.save()
            return JsonResponse({'success': True, 'weekly_walks': dog.weekly_walks})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    # GET request: Render the counter template
    dogs = Dog.objects.annotate(lower_name=Lower('name')).order_by('lower_name')
    return render(request, 'counter.html', {'dogs': dogs})